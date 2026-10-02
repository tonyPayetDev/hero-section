#!/usr/bin/env python3
"""VSL ShortForge - place the cloned VO lines on the 120 BPM grid -> voice.wav + vo.json.

Each line starts on its scene's beat (never before), is sped up (atempo <= 1.15) only
if it would spill into the next scene, and is transcribed word by word so every slam
lands on the word as it is said, never ahead of it.

  python3 vo.py VO_DIR OUT_DIR      (VO_DIR/ia/iaNN.mp3 from the tts-gen webhook, VO_DIR/lines.json)
"""
import json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or shutil.which("ffprobe") or "ffprobe"
SR, T = 48000, 32.0
vo, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
lines = json.load(open(os.path.join(vo, "lines.json")))
# (start, latest end) per line, video seconds - scenes of STORYBOARD.md, countdown on beats 26/26.5/27
SLOT = [(1.0, 3.9), (4.05, 5.9), (6.0, 9.95), (10.1, 11.9), (12.1, 13.9), (13.95, 16.0), (16.05, 17.95),
        (18.05, 19.95), (20.05, 21.95), (22.0, 23.75), (23.8, 25.75), (26.0, 26.45), (26.5, 26.95),
        (27.0, 27.4), (28.0, 28.9)]
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())


from faster_whisper import WhisperModel  # noqa: E402
model = WhisperModel("medium", device="cpu", compute_type="int8")
parts, items = [], []
for L, (a, b) in zip(lines, SLOT):
    src = os.path.join(vo, "ia", f"ia{L['li']:02d}.mp3")
    raw = os.path.join(out, f"l{L['li']:02d}_raw.wav")
    subprocess.run([FF, "-nostdin", "-v", "error", "-i", src, "-af", TRIM, "-ar", str(SR), "-ac", "1", raw, "-y"], check=True)
    d = dur(raw)
    tempo = min(1.15, max(1.0, d / (b - a)))
    fin = os.path.join(out, f"l{L['li']:02d}.wav")
    subprocess.run([FF, "-nostdin", "-v", "error", "-i", raw, "-af", f"atempo={tempo:.4f}", fin, "-y"], check=True)
    d2 = dur(fin)
    segs, _ = model.transcribe(fin, language="fr", word_timestamps=True, initial_prompt=L["text"], condition_on_previous_text=False)
    words = [{"w": w.word.strip(), "s": round(a + w.start, 3), "e": round(a + w.end, 3)} for s in segs for w in s.words]
    items.append({"li": L["li"], "text": L["text"], "start": a, "end": round(a + d2, 3), "tempo": round(tempo, 3), "words": words})
    parts.append((a, fin))
    print(f"l{L['li']:02d} {a:6.2f} -> {a + d2:6.2f} (x{tempo:.2f})  {' '.join(w['w'] + '@' + format(w['s'], '.2f') for w in words)}")
ins = sum((["-i", p] for _, p in parts), [])
flt = ";".join(f"[{k}:a]adelay={int(round(a * 1000))}[d{k}]" for k, (a, _) in enumerate(parts))
flt += ";" + "".join(f"[d{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{T}[v]"
subprocess.run([FF, "-nostdin", "-v", "error", *ins, "-filter_complex", flt, "-map", "[v]", "-ar", str(SR), "-ac", "1",
                os.path.join(out, "voice.wav"), "-y"], check=True)
json.dump(items, open(os.path.join(out, "vo.json"), "w"), ensure_ascii=False, indent=1)
print("voice.wav + vo.json")

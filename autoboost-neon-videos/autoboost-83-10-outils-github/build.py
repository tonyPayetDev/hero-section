#!/usr/bin/env python3
"""autoboost-83 - « 10 outils GitHub », Tony (real take) vs Tony IA, every line in his cloned voice (copied from autoboost-80).

  voice.wav + vo.json   the 15 lines end to end (cloned voice, tts-gen webhook = WaveSpeed clone);
                        IA lines get a light « machine » colour (pitch +1 st, short slapback) so the
                        two voices read apart; word timings by faster-whisper
  tony_src.mp4          1080x1440, the real take (video_25), muted: talking passages under Tony's
                        lines, silent ones (he listens) under the IA's lines and the gaps
                        (v1, superseded by resync.py, which matches the take to the voice's rhythm)
  avatar.mp4            600x600, the BUREAU avatar: lips-active ranges under IA lines, still otherwise
  bed.wav               Deep Urban from its drop (file 14.258 s) (v1, superseded by bed_valse.py)

  python3 build.py TAKE.mp4 TAKE_TRANSCRIPT.json VO_DIR OUT_DIR
"""
import json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or FF.replace("ffmpeg", "ffprobe")
HERE = os.path.dirname(os.path.abspath(__file__))
SH = os.path.abspath(os.path.join(HERE, "..", "_shared"))
FPS, SR = 30, 48000
take, tt, vo, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
LINES = json.load(open(os.path.join(HERE, "session", "script.json")))["lines"]
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
IA_FX = "asetrate=48000*1.06,aresample=48000,atempo=0.9434,aecho=0.8:0.5:14:0.22,highpass=f=140"


def ff(*a):
    subprocess.run([FF, "-nostdin", "-v", "error", *a, "-y"], check=True)


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())


# ------------------------------------------------------------------ voice: lines end to end
from faster_whisper import WhisperModel  # noqa: E402
model = WhisperModel("medium", device="cpu", compute_type="int8")
items, t = [], 0.12
for i, (who, text) in enumerate(LINES):
    raw, fin = os.path.join(out, f"l{i:02d}_raw.wav"), os.path.join(out, f"l{i:02d}.wav")
    ff("-i", os.path.join(vo, f"l{i:02d}.mp3"), "-af", "aresample=48000," + TRIM, "-ar", str(SR), "-ac", "1", raw)
    fx = IA_FX if who == "ia" else "atempo=1.04"
    ff("-i", raw, "-af", fx, "-ar", str(SR), "-ac", "1", fin)
    d = dur(fin)
    segs, _ = model.transcribe(fin, language="fr", word_timestamps=True, initial_prompt=text, condition_on_previous_text=False)
    words = []
    for s in segs:
        for w in s.words:
            x = {"w": w.word.strip(), "s": round(t + w.start, 3), "e": round(t + w.end, 3)}
            if words and x["w"][:1] in ("-", "'"):
                words[-1]["w"] += x["w"]; words[-1]["e"] = x["e"]
            else:
                words.append(x)
    items.append({"li": i, "who": who, "text": text, "start": round(t, 3), "end": round(t + d, 3), "words": words})
    print(f"{i:02d} {who:3s} {t:6.2f} -> {t + d:6.2f}  {text}", flush=True)
    # comic timing: a beat after each IA punchline, a quick reply after « Pas Teams » style lines
    t += d + (0.32 if who == "ia" else 0.16)
TOTAL = round(t + 1.6, 3)                     # + the CTA held
NF = round(TOTAL * FPS)
flt = ";".join(f"[{k}:a]adelay={int(round(it['start'] * 1000))}[d{k}]" for k, it in enumerate(items))
flt += ";" + "".join(f"[d{k}]" for k in range(len(items))) + f"amix=inputs={len(items)}:normalize=0:duration=longest,apad=whole_dur={TOTAL}[v]"
ff(*sum((["-i", os.path.join(out, f"l{k:02d}.wav")] for k in range(len(items))), []), "-filter_complex", flt, "-map", "[v]",
   "-t", str(TOTAL), "-ar", str(SR), "-ac", "1", os.path.join(out, "voice.wav"))
json.dump({"total": TOTAL, "lines": items}, open(os.path.join(out, "vo.json"), "w"), ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ IA avatar: lips move only on IA lines
CLIPS = os.path.join(SH, "avatar-bank", "clips")
LIPS = [("B1_principe", 0.08, 4.88), ("C2_commente_motcle", 0.08, 4.83), ("A1_hook_frontal", 0.67, 4.58)]
VF = "crop=720:720:0:40,scale=600:600,fps=30,format=yuv420p"
segs, rot, k = [], 0, 0
still = os.path.join(out, "av_still.png")
ff("-ss", "0.05", "-i", os.path.join(CLIPS, "B1_principe.mp4"), "-vf", "crop=720:720:0:40,scale=600:600", "-frames:v", "1", still)


def av_seg(args, n):
    global k
    p = os.path.join(out, f"av{k:03d}.mp4"); k += 1
    ff(*args, "-frames:v", str(n), "-c:v", "libx264", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p", p)
    segs.append(p)
    return p


cur = 0
for it in [x for x in items if x["who"] == "ia"]:
    a, b = round(it["start"] * FPS), round(it["end"] * FPS)
    if a > cur:
        av_seg(["-loop", "1", "-i", still, "-vf", "fps=30,format=yuv420p"], a - cur)
    left = b - a
    while left > 0:
        name, s0, s1 = LIPS[rot % 3]; rot += 1
        n = min(left, int((s1 - s0) * FPS))
        p = av_seg(["-ss", f"{s0:.3f}", "-i", os.path.join(CLIPS, name + ".mp4"), "-an", "-vf", VF], n)
        left -= n
        ff("-sseof", "-0.05", "-i", p, "-frames:v", "1", "-update", "1", still)
    cur = b
if cur < NF:
    av_seg(["-loop", "1", "-i", still, "-vf", "fps=30,format=yuv420p"], NF - cur)
open(os.path.join(out, "av.txt"), "w").write("".join(f"file '{p}'\n" for p in segs))
ff("-f", "concat", "-safe", "0", "-i", os.path.join(out, "av.txt"), "-c:v", "libx264", "-crf", "18", "-g", "30", "-keyint_min", "30",
   "-pix_fmt", "yuv420p", "-frames:v", str(NF), "-movflags", "+faststart", os.path.join(out, "avatar.mp4"))

print(f"done: {NF} frames, {TOTAL} s")

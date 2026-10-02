#!/usr/bin/env python3
"""autoboost-80 - « Claude monte comme un pro », Tony (real take) vs Tony IA, every line in his cloned voice.

  voice.wav + vo.json   the 15 lines end to end (cloned voice, tts-gen webhook = WaveSpeed clone);
                        IA lines get a light « machine » colour (pitch +1 st, short slapback) so the
                        two voices read apart; word timings by faster-whisper
  tony_src.mp4          1080x1440, the real take (video_25), muted: talking passages under Tony's
                        lines, silent ones (he listens) under the IA's lines and the gaps
  avatar.mp4            600x600, the BUREAU avatar: lips-active ranges under IA lines, still otherwise
  bed.wav               Deep Urban from its drop (file 14.258 s)

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
    ff("-i", os.path.join(vo, "ia", f"ia{i:02d}.mp3"), "-af", TRIM, "-ar", str(SR), "-ac", "1", raw)
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


# ------------------------------------------------------------------ Tony: talk under his lines, listening under the IA's
def runs(words, total, gap=0.3):
    talk = []
    for w in words:
        if talk and w["s"] - talk[-1][1] < gap:
            talk[-1][1] = w["e"]
        else:
            talk.append([w["s"], w["e"]])
    sil, cur = [], 0.0
    for a, b in talk:
        if a - cur >= 0.5:
            sil.append([cur + 0.1, a - 0.1])
        cur = b
    if total - cur >= 0.5:
        sil.append([cur + 0.1, total - 0.05])
    return talk, sil


tj = json.load(open(tt))
tw = [w for s in (tj if isinstance(tj, list) else tj["segments"]) for w in s["words"]]
talk, sil = runs(tw, dur(take))
pools = {"talk": [[round(a * FPS) + 2, round(b * FPS) - 2] for a, b in talk if b - a > 0.5],
         "sil": [[round(a * FPS), round(b * FPS)] for a, b in sil]}
marks = [(0, "sil")]
for it in items:
    marks += [(round(it["start"] * FPS), "talk" if it["who"] == "moi" else "sil"), (round(it["end"] * FPS), "sil")]
marks.append((NF, "end"))
marks = sorted(set(marks), key=lambda m: m[0])
ptr = {"talk": [0, None], "sil": [0, None]}
chunks, cuts = [], []
for (fa, kind), (fb, _) in zip(marks, marks[1:]):
    need = fb - fa
    while need > 0:
        i, pos = ptr[kind]
        run = pools[kind][i % len(pools[kind])]
        pos = run[0] if pos is None else pos
        n = min(need, run[1] - pos)
        if n <= 0:
            ptr[kind] = [i + 1, None]; continue
        cuts.append(round((fb - need) / FPS, 3))
        chunks.append((pos, n))
        need -= n
        ptr[kind] = [i, pos + n] if pos + n < run[1] else [i + 1, None]
files = []
for k, (pos, n) in enumerate(chunks):
    f = os.path.join(out, f"t{k:03d}.mp4")
    ff("-ss", f"{pos / FPS:.4f}", "-i", take, "-an", "-vf", "fps=30", "-frames:v", str(n), "-c:v", "libx264", "-crf", "16",
       "-preset", "veryfast", "-pix_fmt", "yuv420p", "-video_track_timescale", "30000", f)
    files.append(f)
open(os.path.join(out, "t.txt"), "w").write("".join(f"file '{f}'\n" for f in files))
ff("-f", "concat", "-safe", "0", "-i", os.path.join(out, "t.txt"), "-c:v", "libx264", "-crf", "16", "-g", "30", "-pix_fmt", "yuv420p",
   "-frames:v", str(NF), os.path.join(out, "tony_src.mp4"))
json.dump({"frames": NF, "cuts": cuts}, open(os.path.join(out, "tony_cuts.json"), "w"))

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

# ------------------------------------------------------------------ bed: Deep Urban from its drop, +16 dB on the voiceless CTA hold
last = items[-1]["end"]
ff("-ss", "14.258", "-t", f"{TOTAL}", "-i", os.path.join(SH, "bgm", "food-deep-urban-122.mp3"),
   "-af", f"volume='if(gt(t,{last + 0.1:.2f}),6.3,1)':eval=frame,afade=t=in:d=0.03,afade=t=out:st={TOTAL - 0.7:.2f}:d=0.7",
   "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", os.path.join(out, "bed.wav"))
print(f"done: {NF} frames, {TOTAL} s, {len(chunks)} take chunks")

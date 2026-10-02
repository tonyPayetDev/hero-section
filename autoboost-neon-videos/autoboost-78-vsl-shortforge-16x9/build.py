#!/usr/bin/env python3
"""VSL ShortForge 16:9 (v2) - every media track of the composition, frame-exact.

  voice.wav      the cloned VO lines, each on its beat of Deep Urban (124 BPM measured,
                 bar 1.9356 s), atempo <= 1.15 only if a line would spill; vo.json has
                 the word timings (faster-whisper) so slams never precede the voice
  avatar.mp4     600x600, Tony's BUREAU avatar: lips-active ranges (LIPS-MAP.md) while a
                 line is spoken, a still frame in between - the mouth never moves on silence
  ex0..ex4.mp4   360x640, real videos made with the pipeline, playing only in their window
                 (first frame held before, last frame after), muted
  bed.wav        Deep Urban, file 45.227 s (a downbeat) -> +44.52 s: full groove, the
                 breakdown lands at video 29.03, the re-drop at 38.71 (« Action ! »)

  python3 build.py VO_DIR OUT_DIR       (VO_DIR/ia/iaNN.mp3 + VO_DIR/lines.json)
"""
import json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or shutil.which("ffprobe") or "ffprobe"
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.abspath(os.path.join(HERE, ".."))
SH = os.path.join(V, "_shared")
FPS, SR = 30, 48000
BEAT, BAR = 0.48389, 1.93556
TOTAL = round(23 * BAR, 3)            # 44.518 s = 23 bars
NF = round(TOTAL * FPS)
vo, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)

# line index (lines.json "li") -> (start, latest end), video seconds
SLOT = [(0, 0.40, 1.90), (1, 1.94, 3.80), (2, 3.95, 9.40), (3, 9.75, 11.0), (15, 11.1, 13.4),
        (4, 13.62, 15.3), (5, 15.48, 18.0), (6, 19.36, 21.3), (7, 23.3, 25.1), (16, 25.2, 28.9),
        (17, 29.2, 36.9), (11, 37.26, 37.70), (12, 37.74, 38.18), (13, 38.23, 38.62), (14, 38.71, 39.30),
        (10, 39.45, 41.8)]
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"


def ff(*a):
    subprocess.run([FF, "-nostdin", "-v", "error", *a, "-y"], check=True)


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())


# ------------------------------------------------------------------ voice
lines = {L["li"]: L for L in json.load(open(os.path.join(vo, "lines.json")))}
from faster_whisper import WhisperModel  # noqa: E402
model = WhisperModel("medium", device="cpu", compute_type="int8")
items, parts = [], []
for li, a, b in SLOT:
    raw, fin = os.path.join(out, f"l{li:02d}_raw.wav"), os.path.join(out, f"l{li:02d}.wav")
    ff("-i", os.path.join(vo, "ia", f"ia{li:02d}.mp3"), "-af", TRIM, "-ar", str(SR), "-ac", "1", raw)
    tempo = min(1.15, max(1.0, dur(raw) / (b - a)))
    ff("-i", raw, "-af", f"atempo={tempo:.4f}", fin)
    d = dur(fin)
    segs, _ = model.transcribe(fin, language="fr", word_timestamps=True, initial_prompt=lines[li]["text"],
                               condition_on_previous_text=False)
    words = [{"w": w.word.strip(), "s": round(a + w.start, 3), "e": round(a + w.end, 3)} for s in segs for w in s.words]
    items.append({"li": li, "text": lines[li]["text"], "start": a, "end": round(a + d, 3), "tempo": round(tempo, 3), "words": words})
    parts.append((a, fin))
    print(f"l{li:02d} {a:6.2f} -> {a + d:6.2f} x{tempo:.2f}  {lines[li]['text']}")
flt = ";".join(f"[{k}:a]adelay={int(round(a * 1000))}[d{k}]" for k, (a, _) in enumerate(parts))
flt += ";" + "".join(f"[d{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0:duration=longest,apad=whole_dur={TOTAL}[v]"
ff(*sum((["-i", p] for _, p in parts), []), "-filter_complex", flt, "-map", "[v]", "-t", f"{TOTAL}", "-ar", str(SR), "-ac", "1", os.path.join(out, "voice.wav"))
json.dump({"total": TOTAL, "beat": BEAT, "bar": BAR, "lines": items}, open(os.path.join(out, "vo.json"), "w"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ avatar: lips move only while a line is spoken
CLIPS = os.path.join(SH, "avatar-bank", "clips")
LIPS = [("B1_principe", 0.08, 4.88), ("C2_commente_motcle", 0.08, 4.83), ("A1_hook_frontal", 0.67, 4.58)]
AV = "crop=720:720:0:40,scale=600:600,fps=30,format=yuv420p"
segs, f0, rot, still = [], 0, 0, None
spans = sorted((round(it["start"] * FPS), round(it["end"] * FPS)) for it in items)
merged = []
for a, b in spans:  # lines closer than 6 frames are one speaking span
    if merged and a - merged[-1][1] < 6:
        merged[-1][1] = max(merged[-1][1], b)
    else:
        merged.append([a, b])
k = 0


def seg_still(n):
    global k
    p = os.path.join(out, f"av{k:03d}.mp4"); k += 1
    ff("-loop", "1", "-i", still, "-vf", "fps=30,format=yuv420p", "-frames:v", str(n), "-c:v", "libx264", "-crf", "18", "-g", "30", p)
    segs.append(p)


def seg_talk(n):
    global k, rot, still
    left = n
    while left > 0:
        name, s0, s1 = LIPS[rot % 3]; rot += 1
        take = min(left, int((s1 - s0) * FPS))
        p = os.path.join(out, f"av{k:03d}.mp4"); k += 1
        ff("-ss", f"{s0:.3f}", "-i", os.path.join(CLIPS, name + ".mp4"), "-an", "-vf", AV, "-frames:v", str(take),
           "-c:v", "libx264", "-crf", "18", "-g", "30", p)
        segs.append(p); left -= take
        still = os.path.join(out, "still.png")
        ff("-sseof", "-0.05", "-i", p, "-frames:v", "1", "-update", "1", still)


still = os.path.join(out, "still.png")
ff("-ss", "0.05", "-i", os.path.join(CLIPS, "B1_principe.mp4"), "-vf", "crop=720:720:0:40,scale=600:600", "-frames:v", "1", still)
cur = 0
for a, b in merged:
    if a > cur:
        seg_still(a - cur)
    seg_talk(b - a)
    cur = b
if cur < NF:
    seg_still(NF - cur)
lst = os.path.join(out, "av.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
ff("-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "18", "-g", "30", "-keyint_min", "30",
   "-pix_fmt", "yuv420p", "-frames:v", str(NF), "-movflags", "+faststart", os.path.join(out, "avatar.mp4"))

# ------------------------------------------------------------------ examples: real renders, each playing in its window
EX = [("autoboost-61-debunk-10k-freelance/video.mp4", 8.0, 19.2, 23.4),     # the phone of step 3
      ("autoboost-62-claude-sonnet-5/video.mp4", 10.0, 23.1, 29.2),
      ("autoboost-63-zapier-vers-n8n/video.mp4", 0.0, 23.1, 29.2),
      ("autoboost-10-livres-enfants/renders/public_2026-07-09_16-55-14.mp4", 12.0, 23.1, 29.2)]
for i, (src, s0, a, b) in enumerate(EX):
    fa, fb = round(a * FPS), round(b * FPS)
    ff("-ss", f"{s0:.3f}", "-i", os.path.join(V, src), "-an",
       "-vf", f"fps=30,scale=360:640,trim=end_frame={fb - fa},tpad=start_mode=clone:start={fa}:stop_mode=clone:stop={NF - fb},format=yuv420p",
       "-frames:v", str(NF), "-c:v", "libx264", "-crf", "20", "-g", "30", "-keyint_min", "30", "-movflags", "+faststart",
       os.path.join(out, f"ex{i}.mp4"))

# ------------------------------------------------------------------ bed: Deep Urban, start_gain -22.4 (manifest), +16 dB on the voiceless CTA hold, +6 dB on « Action ! »
ff("-ss", "45.227", "-t", f"{TOTAL}", "-i", os.path.join(SH, "bgm", "food-deep-urban-122.mp3"),
   "-af", "volume='if(between(t,41.9,44.6),6.3,if(between(t,38.71,39.40),2.0,1))':eval=frame,afade=t=in:d=0.05,afade=t=out:st=43.5:d=1.0",
   "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", os.path.join(out, "bed.wav"))
print(f"voice.wav vo.json avatar.mp4 ex0-4.mp4 bed.wav - {NF} frames, {TOTAL} s")

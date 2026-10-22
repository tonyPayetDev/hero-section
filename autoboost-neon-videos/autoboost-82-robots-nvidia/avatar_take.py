#!/usr/bin/env python3
"""autoboost-82 - build a « face cam » take from the VOITURE avatar bank + the cloned voice lines.

The avatar's lips move only under the voice: each line is filled with the bank's lips-active windows
(lips-map-d.json), the gaps between lines with a still moment. The result (1080x1920, voice included) is a
normal talking-head video, so AutoBoost Studio can dress it in any style.

  python3 avatar_take.py session/remake.json VOICE_DIR OUT.mp4
      VOICE_DIR holds l00.mp3, l01.mp3… (one per line, cloned voice)
"""
import json, os, shutil, subprocess, sys, tempfile

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or FF.replace("ffmpeg", "ffprobe")
HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, "..", "_shared", "avatar-bank")
FPS, SR = 30, 48000
IA_FX = "asetrate=48000*1.06,aresample=48000,atempo=0.9434,aecho=0.8:0.5:14:0.22,highpass=f=140"   # the IA's « machine » colour
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
script, vdir, out = sys.argv[1:4]
lines = json.load(open(script))["lines"]
lips = json.load(open(os.path.join(BANK, "lips-map-d.json")))["clips"]
ORDER = ["D1_hook_frontal.mp4", "D2_insistance_doigts.mp4", "D4_relance_barbe.mp4", "D3_cta_lunettes.mp4"]
talk = [(c, w["start"], w["end"]) for k in range(2) for c in ORDER for w in lips[c]["active"][k:k + 1]]
rest = [(c, lips[c]["active"][0]["end"] + 0.05, lips[c]["active"][1]["start"] - 0.05) for c in ORDER if len(lips[c]["active"]) > 1]
tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(out)))


def ff(*a):
    subprocess.run([FF, "-nostdin", "-v", "error", *a, "-y"], check=True)


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())


# ---- voice: lines end to end, the IA lines coloured
wavs, t, plan = [], 0.15, []
for i, (who, text, *_) in enumerate(lines):
    w = os.path.join(tmp, f"v{i:02d}.wav")
    ff("-i", os.path.join(vdir, f"l{i:02d}.mp3"), "-af", "aresample=48000," + TRIM + ("," + IA_FX if who == "ia" else ""), "-ar", str(SR), "-ac", "1", w)
    d = dur(w)
    plan.append((t, d, who)); wavs.append(w)
    t += d + (0.35 if who == "ia" else 0.2)
total = round(t + 0.6, 3)
flt = ";".join(f"[{k}:a]adelay={int(round(p[0] * 1000))}[d{k}]" for k, p in enumerate(plan))
flt += ";" + "".join(f"[d{k}]" for k in range(len(plan))) + f"amix=inputs={len(plan)}:normalize=0:duration=longest,apad=whole_dur={total}[a]"
voice = os.path.join(tmp, "voice.wav")
ff(*sum((["-i", w] for w in wavs), []), "-filter_complex", flt, "-map", "[a]", "-t", str(total), "-ar", str(SR), "-ac", "1", voice)

# ---- picture: lips-active windows under the lines, a still moment in the gaps
segs, ti, ri, cur = [], 0, 0, 0.0


def piece(clip, a, n):
    p = os.path.join(tmp, f"p{len(segs):03d}.mp4")
    ff("-ss", f"{a:.3f}", "-i", os.path.join(BANK, "clips-new", clip), "-an", "-frames:v", str(n),
       "-vf", "fps=30,scale=1080:1920:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", p)
    segs.append(p)


def fill(sec, pool, idx):
    n_left = round(sec * FPS)
    while n_left > 0:
        clip, a, b = pool[idx % len(pool)]
        n = min(n_left, int((b - a) * FPS))
        piece(clip, a, n)
        n_left -= n; idx += 1
    return idx


for (a, d, who) in plan:
    if a > cur:
        ri = fill(a - cur, rest, ri)
    ti = fill(d, talk, ti)
    cur = a + d
if total > cur:
    fill(total - cur, rest, ri)
lst = os.path.join(tmp, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
ff("-f", "concat", "-safe", "0", "-i", lst, "-i", voice, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
   "-c:a", "aac", "-b:a", "192k", "-t", str(total), out)
shutil.rmtree(tmp)
print(f"{out}: {total} s, {len(plan)} lines, {len(segs)} avatar pieces")

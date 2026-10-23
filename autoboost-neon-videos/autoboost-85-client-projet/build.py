#!/usr/bin/env python3
"""autoboost-85 - « Quand le client décrit son projet » : Tony's lip-sync take (never cut), Tony IA on freeze frames.

  base.mp4      1080x1920 @ 30 fps: the take's passages from session/edit.json, a freeze frame under every IA line
  tony.wav      the take's own sound on its passages, silence on the freezes
  ia.wav        the IA lines (cloned voice + « machine » colour) on their freezes
  avatar.mp4    600x600 BUREAU avatar, lips-active only under IA lines (same bank as autoboost-80/83/84)
  vo.json       {total, lines: [{who, start, end, text, words, tag}], cuts: [...]}  (same shape as autoboost-84)

  python3 build.py TAKE.mp4 IA_VO_DIR OUT_DIR          IA_VO_DIR: l00.mp3… one per IA item, in order
"""
import json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or FF.replace("ffmpeg", "ffprobe")
HERE = os.path.dirname(os.path.abspath(__file__))
SH = os.path.abspath(os.path.join(HERE, "..", "_shared"))
FPS, SR = 30, 48000
IA_FX = "asetrate=48000*1.06,aresample=48000,atempo=0.9434,aecho=0.8:0.5:14:0.22,highpass=f=140"
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
take, iavo, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
ITEMS = json.load(open(os.path.join(HERE, "session", "edit.json")))["items"]
VF = "fps=30,scale=1080:1920:flags=lanczos,format=yuv420p"


def ff(*a):
    subprocess.run([FF, "-nostdin", "-v", "error", *a, "-y"], check=True)


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())


def spread(text, a, b, t0):
    """words of a hand-corrected line spread over its Whisper span by syllable weight"""
    toks = text.split()
    wts = [max(1, sum(c in "aeiouyéèêàâîôûAEIOUYÉ" for c in w)) for w in toks]
    step, s, ws = (b - a) / sum(wts), a, []
    for w, k in zip(toks, wts):
        ws.append({"w": w, "s": round(t0 + s, 3), "e": round(t0 + s + k * step, 3)}); s += k * step
    return ws


parts, lines, cuts, t, ia_k, last = [], [], [], 0.0, 0, 0.0
for it in ITEMS:
    k = len(parts)
    if it["who"] == "moi":
        a, b = it["a"], it["b"]
        n = round((b - a) * FPS)
        p = os.path.join(out, f"p{k:02d}.mkv")
        ff("-ss", f"{a:.3f}", "-i", take, "-t", f"{n / FPS:.4f}", "-vf", VF, "-af", "aresample=48000,apad", "-frames:v", str(n),
           "-c:v", "libx264", "-crf", "15", "-preset", "veryfast", "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "1", "-shortest", p)
        for la, lb, text in it["lines"]:
            ws = spread(text, la - a, lb - a, t)
            lines.append({"who": "moi", "start": ws[0]["s"], "end": ws[-1]["e"], "text": text, "words": ws, "tag": it.get("tag", "")})
        cuts.append(round(t, 3)); t += n / FPS; last = b
    else:
        wav = os.path.join(out, f"ia{ia_k:02d}.wav")
        ff("-i", os.path.join(iavo, f"l{ia_k:02d}.mp3"), "-af", "aresample=48000," + TRIM + "," + IA_FX, "-ar", str(SR), "-ac", "1", wav)
        d = dur(wav)
        n = round((d + 0.5) * FPS)
        still = os.path.join(out, f"still{k:02d}.png")
        # « freeze » (edit.json): a frame where Tony is still in shot (he walks out at the very end)
        ff("-ss", f"{it.get('freeze', last - 0.05):.3f}", "-i", take, "-vf", "scale=1080:1920:flags=lanczos", "-frames:v", "1", "-update", "1", still)
        p = os.path.join(out, f"p{k:02d}.mkv")
        ff("-loop", "1", "-i", still, "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-vf", VF, "-frames:v", str(n), "-t", f"{n / FPS:.4f}",
           "-c:v", "libx264", "-crf", "15", "-preset", "veryfast", "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "1", p)
        lines.append({"who": "ia", "start": round(t + 0.2, 3), "end": round(t + 0.2 + d, 3), "text": it["text"], "wav": wav, "tag": it.get("tag", "")})
        lines[-1]["words"] = spread(it["text"], 0.2, 0.2 + d, t)
        cuts.append(round(t, 3)); t += n / FPS; ia_k += 1
    parts.append(p)
TOTAL = round(t + 1.6, 3)                                    # + a hold on the last frame (outro card readable)
NF = round(TOTAL * FPS)
lst = os.path.join(out, "parts.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
ff("-f", "concat", "-safe", "0", "-i", lst, "-vf", "tpad=stop_mode=clone:stop_duration=3", "-frames:v", str(NF),
   "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-g", "30", "-pix_fmt", "yuv420p", "-an", os.path.join(out, "base.mp4"))
ff("-f", "concat", "-safe", "0", "-i", lst, "-vn", "-af", f"apad=whole_dur={TOTAL}", "-t", str(TOTAL), "-ar", str(SR), "-ac", "1",
   os.path.join(out, "tony.wav"))
ias = [ln for ln in lines if ln["who"] == "ia"]
flt = ";".join(f"[{k}:a]adelay={int(round(ln['start'] * 1000))}[d{k}]" for k, ln in enumerate(ias))
flt += ";" + "".join(f"[d{k}]" for k in range(len(ias))) + f"amix=inputs={len(ias)}:normalize=0:duration=longest,apad=whole_dur={TOTAL}[v]"
ff(*sum((["-i", ln["wav"]] for ln in ias), []), "-filter_complex", flt, "-map", "[v]", "-t", str(TOTAL), "-ar", str(SR), "-ac", "1",
   os.path.join(out, "ia.wav"))

# ------------------------------------------------------------------ IA avatar: lips move only on IA lines
CLIPS = os.path.join(SH, "avatar-bank", "clips")
LIPS = [("B1_principe", 0.08, 4.88), ("C2_commente_motcle", 0.08, 4.83), ("A1_hook_frontal", 0.67, 4.58)]
AVF = "crop=720:720:0:40,scale=600:600,fps=30,format=yuv420p"
segs, rot, kk, cur = [], 0, 0, 0
astill = os.path.join(out, "av_still.png")
ff("-ss", "0.05", "-i", os.path.join(CLIPS, "B1_principe.mp4"), "-vf", "crop=720:720:0:40,scale=600:600", "-frames:v", "1", astill)


def av_seg(args, n):
    global kk
    p = os.path.join(out, f"av{kk:03d}.mp4"); kk += 1
    ff(*args, "-frames:v", str(n), "-c:v", "libx264", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p", p)
    segs.append(p)
    return p


for ln in ias:
    a, b = round(ln["start"] * FPS), round(ln["end"] * FPS)
    if a > cur:
        av_seg(["-loop", "1", "-i", astill, "-vf", "fps=30,format=yuv420p"], a - cur)
    left = b - a
    while left > 0:
        name, s0, s1 = LIPS[rot % 3]; rot += 1
        n = min(left, int((s1 - s0) * FPS))
        p = av_seg(["-ss", f"{s0:.3f}", "-i", os.path.join(CLIPS, name + ".mp4"), "-an", "-vf", AVF], n)
        left -= n
        ff("-sseof", "-0.05", "-i", p, "-frames:v", "1", "-update", "1", astill)
    cur = b
if cur < NF:
    av_seg(["-loop", "1", "-i", astill, "-vf", "fps=30,format=yuv420p"], NF - cur)
open(os.path.join(out, "av.txt"), "w").write("".join(f"file '{p}'\n" for p in segs))
ff("-f", "concat", "-safe", "0", "-i", os.path.join(out, "av.txt"), "-c:v", "libx264", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p",
   "-frames:v", str(NF), "-movflags", "+faststart", os.path.join(out, "avatar.mp4"))

for ln in lines:
    ln.pop("wav", None)
json.dump({"total": TOTAL, "lines": lines, "cuts": cuts}, open(os.path.join(out, "vo.json"), "w"), ensure_ascii=False, indent=1)
print(f"done: {NF} frames, {TOTAL} s, {len(parts)} parts, {len(ias)} IA lines")
for ln in lines:
    print(f"  {ln['who']:3s} {ln['start']:6.2f}-{ln['end']:6.2f}  {ln['text'][:70]}")

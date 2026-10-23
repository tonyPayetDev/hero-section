#!/usr/bin/env python3
"""autoboost-84 - « Défi piment » : Tony's own take (spicy noodles), cut on his words, with Tony IA stepping in.

  base.mp4      1080x1920 @ 30 fps, the take cut on the words of every Tony segment (pauses > GAP removed);
                after a segment followed by an IA line, the next seconds of the take run muted under the IA
                (Tony keeps eating while his IA comments)
  tony.wav      Tony's own voice, on his segments only
  ia.wav        the IA lines (cloned voice + « machine » colour), on their slots
  avatar.mp4    600x600, BUREAU avatar for the circle: lips-active only under IA lines
  vo.json       {total, lines: [{who, start, end, text, words: [{w, s, e}]}], cuts: [...]}

  python3 build.py TAKE.mp4 TAKE_TRANSCRIPT.json IA_VO_DIR OUT_DIR
      TAKE_TRANSCRIPT.json: faster-whisper segments with word timings ([{s, e, t, w: [{w, s, e}]}])
      IA_VO_DIR: l00.mp3, l01.mp3… one per IA line of session/edit.json, in order
"""
import json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or FF.replace("ffmpeg", "ffprobe")
HERE = os.path.dirname(os.path.abspath(__file__))
SH = os.path.abspath(os.path.join(HERE, "..", "_shared"))
FPS, SR = 30, 48000
GAP, PAD = 0.45, 0.10                     # cut pauses longer than GAP; keep PAD around the words
IA_FX = "asetrate=48000*1.06,aresample=48000,atempo=0.9434,aecho=0.8:0.5:14:0.22,highpass=f=140"
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
take, tt, iavo, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
ITEMS = json.load(open(os.path.join(HERE, "session", "edit.json")))["items"]
WORDS = [w for s in json.load(open(tt)) for w in s["w"]]


def ff(*a):
    subprocess.run([FF, "-nostdin", "-v", "error", *a, "-y"], check=True)


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())


# ------------------------------------------------------------------ plan: (raw_a, raw_b, mute) pieces in output order
pieces, lines, t, ia_k, last_b, prev_e = [], [], 0.0, 0, 0.0, -9.0
for it in ITEMS:
    if it["who"] == "moi":
        ws = [w for w in WORDS if w["e"] > it["a"] + 0.05 and w["s"] < it["b"] - 0.05]
        runs = []
        for w in ws:
            if runs and w["s"] - runs[-1][-1]["e"] <= GAP:
                runs[-1].append(w)
            else:
                runs.append([w])
        words = []
        for r in runs:
            a, b = max(it["a"] - PAD, r[0]["s"] - PAD), r[-1]["e"] + PAD
            for w in r:
                tok = w["w"].strip()
                if words and tok[:1] in "'-" and abs(w["s"] - prev_e) < 0.2:      # « j » + « 'ai » -> « j'ai »
                    words[-1]["w"] += tok; words[-1]["e"] = round(t + w["e"] - a, 3)
                else:
                    words.append({"w": tok, "s": round(t + w["s"] - a, 3), "e": round(t + w["e"] - a, 3)})
                prev_e = w["e"]
            pieces.append((a, b, False))
            t += b - a
        lines.append({"who": "moi", "start": words[0]["s"], "end": words[-1]["e"], "text": " ".join(w["w"] for w in words),
                      "words": words, "tag": it.get("tag", "")})
        last_b = b
    else:
        src = os.path.join(iavo, f"l{ia_k:02d}.mp3")
        wav = os.path.join(out, f"ia{ia_k:02d}.wav")
        ff("-i", src, "-af", "aresample=48000," + TRIM + "," + IA_FX, "-ar", str(SR), "-ac", "1", wav)
        d = dur(wav)
        a0 = last_b + 0.05
        pieces.append((a0, a0 + d + 0.5, True))             # Tony keeps eating, muted, under his IA
        lines.append({"who": "ia", "start": round(t + 0.2, 3), "end": round(t + 0.2 + d, 3), "text": it["text"], "wav": wav})
        t += d + 0.5
        last_b = a0 + d + 0.5
        ia_k += 1
TOTAL = round(t + 0.8, 3)                                  # + a short hold on the last frame
NF = round(TOTAL * FPS)

# IA words: spread on the line by syllable weight (the voice is regular; captions only need to land on the beat)
for ln in lines:
    if ln["who"] == "ia":
        toks = ln["text"].split()
        wts = [max(1, sum(c in "aeiouyéèêàâîôûAEIOUY" for c in w)) for w in toks]
        step, s = (ln["end"] - ln["start"]) / sum(wts), ln["start"]
        ln["words"] = []
        for w, k in zip(toks, wts):
            ln["words"].append({"w": w, "s": round(s, 3), "e": round(s + k * step, 3)}); s += k * step

# ------------------------------------------------------------------ picture + Tony's voice, piece by piece
parts, cuts, acc = [], [], 0.0
for k, (a, b, mute) in enumerate(pieces):
    p = os.path.join(out, f"p{k:03d}.mkv")
    n = max(1, round((b - a) * FPS))
    af = "volume=0" if mute else "anull"
    ff("-ss", f"{a:.3f}", "-i", take, "-t", f"{n / FPS:.4f}", "-vf", "fps=30,scale=1080:1920:flags=lanczos,format=yuv420p",
       "-af", f"aresample=48000,{af},apad", "-frames:v", str(n), "-c:v", "libx264", "-crf", "15", "-preset", "veryfast",
       "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "1", "-shortest", p)
    parts.append(p); cuts.append(round(acc, 3)); acc += n / FPS
lst = os.path.join(out, "parts.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
ff("-f", "concat", "-safe", "0", "-i", lst, "-vf", f"tpad=stop_mode=clone:stop_duration=2", "-frames:v", str(NF),
   "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-g", "30", "-pix_fmt", "yuv420p", "-an", os.path.join(out, "base.mp4"))
ff("-f", "concat", "-safe", "0", "-i", lst, "-vn", "-af", f"apad=whole_dur={TOTAL}", "-t", str(TOTAL), "-ar", str(SR), "-ac", "1",
   os.path.join(out, "tony.wav"))
ias = [ln for ln in lines if ln["who"] == "ia"]
flt = ";".join(f"[{k}:a]adelay={int(round(ln['start'] * 1000))}[d{k}]" for k, ln in enumerate(ias))
flt += ";" + "".join(f"[d{k}]" for k in range(len(ias))) + f"amix=inputs={len(ias)}:normalize=0:duration=longest,apad=whole_dur={TOTAL}[v]"
ff(*sum((["-i", ln["wav"]] for ln in ias), []), "-filter_complex", flt, "-map", "[v]", "-t", str(TOTAL), "-ar", str(SR), "-ac", "1",
   os.path.join(out, "ia.wav"))

# ------------------------------------------------------------------ IA avatar: lips move only on IA lines (same bank as autoboost-80/83)
CLIPS = os.path.join(SH, "avatar-bank", "clips")
LIPS = [("B1_principe", 0.08, 4.88), ("C2_commente_motcle", 0.08, 4.83), ("A1_hook_frontal", 0.67, 4.58)]
VF = "crop=720:720:0:40,scale=600:600,fps=30,format=yuv420p"
segs, rot, kk, cur = [], 0, 0, 0
still = os.path.join(out, "av_still.png")
ff("-ss", "0.05", "-i", os.path.join(CLIPS, "B1_principe.mp4"), "-vf", "crop=720:720:0:40,scale=600:600", "-frames:v", "1", still)


def av_seg(args, n):
    global kk
    p = os.path.join(out, f"av{kk:03d}.mp4"); kk += 1
    ff(*args, "-frames:v", str(n), "-c:v", "libx264", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p", p)
    segs.append(p)
    return p


for ln in ias:
    a, b = round(ln["start"] * FPS), round(ln["end"] * FPS)
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
ff("-f", "concat", "-safe", "0", "-i", os.path.join(out, "av.txt"), "-c:v", "libx264", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p",
   "-frames:v", str(NF), "-movflags", "+faststart", os.path.join(out, "avatar.mp4"))

for ln in lines:
    ln.pop("wav", None)
json.dump({"total": TOTAL, "lines": lines, "cuts": cuts}, open(os.path.join(out, "vo.json"), "w"), ensure_ascii=False, indent=1)
print(f"done: {NF} frames, {TOTAL} s, {len(pieces)} pieces, {len(ias)} IA lines")
for ln in lines:
    print(f"  {ln['who']:3s} {ln['start']:6.2f}-{ln['end']:6.2f}  {ln['text'][:70]}")

#!/usr/bin/env python3
"""The showcased clip (Tony's song + its AI-generated motion) cut to the timeline.

One 1080x1920 video + one wav, frame-exact on the composition: each block shows
the passage that fits it, sound and picture together (the whole point of the
video is "tout est calé sur mon son"). The finale ends at clip 26.83 s and the
hook starts there: the loop is seamless, picture and song.

  python3 clip_track.py CLIP.mp4 PLAN_ACTUAL.json OUTDIR
"""
import json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FPS, SR = 30, 48000
clip, plan, out = sys.argv[1:4]
P = json.load(open(plan))
starts = [c["out_start"] for c in P["plan"]]
T = P["total"]
# block boundaries on the cut: hook | son | sync | idée + CTA (clip hidden) | finale
B = [0.0, starts[1], starts[2], starts[3], starts[6], T]
SRC = [26.83, 0.5, 14.0, 30.0, None]          # clip time at each block start
fr = [round(b * FPS) for b in B]
SRC[4] = 26.83 - (fr[5] - fr[4]) / FPS         # the finale runs INTO the hook's first frame
os.makedirs(out, exist_ok=True)
vids, auds = [], []
for k in range(5):
    n = fr[k + 1] - fr[k]
    v, a = os.path.join(out, f"seg{k}.mp4"), os.path.join(out, f"seg{k}.wav")
    subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{SRC[k]:.4f}", "-i", clip, "-an", "-vf", f"fps={FPS},scale=1080:1920",
                    "-frames:v", str(n), "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-video_track_timescale", "30000", v, "-y"], check=True)
    ns = round(n / FPS * SR)
    subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{SRC[k]:.4f}", "-i", clip, "-vn", "-ac", "2", "-ar", str(SR),
                    "-af", f"apad,atrim=end_sample={ns},afade=t=in:d=0.012,afade=t=out:st={n / FPS - 0.012:.4f}:d=0.012",
                    a, "-y"], check=True)
    vids.append(v); auds.append(a)
    print(f"bloc {k}: {B[k]:6.2f}s  {n:4d} images  <- clip {SRC[k]:6.2f}s")
lst = os.path.join(out, "segs.txt")
open(lst, "w").write("".join(f"file '{os.path.abspath(v)}'\n" for v in vids))
subprocess.run([FF, "-nostdin", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "18",
                "-g", str(FPS), "-keyint_min", str(FPS), "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                os.path.join(out, "clip.mp4"), "-y"], check=True)
subprocess.run([FF, "-nostdin", "-v", "error", *sum((["-i", a] for a in auds), []), "-filter_complex",
                "".join(f"[{i}:a]" for i in range(5)) + "concat=n=5:v=0:a=1[a]", "-map", "[a]",
                os.path.join(out, "clip_song.wav"), "-y"], check=True)
json.dump({"bounds": B, "src": SRC}, open(os.path.join(out, "clip_track.json"), "w"))
print("clip.mp4 + clip_song.wav", fr[-1], "images")

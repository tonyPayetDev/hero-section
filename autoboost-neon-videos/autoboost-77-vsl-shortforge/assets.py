#!/usr/bin/env python3
"""VSL ShortForge - media for the composition.

  avatar.mp4  720x720, 32 s: black, then the BUREAU avatar (B1_principe, lips-active
              0.08 -> 4.88, LIPS-MAP.md) from 13.85 s to 16.15 s - under the line
              « ta voix clonée, ton avatar, les captions » - muted
  bed.wav     hook-epical-drums-02-80, file 30 -> 62 s: 120 BPM, downbeats on every
              even video second, decay 55.5 s -> silence, full re-entry at file 57.995
              = video 28.0 (the detonation). +16 dB where no one speaks - the first
              second (hook) and after « Action ! » (climax) - ramped (bgm README),
              faded out over the last 0.5 s
  proof/pN.jpg six frames of videos already made with the pipeline (real renders)

  python3 assets.py OUT_DIR
"""
import os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
SH = os.path.abspath(os.path.join(HERE, "..", "_shared"))
V = os.path.abspath(os.path.join(HERE, ".."))
out = sys.argv[1]
os.makedirs(os.path.join(out, "proof"), exist_ok=True)


def ff(*a):
    subprocess.run([FF, "-nostdin", "-v", "error", *a, "-y"], check=True)


ff("-f", "lavfi", "-i", "color=c=#0a0a0f:s=720x720:r=30:d=32", "-i", os.path.join(SH, "avatar-bank", "clips", "B1_principe.mp4"),
   "-filter_complex", "[1:v]trim=start=0.08:duration=2.3,setpts=PTS-STARTPTS+13.85/TB,fps=30,crop=720:720:0:40[a];"
   "[0:v][a]overlay=eof_action=pass,format=yuv420p[v]", "-map", "[v]", "-an", "-frames:v", "960",
   "-c:v", "libx264", "-crf", "18", "-g", "30", "-keyint_min", "30", "-movflags", "+faststart", os.path.join(out, "avatar.mp4"))
ff("-ss", "30", "-t", "32", "-i", os.path.join(SH, "bgm", "hook-epical-drums-02-80.mp3"),
   "-af", "volume='if(lt(t,1.0),6.3,if(lt(t,1.4),6.3-(t-1.0)/0.4*5.3,if(lt(t,28.4),1,if(lt(t,28.7),1+(t-28.4)/0.3*5.3,6.3))))':eval=frame,afade=t=out:st=31.5:d=0.5",
   "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", os.path.join(out, "bed.wav"))  # float: the +16 dB spans must not clip
PROOF = [("autoboost-61-debunk-10k-freelance/video.mp4", 5), ("autoboost-62-claude-sonnet-5/video.mp4", 12),
         ("autoboost-63-zapier-vers-n8n/video.mp4", 5), ("autoboost-09-content-ideas/renders/public_2026-07-09_18-09-38.mp4", 12),
         ("autoboost-08-pinterest-automation/renders/public_2026-07-09_17-31-07.mp4", 12),
         ("autoboost-10-livres-enfants/renders/public_2026-07-09_16-55-14.mp4", 10)]
for i, (v, t) in enumerate(PROOF):
    ff("-ss", str(t), "-i", os.path.join(V, v), "-frames:v", "1",
       "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1", "-q:v", "3",
       os.path.join(out, "proof", f"p{i}.jpg"))
print("avatar.mp4, bed.wav, proof/p0-5.jpg")

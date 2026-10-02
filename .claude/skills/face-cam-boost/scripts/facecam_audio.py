#!/usr/bin/env python3
"""FaceCam Boost - the final mix: real voice + bed + SFX on the motion events.

  python3 facecam_audio.py --voice WORK/voice.wav --events events.json --frames 1178 --out mix.wav [--bed valse]

events.json: [[time_s, "sfx-file.mp3", gain_db], ...] - files from _shared/sfx-palette/v2/assets.

Charter (_shared/CHARTE.md): the voice is normalised FIRST, the bed sits under it
at a fixed level (never normalise the sum), amix normalize=0.

Beds:
  valse   valse-des-fleurs-maison-evidee: our own recording, the bgm README pick
          under a voice. Its intro (0-6.6 s) is ~6 dB hotter and the file is
          35.4 s, so the stable span bar 6 -> bar 26 is looped on a bar boundary.
  drums   mindset-epical-drums-05-75: 5.6 dB spread, energetic.
  --bed-file  a track already cut to the render's timeline (the song of a clip shown
          on screen, in sync with its pictures): used as is, ducked, --bed-gain dB.
"""
import argparse, json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SHARED = os.path.join(REPO, "autoboost-neon-videos", "_shared")
SFX = os.path.join(SHARED, "sfx-palette", "v2", "assets")
BAR = 4 / 3


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:], file=sys.stderr)
        raise SystemExit("ffmpeg failed")


ap = argparse.ArgumentParser()
ap.add_argument("--voice", required=True)
ap.add_argument("--events", required=True)
ap.add_argument("--frames", type=int, required=True, help="frame count of the render (30 fps)")
ap.add_argument("--out", required=True)
ap.add_argument("--bed", default="valse", choices=["valse", "drums", "none"])
ap.add_argument("--bed-file", help="a bed already timed to the render (e.g. the showcased clip's own song): no loop, no fades")
ap.add_argument("--bed-gain", type=float, default=-8.0, help="dB applied to --bed-file")
a = ap.parse_args()
T = a.frames / 30.0
events = json.load(open(a.events))
work = os.path.dirname(os.path.abspath(a.out))

ins, parts = [], []
for k, (t, f, g) in enumerate(events):
    ins += ["-i", os.path.join(SFX, f)]
    parts.append(f"[{k}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,volume={g}dB,adelay={int(t * 1000)}[s{k}]")
sfx = os.path.join(work, "sfx.wav")
run([FF, "-nostdin", "-v", "error", *ins, "-filter_complex",
     ";".join(parts) + ";" + "".join(f"[s{k}]" for k in range(len(events)))
     + f"amix=inputs={len(events)}:normalize=0,apad,atrim=0:{T:.3f}[a]",
     "-map", "[a]", "-ar", "48000", "-ac", "1", sfx, "-y"])

voice = ("[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
         "loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[v][key];")
fade = f"atrim=0:{T:.3f},afade=t=in:st=0:d=0.6,afade=t=out:st={T - 1.2:.3f}:d=1.2"
duck = "[bed][key]sidechaincompress=threshold=0.035:ratio=6:attack=12:release=320[duck];"
if a.bed_file:
    inputs = ["-i", a.bed_file]
    bed = f"[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,apad,atrim=0:{T:.3f},volume={a.bed_gain}dB[bed];"
    sfx_idx = 2
elif a.bed == "valse":
    bgm = os.path.join(SHARED, "bgm", "valse-des-fleurs-maison-evidee.mp3")
    span = ["-ss", f"{5 * BAR:.4f}", "-t", f"{20 * BAR:.4f}", "-i", bgm]
    copies = max(2, int(T // (20 * BAR)) + 2)
    inputs = span * copies
    chain = "".join(f"[{i + 1}:a]" for i in range(copies))
    xf = "[1:a][2:a]acrossfade=d=0.25:c1=tri:c2=tri[x2];" + "".join(
        f"[x{i}][{i + 1}:a]acrossfade=d=0.25:c1=tri:c2=tri[x{i + 1}];" for i in range(2, copies))
    bed = xf + f"[x{copies}]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,{fade},volume=-5dB[bed];"
    sfx_idx = copies + 1
elif a.bed == "drums":
    bgm = os.path.join(SHARED, "bgm", "mindset-epical-drums-05-75.mp3")
    inputs = ["-stream_loop", "-1", "-t", f"{T:.3f}", "-i", bgm]
    bed = f"[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,{fade},volume=-11dB[bed];"
    sfx_idx = 2
else:
    inputs, bed, duck, sfx_idx = [], "", "", 1

mix = (f"[v][duck][{sfx_idx}:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[a]" if a.bed != "none" or a.bed_file
       else f"[v][{sfx_idx}:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]")
run([FF, "-nostdin", "-v", "error", "-i", a.voice, *inputs, "-i", sfx,
     "-filter_complex", voice + bed + duck + mix, "-map", "[a]", "-ar", "48000", "-ac", "2", a.out, "-y"])
print(f"{a.out} ({len(events)} SFX, bed {a.bed_file or a.bed}, {T:.2f}s)")

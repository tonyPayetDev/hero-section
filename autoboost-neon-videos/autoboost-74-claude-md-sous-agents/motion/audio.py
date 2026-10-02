#!/usr/bin/env python3
"""Audio for the motion version: Tony's real voice, the same measured bed as the
first cut, and SFX re-placed on the motion events (screen slides, stamps,
checks, the CTA slam) instead of on the jump cuts.

Charter rules kept: voice normalised first, bed under it at a fixed level,
amix with normalize=0.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.abspath(os.path.join(HERE, "..", "..", "_shared"))
SCRATCH = "/tmp/claude-0/-home-user-hero-section/25c114f9-7c32-5b84-b3ea-354b9cf49fbf/scratchpad"
FF = os.path.join(SCRATCH, "bin", "ffmpeg")
WORK = os.path.join(SCRATCH, "build74")
VOICE = os.path.join(WORK, "voice.wav")
BGM = os.path.join(SHARED, "bgm/mindset-epical-drums-05-75.mp3")
SFX = os.path.join(SHARED, "sfx-palette/v2/assets")
T = 1178 / 30.0

# (time, file, gain dB) - times match gen.py
EVENTS = [
    (3.28, "sfx-dolly-rush.mp3", -16),      # facecam collapses into the ring
    (3.70, "sfx-arrival-stop.mp3", -20),
    (7.55, "sfx-impact.mp3", -15),          # LIMITE ATTEINTE stamp
    (8.40, "sfx-whoosh-v2.mp3", -17),       # screen 2 slides in
    (10.95, "sfx-impact.mp3", -15),         # MAUVAISE QUESTION stamp
    (14.45, "sfx-confirm.mp3", -16),        # the right question, checked
    (14.70, "sfx-whoosh-v2.mp3", -17),      # screen 3
    (15.95, "sfx-chime-v2.mp3", -17),       # CLAUDE.md reveal
    (19.70, "sfx-whoosh-v2.mp3", -17),      # screen 4
    (21.55, "sfx-pop.mp3", -18),            # light model node
    (23.85, "sfx-pop.mp3", -16),            # Opus node
    (24.30, "sfx-whoosh-v2.mp3", -17),      # screen 5
    (26.15, "sfx-impact.mp3", -15),         # GASPILLAGE stamp
    (28.15, "sfx-whoosh-v2.mp3", -17),      # screen 6
    (31.90, "sfx-pop.mp3", -19), (32.30, "sfx-pop.mp3", -19), (32.70, "sfx-pop.mp3", -19),
    (33.07, "sfx-whoosh-v2.mp3", -17),      # CTA screen
    (35.72, "sfx-impact-deep.mp3", -16),    # TOKEN slam
    (36.55, "sfx-click-soft.mp3", -18),     # typing the comment
    (37.05, "sfx-notify.mp3", -17),         # sent
]

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:], file=sys.stderr)
        raise SystemExit("ffmpeg failed")

ins, parts = [], []
for k, (t, f, g) in enumerate(EVENTS):
    ins += ["-i", os.path.join(SFX, f)]
    parts.append(f"[{k}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
                 f"volume={g}dB,adelay={int(t * 1000)}[s{k}]")
sfx = os.path.join(WORK, "sfx_motion.wav")
run([FF, "-nostdin", "-v", "error", *ins, "-filter_complex",
     ";".join(parts) + ";" + "".join(f"[s{k}]" for k in range(len(EVENTS)))
     + f"amix=inputs={len(EVENTS)}:normalize=0,apad,atrim=0:{T:.3f}[a]",
     "-map", "[a]", "-ar", "48000", "-ac", "1", sfx, "-y"])

out = os.path.join(WORK, "mix_motion.wav")
run([FF, "-nostdin", "-v", "error", "-i", VOICE,
     "-stream_loop", "-1", "-t", f"{T:.3f}", "-i", BGM, "-i", sfx,
     "-filter_complex",
     "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
     "loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[v][key];"
     "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
     f"volume=-11dB,afade=t=in:st=0:d=0.8,afade=t=out:st={T - 1.2:.3f}:d=1.2[bed];"
     "[bed][key]sidechaincompress=threshold=0.035:ratio=6:attack=12:release=320[duck];"
     "[v][duck][2:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[a]",
     "-map", "[a]", "-ar", "48000", "-ac", "2", out, "-y"])
print(f"mix_motion.wav ok ({len(EVENTS)} SFX)")

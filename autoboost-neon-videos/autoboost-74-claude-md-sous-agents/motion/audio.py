#!/usr/bin/env python3
"""Audio for the motion version: Tony's real voice, Valse des fleurs (our own
"maison-evidee" recording - the bed the bgm README picks for under a voice), and
SFX on the motion events (slides, stamps, stickers, the pile, the CTA).

The valse intro (0-6.6 s) runs ~6 dB hotter than the rest and the file is only
35.4 s, so the bed loops the stable span bar 6 -> bar 26 (6.667 -> 33.333 s,
5 dB spread measured) on a bar boundary with a short crossfade.

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
BGM = os.path.join(SHARED, "bgm/valse-des-fleurs-maison-evidee.mp3")
BAR = 4 / 3          # one 3/4 bar at 135 bpm (bar 6 starts at 6.667 s per the README)
LOOP_IN, LOOP_LEN = 5 * BAR, 20 * BAR
SFX = os.path.join(SHARED, "sfx-palette/v2/assets")
T = 1178 / 30.0

# (time, file, gain dB) - times match gen.py
EVENTS = [
    (0.15, "sfx-thwip.mp3", -18),           # ÇA PART sticker
    (3.28, "sfx-dolly-rush.mp3", -16),      # facecam collapses into the ring
    (3.70, "sfx-arrival-stop.mp3", -20),
    (7.55, "sfx-impact.mp3", -15),          # LIMITE ATTEINTE stamp
    (7.65, "sfx-pop.mp3", -20),             # ÇA BLOQUE sticker
    (8.40, "sfx-whoosh-v2.mp3", -17),       # screen 2
    (10.95, "sfx-impact.mp3", -15),         # MAUVAISE QUESTION stamp
    (12.80, "sfx-whoosh-lat.mp3", -16),     # top card flies off the pile
    (13.55, "sfx-thwip.mp3", -18),          # PLUS CLAIR
    (14.40, "sfx-confirm.mp3", -16),        # the right question, checked
    (14.70, "sfx-whoosh-v2.mp3", -17),      # screen 3
    (15.95, "sfx-chime-v2.mp3", -17),       # CLAUDE.md reveal
    (18.95, "sfx-thwip.mp3", -18),          # BON SYSTÈME
    (19.70, "sfx-whoosh-v2.mp3", -17),      # screen 4
    (21.55, "sfx-pop.mp3", -18),            # light model node
    (21.70, "sfx-thwip.mp3", -19),          # PLUS SIMPLE
    (23.85, "sfx-pop.mp3", -16),            # Opus node
    (24.30, "sfx-whoosh-v2.mp3", -17),      # screen 5, split opens
    (26.15, "sfx-impact.mp3", -15),         # GASPILLAGE stamp
    (27.55, "sfx-thwip.mp3", -18),          # DÉJÀ MIEUX
    (28.15, "sfx-whoosh-v2.mp3", -17),      # screen 6
    (31.35, "sfx-thwip.mp3", -18),          # ÇA MONTE
    (31.90, "sfx-pop.mp3", -19), (32.30, "sfx-pop.mp3", -19), (32.70, "sfx-pop.mp3", -19),
    (33.07, "sfx-whoosh-v2.mp3", -17),      # CTA screen
    (33.75, "sfx-thwip.mp3", -18),          # NIVEAU MAX
    (35.70, "sfx-impact-deep.mp3", -16),    # TOKEN slam
    (36.28, "sfx-click.mp3", -16),          # button pressed
    (36.58, "sfx-pop.mp3", -18),            # opens into the comment field
    (37.20, "sfx-notify.mp3", -17),         # sent
    (37.60, "sfx-arrival-stop.mp3", -17),   # full-screen finale
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
sfx = os.path.join(WORK, "sfx_motion_v2.wav")
run([FF, "-nostdin", "-v", "error", *ins, "-filter_complex",
     ";".join(parts) + ";" + "".join(f"[s{k}]" for k in range(len(EVENTS)))
     + f"amix=inputs={len(EVENTS)}:normalize=0,apad,atrim=0:{T:.3f}[a]",
     "-map", "[a]", "-ar", "48000", "-ac", "1", sfx, "-y"])

out = os.path.join(WORK, "mix_motion_v2.wav")
run([FF, "-nostdin", "-v", "error", "-i", VOICE,
     "-ss", f"{LOOP_IN:.4f}", "-t", f"{LOOP_LEN:.4f}", "-i", BGM,
     "-ss", f"{LOOP_IN:.4f}", "-t", f"{LOOP_LEN:.4f}", "-i", BGM, "-i", sfx,
     "-filter_complex",
     "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
     "loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[v][key];"
     "[1:a][2:a]acrossfade=d=0.25:c1=tri:c2=tri,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
     f"atrim=0:{T:.3f},volume=-5dB,afade=t=in:st=0:d=0.6,afade=t=out:st={T - 1.2:.3f}:d=1.2[bed];"
     "[bed][key]sidechaincompress=threshold=0.035:ratio=6:attack=12:release=320[duck];"
     "[v][duck][3:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[a]",
     "-map", "[a]", "-ar", "48000", "-ac", "2", out, "-y"])
print(f"mix_motion_v2.wav ok ({len(EVENTS)} SFX)")

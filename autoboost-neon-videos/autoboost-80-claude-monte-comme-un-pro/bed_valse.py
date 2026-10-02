#!/usr/bin/env python3
"""autoboost-80 - the bed: Valse des fleurs (house recording, _shared/bgm/valse-des-fleurs-maison).

The hollow version (évidée) plays under the voices. Its 20-bar loop (bars 6-25, file 6.667-33.333 s,
1 bar = 4/3 s) is seamless. It is laid out backwards from the CTA hold, so that after the last word
the full orchestra (tutti) lands bar 5 and its resolution, in sync with the évidée. The two files are the
same recording taken from two places in the orchestra, so they sum without a seam.

  évidée  file 13.68 -> 33.333 | loop 6.667 -> 33.333 | 0 -> end      (crossfades 0.25 s, tri)
  tutti   file 5.333 -> 8.5, from the last word on, +8 dB with the évidée for the hold

  python3 bed_valse.py BUILD_DIR      (reads vo.json, writes bed.wav, pcm_f32le stereo 48 kHz)
"""
import json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
HERE = os.path.dirname(os.path.abspath(__file__))
BGM = os.path.abspath(os.path.join(HERE, "..", "_shared", "bgm"))
EVI, TUT = os.path.join(BGM, "valse-des-fleurs-maison-evidee.mp3"), os.path.join(BGM, "valse-des-fleurs-maison-tutti.mp3")
BAR, XF = 4 / 3, 0.25
out = sys.argv[1]
vo = json.load(open(os.path.join(out, "vo.json")))
T, last = vo["total"], vo["lines"][-1]["end"]

land = last + 0.05                     # video time of tutti bar 5 (file 5.333)
v0 = land - 4 * BAR                    # video time of évidée file 0 (bar 1)
v_loop = v0 - 20 * BAR                 # video time of the loop start (file 6.667)
head = v_loop                          # the opening plays file (33.333 - head) -> 33.333
assert head > 0, "voice track too short for this layout"
# each joint is centred on its bar line: a segment carries XF/2 of pre-roll and post-roll (bar 1 has no
# pre-roll in the file, so it gets XF/2 of silence instead)
segs = [(25 * BAR - head, head + XF / 2), (5 * BAR - XF / 2, 20 * BAR + XF), (0.0, T - v0 + 0.1)]
inputs = []
for s, d in segs:
    inputs += ["-ss", f"{s:.4f}", "-t", f"{d:.4f}", "-i", EVI]
chain = (f"[2:a]adelay={int(XF / 2 * 1000)}:all=1[c];[0:a][1:a]acrossfade=d={XF}:c1=tri:c2=tri[e1];"
         f"[e1][c]acrossfade=d={XF}:c1=tri:c2=tri,atrim=0:{T:.3f}[evi];")
tut_at = land - 5 * BAR                # tutti file 0 on the video timeline
inputs += ["-ss", f"{5 * BAR - 0.05:.4f}", "-t", "3.4", "-i", TUT]
chain += (f"[3:a]afade=t=in:st=0:d=0.05,adelay={int(round((tut_at + 5 * BAR - 0.05) * 1000))}:all=1,apad,atrim=0:{T:.3f}[tut];"
          f"[evi][tut]amix=inputs=2:normalize=0:duration=first,"
          f"volume='if(gt(t,{last:.2f}),2.5,1)':eval=frame,"
          f"afade=t=in:st=0:d=0.6,afade=t=out:st={T - 0.45:.3f}:d=0.45[bed]")
subprocess.run([FF, "-nostdin", "-v", "error", *inputs, "-filter_complex", chain, "-map", "[bed]", "-ar", "48000", "-ac", "2",
                "-c:a", "pcm_f32le", os.path.join(out, "bed.wav"), "-y"], check=True)
print(f"bed.wav {T:.2f}s: opening {head:.2f}s, loop at {v_loop:.2f}s, bar 1 at {v0:.2f}s, tutti bar 5 at {land:.2f}s")

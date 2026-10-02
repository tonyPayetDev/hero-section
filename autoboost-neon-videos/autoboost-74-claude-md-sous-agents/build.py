#!/usr/bin/env python3
"""autoboost-74 build pipeline. Stages are independent so a failure says where.

  1 cuts   8 speech cuts (dead air removed, tempo applied) -> base.mp4
  2 zoom   base split on the 21 beats, one punch-in per beat -> zoomed.mp4
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/tmp/claude-0/-home-user-hero-section/25c114f9-7c32-5b84-b3ea-354b9cf49fbf/scratchpad"
WORK = os.path.join(SCRATCH, "build74")
FF = os.path.join(SCRATCH, "node_modules/ffmpeg-static/ffmpeg")
FP = os.path.join(SCRATCH, "node_modules/ffprobe-static/bin/linux/x64/ffprobe")
SRC = "/root/.claude/uploads/25c114f9-7c32-5b84-b3ea-354b9cf49fbf/a5b418dc-video_25.mp4"
os.makedirs(WORK, exist_ok=True)

P = json.load(open(os.path.join(HERE, "plan.json")))
TEMPO, TOTAL, BEATS = P["tempo"], P["total"], P["beats"]

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print("\n".join(r.stderr.strip().splitlines()[-12:]), file=sys.stderr)
        raise SystemExit(f"ffmpeg failed: {' '.join(args[:9])}...")

def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries",
        "format=duration", "-of", "csv=p=0", p]).decode().strip())

def nframes(p):
    return int(subprocess.check_output([FP, "-v", "error", "-select_streams", "v:0",
        "-count_frames", "-show_entries", "stream=nb_read_frames",
        "-of", "csv=p=0", p]).decode().strip())

def concat(files, out, extra=()):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in files:
            f.write(f"file '{p}'\n")
    run([FF, "-nostdin", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         *extra, out, "-y"])

# ---------------------------------------------------------------- stage 1
def stage_cuts():
    files = []
    for p in P["plan"]:
        out = os.path.join(WORK, f"cut{p['i']:02d}.mp4")
        run([FF, "-nostdin", "-v", "error", "-ss", str(p["src_in"]), "-to", str(p["src_out"]),
             "-i", SRC,
             "-vf", f"setpts=PTS/{TEMPO},fps=30",
             "-af", f"atempo={TEMPO},aresample=48000",
             "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1",
             "-video_track_timescale", "30000", out, "-y"])
        files.append(out)
    base = os.path.join(WORK, "base.mp4")
    concat(files, base, ("-c", "copy"))
    print(f"base.mp4 {dur(base):.2f}s (plan {TOTAL:.2f}s)")

# ---------------------------------------------------------------- stage 1b
def stage_remap():
    """Rewrites the plan onto the real encoded durations.

    Per-segment encoding rounds each cut to a whole frame, so the planned
    timeline drifts a few tenths by the end. Captions are built from this
    remapped file, never from the planned one.
    """
    t, plan = 0.0, []
    for p in P["plan"]:
        d = dur(os.path.join(WORK, f"cut{p['i']:02d}.mp4"))
        k = d / p["dur"]
        q = dict(p, out_start=round(t, 3), dur=round(d, 3),
                 words=[{"w": w["w"],
                         "s": round(t + (w["s"] - p["out_start"]) * k, 3),
                         "e": round(t + (w["e"] - p["out_start"]) * k, 3)} for w in p["words"]])
        plan.append(q)
        t += d
    # beats carry over proportionally, cut by cut
    beats = []
    for b in P["beats"]:
        src = max((p for p in P["plan"] if p["out_start"] <= b + 1e-6), key=lambda p: p["out_start"])
        dst = plan[src["i"]]
        beats.append(round(dst["out_start"] + (b - src["out_start"]) * dst["dur"] / src["dur"], 3))
    out = {"total": round(t, 3), "tempo": TEMPO, "plan": plan, "beats": sorted(set(beats))}
    json.dump(out, open(os.path.join(HERE, "plan_actual.json"), "w"), ensure_ascii=False, indent=1)
    print(f"timeline recalee : {t:.2f}s")

def _actual():
    global P, TOTAL, BEATS
    P = json.load(open(os.path.join(HERE, "plan_actual.json")))
    TOTAL, BEATS = P["total"], P["beats"]

# ---------------------------------------------------------------- stage 2
# Punch-in pattern: a wide frame is the rest state, tighter frames land on the
# beats that carry the idea. Index into ZOOMS cycles but is forced tight on the
# hook, the reveal and the CTA.
ZOOMS = [1.00, 1.07, 1.03, 1.11, 1.00, 1.09, 1.05, 1.13]
TIGHT = {0, 8, 9, 10, 19, 20}

def stage_zoom():
    """One punch-in per beat, cut on exact frame boundaries.

    Beat edges are snapped to frames and each piece is written with an explicit
    -frames:v count, so the 21 pieces sum back to the base frame count instead
    of each rounding up and drifting half a second by the end.
    """
    _actual()
    base = os.path.join(WORK, "base.mp4")
    audio = os.path.join(WORK, "voice.wav")
    run([FF, "-nostdin", "-v", "error", "-i", base, "-vn", "-c:a", "pcm_s16le", audio, "-y"])

    NF = nframes(base)
    edges = sorted(set([0] + [min(NF, round(b * 30)) for b in BEATS] + [NF]))
    files = []
    for k, (fa, fb) in enumerate(zip(edges, edges[1:])):
        z = 1.13 if k in TIGHT else ZOOMS[k % len(ZOOMS)]
        cw, ch = round(1080 / z / 2) * 2, round(1440 / z / 2) * 2
        x, y = (1080 - cw) // 2, int((1440 - ch) * 0.34)
        out = os.path.join(WORK, f"z{k:02d}.mp4")
        run([FF, "-nostdin", "-v", "error", "-ss", f"{fa/30:.5f}", "-i", base,
             "-frames:v", str(fb - fa), "-an",
             "-vf", f"crop={cw}:{ch}:{x}:{y},scale=1080:1440:flags=lanczos,setsar=1",
             "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
             "-r", "30", "-video_track_timescale", "30000", out, "-y"])
        files.append(out)
    zoomed = os.path.join(WORK, "zoomed.mp4")
    concat(files, zoomed, ("-c", "copy"))
    print(f"zoomed.mp4 {nframes(zoomed)} images / base {NF} ({dur(zoomed):.2f}s)")

# ---------------------------------------------------------------- stage 3
SHARED = os.path.abspath(os.path.join(HERE, "..", "_shared"))
BROLL_SWITCH = 15.0   # s - flux (tokens) until the reveal, then workflow (sub-agents)

def stage_compose():
    """Brand canvas: b-roll bands top and bottom, the facecam window between
    them, gold hairlines, and the ASS captions burned on top."""
    _actual()
    zoomed = os.path.join(WORK, "zoomed.mp4")
    T = nframes(zoomed) / 30.0
    flux = os.path.join(SHARED, "broll-abstrait/flux-9x16.mp4")
    work = os.path.join(SHARED, "broll-abstrait/workflow-9x16.mp4")
    ass = os.path.join(HERE, "captions.ass").replace(":", r"\:")
    out = os.path.join(WORK, "visual.mp4")

    fc = (
        f"[1:v]scale=1080:1920,fps=30,setsar=1,eq=brightness=-0.06[b1];"
        f"[2:v]scale=1080:1920,fps=30,setsar=1,eq=brightness=-0.06[b2];"
        f"[b1][b2]concat=n=2:v=1:a=0[broll];"
        f"color=c=0x0a0a0f:s=1080x1920:r=30:d={T:.3f}[bg];"
        f"[bg][broll]blend=all_mode=screen:all_opacity=0.18,format=yuv420p[canvas];"
        f"[canvas][0:v]overlay=0:180:shortest=1[v1];"
        f"[v1]drawbox=x=0:y=177:w=1080:h=3:color=0xeab308@0.8:t=fill,"
        f"drawbox=x=0:y=1620:w=1080:h=3:color=0xeab308@0.8:t=fill[v2];"
        f"[v2]ass='{ass}'[out]"
    )
    run([FF, "-nostdin", "-v", "error",
         "-i", zoomed,
         "-stream_loop", "-1", "-t", f"{BROLL_SWITCH:.3f}", "-i", flux,
         "-stream_loop", "-1", "-t", f"{T - BROLL_SWITCH:.3f}", "-i", work,
         "-filter_complex", fc, "-map", "[out]", "-an",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-r", "30", "-video_track_timescale", "30000", out, "-y"])
    print(f"visual.mp4 {nframes(out)} images ({dur(out):.2f}s)")

# ---------------------------------------------------------------- stage 4
# mindset-epical-drums-05-75 is the only bed in _shared/bgm whose energy stays
# inside the charter's 10 dB window (measured spread: 5.6 dB over 42 s), so it
# will not climb on its own underneath the voice.
BGM = "bgm/mindset-epical-drums-05-75.mp3"
SFX_DIR = "sfx-palette/v2/assets"

def stage_audio():
    """Voice normalised first, then a fixed-level bed under it - never the sum,
    which would lift the music back up with the voice."""
    _actual()
    voice = os.path.join(WORK, "voice.wav")
    T = nframes(os.path.join(WORK, "zoomed.mp4")) / 30.0

    # one soft transition per cut; a deeper impact on the reveal and on the CTA
    cuts = [p["out_start"] for p in P["plan"] if p["out_start"] > 0.05]
    marks = [(t, "sfx-impact.mp3" if abs(t - 15.0) < 0.3 or t > 35.0 else "sfx-whoosh-v2.mp3")
             for t in cuts]

    ins, parts, labels = [], [], []
    for k, (t, f) in enumerate(marks):
        ins += ["-i", os.path.join(SHARED, SFX_DIR, f)]
        parts.append(f"[{k}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
                     f"volume=-17dB,adelay={int(t*1000)}[s{k}]")
        labels.append(f"[s{k}]")
    sfx = os.path.join(WORK, "sfx.wav")
    run([FF, "-nostdin", "-v", "error", *ins, "-filter_complex",
         ";".join(parts) + ";" + "".join(labels) + f"amix=inputs={len(marks)}:normalize=0,"
         f"apad,atrim=0:{T:.3f}[a]",
         "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", sfx, "-y"])

    out = os.path.join(WORK, "mix.wav")
    run([FF, "-nostdin", "-v", "error",
         "-i", voice,
         "-stream_loop", "-1", "-t", f"{T:.3f}", "-i", os.path.join(SHARED, BGM),
         "-i", sfx,
         "-filter_complex",
         "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
         "loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[v][key];"
         "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,"
         f"volume=-11dB,afade=t=in:st=0:d=0.8,afade=t=out:st={T-1.2:.3f}:d=1.2[bed];"
         "[bed][key]sidechaincompress=threshold=0.035:ratio=6:attack=12:release=320[duck];"
         f"[v][duck][2:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[a]",
         "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", out, "-y"])
    print(f"mix.wav {dur(out):.2f}s")

# ---------------------------------------------------------------- stage 5
def stage_final():
    out = os.path.join(HERE, "autoboost-74.mp4")
    run([FF, "-nostdin", "-v", "error",
         "-i", os.path.join(WORK, "visual.mp4"), "-i", os.path.join(WORK, "mix.wav"),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-movflags", "+faststart", "-shortest", out, "-y"])
    print(f"autoboost-74.mp4 {dur(out):.2f}s / {os.path.getsize(out)/1e6:.1f} Mo")

if __name__ == "__main__":
    for s in sys.argv[1:] or ["cuts", "remap", "zoom", "compose", "audio", "final"]:
        globals()["stage_" + s]()

#!/usr/bin/env python3
"""Tony's real take (video_25) as his avatar under a new voice track.

The take is muted. Where the voice speaks, the picture comes from passages where
Tony speaks in the take; where the voice pauses, from passages where he is silent -
so the mouth moves only while words are heard. Chunks are consumed in order through
the take (no passage used twice until the take runs out), every chunk frame-exact.

  python3 avatar_track.py TAKE.mp4 TAKE_TRANSCRIPT.json VOICE_TRANSCRIPT.json VOICE_DUR OUT_DIR
-> OUT_DIR/avatar_src.mp4 (1080x1440, muted) + avatar_cuts.json (cut times, for punch-ins)
"""
import json, os, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FPS, GAP = 30, 0.30
take, tt, vt, vdur, out = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
os.makedirs(out, exist_ok=True)


def runs(words, total):
    talk = []
    for w in words:
        if talk and w["s"] - talk[-1][1] < GAP:
            talk[-1][1] = w["e"]
        else:
            talk.append([w["s"], w["e"]])
    sil, cur = [], 0.0
    for a, b in talk:
        if a - cur >= GAP:
            sil.append([cur, a])
        cur = b
    if total - cur >= GAP:
        sil.append([cur, total])
    return talk, sil


def words_of(path):
    t = json.load(open(path))
    segs = t if isinstance(t, list) else t["segments"]
    return [w for s in segs for w in s["words"]]


take_dur = float(subprocess.check_output([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", take]).decode())
t_talk, t_sil = runs(words_of(tt), take_dur)
t_sil = [s for s in t_sil if s[1] - s[0] >= 0.5]          # only clean, mouth-closed stretches
v_talk, v_sil = runs(words_of(vt), vdur)
plan = sorted([(a, b, "talk") for a, b in v_talk] + [(a, b, "sil") for a, b in v_sil])
# edges of the voice timeline: snap to frames, cover 0 -> vdur without holes
NF = round(vdur * FPS)
edges = sorted({0, NF} | {round(a * FPS) for a, _, _ in plan})
kind = {}
for a, b, k in plan:
    kind[round(a * FPS)] = k
pools = {"talk": [[round(a * FPS) + 2, round(b * FPS) - 2] for a, b in t_talk if b - a > 0.4],
         "sil": [[round(a * FPS) + 4, round(b * FPS) - 4] for a, b in t_sil]}
ptr = {"talk": [0, None], "sil": [0, None]}
chunks, cuts = [], []
for fa, fb in zip(edges, edges[1:]):
    k = kind.get(fa, "sil")
    need = fb - fa
    while need > 0:
        i, pos = ptr[k]
        run = pools[k][i % len(pools[k])]
        pos = run[0] if pos is None else pos
        take_n = min(need, run[1] - pos)
        if take_n <= 0:
            ptr[k] = [i + 1, None]; continue
        chunks.append((pos, take_n, k))
        cuts.append(round((NF - need - (NF - fb)) / FPS, 3))
        need -= take_n
        ptr[k] = [i, pos + take_n] if pos + take_n < run[1] else [i + 1, None]
files = []
for n, (pos, cnt, k) in enumerate(chunks):
    f = os.path.join(out, f"ch{n:03d}.mp4")
    subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{pos / FPS:.4f}", "-i", take, "-an", "-vf", "fps=30",
                    "-frames:v", str(cnt), "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-video_track_timescale", "30000", f, "-y"], check=True)
    files.append(f)
lst = os.path.join(out, "chunks.txt")
open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
subprocess.run([FF, "-nostdin", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "16",
                "-g", "30", "-pix_fmt", "yuv420p", "-frames:v", str(NF), os.path.join(out, "avatar_src.mp4"), "-y"], check=True)
json.dump({"frames": NF, "cuts": cuts, "chunks": chunks}, open(os.path.join(out, "avatar_cuts.json"), "w"))
print(f"avatar_src.mp4: {NF} frames, {len(chunks)} chunks ({sum(1 for c in chunks if c[2] == 'talk')} talk)")

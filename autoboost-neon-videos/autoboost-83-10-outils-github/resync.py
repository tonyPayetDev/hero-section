#!/usr/bin/env python3
"""autoboost-80 - re-cut Tony's take so his mouth follows the cloned voice (replaces build.py's Tony track).

build.py filled Tony's lines by reading the take's talking passages in order: the mouth kept moving
through the voice's pauses and closed while the voice still spoke (24 s, 36 s). Here every run of
his lines is matched on the voice's own rhythm:

  1. loudness envelopes at 30 fps: the take's own sound, and voice.wav (both relative to their speech level);
  2. each run of consecutive Tony lines (with the short gaps between them) is filled by the take window
     whose envelope matches best (speech on/off agreement + shape), allowed to split at the voice's
     pauses (max 3 pieces, mouth closed on both sides of a cut) and penalised for reusing frames;
     then a DTW warp (hold / step / skip one frame) lands each syllable of the take on the voice's;
  3. the IA lines and the gaps (Tony listens) take silent windows played forward then backward
     (ping-pong: no visible jump inside a long listen).

The take is matted once (take_alpha.webm) and written with the same frame list, so tony_src.mp4
(unmatted, for the segmentation reveal) and tony.webm (cutout) stay frame-identical.

  python3 resync.py TAKE30.mp4 TAKE30_AUDIO TAKE_ALPHA.webm BUILD_DIR
      TAKE30.mp4   the take at constant 30 fps;  TAKE30_AUDIO its sound;  BUILD_DIR has vo.json + voice.wav
"""
import json, os, shutil, subprocess, sys
import numpy as np

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FPS, SR = 30, 48000
take, take_audio, alpha, out = sys.argv[1:5]
vo = json.load(open(os.path.join(out, "vo.json")))
NF = round(vo["total"] * FPS)


def ff(*a):
    subprocess.run([FF, "-nostdin", "-v", "error", *a, "-y"], check=True)


def env(p):
    a = np.frombuffer(subprocess.check_output([FF, "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]), np.float32)
    h = SR // FPS
    n = len(a) // h
    db = 10 * np.log10((a[:n * h].reshape(n, h) ** 2).mean(1) + 1e-10)
    db -= np.percentile(db[db > -60], 90)                    # 0 dB = this track's speech level
    f = np.clip((db + 32) / 26, 0, 1)                        # 0 = closed mouth, 1 = full voice
    return np.convolve(f, np.ones(3) / 3, "same"), db > -26


ft, ont = env(take_audio)
fv, onv = env(os.path.join(out, "voice.wav"))
fv, onv = np.pad(fv, (0, max(0, NF - len(fv))))[:NF], np.pad(onv, (0, max(0, NF - len(onv))))[:NF]
TN = len(ft)

# ------------------------------------------------------------------ spans: runs of Tony's lines vs the rest
lines = vo["lines"]
spans = []                                                   # [a, b, kind]
for it in lines:
    a, b = round(it["start"] * FPS), round(it["end"] * FPS)
    kind = "talk" if it["who"] == "moi" else "sil"
    if spans and spans[-1][2] == kind and a - spans[-1][1] < 8:
        spans[-1][1] = b
        continue
    if spans and a > spans[-1][1]:
        spans.append([spans[-1][1], a, "sil"])
    elif not spans and a > 0:
        spans.append([0, a, "sil"])
    spans.append([a, b, kind])
if spans[-1][1] < NF:
    spans.append([spans[-1][1], NF, "sil"])
merged = []                                                  # a sil sliver < 8 frames joins the talk next to it
for s in spans:
    if merged and merged[-1][2] == s[2]:
        merged[-1][1] = s[1]
    elif s[2] == "sil" and s[1] - s[0] < 8 and merged and merged[-1][2] == "talk":
        merged[-1][1] = s[1]
    elif merged and merged[-1][2] == "sil" and merged[-1][1] - merged[-1][0] < 8 and s[2] == "talk" and len(merged) == 1:
        merged[-1] = [merged[-1][0], s[1], "talk"]
    else:
        merged.append(list(s))
spans = merged

used = np.zeros(TN)


def window_costs(a, b):
    L = b - a
    v, ov = fv[a:b], onv[a:b]
    return np.array([np.abs(ft[s:s + L] - v).mean() + 0.8 * (ont[s:s + L] != ov).mean() + 0.35 * (used[s:s + L] > 0).mean()
                     for s in range(0, TN - L)])


def best_window(a, b):
    """take start frame minimising the envelope mismatch with the voice on [a, b)"""
    c = window_costs(a, b)
    return float(c.min()), int(c.argmin())


SLACK, HOLD, SKIP = 8, 0.12, 0.12


def warp(a, b, s):
    """DTW: one take frame per output frame, monotone, steps of 0 (hold), 1 or 2 (skip) source frames,
    so each syllable of the take lands on the voice's syllable (local speed 0.5x-2x, mostly 1x)"""
    L = b - a
    j0, j1 = max(0, s - SLACK), min(TN, s + L + SLACK)
    M = j1 - j0
    C = np.abs(fv[a:b, None] - ft[None, j0:j1]) + 0.8 * (onv[a:b, None] != ont[None, j0:j1])
    # state h = consecutive holds so far (0..2): a held frame never lasts more than 2 frames (no visible freeze)
    D = np.full((L, 3, M), np.inf)
    B = np.zeros((L, 3, M), int)
    D[0, 0] = C[0] + 0.02 * np.abs(np.arange(M) - (s - j0))
    inf1, inf2 = np.full(1, np.inf), np.full(2, np.inf)
    for i in range(1, L):
        best = D[i - 1].min(0)
        step, skip = np.r_[inf1, best[:-1]], np.r_[inf2, best[:-2]] + SKIP
        D[i, 0] = C[i] + np.minimum(step, skip)
        B[i, 0] = np.where(step <= skip, 0, 1)
        D[i, 1] = C[i] + D[i - 1, 0] + HOLD
        D[i, 2] = C[i] + D[i - 1, 1] + HOLD
    j = int(D[-1].min(0).argmin())
    h = int(D[-1, :, j].argmin())
    path = [j]
    for i in range(L - 1, 0, -1):
        if h > 0:
            h -= 1
        else:
            j -= (1, 2)[B[i, 0, j]]
            h = int(D[i - 1, :, j].argmin())
        path.append(j)
    return float(D[-1].min() / L), [j0 + x for x in path[::-1]]


def fill_talk(a, b):
    """split [a, b) at the voice's pauses (<= 3 pieces), each piece on its best take window"""
    pauses, k = [], a + 20
    while k < b - 20:
        if not onv[k:k + 4].any():
            e = k
            while e < b and not onv[e]:
                e += 1
            pauses.append((k + e) // 2)
            k = e
        k += 1
    cands = [p for p in pauses if a + 20 <= p <= b - 20]
    one = best_window(a, b)
    plans = [(one[0], [(a, b, one[1])])]
    if b - a > 75:                                           # long runs: try one or two cuts at pauses
        for p in cands:
            l, r = best_window(a, p), best_window(p, b)
            c = (l[0] * (p - a) + r[0] * (b - p)) / (b - a) + 0.03
            plans.append((c, [(a, p, l[1]), (p, b, r[1])]))
        plans.sort(key=lambda x: x[0])
        if b - a > 150 and len(plans) > 1:
            for p in cands:
                for q in cands:
                    if q - p < 20:
                        continue
                    w = [best_window(x, y) for x, y in ((a, p), (p, q), (q, b))]
                    c = (w[0][0] * (p - a) + w[1][0] * (q - p) + w[2][0] * (b - q)) / (b - a) + 0.06
                    plans.append((c, [(a, p, w[0][1]), (p, q, w[1][1]), (q, b, w[2][1])]))
    plans.sort(key=lambda x: x[0])
    return plans[0]


# silent windows of the take (he listens): sound off for >= 0.6 s, 2 frames of margin
sil_w, k = [], 0
while k < TN:
    if not ont[k]:
        e = k
        while e < TN and not ont[e]:
            e += 1
        if e - k >= 18:
            sil_w.append((k + 2, e - 2))
        k = e
    k += 1
sil_w.sort(key=lambda w: -(w[1] - w[0]))
sil_w = sil_w[:6]

frames = []                                                  # take frame index for every output frame
report, rr = [], 0
for a, b, kind in spans:
    if kind == "talk":
        cost, plan = fill_talk(a, b)
        for x, y, _ in plan:
            c = window_costs(x, y)
            cands = []
            for s in np.argsort(c):                              # 4 distinct candidate windows, the warp decides
                if all(abs(s - t) > 10 for t in cands):
                    cands.append(int(s))
                if len(cands) == 4:
                    break
            wc, path, s = min((*warp(x, y, s), s) for s in cands)
            frames += path
            used[min(path):max(path) + 1] += 1
            m = (ont[path] != onv[x:y]).mean()
            report.append(f"talk {x / FPS:6.2f}-{y / FPS:6.2f}  take {s / FPS:6.2f}  on/off mismatch {m:4.0%}  warp {wc:.3f}")
    else:
        w0, w1 = sil_w[rr % len(sil_w)]; rr += 1
        k = 0
        for _ in range(b - a):                                   # ping-pong inside the silent window
            per = 2 * (w1 - w0 - 1)
            ph = k % per
            frames.append(w0 + (ph if ph < w1 - w0 else per - ph))
            k += 1
        report.append(f"sil  {a / FPS:6.2f}-{b / FPS:6.2f}  take {w0 / FPS:6.2f}-{w1 / FPS:6.2f} (ping-pong)")
print("\n".join(report))
frames = frames[:NF]
assert len(frames) == NF, len(frames)

# diagnostic: the rebuilt take sound against the voice, per Tony line
seq = ont[frames]
for it in lines:
    if it["who"] == "moi":
        a, b = round(it["start"] * FPS), round(it["end"] * FPS)
        print(f"  line {it['li']:2d} {it['start']:6.2f}  mouth/voice on-off mismatch {(seq[a:b] != onv[a:b]).mean():4.0%}  {it['text'][:40]}")
cuts = [round(j / FPS, 3) for j in range(1, NF) if abs(frames[j] - frames[j - 1]) > 3]
holds = sum(frames[j] == frames[j - 1] for j in range(1, NF))
print(f"{len(cuts)} cuts, {holds} held frames")


# ------------------------------------------------------------------ write the take (plain and matted) with the same frame list
W, H = 1080, 1440


def build(src, dst, alpha_):
    pix, fsz = ("yuva420p", W * H * 5 // 2) if alpha_ else ("yuv420p", W * H * 3 // 2)
    dec = ["-c:v", "libvpx-vp9"] if alpha_ else []
    enc = (["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "24", "-row-mt", "1", "-deadline", "good",
            "-cpu-used", "3", "-auto-alt-ref", "0"] if alpha_ else
           ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-g", "30", "-pix_fmt", "yuv420p"])
    p = subprocess.Popen([FF, "-nostdin", "-v", "error", "-f", "rawvideo", "-pix_fmt", pix, "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", *enc, dst, "-y"], stdin=subprocess.PIPE)
    runs, cur = [], [frames[0]]
    for f in frames[1:]:
        if abs(f - cur[-1]) <= 3:
            cur.append(f)
        else:
            runs.append(cur); cur = [f]
    runs.append(cur)
    for r in runs:
        lo, hi = min(r), max(r)
        raw = subprocess.check_output([FF, "-nostdin", "-v", "error", *dec, "-ss", f"{lo / FPS:.4f}", "-i", src, "-an",
                                       "-frames:v", str(hi - lo + 1), "-f", "rawvideo", "-pix_fmt", pix, "-"])
        got = len(raw) // fsz
        for f in r:
            k = min(f - lo, got - 1)
            p.stdin.write(raw[k * fsz:(k + 1) * fsz])
    p.stdin.close()
    assert p.wait() == 0


json.dump({"frames": NF, "cuts": cuts, "map": frames}, open(os.path.join(out, "tony_cuts.json"), "w"))
build(take, os.path.join(out, "tony_src.mp4"), False)
if os.path.exists(alpha):
    build(alpha, os.path.join(out, "tony.webm"), True)
print(f"done: {NF} frames")

#!/usr/bin/env python3
"""Two-state mouth variants for the hero, guaranteeing that ONLY the mouth changes.

The master sheet gives one closed/open pair for the sitting pose, but the two drawings are
not aligned (different framing, tail position) and the other poses only exist once.
Swapping whole images would make the body jump, so every pose gets a pair built here:

  * pair mode  (sitting pose): the OPEN drawing is registered onto the CLOSED one
    (scale + translation search on the eyes/nose area), then only the mouth patch
    (auto-detected from the difference, feathered) is pasted onto the closed image.
    -> <hero>_closed is the original, <hero>_talk_open = closed body + open mouth.
  * close mode (single poses): the open mouth inside a measured box is detected by
    colour distance to the muzzle skin, in-painted with skin (diffusion) and a soft
    smile line is drawn between the mouth corners.
    -> <pose>__open = the original drawing, <pose>__closed = procedural closed mouth.

Used by tools/slice_sheet.py; can also be run alone:
    python3 tools/mouth.py <LETTER>
"""
import json
import os
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _gray(a):
    return a[..., :3].mean(2)


def register(base, donor, region, scales=None, search=60):
    """Find (scale, dx, dy) so that donor resized by scale and pasted at (dx, dy) matches base in region."""
    x0, y0, x1, y1 = region
    tgt = _gray(base)[y0:y1, x0:x1]
    tmask = base[y0:y1, x0:x1, 3] > 200
    best = None
    dimg = Image.fromarray(donor.astype(np.uint8), "RGBA")
    for s in (scales if scales is not None else np.arange(0.86, 1.161, 0.02)):
        d = np.asarray(dimg.resize((round(dimg.width * s), round(dimg.height * s)), Image.BILINEAR)).astype(np.float64)
        dg = _gray(d)
        # coarse-to-fine translation search: correlate via SSD on a stride grid then refine
        best_local = (0, 0)
        for step in (4, 1):
            cands = []
            if step == 4:
                rng = [(dx, dy) for dx in range(-search, search + 1, 4) for dy in range(-search, search + 1, 4)]
            else:
                bx, by = best_local
                rng = [(bx + i, by + j) for i in range(-4, 5) for j in range(-4, 5)]
            for dx, dy in rng:
                # donor pixel (u, v) lands on base (u + dx, v + dy)
                u0, v0 = x0 - dx, y0 - dy
                if u0 < 0 or v0 < 0 or u0 + (x1 - x0) > dg.shape[1] or v0 + (y1 - y0) > dg.shape[0]:
                    continue
                patch = dg[v0:v0 + (y1 - y0), u0:u0 + (x1 - x0)]
                err = ((patch - tgt) ** 2)[tmask].mean()
                cands.append((err, dx, dy))
            if not cands:
                break
            e, bdx, bdy = min(cands)
            best_local = (bdx, bdy)
        if cands and (best is None or e < best[0]):
            best = (e, s, bdx, bdy)
    return best


def warp(donor, s, dx, dy, shape):
    dimg = Image.fromarray(donor.astype(np.uint8), "RGBA")
    d = dimg.resize((round(dimg.width * s), round(dimg.height * s)), Image.LANCZOS)
    canvas = Image.new("RGBA", (shape[1], shape[0]), (0, 0, 0, 0))
    canvas.paste(d, (dx, dy), d)
    return np.asarray(canvas).astype(np.float64)


def _largest(mask):
    h, w = mask.shape
    seen = np.zeros_like(mask)
    best = []
    for y0 in range(h):
        for x0 in range(w):
            if mask[y0, x0] and not seen[y0, x0]:
                comp, q = [], deque([(y0, x0)])
                seen[y0, x0] = True
                while q:
                    y, x = q.popleft()
                    comp.append((y, x))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            q.append((ny, nx))
                if len(comp) > len(best):
                    best = comp
    out = np.zeros_like(mask)
    for y, x in best:
        out[y, x] = True
    return out


def _fill_holes(mask):
    inv = ~mask
    h, w = mask.shape
    outside = np.zeros_like(mask)
    q = deque([(y, x) for y in range(h) for x in (0, w - 1) if inv[y, x]] + [(y, x) for x in range(w) for y in (0, h - 1) if inv[y, x]])
    for y, x in q:
        outside[y, x] = True
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and inv[ny, nx] and not outside[ny, nx]:
                outside[ny, nx] = True
                q.append((ny, nx))
    return ~outside


def _morph(mask, size, op):
    im = Image.fromarray((mask * 255).astype(np.uint8))
    f = ImageFilter.MaxFilter(size) if op == "dilate" else ImageFilter.MinFilter(size)
    return np.asarray(im.filter(f)) > 127


def skin_color(img, box):
    x, y, w, h = box
    ring = np.concatenate([img[y, x:x + w], img[y + h - 1, x:x + w], img[y:y + h, x], img[y:y + h, x + w - 1]])
    ok = ring[(ring[:, 3] > 200) & (ring[:, 0] > 150) & (ring[:, 0] >= ring[:, 1]) & (ring[:, 1] >= ring[:, 2])]
    return np.median(ok[:, :3], 0) if len(ok) else np.array([238.0, 196.0, 160.0])


def mouth_mask(img, box):
    """Open-mouth pixels: dark/red interior + pink tongue (green much lower than red, unlike
    the orange-brown fur) and the white teeth, restricted to the largest blob in box."""
    x, y, w, h = box
    reg = img[y:y + h, x:x + w, :3]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    lum = reg.mean(2)
    sat = reg.max(2) - reg.min(2)
    inner = (g < 0.55 * r) & (r > 50) & (b < 0.65 * r)
    teeth = (lum > 200) & (sat < 50)
    dark = (lum < 125) & (g < 0.7 * r)
    cand = inner | teeth | dark
    m = _largest(inner)
    for _ in range(12):  # region-grow from the red interior into teeth / dark gaps only
        grown = _morph(m, 3, "dilate") & cand
        if grown.sum() == m.sum():
            break
        m = grown | m
    m = _fill_holes(m)
    full = np.zeros(img.shape[:2], bool)
    full[y:y + h, x:x + w] = m
    return full, skin_color(img, box)


def pair_open(closed, opened, region, mouth_box):
    """closed body + registered open mouth patch."""
    err, s, dx, dy = register(closed, opened, region)
    w = warp(opened, s, dx, dy, closed.shape)
    x, y, bw, bh = mouth_box
    diff = np.sqrt(((w[..., :3] - closed[..., :3]) ** 2).sum(2))
    m = np.zeros(closed.shape[:2], bool)
    m[y:y + bh, x:x + bw] = (diff[y:y + bh, x:x + bw] > 40) & (w[y:y + bh, x:x + bw, 3] > 200)
    m = _fill_holes(_largest(_morph(m, 5, "dilate")))
    m = _morph(m, 7, "dilate")
    soft = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))) / 255.0
    out = closed.copy()
    out[..., :3] = closed[..., :3] * (1 - soft[..., None]) + w[..., :3] * soft[..., None]
    return out, {"scale": round(float(s), 3), "dx": int(dx), "dy": int(dy), "err": round(float(err), 1)}


def close_mouth(img, box, line=(96, 48, 34)):
    m, skin = mouth_mask(img, box)
    if m.sum() < 12:
        return img.copy(), {"note": "no mouth found"}
    ys, xs = np.nonzero(m)
    grow = _morph(m, 7, "dilate")
    out = img.copy()
    rgb = out[..., :3]
    rgb[grow] = skin
    # diffusion in-paint so the patch takes the local shading of the muzzle
    known = ~grow
    for _ in range(80):
        blur = np.asarray(Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(2))).astype(np.float64)
        rgb[grow] = blur[grow]
        rgb[known] = img[..., :3][known]
    # smile line from corner to corner, sagging at the middle (supersampled)
    left = (xs.min(), ys[xs == xs.min()].mean())
    right = (xs.max(), ys[xs == xs.max()].mean())
    hgt = ys.max() - ys.min()
    cx, cy = (left[0] + right[0]) / 2, (left[1] + right[1]) / 2
    k = 0.82  # a closed smile is a bit narrower than the laughing mouth
    left = (cx + (left[0] - cx) * k, cy + (left[1] - cy) * k)
    right = (cx + (right[0] - cx) * k, cy + (right[1] - cy) * k)
    vx, vy = right[0] - left[0], right[1] - left[1]
    n = np.hypot(vx, vy) or 1.0
    nx, ny = -vy / n, vx / n  # normal pointing down for a left->right line
    if ny < 0:
        nx, ny = -nx, -ny
    sag = max(3.0, 0.22 * n, 0.3 * hgt)
    mid = (cx + nx * sag, cy + ny * sag)
    ss = 4
    H, W = img.shape[:2]
    lay = Image.new("L", (W * ss, H * ss), 0)
    dr = ImageDraw.Draw(lay)
    pts = []
    for i in range(41):
        t = i / 40
        px = (1 - t) ** 2 * left[0] + 2 * (1 - t) * t * mid[0] + t ** 2 * right[0]
        py = (1 - t) ** 2 * left[1] + 2 * (1 - t) * t * mid[1] + t ** 2 * right[1]
        pts.append((px * ss, py * ss))
    width = max(2.5, 0.07 * (xs.max() - xs.min())) * ss
    dr.line(pts, fill=255, width=int(width), joint="curve")
    for p in (pts[0], pts[-1]):
        r = width / 2
        dr.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=255)
    feather = np.asarray(Image.fromarray((grow * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))) / 255.0
    feather = np.maximum(feather, m)
    rgb[:] = img[..., :3] * (1 - feather[..., None]) + rgb * feather[..., None]
    lay = np.asarray(lay.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.5))) / 255.0
    rgb[:] = rgb * (1 - lay[..., None]) + np.array(line) * lay[..., None]
    out[..., :3] = rgb
    return out, {"mouth_px": int(m.sum()), "corners": [list(map(float, left)), list(map(float, right))]}


def load(p):
    return np.asarray(Image.open(p).convert("RGBA")).astype(np.float64)


def save(a, p):
    Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8), "RGBA").save(p)


def build(cut_dir, mouths):
    """mouths = sheet_map["mouths"]. Writes <name>__closed.png / <name>__open.png for each pose."""
    report = {}
    for name, cfg in mouths.items():
        src = os.path.join(cut_dir, name + ".png")
        if not os.path.exists(src):
            continue
        img = load(src)
        if cfg.get("mode") == "pair":
            donor = os.path.join(cut_dir, cfg["open_from"] + ".png")
            out, info = pair_open(img, load(donor), cfg["register_region"], cfg["box"])
            save(img, os.path.join(cut_dir, name + "__closed.png"))
            save(out, os.path.join(cut_dir, name + "__open.png"))
        else:
            out, info = close_mouth(img, cfg["box"])
            save(out, os.path.join(cut_dir, name + "__closed.png"))
            save(img, os.path.join(cut_dir, name + "__open.png"))
        report[name] = info
    return report


if __name__ == "__main__":
    letter = sys.argv[1] if len(sys.argv) > 1 else "M"
    ep = os.path.join(ROOT, "episodes", letter)
    smap = json.load(open(os.path.join(ep, "sheet_map.json")))
    print(json.dumps(build(os.path.join(ep, "assets", "cut"), smap.get("mouths", {})), indent=1))

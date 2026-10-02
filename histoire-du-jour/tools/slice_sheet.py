#!/usr/bin/env python3
"""Cut an episode master sheet into individual assets.

    python3 tools/slice_sheet.py <LETTER> [--sheet path.png] [--map path.json]

Reads  episodes/<L>/sheet_map.json   (cells measured on the sheet, see README)
       episodes/<L>/assets/source/assets_master_sheet.png
Writes episodes/<L>/assets/cut/<name>.png  (+ _preview.png contact sheet)

The generated sheets have NO real alpha: the "transparent" areas are a printed light
checkerboard. Each cell is keyed out with numpy:
  * cutout : flood-fill of the light, low-saturation card colour from the cell borders,
             soft alpha on the outer ring only (whites inside the subject - teeth, snow,
             a white cat - are kept because the flood cannot reach them), colour
             un-mixing on the edge, then trimmed to the content and small stray
             fragments (neighbour items bleeding into the cell) are dropped.
  * glow   : soft alpha everywhere from the distance to the card colour (sparkles,
             halos) + un-mixing, so glows stay glows instead of grey blobs.
  * opaque : plain crop.
  * background : cell -> 9:16 cover crop around focusX -> Lanczos upscale to 1080x1920
             (the sheet thumbnails are ~240x340, so backgrounds are ~5.6x upscaled and soft).
Hero items ("hero": true) also get perfectly aligned two-state mouth variants
(<name>__closed.png / <name>__open.png) via tools/mouth.py when a "mouth" entry exists.
"""
import argparse
import json
import os
import shutil
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W, H = 1080, 1920


def load_map(letter, map_path=None):
    ep = os.path.join(ROOT, "episodes", letter)
    mp = map_path or os.path.join(ep, "sheet_map.json")
    if not os.path.exists(mp):  # fall back to the M reference layout
        mp = os.path.join(ROOT, "episodes", "M", "sheet_map.json")
    return ep, json.load(open(mp)), mp


def bg_color(cell):
    """Median colour of the light, desaturated pixels on the cell border (= card checker)."""
    b = np.concatenate([cell[:3].reshape(-1, 3), cell[-3:].reshape(-1, 3), cell[:, :3].reshape(-1, 3), cell[:, -3:].reshape(-1, 3)])
    sat = b.max(1) - b.min(1)
    lum = b.mean(1)
    ok = b[(sat < 30) & (lum > 170)]
    return np.median(ok, 0) if len(ok) > 10 else np.array([224.0, 224.0, 224.0])


def flood(mask_ok):
    """Pixels of mask_ok connected to the cell border (4-connectivity)."""
    h, w = mask_ok.shape
    out = np.zeros_like(mask_ok)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if mask_ok[y, x] and not out[y, x]:
                out[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if mask_ok[y, x] and not out[y, x]:
                out[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and mask_ok[ny, nx] and not out[ny, nx]:
                out[ny, nx] = True
                q.append((ny, nx))
    return out


def components(mask):
    """Label 8-connected components; returns (labels, sizes)."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    sizes = [0]
    n = 0
    for y0 in range(h):
        for x0 in range(w):
            if mask[y0, x0] and not lab[y0, x0]:
                n += 1
                cnt = 0
                q = deque([(y0, x0)])
                lab[y0, x0] = n
                while q:
                    y, x = q.popleft()
                    cnt += 1
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                                lab[ny, nx] = n
                                q.append((ny, nx))
                sizes.append(cnt)
    return lab, np.array(sizes)


def inset(cell, maxpx=8):
    """Drop dark card borders / gutters caught on the cell edges."""
    dark = cell.mean(2) < 110
    t = b = l = r = 0
    while t < maxpx and dark[t].mean() > 0.8: t += 1
    while b < maxpx and dark[-1 - b].mean() > 0.8: b += 1
    while l < maxpx and dark[:, l].mean() > 0.8: l += 1
    while r < maxpx and dark[:, -1 - r].mean() > 0.8: r += 1
    # include the 1-2 px anti-aliased transition
    t, b, l, r = [v + 2 if v else 0 for v in (t, b, l, r)]
    return cell[t:cell.shape[0] - b, l:cell.shape[1] - r]


def unmix(cell, alpha, bg):
    a = np.clip(alpha, 1e-3, 1)[..., None]
    bg = np.asarray(bg)
    fg = (cell - (1 - a) * bg) / a
    return np.clip(fg, 0, 255)


def _grow(seed, outside, ok, steps=3):
    """Extend a background hole by a few px into similar pixels (its anti-aliased rim)."""
    m = seed.copy()
    for _ in range(steps):
        g = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
        m = m | (g & ok)
    return m


def key_cutout(cell, t_flood=46.0, t_lo=24.0, t_hi=78.0, halo=False, holes=True, erode=True):
    bg = bg_color(cell)
    d = np.abs(cell - bg).max(2)
    sat = cell.max(2) - cell.min(2)
    lum = cell.mean(2)
    ok = (d < t_flood) & (sat < 40)
    if halo:  # pastel glow around glossy letters: bright, any tint
        ok |= (lum > 175) & (d < 95) & (cell.min(2) > 120)
        t_lo, t_hi = 40.0, 120.0
    outside = flood(ok)
    bgmap = np.broadcast_to(bg, cell.shape).copy()
    if holes:  # checker visible through enclosed gaps (arm/tail/backpack loops)
        # card colour, or the card in the subject's shadow (greyer, lum ~190); eye whites/teeth are brighter (>240)
        cand = (sat < 24) & (lum > 150) & (lum < 236) & ~outside
        lab, sizes = components(cand)
        for i in range(1, len(sizes)):
            if sizes[i] >= 30:
                m = lab == i
                if np.median(lum[m]) < 232:
                    local = np.median(cell[m], 0)
                    g = _grow(m, outside, (sat < 30) & (lum > 140))
                    outside |= g
                    bgmap[g] = local
    d = np.abs(cell - bgmap).max(2)
    # soft alpha only where the flood reached; everything else is subject
    alpha = np.where(outside, np.clip((d - t_lo) / (t_hi - t_lo), 0, 1), 1.0)
    # drop stray fragments (neighbour items, label specks)
    solid = alpha > 0.5
    lab, sizes = components(solid)
    if len(sizes) > 1:
        big = sizes[1:].max()
        keep = np.zeros(len(sizes), bool)
        keep[1:] = sizes[1:] >= max(40, 0.04 * big)
        # a fragment hugging the cell border and much smaller than the main body is a neighbour
        hh, ww = solid.shape
        for i in range(1, len(sizes)):
            if keep[i] and sizes[i] < 0.25 * big:
                ys, xs = np.nonzero(lab == i)
                if ys.min() == 0 or xs.min() == 0 or ys.max() == hh - 1 or xs.max() == ww - 1:
                    keep[i] = False
        kept = keep[lab]
        # grow the kept mask by 2 px so soft edges around kept parts survive
        grown = np.asarray(Image.fromarray((kept * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
        alpha = alpha * grown
    # light feather to kill the jaggies of the flood boundary
    a8 = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    alpha = np.minimum(alpha, np.asarray(a8) / 255.0 + (alpha >= 0.999) * 1.0)
    if erode:  # the sheet draws a pale "sticker" halo around subjects: eat 1 px of edge
        er = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))) / 255.0
        alpha = 0.35 * alpha + 0.65 * er
    rgb = unmix(cell, alpha, bgmap)
    return rgb, alpha


def key_glow(cell, t_lo=30.0, t_hi=110.0):
    bg = bg_color(cell)
    d = np.abs(cell - bg).max(2)
    alpha = np.clip((d - t_lo) / (t_hi - t_lo), 0, 1) ** 0.8
    rgb = unmix(cell, alpha, bg)
    # glows are emissive: brighten un-mixed colour a little so they read on dark scenes too
    return rgb, alpha


def trim(rgb, alpha, pad=4):
    ys, xs = np.nonzero(alpha > 0.03)
    if not len(ys):
        return rgb, alpha
    y0, y1 = max(0, ys.min() - pad), min(alpha.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(alpha.shape[1], xs.max() + pad + 1)
    return rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1]


def to_png(rgb, alpha, path, upscale=2):
    im = Image.fromarray(np.dstack([rgb, alpha * 255]).round().astype(np.uint8), "RGBA")
    if upscale > 1:
        im = im.resize((im.width * upscale, im.height * upscale), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    im.save(path)
    return im


def make_background(sheet, box, focus, path):
    x, y, w, h = box
    cell = sheet.crop((x, y, x + w, y + h))
    tw = h * W / H
    if tw <= w:
        cx = x + focus * w
        x0 = min(max(x, cx - tw / 2), x + w - tw)
        crop = sheet.crop((round(x0), y, round(x0 + tw), y + h))
    else:  # cell narrower than 9:16 -> crop height instead
        th = w * H / W
        crop = cell.crop((0, round((h - th) / 2), w, round((h + th) / 2)))
    big = crop.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=3))
    big.convert("RGB").save(path, quality=92)
    return crop.size


def preview(out_dir, names):
    tiles = []
    for n in names:
        p = os.path.join(out_dir, n + ".png")
        if not os.path.exists(p):
            p = os.path.join(out_dir, n + ".jpg")
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        im.thumbnail((220, 220))
        tiles.append(im)
    cols = 8
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 240, rows * 240), (40, 90, 60))
    for i, t in enumerate(tiles):
        cx, cy = (i % cols) * 240, (i // cols) * 240
        # half dark / half colour backdrop to judge fringes
        bgc = Image.new("RGB", (240, 240), (20, 24, 40) if (i // cols + i) % 2 else (90, 150, 210))
        sheet.paste(bgc, (cx, cy))
        sheet.paste(t, (cx + (240 - t.width) // 2, cy + (240 - t.height) // 2), t)
    sheet.save(os.path.join(out_dir, "_preview.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("letter")
    ap.add_argument("--sheet")
    ap.add_argument("--map")
    ap.add_argument("--only", help="comma-separated item names")
    ap.add_argument("--publish-hero", metavar="HERO_ID", help="also copy the hero items (+ mouth variants) to heroes/<HERO_ID>/")
    args = ap.parse_args()
    ep, smap, mp = load_map(args.letter, args.map)
    sheet_path = args.sheet or os.path.join(ep, "assets", "source", "assets_master_sheet.png")
    if not os.path.exists(sheet_path):
        sys.exit(f"missing sheet: {sheet_path}")
    sheet = Image.open(sheet_path).convert("RGB")
    rw, rh = smap.get("reference_size", sheet.size)
    sx, sy = sheet.width / rw, sheet.height / rh
    arr = np.asarray(sheet).astype(np.float64)
    out_dir = os.path.join(ep, "assets", "cut")
    os.makedirs(out_dir, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    report = {}
    for name, it in smap["items"].items():
        if only and name not in only:
            continue
        if it.get("skip"):  # e.g. Milo base poses on a new sheet: the heroes/<id>/ library is used instead
            continue
        x, y, w, h = it["box"]
        box = [round(x * sx), round(y * sy), round(w * sx), round(h * sy)]
        kind = it.get("kind", "cutout")
        if kind == "background":
            src = make_background(sheet, box, it.get("focusX", 0.5), os.path.join(out_dir, name + ".jpg"))
            report[name] = f"background from {src[0]}x{src[1]} -> {W}x{H} (x{H / src[1]:.1f} upscale)"
            continue
        cell = inset(arr[box[1]:box[1] + box[3], box[0]:box[0] + box[2]])
        if kind == "opaque":
            rgb, alpha = cell, np.ones(cell.shape[:2])
        elif kind == "glow":
            rgb, alpha = trim(*key_glow(cell))
        else:
            rgb, alpha = trim(*key_cutout(cell, t_flood=it.get("flood", 46.0), halo=it.get("halo", False), holes=it.get("holes", True), erode=it.get("erode", True)))
        im = to_png(rgb, alpha, os.path.join(out_dir, name + ".png"))
        report[name] = f"{kind} {im.width}x{im.height}"
    if smap.get("mouths"):
        sys.path.insert(0, HERE)
        import mouth
        for k, v in mouth.build(out_dir, {k: v for k, v in smap["mouths"].items() if not k.startswith("_")}).items():
            report[k + " (mouth)"] = json.dumps(v)
    if args.publish_hero:
        hdir = os.path.join(ROOT, "heroes", args.publish_hero)
        os.makedirs(hdir, exist_ok=True)
        for name, it in smap["items"].items():
            if it.get("hero"):
                for suf in ("", "__closed", "__open"):
                    p = os.path.join(out_dir, name + suf + ".png")
                    if os.path.exists(p):
                        shutil.copy(p, hdir)
        print(f"hero assets published to {hdir}")
    if not only:
        preview(out_dir, [n for n in smap["items"] if smap["items"][n].get("kind") != "background"])
    json.dump({"map": os.path.relpath(mp, ROOT), "sheet": os.path.relpath(sheet_path, ROOT), "items": report},
              open(os.path.join(out_dir, "_slice_report.json"), "w"), indent=1)
    for k, v in report.items():
        print(f"  {k:20s} {v}")


if __name__ == "__main__":
    main()

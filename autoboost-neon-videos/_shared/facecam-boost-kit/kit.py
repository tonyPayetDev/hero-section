"""FaceCam Boost kit - markup helpers for HyperFrames compositions generated in Python.

Pairs with kit.css (look) and kit.js (motion). Import from a project's gen.py:

    sys.path.insert(0, "<repo>/autoboost-neon-videos/_shared/facecam-boost-kit")
    import kit

Nothing here invents figures: stats and labels are passed in by the caller and
must come from what is said in the video.
"""
import html

ICON = {
    "warn": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 3 2 21h20L12 3z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><path d="M12 10v5M12 18v.5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z" fill="currentColor"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M6 2h8l5 5v15H6z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M14 2v5h5M9 12h7M9 16h7" stroke="currentColor" stroke-width="2"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><circle cx="12" cy="13" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 9v4l3 2M10 2h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><rect x="5" y="11" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    "gauge": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M4 18a8 8 0 1 1 16 0" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 18l4-6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "check": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="m5 12 5 5 9-10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "checkc": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="m7 12 3.5 3.5L17 9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "cross": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>',
    "rocket": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M14 4c3-1 6-1 6-1s0 3-1 6l-6 6-5-5 6-6z" fill="currentColor"/><path d="M8 11l-4 1 2-4 4-1M13 16l-1 4 4-2 1-4" fill="currentColor"/><circle cx="15.5" cy="8.5" r="1.4" fill="#0a0a0f"/></svg>',
    "send": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M3 11 21 3l-8 18-2-8-8-2z" fill="currentColor"/></svg>',
    "brain": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="currentColor"/><path d="M12 4v3M12 17v3M4 12h3M17 12h3" stroke="currentColor" stroke-width="2"/></svg>',
    "feather": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M20 4C10 4 6 10 5 19l3-3h5c4-2 6-7 7-12z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M5 19 14 10" stroke="currentColor" stroke-width="2"/></svg>',
    "down": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 4v15M6 13l6 6 6-6" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "up": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 20V5M6 11l6-6 6 6" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "trend": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M3 17l6-6 4 4 8-8M15 7h6v6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "gear": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9 7 7M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "bulb": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "crown": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M3 18 5 7l5 5 2-7 2 7 5-5 2 11z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "search": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>',
    "quote": '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M4 18v-5a6 6 0 0 1 6-6v3a3 3 0 0 0-3 3h3v5zM14 18v-5a6 6 0 0 1 6-6v3a3 3 0 0 0-3 3h3v5z" fill="currentColor"/></svg>',
}

SPARK = ('<svg class="fb-spark" viewBox="0 0 56 56"><path d="M10 46 22 20M26 50 46 34M30 40 52 14" stroke="{c}" '
         'stroke-width="4" stroke-linecap="round" style="filter:drop-shadow(0 0 6px {c})"/></svg>')


def icon(name, size=40):
    return ICON[name].replace("{s}", str(size))


def chars(text, cls=""):
    out = []
    for ch in text:
        if ch == " ":
            out.append('<span class="char sp">&nbsp;</span>')
        else:
            out.append(f'<span class="char{(" " + cls) if cls else ""}">{html.escape(ch)}</span>')
    return "".join(out)


def sticker(el_id, a, b, variant="gold", ico=None, deco=None, left=0, top=0):
    """Punch badge. variant gold | violet | red. deco: spark | bar | swoosh | None."""
    c = {"gold": "#eab308", "violet": "#a78bfa", "red": "#ff6b6b"}[variant]
    parts = []
    if ico:
        parts.append(f'<i class="fb-ico">{icon(ico, 58)}</i>')
    parts.append(f'<span class="a">{html.escape(a)}</span>')
    if b:
        parts.append(f'<span class="b">{html.escape(b)}</span>')
    if deco == "spark":
        parts.append(SPARK.replace("{c}", c))
    elif deco == "bar":
        parts.append('<i class="fb-bar"></i>')
    elif deco == "swoosh":
        parts.append('<i class="fb-swoosh"></i>')
    return (f'<div id="{el_id}" class="fb-sticker fb-{variant}" style="left:{left}px;top:{top}px">'
            + "".join(parts) + "</div>")


def level(el_id, n, total=6, label="NIVEAU", left=40, top=40):
    segs = "".join(f'<i class="{"on new" if i == n - 1 else ("on" if i < n else "")}"></i>' for i in range(total))
    return (f'<div id="{el_id}" class="fb-level" style="left:{left}px;top:{top}px">'
            f'<span>{label} {n}</span><span class="seg">{segs}</span></div>')


def chart_svg(points, w=880, h=300, label="100 %", label_at=-1):
    """Notion #3 curve. points: list of (x 0..1, y 0..1, 1 = top). Returns <svg>."""
    pad = 20
    P = [(pad + x * (w - 2 * pad), pad + (1 - y) * (h - 2 * pad)) for x, y in points]
    d = f"M {P[0][0]:.1f} {P[0][1]:.1f} " + " ".join(
        f"C {(a[0] + b[0]) / 2:.1f} {a[1]:.1f}, {(a[0] + b[0]) / 2:.1f} {b[1]:.1f}, {b[0]:.1f} {b[1]:.1f}"
        for a, b in zip(P, P[1:]))
    area = d + f" L {P[-1][0]:.1f} {h} L {P[0][0]:.1f} {h} Z"
    grid = "".join(f'<line class="fb-gridline" x1="0" x2="{w}" y1="{y}" y2="{y}"/>' for y in range(0, h + 1, h // 4))
    lx, ly = P[label_at]
    return (f'<svg class="fb-chart" width="{w}" height="{h + 60}" viewBox="0 -60 {w} {h + 60}" style="overflow:visible">'
            '<defs><linearGradient id="fbArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6" stop-opacity=".45"/>'
            '<stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></linearGradient></defs>'
            f'{grid}<path class="fb-area" d="{area}" fill="url(#fbArea)"/><path class="fb-line" d="{d}"/>'
            f'<circle class="fb-dot" cx="{lx:.1f}" cy="{ly:.1f}" r="14" fill="#eab308" stroke="#0a0a0f" stroke-width="4" style="filter:drop-shadow(0 0 12px #eab308)"/>'
            f'<g class="fb-label"><rect x="{min(lx - 75, w - 150):.1f}" y="{ly - 78:.1f}" width="150" height="50" rx="12" fill="#0a0a0f" stroke="#eab308" stroke-width="3"/>'
            f'<text x="{min(lx - 75, w - 150) + 75:.1f}" y="{ly - 44:.1f}" text-anchor="middle" font-family="AB Sans" font-weight="700" font-size="28" fill="#eab308">{html.escape(label)}</text></g>'
            '</svg>')


def elastic(text, cls="fb-g"):
    return ('<span class="fb-elastic">' + "".join(
        f'<span class="fb-ech {cls}">{html.escape(c)}</span>' for c in text) + "</span>")


def facecam_mode(box, focus, crop_h=None, radius=0, src=(1080, 1440)):
    """Transform + clip that shows a source region inside a canvas box.

    box    (x, y, w, h) on the 1080x1920 canvas
    focus  (cx, cy) source point to centre (usually the face)
    crop_h source height to show (default: as much as fits) - smaller = tighter
    radius corner radius in canvas px; radius = w/2 on a square box -> circle
    The <video> keeps transform-origin 0 0; clip-path is in source pixels.
    """
    sw, sh = src
    bx, by, bw, bh = box
    ar = bw / bh
    ch = min(sh, sw / ar) if crop_h is None else min(crop_h, sh, sw / ar)
    cw = ch * ar
    cx0 = min(max(focus[0] - cw / 2, 0), sw - cw)
    cy0 = min(max(focus[1] - ch / 2, 0), sh - ch)
    s = bw / cw
    r = radius / s
    clip = (f"inset({cy0:.1f}px {sw - cx0 - cw:.1f}px {sh - cy0 - ch:.1f}px {cx0:.1f}px "
            f"round {r:.1f}px)")
    return {"x": round(bx - cx0 * s, 2), "y": round(by - cy0 * s, 2), "scale": round(s, 5), "clip": clip}

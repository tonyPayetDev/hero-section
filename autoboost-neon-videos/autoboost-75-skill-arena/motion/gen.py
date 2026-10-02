#!/usr/bin/env python3
"""autoboost-75 Skill Arena - HyperFrames composition on the FaceCam Boost kit.

Driven by ../asm/timeline.json (assemble.py): MOI items = Tony's cut take, IA
items = his avatar answering (Tony frozen + dimmed, avatar card + speech bubble).
Screens follow the script blocks; every reveal is pinned to a word of the script.
"""
import json, os, re, html, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
KIT = os.path.abspath(os.path.join(PROJ, "..", "_shared", "facecam-boost-kit"))
sys.path.insert(0, KIT)
from kit import icon, chars, sticker, chart_svg, elastic, facecam_mode  # noqa: E402

ASM = os.environ.get("ASM", os.path.join(PROJ, "asm"))
TL = json.load(open(os.path.join(ASM, "timeline.json")))
TOTAL = TL["total"]
FPS = 30
ITEMS = TL["items"]

def q(t):
    return round(round(t * FPS) / FPS, 4)

# ------------------------------------------------------------------ words by script line
W = {}
for it in ITEMS:
    if it["kind"] == "moi":
        for w in it["words"]:
            W.setdefault(w["li"], []).append(w)

def wt(li, k=0):
    ws = W[li]
    return ws[min(k, len(ws) - 1)]["s"]

def wend(li):
    return W[li][-1]["e"]

def wfind(li, needle, after=0):
    for i, w in enumerate(W[li]):
        if i >= after and needle.lower() in w["w"].lower():
            return w["s"]
    return wt(li, after)

# ------------------------------------------------------------------ groups (blocks of the script)
TAGMAP = {"": "redemande"}
groups = []
for it in ITEMS:
    if it["kind"] != "moi":
        continue
    tag = TAGMAP.get(it["tag"], it["tag"])
    if not groups or groups[-1]["tag"] != tag:
        groups.append({"tag": tag, "start": it["start"]})
for g, nxt in zip(groups, groups[1:] + [None]):
    g["end"] = nxt["start"] if nxt else TOTAL
G = {g["tag"]: g for g in groups}

FACE = (540, 690)
MODES = {
    "FULL": facecam_mode((0, 0, 1080, 1920), FACE),
    "RECT": facecam_mode((24, 1000, 1032, 920), (540, 700), crop_h=920, radius=34),
    "CIRCLE": facecam_mode((220, 1100, 640, 640), FACE, crop_h=900, radius=320),
    "BIG": facecam_mode((160, 980, 760, 760), FACE, crop_h=900, radius=380),
}
MODE = {"hook": "FULL", "redemande": "RECT", "arena": "CIRCLE", "flow": "RECT", "agents": "RECT", "duel": "CIRCLE",
        "fast": "RECT", "lance": "CIRCLE", "install": "RECT", "cta": "BIG", "fin": "FULL"}

# ------------------------------------------------------------------ JS helpers
js = []
def R(sel, t, frm, to, d=0.45, ease="power3.out"):
    dest = dict(to, duration=d, ease=ease, immediateRender=False)
    js.append(f'tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(dest)},{q(t)});')

def S(sel, t, props):
    js.append(f'tl.set({json.dumps(sel)},{json.dumps(props)},{q(t)});')

def up(sel, t, d=0.42, dist=40):
    R(sel, t, {"opacity": 0, "y": dist}, {"opacity": 1, "y": 0}, d)

def pop(sel, t, d=0.36):
    R(sel, t, {"opacity": 0, "scale": 0.5}, {"opacity": 1, "scale": 1}, d, "back.out(2.2)")

def stamp(sel, t, rot=-8):
    R(sel, t, {"opacity": 0, "scale": 2.2, "rotation": rot - 10}, {"opacity": 1, "scale": 1, "rotation": rot}, 0.3, "power4.in")

def kin(sel, t, stagger=0.03, d=0.4):
    js.append(f'tl.fromTo({json.dumps(sel + " .char")},{{opacity:0,y:46,scale:.6}},'
              f'{{opacity:1,y:0,scale:1,duration:{d},ease:"back.out(1.8)",stagger:{stagger},immediateRender:false}},{q(t)});')

def draw(sel, t, d=0.5, all_=False):
    pick = f"document.querySelectorAll({json.dumps(sel)})" if all_ else f"[document.querySelector({json.dumps(sel)})]"
    js.append(f'(function(){{var els={pick};for(var i=0;i<els.length;i++){{var el=els[i];if(!el)continue;var L=el.getTotalLength();'
              f'tl.fromTo(el,{{strokeDasharray:L,strokeDashoffset:L}},{{strokeDashoffset:0,duration:{d},ease:"power2.inOut",immediateRender:false}},{q(t)}+i*0.08);}}}})();')

def fb(call):
    js.append("FB." + call + ";")

# ------------------------------------------------------------------ facecam modes per block
first = MODES[MODE[groups[0]["tag"]]]
S("#facecam", 0, {"x": first["x"], "y": first["y"], "scale": first["scale"], "transformOrigin": "0px 0px", "clipPath": first["clip"]})
for a, b in zip(groups, groups[1:]):
    fa, fbm = MODES[MODE[a["tag"]]], MODES[MODE[b["tag"]]]
    if fa is fbm:
        continue
    R("#facecam", b["start"] - 0.25, {"x": fa["x"], "y": fa["y"], "scale": fa["scale"], "clipPath": fa["clip"]},
      {"x": fbm["x"], "y": fbm["y"], "scale": fbm["scale"], "clipPath": fbm["clip"]}, 0.5, "power3.inOut")

# ring follows the circle blocks, frame + seam line follow the stacked blocks
for g in groups:
    m = MODE[g["tag"]]
    if m in ("CIRCLE", "BIG"):
        if m == "BIG":
            S("#ring-pos", g["start"] - 0.3, {"y": -60, "scale": 1.1875})
        else:
            S("#ring-pos", g["start"] - 0.3, {"y": 0, "scale": 1})
        R("#ring", g["start"] + 0.2, {"opacity": 0, "scale": 0.82}, {"opacity": 1, "scale": 1}, 0.45, "back.out(1.6)")
        R("#ring", g["end"] - 0.3, {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 1.15}, 0.3, "power2.in")
    if m == "RECT":
        R(".rect-fx", g["start"] + 0.2, {"opacity": 0}, {"opacity": 1}, 0.35, "power2.out")
        R(".rect-fx", g["end"] - 0.3, {"opacity": 1}, {"opacity": 0}, 0.3, "power2.in")
draw("#ring-main", G["arena"]["start"] + 0.2, 0.7)
R("#arc-a", 0, {"rotation": 0}, {"rotation": 1440}, TOTAL, "none")
R("#arc-b", 0, {"rotation": 0}, {"rotation": -1800}, TOTAL, "none")
R("#arc-c", 0, {"rotation": 30}, {"rotation": 990}, TOTAL, "none")
R("#glow-a", 0, {"x": 0, "y": 0}, {"x": 160, "y": 220}, TOTAL, "sine.inOut")
R("#glow-b", 0, {"x": 0, "y": 0}, {"x": -140, "y": -180}, TOTAL, "sine.inOut")
draw("#bg-curve", 0.2, 2.4)

# ------------------------------------------------------------------ screens slide in / out
SCREEN_TAGS = [g["tag"] for g in groups if MODE[g["tag"]] != "FULL"]
for g in groups:
    if MODE[g["tag"]] == "FULL":
        continue
    R(f"#sc-{g['tag']}", g["start"] - 0.28, {"x": 1080}, {"x": 0}, 0.5, "power4.out")
    R(f"#sc-{g['tag']}", g["end"] - 0.28, {"x": 0}, {"x": -1080}, 0.45, "power3.in")
    R("#streak", g["start"] - 0.34, {"x": 1300, "opacity": 1}, {"x": -1500, "opacity": 1}, 0.42, "power2.inOut")

# ------------------------------------------------------------------ IA interjections
ia_items = [it for it in ITEMS if it["kind"] == "ia"]
AV_SCALE = 560 / 720
SIDES = {"right": (490, 420), "left": (30, 420)}
bubbles = []
for n, it in enumerate(ia_items):
    t0, t1 = it["start"], it["start"] + it["dur"]
    side = "right" if n % 2 == 0 else "left"
    x, y = SIDES[side]
    off = 1080 if side == "right" else -600
    R("#ia-dim", t0, {"opacity": 0}, {"opacity": 1}, 0.16, "power2.out")
    R("#ia-dim", t1 - 0.16, {"opacity": 1}, {"opacity": 0}, 0.16, "power2.in")
    R("#capbar", t0, {"opacity": 1}, {"opacity": 0}, 0.12, "power2.out")
    R("#capbar", t1 - 0.1, {"opacity": 0}, {"opacity": 1}, 0.15, "power2.out")
    if n == 0:  # "apparaît brusquement": glitch slam, no slide
        for k, (dx, op) in enumerate([(40, 1), (-60, .4), (24, 1), (-12, .7), (0, 1)]):
            S("#avatar", t0 + k * 0.04, {"x": x + dx, "y": y, "scale": AV_SCALE, "opacity": op})
            S("#av-frame", t0 + k * 0.04, {"x": x + dx, "y": y, "opacity": op, "skewX": [-8, 6, -3, 2, 0][k]})
        R("#flash", t0, {"opacity": 0.85}, {"opacity": 0}, 0.25, "power2.out")
    else:
        R("#avatar", t0, {"x": off, "y": y, "scale": AV_SCALE, "opacity": 1}, {"x": x, "y": y, "scale": AV_SCALE, "opacity": 1}, 0.32, "power4.out")
        R("#av-frame", t0, {"x": off, "y": y, "opacity": 1, "skewX": 0}, {"x": x, "y": y, "opacity": 1, "skewX": 0}, 0.32, "power4.out")
    R("#avatar", t1 - 0.2, {"opacity": 1}, {"opacity": 0}, 0.18, "power2.in")
    R("#av-frame", t1 - 0.2, {"opacity": 1}, {"opacity": 0}, 0.18, "power2.in")
    R("#ia-bubble", t0 + 0.05, {"opacity": 0, "y": -30, "scale": 0.94}, {"opacity": 1, "y": 0, "scale": 1}, 0.25, "back.out(1.8)")
    R("#ia-bubble", t1 - 0.2, {"opacity": 1}, {"opacity": 0}, 0.18, "power2.in")
    # bubble words: TTS speaks at an even pace - spread over the voice, a beat longer on "…" and ","
    words = it["text"].replace("« ", "").replace(" »", "").split()
    weights = [len(w) + (6 if w.endswith("…") else 3 if w.endswith((",", "?", ".")) else 1) for w in words]
    tot = sum(weights)
    ts, acc = [], it["start"] + it["voice_at"]
    for w, wg in zip(words, weights):
        ts.append(acc); acc += it["voice_dur"] * wg / tot
    bid = f"b{n}"
    bubbles.append(f'<div class="bub" id="{bid}">' + "".join(
        f'<span class="bw" id="{bid}w{i}">{html.escape(w)}</span>' for i, w in enumerate(words)) + "</div>")
    S(f"#{bid}", t0, {"opacity": 1})
    S(f"#{bid}", t1, {"opacity": 0})
    for i, tw in enumerate(ts):
        S(f"#{bid}w{i}", tw, {"color": "#c4b5fd", "textShadow": "0 0 18px rgba(139,92,246,.9)"})
        nxt = ts[i + 1] if i + 1 < len(ts) else t1
        S(f"#{bid}w{i}", nxt, {"color": "#EDEDED", "textShadow": "0 0 0px rgba(139,92,246,0)"})
IA = {it["tag"]: it for it in ia_items}

# ------------------------------------------------------------------ captions (MOI only)
KEY = {"Claude", "ARENA", "ARENA,", "Arena.", "Arena", "l'Arena.", "l'Arena", "sous-agents.", "prompt", "prompt.",
       "éclatée…", "quinze", "challengée,", "comparée", "améliorée.", "2026."}
cap_html, cap_js = [], []
ci = 0
for it in ITEMS:
    if it["kind"] != "moi":
        continue
    chunks, cur = [], []
    for w in it["words"]:
        probe = " ".join(x["w"] for x in cur + [w])
        ends = bool(cur) and re.search(r"[.,!?:…]$", cur[-1]["w"])
        if cur and (len(probe) > 24 or (ends and len(" ".join(x["w"] for x in cur)) >= 12)):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    end_item = it["start"] + it["dur"]
    for k, ch in enumerate(chunks):
        a = ch[0]["s"] - 0.04
        b = chunks[k + 1][0]["s"] - 0.04 if k + 1 < len(chunks) else end_item - 0.02
        spans = [f'<span id="c{ci}w{j}" class="{"cw key" if w["w"] in KEY else "cw"}">{html.escape(w["w"])}</span>' for j, w in enumerate(ch)]
        cap_html.append(f'<div class="cap" id="c{ci}">{" ".join(spans)}</div>')
        cap_js.append(f'tl.fromTo("#c{ci}",{{opacity:0,y:14,scale:.96}},{{opacity:1,y:0,scale:1,duration:.12,ease:"power2.out",immediateRender:false}},{q(max(0, a))});')
        cap_js.append(f'tl.set("#c{ci}",{{opacity:0}},{q(b)});')
        for j, w in enumerate(ch):
            base = "#a78bfa" if w["w"] in KEY else "#EDEDED"
            nxt = min(ch[j + 1]["s"] if j + 1 < len(ch) else b, b)
            cap_js.append(f'tl.set("#c{ci}w{j}",{{color:"#eab308",textShadow:"0 0 18px rgba(234,179,8,.8)"}},{q(w["s"])});')
            cap_js.append(f'tl.set("#c{ci}w{j}",{{color:"{base}",textShadow:"0 0 0px rgba(234,179,8,0)"}},{q(nxt)});')
        ci += 1

# ------------------------------------------------------------------ markup helpers
def screen(tag, inner):
    g = G[tag]
    a, b = q(max(0, g["start"] - 0.3)), q(min(TOTAL, g["end"] + 0.3))
    track = 2 if SCREEN_TAGS.index(tag) % 2 == 0 else 3
    return (f'<section id="sc-{tag}" class="screen clip" data-start="{a}" data-duration="{q(b - a)}" '
            f'data-track-index="{track}"><div class="inner">{inner}</div></section>')

def pill(text, kind="gold", ico=None):
    return f'<div class="row" style="top:56px"><div class="pill {kind}">{icon(ico, 30) if ico else ""}<span>{text}</span></div></div>'

def head(l1, l2, top=150, size=88, size2=None):
    return (f'<div class="row" style="top:{top}px"><div class="hd"><div class="l1" style="font-size:{size}px">{l1}</div>'
            f'<div class="l2" style="font-size:{size2 or size}px">{l2}</div></div></div>')

AGENT = ('<svg viewBox="0 0 40 40" width="{s}" height="{s}"><rect x="5" y="9" width="30" height="24" rx="8" fill="currentColor" opacity=".18" stroke="currentColor" stroke-width="2.5"/>'
         '<circle cx="15" cy="21" r="3.2" fill="currentColor"/><circle cx="25" cy="21" r="3.2" fill="currentColor"/>'
         '<path d="M20 9V4M17 4h6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>')

def wire(d, color, cls):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" '
            f'style="filter:drop-shadow(0 0 8px {color}) drop-shadow(0 0 18px {color})"/>')

def zig(x0, y0, x1, y1, amp=10, waves=5):
    """electric connector: a sine wiggle between two points (refs 1-3, in gold/violet)."""
    import math
    pts, n = [], 40
    for i in range(n + 1):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1
        off = amp * math.sin(t * waves * 2 * math.pi) * math.sin(t * math.pi)
        pts.append((x - dy / L * off, y + dx / L * off))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)

screens, overlays = [], []

# ---- hook (full-bleed) -----------------------------------------------------
g = G["hook"]
overlays.append(
    f'<section id="ov-hook" class="hook clip" data-start="0" data-duration="{q(g["end"] + 0.4)}" data-track-index="4">'
    '<div id="shade"></div>'
    f'<div class="row" style="top:120px"><div class="hd"><div id="h-l1" class="l1" style="font-size:92px">{chars("SI CLAUDE TE DONNE", "w")}</div>'
    f'<div id="h-l2" class="l2" style="font-size:96px">{chars("UNE RÉPONSE", "w")}</div>'
    f'<div id="h-l3" class="l2 shard" style="font-size:150px">{chars("ÉCLATÉE", "g")}</div></div></div></section>')
kin("#h-l1", wt(0, 0), 0.025)
kin("#h-l2", wfind(0, "une"), 0.03)
kin("#h-l3", wfind(0, "éclat"), 0.05, 0.45)
# the word cracks: each letter is knocked off its line (seeded offsets, deterministic)
shards = [(-14, -18, -9), (10, 12, 7), (-6, 22, -12), (16, -10, 10), (-18, 8, -6), (8, -22, 13), (-10, 14, -8)]
for i, (dx, dy, r) in enumerate(shards):
    R(f"#h-l3 .char:nth-child({i + 1})", wfind(0, "éclat") + 0.55, {"x": 0, "y": 0, "rotation": 0},
      {"x": dx, "y": dy, "rotation": r}, 0.18, "power4.out")
R("#shade", g["end"] + 0.1, {"opacity": 1}, {"opacity": 0}, 0.3, "power2.out")

# ---- redemande: Claude chat, the prompts pile up ------------------------------
screens.append(screen("redemande",
    pill("LE RÉFLEXE", "red", "warn")
    + head(chars("REDEMANDER", "w"), chars("15 FOIS", "r"), 150, 92, 112)
    + '<div class="row" style="top:420px"><div class="win chat">'
      '<div class="bar"><i class="d1"></i><i class="d2"></i><i class="d3"></i><span>Claude</span><b>RÉPONSE ÉCLATÉE</b></div>'
      '<div class="ans"><i style="width:82%"></i><i style="width:46%;margin-left:30%"></i><i style="width:64%"></i><i style="width:28%;margin-left:52%"></i></div>'
      '<div class="ub u0">améliore ça…</div><div class="ub u1">recommence…</div><div class="ub u2">sois plus intelligent…</div>'
      '<div class="cnt">× 15</div></div></div>'))
R("#sc-redemande .pill", G["redemande"]["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
up("#sc-redemande .win", G["redemande"]["start"] + 0.25)
kin("#sc-redemande .l1", wt(4, 0)); kin("#sc-redemande .l2", wfind(4, "quinze"), 0.05)
pop("#sc-redemande .cnt", wfind(4, "quinze"))
for i, li in enumerate((5, 6, 7)):
    R(f"#sc-redemande .u{i}", wt(li, 0), {"opacity": 0, "x": 120, "scale": .9}, {"opacity": 1, "x": 0, "scale": 1}, 0.32, "back.out(1.8)")
overlays.append(sticker("st-bref", "BREF", ".", "violet", None, "spark", left=40, top=1050))
fb(f'sticker(tl,"#st-bref",{q(wt(3, 0))},{q(wend(3) + 0.6)},-4)')

# ---- arena: several Claude versions, one problem -> SKILL ARENA ----------------
ga = G["arena"]
screens.append(screen("arena",
    pill("LA SOLUTION", "gold", "bolt")
    + head(chars("PLUSIEURS CLAUDE", "w"), chars("MÊME PROBLÈME", "g"), 150, 84)
    + '<div class="vs-zone">'
      '<svg class="aw" width="1080" height="560" viewBox="0 0 1080 560">'
      + "".join(wire(zig(x, y, 540, 300, 9, 4), "#8b5cf6", f"aw{i}") for i, (x, y) in enumerate([(180, 90), (900, 90), (180, 500), (900, 500)]))
      + '</svg>'
      + "".join(f'<div class="cl cl{i}" style="left:{x - 110}px;top:{y - 44}px">{icon("brain", 34)}<b>CLAUDE #{i + 1}</b></div>'
                for i, (x, y) in enumerate([(180, 90), (900, 90), (180, 500), (900, 500)]))
      + f'<div class="pb">{icon("doc", 46)}<b>LE MÊME<br>PROBLÈME</b></div>'
      + '<canvas id="arena-p" class="fb-particles" width="1000" height="300" style="left:40px;top:150px"></canvas>'
      '</div>'))
R("#sc-arena .pill", ga["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
kin("#sc-arena .l1", wt(9, 1)); kin("#sc-arena .l2", wfind(9, "même"), 0.04)
pop("#sc-arena .pb", wfind(9, "problème") - 0.2)
for i in range(4):
    pop(f"#sc-arena .cl{i}", wfind(9, "plusieurs") + i * 0.12)
draw("#sc-arena .aw path", wfind(9, "versions"), 0.45, all_=True)
R("#sc-arena .cl, #sc-arena .pb, #sc-arena .aw", wt(10, 0), {"opacity": 1}, {"opacity": 0}, 0.3, "power2.in")
fb(f'particles(tl,"#arena-p","SKILL ARENA",{q(wt(10, 1))},{{font:"700 150px AB Sans",step:7,r:2.6,dIn:0.9,seed:5}})')

# ---- flow: one task -> the Arena -> an army of sub-agents (refs 1-3) ----------
gf = G["flow"]
AG_Y = [70, 170, 270, 370, 470]
screens.append(screen("flow",
    pill("LE PRINCIPE", "violet", "bolt")
    + head(chars("UNE SEULE TÂCHE", "w"), chars("UNE ARMÉE D'AGENTS", "g"), 150, 80, 76)
    + '<div class="flow-zone"><svg class="fw" width="1080" height="560" viewBox="0 0 1080 560">'
      + wire(zig(250, 270, 430, 270, 10, 4), "#eab308", "f0")
      + "".join(wire(zig(650, 270, 790, y, 8, 3), "#8b5cf6", f"f{i + 1}") for i, y in enumerate(AG_Y))
      + '</svg>'
      + f'<div class="nd n-task" style="left:40px;top:200px">{icon("doc", 46)}<b>1 TÂCHE</b><i class="bz">{icon("bolt", 22)}</i></div>'
      + f'<div class="nd n-arena" style="left:430px;top:180px">{icon("brain", 60)}<b>ARENA</b></div>'
      + "".join(f'<div class="ag ag{i}" style="left:790px;top:{y - 34}px">{AGENT.replace("{s}", "44")}<b>sous-agent</b></div>'
                for i, y in enumerate(AG_Y))
      + '</div>'))
R("#sc-flow .pill", gf["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
kin("#sc-flow .l1", wt(13, 0)); kin("#sc-flow .l2", wfind(14, "armée"), 0.03)
pop("#sc-flow .n-task", wt(13, 0))
draw("#sc-flow .f0", wfind(14, "Arena") - 0.1, 0.35)
pop("#sc-flow .n-arena", wfind(14, "Arena") + 0.15)
draw("#sc-flow .fw path:not(.f0)", wfind(14, "armée"), 0.3, all_=True)
for i in range(5):
    R(f"#sc-flow .ag{i}", wfind(14, "armée") + 0.15 + i * 0.08, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0}, 0.3, "back.out(2)")
js.append('tl.fromTo("#sc-flow .fw path",{strokeDasharray:"18 14"},{strokeDashoffset:-320,duration:%s,ease:"none",immediateRender:false},%s);'
          % (q(gf["end"] - wfind(14, "armée") - 0.5), q(wfind(14, "armée") + 0.5)))

# ---- agents: they multiply, then split into three strategies -----------------
gg = G["agents"]
cells = []
for r in range(6):
    for c in range(8):
        k = r * 8 + c
        cells.append(f'<i class="cell k{k} band{r // 2}" style="left:{c * 78}px;top:{r * 84}px">{AGENT.replace("{s}", "62")}</i>')
screens.append(screen("agents",
    pill("L'ARMÉE", "gold", "bolt")
    + head(chars("CHACUN", "w"), chars("SA STRATÉGIE", "g"), 150, 88)
    + '<div class="grid48">' + "".join(cells) + '</div>'
    + '<div class="bands">'
      f'<div class="bl b0">{icon("feather", 30)}<span>LA PLUS SIMPLE</span></div>'
      f'<div class="bl b1">{icon("search", 30)}<span>LES FAILLES</span></div>'
      f'<div class="bl b2">{icon("gear", 30)}<span>AUTRE STRATÉGIE</span></div></div>'))
R("#sc-agents .pill", gg["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
kin("#sc-agents .l1", gg["start"] + 0.2); kin("#sc-agents .l2", gg["start"] + 0.45)
# "multiplication rapide": 1, 2, 4, 8, 16, 32, 48 - each wave 0.16 s apart
order, t = [], gg["start"] + 0.35
for wave, upto in enumerate([1, 2, 4, 8, 16, 32, 48]):
    for k in range(len(order), upto):
        order.append(k)
        R(f"#sc-agents .k{k}", t, {"opacity": 0, "scale": 0.2}, {"opacity": 1, "scale": 1}, 0.22, "back.out(3)")
    t += 0.16
COL = {"gold": ("#eab308", "rgba(234,179,8,.8)"), "red": ("#ff6b6b", "rgba(255,107,107,.8)"), "violet": ("#a78bfa", "rgba(139,92,246,.9)")}
for b, (li, cls) in enumerate([(15, "gold"), (16, "red"), (17, "violet")]):
    tb = wt(li, 0) + 0.1
    c, glow = COL[cls]
    R(f"#sc-agents .band{b}", tb, {"color": "#6b6782", "filter": "drop-shadow(0 0 0px rgba(0,0,0,0))"},
      {"color": c, "filter": f"drop-shadow(0 0 8px {glow})"}, 0.25, "power2.out")
    R(f"#sc-agents .b{b}", tb, {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0}, 0.35, "back.out(2)")

# ---- duel: compare, criticise, eliminate --------------------------------------
gd = G["duel"]
R1 = [(40, 410 + i * 66 + (i // 2) * 14) for i in range(8)]
R2 = [(360, (R1[2 * i][1] + R1[2 * i + 1][1]) / 2) for i in range(4)]
R3 = [(640, (R2[2 * i][1] + R2[2 * i + 1][1]) / 2) for i in range(2)]
WIN = (880, (R3[0][1] + R3[1][1]) / 2)
def br(a, b):
    return f"M {a[0] + 200} {a[1] + 26} C {a[0] + 240} {a[1] + 26}, {b[0] - 40} {b[1] + 26}, {b[0]} {b[1] + 26}"
lines_html = ("".join(f'<path class="dl1" d="{br(R1[i], R2[i // 2])}"/>' for i in range(8))
              + "".join(f'<path class="dl2" d="{br(R2[i], R3[i // 2])}"/>' for i in range(4))
              + "".join(f'<path class="dl3" d="{br(R3[i], WIN)}"/>' for i in range(2)))
LOSE1, LOSE2, LOSE3 = [1, 2, 5, 6], [1, 2], [1]
screens.append(screen("duel",
    pill("LE TOURNOI", "red", "warn")
    + head(chars("COMPARÉES", "w"), chars("ÉLIMINÉES", "r"), 150, 88)
    + f'<svg class="dsvg" width="1080" height="980" viewBox="0 0 1080 980">{lines_html}</svg>'
    + "".join(f'<div class="dc d1 r1-{i}" style="left:{x}px;top:{y}px"><b>RÉPONSE {i + 1}</b><i class="x">{icon("cross", 26)}</i></div>' for i, (x, y) in enumerate(R1))
    + "".join(f'<div class="dc d2 r2-{i}" style="left:{x}px;top:{y}px"><b>R{[1, 4, 5, 8][i]}</b><i class="x">{icon("cross", 26)}</i></div>' for i, (x, y) in enumerate(R2))
    + "".join(f'<div class="dc d3 r3-{i}" style="left:{x}px;top:{y}px"><b>R{[1, 8][i]}</b><i class="x">{icon("cross", 26)}</i></div>' for i, (x, y) in enumerate(R3))
    + f'<div class="dc win" style="left:{WIN[0]}px;top:{WIN[1] - 20}px">{icon("crown", 34)}<b>LA MEILLEURE</b></div>'
    + '<div class="rd rd1" style="left:40px">ROUND 1</div><div class="rd rd2" style="left:360px">ROUND 2</div><div class="rd rd3" style="left:640px">FINALE</div>'))
R("#sc-duel .pill", gd["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
kin("#sc-duel .l1", wfind(20, "compar")); kin("#sc-duel .l2", wfind(22, "élimin"), 0.04)
R("#sc-duel .d1", gd["start"] + 0.3, {"opacity": 0, "x": -60}, {"opacity": 1, "x": 0}, 0.3, "power3.out")
js.append(f'tl.fromTo("#sc-duel .d1",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.3,ease:"power3.out",stagger:.06,immediateRender:false}},{q(gd["start"] + 0.3)});')
js.pop(-2)
pop("#sc-duel .rd1", wfind(20, "compar") - 0.1)
draw("#sc-duel .dl1", wfind(20, "compar"), 0.35, all_=True)
R("#sc-duel .d1", wfind(21, "critiqu"), {"rotation": 0}, {"rotation": 2.5}, 0.12, "power2.inOut")
R("#sc-duel .d1", wfind(21, "critiqu") + 0.12, {"rotation": 2.5}, {"rotation": 0}, 0.2, "back.out(3)")
te = wfind(22, "élimin")
for i in LOSE1:
    R(f"#sc-duel .r1-{i}", te, {"opacity": 1, "filter": "grayscale(0)"}, {"opacity": 0.32, "filter": "grayscale(1)"}, 0.25, "power2.out")
    pop(f"#sc-duel .r1-{i} .x", te)
pop("#sc-duel .rd2", te + 0.35)
draw("#sc-duel .dl2", te + 0.35, 0.3, all_=True)
for i in range(4):
    pop(f"#sc-duel .r2-{i}", te + 0.45 + i * 0.05)
for i in LOSE2:
    R(f"#sc-duel .r2-{i}", te + 0.95, {"opacity": 1, "filter": "grayscale(0)"}, {"opacity": 0.32, "filter": "grayscale(1)"}, 0.25, "power2.out")
    pop(f"#sc-duel .r2-{i} .x", te + 0.95)
pop("#sc-duel .rd3", te + 1.2)
draw("#sc-duel .dl3", te + 1.2, 0.3, all_=True)
for i in range(2):
    pop(f"#sc-duel .r3-{i}", te + 1.3 + i * 0.05)
for i in LOSE3:
    R(f"#sc-duel .r3-{i}", te + 1.75, {"opacity": 1, "filter": "grayscale(0)"}, {"opacity": 0.32, "filter": "grayscale(1)"}, 0.25, "power2.out")
    pop(f"#sc-duel .r3-{i} .x", te + 1.75)
pop("#sc-duel .win", te + 2.0)
overlays.append(sticker("st-facon", "FAÇON DE", "PARLER", "violet", None, "spark", left=30, top=1030))
fb(f'sticker(tl,"#st-facon",{q(wt(24, 0))},{q(wend(24) + 0.5)},-4)')

# ---- fast: first answer vs the Arena's, three stamps --------------------------
gq = G["fast"]
screens.append(screen("fast",
    pill("LE RÉSULTAT", "gold", "bolt")
    + head(chars("PAS LA PREMIÈRE", "w"), chars("LA MEILLEURE", "g"), 150, 84)
    + '<div class="cmp">'
      '<div class="cc c-first"><small>1RE RÉPONSE TROUVÉE</small><i></i><i style="width:70%"></i><i style="width:48%"></i>'
      '<svg class="strk2" width="420" height="300" viewBox="0 0 420 300"><path d="M20 30 L400 270 M400 30 L20 270" stroke="#ff6b6b" stroke-width="10" stroke-linecap="round" fill="none"/></svg></div>'
      '<div class="cc c-arena"><small>RÉPONSE ARENA</small><i></i><i style="width:82%"></i><i style="width:64%"></i><i style="width:90%"></i></div>'
      '</div>'))
R("#sc-fast .pill", gq["start"] + 0.08, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.3, "back.out(2.2)")
kin("#sc-fast .l1", wfind(27, "première"), 0.022); kin("#sc-fast .l2", wt(28, 0), 0.03)
up("#sc-fast .c-first", wfind(27, "première") - 0.1, 0.3)
draw("#sc-fast .strk2 path", wt(28, 0), 0.3)
up("#sc-fast .c-arena", wt(28, 0) + 0.1, 0.3)
for i, (word, (a, b, v, ic)) in enumerate(zip(["challeng", "compar", "amélior"],
        [("CHALLENGÉE", "", "violet", "checkc"), ("COMPARÉE", "", "gold", "checkc"), ("AMÉLIORÉE", "", "violet", "checkc")])):
    overlays.append(sticker(f"st-q{i}", a, b, v, ic, "spark", left=[60, 330, 140][i], top=[640, 760, 880][i]))
    fb(f'sticker(tl,"#st-q{i}",{q(wfind(29, word))},{q(gq["end"] - 0.35)},{[-6, 3, -3][i]})')

# ---- lance: welcome to 2026, 10 min of rewording -> launch the Arena ------------
gl = G["lance"]
screens.append(screen("lance",
    pill("LE MEILLEUR", "gold", "bolt")
    + head(chars("FINI DE", "w"), chars("REFORMULER", "r"), 150, 88)
    + f'<div class="row" style="top:420px"><div class="timer">{icon("clock", 64)}<b>10:00</b><small>à reformuler ton prompt</small>'
      '<svg class="strk3" width="560" height="60" viewBox="0 0 560 60"><path d="M10 40 C 180 10, 380 50, 550 18" stroke="#ff6b6b" stroke-width="9" stroke-linecap="round" fill="none"/></svg></div></div>'
    + f'<div class="row" style="top:660px"><div class="fb-btn go">{icon("rocket", 40)}<span>LANCER L\'ARENA</span></div></div>'
    + '<div class="row" style="top:660px"><div class="run"><b>ARENA EN COURS</b><div class="rb"><i></i></div></div></div>'))
overlays.append(sticker("st-2026", "BIENVENUE EN", "2026", "gold", "rocket", "spark", left=40, top=1030))
fb(f'sticker(tl,"#st-2026",{q(wt(31, 0))},{q(wend(31) + 0.9)},-4)')
R("#sc-lance .pill", wt(32, 0) - 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
kin("#sc-lance .l1", wt(33, 0)); kin("#sc-lance .l2", wfind(34, "reformul"), 0.04)
up("#sc-lance .timer", wfind(34, "dix") - 0.15)
draw("#sc-lance .strk3 path", wfind(34, "reformul") + 0.2, 0.3)
pop("#sc-lance .go", wt(35, 0))
fb(f'press(tl,"#sc-lance .go",{q(wfind(35, "Arena"))})')
R("#sc-lance .go", wfind(35, "Arena") + 0.3, {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 1.3}, 0.16, "power2.in")
R("#sc-lance .run", wfind(35, "Arena") + 0.34, {"opacity": 0, "scaleX": .4}, {"opacity": 1, "scaleX": 1}, 0.3, "back.out(1.6)")
R("#sc-lance .rb i", wfind(35, "Arena") + 0.5, {"scaleX": 0}, {"scaleX": 1}, max(1.0, gl["end"] - wfind(35, "Arena") - 0.8), "power1.inOut")

# ---- install: light card, refs 4/5 --------------------------------------------
gi = G["install"]
STEPS = [("doc", "Le lien", "copié"), ("brain", "Claude", "tu le colles"), ("send", "Le prompt", "d'installation"), ("checkc", "Arena", "installée")]
screens.append(screen("install",
    '<div class="row" style="top:40px"><div class="lcard">'
    '<div class="lbar"><span>AUTOMATISATION<b>BOOST</b></span><i class="d1"></i><i class="d2"></i><i class="d3"></i></div>'
    '<div class="lt">Pour l\'installer,</div><div class="lh"><span>2 copier-coller.</span></div>'
    '<div class="steps">' + "".join(
        f'<div class="st st{i}"><div class="stile">{icon(ic, 54)}</div><b>{a}</b><small>{b}</small></div>'
        + (f'<i class="ar ar{i}"></i>' if i < 3 else "") for i, (ic, a, b) in enumerate(STEPS)) + '</div></div></div>'))
up("#sc-install .lcard", gi["start"] + 0.1, 0.4, 60)
R("#sc-install .lh span", wfind(39, "colles"), {"backgroundSize": "0% 100%"}, {"backgroundSize": "100% 100%"}, 0.4, "power2.out")
for i, t in enumerate([wfind(39, "lien"), wfind(39, "Claude"), wfind(40, "prompt"), wend(40) - 0.2]):
    pop(f"#sc-install .st{i}", t)
    if i:
        R(f"#sc-install .ar{i - 1}", t - 0.15, {"scaleX": 0}, {"scaleX": 1}, 0.2, "power2.out")

# ---- cta: comment ARENA + follow -----------------------------------------------
gc = G["cta"]
screens.append(screen("cta",
    f'<div class="row" style="top:50px"><div class="brand">{icon("rocket", 34)}<span>AUTOMATISATION<b>BOOST</b></span></div></div>'
    + head(chars("COMMENTE", "w"), elastic("ARENA", "tokc"), 160, 100, 180)
    + '<div class="row" style="top:600px"><div class="igc">'
      '<div class="pr"><div class="av">AB</div><div><b>automatisationboost</b><small>Claude Code · n8n · IA</small></div>'
      '<div class="follow"><span class="f1">Suivre</span><span class="f2">Abonné ✓</span></div></div>'
      '<div class="cf"><span class="ph">Ajouter un commentaire…</span><span class="tc">' + chars("ARENA") + '</span>'
      f'<i class="snd">{icon("send", 36)}</i></div>'
      '<div class="sub">→ le lien + le prompt prêt à copier-coller</div></div></div>'))
R("#sc-cta .brand", gc["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
kin("#sc-cta .l1", wfind(44, "commente"), 0.03)
R("#sc-cta .l2", wfind(44, "ARENA") - 0.05, {"opacity": 0, "scale": 2.4}, {"opacity": 1, "scale": 1}, 0.34, "power4.in")
fb(f'elastic(tl,"#sc-cta .l2",{q(wfind(44, "ARENA") + 0.4)},{q(min(3.2, gc["end"] - wfind(44, "ARENA") - 1))})')
up("#sc-cta .igc", wt(43, 0), 0.4, 50)
R("#sc-cta .ph", wfind(44, "ARENA") - 0.1, {"opacity": 1}, {"opacity": 0}, 0.1, "power2.out")
fb(f'type(tl,"#sc-cta .tc",{q(wfind(44, "ARENA"))},0.08)')
pop("#sc-cta .snd", wfind(44, "ARENA") + 0.5)
up("#sc-cta .sub", wt(43, 2))
fb(f'press(tl,"#sc-cta .follow",{q(wfind(46, "follow"))})')
R("#sc-cta .f1", wfind(46, "follow") + 0.15, {"opacity": 1}, {"opacity": 0}, 0.12, "power2.out")
R("#sc-cta .f2", wfind(46, "follow") + 0.15, {"opacity": 0}, {"opacity": 1}, 0.15, "power2.out")
R("#sc-cta .follow", wfind(46, "follow") + 0.15, {"backgroundColor": "#eab308"}, {"backgroundColor": "#8b5cf6"}, 0.2, "power2.out")

# ---- fin (full-bleed) ----------------------------------------------------------
gn = G["fin"]
overlays.append(
    f'<section id="ov-fin" class="finale clip" data-start="{q(gn["start"] - 0.2)}" data-duration="{q(TOTAL - gn["start"] + 0.2)}" data-track-index="5">'
    '<div id="fin-shade"></div><div class="row" style="top:1290px"><div class="hd">'
    f'<div class="l1" style="font-size:104px">{chars("À LA PROCHAINE", "w")}</div>'
    f'<div class="l2" style="font-size:170px">{chars("ARENA", "g")}</div></div></div>'
    '<div class="row" style="top:1570px"><i class="sw"></i></div></section>')
R("#capbar", gn["start"] - 0.1, {"opacity": 1}, {"opacity": 0}, 0.2, "power2.in")
R("#fin-shade", gn["start"] - 0.2, {"opacity": 0}, {"opacity": 1}, 0.4, "power2.out")
# the take loops straight back to the hook, so the line lands fast: 1.4 s of screen
kin("#ov-fin .l1", gn["start"] - 0.05, 0.012, 0.3)
kin("#ov-fin .l2", gn["start"] + 0.2, 0.03, 0.32)
R("#ov-fin .sw", gn["start"] + 0.45, {"scaleX": 0}, {"scaleX": 1}, 0.35, "power3.out")

# ---- stickers on two IA jokes ----------------------------------------------------
for sid, tag, a, b, v in (("st-ia4", 4, "TROP", "LENT", "red"), ("st-ia9", 9, "SANS", "GÉRARD", "violet")):
    it = IA[tag]
    overlays.append(sticker(sid, a, b, v, None, "spark", left=60, top=1420))
    fb(f'sticker(tl,"#{sid}",{q(it["start"] + it["dur"] * 0.55)},{q(it["start"] + it["dur"] - 0.22)},-6)')

# ------------------------------------------------------------------ write
for f in ("kit.css", "kit.js"):
    os.makedirs(os.path.join(HERE, "public", "kit"), exist_ok=True)
    shutil.copy(os.path.join(KIT, f), os.path.join(HERE, "public", "kit", f))
TEMPLATE = open(os.path.join(HERE, "template.html")).read()
out = (TEMPLATE.replace("%%TOTAL%%", str(q(TOTAL)))
       .replace("%%SCREENS%%", "\n".join(screens))
       .replace("%%HOOK%%", "\n".join(overlays) + '\n<div id="flash"></div>')
       .replace("%%BUBBLES%%", "\n".join(bubbles))
       .replace("%%CAPTIONS%%", "\n".join(cap_html))
       .replace("%%JS%%", "\n".join(js + cap_js)))
open(os.path.join(HERE, "public", "index.html"), "w").write(out)
print(f"index.html: {len(groups)} blocs, {len(ia_items)} répliques IA, {ci} blocs de captions, {len(js)} animations, {q(TOTAL)} s")
print("  " + " | ".join(f"{g['tag']} {g['start']:.1f}-{g['end']:.1f}" for g in groups))

# ------------------------------------------------------------------ SFX events (for facecam_audio.py)
EV = []
for g in groups[1:]:
    EV.append([round(g["start"] - 0.30, 3), "sfx-whoosh-v2.mp3", -17])
for n, it in enumerate(ia_items):
    EV.append([round(it["start"], 3), "sfx-glitch-hard.mp3" if n == 0 else "sfx-thwip.mp3", -15 if n == 0 else -18])
EV.append([round(wfind(0, "éclat") + 0.5, 3), "sfx-glass-break.mp3", -19])          # the word cracks
EV.append([round(wfind(4, "quinze"), 3), "sfx-pop.mp3", -18])
for li in (5, 6, 7):
    EV.append([round(wt(li, 0), 3), "sfx-notify.mp3", -21])                          # prompts land in the chat
EV.append([round(wt(10, 1), 3), "sfx-chime-v2.mp3", -16])                            # SKILL ARENA assembles
EV.append([round(wfind(14, "Arena") - 0.1, 3), "sfx-zoom.mp3", -18])
for k in range(7):
    EV.append([round(G["agents"]["start"] + 0.35 + k * 0.16, 3), "sfx-pop.mp3", -24 + k])  # the army multiplies
EV.append([round(te, 3), "sfx-impact.mp3", -15])
EV.append([round(te + 0.95, 3), "sfx-impact.mp3", -17])
EV.append([round(te + 1.75, 3), "sfx-impact.mp3", -17])
EV.append([round(te + 2.0, 3), "sfx-confirm.mp3", -16])                              # the winner
for i, word in enumerate(["challeng", "compar", "amélior"]):
    EV.append([round(wfind(29, word), 3), "sfx-impact.mp3", -18])
EV.append([round(wt(28, 0), 3), "sfx-glitch-soft.mp3", -19])                         # first answer struck
EV.append([round(wfind(35, "Arena"), 3), "sfx-click.mp3", -15])
EV.append([round(wfind(44, "ARENA") - 0.05, 3), "sfx-impact-deep.mp3", -16])
EV.append([round(wfind(44, "ARENA"), 3), "sfx-click-soft.mp3", -18])
EV.append([round(wfind(46, "follow"), 3), "sfx-notify.mp3", -16])
EV.append([round(gn["start"] - 0.25, 3), "sfx-arrival-stop.mp3", -17])
for sid, t in (("bref", wt(3, 0)), ("facon", wt(24, 0)), ("2026", wt(31, 0)), ("ia4", IA[4]["start"] + IA[4]["dur"] * 0.55),
               ("ia9", IA[9]["start"] + IA[9]["dur"] * 0.55)):
    EV.append([round(t, 3), "sfx-thwip.mp3", -19])
EV = sorted(e for e in EV if 0 <= e[0] < TOTAL - 0.1)
json.dump(EV, open(os.path.join(HERE, "events.json"), "w"))
print(f"events.json: {len(EV)} SFX")

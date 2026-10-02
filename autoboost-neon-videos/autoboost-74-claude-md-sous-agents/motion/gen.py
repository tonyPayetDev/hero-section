#!/usr/bin/env python3
"""Generates public/index.html - autoboost-74 motion v2, built on the FaceCam Boost kit.

v2 over v1 (gen_v1.py): punch stickers, NIVEAU chips, the progression curve
(Notion #3), the question card pile (Notion #5), a vertical split for the
bazooka/clou comparison (layout 2), button -> comment field (Notion #1), the
elastic TOKEN (Notion #7) and a full-screen facecam finale (layout 4).

All times come from ../plan_actual.json, the real timeline of the cut facecam.
"""
import json, os, re, html, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "_shared", "facecam-boost-kit"))
sys.path.insert(0, KIT)
import kit  # noqa: E402
from kit import icon, chars, sticker, level, chart_svg, elastic, facecam_mode  # noqa: E402

P = json.load(open(os.path.join(HERE, "..", "plan_actual.json")))
TOTAL = P["total"]
FPS = 30

def q(t):
    return round(round(t * FPS) / FPS, 4)

# ------------------------------------------------------------------ facecam modes
FACE = (540, 520)
FULL = facecam_mode((0, 0, 1080, 1920), FACE)
CIRCLE = facecam_mode((220, 1100, 640, 640), FACE, crop_h=940, radius=320)
BIG = facecam_mode((160, 980, 760, 760), FACE, crop_h=940, radius=380)
RECT = facecam_mode((24, 1000, 1032, 920), (540, 560), crop_h=920, radius=34)
SPLIT = facecam_mode((24, 420, 500, 1290), (540, 600), crop_h=1240, radius=30)
FINALE = facecam_mode((0, 0, 1080, 1920), (540, 600), crop_h=1300)

MORPHS = [  # (start, duration, from, to)
    (3.30, 0.52, FULL, CIRCLE),
    (8.45, 0.50, CIRCLE, RECT),
    (14.75, 0.50, RECT, CIRCLE),
    (24.32, 0.50, CIRCLE, SPLIT),
    (28.20, 0.50, SPLIT, RECT),
    (33.12, 0.54, RECT, BIG),
    (37.62, 0.46, BIG, FINALE),
]
RING_ON = [(3.68, 8.45), (15.0, 24.32), (33.40, 37.62)]
RECT_ON = [(8.75, 14.85), (28.5, 33.2)]
SPLIT_ON = (24.70, 28.20)

B = [0.0, 3.55, 8.70, 15.00, 20.00, 24.60, 28.45, 33.37, 37.62, TOTAL]

KEY = {"CLAUDE.md", "sous-agents.", "Opus.", "TOKEN", "tokens", "token", "Commente",
       "clou.", "Astra,", "fichier.", "léger,", "bazooka"}

# ------------------------------------------------------------------ captions
chunks = []
for p in P["plan"]:
    cur = []
    for w in p["words"]:
        txt = " ".join(x["w"] for x in cur)
        probe = " ".join(x["w"] for x in cur + [w])
        ends_clause = bool(cur) and re.search(r"[.,!?:]$", cur[-1]["w"])
        if cur and (len(probe) > 24 or (ends_clause and len(txt) >= 14)):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)

CAP_END = 37.75  # the finale carries the last line itself
cap_html, cap_js = [], []
for ci, ch in enumerate(chunks):
    if ch[0]["s"] >= CAP_END:
        continue
    spans = [f'<span id="c{ci}w{wi}" class="{"cw key" if w["w"] in KEY else "cw"}">{html.escape(w["w"])}</span>'
             for wi, w in enumerate(ch)]
    cap_html.append(f'<div class="cap" id="c{ci}">{" ".join(spans)}</div>')
    a = ch[0]["s"] - 0.04
    b = min(chunks[ci + 1][0]["s"] - 0.04 if ci + 1 < len(chunks) else TOTAL, CAP_END)
    cap_js.append(f'tl.fromTo("#c{ci}",{{opacity:0,y:14,scale:.96}},{{opacity:1,y:0,scale:1,duration:.14,ease:"power2.out",immediateRender:false}},{q(max(0, a))});')
    cap_js.append(f'tl.set("#c{ci}",{{opacity:0}},{q(b)});')
    for wi, w in enumerate(ch):
        base = "#a78bfa" if w["w"] in KEY else "#EDEDED"
        nxt = min(ch[wi + 1]["s"] if wi + 1 < len(ch) else b, b)
        cap_js.append(f'tl.set("#c{ci}w{wi}",{{color:"#eab308",textShadow:"0 0 18px rgba(234,179,8,.8)"}},{q(w["s"])});')
        cap_js.append(f'tl.set("#c{ci}w{wi}",{{color:"{base}",textShadow:"0 0 0px rgba(234,179,8,0)"}},{q(nxt)});')

# ------------------------------------------------------------------ JS helpers
js = []
def R(sel, t, frm, to, d=0.45, ease="power3.out"):
    dest = dict(to, duration=d, ease=ease, immediateRender=False)
    js.append(f'tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(dest)},{q(t)});')

def S(sel, t, props):
    js.append(f'tl.set({json.dumps(sel)},{json.dumps(props)},{q(t)});')

def up(sel, t, d=0.42, dist=40):
    R(sel, t, {"opacity": 0, "y": dist}, {"opacity": 1, "y": 0}, d)

def pop(sel, t, d=0.38):
    R(sel, t, {"opacity": 0, "scale": 0.55}, {"opacity": 1, "scale": 1}, d, "back.out(2)")

def stamp(sel, t):
    R(sel, t, {"opacity": 0, "scale": 2.2, "rotation": -18}, {"opacity": 1, "scale": 1, "rotation": -8}, 0.32, "power4.in")

def kin(sel, t, stagger=0.035, d=0.42):
    js.append(f'tl.fromTo({json.dumps(sel + " .char")},{{opacity:0,y:46,scale:.6}},'
              f'{{opacity:1,y:0,scale:1,duration:{d},ease:"back.out(1.8)",stagger:{stagger},immediateRender:false}},{q(t)});')

def draw(sel, t, d=0.5):
    js.append(f'(function(){{var el=document.querySelector({json.dumps(sel)});if(!el)return;var L=el.getTotalLength();'
              f'tl.fromTo(el,{{strokeDasharray:L,strokeDashoffset:L}},{{strokeDashoffset:0,duration:{d},ease:"power2.inOut",immediateRender:false}},{q(t)});}})();')

def grow(sel, t, frm, to, d):
    R(sel, t, {"scaleX": frm}, {"scaleX": to}, d, "power2.inOut")

def fb(call):
    js.append("FB." + call + ";")

# ---- facecam
S("#facecam", 0, {"x": FULL["x"], "y": FULL["y"], "scale": FULL["scale"], "transformOrigin": "0px 0px", "clipPath": FULL["clip"]})
for a, d, f, t in MORPHS:
    R("#facecam", a, {"x": f["x"], "y": f["y"], "scale": f["scale"], "clipPath": f["clip"]},
      {"x": t["x"], "y": t["y"], "scale": t["scale"], "clipPath": t["clip"]}, d, "power3.inOut")

# ---- ring (circle modes), stacked frame, split divider
for a, b in RING_ON:
    R("#ring", a, {"opacity": 0, "scale": 0.82}, {"opacity": 1, "scale": 1}, 0.45, "back.out(1.6)")
    R("#ring", b, {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 1.15}, 0.3, "power2.in")
S("#ring-pos", 0, {"y": 0, "scale": 1})
S("#ring-pos", 33.2, {"y": -60, "scale": 1.1875})
draw("#ring-main", 3.68, 0.7)
for a, b in RECT_ON:
    R(".rect-fx", a, {"opacity": 0}, {"opacity": 1}, 0.35, "power2.out")
    R(".rect-fx", b, {"opacity": 1}, {"opacity": 0}, 0.3, "power2.in")
R("#split-div", SPLIT_ON[0], {"opacity": 0, "scaleY": 0}, {"opacity": 1, "scaleY": 1}, 0.45, "power3.out")
R("#split-div", SPLIT_ON[1], {"opacity": 1, "scaleY": 1}, {"opacity": 0, "scaleY": 1}, 0.25, "power2.in")
R("#split-knob", SPLIT_ON[0] + 0.3, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.35, "back.out(2.4)")
R("#split-knob", SPLIT_ON[1], {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 0.3}, 0.2, "power2.in")
for bt in P["beats"]:
    if any(a + 0.4 <= bt <= b - 0.2 for a, b in RING_ON):
        js.append(f'tl.fromTo("#ring-core",{{scale:1.045,filter:"brightness(1.6)"}},'
                  f'{{scale:1,filter:"brightness(1)",duration:.32,ease:"power2.out",immediateRender:false}},{q(bt)});')

# ---- screens slide in / out, speed streak on each change
for k in range(1, 8):
    R(f"#s{k}", B[k] - 0.28, {"x": 1080, "opacity": 1}, {"x": 0, "opacity": 1}, 0.5, "power4.out")
    R(f"#s{k}", B[k + 1] - 0.28, {"x": 0}, {"x": -1080}, 0.45, "power3.in")
    R("#streak", B[k] - 0.34, {"x": 1300, "opacity": 1}, {"x": -1500, "opacity": 1}, 0.42, "power2.inOut")
R("#streak", B[8] - 0.34, {"x": 1300, "opacity": 1}, {"x": -1500, "opacity": 1}, 0.42, "power2.inOut")

# ---- S0 hook (full-bleed facecam)
fb('sticker(tl,"#st0",0.15,1.10,-4)')
kin("#h0-l1", 0.10, 0.03)
kin("#h0-l2", 0.55, 0.045, 0.5)
pop("#h0-astra", 1.25)
draw("#h0-strike", 1.70, 0.3)
up("#h0-chip", 2.80, 0.45, 60)
R("#h0-title", 3.25, {"opacity": 1, "y": 0}, {"opacity": 0, "y": -160}, 0.4, "power3.in")
R("#h0-chip", 3.25, {"opacity": 1, "x": 0}, {"opacity": 0, "x": -300}, 0.35, "power3.in")
R("#h0-astra", 3.25, {"opacity": 1, "x": 0}, {"opacity": 0, "x": 300}, 0.35, "power3.in")
R("#shade", 3.3, {"opacity": 1}, {"opacity": 0}, 0.4, "power2.out")

# ---- S1 problème: progression curve (Notion #3)
fb('level(tl,"#lv1",3.80,8.40)')
pop("#s1 .pill", 3.75)
kin("#s1 .l1", 3.90); kin("#s1 .l2", 5.75)
up("#s1 .card", 4.40)
fb('chart(tl,"#s1 .card",4.80,2.4)')
up("#s1 .t1", 6.10); up("#s1 .t2", 6.30); up("#s1 .t3", 6.50)
stamp("#s1 .stamp", 7.55)
fb('sticker(tl,"#st1",7.65,8.40,-6)')

# ---- S2 vraie question: card pile (Notion #5)
fb('level(tl,"#lv2",8.95,14.62)')
pop("#s2 .pill", 8.90)
kin("#s2 .l1", 9.05); kin("#s2 .l2", 9.45)
up("#s2 .pile", 9.30, 0.45, 60)
draw("#s2 .strike", 10.70, 0.35)
stamp("#s2 .stamp", 10.95)
fb('stackFly(tl,"#s2 .qa",12.80,"#s2 .qb",{y:46,r:4,s:.94})')
R("#s2 .qb .ql, #s2 .qb .qt", 13.05, {"opacity": 0}, {"opacity": 1}, 0.3, "power2.out")
pop("#s2 .qb .ok", 14.40)
fb('sticker(tl,"#st2",13.55,14.62,-4)')

# ---- S3 la solution: CLAUDE.md typed line by line
fb('level(tl,"#lv3",15.25,19.70)')
pop("#s3 .pill", 15.20)
kin("#s3 .l1", 15.30); kin("#s3 .l2", 15.95, 0.05)
up("#s3 .win", 16.30)
for i, t in enumerate([16.75, 17.55, 18.15, 18.80, 19.35]):
    R(f"#s3 .ln{i}", t, {"clipPath": "inset(0 100% 0 0)", "opacity": 1}, {"clipPath": "inset(0 0% 0 0)", "opacity": 1}, 0.42, "power2.out")
js.append('tl.fromTo("#s3 .caret",{opacity:1},{opacity:0,duration:.4,ease:"steps(1)",repeat:4,yoyo:true,immediateRender:false},' + str(q(16.4)) + ');')
fb('sticker(tl,"#st3",18.95,19.72,-4)')

# ---- S4 routage
fb('level(tl,"#lv4",20.25,24.30)')
pop("#s4 .pill", 20.20)
kin("#s4 .l1", 20.30); kin("#s4 .l2", 20.65)
up("#s4 .win", 20.45)
pop("#s4 .n0", 20.70)
draw("#s4 .p-top", 20.85, 0.4); pop("#s4 .n1", 21.00)
draw("#s4 .p-top2", 21.30, 0.3); pop("#s4 .n2", 21.55)
draw("#s4 .p-bot", 22.85, 0.4); pop("#s4 .n3", 23.05)
draw("#s4 .p-bot2", 23.55, 0.3); pop("#s4 .n4", 23.85)
R("#s4 .n4", 24.05, {"boxShadow": "0 0 0px rgba(139,92,246,0)"}, {"boxShadow": "0 0 60px rgba(139,92,246,.9)"}, 0.3, "power2.out")
fb('sticker(tl,"#st4",21.70,23.80,-4)')

# ---- S5 bazooka / clou: vertical split (layout 2)
fb('level(tl,"#lv5",24.85,28.15)')
pop("#s5 .pill", 24.80)
kin("#s5 .l1", 24.95); kin("#s5 .l2", 26.90)
R("#s5 .cl", 25.30, {"opacity": 0, "x": 120}, {"opacity": 1, "x": 0}, 0.45, "power3.out")
stamp("#s5 .cl .stamp", 26.15)
R("#s5 .cr", 27.00, {"opacity": 0, "x": 120}, {"opacity": 1, "x": 0}, 0.45, "power3.out")
pop("#s5 .cr .badge", 27.40)
fb('sticker(tl,"#st5",27.55,28.15,-4)')

# ---- S6 objectif
fb('level(tl,"#lv6",28.70,33.05)')
pop("#s6 .pill", 28.65)
kin("#s6 .l1", 28.80); kin("#s6 .l2", 29.70)
up("#s6 .card", 29.40)
grow("#s6 .m1", 29.95, 1, 0.28, 1.1)
grow("#s6 .m2", 31.20, 0.30, 1, 1.1)
for i, t in enumerate([31.90, 32.30, 32.70]):
    R(f"#s6 .ck{i}", t, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0}, 0.35, "power3.out")
fb('sticker(tl,"#st6",31.35,33.05,-4)')

# ---- S7 CTA: button -> comment field (Notion #1), elastic TOKEN (Notion #7)
pop("#s7 .brand", 33.55)
fb('sticker(tl,"#st7",33.75,35.25,-4)')
kin("#s7 .qa .l1", 33.60); kin("#s7 .qa .l2", 34.15, 0.04)
R("#s7 .qa", 35.20, {"opacity": 1, "y": 0}, {"opacity": 0, "y": -60}, 0.25, "power2.in")
kin("#s7 .qb .l1", 35.40, 0.03)
R("#s7 .qb .l2", 35.70, {"opacity": 0, "scale": 2.6}, {"opacity": 1, "scale": 1}, 0.34, "power4.in")
fb('elastic(tl,"#s7 .qb .l2",36.10,1.45)')
pop("#s7 .btn-wrap", 35.95, 0.3)
fb('press(tl,"#s7 .fb-btn",36.28)')
R("#s7 .btn-wrap", 36.55, {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 1.4}, 0.18, "power2.in")
R("#s7 .box", 36.58, {"opacity": 0, "scaleX": 0.35, "scaleY": 0.6}, {"opacity": 1, "scaleX": 1, "scaleY": 1}, 0.32, "back.out(1.6)")
fb('type(tl,"#s7 .box .tc",36.80,0.07)')
pop("#s7 .box .snd", 37.20)
up("#s7 .sub", 37.15)

# ---- S8 finale: full-screen facecam + punchline (layout 4)
R("#capbar", 37.70, {"opacity": 1}, {"opacity": 0}, 0.25, "power2.in")
R("#fin-shade", 37.62, {"opacity": 0}, {"opacity": 1}, 0.4, "power2.out")
kin("#fin .l1", 37.90, 0.035)
kin("#fin .l2", 38.30, 0.04, 0.45)
R("#fin .sw", 38.55, {"scaleX": 0, "opacity": 1}, {"scaleX": 1, "opacity": 1}, 0.4, "power3.out")

# ---- ambient
R("#glow-a", 0, {"x": 0, "y": 0}, {"x": 160, "y": 220}, TOTAL, "sine.inOut")
R("#glow-b", 0, {"x": 0, "y": 0}, {"x": -140, "y": -180}, TOTAL, "sine.inOut")
R("#arc-a", 0, {"rotation": 0}, {"rotation": 540}, TOTAL, "none")
R("#arc-b", 0, {"rotation": 0}, {"rotation": -720}, TOTAL, "none")
R("#arc-c", 0, {"rotation": 30}, {"rotation": 390}, TOTAL, "none")
draw("#bg-curve", 0.2, 2.4)

# ------------------------------------------------------------------ markup
def screen(k, inner, top=0):
    a = q(max(0, B[k] - 0.30))
    b = q(min(TOTAL, B[k + 1] + 0.30))
    return (f'<section id="s{k}" class="screen clip" data-start="{a}" data-duration="{q(b - a)}" '
            f'data-track-index="{2 if k % 2 else 3}"><div class="inner">{inner}</div></section>')

def pill(text, kind="gold", ico=None):
    return f'<div class="row" style="top:56px"><div class="pill {kind}">{icon(ico, 30) if ico else ""}<span>{text}</span></div></div>'

def head(l1, l2, top=150, size=88, size2=None):
    size2 = size2 or size
    return (f'<div class="row" style="top:{top}px"><div class="hd">'
            f'<div class="l1" style="font-size:{size}px">{l1}</div>'
            f'<div class="l2" style="font-size:{size2}px">{l2}</div></div></div>')

# stickers live outside the screens so they can sit across the screen / facecam seam
STICKERS = "\n".join([
    sticker("st0", "ÇA", "PART", "violet", "rocket", "spark", left=40, top=1180),
    sticker("st1", "ÇA", "BLOQUE", "red", "warn", "spark", left=26, top=1030),
    sticker("st2", "PLUS", "CLAIR", "gold", "bulb", "spark", left=40, top=1050),
    sticker("st3", "BON", "SYSTÈME", "violet", "checkc", "swoosh", left=26, top=1030),
    sticker("st4", "PLUS", "SIMPLE", "gold", None, "spark", left=26, top=1030),
    sticker("st5", "DÉJÀ", "MIEUX", "violet", None, "spark", left=566, top=1420),
    sticker("st6", "ÇA", "MONTE", "gold", "trend", "swoosh", left=40, top=1050),
    sticker("st7", "NIVEAU", "MAX", "violet", "crown", "bar", left=26, top=990),
])
LEVELS = "\n".join(level(f"lv{n}", n, 6, left=36, top=36) for n in range(1, 7))

CHART = chart_svg([(0, .06), (.2, .14), (.4, .3), (.6, .5), (.8, .78), (1, 1)], w=880, h=200, label="100 %")

S1 = screen(1,
    pill("LE PROBLÈME", "red", "warn")
    + head(chars("LIMITE", "w") + chars(" ") + chars("EXPLOSÉE", "g"),
           chars("EN", "w") + chars(" ") + chars("½ JOURNÉE", "r"), 150, 92)
    + '<div class="row" style="top:400px"><div class="card c1">'
      '<div class="ch"><span>USAGE DES TOKENS</span><span class="mut">SESSION CLAUDE</span></div>'
      f'<div class="chartbox">{CHART}</div>'
      '<div class="axis"><span>9h</span><span>11h</span><span class="r">13h · ½ journée</span></div>'
      '<div class="stamp red">LIMITE ATTEINTE</div></div></div>'
    + '<div class="row tiles" style="top:790px">'
      f'<div class="tile t1"><div class="ic g">{icon("gauge")}</div><div><div class="tl">Usage</div><div class="tv">100 %</div></div></div>'
      f'<div class="tile t2"><div class="ic v">{icon("clock")}</div><div><div class="tl">Durée</div><div class="tv">½ journée</div></div></div>'
      f'<div class="tile t3"><div class="ic r">{icon("lock")}</div><div><div class="tl">Travail</div><div class="tv r">bloqué</div></div></div>'
      '</div>')

S2 = screen(2,
    pill("LA VRAIE QUESTION", "violet", "bolt")
    + head(chars("TU REGARDES", "w"), chars("LE MAUVAIS CHIFFRE", "g"), 150, 80, 80)
    + '<div class="row" style="top:430px"><div class="pile fb-stack">'
      '<div class="fb-scard qb" style="transform:translateY(46px) rotate(4deg) scale(.94)">'
      '<div class="ql g">LA BONNE QUESTION</div><div class="qt">Quel modèle travaille sur quelle tâche ?</div>'
      f'<div class="ok">{icon("check", 30)}</div></div>'
      '<div class="fb-scard qa">'
      '<div class="ql">CE QUE TU TE DEMANDES</div><div class="qt">Combien tu utilises Claude ?</div>'
      '<svg class="strk" width="860" height="40" viewBox="0 0 860 40"><path class="strike" d="M10 26 C 300 10, 560 34, 850 16" fill="none" stroke="#ff6b6b" stroke-width="7" stroke-linecap="round"/></svg>'
      '<div class="stamp red">MAUVAISE QUESTION</div></div>'
      '</div></div>')

S3 = screen(3,
    pill("LA SOLUTION", "gold", "bolt")
    + head(chars("UN SIMPLE", "w"), chars("CLAUDE.md", "g"), 150, 92, 112)
    + '<div class="row" style="top:440px"><div class="win">'
      '<div class="bar"><i class="d1"></i><i class="d2"></i><i class="d3"></i><span>CLAUDE.md</span><b>TON PROJET</b></div>'
      '<div class="code">'
      '<div class="ln ln0"><span class="v"># Règles de délégation</span></div>'
      '<div class="ln ln1">- tâche simple  → <span class="g">sous-agent</span></div>'
      '<div class="ln ln2">  modèle       : <span class="g">léger</span></div>'
      '<div class="ln ln3">- tâche complexe → <span class="v">Opus</span></div>'
      '<div class="ln ln4">- objectif     : <span class="g">moins de tokens</span><i class="caret"></i></div>'
      '</div></div></div>')

S4 = screen(4,
    pill("LE ROUTAGE", "violet", "bolt")
    + head(chars("CHAQUE TÂCHE", "w"), chars("SON MODÈLE", "g"), 150, 88)
    + '<div class="row" style="top:420px"><div class="win flow">'
      '<div class="bar"><i class="d1"></i><i class="d2"></i><i class="d3"></i><span>Claude Code — routage</span><b>SOUS-AGENTS</b></div>'
      '<svg class="wires" width="960" height="430" viewBox="0 0 960 430">'
      '<path class="p-top" d="M250 215 C 290 215, 290 110, 330 110" fill="none" stroke="#eab308" stroke-width="5"/>'
      '<path class="p-top2" d="M600 110 L 660 110" fill="none" stroke="#eab308" stroke-width="5"/>'
      '<path class="p-bot" d="M250 215 C 290 215, 290 320, 330 320" fill="none" stroke="#8b5cf6" stroke-width="5"/>'
      '<path class="p-bot2" d="M600 320 L 660 320" fill="none" stroke="#8b5cf6" stroke-width="5"/>'
      '</svg>'
      f'<div class="node n0" style="left:30px;top:150px">{icon("doc")}<div><b>CLAUDE.md</b><small>RÈGLES</small></div></div>'
      '<div class="node n1" style="left:330px;top:50px"><div><b>Tâche simple</b><small>RENOMMER, RÉSUMER</small></div></div>'
      f'<div class="node n2 gold" style="left:650px;top:50px">{icon("feather")}<div><b>Modèle léger</b><small>RAPIDE · ÉCONOME</small></div></div>'
      '<div class="node n3" style="left:330px;top:260px"><div><b>Tâche complexe</b><small>ARCHITECTURE</small></div></div>'
      f'<div class="node n4 violet" style="left:650px;top:260px">{icon("brain")}<div><b>Opus</b><small>PUISSANCE MAX</small></div></div>'
      '</div></div>')

S5 = screen(5,
    pill("L'ERREUR", "red", "warn")
    + head(chars("UN BAZOOKA", "w"), chars("POUR UN CLOU", "g"), 140, 84)
    + '<div class="col-r">'
      '<div class="vc cl"><div class="vk">OPUS</div><div class="vd">sur une tâche simple</div>'
      '<div class="bar-red"></div><div class="stamp red">GASPILLAGE</div></div>'
      '<div class="vc cr"><div class="vk g">LÉGER</div><div class="vd">sur une tâche simple</div>'
      '<div class="bar-gold"></div><div class="badge">JUSTE CE QU\'IL FAUT</div></div>'
      '</div>')

S6 = screen(6,
    pill("L'OBJECTIF", "gold", "bolt")
    + head(chars("MOINS DE", "w") + chars(" ") + chars("TOKENS", "g"), chars("GASPILLÉS", "v"), 150, 88)
    + '<div class="row" style="top:420px"><div class="card c6">'
      f'<div class="mrow"><div class="ml r">{icon("down", 34)}<span>Tokens gaspillés</span></div><div class="mt"><div class="m1"></div></div></div>'
      f'<div class="mrow"><div class="ml g">{icon("up", 34)}<span>Puissance pour l\'important</span></div><div class="mt"><div class="m2"></div></div></div>'
      '<div class="sep"></div>'
      f'<div class="ck ck0"><i>{icon("check", 30)}</i>Chaque tâche au bon modèle</div>'
      f'<div class="ck ck1"><i>{icon("check", 30)}</i>Opus gardé pour l\'important</div>'
      f'<div class="ck ck2"><i>{icon("check", 30)}</i>Moins de tokens gaspillés</div>'
      '</div></div>')

S7 = screen(7,
    f'<div class="row" style="top:50px"><div class="brand">{icon("rocket", 34)}<span>AUTOMATISATION<b>BOOST</b></span></div></div>'
    + '<div class="qa">' + head(chars("TU VEUX LE", "w"), chars("CLAUDE.md ?", "g"), 190, 92, 108) + '</div>'
    + '<div class="qb">' + head(chars("COMMENTE", "w"), elastic("TOKEN", "tokc"), 160, 104, 190) + '</div>'
    + f'<div class="row" style="top:630px"><div class="btn-wrap"><div class="fb-btn">{icon("send", 36)}<span>COMMENTER</span></div></div></div>'
    + '<div class="row" style="top:620px"><div class="box">'
      '<div class="av">T</div><div class="tc">' + chars("TOKEN") + '</div>'
      f'<div class="snd">{icon("send")}</div></div></div>'
    + '<div class="row" style="top:770px"><div class="sub">→ je t\'envoie le <b>prompt</b></div></div>')

S0 = (f'<section id="s0" class="hook clip" data-start="0" data-duration="{q(3.9)}" data-track-index="4">'
      '<div id="shade"></div>'
      '<div id="h0-title">'
      f'<div class="row" style="top:110px"><div class="hd"><div id="h0-l1" class="l1" style="font-size:98px">{chars("CLAUDE VIENT DE", "w")}</div>'
      f'<div id="h0-l2" class="l2" style="font-size:132px">{chars("TUER ASTRA ?", "g")}</div></div></div></div>'
      '<div id="h0-astra" class="chip" style="left:610px;top:1040px"><span class="xl">ASTRA</span>'
      '<svg width="220" height="40" viewBox="0 0 220 40" style="position:absolute;left:28px;top:30px"><path id="h0-strike" d="M6 24 L 214 14" stroke="#ff6b6b" stroke-width="7" stroke-linecap="round" fill="none"/></svg></div>'
      f'<div id="h0-chip" class="chip" style="left:40px;top:1400px"><span class="ic g">{icon("doc")}</span><span><small>TOUT ÇA GRÂCE À</small><b>UN SIMPLE <em>FICHIER</em></b></span></div>'
      '</section>')

FIN = (f'<section id="fin" class="finale clip" data-start="{q(B[8] - 0.1)}" data-duration="{q(TOTAL - B[8] + 0.1)}" data-track-index="5">'
       '<div id="fin-shade"></div>'
       '<div class="row" style="top:1300px"><div class="hd">'
       f'<div class="l1" style="font-size:104px">{chars("ÇA POURRAIT", "w")}</div>'
       f'<div class="l2" style="font-size:124px">{chars("TOUT CHANGER", "g")}</div></div></div>'
       '<div class="row" style="top:1590px"><i class="sw"></i></div>'
       '</section>')

# stage the kit next to the composition (HyperFrames only reads files under public/)
os.makedirs(os.path.join(HERE, "public", "kit"), exist_ok=True)
for f in ("kit.css", "kit.js"):
    shutil.copy(os.path.join(KIT, f), os.path.join(HERE, "public", "kit", f))

TEMPLATE = open(os.path.join(HERE, "template.html")).read()
out = (TEMPLATE
       .replace("%%TOTAL%%", str(q(TOTAL)))
       .replace("%%SCREENS%%", "\n".join([S1, S2, S3, S4, S5, S6, S7]))
       .replace("%%HOOK%%", S0 + "\n" + FIN + "\n" + LEVELS + "\n" + STICKERS)
       .replace("%%CAPTIONS%%", "\n".join(cap_html))
       .replace("%%JS%%", "\n".join(js + cap_js)))
open(os.path.join(HERE, "public", "index.html"), "w").write(out)
print(f"index.html v2: {len(cap_html)} blocs de captions, {len(js)} animations, duree {q(TOTAL)}s")

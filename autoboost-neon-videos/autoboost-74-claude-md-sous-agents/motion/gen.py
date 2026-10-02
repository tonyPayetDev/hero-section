#!/usr/bin/env python3
"""Generates public/index.html - the HyperFrames motion version of autoboost-74.

Layout follows Tony's references: a motion "screen" on top that slides in
screen after screen, the real facecam below - morphing between full-bleed
(hook), a neon circle (gold -> violet ring) and a stacked rectangle - and a
caption plate under it. Every time comes from ../plan_actual.json, the real
timeline of the cut facecam, so captions and reveals land on the spoken word.

The facecam <video> is a direct child of the root (HyperFrames contract), so it
is shaped with transform + clip-path: inset(... round R) - the one clip-path
form that interpolates between rectangle, rounded rectangle and circle.
"""
import json, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "..", "plan_actual.json")))
TOTAL = P["total"]
FPS = 30

# ------------------------------------------------------------------ facecam
# Source is 1080x1440. Each mode = transform (x, y, scale, origin 0 0) + clip.
FULL = dict(x=-180, y=0, scale=1.33334, clip="inset(0px 0px 0px 0px round 0px)")
# circle box in source px: x 70..1010, y 50..990 (940), centre (540, 520)
CIRCLE = dict(x=172.34, y=1065.96, scale=0.68085, clip="inset(50px 70px 450px 70px round 470px)")
BIG = dict(x=103.40, y=939.57, scale=0.80851, clip="inset(50px 70px 450px 70px round 470px)")
# stacked rectangle: source rows 100..1020 -> canvas 1000..1920
RECT = dict(x=0, y=900, scale=1.0, clip="inset(100px 24px 420px 24px round 34px)")

# (start, end, from, to) - the morphs that make the facecam travel
MORPHS = [
    (3.30, 3.82, FULL, CIRCLE),
    (8.45, 8.95, CIRCLE, RECT),
    (14.75, 15.25, RECT, CIRCLE),
    (28.20, 28.70, CIRCLE, RECT),
    (33.12, 33.66, RECT, BIG),
]
RING_ON = [(3.68, 8.45), (15.0, 28.2), (33.40, TOTAL)]  # circle-mode spans
RECT_ON = [(8.75, 14.85), (28.5, 33.2)]                  # stacked-mode spans

# screen boundaries: S0 hook, then 7 screens that slide in one after another
B = [0.0, 3.55, 8.70, 15.00, 20.00, 24.60, 28.45, 33.37, TOTAL]

KEY = {"CLAUDE.md", "sous-agents.", "Opus.", "TOKEN", "tokens", "token", "Commente",
       "clou.", "Astra,", "fichier.", "léger,", "bazooka"}

def q(t):
    return round(round(t * FPS) / FPS, 4)

# ------------------------------------------------------------------ icons
ICON = {
    "warn": '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M12 3 2 21h20L12 3z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><path d="M12 10v5M12 18v.5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z" fill="currentColor"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M6 2h8l5 5v15H6z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M14 2v5h5M9 12h7M9 16h7" stroke="currentColor" stroke-width="2"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" width="40" height="40"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" width="40" height="40"><rect x="5" y="11" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    "gauge": '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M4 18a8 8 0 1 1 16 0" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 18l4-6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "check": '<svg viewBox="0 0 24 24" width="30" height="30"><path d="m5 12 5 5 9-10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "rocket": '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M14 4c3-1 6-1 6-1s0 3-1 6l-6 6-5-5 6-6z" fill="currentColor"/><path d="M8 11l-4 1 2-4 4-1M13 16l-1 4 4-2 1-4" fill="currentColor"/><circle cx="15.5" cy="8.5" r="1.4" fill="#0a0a0f"/></svg>',
    "send": '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M3 11 21 3l-8 18-2-8-8-2z" fill="currentColor"/></svg>',
    "brain": '<svg viewBox="0 0 24 24" width="40" height="40"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="currentColor"/><path d="M12 4v3M12 17v3M4 12h3M17 12h3" stroke="currentColor" stroke-width="2"/></svg>',
    "feather": '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M20 4C10 4 6 10 5 19l3-3h5c4-2 6-7 7-12z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M5 19 14 10" stroke="currentColor" stroke-width="2"/></svg>',
    "down": '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 4v15M6 13l6 6 6-6" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "up": '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 20V5M6 11l6-6 6 6" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}

def chars(text, cls=""):
    out = []
    for ch in text:
        if ch == " ":
            out.append('<span class="char sp">&nbsp;</span>')
        else:
            out.append(f'<span class="char{(" " + cls) if cls else ""}">{html.escape(ch)}</span>')
    return "".join(out)

# ------------------------------------------------------------------ captions
def glue_needed(w):
    return not re.match(r"^['\-.,!?]", w)

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

cap_html, cap_js = [], []
for ci, ch in enumerate(chunks):
    spans = []
    for wi, w in enumerate(ch):
        cls = "cw key" if w["w"] in KEY else "cw"
        spans.append(f'<span id="c{ci}w{wi}" class="{cls}">{html.escape(w["w"])}</span>')
    cap_html.append(f'<div class="cap" id="c{ci}">{" ".join(spans)}</div>')
    a = ch[0]["s"] - 0.04
    b = chunks[ci + 1][0]["s"] - 0.04 if ci + 1 < len(chunks) else TOTAL
    cap_js.append(f'tl.fromTo("#c{ci}",{{opacity:0,y:14,scale:.96}},{{opacity:1,y:0,scale:1,duration:.14,ease:"power2.out",immediateRender:false}},{q(max(0,a))});')
    cap_js.append(f'tl.set("#c{ci}",{{opacity:0}},{q(b)});')
    for wi, w in enumerate(ch):
        base = "#a78bfa" if w["w"] in KEY else "#EDEDED"
        nxt = ch[wi + 1]["s"] if wi + 1 < len(ch) else b
        cap_js.append(f'tl.set("#c{ci}w{wi}",{{color:"#eab308",textShadow:"0 0 18px rgba(234,179,8,.8)"}},{q(w["s"])});')
        cap_js.append(f'tl.set("#c{ci}w{wi}",{{color:"{base}",textShadow:"0 0 0px rgba(234,179,8,0)"}},{q(nxt)});')

# ------------------------------------------------------------------ JS helpers
js = []
def R(sel, t, frm, to, d=0.45, ease="power3.out"):
    """fromTo that never renders before its own start (CSS holds the from state)."""
    # plain object literals: the HyperFrames linter reads them statically and
    # cannot see through Object.assign
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

def count(sel, t, a, b, d, suffix=""):
    js.append(f'(function(){{var o={{v:{a}}};tl.fromTo(o,{{v:{a}}},{{v:{b},duration:{d},ease:"power2.inOut",immediateRender:false,'
              f'onUpdate:function(){{var el=document.querySelector({json.dumps(sel)});if(el)el.textContent=Math.round(o.v)+{json.dumps(suffix)};}}}},{q(t)});}})();')

# ---- facecam morphs
S("#facecam", 0, {"x": FULL["x"], "y": FULL["y"], "scale": FULL["scale"],
                  "transformOrigin": "0px 0px", "clipPath": FULL["clip"]})
for a, b, f, t in MORPHS:
    R("#facecam", a, {"x": f["x"], "y": f["y"], "scale": f["scale"], "clipPath": f["clip"]},
      {"x": t["x"], "y": t["y"], "scale": t["scale"], "clipPath": t["clip"]}, b - a, "power3.inOut")

# ---- ring: draw in on the collapse, hide in stacked mode, grow for the CTA
for a, b in RING_ON:
    R("#ring", a, {"opacity": 0, "scale": 0.82}, {"opacity": 1, "scale": 1}, 0.45, "back.out(1.6)")
    if b < TOTAL:
        R("#ring", b, {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 1.15}, 0.3, "power2.in")
S("#ring-pos", 0, {"y": 0, "scale": 1})
S("#ring-pos", 33.2, {"y": -60, "scale": 1.1875})
draw("#ring-main", 3.68, 0.7)
for a, b in RECT_ON:
    R(".rect-fx", a, {"opacity": 0}, {"opacity": 1}, 0.35, "power2.out")
    R(".rect-fx", b, {"opacity": 1}, {"opacity": 0}, 0.3, "power2.in")
# ring breathes on every beat of the cut grid while the circle is up
for bt in P["beats"]:
    if any(a + 0.4 <= bt <= b - 0.2 for a, b in RING_ON):
        js.append(f'tl.fromTo("#ring-core",{{scale:1.045,filter:"brightness(1.6)"}},'
                  f'{{scale:1,filter:"brightness(1)",duration:.32,ease:"power2.out",immediateRender:false}},{q(bt)});')

# ---- screens: slide in from the right, out to the left ("écran par écran")
for k in range(1, 8):
    sel = f"#s{k}"
    R(sel, B[k] - 0.28, {"x": 1080, "opacity": 1}, {"x": 0, "opacity": 1}, 0.5, "power4.out")
    if k < 7:
        R(sel, B[k + 1] - 0.28, {"x": 0}, {"x": -1080}, 0.45, "power3.in")
# speed streak across the top zone on every screen change
for k in range(1, 8):
    R("#streak", B[k] - 0.34, {"x": 1300, "opacity": 1}, {"x": -1500, "opacity": 1}, 0.42, "power2.inOut")

# ---- S0 hook (full-bleed facecam)
kin("#h0-l1", 0.10, 0.03)
kin("#h0-l2", 0.55, 0.045, 0.5)
pop("#h0-astra", 1.25)
draw("#h0-strike", 1.70, 0.3)
up("#h0-chip", 2.80, 0.45, 60)
R("#h0-title", 3.25, {"opacity": 1, "y": 0}, {"opacity": 0, "y": -160}, 0.4, "power3.in")
R("#h0-chip", 3.25, {"opacity": 1, "x": 0}, {"opacity": 0, "x": -300}, 0.35, "power3.in")
R("#h0-astra", 3.25, {"opacity": 1, "x": 0}, {"opacity": 0, "x": 300}, 0.35, "power3.in")
R("#shade", 3.3, {"opacity": 1}, {"opacity": 0}, 0.4, "power2.out")

# ---- S1 problème (3.55 - 8.70)
pop("#s1 .pill", 3.75)
kin("#s1 .l1", 3.90); kin("#s1 .l2", 5.75)
up("#s1 .card", 4.40)
grow("#s1 .fill", 4.90, 0.02, 1, 2.6)
count("#s1 .pct", 4.90, 0, 100, 2.6, " %")
up("#s1 .t1", 6.10); up("#s1 .t2", 6.30); up("#s1 .t3", 6.50)
stamp("#s1 .stamp", 7.55)

# ---- S2 la vraie question (8.70 - 15.00)
pop("#s2 .pill", 8.90)
kin("#s2 .l1", 9.05); kin("#s2 .l2", 9.45)
up("#s2 .qa", 9.30)
draw("#s2 .strike", 10.70, 0.35)
stamp("#s2 .stamp", 10.95)
R("#s2 .qa", 12.85, {"opacity": 1}, {"opacity": 0.35}, 0.3, "power2.out")
up("#s2 .qb", 13.05, 0.45, 70)
pop("#s2 .qb .ok", 14.45)

# ---- S3 la solution (15.00 - 20.00)
pop("#s3 .pill", 15.20)
kin("#s3 .l1", 15.30); kin("#s3 .l2", 15.95, 0.05)
up("#s3 .win", 16.30)
for i, t in enumerate([16.75, 17.55, 18.15, 18.80, 19.35]):
    R(f"#s3 .ln{i}", t, {"clipPath": "inset(0 100% 0 0)", "opacity": 1}, {"clipPath": "inset(0 0% 0 0)", "opacity": 1}, 0.42, "power2.out")
js.append('tl.fromTo("#s3 .caret",{opacity:1},{opacity:0,duration:.4,ease:"steps(1)",repeat:4,yoyo:true,immediateRender:false},' + str(q(16.4)) + ');')

# ---- S4 routage (20.00 - 24.60)
pop("#s4 .pill", 20.20)
kin("#s4 .l1", 20.30); kin("#s4 .l2", 20.65)
up("#s4 .win", 20.45)
pop("#s4 .n0", 20.70)
draw("#s4 .p-top", 20.85, 0.4); pop("#s4 .n1", 21.00)
draw("#s4 .p-top2", 21.30, 0.3); pop("#s4 .n2", 21.55)
draw("#s4 .p-bot", 22.85, 0.4); pop("#s4 .n3", 23.05)
draw("#s4 .p-bot2", 23.55, 0.3); pop("#s4 .n4", 23.85)
R("#s4 .n4", 24.05, {"boxShadow": "0 0 0px rgba(139,92,246,0)"}, {"boxShadow": "0 0 60px rgba(139,92,246,.9)"}, 0.3, "power2.out")

# ---- S5 bazooka (24.60 - 28.45)
pop("#s5 .pill", 24.80)
kin("#s5 .l1", 24.95); kin("#s5 .l2", 26.90)
up("#s5 .cl", 25.35, 0.45, 60)
stamp("#s5 .cl .stamp", 26.15)
pop("#s5 .vs", 26.50)
up("#s5 .cr", 27.05, 0.45, 60)
pop("#s5 .cr .badge", 27.45)

# ---- S6 objectif (28.45 - 33.37)
pop("#s6 .pill", 28.65)
kin("#s6 .l1", 28.80); kin("#s6 .l2", 29.70)
up("#s6 .card", 29.40)
grow("#s6 .m1", 29.95, 1, 0.28, 1.1)
grow("#s6 .m2", 31.20, 0.30, 1, 1.1)
for i, t in enumerate([31.90, 32.30, 32.70]):
    R(f"#s6 .ck{i}", t, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0}, 0.35, "power3.out")

# ---- S7 CTA (33.37 - end)
pop("#s7 .brand", 33.55)
kin("#s7 .qa .l1", 33.60); kin("#s7 .qa .l2", 34.15, 0.04)
R("#s7 .qa", 35.20, {"opacity": 1, "y": 0}, {"opacity": 0, "y": -60}, 0.25, "power2.in")
kin("#s7 .qb .l1", 35.40, 0.03)
R("#s7 .qb .l2", 35.72, {"opacity": 0, "scale": 2.6}, {"opacity": 1, "scale": 1}, 0.36, "power4.in")
up("#s7 .box", 36.30, 0.4, 50)
js.append('tl.fromTo("#s7 .box .tc .char",{opacity:0},{opacity:1,duration:.05,stagger:.08,immediateRender:false},' + str(q(36.55)) + ');')
pop("#s7 .box .snd", 37.05)
up("#s7 .sub", 37.20)
R("#s7 .qb .l2", 38.30, {"textShadow": "0 0 30px rgba(234,179,8,.6)"}, {"textShadow": "0 0 90px rgba(234,179,8,1)"}, 0.5, "power2.out")

# ---- ambient: glow drift + orbit arcs (finite, no repeat:-1)
R("#glow-a", 0, {"x": 0, "y": 0}, {"x": 160, "y": 220}, TOTAL, "sine.inOut")
R("#glow-b", 0, {"x": 0, "y": 0}, {"x": -140, "y": -180}, TOTAL, "sine.inOut")
R("#arc-a", 0, {"rotation": 0}, {"rotation": 540}, TOTAL, "none")
R("#arc-b", 0, {"rotation": 0}, {"rotation": -720}, TOTAL, "none")
R("#arc-c", 0, {"rotation": 30}, {"rotation": 390}, TOTAL, "none")
draw("#bg-curve", 0.2, 2.4)

# ------------------------------------------------------------------ markup
def screen(k, inner):
    a = q(max(0, B[k] - 0.30))
    b = q(min(TOTAL, B[k + 1] + 0.30))
    track = 2 if k % 2 else 3
    return (f'<section id="s{k}" class="screen clip" data-start="{a}" data-duration="{q(b - a)}" '
            f'data-track-index="{track}">{inner}</section>')

def pill(text, kind="gold", icon=None):
    ic = ICON[icon] if icon else ""
    return f'<div class="row" style="top:56px"><div class="pill {kind}">{ic}<span>{text}</span></div></div>'

def head(l1, l2, top=150, size=88, size2=None):
    size2 = size2 or size
    return (f'<div class="row" style="top:{top}px"><div class="hd">'
            f'<div class="l1" style="font-size:{size}px">{l1}</div>'
            f'<div class="l2" style="font-size:{size2}px">{l2}</div></div></div>')

S1 = screen(1,
    pill("LE PROBLÈME", "red", "warn")
    + head(chars("LIMITE", "w") + chars(" ") + chars("EXPLOSÉE", "g"),
           chars("EN", "w") + chars(" ") + chars("½ JOURNÉE", "r"), 150, 92)
    + '<div class="row" style="top:410px"><div class="card c1">'
      '<div class="ch"><span>SESSION CLAUDE</span><span class="mut">USAGE DES TOKENS</span></div>'
      '<div class="meter"><div class="fill"></div></div>'
      '<div class="axis"><span>9h</span><span>11h</span><span class="r">13h · ½ journée</span></div>'
      '<div class="pct">0 %</div>'
      '<div class="stamp red">LIMITE ATTEINTE</div></div></div>'
    + '<div class="row tiles" style="top:770px">'
      f'<div class="tile t1"><div class="ic g">{ICON["gauge"]}</div><div><div class="tl">Usage</div><div class="tv">100 %</div></div></div>'
      f'<div class="tile t2"><div class="ic v">{ICON["clock"]}</div><div><div class="tl">Durée</div><div class="tv">½ journée</div></div></div>'
      f'<div class="tile t3"><div class="ic r">{ICON["lock"]}</div><div><div class="tl">Travail</div><div class="tv r">bloqué</div></div></div>'
      '</div>')

S2 = screen(2,
    pill("LA VRAIE QUESTION", "violet", "bolt")
    + head(chars("TU REGARDES", "w"), chars("LE MAUVAIS CHIFFRE", "g"), 150, 80, 80)
    + '<div class="row" style="top:410px"><div class="q qa">'
      '<div class="ql">CE QUE TU TE DEMANDES</div>'
      '<div class="qt">Combien tu utilises Claude ?</div>'
      '<svg class="strk" width="860" height="40" viewBox="0 0 860 40"><path class="strike" d="M10 26 C 300 10, 560 34, 850 16" fill="none" stroke="#ff6b6b" stroke-width="7" stroke-linecap="round"/></svg>'
      '<div class="stamp red">MAUVAISE QUESTION</div></div></div>'
    + '<div class="row" style="top:660px"><div class="q qb">'
      '<div class="ql g">LA BONNE QUESTION</div>'
      '<div class="qt">Quel modèle travaille sur quelle tâche ?</div>'
      f'<div class="ok">{ICON["check"]}</div></div></div>')

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
      f'<div class="node n0" style="left:30px;top:150px">{ICON["doc"]}<div><b>CLAUDE.md</b><small>RÈGLES</small></div></div>'
      f'<div class="node n1" style="left:330px;top:50px"><div><b>Tâche simple</b><small>RENOMMER, RÉSUMER</small></div></div>'
      f'<div class="node n2 gold" style="left:660px;top:50px">{ICON["feather"]}<div><b>Modèle léger</b><small>RAPIDE · ÉCONOME</small></div></div>'
      f'<div class="node n3" style="left:330px;top:260px"><div><b>Tâche complexe</b><small>ARCHITECTURE</small></div></div>'
      f'<div class="node n4 violet" style="left:660px;top:260px">{ICON["brain"]}<div><b>Opus</b><small>PUISSANCE MAX</small></div></div>'
      '</div></div>')

S5 = screen(5,
    pill("L'ERREUR", "red", "warn")
    + head(chars("UN BAZOOKA", "w"), chars("POUR UN CLOU", "g"), 150, 92)
    + '<div class="row duo" style="top:430px">'
      '<div class="vc cl"><div class="vk">OPUS</div><div class="vd">sur une tâche simple</div>'
      '<div class="bar-red"></div><div class="stamp red">GASPILLAGE</div></div>'
      '<div class="vs">VS</div>'
      '<div class="vc cr"><div class="vk g">LÉGER</div><div class="vd">sur une tâche simple</div>'
      '<div class="bar-gold"></div><div class="badge">JUSTE CE QU\'IL FAUT</div></div>'
      '</div>')

S6 = screen(6,
    pill("L'OBJECTIF", "gold", "bolt")
    + head(chars("MOINS DE", "w") + chars(" ") + chars("TOKENS", "g"),
           chars("GASPILLÉS", "v"), 150, 92)
    + '<div class="row" style="top:420px"><div class="card c6">'
      f'<div class="mrow"><div class="ml r">{ICON["down"]}<span>Tokens gaspillés</span></div><div class="mt"><div class="m1"></div></div></div>'
      f'<div class="mrow"><div class="ml g">{ICON["up"]}<span>Puissance pour l\'important</span></div><div class="mt"><div class="m2"></div></div></div>'
      '<div class="sep"></div>'
      f'<div class="ck ck0"><i>{ICON["check"]}</i>Chaque tâche au bon modèle</div>'
      f'<div class="ck ck1"><i>{ICON["check"]}</i>Opus gardé pour l\'important</div>'
      f'<div class="ck ck2"><i>{ICON["check"]}</i>Moins de tokens gaspillés</div>'
      '</div></div>')

S7 = screen(7,
    f'<div class="row" style="top:50px"><div class="brand">{ICON["rocket"]}<span>AUTOMATISATION<b>BOOST</b></span></div></div>'
    + '<div class="qa">' + head(chars("TU VEUX LE", "w"), chars("CLAUDE.md ?", "g"), 190, 92, 108) + '</div>'
    + '<div class="qb">' + head(chars("COMMENTE", "w"), '<span class="tok">TOKEN</span>', 170, 104, 190) + '</div>'
    + '<div class="row" style="top:620px"><div class="box">'
      '<div class="av">T</div><div class="tc">' + chars("TOKEN") + '</div>'
      f'<div class="snd">{ICON["send"]}</div></div></div>'
    + '<div class="row" style="top:770px"><div class="sub">→ je t\'envoie le <b>prompt</b></div></div>')

S0 = (f'<section id="s0" class="hook clip" data-start="0" data-duration="{q(3.9)}" data-track-index="4">'
      '<div id="shade"></div>'
      '<div id="h0-title">'
      f'<div class="row" style="top:110px"><div class="hd"><div id="h0-l1" class="l1" style="font-size:98px">{chars("CLAUDE VIENT DE", "w")}</div>'
      f'<div id="h0-l2" class="l2" style="font-size:132px">{chars("TUER ASTRA ?", "g")}</div></div></div></div>'
      '<div id="h0-astra" class="chip" style="left:610px;top:1040px"><span class="xl">ASTRA</span>'
      '<svg width="220" height="40" viewBox="0 0 220 40" style="position:absolute;left:28px;top:30px"><path id="h0-strike" d="M6 24 L 214 14" stroke="#ff6b6b" stroke-width="7" stroke-linecap="round" fill="none"/></svg></div>'
      f'<div id="h0-chip" class="chip" style="left:40px;top:1280px"><span class="ic g">{ICON["doc"]}</span><span><small>TOUT ÇA GRÂCE À</small><b>UN SIMPLE <em>FICHIER</em></b></span></div>'
      '</section>')

TEMPLATE = open(os.path.join(HERE, "template.html")).read()
out = (TEMPLATE
       .replace("%%TOTAL%%", str(q(TOTAL)))
       .replace("%%SCREENS%%", "\n".join([S1, S2, S3, S4, S5, S6, S7]))
       .replace("%%HOOK%%", S0)
       .replace("%%CAPTIONS%%", "\n".join(cap_html))
       .replace("%%JS%%", "\n".join(js + cap_js)))
open(os.path.join(HERE, "public", "index.html"), "w").write(out)
print(f"index.html: {len(chunks)} blocs de captions, {len(js)} animations, duree {q(TOTAL)}s")

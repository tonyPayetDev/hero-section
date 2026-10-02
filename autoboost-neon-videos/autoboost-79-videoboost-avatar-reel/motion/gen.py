#!/usr/bin/env python3
"""autoboost-79 - VideoBoost reel: a new voice on Tony's real take, background removed.

The take (video_25) is cut to the voice by avatar_track.py (mouth moves only on words),
matted with `hyperframes remove-background`, and placed bottom-centre over a studio
backdrop (neon tubes, bokeh). The top zone carries the motion that follows the words,
in the style of Tony's references: light card with a yellow-highlight headline and an
app chain, a node graph with electric connectors (gold / violet - never green), a
card behind his head, a mono caption pill, punch-ins on every cut of the take.

  BUILD=<dir with avatar.webm, avatar_cuts.json> python3 gen.py
"""
import json, os, html, shutil, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
KIT = os.path.abspath(os.path.join(PROJ, "..", "_shared", "facecam-boost-kit"))
sys.path.insert(0, KIT)
from kit import icon, chars as _chars, sticker, elastic  # noqa: E402


def chars(text, cls=""):
    """per-char spans, but a line can only break between words"""
    return '<span class="char sp">&nbsp;</span>'.join(f'<span style="white-space:nowrap">{_chars(w, cls)}</span>' for w in text.split(" "))

BUILD = os.environ.get("BUILD", os.path.join(PROJ, "build"))
FPS = 30
VDUR = 31.056                      # the voice
TOTAL = 32.5                       # + the CTA held after the last word
CUTS = json.load(open(os.path.join(BUILD, "avatar_cuts.json")))["cuts"]

# ------------------------------------------------------------------ words (Whisper + checked fixes)
raw = [w for s in json.load(open(os.path.join(PROJ, "session", "voice_transcript.json"))) for w in s["words"]]
FIX = {8: "une ?", 36: "VideoBoost,", 41: "l'IA", 42: "prépare", 101: "toi ?"}
DROP = {9, 43, 102}
W = []
for i, w in enumerate(raw):
    if i in DROP:
        if i == 43:
            W[-1]["e"] = w["e"]
        continue
    w = dict(w, w=FIX.get(i, w["w"]), i=i)
    if W and w["w"].startswith("'"):
        W[-1]["w"] += w["w"]; W[-1]["e"] = w["e"]
    else:
        W.append(w)
T = {i: w["s"] for i, w in enumerate(raw)}          # every raw index, merged fragments included


def t(i):
    return T[i]


def q(x):
    return round(round(x * FPS) / FPS, 4)


js = []


def R(sel, at, frm, to, d=0.3, ease="power3.out"):
    js.append(f'tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(dict(to, duration=d, ease=ease, immediateRender=False))},{q(at)});')


def S(sel, at, props):
    js.append(f'tl.set({json.dumps(sel)},{json.dumps(props)},{q(at)});')


def up(sel, at, d=0.3, dist=40):
    R(sel, at, {"opacity": 0, "y": dist}, {"opacity": 1, "y": 0}, d)


def pop(sel, at, d=0.3):
    R(sel, at, {"opacity": 0, "scale": 0.5}, {"opacity": 1, "scale": 1}, d, "back.out(2.2)")


def kin(sel, at, stagger=0.022, d=0.3):
    js.append(f'tl.fromTo({json.dumps(sel + " .char")},{{opacity:0,y:40}},{{opacity:1,y:0,duration:{d},ease:"back.out(1.8)",stagger:{stagger},immediateRender:false}},{q(at)});')


def hl(sel, at, d=0.35):
    R(sel, at, {"backgroundSize": "0% 100%"}, {"backgroundSize": "100% 100%"}, d, "power2.out")


def fb(call):
    js.append("FB." + call + ";")


def flash(at, op=0.6, d=0.25, color="#fff3b0"):
    S("#flash", at, {"backgroundColor": color})
    R("#flash", at, {"opacity": op}, {"opacity": 0}, d, "power2.out")


SC, FRONT, OV = [], [], []
BOUNDS = [0.0, 3.52, 9.5, 19.0, 24.33, 27.75, TOTAL]


def scene(i, inner, front=False):
    a, b = BOUNDS[i], BOUNDS[i + 1]
    s0, s1 = max(0, a - 0.3), min(TOTAL, b + 0.3)
    el = (f'<section id="s{i}" class="scene clip{" front" if front else ""}" data-start="{q(s0)}" data-duration="{q(s1 - s0)}" '
          f'data-track-index="{2 + i % 2}"><div class="in">{inner}</div></section>')
    (FRONT if front else SC).append(el)
    if i > 0:
        R(f"#s{i} .in", a - 0.12, {"opacity": 0, "x": 120}, {"opacity": 1, "x": 0}, 0.3, "power3.out")
    if i < 5:
        R(f"#s{i} .in", b - 0.2, {"opacity": 1, "x": 0}, {"opacity": 0, "x": -120}, 0.2, "power2.in")


def lbar():
    return '<div class="lbar"><span>AUTOMATISATION<b>BOOST</b></span><i class="d1"></i><i class="d2"></i><i class="d3"></i></div>'


# ------------------------------------------------------------------ the presenter: placed low, punch-in on every cut
TY, BASE = 640, 0.94
S("#tony", 0, {"x": 0, "y": TY, "scale": BASE})
R("#tony", 0, {"scale": BASE * 1.25, "y": TY + 100}, {"scale": BASE, "y": TY}, 0.32, "expo.out")      # hook visual: he slams in
flash(0.12, 0.35, 0.22)            # after frame 0: the first frame is the thumbnail
zoom = BASE
for k, c in enumerate(CUTS[1:], 1):
    zoom = BASE * 1.06 if zoom == BASE else BASE
    S("#tony", c, {"scale": zoom})
R("#tonyglow", 0, {"opacity": 0.7}, {"opacity": 1}, 2, "sine.inOut")
R("#tony", VDUR - 0.15, {"opacity": 1}, {"opacity": 0}, 0.2, "power2.in")                 # the take ends with the voice

# ------------------------------------------------------------------ A hook 0 - 3.52: tu crées encore chaque vidéo une par une ?
scene(0, '<div class="head" style="top:150px"><span class="l1 white">' + chars("Tu crées encore") + '</span></div>'
         '<div class="head" style="top:268px"><span class="hl l2">' + chars("une par une ?") + '</span></div>'
         + "".join(f'<div class="vt v{k}" style="left:{215 + k * 240}px">{icon("doc", 50)}<b>VIDÉO {k + 1}</b></div>' for k in range(3)))
kin("#s0 .l1", t(1), 0.02)
kin("#s0 .l2", t(6), 0.03)
hl("#s0 .hl", t(6) + 0.1)
S("#s0 .hl", 0, {"color": "#0a0a0f"})
for k, i in enumerate((6, 7, 8)):
    R(f"#s0 .v{k}", t(i), {"opacity": 0, "y": 60, "rotation": -6}, {"opacity": 1, "y": 0, "rotation": 0}, 0.25, "back.out(2)")
OV.append(sticker("st-att", "ATTENDS", ".", "red", "warn", "spark", left=60, top=1240))
fb(f'sticker(tl,"#st-att",{q(t(0))},{q(2.2)},-6)')

# ------------------------------------------------------------------ B problem 3.52 - 9.5: pas une bonne vidéo, en refaire encore x4
ENC = [25, 27, 29, 31]
scene(1, '<div class="lcard">' + lbar()
         + '<div class="t1"><span class="b1">' + chars("Pas UNE bonne vidéo.") + '</span><br><span class="hl b2">' + chars("En refaire. Encore.") + '</span></div>'
         + '<div class="chain">' + "".join(
             (f'<div class="arr r{k}"></div>' if k else "")
             + f'<div class="app a{k}"><div class="tile{" red" if k == 3 else ""}">{icon("doc", 50)}<i class="cnt">×{k + 1}</i></div><b>Encore</b><small>vidéo {k + 1}</small></div>'
             for k in range(4)) + '</div></div>')
up("#s1 .lcard", BOUNDS[1] - 0.05, 0.3, 50)
kin("#s1 .b1", t(10), 0.018)
kin("#s1 .b2", t(23), 0.02)
hl("#s1 .b2", t(24))
for k, i in enumerate(ENC):
    R(f"#s1 .a{k}", t(i), {"opacity": 0, "scale": 0.6}, {"opacity": 1, "scale": 1}, 0.22, "back.out(2.5)")
    if k:
        R(f"#s1 .r{k}", t(i) - 0.12, {"scaleX": 0}, {"scaleX": 1}, 0.15, "power2.out")
OV.append(sticker("st-lent", "TROP", "LENT", "red", "clock", "spark", left=600, top=1250))
fb(f'sticker(tl,"#st-lent",{q(t(31))},{q(BOUNDS[2] - 0.2)},-6)')

# ------------------------------------------------------------------ C VideoBoost 9.5 - 19.0: the machine, node by node on the words
NODES = [("IDÉE", "ton idée", "bulb", 40, 130, 40), ("SCRIPT", "l'IA le prépare", "brain", 385, 130, 45),
         ("VOIX", "arrive", "feather", 730, 130, 47), ("SOUS-TITRES", "se calent", "quote", 730, 380, 50),
         ("MOTION", "suit le rythme", "bolt", 385, 380, 55), ("VIDÉO", "elle sort", "rocket", 40, 380, 62)]
NW, NH = 250, 190


def zig(x0, y0, x1, y1, amp=9, waves=4):
    pts = []
    for k in range(41):
        u = k / 40
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        L = math.hypot(x1 - x0, y1 - y0) or 1
        off = amp * math.sin(u * waves * 2 * math.pi) * math.sin(u * math.pi)
        pts.append((x - (y1 - y0) / L * off, y + (x1 - x0) / L * off))
    return "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts)


def mid(n, side):
    x, y = NODES[n][3], NODES[n][4]
    return {"r": (x + NW, y + NH / 2), "l": (x, y + NH / 2), "b": (x + NW / 2, y + NH), "t": (x + NW / 2, y)}[side]


LINKS = [(0, "r", 1, "l"), (1, "r", 2, "l"), (2, "b", 3, "t"), (3, "l", 4, "r"), (4, "l", 5, "r")]
paths = ""
for k, (a, sa, b, sb) in enumerate(LINKS):
    (x0, y0), (x1, y1) = mid(a, sa), mid(b, sb)
    col = "#eab308" if k % 2 == 0 else "#a78bfa"
    paths += (f'<path class="lk{k}" d="{zig(x0, y0, x1, y1)}" stroke="{col}" style="filter:drop-shadow(0 0 8px {col}) drop-shadow(0 0 18px {col})"/>'
              f'<circle class="dt{k}a" cx="{x0}" cy="{y0}" r="10" fill="{col}" style="filter:drop-shadow(0 0 10px {col})"/>'
              f'<circle class="dt{k}b" cx="{x1}" cy="{y1}" r="10" fill="{col}" style="filter:drop-shadow(0 0 10px {col})"/>')
scene(2, '<div class="graph"><i class="gg"></i>'
         '<div class="gtitle">' + chars("J'ai construit") + ' <em>' + chars("VideoBoost") + '</em></div>'
         f'<svg class="wsvg" width="1020" height="600" viewBox="0 0 1020 600">{paths}</svg>'
         + "".join(f'<div class="node n{k}" style="left:{x}px;top:{y}px"><i class="ic">{icon(ic, 38)}</i><b>{a}</b><small>{b}</small>'
                   f'<i class="bz">{icon("bolt", 22)}</i></div>' for k, (a, b, ic, x, y, _) in enumerate(NODES))
         + '</div>')
up("#s2 .graph", BOUNDS[2] - 0.05, 0.3, 40)
kin("#s2 .gtitle", t(33), 0.02)
R("#s2 .gtitle em", t(36), {"textShadow": "0 0 0px rgba(234,179,8,0)"}, {"textShadow": "0 0 24px rgba(234,179,8,.9)"}, 0.3)
for k, (_, _, _, _, _, wi) in enumerate(NODES):
    at = t(wi)
    if k:
        R(f"#s2 .lk{k - 1}", at - 0.3, {"strokeDashoffset": 1400}, {"strokeDashoffset": 0}, 0.3, "power2.out")
        R(f"#s2 .dt{k - 1}a, #s2 .dt{k - 1}b", at - 0.3, {"opacity": 0}, {"opacity": 1}, 0.1)
    R(f"#s2 .n{k}", at, {"opacity": 0.35, "scale": 1, "borderColor": "#34304a"}, {"opacity": 1, "scale": 1.06, "borderColor": "#eab308"}, 0.18, "power3.out")
    R(f"#s2 .n{k}", at + 0.18, {"scale": 1.06}, {"scale": 1}, 0.25, "back.out(3)")
    R(f"#s2 .n{k} .ic", at, {"backgroundColor": "#262236", "color": "#8A8A8A"}, {"backgroundColor": "#eab308", "color": "#0a0a0f"}, 0.2)
    if k == 0:
        pop(f"#s2 .n{k} .bz", at + 0.1)
# the electric current flows along the links once they exist
js.append(f'tl.fromTo("#s2 .wsvg path",{{strokeDasharray:"16 12"}},{{strokeDashoffset:-400,duration:{q(BOUNDS[3] - t(45))},ease:"none",immediateRender:false}},{q(t(45))});')
for k in range(4):                                   # « le motion design suit le rythme »: the graph pulses
    R("#s2 .node", t(59) + k * 0.24, {"scale": 1.04}, {"scale": 1}, 0.18, "power2.out")
OV.append(sticker("st-auto", "AUTOMATISE", "ÇA", "gold", "bolt", "spark", left=520, top=1250))
fb(f'sticker(tl,"#st-auto",{q(t(63))},{q(BOUNDS[3] - 0.15)},-5)')

# ------------------------------------------------------------------ D 19.0 - 24.33: tu construis une machine - moi / la machine
scene(3, '<div class="lcard">' + lbar()
         + '<div class="t1" style="font-size:84px"><span class="d1">' + chars("Tu construis") + '</span><br><span class="hl d2">' + chars("une machine.") + '</span></div>'
         + '<div class="duo">'
           f'<div class="side m"><small>MOI</small><b><i>{icon("bulb", 44)}</i>la création</b></div>'
           f'<div class="side x"><small>LA MACHINE</small><b><i>{icon("gear", 44)}</i>le répétitif</b></div></div></div>')
up("#s3 .lcard", BOUNDS[3] - 0.05, 0.3, 50)
kin("#s3 .d1", t(64), 0.02)
kin("#s3 .d2", t(72), 0.03)
hl("#s3 .d2", t(73))
up("#s3 .side.m", t(74), 0.28, 30)
up("#s3 .side.x", t(79), 0.28, 30)
js.append(f'tl.fromTo("#s3 .side.x i",{{rotation:0}},{{rotation:360,duration:1.6,ease:"none",immediateRender:false}},{q(t(80))});')
OV.append(sticker("st-sys", "BON", "SYSTÈME", "gold", "checkc", "spark", left=560, top=1250))
fb(f'sticker(tl,"#st-sys",{q(t(83))},{q(BOUNDS[4] - 0.15)},-5)')

# ------------------------------------------------------------------ E 24.33 - 27.75: j'installe ce système pour d'autres entreprises (card behind the head)
COS = [("gear", "Entreprise 1"), ("rocket", "Entreprise 2"), ("trend", "Entreprise 3")]
scene(4, '<div style="position:absolute;left:0;top:96px;width:1080px;text-align:center"><span class="chip">NIVEAU<b>SUPÉRIEUR</b></span></div>'
         '<div class="head" style="top:190px;font-size:92px"><span class="white e1">' + chars("J'installe") + '</span> <span class="hl e2">' + chars("ce système.") + '</span></div>'
         '<div class="dash"><h4>Pour d\'autres entreprises</h4><p>La même machine, installée chez eux.</p><span class="live"><i></i>Système installé</span>'
         '<div class="cos">' + "".join(f'<div class="co c{k}">{icon(ic, 46)}<b>{lab}</b><i class="ok">{icon("check", 20)}</i></div>' for k, (ic, lab) in enumerate(COS)) + '</div></div>')
R("#s4 .chip", BOUNDS[4], {"opacity": 0, "scale": 0.7}, {"opacity": 1, "scale": 1}, 0.25, "back.out(2)")
kin("#s4 .e1", t(86), 0.025)
kin("#s4 .e2", t(88), 0.03)
hl("#s4 .e2", t(89))
S("#s4 .e2", 0, {"color": "#0a0a0f"})
up("#s4 .dash", t(90) - 0.1, 0.3, 50)
for k in range(3):
    R(f"#s4 .c{k}", t(93) + k * 0.12, {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, 0.25, "back.out(2)")
    pop(f"#s4 .c{k} .ok", t(93) + 0.6 + k * 0.25)

# ------------------------------------------------------------------ F CTA 27.75 - end: chez toi ? écris BOOST
scene(5, '<div class="ctaw"><div class="a q1">' + chars("Chez toi ?") + '</div></div>'
         '<div class="ctaw c2" style="top:150px"><div class="a">' + chars("ÉCRIS") + '</div><div class="b">' + elastic("BOOST", "") + '</div></div>'
         '<div class="cfield"><span class="pre">écris</span><span class="kw">' + chars("BOOST") + f'</span><i class="snd">{icon("send", 40)}</i></div>', front=True)
S("#s5 .c2 .b", 0, {"opacity": 0})
kin("#s5 .q1", t(94), 0.03, 0.28)
R("#s5 .q1", t(103) - 0.12, {"opacity": 1}, {"opacity": 0}, 0.12, "power2.in")
kin("#s5 .c2 .a", t(103), 0.03, 0.25)
R("#s5 .c2 .b", t(104) - 0.02, {"opacity": 0, "scale": 2.2}, {"opacity": 1, "scale": 1}, 0.25, "power4.in")
fb(f'elastic(tl,"#s5 .c2 .b",{q(t(104) + 0.35)},{q(TOTAL - t(104) - 0.6)})')
up("#s5 .cfield", t(94), 0.3, 30)
fb(f'type(tl,"#s5 .kw",{q(t(104))},0.07)')
pop("#s5 .snd", t(104) + 0.45)
flash(t(104) - 0.02, 0.5, 0.25)
R("#s5 .ctaw.c2", VDUR - 0.1, {"y": 0}, {"y": 380}, 0.45, "power3.inOut")      # Tony leaves, BOOST takes the centre
R("#s5 .cfield", VDUR - 0.1, {"y": 0}, {"y": 470}, 0.45, "power3.inOut")

# ------------------------------------------------------------------ captions: mono pill, active word gold
caps, cj, ci = [], [], 0
chunks, cur = [], []
for w in W:
    if cur and (w["s"] - cur[-1]["e"] > 0.35 or len(" ".join(x["w"] for x in cur + [w])) > 20 or len(cur) >= 3):
        chunks.append(cur); cur = []
    cur.append(w)
chunks.append(cur)
CW = {}
for k, ch in enumerate(chunks):
    a = ch[0]["s"] - 0.03
    b = min(chunks[k + 1][0]["s"] - 0.03, ch[-1]["e"] + 0.5) if k + 1 < len(chunks) else VDUR
    txt = " ".join(x["w"] for x in ch)
    width = int(len(txt) * 30.5 + 88)
    caps.append(f'<div class="cap" id="c{ci}" style="width:{width}px">' + " ".join(
        f'<span class="cw" id="c{ci}w{j}">{html.escape(x["w"])}</span>' for j, x in enumerate(ch)) + '</div>')
    cj.append(f'tl.set("#cap",{{width:{width},x:{540 - width / 2:.0f}}},{q(max(0, a))});')
    cj.append(f'tl.fromTo("#c{ci}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.1,ease:"power2.out",immediateRender:false}},{q(max(0, a))});')
    cj.append(f'tl.set("#c{ci}",{{opacity:0}},{q(b)});')
    for j, x in enumerate(ch):
        nxt = min(ch[j + 1]["s"] if j + 1 < len(ch) else b, b)
        cj.append(f'tl.set("#c{ci}w{j}",{{color:"#eab308",textShadow:"0 0 16px rgba(234,179,8,.8)"}},{q(x["s"])});')
        cj.append(f'tl.set("#c{ci}w{j}",{{color:"#EDEDED",textShadow:"0 0 0px rgba(234,179,8,0)"}},{q(nxt)});')
    ci += 1
S("#cap", 0, {"y": 1720})
R("#cap", VDUR - 0.1, {"opacity": 1}, {"opacity": 0}, 0.2)

# ------------------------------------------------------------------ write
TPL = open(os.path.join(HERE, "template.html")).read()
out = (TPL.replace("%%TOTAL%%", str(TOTAL)).replace("%%SCENES%%", "\n".join(SC)).replace("%%FRONT%%", "\n".join(FRONT))
       .replace("%%CAPTIONS%%", "\n".join(caps)).replace("%%OVERLAYS%%", "\n".join(OV)).replace("%%JS%%", "\n".join(js + cj)))
out = out.replace('data-duration="%s" data-track-index="6"' % TOTAL, 'data-duration="%s" data-track-index="6"' % VDUR)
pub = os.path.join(HERE, "public")
os.makedirs(os.path.join(pub, "kit"), exist_ok=True)
for f in ("kit.css", "kit.js"):
    shutil.copy(os.path.join(KIT, f), os.path.join(pub, "kit", f))
shutil.copy(os.path.join(BUILD, "avatar.webm"), os.path.join(pub, "avatar.webm"))
open(os.path.join(pub, "index.html"), "w").write(out)
print(f"index.html: {len(SC) + len(FRONT)} scènes, {ci} captions, {len(js)} animations, {TOTAL} s")

# ------------------------------------------------------------------ SFX
EV = [[0.0, "sfx-impact-deep.mp3", -17], [round(t(0), 3), "sfx-thwip.mp3", -21]]
EV += [[round(t(i), 3), "sfx-pop.mp3", -22] for i in (6, 7, 8)]
EV += [[round(b - 0.12, 3), "sfx-whoosh-lat.mp3", -22] for b in BOUNDS[1:6]]
EV += [[round(t(i), 3), "sfx-click.mp3", -21 + k] for k, i in enumerate(ENC)]
EV += [[round(t(31), 3), "sfx-impact.mp3", -19], [round(t(36), 3), "sfx-chime-v2.mp3", -19]]
EV += [[round(t(n[5]), 3), "sfx-click-soft.mp3", -21] for n in NODES]
EV += [[round(t(63), 3), "sfx-confirm.mp3", -18], [round(t(72), 3), "sfx-pop.mp3", -21], [round(t(83), 3), "sfx-thwip.mp3", -20]]
EV += [[round(t(93) + 0.6 + k * 0.25, 3), "sfx-confirm.mp3", -24] for k in range(3)]
EV += [[round(t(104) - 0.02, 3), "sfx-impact-deep.mp3", -15], [round(t(104), 3), "sfx-click-soft.mp3", -20]]
json.dump(sorted(EV), open(os.path.join(HERE, "events.json"), "w"))
print(f"events.json: {len(EV)} SFX")

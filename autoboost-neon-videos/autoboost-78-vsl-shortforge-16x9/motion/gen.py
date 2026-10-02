#!/usr/bin/env python3
"""autoboost-78 - VSL ShortForge v2, 16:9, in the « boost niveau » grammar.

Tony's notes on v1: no price, 16:9, closer to the boost-niveau reels (NIVEAU 1 -> MAX
chip, neon side tubes, avatar in a neon circle with caption pill, punch stickers),
a stylish track, a minimalist font, and the value and real examples on screen.

Layout 1920x1080: content panel left (x 110-1190), avatar circle + captions right.
Music: Deep Urban (house, 124 BPM measured, bar 1.9356 s). Scene cuts on downbeats,
the breakdown carries « ce que tu reçois » + the countdown, the re-drop is « Action ! ».
Every reveal is pinned to the cloned voice's word (build.py -> vo.json).

  BUILD=<build.py out dir> python3 gen.py
"""
import json, os, html, shutil, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
KIT = os.path.abspath(os.path.join(PROJ, "..", "_shared", "facecam-boost-kit"))
sys.path.insert(0, KIT)
from kit import icon, chars, sticker, elastic  # noqa: E402

BUILD = os.environ.get("BUILD", os.path.join(PROJ, "build"))
VO = json.load(open(os.path.join(BUILD, "vo.json")))
TOTAL, BEAT, BAR = VO["total"], VO["beat"], VO["bar"]
L = {it["li"]: it for it in VO["lines"]}
FPS = 30
D = [round(k * BAR, 3) for k in range(24)]          # downbeats
SC_T = [0, D[2], D[5], D[7], D[12], D[15], D[20], TOTAL]
BREAK = (D[15], D[20])                              # the track's breakdown


def q(t):
    return round(round(t * FPS) / FPS, 4)


def w(li, k=0):
    ws = L[li]["words"]
    return ws[min(k, len(ws) - 1)]["s"] if ws else L[li]["start"]


def wf(li, needle):
    for x in L[li]["words"]:
        if needle.lower() in x["w"].lower():
            return x["s"]
    raise KeyError((li, needle))


js = []


def R(sel, t, frm, to, d=0.3, ease="power3.out"):
    js.append(f'tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(dict(to, duration=d, ease=ease, immediateRender=False))},{q(t)});')


def S(sel, t, props):
    js.append(f'tl.set({json.dumps(sel)},{json.dumps(props)},{q(t)});')


def up(sel, t, d=0.32, dist=40):
    R(sel, t, {"opacity": 0, "y": dist}, {"opacity": 1, "y": 0}, d)


def pop(sel, t, d=0.3):
    R(sel, t, {"opacity": 0, "scale": 0.5}, {"opacity": 1, "scale": 1}, d, "back.out(2.2)")


def kin(sel, t, stagger=0.025, d=0.32):
    js.append(f'tl.fromTo({json.dumps(sel + " .char")},{{opacity:0,y:40}},{{opacity:1,y:0,duration:{d},ease:"back.out(1.8)",stagger:{stagger},immediateRender:false}},{q(t)});')


def fb(call):
    js.append("FB." + call + ";")


def flash(t, op=0.6, d=0.25, color="#fff3b0"):
    S("#flash", t, {"backgroundColor": color})
    R("#flash", t, {"opacity": op}, {"opacity": 0}, d, "power2.out")


SCENES, OV = [], []


def scene(i, inner):
    a, b = SC_T[i], SC_T[i + 1]
    s0, s1 = max(0, a - 0.35), min(TOTAL, b + 0.35)
    SCENES.append(f'<section id="s{i}" class="scene clip" data-start="{q(s0)}" data-duration="{q(s1 - s0)}" data-track-index="{2 + i % 2}">'
                  f'<div class="panel">{inner}</div></section>')
    # no empty frame at a cut: the next panel is already sliding in while this one leaves
    if i > 0:
        R(f"#s{i} .panel", a - 0.12, {"x": 140, "opacity": 0}, {"x": 0, "opacity": 1}, 0.32, "power3.out")
    if i < 6:
        R(f"#s{i} .panel", b - 0.2, {"x": 0, "opacity": 1}, {"x": -120, "opacity": 0}, 0.2, "power2.in")


def brackets():
    return '<i class="brk a"></i><i class="brk b"></i><i class="brk c"></i><i class="brk d"></i>'


# ------------------------------------------------------------------ avatar column (all along)
AV = (1525, 455, 460)          # centre x, centre y, diameter
ax, ay, ad = AV
S("#avatar", 0, {"x": ax - ad / 2, "y": ay - ad / 2, "scale": ad / 600, "transformOrigin": "0px 0px"})
S("#ring", 0, {"x": ax - 250, "y": ay - 250})
S("#ring2", 0, {"x": ax - 270, "y": ay - 270})
S("#cap", 0, {"x": ax - 350, "y": 760})
# hook visual: the avatar slams in on frame 1, ring snaps, flash
R("#avatar", 0, {"opacity": 0, "scale": ad / 600 * 1.5, "x": ax - ad * 0.75, "y": ay - ad * 0.75},
  {"opacity": 1, "scale": ad / 600, "x": ax - ad / 2, "y": ay - ad / 2}, 0.28, "expo.out")
R("#ring", 0.05, {"opacity": 0, "scale": 1.4}, {"opacity": 1, "scale": 1}, 0.3, "expo.out")
R("#ring2", 0.15, {"opacity": 0, "rotation": -60}, {"opacity": 1, "rotation": 0}, 0.4, "power3.out")
R("#ring2", 0.55, {"rotation": 0}, {"rotation": 360}, TOTAL - 0.6, "none")
S("#cap", 0, {"y": 760, "opacity": 0})
flash(0.0, 0.5, 0.25)
R("#glow-a", 0, {"x": 0, "y": 0}, {"x": 240, "y": 160}, TOTAL, "sine.inOut")
R("#glow-b", 0, {"x": 0, "y": 0}, {"x": -200, "y": -120}, TOTAL, "sine.inOut")
# beat: tubes breathe on every beat, the ring kicks on every downbeat - softer in the breakdown
for k in range(int(TOTAL / BEAT) + 1):
    t = k * BEAT
    if t > TOTAL - 0.3:
        break
    soft = BREAK[0] <= t < BREAK[1]
    R(".tube", t, {"opacity": 1}, {"opacity": 0.55 if not soft else 0.8}, 0.4, "power2.out")
for k, t in enumerate(D[:23]):
    if BREAK[0] <= t < BREAK[1]:
        continue
    R("#ring", t, {"scale": 1.045}, {"scale": 1}, 0.32, "power2.out")

# ------------------------------------------------------------------ level chip: NIVEAU 1 -> MAX
LV = [(1, "NIVEAU 1", SC_T[1]), (2, "NIVEAU 2", SC_T[2]), (3, "NIVEAU 3", SC_T[3]), (4, "NIVEAU 4", SC_T[4]), (5, "NIVEAU MAX", SC_T[5])]
levels = []
for n, lab, t in LV:
    segs = "".join(f'<i class="{"on" if i < n else ""}"></i>' for i in range(5))
    levels.append(f'<div class="lvl{" max" if n == 5 else ""}" id="lv{n}"><span>{lab}</span><span class="seg">{segs}</span></div>')
    R(f"#lv{n}", t - 0.05, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0}, 0.3, "back.out(2)")
    js.append(f'tl.fromTo("#lv{n} .seg i.on:last-child, #lv{n} .seg i.on:nth-child({n})",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"power2.out",transformOrigin:"0% 50%",immediateRender:false}},{q(t + 0.25)});')
    if n < 5:
        S(f"#lv{n}", LV[n][2] - 0.05, {"opacity": 0})

# ------------------------------------------------------------------ S0 hook 0 - D2: tu sais qu'il faut poster... tu ne le fais pas
DAYS = ["LUN", "MAR", "MER", "JEU", "VEN", "SAM", "DIM"]
OKD = {0, 3}
scene(0, '<div class="kick" style="position:absolute;left:0;top:40px">LE CONSTAT</div>'
      '<div class="h1" style="position:absolute;left:0;top:96px"><span class="l1">' + chars("TU SAIS QU'IL FAUT") + '</span><br>'
      '<span class="l2 g" style="font-size:150px;letter-spacing:-0.05em">' + chars("POSTER", "") + '</span><br>'
      '<span class="l3">' + chars("TOUS LES JOURS.") + '</span></div>'
      + '<div class="week">' + "".join(
          f'<div class="day {"ok" if i in OKD else "no"} d{i}"><b>{d}</b><i>{icon("check" if i in OKD else "cross", 34)}</i></div>'
          for i, d in enumerate(DAYS)) + '</div>'
      + '<div class="stampx" style="left:300px;top:690px;transform:rotate(-7deg)">TU NE LE FAIS PAS.</div>')
kin("#s0 .l1", w(0, 0), 0.018)
kin("#s0 .l2", wf(0, "poster") - 0.05, 0.03, 0.28)
kin("#s0 .l3", wf(0, "tous"), 0.02)
for i in range(7):
    R(f"#s0 .d{i}", 1.94 + i * BEAT / 2, {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0}, 0.2, "back.out(2)")
R("#s0 .stampx", wf(1, "pas") - 0.05, {"opacity": 0, "scale": 2.2, "rotation": -18}, {"opacity": 1, "scale": 1, "rotation": -7}, 0.2, "power4.in")
OV.append(sticker("st-part", "ÇA", "PART", "gold", "bolt", "spark", left=1290, top=150))
fb(f'sticker(tl,"#st-part",0.25,{q(1.8)},-5)')

# ------------------------------------------------------------------ S1 problem D2 - D5: six steps, two hours
STEPS = [("ÉCRIRE", "feather"), ("FILMER", "search"), ("MONTER", "gear"), ("SOUS-TITRER", "quote"), ("EXPORTER", "down"), ("PUBLIER", "send")]
KW = ["écrire", "filmer", "monter", "sous", "exporter", "publier"]
CLK = ["0 h 00", "0 h 20", "0 h 40", "1 h 00", "1 h 20", "1 h 40", "2 h 00"]
scene(1, brackets()
      + '<div class="kick" style="position:absolute;left:40px;top:40px">CE QUI TE BLOQUE</div>'
      + '<div class="h2" style="position:absolute;left:40px;top:96px">' + chars("UNE VIDÉO, À LA MAIN :") + '</div>'
      + '<div class="chips" style="left:40px">' + "".join(f'<div class="chip c{i}"><i>{icon(ic, 30)}</i><span>{s}</span></div>' for i, (s, ic) in enumerate(STEPS)) + '</div>'
      + '<div class="clock" style="left:40px"><div class="t">' + "".join(f'<span class="k{i}">{c}</span>' for i, c in enumerate(CLK)) + '</div><small>de travail par vidéo</small></div>')
kin("#s1 .h2", SC_T[1] + 0.05, 0.015)
S("#s1 .k0", SC_T[1], {"opacity": 1})
for i, kw in enumerate(KW):
    t = wf(2, kw)
    R(f"#s1 .c{i}", t, {"borderColor": "#2b2840", "color": "#6b6782", "scale": 1.08}, {"borderColor": "#eab308", "color": "#EDEDED", "scale": 1}, 0.25, "back.out(2)")
    R(f"#s1 .c{i} i", t, {"color": "#6b6782", "backgroundColor": "#1b1828"}, {"color": "#0a0a0f", "backgroundColor": "#eab308"}, 0.2)
    S(f"#s1 .k{i}", t, {"opacity": 0})
    S(f"#s1 .k{i + 1}", t, {"opacity": 1})
t2h = wf(2, "deux")
R("#s1 .clock .t", t2h, {"color": "#EDEDED", "scale": 1}, {"color": "#ff6b6b", "scale": 1.12}, 0.2, "back.out(3)")
OV.append(sticker("st-lent", "TROP", "LENT", "red", "clock", "spark", left=760, top=700))
fb(f'sticker(tl,"#st-lent",{q(t2h)},{q(SC_T[2] - 0.25)},-6)')

# ------------------------------------------------------------------ S2 reveal D5 - D7: ShortForge, from one paragraph, the six steps
scene(2, '<div class="kick" style="position:absolute;left:0;top:60px">LA SOLUTION</div>'
      + '<div class="logo">' + elastic("SHORTFORGE", "g") + '</div>'
      + '<div class="h2 v" style="position:absolute;left:4px;top:380px;font-size:40px;font-weight:400">skill Claude Code</div>'
      + '<div class="card para"><b class="kick" style="font-size:18px">TON PARAGRAPHE</b><i style="width:92%"></i><i style="width:78%"></i><i style="width:86%"></i><i style="width:54%"></i></div>'
      + '<i class="arrow"></i>'
      + '<div class="six">' + "".join(f'<span class="x{i}"><i>{icon("check", 22)}</i>{s}</span>' for i, (s, _) in enumerate(STEPS)) + '</div>')
flash(SC_T[2], 0.35, 0.3, "#8b5cf6")
R("#s2 .logo", w(3, 0), {"opacity": 0, "scaleX": 0.6}, {"opacity": 1, "scaleX": 1}, 0.3, "expo.out")
S("#s2 .logo", SC_T[2] - 0.2, {"opacity": 0})
fb(f'elastic(tl,"#s2 .logo",{q(w(3, 0) + 0.3)},1.3)')
up("#s2 .v", w(3, 1), 0.25, 20)
up("#s2 .para", wf(15, "paragraphe") - 0.3, 0.3, 40)
R("#s2 .arrow", wf(15, "paragraphe"), {"scaleX": 0}, {"scaleX": 1}, 0.25, "power2.out")
js.append(f'tl.fromTo("#s2 .six span",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.2,stagger:{BEAT / 4:.3f},ease:"back.out(2)",immediateRender:false}},{q(wf(15, "paragraphe") + 0.2)});')
OV.append(sticker("st-simple", "PLUS", "SIMPLE", "gold", "bolt", "spark", left=1300, top=150))
fb(f'sticker(tl,"#st-simple",{q(wf(15, "simple"))},{q(SC_T[3] - 0.2)},-5)')

# ------------------------------------------------------------------ S3 demo D7 - D12: brief -> voice/avatar/captions -> a real video
BRIEF = "présente mon offre en 30 s"
scene(3, '<div class="kick" style="position:absolute;left:0;top:10px">COMMENT ÇA MARCHE</div>'
      + '<div class="card step st1" style="top:80px"><span class="n">1</span><span class="tt">Tu colles un brief</span>'
        '<div class="field"><span class="typed">' + chars(BRIEF) + '</span></div></div>'
      + '<div class="card step st2" style="top:330px"><span class="n">2</span><span class="tt">L\'IA produit</span>'
        f'<div class="layers"><span class="y0">{icon("feather", 24)}ta voix</span><span class="y1">{icon("brain", 24)}ton avatar</span><span class="y2">{icon("quote", 24)}captions</span></div></div>'
      + '<div class="card step st3" style="top:580px"><span class="n">3</span><span class="tt">Prête à poster</span>'
        '<div class="kick" style="margin-top:16px;color:#8A8A8A">1080 × 1920 · TikTok · Reels · Shorts</div></div>'
      + '<i class="wire w1" style="left:530px;top:200px;width:110px"></i><i class="wire w2" style="left:530px;top:450px;width:110px"></i>'
      + '<i class="wire w3" style="left:530px;top:690px;width:110px"></i>'
      + '<div class="phone"></div><div class="plabel">↑ une vraie vidéo sortie du pipeline</div>')
up("#s3 .st1", w(4, 0), 0.3)
fb(f'type(tl,"#s3 .typed",{q(w(4, 0) + 0.2)},0.035)')
up("#s3 .st2", w(5, 0), 0.3)
for i, kw in enumerate(["voix", "avatar", "captions"]):
    t = wf(5, kw)
    R(f"#s3 .y{i}", t, {"borderColor": "#3a3350", "color": "#6b6782"}, {"borderColor": "#eab308", "color": "#EDEDED"}, 0.2)
up("#s3 .st3", w(6, 0), 0.3)
for i, t in enumerate([w(4, 0) + 0.4, w(5, 0) + 0.3, w(6, 0) + 0.2]):
    R(f"#s3 .w{i + 1}", t, {"scaleX": 0}, {"scaleX": 1}, 0.3, "power2.out")
# the phone: a real render plays inside (ex0 window 19.2 - 23.4)
PX, PY = 110 + 640, 140 + 120
R("#s3 .phone", w(6, 0) - 0.15, {"opacity": 0, "scale": 0.85}, {"opacity": 1, "scale": 1}, 0.3, "back.out(1.8)")
S("#ex0", 0, {"x": PX + 4, "y": PY + 4, "scale": 372 / 360, "transformOrigin": "0px 0px"})
R("#ex0", w(6, 0) - 0.15, {"opacity": 0}, {"opacity": 1}, 0.25)
S("#ex0", SC_T[4] - 0.12, {"opacity": 0})
up("#s3 .plabel", w(6, 0) + 0.5, 0.25, 20)
OV.append(sticker("st-temps", "GAIN", "TEMPS", "violet", "clock", "spark", left=1290, top=150))
fb(f'sticker(tl,"#st-temps",{q(wf(6, "prête"))},{q(SC_T[4] - 0.2)},-5)')

# ------------------------------------------------------------------ S4 examples D12 - D15: three real videos playing, render time
XS = [0, 375, 750]
scene(4, '<div class="kick" style="position:absolute;left:0;top:10px">LES EXEMPLES · VRAIES VIDÉOS</div>'
      + '<div class="h2" style="position:absolute;left:0;top:46px;font-size:46px">' + chars("6 FORMATS, DÉJÀ PUBLIÉS") + '</div>'
      + "".join(f'<div class="ph3{" v" if i == 1 else ""} p{i}" style="left:{x}px"></div>' for i, x in enumerate(XS))
      + '<div class="rend"><span class="old">2 h<svg width="140" height="40" viewBox="0 0 140 40"><path d="M4 30 L136 8"/></svg></span>'
        '<span class="to">→</span><span class="new g">quelques minutes</span></div>')
kin("#s4 .h2", w(7, 0), 0.015)
for i, x in enumerate(XS):
    t = SC_T[4] + 0.1 + i * BEAT / 2
    R(f"#s4 .p{i}", t, {"opacity": 0, "y": 60}, {"opacity": 1, "y": 0}, 0.3, "back.out(1.6)")
    vid = f"#ex{i + 1}"
    S(vid, 0, {"x": 110 + x + 4, "y": 140 + 130 + 4, "scale": 322 / 360, "transformOrigin": "0px 0px"})
    R(vid, t, {"opacity": 0}, {"opacity": 1}, 0.3)
    S(vid, SC_T[5] - 0.12, {"opacity": 0})
R("#s4 .old", wf(16, "rendu"), {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, 0.25)
R("#s4 .old path", wf(16, "deux") - 0.05, {"strokeDashoffset": 220}, {"strokeDashoffset": 0}, 0.2)
R("#s4 .to", wf(16, "quelques") - 0.1, {"opacity": 0, "x": -20}, {"opacity": 1, "x": 0}, 0.2)
R("#s4 .new", wf(16, "quelques"), {"opacity": 0, "scale": 1.4}, {"opacity": 1, "scale": 1}, 0.25, "expo.out")
OV.append(sticker("st-monte", "ÇA", "MONTE", "gold", "trend", "spark", left=1300, top=150))
fb(f'sticker(tl,"#st-monte",{q(w(7, 0))},{q(SC_T[5] - 0.2)},-5)')

# ------------------------------------------------------------------ S5 what you get (breakdown) D15 - D20, countdown on beats
GET = [("Le skill complet", "à vie, mises à jour incluses", "skill"), ("10 formats × 10 directions artistiques", "", "dix"),
       ("Un seul tournage", "30 s de voix · 45 s face caméra", "tournes")]
scene(5, '<div class="kick" style="position:absolute;left:0;top:40px">CE QUE TU REÇOIS</div>'
      + '<div class="h2" style="position:absolute;left:0;top:96px">' + chars("TOUT LE SYSTÈME.") + '</div>'
      + '<div class="list">' + "".join(f'<div class="li i{i}"><i>{icon("check", 30)}</i><span>{a}</span><small>{b}</small></div>' for i, (a, b, _) in enumerate(GET)) + '</div>')
kin("#s5 .h2", SC_T[5] + 0.05, 0.02)
for i, (_, _, kw) in enumerate(GET):
    R(f"#s5 .i{i}", wf(17, kw), {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0}, 0.3, "back.out(1.8)")
    R(f"#s5 .i{i} i", wf(17, kw) + 0.15, {"backgroundColor": "rgba(234,179,8,0)", "color": "#eab308"}, {"backgroundColor": "#eab308", "color": "#0a0a0f"}, 0.2)
OV.append(sticker("st-sys", "BON", "SYSTÈME", "gold", "checkc", "spark", left=1290, top=150))
fb(f'sticker(tl,"#st-sys",{q(L[17]["end"] + 0.1)},{q(SC_T[6] - 0.2)},-5)')
COUNT = '<div class="cd" id="cd">' + "".join(f'<span class="n{n}">{n}</span>' for n in (3, 2, 1)) + '</div>'
R("#dim", L[11]["start"] - 0.15, {"opacity": 0}, {"opacity": 1}, 0.15)
for n, li in ((3, 11), (2, 12), (1, 13)):
    t = L[li]["start"]
    R(f"#cd .n{n}", t, {"opacity": 0, "scale": 1.5}, {"opacity": 1, "scale": 1}, 0.15, "expo.out")
    if n > 1:
        S(f"#cd .n{n}", t + BEAT - 0.02, {"opacity": 0})
S("#cd .n1", SC_T[6], {"opacity": 0})
S("#dim", SC_T[6], {"opacity": 0})

# ------------------------------------------------------------------ S6 CTA D20 - end: re-drop, COMMENTE FORGE
tw = wf(10, "forge")
scene(6, '<svg class="burst" width="1300" height="1080" viewBox="0 0 1300 1080">' + "".join(
          f'<line x1="650" y1="540" x2="{650 + 900 * math.cos(a):.0f}" y2="{540 + 900 * math.sin(a):.0f}" stroke="{"#eab308" if k % 3 else "#8b5cf6"}" stroke-width="{2 + (k * 7) % 4}"/>'
          for k, a in enumerate([2 * math.pi * k / 48 for k in range(48)])) + '</svg>'
      + '<div class="cta1">' + chars("COMMENTE") + '</div>'
      + '<div class="cta2">' + elastic("FORGE", "g") + '</div>'
      + '<div class="cfield"><span class="pre">commente</span><span class="kw">' + chars("FORGE") + f'</span><i class="snd">{icon("send", 40)}</i></div>'
      + '<div class="dmline">→ je t\'envoie le lien en <b class="g">DM</b></div>')
t6 = SC_T[6]
flash(t6, 0.85, 0.25, "#ffffff")
R("#s6 .burst", t6, {"opacity": 1, "scale": 0.1}, {"opacity": 0, "scale": 1.5}, 0.7, "expo.out")
kin("#s6 .cta1", t6 + 0.02, 0.02, 0.22)
R("#s6 .cta2", t6 + 0.08, {"opacity": 0, "scale": 2}, {"opacity": 1, "scale": 1}, 0.25, "power4.in")
fb(f'elastic(tl,"#s6 .cta2",{q(t6 + 0.5)},{q(TOTAL - t6 - 1.0)})')
up("#s6 .cfield", w(10, 0) - 0.1, 0.25, 30)
fb(f'type(tl,"#s6 .kw",{q(tw)},0.06)')
pop("#s6 .snd", tw + 0.4)
up("#s6 .dmline", wf(10, "lien") - 0.2, 0.25, 20)
for k in range(1, 12):
    t = t6 + k * BEAT
    if t > TOTAL - 0.4:
        break
    R("#s6 .cta2", t, {"scale": 1.035}, {"scale": 1}, 0.14, "power2.out")
S("#flash", TOTAL - 0.6, {"backgroundColor": "#0a0a0f"})
R("#flash", TOTAL - 0.6, {"opacity": 0}, {"opacity": 1}, 0.55, "power2.in")       # fade to ink

# ------------------------------------------------------------------ captions (pill under the avatar)
caps, cjs, ci = [], [], 0
items = sorted(VO["lines"], key=lambda x: x["start"])
for n, it in enumerate(items):
    ws = []
    for x in it["words"]:
        if x["w"] in ("!",):
            continue
        if ws and x["w"][:1] in ("-", "'"):          # Whisper splits sous-titrer, l'IA...
            ws[-1] = dict(ws[-1], w=ws[-1]["w"] + x["w"], e=x["e"])
        else:
            ws.append(dict(x))
    if not ws:
        continue
    chunks, cur = [], []
    for x in ws:
        if cur and (len(" ".join(y["w"] for y in cur + [x])) > 22 or len(cur) >= 4):
            chunks.append(cur); cur = []
        cur.append(x)
    chunks.append(cur)
    end_line = min(it["end"] + 0.15, items[n + 1]["start"] - 0.02) if n + 1 < len(items) else it["end"] + 0.4
    for k, ch in enumerate(chunks):
        a = ch[0]["s"] - 0.03
        b = chunks[k + 1][0]["s"] - 0.03 if k + 1 < len(chunks) else end_line
        spans = " ".join(f'<span class="cw" id="c{ci}w{j}">{html.escape(x["w"])}</span>' for j, x in enumerate(ch))
        caps.append(f'<div class="cap" id="c{ci}">{spans}</div>')
        cjs.append(f'tl.fromTo("#c{ci}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.1,ease:"power2.out",immediateRender:false}},{q(max(0, a))});')
        cjs.append(f'tl.set("#c{ci}",{{opacity:0}},{q(b)});')
        cjs.append(f'tl.set("#cap",{{opacity:1}},{q(max(0, a))});')   # the pill only exists while words do
        if k + 1 == len(chunks):
            cjs.append(f'tl.set("#cap",{{opacity:0}},{q(b)});')
        for j, x in enumerate(ch):
            nxt = min(ch[j + 1]["s"] if j + 1 < len(ch) else b, b)
            cjs.append(f'tl.set("#c{ci}w{j}",{{color:"#eab308",textShadow:"0 0 16px rgba(234,179,8,.8)"}},{q(x["s"])});')
            cjs.append(f'tl.set("#c{ci}w{j}",{{color:"#EDEDED",textShadow:"0 0 0px rgba(234,179,8,0)"}},{q(nxt)});')
        ci += 1

# ------------------------------------------------------------------ write
TPL = open(os.path.join(HERE, "template.html")).read()
out = (TPL.replace("%%TOTAL%%", str(TOTAL)).replace("%%LEVELS%%", "\n".join(levels)).replace("%%SCENES%%", "\n".join(SCENES))
       .replace("%%COUNT%%", COUNT).replace("%%CAPTIONS%%", "\n".join(caps)).replace("%%OVERLAYS%%", "\n".join(OV))
       .replace("%%JS%%", "\n".join(js + cjs)))
pub = os.path.join(HERE, "public")
os.makedirs(os.path.join(pub, "kit"), exist_ok=True)
for f in ("kit.css", "kit.js"):
    shutil.copy(os.path.join(KIT, f), os.path.join(pub, "kit", f))
for f in ("avatar.mp4", "ex0.mp4", "ex1.mp4", "ex2.mp4", "ex3.mp4"):
    shutil.copy(os.path.join(BUILD, f), os.path.join(pub, f))
open(os.path.join(pub, "index.html"), "w").write(out)
print(f"index.html: {len(SCENES)} scènes, {ci} captions, {len(js)} animations, {TOTAL} s")

# ------------------------------------------------------------------ SFX
EV = [[0.0, "sfx-impact-deep.mp3", -17], [0.25, "sfx-thwip.mp3", -21], [round(wf(0, "poster") - 0.05, 3), "sfx-pop.mp3", -21]]
EV += [[round(1.94 + i * BEAT / 2, 3), "sfx-click-soft.mp3", -26] for i in range(7)]
EV += [[round(wf(1, "pas") - 0.05, 3), "sfx-landing-thud.mp3", -17]]
EV += [[round(SC_T[i] - 0.12, 3), "sfx-whoosh-lat.mp3", -22] for i in range(1, 6)]
EV += [[round(wf(2, k), 3), "sfx-click.mp3", -24] for k in KW]
EV += [[round(t2h, 3), "sfx-impact.mp3", -18], [round(w(3, 0), 3), "sfx-chime-v2.mp3", -18], [round(wf(15, "simple"), 3), "sfx-thwip.mp3", -20]]
EV += [[round(w(6, 0) - 0.15, 3), "sfx-web-latch.mp3", -19], [round(wf(6, "prête"), 3), "sfx-thwip.mp3", -21]]
EV += [[round(SC_T[4] + 0.1 + i * BEAT / 2, 3), "sfx-pop.mp3", -22] for i in range(3)]
EV += [[round(wf(16, "deux") - 0.05, 3), "sfx-glitch-soft.mp3", -22], [round(wf(16, "quelques"), 3), "sfx-confirm.mp3", -19]]
EV += [[round(wf(17, kw), 3), "sfx-confirm.mp3", -22] for _, _, kw in GET]
EV += [[round(L[li]["start"], 3), "sfx-impact-deep.mp3", g] for li, g in ((11, -19), (12, -17), (13, -15))]
EV += [[round(t6, 3), "sfx-impact-deep.mp3", -14], [round(t6, 3), "sfx-glass-break.mp3", -20], [round(tw, 3), "sfx-click-soft.mp3", -20],
       [round(wf(10, "lien") - 0.2, 3), "sfx-notify.mp3", -19]]
json.dump(sorted(EV), open(os.path.join(HERE, "events.json"), "w"))
print(f"events.json: {len(EV)} SFX")

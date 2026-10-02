#!/usr/bin/env python3
"""autoboost-77 - VSL ShortForge, pdoom-video grammar in the AutomatisationBoost charter.

32 s = 16 bars of hook-epical-drums at 120 BPM: every scene cut is a downbeat (even
second), stamps and pulses land on beats, every word slam lands on the cloned voice's
word (vo.json, never ahead of it). pdoom pieces ported: the spark that cuts through
the plates, the full-frame word slams, the bureau-paper inverted plate with its rubber
stamp, the vertical Gantt with a playhead, the number readout blown up, the prompt
field, deadpan mono footnotes, crop marks at the bookends, flash / shake / zoom.
pdoom's orange becomes gold, its mono voice violet, its one acid-green accent a
violet flash (no green in the charter).

  BUILD=<dir with vo.json, avatar.mp4, proof/> python3 gen.py
"""
import json, os, html, shutil, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
KIT = os.path.abspath(os.path.join(PROJ, "..", "_shared", "facecam-boost-kit"))
sys.path.insert(0, KIT)
from kit import icon, chars, sticker, elastic  # noqa: E402

BUILD = os.environ.get("BUILD", os.path.join(PROJ, "build"))
VO = json.load(open(os.path.join(BUILD, "vo.json")))
FPS, TOTAL, BEAT = 30, 32.0, 0.5


def q(t):
    return round(round(t * FPS) / FPS, 4)


def w(li, k):
    """start of word k of VO line li (the slam never precedes the voice)."""
    ws = VO[li]["words"]
    return ws[min(k, len(ws) - 1)]["s"] if ws else VO[li]["start"]


js = []


def R(sel, t, frm, to, d=0.3, ease="power3.out"):
    js.append(f'tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(dict(to, duration=d, ease=ease, immediateRender=False))},{q(t)});')


def S(sel, t, props):
    js.append(f'tl.set({json.dumps(sel)},{json.dumps(props)},{q(t)});')


def show(sel, a, b=None):
    S(sel, a, {"opacity": 1})
    if b is not None:
        S(sel, b, {"opacity": 0})


def slam(sel, t, s0=1.35, d=0.22):
    R(sel, t, {"opacity": 0, "scale": s0}, {"opacity": 1, "scale": 1}, d, "expo.out")


def shake(t, amp=10, n=6):
    rnd = random.Random(int(t * 1000))
    for k in range(n):
        a = amp * (1 - k / n)
        S("#stage", t + k / FPS, {"x": round(rnd.uniform(-a, a), 1), "y": round(rnd.uniform(-a, a), 1)})
    S("#stage", t + n / FPS, {"x": 0, "y": 0})


def flash(t, op=0.8, d=0.2, color="#fff3b0"):
    S("#flash", t, {"backgroundColor": color})
    R("#flash", t, {"opacity": op}, {"opacity": 0}, d, "power2.out")


def fb(call):
    js.append("FB." + call + ";")


def scene(sid, a, b, inner, cls="", track=2):
    return (f'<section id="{sid}" class="scene clip {cls}" data-start="{q(a)}" data-duration="{q(b - a)}" '
            f'data-track-index="{track}">{inner}</section>')


def foot(text):
    return f'<div class="foot">{html.escape(text)}</div>'


def mid(text, cls="w", size=120, top=860, extra=""):
    return f'<div class="row" style="top:{top}px"><div class="hd {extra}" style="font-size:{size}px">{chars(text, cls)}</div></div>'


SC = []      # scenes
OV = []      # overlays (stickers)

# ---------------------------------------------------------------- S0  hook visuel 0-1: « 2 H » cut by the spark
SC.append(scene("s0", 0, 1.0,
    '<div class="big2h half top">2 H</div><div class="big2h half bot">2 H</div>'
    + "".join(f'<i class="ember e{k}"></i>' for k in range(12))
    + foot("fig. 1 · une vidéo à la main")))
R("#s0 .half", 0, {"scale": 1.18}, {"scale": 1}, 0.27, "expo.out")
shake(0.0, 8)
R("#spark", 0.5, {"x": -120, "y": 930, "opacity": 1}, {"x": 1180, "y": 930, "opacity": 1}, 0.18, "power2.in")
S("#spark", 0.7, {"opacity": 0})
R("#s0 .top", 0.6, {"y": 0, "opacity": 1}, {"y": -60, "opacity": 0}, 0.38, "power2.in")
R("#s0 .bot", 0.6, {"y": 0, "opacity": 1}, {"y": 60, "opacity": 0}, 0.38, "power2.in")
rnd = random.Random(7)
for k in range(12):
    x0 = 120 + k * 75
    R(f"#s0 .e{k}", 0.55 + k * 0.012, {"x": x0, "y": 930, "opacity": 1, "scale": 1},
      {"x": x0 + rnd.uniform(-60, 60), "y": 930 + rnd.uniform(-260, 260), "opacity": 0, "scale": 0.3}, 0.42, "power2.out")

# ---------------------------------------------------------------- S1  hook verbal 1-4: word slams, then the dense stack
G1 = [("TU SAIS", "w", 0), ("QU'IL FAUT", "w", 2), ("POSTER", "g", 5), ("TOUS LES JOURS.", "w", 6)]
SC.append(scene("s1", 1.0, 4.0,
    "".join(f'<div class="row slam g{i}" style="top:800px"><div class="hd" style="font-size:{[150, 140, 200, 120][i]}px">{chars(t, c)}</div></div>'
            for i, (t, c, _) in enumerate(G1))
    + '<div class="stack">' + "".join(f'<div class="sl st{i}"><span class="{c}">{html.escape(t)}</span></div>' for i, (t, c, _) in enumerate(G1)) + '</div>'
    + foot("fig. 2 · ce que tout le monde sait")))
ts = [w(0, k) for _, _, k in G1]
for i, t in enumerate(ts):
    slam(f"#s1 .g{i}", t)
    S(f"#s1 .g{i} .char", t, {"opacity": 1})
    if i < 3:
        S(f"#s1 .g{i}", ts[i + 1], {"opacity": 0})
R("#s1 .g2 .char", ts[2], {"y": 80}, {"y": 0}, 0.25, "back.out(2)")            # POSTER rises
R("#s1 .g3", ts[3], {"scaleX": 1.15}, {"scaleX": 0.86}, 0.5, "power2.out")      # pressure
S("#s1 .g3", 2.5, {"opacity": 0})
R("#s1 .stack", 2.5, {"opacity": 0, "scale": 1.1}, {"opacity": 1, "scale": 1}, 0.2, "expo.out")
for b in (3.0, 3.5):
    R("#s1 .stack", b, {"scale": 1.04}, {"scale": 1}, 0.2, "power2.out")
R("#stage", 2.0, {"scale": 1.0}, {"scale": 1.06}, 0.12, "power3.out")
R("#stage", 2.12, {"scale": 1.06}, {"scale": 1.0}, 0.3, "power2.inOut")

# ---------------------------------------------------------------- S2  relance 4-6: the bureau paper plate + stamp
SC.append(scene("s2", 4.0, 6.0,
    '<div class="paper"></div>'
    '<div class="row" style="top:640px"><div class="ink" style="font-size:130px">TU NE LE</div></div>'
    '<div class="row" style="top:800px"><div class="ink" style="font-size:210px">FAIS</div></div>'
    '<div class="row" style="top:1050px"><div class="rstamp">PAS.</div></div>'
    + '<div class="foot dark">fig. 3 · la relance (hook n°2)</div>'))
R("#s2 .ink", w(1, 0), {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, 0.16, "power3.out")
R("#s2 .rstamp", w(1, 4), {"opacity": 0, "scale": 2.4, "rotation": -16}, {"opacity": 1, "scale": 1, "rotation": -7}, 0.2, "power4.in")
shake(w(1, 4) + 0.2, 12)

# ---------------------------------------------------------------- S3  problem + cost 6-10: vertical Gantt, playhead, clock
STEPS6 = ["ÉCRIRE", "FILMER", "MONTER", "SOUS-TITRER", "EXPORTER", "PUBLIER"]
KW = [0, 1, 2, 3, 5, 6]
CLK = ["0 h 00", "0 h 20", "0 h 40", "1 h 00", "1 h 20", "1 h 40", "2 h 00"]
SC.append(scene("s3", 6.0, 10.0,
    '<div class="clock">' + "".join(f'<b class="ck{i}">{c}</b>' for i, c in enumerate(CLK)) + '<small>temps passé</small></div>'
    + '<i class="rail"></i>'
    + "".join(f'<div class="gt gt{i}" style="top:{470 + i * 150}px"><em>{i + 1:02d}</em><span>{s}</span><i class="tick">{icon("check", 30)}</i></div>'
              for i, s in enumerate(STEPS6))
    + foot("fig. 4 · source : page de vente ShortForge")))
show("#s3 .ck0", 6.0)
for i, k in enumerate(KW):
    t = w(2, k)
    R(f"#s3 .gt{i}", t, {"opacity": 0, "x": 120, "scale": 1.15}, {"opacity": 1, "x": 0, "scale": 1}, 0.18, "expo.out")
    R(f"#s3 .gt{i} .tick", t + 0.12, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.18, "back.out(3)")
    S(f"#s3 .ck{i}", t, {"opacity": 0})
    show(f"#s3 .ck{i + 1}", t)
R("#s3 .rail", 6.0, {"scaleY": 0}, {"scaleY": 1}, 3.0, "none")
R("#spark", 6.0, {"x": 132, "y": 470, "opacity": 1}, {"x": 132, "y": 1300, "opacity": 1}, 3.0, "none")
S("#spark", 9.6, {"opacity": 0})
t2h = w(2, 7)
R("#s3 .clock b", t2h, {"color": "#EDEDED"}, {"color": "#ff6b6b"}, 0.15, "power2.out")
R("#s3 .clock", t2h, {"scale": 1}, {"scale": 1.25}, 0.18, "back.out(3)")
OV.append(sticker("st-lent", "TROP", "LENT", "red", "clock", "spark", left=560, top=1390))
fb(f'sticker(tl,"#st-lent",{q(t2h)},{q(9.85)},-6)')

# ---------------------------------------------------------------- S4  reveal 10-12: collapse into the spark, violet flash, SHORTFORGE
SC.append(scene("s4", 10.0, 12.0,
    '<div class="row" style="top:760px"><div class="hd big" style="font-size:118px">' + elastic("SHORTFORGE", "fb-g") + '</div></div>'
    '<div class="row" style="top:960px"><div class="mono tag">skill Claude Code</div></div>'
    + mid("FAIT LES 6 ÉTAPES", "w", 70, 1090)
    + foot("fig. 5 · l'outil")))
R("#s3 .gt", 9.9, {"scaleY": 1, "opacity": 1}, {"scaleY": 0, "opacity": 0}, 0.1, "power4.in")
flash(10.0, 0.85, 0.3, "#8b5cf6")
R("#s4 .big", w(3, 0), {"opacity": 0, "scaleX": 0.55}, {"opacity": 1, "scaleX": 1}, 0.3, "expo.out")
fb(f'elastic(tl,"#s4 .big",{q(w(3, 0) + 0.3)},1.4)')
R("#s4 .tag", w(3, 1), {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, 0.2)
js.append(f'tl.fromTo("#s4 .hd:not(.big) .char",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.2,ease:"back.out(2)",stagger:.02,immediateRender:false}},{q(w(3, 2))});')

# ---------------------------------------------------------------- S5  method 12-18: three plates, one bar each, exit left / enter right
BRIEF = "brief : présente mon offre en 30 s"
SC.append(scene("s5a", 12.0, 14.0,
    '<div class="lab"><b>1</b> TU COLLES UN BRIEF</div>'
    '<div class="field"><span class="typed">' + chars(BRIEF) + '</span><i class="caret"></i><i class="ret">⏎</i></div>'
    '<div class="dist">' + "".join(f'<div class="dr d{k}"><i style="width:{wd}px"></i></div>' for k, wd in enumerate([360, 220, 140, 80])) + '</div>'
    + foot("fig. 6 · étape 1 / 3"), "plate"))
SC.append(scene("s5b", 14.0, 16.0,
    '<div class="lab"><b>2</b> VOIX · AVATAR · CAPTIONS</div>'
    '<svg class="scope" width="1000" height="200" viewBox="0 0 1000 200"><path d="' + " ".join(
        ("M" if i == 0 else "L") + f" {i * 10} {100 + 60 * math.sin(i * 0.45) * math.sin(i * 0.07 + 0.4):.1f}" for i in range(101)) + '"/></svg>'
    '<div class="avc"><i class="avring"></i></div>'
    '<div class="capp"><span class="cw c0">ta voix</span> <span class="cw c1">ton avatar</span> <span class="cw c2">les captions</span></div>'
    + foot("fig. 7 · étape 2 / 3 · un seul tournage"), "plate"))
SC.append(scene("s5c", 16.0, 18.0,
    '<div class="lab"><b>3</b> UNE VIDÉO VERTICALE</div>'
    '<svg class="phone" width="440" height="780" viewBox="0 0 440 780"><rect x="6" y="6" width="428" height="768" rx="56"/></svg>'
    '<img class="pthumb" src="proof/p3.jpg">'
    '<div class="row" style="top:1430px"><div class="mono dim">1080 × 1920 · TikTok · Reels · Shorts</div></div>'
    '<div class="gstamp">PRÊT À POSTER</div>'
    + foot("fig. 8 · étape 3 / 3"), "plate"))
for sid, a in (("s5a", 12.0), ("s5b", 14.0), ("s5c", 16.0)):
    R(f"#{sid}", a, {"x": 1080}, {"x": 0}, 0.3, "power4.out")
    R(f"#{sid}", a + 1.72, {"x": 0}, {"x": -1080}, 0.28, "power3.in")
R("#streak", 11.7, {"x": 1300}, {"x": -1500}, 0.36, "power2.inOut")
R("#streak", 13.7, {"x": 1300}, {"x": -1500}, 0.36, "power2.inOut")
R("#streak", 15.7, {"x": 1300}, {"x": -1500}, 0.36, "power2.inOut")
R("#s5a .field", 12.05, {"opacity": 0, "scaleX": 0.6}, {"opacity": 1, "scaleX": 1}, 0.25, "expo.out")
fb(f'type(tl,"#s5a .typed",{q(w(4, 0))},0.032)')
R("#s5a .caret", 12.1, {"x": 0}, {"x": 760}, 1.15, "none")
for k in range(4):
    R(f"#s5a .d{k} i", 12.3 + k * 0.08, {"scaleX": 0}, {"scaleX": 1}, 0.25, "power3.out")
R("#s5a .dist", 13.0, {"opacity": 1}, {"opacity": 0.3}, 0.3)
R("#s5a .ret", 13.5, {"opacity": 0, "scale": 2}, {"opacity": 1, "scale": 1}, 0.18, "back.out(3)")
R("#s5a .field", 13.5, {"borderColor": "#eab308"}, {"borderColor": "#8b5cf6"}, 0.15)
# step 2 - each layer pops on its word
R("#s5b .scope path", w(5, 1), {"strokeDashoffset": 1400}, {"strokeDashoffset": 0}, 0.5, "power2.out")
for b in (14.5, 15.0, 15.5):
    R("#s5b .scope", b, {"scaleY": 1.5}, {"scaleY": 1}, 0.25, "power2.out")
R("#avatar", w(5, 3) - 0.05, {"opacity": 0, "scale": 0.6}, {"opacity": 1, "scale": 1}, 0.3, "back.out(2)")
R("#s5b .avc", w(5, 3) - 0.05, {"opacity": 0, "scale": 0.6}, {"opacity": 1, "scale": 1}, 0.3, "back.out(2)")
S("#avatar", 15.95, {"opacity": 0})
R("#s5b .capp", w(5, 5) - 0.1, {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0}, 0.2)
for k, (a, b) in enumerate([(w(5, 1), w(5, 3)), (w(5, 3), w(5, 5)), (w(5, 5), 16.0)]):
    S(f"#s5b .c{k}", a, {"color": "#eab308", "textShadow": "0 0 18px rgba(234,179,8,.8)"})
    S(f"#s5b .c{k}", b, {"color": "#EDEDED", "textShadow": "0 0 0px rgba(234,179,8,0)"})
# step 3 - the spark draws the phone, the stamp lands on « prête »
R("#s5c .phone rect", 16.05, {"strokeDashoffset": 2400}, {"strokeDashoffset": 0}, 0.55, "power2.inOut")
R("#s5c .pthumb", 16.6, {"opacity": 0, "scale": 0.9}, {"opacity": 1, "scale": 1}, 0.25, "power3.out")
R("#s5c .dim", 16.8, {"opacity": 0}, {"opacity": 1}, 0.2)
R("#s5c .gstamp", w(6, 3), {"opacity": 0, "scale": 2.4, "rotation": -18}, {"opacity": 1, "scale": 1, "rotation": -8}, 0.2, "power4.in")
shake(w(6, 3) + 0.2, 8)

# ---------------------------------------------------------------- S6  proof 18-22: six real frames, then the cost readout
SC.append(scene("s6a", 18.0, 20.0,
    "".join(f'<img class="pf pf{k}" src="proof/p{k}.jpg">' for k in range(6))
    + '<div class="pshade"></div>'
    + mid("6 FORMATS", "w", 120, 760) + mid("DÉJÀ PUBLIÉS", "g", 110, 900)
    + '<div class="foot">fig. 9 · images de vidéos déjà sorties</div>'))
for k in range(6):
    t = 18.0 + k * 0.25
    show(f"#s6a .pf{k}", t)
    R(f"#s6a .pf{k}", t, {"scale": 1.08}, {"scale": 1}, 0.25, "power2.out")
R("#s6a .pshade", 19.5, {"opacity": 0}, {"opacity": 1}, 0.15)
js.append(f'tl.fromTo("#s6a .hd .char",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.18,ease:"back.out(2)",stagger:.015,immediateRender:false}},{q(w(7, 2))});')
SC.append(scene("s6b", 20.0, 22.0,
    '<div class="mono math">coût / vidéo</div>'
    '<div class="row" style="top:560px"><div class="old">80–150 €<svg width="640" height="60" viewBox="0 0 640 60"><path d="M10 40 C 200 10, 440 50, 630 18"/></svg></div></div>'
    '<div class="row" style="top:770px"><div class="mono dim">un monteur freelance</div></div>'
    '<div class="row" style="top:930px"><div class="readout">≈ 0,50 €</div></div>'
    '<div class="tbar">' + "".join(f'<i class="tk{k}"></i>' for k in range(24)) + '</div>'
    + foot("fig. 10 · API vocale à ton compte · source : page de vente")))
R("#s6b .old", 20.05, {"opacity": 0, "scale": 1.3}, {"opacity": 1, "scale": 1}, 0.2, "expo.out")
R("#s6b .dim", 20.15, {"opacity": 0}, {"opacity": 1}, 0.2)
R("#s6b .old path", w(8, 1), {"strokeDashoffset": 700}, {"strokeDashoffset": 0}, 0.22, "power2.out")
R("#s6b .old", w(8, 1) + 0.2, {"opacity": 1}, {"opacity": 0.4}, 0.2)
R("#s6b .readout", w(8, 2), {"opacity": 0, "scale": 1.6}, {"opacity": 1, "scale": 1}, 0.24, "expo.out")
shake(w(8, 2), 10)
js.append(f'tl.fromTo("#s6b .tbar i",{{scaleY:0}},{{scaleY:1,duration:.12,ease:"power2.out",stagger:.02,immediateRender:false}},{q(w(8, 2) + 0.1)});')

# ---------------------------------------------------------------- S7  price + action 22-26
SC.append(scene("s7", 22.0, 26.0,
    '<div class="pcard"><small>SHORTFORGE · SKILL CLAUDE CODE</small>'
    '<div class="prow"><span class="p97">97 €<svg width="230" height="40" viewBox="0 0 230 40"><path d="M6 30 L224 8"/></svg></span><span class="p67">67 €</span></div>'
    '<div class="plines"><span>prix fondateur</span><span>paiement unique</span><span>garantie 14 jours</span></div></div>'
    '<div class="cfield"><span class="pre">commente</span><span class="kw">' + chars("FORGE") + f'</span><i class="snd">{icon("send", 44)}</i></div>'
    + foot("fig. 11 · ce que tu reçois")))
R("#s7 .pcard", 22.0, {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0}, 0.25, "expo.out")
R("#s7 .p97 path", w(9, 0) + 0.1, {"strokeDashoffset": 260}, {"strokeDashoffset": 0}, 0.2)
R("#s7 .p67", w(9, 0), {"opacity": 0, "scale": 1.8}, {"opacity": 1, "scale": 1}, 0.24, "expo.out")
shake(w(9, 0) + 0.05, 8)
js.append(f'tl.fromTo("#s7 .plines span",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.2,stagger:.12,ease:"power3.out",immediateRender:false}},{q(w(9, 3))});')
R("#s7 .cfield", w(10, 0) - 0.1, {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0}, 0.2)
fb(f'type(tl,"#s7 .kw",{q(w(10, 1))},0.06)')
R("#s7 .snd", w(10, 1) + 0.4, {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, 0.2, "back.out(3)")
fb(f'press(tl,"#s7 .snd",{q(w(10, 2))})')

# ---------------------------------------------------------------- S8  countdown 26-28 on beats, freeze 27.4-28
SC.append(scene("s8", 26.0, 28.0,
    "".join(f'<div class="num n{n}"><span class="c3">{n}</span><span class="c2">{n}</span><span class="c1">{n}</span></div>' for n in (3, 2, 1))))
for n, t in ((3, 26.0), (2, 26.5), (1, 27.0)):
    R(f"#s8 .n{n}", t, {"opacity": 0, "scale": 1.4}, {"opacity": 1, "scale": 1}, 0.16, "expo.out")
    R(f"#s8 .n{n} .c2", t, {"x": 0, "y": 0}, {"x": 16, "y": 14}, 0.16, "power3.out")
    R(f"#s8 .n{n} .c3", t, {"x": 0, "y": 0}, {"x": 32, "y": 28}, 0.16, "power3.out")
    shake(t, 8 + (3 - n) * 4, 5)
    if n > 1:
        S(f"#s8 .n{n}", t + 0.5, {"opacity": 0})
# 27.4 -> 28.0: nothing moves (VSL page: a short freeze before the strong moment)

# ---------------------------------------------------------------- S9  detonation 28-32: COMMENTE FORGE held, pulses on every beat
SC.append(scene("s9", 28.0, TOTAL,
    '<svg class="burst" width="1080" height="1920" viewBox="0 0 1080 1920">' + "".join(
        f'<line x1="540" y1="930" x2="{540 + 1400 * math.cos(a):.0f}" y2="{930 + 1400 * math.sin(a):.0f}" stroke="{"#eab308" if k % 3 else "#8b5cf6"}" stroke-width="{2 + (k * 7) % 5}"/>'
        for k, a in enumerate([2 * math.pi * k / 64 + (k % 5) * 0.013 for k in range(64)])) + '</svg>'
    + '<div class="row" style="top:640px"><div class="hd cm" style="font-size:120px">' + chars("COMMENTE", "w") + '</div></div>'
    + '<div class="row" style="top:800px"><div class="hd fg">' + elastic("FORGE", "fb-g") + '</div></div>'
    + '<div class="row" style="top:1180px"><div class="mono dim2">→ le lien de ShortForge en DM</div></div>'))
flash(28.0, 0.9, 0.22, "#ffffff")
shake(28.0, 16, 8)
R("#s9 .burst", 28.0, {"opacity": 1, "scale": 0.1}, {"opacity": 0, "scale": 1.6}, 0.7, "expo.out")
js.append('tl.fromTo("#s9 .cm .char",{opacity:0,y:-50},{opacity:1,y:0,duration:.18,ease:"expo.out",stagger:.02,immediateRender:false},%s);' % q(28.02))
R("#s9 .fg", 28.05, {"opacity": 0, "scale": 2.2}, {"opacity": 1, "scale": 1}, 0.25, "power4.in")
fb(f'elastic(tl,"#s9 .fg",{q(28.4)},1.9)')
R("#s9 .dim2", 28.6, {"opacity": 0}, {"opacity": 1}, 0.25)
for k in range(1, 8):
    R("#s9 .fg", 28.0 + k * BEAT, {"scale": 1.04}, {"scale": 1}, 0.14, "power2.out")
R("#crops", 31.0, {"opacity": 1, "scale": 1.12}, {"opacity": 1, "scale": 1}, 0.6, "power3.inOut")
R("#s9 .row", 31.55, {"opacity": 1}, {"opacity": 0}, 0.4, "power2.in")

# ---------------------------------------------------------------- global: crop marks at the bookends, a beat pulse under everything
S("#crops", 0, {"opacity": 1})
S("#crops", 1.0, {"opacity": 0})
for k in range(64):
    t = k * BEAT
    if 27.4 <= t < 28.0:
        continue  # the freeze
    R("#pulse", t, {"opacity": 0.55 if k % 4 == 0 else 0.25}, {"opacity": 0}, 0.3, "power2.out")

# ---------------------------------------------------------------- write
TPL = open(os.path.join(HERE, "template.html")).read()
out = (TPL.replace("%%TOTAL%%", str(TOTAL)).replace("%%SCENES%%", "\n".join(SC))
       .replace("%%OVERLAYS%%", "\n".join(OV)).replace("%%JS%%", "\n".join(js)))
pub = os.path.join(HERE, "public")
os.makedirs(os.path.join(pub, "kit"), exist_ok=True)
for f in ("kit.css", "kit.js"):
    shutil.copy(os.path.join(KIT, f), os.path.join(pub, "kit", f))
shutil.copy(os.path.join(BUILD, "avatar.mp4"), os.path.join(pub, "avatar.mp4"))
shutil.copytree(os.path.join(BUILD, "proof"), os.path.join(pub, "proof"), dirs_exist_ok=True)
open(os.path.join(pub, "index.html"), "w").write(out)
print(f"index.html: {len(SC)} scènes, {len(js)} animations")

# ---------------------------------------------------------------- SFX (facecam_audio.py events)
EV = [[0.0, "sfx-impact-deep.mp3", -16], [0.5, "sfx-glitch-hard.mp3", -18]]
EV += [[round(t, 3), "sfx-thwip.mp3", -21] for t in ts]
EV += [[round(w(1, 4), 3), "sfx-landing-thud.mp3", -15]]
EV += [[round(w(2, k), 3), "sfx-click.mp3", -22] for k in KW]
EV += [[round(t2h, 3), "sfx-impact.mp3", -17], [9.7, "sfx-whoosh-v2.mp3", -18], [10.0, "sfx-chime-v2.mp3", -16]]
EV += [[11.7, "sfx-whoosh-lat.mp3", -20], [13.7, "sfx-whoosh-lat.mp3", -20], [15.7, "sfx-whoosh-lat.mp3", -20]]
EV += [[13.5, "sfx-confirm.mp3", -18], [round(w(5, 3) - 0.05, 3), "sfx-pop.mp3", -19], [round(w(6, 3), 3), "sfx-web-latch.mp3", -16]]
EV += [[round(18.0 + k * 0.25, 3), "sfx-zoom.mp3", -26] for k in range(6)]
EV += [[round(w(8, 1), 3), "sfx-glitch-soft.mp3", -20], [round(w(8, 2), 3), "sfx-confirm.mp3", -17]]
EV += [[round(w(9, 0), 3), "sfx-impact.mp3", -17], [round(w(10, 1), 3), "sfx-click-soft.mp3", -19]]
EV += [[26.0, "sfx-impact-deep.mp3", -18], [26.5, "sfx-impact-deep.mp3", -16], [27.0, "sfx-impact-deep.mp3", -14]]
EV += [[28.0, "sfx-impact-deep.mp3", -13], [28.0, "sfx-glass-break.mp3", -18], [31.0, "sfx-whoosh-lat.mp3", -21]]
json.dump(sorted(EV), open(os.path.join(HERE, "events.json"), "w"))
print(f"events.json: {len(EV)} SFX")

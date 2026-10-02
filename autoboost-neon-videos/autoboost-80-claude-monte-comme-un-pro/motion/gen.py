#!/usr/bin/env python3
"""autoboost-80 - « Claude monte comme un pro » (remake of @pauloshimas' reel, Tony's style, Tony vs Tony IA).

Tony = his real take, matted (tony.webm), with the unmatted take (tony_src.mp4) underneath for the
segmentation reveal. Tony IA = the BUREAU avatar in a violet neon circle, lips moving only on its lines.
Every reveal is pinned to a word of the cloned voice (build.py -> vo.json).

  BUILD=<build dir> python3 gen.py
"""
import json, os, html, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
KIT = os.path.abspath(os.path.join(PROJ, "..", "_shared", "facecam-boost-kit"))
sys.path.insert(0, KIT)
from kit import icon, chars as _chars, sticker, elastic  # noqa: E402

BUILD = os.environ.get("BUILD", os.path.join(PROJ, "build"))
VO = json.load(open(os.path.join(BUILD, "vo.json")))
TOTAL = VO["total"]
L = VO["lines"]
CUTS = json.load(open(os.path.join(BUILD, "tony_cuts.json")))["cuts"]
FPS = 30


def chars(text, cls=""):
    return '<span class="char sp">&nbsp;</span>'.join(f'<span style="white-space:nowrap">{_chars(w, cls)}</span>' for w in text.split(" "))


def q(t):
    return round(round(t * FPS) / FPS, 4)


def ws(li):
    return L[li]["words"] or [{"w": L[li]["text"], "s": L[li]["start"], "e": L[li]["end"]}]


def wf(li, needle, nth=0):
    hits = [w for w in ws(li) if needle.lower() in w["w"].lower()]
    return hits[min(nth, len(hits) - 1)]["s"] if hits else L[li]["start"]


st = lambda li: L[li]["start"]      # noqa: E731
en = lambda li: L[li]["end"]        # noqa: E731
js = []


def R(sel, t, frm, to, d=0.3, ease="power3.out"):
    js.append(f'tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(dict(to, duration=d, ease=ease, immediateRender=False))},{q(t)});')


def S(sel, t, props):
    js.append(f'tl.set({json.dumps(sel)},{json.dumps(props)},{q(t)});')


def up(sel, t, d=0.3, dist=40):
    R(sel, t, {"opacity": 0, "y": dist}, {"opacity": 1, "y": 0}, d)


def pop(sel, t, d=0.3):
    R(sel, t, {"opacity": 0, "scale": 0.5}, {"opacity": 1, "scale": 1}, d, "back.out(2.2)")


def kin(sel, t, stagger=0.022, d=0.3):
    js.append(f'tl.fromTo({json.dumps(sel + " .char")},{{opacity:0,y:40}},{{opacity:1,y:0,duration:{d},ease:"back.out(1.8)",stagger:{stagger},immediateRender:false}},{q(t)});')


def hl(sel, t):
    R(sel, t, {"backgroundSize": "0% 100%"}, {"backgroundSize": "100% 100%"}, 0.35, "power2.out")


def fb(c):
    js.append("FB." + c + ";")


def flash(t, op=0.4, d=0.22, color="#fff3b0"):
    S("#flash", t, {"backgroundColor": color})
    R("#flash", t, {"opacity": op}, {"opacity": 0}, d, "power2.out")


def stamp(sel, t, rot=-8):
    R(sel, t, {"opacity": 0, "scale": 2.3, "rotation": rot - 12}, {"opacity": 1, "scale": 1, "rotation": rot}, 0.22, "power4.in")


SC, OV, EV = [], [], []


def scene(sid, a, b, inner):
    s0, s1 = max(0, a - 0.3), min(TOTAL, b + 0.3)
    SC.append(f'<section id="{sid}" class="scene clip" data-start="{q(s0)}" data-duration="{q(s1 - s0)}" data-track-index="{2 + len(SC) % 2}">'
              f'<div class="in">{inner}</div></section>')
    if a > 0.1:
        R(f"#{sid} .in", a - 0.1, {"opacity": 0, "x": 120}, {"opacity": 1, "x": 0}, 0.28)
        EV.append([a - 0.1, "sfx-whoosh-lat.mp3", -23])
    if b < TOTAL - 0.2:
        R(f"#{sid} .in", b - 0.18, {"opacity": 1, "x": 0}, {"opacity": 0, "x": -120}, 0.18, "power2.in")


# ------------------------------------------------------------------ Tony (cutout) + base, punch-ins on every cut
TY, BASE = 640, 0.94
for sel in ("#tony", "#basew"):
    S(sel, 0, {"x": 0, "y": TY, "scale": BASE})
R("#tony", 0, {"scale": BASE * 1.25, "y": TY + 100}, {"scale": BASE, "y": TY}, 0.32, "expo.out")
flash(0.12, 0.35)
EV.append([0.0, "sfx-impact-deep.mp3", -17])
z = BASE
for c in CUTS[1:]:
    z = BASE * 1.06 if z == BASE else BASE
    for sel in ("#tony", "#basew"):
        S(sel, c, {"scale": z})

# ------------------------------------------------------------------ Tony IA: violet circle bottom-right, glitch entrance on its first line
IAX, IAY, IAS = 640, 1130, 0.62
S("#iaw", 0, {"x": IAX, "y": IAY, "scale": IAS, "opacity": 0})
for n, it in enumerate(l for l in L if l["who"] == "ia"):
    a, b = it["start"], it["end"]
    if n == 0:
        for k, (dx, op) in enumerate([(50, 1), (-70, .4), (30, 1), (-12, .7), (0, 1)]):
            S("#iaw", a - 0.12 + k * 0.04, {"x": IAX + dx, "opacity": op, "skewX": [-10, 7, -4, 2, 0][k]})
        flash(a - 0.12, 0.6, 0.25, "#ede9fe")
        EV.append([a - 0.12, "sfx-glitch-hard.mp3", -16])
    else:
        R("#iaw", a - 0.15, {"opacity": 0, "x": 1100, "scale": IAS}, {"opacity": 1, "x": IAX, "scale": IAS}, 0.28, "back.out(1.6)")
        EV.append([a - 0.15, "sfx-thwip.mp3", -20])
    R("#iaw", b + 0.05, {"opacity": 1, "x": IAX}, {"opacity": 0, "x": 1100}, 0.22, "power2.in")
    R("#tony", a - 0.1, {"filter": "brightness(1)"}, {"filter": "brightness(.72)"}, 0.2)        # Tony listens
    R("#tony", b, {"filter": "brightness(.72)"}, {"filter": "brightness(1)"}, 0.2)

# ------------------------------------------------------------------ 0 hook: Claude monte comme un pro (+ IA line 1)
scene("s0", 0, st(2) - 0.15,
      '<div class="dhead"><div class="p">' + chars("Claude monte") + '</div><div><span class="hl h">' + chars("comme un pro.") + '</span></div></div>'
      f'<div style="text-align:center;margin-top:34px"><span class="chip c0"><i>{icon("brain", 36)}</i>Claude Code · HyperFrames</span></div>')
kin("#s0 .p", 0.0)
kin("#s0 .h", wf(0, "comme"), 0.03)
hl("#s0 .h", wf(0, "comme") + 0.1)
pop("#s0 .c0", wf(0, "pro"))
OV.append(sticker("st-sur", "MAIS BIEN", "SÛR.", "violet", None, "spark", left=60, top=1240))
fb(f'sticker(tl,"#st-sur",{q(wf(1, "déjà"))},{q(en(1) + 0.1)},-5)')
EV.append([wf(1, "déjà"), "sfx-thwip.mp3", -21])

# ------------------------------------------------------------------ 1 vision: boxes on the real room (+ IA: coiffure en option)
BOX = [("plante", "PLANTE", 0, 580, 70, 180, ""), ("figurine", "FIGURINE", 0, 740, 124, 320, ""), ("horloge", "HORLOGE", 124, 800, 216, 260, ""),
       ("moi", "TONY", 400, 240, 520, 560, " v")]
k = 480 / 1080
boxes = "".join(f'<i class="box b{i}{v}" style="left:{x * k:.0f}px;top:{y * k:.0f}px;width:{w * k:.0f}px;height:{h * k:.0f}px"><b>{lab}</b></i>'
                for i, (_, lab, x, y, w, h, v) in enumerate(BOX))
scene("s1", st(2) - 0.15, st(4) - 0.15,
      '<div style="text-align:center"><span class="kick">1 · <b>VISION</b></span></div>'
      f'<div class="cam"><img src="room.jpg">{boxes}<i class="scanl"></i><span class="hud">détection · 4 objets</span></div>')
R("#s1 .kick", st(2), {"opacity": 0, "y": -20}, {"opacity": 1, "y": 0}, 0.25)
up("#s1 .cam", st(2) + 0.05, 0.3, 50)
R("#s1 .scanl", wf(2, "reconna"), {"opacity": 1, "y": 0}, {"opacity": 1, "y": 634}, 0.9, "none")
for i, (needle, *_r) in enumerate(BOX):
    t = wf(2, needle, 1 if needle == "moi" else 0)
    R(f"#s1 .b{i}", t, {"opacity": 0, "scale": 1.3}, {"opacity": 1, "scale": 1}, 0.2, "back.out(2)")
    EV.append([t, "sfx-click.mp3", -21])
# IA: « objet numéro quatre : humain » -> the label changes, then the sticker
S("#s1 .b3 b", wf(3, "humain"), {"backgroundColor": "#ff6b6b"})
js.append(f'tl.set("#s1 .b3 b",{{innerText:"HUMAIN ?"}},{q(wf(3, "humain"))});')
OV.append(sticker("st-coif", "COIFFURE", "EN OPTION", "red", None, "spark", left=110, top=860))
fb(f'sticker(tl,"#st-coif",{q(wf(3, "coiffure"))},{q(en(3) + 0.3)},-7)')
EV.append([wf(3, "coiffure"), "sfx-impact.mp3", -19])

# ------------------------------------------------------------------ 2 transcription: his words with their real timestamps (+ IA: les euh)
tw = [w for w in ws(4) if w["w"].strip(".,…")][:9]
chips = "".join(f'<span class="tw t{i}"><small>0:{w["s"]:05.2f}</small><span>{html.escape(w["w"].strip(".,"))}</span></span>' for i, w in enumerate(tw))
euh = "".join(f'<span class="tw euh e{i}"><small>0:{(st(5) + i * 0.4):05.2f}</small><span>euh</span></span>' for i in range(3))
scene("s2", st(4) - 0.15, st(6) - 0.15,
      '<div style="text-align:center"><span class="kick">2 · <b>TRANSCRIPTION</b></span></div>'
      f'<div class="tlist">{chips}{euh}</div>')
R("#s2 .kick", st(4), {"opacity": 0, "y": -20}, {"opacity": 1, "y": 0}, 0.25)
for i, w in enumerate(tw):
    R(f"#s2 .t{i}", w["s"], {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, 0.18, "back.out(2)")
for i, needle in enumerate(("euh", "euh", "euh")):
    t = wf(5, "euh", min(i, 1)) + (0.45 if i == 2 else 0)
    R(f"#s2 .e{i}", t, {"opacity": 0, "scale": 1.6}, {"opacity": 1, "scale": 1}, 0.2, "back.out(3)")
    EV.append([t, "sfx-pop.mp3", -20])

# ------------------------------------------------------------------ 3 segmentation: the room peels away, Tony becomes a sticker
scene("s3", st(6) - 0.15, st(7) - 0.12,
      '<div style="text-align:center"><span class="kick">3 · <b>SEGMENTATION</b></span></div>'
      '<div class="dhead" style="font-size:88px;padding-top:30px"><div class="p">' + chars("pixel par pixel,") + '</div><div><span class="hl h">' + chars("comme un sticker.") + '</span></div></div>')
R("#s3 .kick", st(6), {"opacity": 0, "y": -20}, {"opacity": 1, "y": 0}, 0.25)
S("#basew", st(6) - 0.05, {"opacity": 1})
tcut = wf(6, "découpe")
R("#basew", tcut, {"clipPath": "inset(0px 0px 0px 0px)"}, {"clipPath": "inset(0px 0px 1440px 0px)"}, 0.9, "power1.inOut")
S("#basew", tcut + 0.95, {"opacity": 0})
EV.append([tcut, "sfx-zoom.mp3", -19])
kin("#s3 .p", wf(6, "pixel"), 0.02)
kin("#s3 .h", wf(6, "comme"), 0.03)
hl("#s3 .h", wf(6, "sticker"))
tst = wf(6, "sticker")
R("#tony", tst, {"rotation": 0, "filter": "drop-shadow(0px 0px 0px #fff)"},
  {"rotation": -4, "filter": "drop-shadow(6px 0px 0px #fff) drop-shadow(-6px 0px 0px #fff) drop-shadow(0px 6px 0px #fff) drop-shadow(0px -6px 0px #fff)"}, 0.25, "back.out(2)")
R("#tony", st(7) + 0.1, {"rotation": -4}, {"rotation": 0, "filter": "drop-shadow(0px 0px 0px #fff)"}, 0.25)
EV.append([tst, "sfx-web-latch.mp3", -17])

# ------------------------------------------------------------------ 4 IA: n'importe où -> plage, lune, Teams ; Tony: « Non. Pas Teams. »
scene("s4", st(7) - 0.12, st(9) - 0.15,
      '<div style="text-align:center"><span class="chip w0">À la plage</span> <span class="chip w1">Sur la lune</span> <span class="chip w2">En réunion Teams</span></div>')
for i, (needle, wid) in enumerate((("plage", "#w-beach"), ("lune", "#w-moon"), ("teams", "#w-teams"))):
    t = wf(7, needle)
    pop(f"#s4 .w{i}", t)
    R(wid, t - 0.05, {"opacity": 0}, {"opacity": 1}, 0.12)
    if i < 2:
        S(wid, wf(7, ("lune", "teams")[i]) - 0.05, {"opacity": 0})
    flash(t - 0.05, 0.3, 0.15, "#ffffff")
    EV.append([t, "sfx-whoosh-v2.mp3", -19])
tno = wf(8, "pas")
S("#w-teams", tno + 0.25, {"opacity": 0})
OV.append(f'<div class="stamp" id="st-teams" style="left:170px;top:1000px">PAS TEAMS.</div>')
stamp("#st-teams", tno)
R("#st-teams", en(8) + 0.35, {"opacity": 1}, {"opacity": 0}, 0.2)
EV.append([tno, "sfx-landing-thud.mp3", -15])
flash(tno + 0.25, 0.4, 0.2, "#ff6b6b")

# ------------------------------------------------------------------ 5 code: cuts, captions, animations
scene("s5", st(9) - 0.15, st(10) - 0.15,
      '<div style="text-align:center"><span class="kick">4 · <b>TOUT DEVIENT DU CODE</b></span></div>'
      '<div class="win"><div class="bar"><i class="d1"></i><i class="d2"></i><i class="d3"></i><span>montage.js</span></div><div class="code">'
      '<div class="ln l0"><span class="k">cut</span>(<span class="s">"silences"</span>)</div>'
      '<div class="ln l1"><span class="k">captions</span>(<span class="s">"mot à mot"</span>)</div>'
      '<div class="ln l2"><span class="k">animate</span>(<span class="s">"motion"</span>)</div>'
      '<div class="ln l3 m">// 0 timeline à la main</div></div></div>')
R("#s5 .kick", st(9), {"opacity": 0, "y": -20}, {"opacity": 1, "y": 0}, 0.25)
up("#s5 .win", wf(9, "code") - 0.1, 0.3, 40)
for i, needle in enumerate(("coupes", "sous", "animations")):
    t = wf(9, needle)
    R(f"#s5 .l{i}", t, {"clipPath": "inset(0px 100% 0px 0px)"}, {"clipPath": "inset(0px 0% 0px 0px)"}, 0.35, "none")
    EV.append([t, "sfx-click-soft.mp3", -20])
R("#s5 .l3", wf(9, "animations") + 0.4, {"clipPath": "inset(0px 100% 0px 0px)"}, {"clipPath": "inset(0px 0% 0px 0px)"}, 0.35, "none")
S("#s5 .ln", 0, {"clipPath": "inset(0px 100% 0px 0px)"})

# ------------------------------------------------------------------ 6 « tu sers à quoi ? » - « j'ai les idées » - « parfois »
scene("s6", st(10) - 0.15, st(13) - 0.15,
      '<div class="dhead q" style="font-size:96px"><div class="p">' + chars("Et toi, tu sers") + '</div><div><span class="hl h">' + chars("à quoi ?") + '</span></div></div>'
      f'<div class="lcard idea" style="margin-top:20px"><i class="bulb">{icon("bulb", 110)}</i><div class="t1">' + chars("J'ai les idées.") + '</div></div>')
kin("#s6 .p", st(10), 0.02)
kin("#s6 .h", wf(10, "quoi"), 0.04)
hl("#s6 .h", wf(10, "quoi") + 0.1)
R("#s6 .q", st(11) - 0.1, {"opacity": 1}, {"opacity": 0.25}, 0.2)
up("#s6 .lcard", st(11), 0.3, 40)
kin("#s6 .t1", wf(11, "idées") - 0.2, 0.025)
tpar = st(12)
OV.append(sticker("st-parfois", "PARFOIS", ".", "violet", None, "spark", left=300, top=820))
fb(f'sticker(tl,"#st-parfois",{q(tpar)},{q(st(13) - 0.2)},-6)')
for k_, (o_, t_) in enumerate([(0.2, 0), (1, 0.08), (0.15, 0.16), (0.15, 0.3)]):
    S("#s6 .bulb", tpar + t_, {"opacity": o_})
S("#s6 .bulb", tpar + 0.3, {"filter": "drop-shadow(0 0 0px rgba(0,0,0,0))", "color": "#55536a", "opacity": 1})
EV += [[tpar, "sfx-glitch-soft.mp3", -18], [tpar + 0.05, "sfx-thwip.mp3", -20]]

# ------------------------------------------------------------------ 7 CTA: pilule bleue / pilule rouge, commente BOOST (+ IA: prends la rouge)
scene("s7", st(13) - 0.15, TOTAL,
      '<div class="dhead" style="font-size:84px;padding-top:10px"><div class="p">' + chars("Tu n'as plus besoin") + '</div><div><span class="hl h">' + chars("de savoir monter.") + '</span></div></div>'
      '<div class="pills"><div class="pill blue"><small>PILULE BLEUE</small><b>tu continues à la main</b></div>'
      '<div class="pill red"><small>PILULE ROUGE</small><b>commente BOOST</b></div></div>'
      f'<div class="cfield"><span class="pre">commente</span><span class="kw">' + chars("BOOST") + f'</span><i class="snd">{icon("send", 40)}</i></div>')
kin("#s7 .p", st(13), 0.02)
kin("#s7 .h", wf(13, "savoir"), 0.03)
hl("#s7 .h", wf(13, "monter"))
R("#s7 .blue", wf(13, "bleue"), {"opacity": 0, "x": -80}, {"opacity": 1, "x": 0}, 0.3, "back.out(1.8)")
R("#s7 .blue", wf(13, "rouge") - 0.1, {"opacity": 1}, {"opacity": 0.35}, 0.25)
R("#s7 .red", wf(13, "rouge"), {"opacity": 0, "x": 80}, {"opacity": 1, "x": 0}, 0.3, "back.out(1.8)")
EV += [[wf(13, "bleue"), "sfx-pop.mp3", -20], [wf(13, "rouge"), "sfx-pop.mp3", -19]]
tk = wf(13, "boost")
up("#s7 .cfield", tk - 0.4, 0.25, 30)
fb(f'type(tl,"#s7 .kw",{q(tk)},0.07)')
pop("#s7 .snd", tk + 0.45)
EV += [[tk, "sfx-impact-deep.mp3", -16], [tk + 0.05, "sfx-click-soft.mp3", -20]]
for kk in range(6):                                   # IA: « prends la rouge » - the red pill pulses
    t = wf(14, "rouge") + kk * 0.35
    if t < TOTAL - 0.4:
        R("#s7 .red", t, {"scale": 1.08}, {"scale": 1}, 0.25, "power2.out")
EV.append([wf(14, "rouge"), "sfx-notify.mp3", -19])
S("#flash", TOTAL - 0.5, {"backgroundColor": "#0a0a0f"})
R("#flash", TOTAL - 0.5, {"opacity": 0}, {"opacity": 1}, 0.45, "power2.in")

# ------------------------------------------------------------------ captions: one pill, gold for Tony, violet for Tony IA
caps, cj, ci = [], [], 0
for n, it in enumerate(L):
    words = ws(n)
    chunks, cur = [], []
    for w in words:
        if cur and (len(" ".join(x["w"] for x in cur + [w])) > 20 or len(cur) >= 3 or w["s"] - cur[-1]["e"] > 0.35):
            chunks.append(cur); cur = []
        cur.append(w)
    chunks.append(cur)
    ia = it["who"] == "ia"
    nxt_line = L[n + 1]["start"] if n + 1 < len(L) else TOTAL
    for k2, ch in enumerate(chunks):
        a = ch[0]["s"] - 0.03
        b = chunks[k2 + 1][0]["s"] - 0.03 if k2 + 1 < len(chunks) else min(it["end"] + 0.2, nxt_line - 0.03)
        txt = " ".join(x["w"] for x in ch)
        width = int(len(txt) * 29 + 88 + (70 if ia else 0))
        caps.append(f'<div class="cap{" ia" if ia else ""}" id="c{ci}" style="width:{width}px">' + ('<span class="who">IA</span>' if ia else "")
                    + " ".join(f'<span class="cw" id="c{ci}w{j}">{html.escape(x["w"])}</span>' for j, x in enumerate(ch)) + "</div>")
        bc, sh = ("#8b5cf6", "0 0 26px rgba(139,92,246,.7)") if ia else ("#eab308", "0 0 26px rgba(234,179,8,.5)")
        cj.append(f'tl.set("#cap",{{width:{width},x:{540 - width / 2:.0f},opacity:1,borderColor:"{bc}",boxShadow:"{sh}"}},{q(max(0, a))});')
        cj.append(f'tl.fromTo("#c{ci}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.1,ease:"power2.out",immediateRender:false}},{q(max(0, a))});')
        cj.append(f'tl.set("#c{ci}",{{opacity:0}},{q(b)});')
        if k2 + 1 == len(chunks):
            cj.append(f'tl.set("#cap",{{opacity:0}},{q(b)});')
        for j, x in enumerate(ch):
            nx = min(ch[j + 1]["s"] if j + 1 < len(ch) else b, b)
            cj.append(f'tl.set("#c{ci}w{j}",{{color:"#eab308",textShadow:"0 0 16px rgba(234,179,8,.8)"}},{q(x["s"])});')
            cj.append(f'tl.set("#c{ci}w{j}",{{color:"{"#c4b5fd" if ia else "#EDEDED"}",textShadow:"0 0 0px rgba(234,179,8,0)"}},{q(nx)});')
        ci += 1
S("#cap", 0, {"y": 1720})

# ------------------------------------------------------------------ write
TPL = open(os.path.join(HERE, "template.html")).read()
out = (TPL.replace("%%TOTAL%%", str(TOTAL)).replace("%%SCENES%%", "\n".join(SC)).replace("%%CAPTIONS%%", "\n".join(caps))
       .replace("%%OVERLAYS%%", "\n".join(OV)).replace("%%JS%%", "\n".join(js + cj)))
pub = os.path.join(HERE, "public")
os.makedirs(os.path.join(pub, "kit"), exist_ok=True)
for f in ("kit.css", "kit.js"):
    shutil.copy(os.path.join(KIT, f), os.path.join(pub, "kit", f))
for f in ("tony.webm", "tony_src.mp4", "avatar.mp4"):
    if os.path.exists(os.path.join(BUILD, f)):
        shutil.copy(os.path.join(BUILD, f), os.path.join(pub, f))
open(os.path.join(pub, "index.html"), "w").write(out)
json.dump(sorted(e for e in EV if 0 <= e[0] < TOTAL - 0.1), open(os.path.join(HERE, "events.json"), "w"))
print(f"index.html: {len(SC)} scènes, {ci} captions, {len(js)} animations, {TOTAL} s, {len(EV)} SFX")

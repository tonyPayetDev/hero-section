#!/usr/bin/env python3
"""autoboost-83 - « 10 outils GitHub » (remake of @baptsimard.ia's reel, Tony's style, Tony vs Tony IA).

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
TY, BASE = 1050, 1.0            # the take is 1080x870 (split-preuve face cam): bottom on the frame edge
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
IAX, IAY, IAS = 640, 1230, 0.5           # visual centre ~(890, 1500): on his shoulder, never over his face
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
    # Tony listens: dimmed (inner wrapper, so it never fights the sticker outline) and nudged left
    R("#tonyi", a - 0.1, {"filter": "brightness(1)", "x": 0}, {"filter": "brightness(.72)", "x": -70}, 0.25)
    R("#tonyi", b, {"filter": "brightness(.72)", "x": -70}, {"filter": "brightness(1)", "x": 0}, 0.25)


# ------------------------------------------------------------------ data: the 10 tools (line index, number, name, what it does)
TOOLS = [(2, "Humanizer", ["repère les tics IA", "corrige tes textes"], "feather"),
         (4, "HyperFrames", ["vidéo écrite comme une page web", "vrai fichier .mp4"], "rocket"),
         (5, "21st.dev", ["10 000+ éléments de site", "boutons · menus · en-têtes"], "gear"),
         (6, "Watch", ["un lien de vidéo", "ce qu'on voit + ce qui se dit"], "search"),
         (7, "REA", ["démonte une appli", "comprend comment elle marche"], "brain"),
         (9, "Apify", ["Instagram · LinkedIn", "Google Maps"], "bolt"),
         (10, "Google Workspace", ["Gmail · Drive", "Agenda · Sheets"], "doc"),
         (11, "Find Skills", ["tu dis ce que tu veux", "il trouve le skill"], "bulb"),
         (12, "Orca", ["Claude Code + Codex", "côte à côte"], "brain"),
         (14, "Playwright", ["vrai navigateur", "teste ton site"], "check")]

# ------------------------------------------------------------------ 0 hook: 100 testés -> 10 gardés (+ IA: « dont celui qui a monté cette vidéo »)
dots = "".join(f'<i class="dot d{i}"></i>' for i in range(100))
scene("s0", 0, st(2) - 0.15,
      '<div class="dhead"><div class="p">' + chars("100 outils GitHub") + '</div><div><span class="hl h">' + chars("j'en garde 10.") + '</span></div></div>'
      f'<div class="dots">{dots}</div>')
kin("#s0 .p", 0.0)
js.append(f'tl.fromTo("#s0 .dot",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:.25,ease:"back.out(2)",stagger:{{each:.008,from:"random"}},immediateRender:false}},{q(wf(0, "centaine"))});')
kin("#s0 .h", wf(0, "garde"), 0.03)
hl("#s0 .h", wf(0, "garde") + 0.1)
keep = [3, 17, 24, 38, 45, 52, 66, 71, 83, 96]
for i in range(100):
    if i not in keep:
        R(f"#s0 .d{i}", wf(0, "dix"), {"opacity": 1}, {"opacity": 0.12}, 0.3)
for n, i in enumerate(keep):
    R(f"#s0 .d{i}", wf(0, "dix") + n * 0.03, {"scale": 1, "backgroundColor": "#3a3550"}, {"scale": 1.6, "backgroundColor": "#eab308"}, 0.25, "back.out(3)")
EV += [[wf(0, "centaine"), "sfx-whoosh-v2.mp3", -21], [wf(0, "dix"), "sfx-impact.mp3", -17]]
OV.append(sticker("st-rien", "DE", "RIEN.", "violet", None, "spark", left=80, top=720))
fb(f'sticker(tl,"#st-rien",{q(wf(1, "rien"))},{q(en(1) + 0.15)},-6)')
EV.append([wf(1, "rien"), "sfx-thwip.mp3", -21])

# ------------------------------------------------------------------ 1-10: one neon card per tool, its number pinned on « Un : », « Deux : »…
for n, (li, name, lines2, ico) in enumerate(TOOLS):
    sid = f"t{n}"
    nxt = TOOLS[n + 1][0] if n + 1 < len(TOOLS) else 15
    b = st(nxt) - 0.15
    scene(sid, st(li) - 0.15, b,
          f'<div class="tool"><div class="num">{n + 1:02d}<small>/10</small></div><div class="nm"><i>{icon(ico, 64)}</i><span>' + chars(name) + '</span></div>'
          + "".join(f'<div class="ln l{k}"><b></b>{html.escape(t)}</div>' for k, t in enumerate(lines2)) + '</div>'
          + f'<div class="prog">' + "".join(f'<i class="{"on" if k <= n else ""}"></i>' for k in range(10)) + '</div>')
    pop(f"#{sid} .num", st(li))
    kin(f"#{sid} .nm span", st(li) + 0.15, 0.025)
    pop(f"#{sid} .nm i", st(li) + 0.15)
    words = ws(li)
    for k in range(len(lines2)):
        t = words[min(len(words) - 1, int(len(words) * (0.35 + 0.3 * k)))]["s"]
        R(f"#{sid} .l{k}", t, {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0}, 0.3, "back.out(1.8)")
        EV.append([t, "sfx-click.mp3", -22])
    EV.append([st(li), "sfx-pop.mp3", -19])

# IA lines: stickers on the joint
for li, a_, b_, v in [(3, "JE ME SENS", "VISÉ.", "red"), (8, "JE REMONTE", "TOUT.", "violet"), (13, "ENFIN UN", "COLLÈGUE.", "gold")]:
    OV.append(sticker(f"st{li}", a_, b_, v, None, "spark", left=70, top=720))
    fb(f'sticker(tl,"#st{li}",{q(st(li) + 0.1)},{q(en(li) + 0.3)},-6)')
    EV.append([st(li) + 0.1, "sfx-thwip.mp3", -21])

# ------------------------------------------------------------------ CTA: commente GITHUB
scene("s9", st(15) - 0.15, TOTAL,
      '<div class="dhead" style="font-size:96px"><div class="p">' + chars("Les 10 liens") + '</div><div><span class="hl h">' + chars("+ le prompt.") + '</span></div></div>'
      f'<div class="cfield"><span class="pre">commente</span><span class="kw">' + chars("GITHUB") + f'</span><i class="snd">{icon("send", 40)}</i></div>')
kin("#s9 .p", st(15), 0.02)
kin("#s9 .h", wf(15, "liens"), 0.03)
hl("#s9 .h", wf(15, "prompt"))
tk = wf(15, "github")
up("#s9 .cfield", tk - 0.4, 0.25, 30)
fb(f'type(tl,"#s9 .kw",{q(tk)},0.07)')
pop("#s9 .snd", tk + 0.45)
EV += [[tk, "sfx-impact-deep.mp3", -16], [tk + 0.05, "sfx-click-soft.mp3", -20]]
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
        cj.append(f'tl.fromTo("#c{ci}",{{opacity:0.5,y:6}},{{opacity:1,y:0,duration:.06,ease:"power2.out",immediateRender:false}},{q(max(0, a))});')
        cj.append(f'tl.set("#c{ci}",{{opacity:0}},{q(b)});')
        if k2 + 1 == len(chunks):
            cj.append(f'tl.set("#cap",{{opacity:0}},{q(b)});')
        for j, x in enumerate(ch):
            nx = min(ch[j + 1]["s"] if j + 1 < len(ch) else b, b)
            cj.append(f'tl.set("#c{ci}w{j}",{{color:"#eab308",textShadow:"0 0 16px rgba(234,179,8,.8)"}},{q(x["s"])});')
            cj.append(f'tl.set("#c{ci}w{j}",{{color:"{"#c4b5fd" if ia else "#EDEDED"}",textShadow:"0 0 0px rgba(234,179,8,0)"}},{q(nx)});')
        ci += 1
S("#cap", 0, {"y": 960})

# ------------------------------------------------------------------ write
TPL = open(os.path.join(HERE, "template.html")).read()
out = (TPL.replace("%%TOTAL%%", str(TOTAL)).replace("%%SCENES%%", "\n".join(SC)).replace("%%CAPTIONS%%", "\n".join(caps))
       .replace("%%OVERLAYS%%", "\n".join(OV)).replace("%%JS%%", "\n".join(js + cj)))
pub = os.path.join(HERE, "public")
os.makedirs(os.path.join(pub, "kit"), exist_ok=True)
for f in ("kit.css", "kit.js"):
    shutil.copy(os.path.join(KIT, f), os.path.join(pub, "kit", f))
for f in ("tony.webm", "tony_src.mp4", "avatar.mp4"):  # built by build.py + resync.py
    if os.path.exists(os.path.join(BUILD, f)):
        shutil.copy(os.path.join(BUILD, f), os.path.join(pub, f))
open(os.path.join(pub, "index.html"), "w").write(out)
json.dump(sorted(e for e in EV if 0 <= e[0] < TOTAL - 0.1), open(os.path.join(HERE, "events.json"), "w"))
print(f"index.html: {len(SC)} scènes, {ci} captions, {len(js)} animations, {TOTAL} s, {len(EV)} SFX")

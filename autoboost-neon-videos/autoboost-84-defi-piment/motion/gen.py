#!/usr/bin/env python3
"""autoboost-84 - « Défi piment » : HyperFrames composition over Tony's cut take (kit « Piment Power »).

  BUILD=path/to/build python3 motion/gen.py      -> motion/public/index.html + motion/events.json (SFX for the mix)

Full-frame take with a punch-in on every cut, hook title, chili meter that climbs with the bites, kit stickers
on the reactions, Tony IA in the chili ring when he speaks, word-by-word captions (orange Tony / violet IA),
like + subscribe on his own call to action.
"""
import html, json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "public")
BUILD = os.environ.get("BUILD", os.path.join(HERE, "..", "build"))
VO = json.load(open(os.path.join(BUILD, "vo.json")))
TOTAL, L, CUTS = VO["total"], VO["lines"], VO["cuts"]
# caption wording: what he says, spelled right (Whisper's slips on his take)
FIX = {"au moitié": "la moitié", "comment je coulais": "commence à couler", "j'y": "", "lui,": "", "donc likez,": "likez,"}

js, EV, OV = [], [], []


def q(t):
    return f"{max(0.0, t):.3f}"


def R(sel, t, frm, to, d=0.3, ease="power3.out"):
    if to.get("opacity") == 0 or (frm.get("opacity", 1) > 0 and "opacity" in frm and to.get("opacity", 1) < frm["opacity"]):
        # a fade-out: tween to the end state only (a cold seek never needs the from-vars to reveal it)
        js.append(f'tl.to("{sel}",{{...{json.dumps(to)},duration:{d},ease:"{ease}"}},{q(t)});')
        return
    js.append(f'tl.fromTo("{sel}",{json.dumps(frm)},{{...{json.dumps(to)},duration:{d},ease:"{ease}",immediateRender:false}},{q(t)});')


def S(sel, t, props):
    js.append(f'tl.set("{sel}",{json.dumps(props)},{q(t)});')


def line(i):
    return L[i]


def wt(i, needle):
    """start time of the first word of line i containing needle"""
    for w in L[i]["words"]:
        if needle.lower() in w["w"].lower():
            return w["s"]
    raise KeyError(f"{needle!r} not in line {i}: {L[i]['text']}")


# ------------------------------------------------------------------ take: punch-in on every cut, slow push between
S("#camw", 0, {"scale": 1.0})
z = 1.0
for c in CUTS[1:]:
    z = 1.07 if z == 1.0 else 1.0
    S("#camw", c, {"scale": z})

# ------------------------------------------------------------------ hook (line 0 « Bon on va tester ça »)
hook_end = L[1]["start"] + 0.6
S("#tsh", 0, {"opacity": 1})
R("#hook .k", 0.05, {"opacity": 0, "y": -30}, {"opacity": 1, "y": 0}, 0.3, "back.out(2)")
title = "NOUILLES<br>AU PIMENT"
spans = "".join(f"<span>{c}</span>" if c not in " " else " " for c in "NOUILLES") + "<br>" + "".join(f"<span>{c}</span>" if c != " " else " " for c in "AU PIMENT")
js.append(f'tl.fromTo("#hook .t span",{{opacity:0,y:60,scale:1.6}},{{opacity:1,y:0,scale:1,duration:.32,ease:"back.out(2.2)",stagger:.035,immediateRender:false}},0.15);')
R("#hook .s", 0.75, {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, 0.3)
R("#fl1", 0.1, {"opacity": 0, "y": 120}, {"opacity": 0.95, "y": 0}, 0.4)
R("#heat", 0.1, {"opacity": 0}, {"opacity": 1}, 0.4)
R("#hook", hook_end, {"opacity": 1, "y": 0}, {"opacity": 0, "y": -80}, 0.3, "power2.in")
R("#fl1", hook_end, {"opacity": 0.95}, {"opacity": 0}, 0.4)
R("#heat", hook_end, {"opacity": 1}, {"opacity": 0}, 0.4)
R("#tsh", hook_end + 0.1, {"opacity": 1}, {"opacity": 0.6}, 0.4)
R("#flash", 0.08, {"opacity": 0.5}, {"opacity": 0}, 0.25, "power2.out")
EV += [[0.0, "sfx-impact-deep.mp3", -15], [0.15, "sfx-whoosh-v2.mp3", -20]]

# ------------------------------------------------------------------ chili meter: shows up at the first bite, one chili per reaction
lv_steps = [(wt(10, "parti"), 1), (wt(11, "pique"), 2), (wt(13, "goût"), 3), (wt(14, "nez"), 4), (wt(16, "sensation"), 5)]
R("#meter", lv_steps[0][0] - 0.3, {"opacity": 0, "y": -40}, {"opacity": 1, "y": 0}, 0.35, "back.out(2)")
for t, n in lv_steps:
    js.append(f'tl.set("#p{n}",{{className:"p on"}},{q(t)});')
    js.append(f'tl.fromTo("#p{n}",{{scale:1.8}},{{scale:1,duration:.35,ease:"back.out(3)",immediateRender:false}},{q(t)});')
    js.append(f'tl.set("#lv",{{textContent:"{n}/5"}},{q(t)});')
    R("#heat", t, {"opacity": 0.25 + 0.12 * n}, {"opacity": 0.12 * n}, 0.8, "power2.out")
    EV.append([t, "sfx-impact.mp3", -19])
R("#meter", L[-1]["start"] - 0.2, {"opacity": 1}, {"opacity": 0}, 0.3)          # the outro card takes the top

# ------------------------------------------------------------------ kit stickers on the reactions (black matte, screen blend)
STICK = [("regarde-ca", wt(1, "knakis"), 2.0, 40, 1150, -6),
         ("ca-choque", wt(6, "horreur"), 2.0, 480, 1150, 5),
         ("trop-fort", wt(10, "fort"), 2.0, 40, 1150, -5),
         ("hyper-fort-piment", wt(11, "pique"), 2.4, 480, 1140, 4),
         ("ca-monte", wt(14, "nez"), 2.2, 40, 1150, -4)]
for k, (name, t, d, x, y, rot) in enumerate(STICK):
    OV.append(f'<img class="st" id="st{k}" src="piment/{name}.png" alt="" style="left:{x}px;top:{y}px" />')
    js.append(f'tl.fromTo("#st{k}",{{opacity:0,scale:2.2,rotation:{rot * 3}}},{{opacity:1,scale:1,rotation:{rot},duration:.28,ease:"back.out(2.4)",immediateRender:false}},{q(t)});')
    js.append(f'tl.to("#st{k}",{{opacity:0,scale:.85,duration:.2,ease:"power2.in"}},{q(t + d)});')
    EV.append([t, "sfx-thwip.mp3", -18])

# ------------------------------------------------------------------ Tony IA: chili ring top-right, pops in on each line, Tony's take dims
IAX, IAY = 650, 880            # visual ring ~(720-1060, 900-1300): beside his shoulder, above the captions
S("#iaw", 0, {"x": IAX, "y": IAY, "opacity": 0, "scale": 0.9})
for n, it in enumerate(x for x in L if x["who"] == "ia"):
    a, b = it["start"], it["end"]
    if n == 0:
        for k, (dx, op) in enumerate([(40, 1), (-60, .4), (24, 1), (-10, .7), (0, 1)]):
            S("#iaw", a - 0.2 + k * 0.04, {"x": IAX + dx, "opacity": op, "scale": 1, "skewX": [-10, 7, -4, 2, 0][k]})
        EV.append([a - 0.2, "sfx-glitch-hard.mp3", -16])
    else:
        R("#iaw", a - 0.22, {"opacity": 0, "x": 1100, "scale": 1}, {"opacity": 1, "x": IAX, "scale": 1}, 0.28, "back.out(1.6)")
        EV.append([a - 0.22, "sfx-glitch-soft.mp3", -18])
    R("#iaw", b + 0.15, {"opacity": 1, "x": IAX}, {"opacity": 0, "x": 1100}, 0.24, "power2.in")
    R("#camw", a - 0.15, {"filter": "brightness(1) saturate(1)"}, {"filter": "brightness(.7) saturate(.8)"}, 0.25)
    R("#camw", b + 0.1, {"filter": "brightness(.7) saturate(.8)"}, {"filter": "brightness(1) saturate(1)"}, 0.25)

# ------------------------------------------------------------------ CTA on « likez, abonnez-vous »
cta_i = next(i for i, x in enumerate(L) if x.get("tag") == "cta")
t_like, t_sub = wt(cta_i, "likez"), wt(cta_i, "abonnez")
R("#cta", t_like - 0.05, {"opacity": 0, "y": 40}, {"opacity": 1, "y": 0}, 0.3, "back.out(2)")
js.append(f'tl.fromTo("#cta .like",{{scale:1.5}},{{scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{q(t_like)});')
js.append(f'tl.fromTo("#cta .sub",{{scale:1.6,opacity:.3}},{{scale:1,opacity:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{q(t_sub)});')
js.append(f'tl.to("#cta .sub",{{scale:1.06,duration:.35,yoyo:true,repeat:5,ease:"sine.inOut"}},{q(t_sub + 0.4)});')
R("#cta", L[cta_i]["end"] + 0.4, {"opacity": 1}, {"opacity": 0}, 0.3)
EV += [[t_like, "sfx-pop.mp3", -17], [t_sub, "sfx-confirm.mp3", -17]]
S("#flash", TOTAL - 0.5, {"backgroundColor": "#050305"})
R("#flash", TOTAL - 0.5, {"opacity": 0}, {"opacity": 1}, 0.45, "power2.in")

# ------------------------------------------------------------------ outro: « montée entièrement avec Claude » + commente MONTAGE (last IA line)
KW = "MONTAGE"
oi = len(L) - 1
assert L[oi]["who"] == "ia" and "MONTAGE" in L[oi]["text"], "the outro must be the last line"
oa, ob = L[oi]["start"], L[oi]["end"]
R("#outro", oa - 0.1, {"opacity": 0, "y": -60, "scale": 0.92}, {"opacity": 1, "y": 0, "scale": 1}, 0.4, "back.out(1.8)")
EV.append([oa - 0.1, "sfx-whoosh-v2.mp3", -19])
tk = wt(oi, "Commente")
R("#outro .f", tk - 0.2, {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, 0.3, "back.out(2)")
for k, ch in enumerate(KW):
    js.append(f'tl.set("#outro .kw span:nth-child({k + 1})",{{opacity:1}},{q(tk + 0.25 + k * 0.07)});')
    EV.append([tk + 0.25 + k * 0.07, "sfx-click-soft.mp3", -24])
js.append(f'tl.fromTo("#outro .f svg",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.3,ease:"back.out(3)",immediateRender:false}},{q(tk + 0.3 + len(KW) * 0.07)});')
R("#outro .d", wt(oi, "envoie") - 0.1, {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, 0.3)
EV += [[tk, "sfx-impact-deep.mp3", -16], [wt(oi, "envoie"), "sfx-notify.mp3", -19]]

# ------------------------------------------------------------------ captions: chunks of <= 3 words, active word yellow
caps, ci = [], 0
for n, it in enumerate(L):
    words = []
    for w in it["words"]:
        words.append(dict(w))
    txt_all = " ".join(w["w"] for w in words)
    for bad, good in FIX.items():                       # simple word-level fixes, keep the timings
        if bad.strip(",") in txt_all.lower():
            bt = bad.split()
            for j in range(len(words) - len(bt) + 1):
                if [w["w"].strip(",.!?").lower() for w in words[j:j + len(bt)]] == [x.strip(",.!?").lower() for x in bt]:
                    gt = good.split() if good else []
                    for k2 in range(len(bt)):
                        words[j + k2]["w"] = gt[k2] if k2 < len(gt) else ""
                    if len(gt) > len(bt):
                        words[j + len(bt) - 1]["w"] += " " + " ".join(gt[len(bt):])
            words = [w for w in words if w["w"]]
    chunks, cur = [], []
    for w in words:
        if cur and (len(" ".join(x["w"] for x in cur + [w])) > 18 or len(cur) >= 3 or w["s"] - cur[-1]["e"] > 0.35):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    ia = it["who"] == "ia"
    nxt = L[n + 1]["start"] if n + 1 < len(L) else TOTAL
    for k2, ch in enumerate(chunks):
        a = ch[0]["s"] - 0.03
        b = chunks[k2 + 1][0]["s"] - 0.03 if k2 + 1 < len(chunks) else min(it["end"] + 0.25, nxt - 0.03)
        caps.append(f'<div class="cap{" ia" if ia else ""}" id="c{ci}">' + ('<span class="who">IA</span>' if ia else "")
                    + " ".join(f'<span class="cw" id="c{ci}w{j}">{html.escape(x["w"])}</span>' for j, x in enumerate(ch)) + "</div>")
        js.append(f'tl.fromTo("#c{ci}",{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.08,ease:"power2.out",immediateRender:false}},{q(a)});')
        js.append(f'tl.set("#c{ci}",{{opacity:0}},{q(b)});')
        for j, x in enumerate(ch):
            nx = min(ch[j + 1]["s"] if j + 1 < len(ch) else b, b)
            js.append(f'tl.set("#c{ci}w{j}",{{color:"#FFD600",textShadow:"0 0 18px rgba(255,138,0,.9)"}},{q(x["s"])});')
            js.append(f'tl.set("#c{ci}w{j}",{{color:"{"#d8b4fe" if ia else "#ffffff"}",textShadow:"0 0 0px rgba(0,0,0,0)"}},{q(nx)});')
        ci += 1

# ------------------------------------------------------------------ write
tpl = open(os.path.join(HERE, "template.html")).read()
page = (tpl.replace("%%TOTAL%%", q(TOTAL)).replace("%%HOOK%%", spans).replace("%%KW%%", "".join(f"<span>{c}</span>" for c in KW)).replace("%%OVERLAYS%%", "\n".join(OV))
        .replace("%%CAPTIONS%%", "\n".join(caps)).replace("%%JS%%", "\n".join("    " + x for x in js)))
open(os.path.join(PUB, "index.html"), "w").write(page)
json.dump(sorted(EV), open(os.path.join(HERE, "events.json"), "w"))
for f in ("base.mp4", "avatar.mp4"):
    shutil.copy(os.path.join(BUILD, f), os.path.join(PUB, f))
print(f"index.html: {ci} captions, {len(js)} animations, {TOTAL} s, {len(EV)} SFX")

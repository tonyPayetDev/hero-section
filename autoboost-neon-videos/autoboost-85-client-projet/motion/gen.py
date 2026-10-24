#!/usr/bin/env python3
"""autoboost-85 - « Quand le client décrit son projet » : HyperFrames over Tony's lip-sync take (kit « Piment Power »).

  BUILD=path/to/build python3 motion/gen.py      -> motion/public/index.html + motion/events.json (SFX for the mix)

Full-frame lip-sync take (never cut, Tony IA on freeze frames), hook title « quand le client décrit son projet », kit stickers
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
FIX = {}                                    # captions are hand-corrected in session/edit.json

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
T_IN = 1.0                                         # Tony's « LE CLIENT / LE FREELANCE » frame first, then the desert
hook_end = L[2]["start"] + 0.2                     # over « Convoque… fais creuser les fondations »
S("#tsh", T_IN, {"opacity": 1})
R("#hook .k", T_IN + 0.05, {"opacity": 0, "y": -30}, {"opacity": 1, "y": 0}, 0.3, "back.out(2)")
HOOK = json.load(open(os.path.join(HERE, "..", "session", "edit.json")))["hook"]
spans = "<br>".join("".join(f"<span>{c}</span>" if c != " " else " " for c in row) for row in HOOK)
js.append(f'tl.fromTo("#hook .t span",{{opacity:0,y:60,scale:1.6}},{{opacity:1,y:0,scale:1,duration:.32,ease:"back.out(2.2)",stagger:.035,immediateRender:false}},{q(T_IN + 0.15)});')
R("#hook .s", T_IN + 0.75, {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, 0.3)
R("#heat", T_IN + 0.1, {"opacity": 0}, {"opacity": 1}, 0.4)
R("#hook", hook_end, {"opacity": 1, "y": 0}, {"opacity": 0, "y": -80}, 0.3, "power2.in")
R("#heat", hook_end, {"opacity": 1}, {"opacity": 0}, 0.4)
R("#tsh", hook_end + 0.1, {"opacity": 1}, {"opacity": 0.6}, 0.4)
js.append('tl.fromTo("#intro",{scale:1.0},{scale:1.06,duration:1.0,ease:"none",immediateRender:false},0);')
EV += [[0.0, "sfx-impact-deep.mp3", -15], [T_IN + 0.15, "sfx-whoosh-v2.mp3", -20]]

# ------------------------------------------------------------------ Sahara set: Tony cut out, the decor follows his words
R("#intro", T_IN, {"opacity": 1}, {"opacity": 0}, 0.12)                # flash « teleports » the client to his desert
# who is who: the client is Tony, the freelance is his IA
R("#lbl-client", T_IN + 0.4, {"opacity": 0, "scale": 0.6}, {"opacity": 1, "scale": 1}, 0.3, "back.out(2.4)")
R("#lbl-client", L[2]["start"] + 0.5, {"opacity": 1}, {"opacity": 0}, 0.25)
R("#flash", T_IN - 0.02, {"opacity": 0.9}, {"opacity": 0}, 0.35, "power2.out")
EV.append([T_IN - 0.05, "sfx-whoosh-v2.mp3", -17])
DEC = [("#dc1", T_IN), ("#dc2", wt(2, "palmier") - 0.15), ("#dc3", wt(6, "palais") - 0.15), ("#dc4", wt(8, "danseuses") - 0.25)]
for k, (sel, t0) in enumerate(DEC):
    t1 = DEC[k + 1][1] if k + 1 < len(DEC) else TOTAL
    R(sel, t0, {"opacity": 0, "scale": 1.0}, {"opacity": 1, "scale": 1.0}, 0.35 if k else 0.01, "power2.out")
    js.append(f'tl.fromTo("{sel}",{{scale:1}},{{scale:1.08,duration:{t1 - t0:.3f},ease:"none",immediateRender:false}},{q(t0)});')
    if k + 1 < len(DEC):
        R(sel, t1 + 0.3, {"opacity": 1}, {"opacity": 0}, 0.05)
    if k:
        EV.append([t0, "sfx-whoosh-lat.mp3", -20])
# « une grande allée avec plein de statues » : two pharaohs; « oliviers, orangers, saules pleureurs » : the trees
ts = wt(2, "statues")
for k, sel in enumerate(("#stat1", "#stat2")):
    R(sel, ts + 0.12 * k, {"opacity": 0, "y": 260, "scale": 0.85}, {"opacity": 1, "y": 0, "scale": 1}, 0.45, "back.out(1.6)")
    R(sel, wt(4, "oliviers") - 0.2, {"opacity": 1}, {"opacity": 0}, 0.3)
EV += [[ts, "sfx-landing-thud.mp3", -17]]
for sel, word, li in (("#olive", "oliviers", 4), ("#orange", "orangers", 4), ("#willow", "saules", 5)):
    t = wt(li, word)
    R(sel, t, {"opacity": 0, "scale": 0.3, "y": 200}, {"opacity": 1, "scale": 1, "y": 0}, 0.45, "back.out(1.8)")
    R(sel, DEC[2][1], {"opacity": 1}, {"opacity": 0}, 0.3)
    EV.append([t, "sfx-pop.mp3", -19])
# « Et là-bas, le palais » : the fortress rises behind him, leaves when the camp comes
tp = wt(6, "palais")
R("#palace", tp, {"opacity": 0, "y": 420, "scale": 0.8}, {"opacity": 1, "y": 0, "scale": 1}, 0.7, "back.out(1.4)")
R("#palace", DEC[3][1], {"opacity": 1}, {"opacity": 0}, 0.4)
EV += [[tp, "sfx-landing-thud.mp3", -15], [tp + 0.1, "sfx-debris.mp3", -22]]
# « plein de danseuses qui pourront danser » : three dancers, a slow sway each
td = wt(8, "danseuses")
for k, (sel, dt, rot) in enumerate([("#dz1", 0.0, -6), ("#dz2", 0.18, 6), ("#dz3", 0.36, -4)]):
    R(sel, td + dt, {"opacity": 0, "y": 160, "scale": 0.7}, {"opacity": 1, "y": 0, "scale": 1}, 0.45, "back.out(1.8)")
    js.append(f'tl.fromTo("{sel}",{{rotation:{-rot}}},{{rotation:{rot},duration:.55,ease:"sine.inOut",yoyo:true,repeat:{int((TOTAL - td) / 0.55)},immediateRender:false}},{q(td + dt + 0.45)});')
    EV.append([td + dt, "sfx-pop.mp3", -20])
# « Et juste là, un petit géranium » : tiny, in front, bounce
tg = wt(9, "géranium")
R("#geranium", tg, {"opacity": 0, "scale": 0, "rotation": -20}, {"opacity": 1, "scale": 1, "rotation": 0}, 0.5, "back.out(3)")
EV += [[tg, "sfx-pop.mp3", -16], [tg + 0.15, "sfx-chime-v2.mp3", -21]]

# ------------------------------------------------------------------ kit stickers on the reactions (black matte, screen blend)
STICK = [("ca-monte", wt(3, "appellera"), 2.0, 40, 1150, -6)]          # the scope creeps already
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

S("#flash", TOTAL - 0.5, {"backgroundColor": "#050305"})
R("#flash", TOTAL - 0.5, {"opacity": 0}, {"opacity": 1}, 0.45, "power2.in")

# ------------------------------------------------------------------ « j'imagine surtout le devis » : the quote climbs to 250 000 €
ia = [i for i, x in enumerate(L) if x["who"] == "ia"]
dv = L[ia[0]]
R("#devis", dv["start"] - 0.1, {"opacity": 0, "y": -60, "scale": 0.9}, {"opacity": 1, "y": 0, "scale": 1}, 0.3, "back.out(2)")
steps = 24                                             # the count, frame by frame (a seek-safe set per step, ease-in like a bill that runs away)
for k in range(steps + 1):
    v = round(250000 * (k / steps) ** 2.2 / 1000) * 1000
    js.append(f'tl.set("#devis .n",{{textContent:"{v:,}".replace(",", " ")}},{q(dv["start"] + 0.1 + (dv["end"] - dv["start"] - 0.1) * k / steps)});')
js.append(f'tl.fromTo("#devis",{{rotation:0}},{{rotation:-3,duration:.06,yoyo:true,repeat:5,ease:"none",immediateRender:false}},{q(dv["end"])});')
R("#devis", dv["end"] + 0.6, {"opacity": 1}, {"opacity": 0}, 0.25)
EV += [[dv["end"], "sfx-confirm.mp3", -15], [dv["end"] + 0.05, "sfx-chime-v2.mp3", -17]]

# ------------------------------------------------------------------ « Dans un mois ? Maximum ! » : Tony's DEADLINE : HIER frame, the IA answers over it
tm = wt(len(L) - 3, "Maximum")
R("#payoff", tm - 0.05, {"opacity": 0, "scale": 1.25}, {"opacity": 1, "scale": 1}, 0.25, "power4.out")
js.append(f'tl.fromTo("#payoff",{{x:-14}},{{x:14,duration:.05,yoyo:true,repeat:7,ease:"none",immediateRender:false}},{q(tm + 0.2)});')
js.append(f'tl.set("#payoff",{{x:0}},{q(tm + 0.62)});')
js.append(f'tl.fromTo("#payoff",{{scale:1}},{{scale:1.06,duration:{L[ia[1]]["end"] - tm + 0.3:.2f},ease:"none",immediateRender:false}},{q(tm + 0.62)});')
R("#payoff", L[ia[2]]["start"] - 0.25, {"opacity": 1}, {"opacity": 0}, 0.2)
EV += [[tm, "sfx-impact-deep.mp3", -14], [tm + 0.2, "sfx-glass-break.mp3", -20]]

# ------------------------------------------------------------------ end card (3 s): « Montée avec Claude — Commente MONTAGE »
oi = ia[2]
assert "MONTAGE" in L[oi]["text"], "the last IA line is the end card"
R("#endcard", L[oi]["start"] - 0.25, {"opacity": 0, "scale": 1.1}, {"opacity": 1, "scale": 1}, 0.3, "power3.out")
js.append(f'tl.fromTo("#endcard",{{scale:1}},{{scale:1.05,duration:{TOTAL - L[oi]["start"]:.2f},ease:"none",immediateRender:false}},{q(L[oi]["start"] + 0.05)});')
S("#cap", L[oi]["start"] - 0.25, {"opacity": 0})
EV += [[L[oi]["start"] - 0.25, "sfx-whoosh-v2.mp3", -18], [wt(oi, "MONTAGE"), "sfx-notify.mp3", -17]]

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
page = (tpl.replace("%%TOTAL%%", q(TOTAL)).replace("%%HOOK%%", spans).replace("%%OVERLAYS%%", "\n".join(OV))
        .replace("%%CAPTIONS%%", "\n".join(caps)).replace("%%JS%%", "\n".join("    " + x for x in js)))
open(os.path.join(PUB, "index.html"), "w").write(page)
json.dump(sorted(EV), open(os.path.join(HERE, "events.json"), "w"))
for f in ("base.mp4", "avatar.mp4", "tony.webm"):
    shutil.copy(os.path.join(BUILD, f), os.path.join(PUB, f))
print(f"index.html: {ci} captions, {len(js)} animations, {TOTAL} s, {len(EV)} SFX")

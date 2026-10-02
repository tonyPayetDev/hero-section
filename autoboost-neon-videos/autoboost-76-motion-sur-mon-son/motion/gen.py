#!/usr/bin/env python3
"""autoboost-76 - "Ce clip-là, je l'ai quasiment pas monté" - FaceCam Boost composition.

Tony's cut take (plan_actual.json from facecam_cut.py) + the showcased clip
(clip_track.py: his song + the AI-generated motion, cut to the same timeline).
The clip opens full-bleed with Tony in a neon PiP, shrinks into the screens as
proof, disappears for the argument and the CTA, and comes back full-bleed for the
finale, which runs straight into the hook frame (seamless loop).

  BUILD=<facecam_cut work dir> CLIPTRACK=<clip_track.py out dir> python3 gen.py
"""
import json, os, re, html, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
KIT = os.path.abspath(os.path.join(PROJ, "..", "_shared", "facecam-boost-kit"))
sys.path.insert(0, KIT)
from kit import icon, chars, sticker, elastic, facecam_mode  # noqa: E402

BUILD = os.environ.get("BUILD", os.path.join(PROJ, "build"))
CLIPTRACK = os.environ.get("CLIPTRACK", os.path.join(PROJ, "cliptrack"))
FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
P = json.load(open(os.path.join(BUILD, "plan_actual.json")))
TOTAL = P["total"]
FPS = 30
CT = json.load(open(os.path.join(CLIPTRACK, "clip_track.json")))


def q(t):
    return round(round(t * FPS) / FPS, 4)


# ------------------------------------------------------------------ words
W = [c["words"] for c in P["plan"]]


def wt(ci, k=0):
    return W[ci][min(k, len(W[ci]) - 1)]["s"]


def wend(ci):
    return W[ci][-1]["e"]


def wf(ci, needle, after=0):
    for i, w in enumerate(W[ci]):
        if i >= after and needle.lower() in w["w"].lower():
            return w["s"]
    raise KeyError(f"{needle!r} not in cut {ci}")


# blocks = the clip track's bounds: hook | son | sync | idee + cta | fin
B = CT["bounds"]
groups = [{"tag": "hook", "start": B[0], "end": B[1]}, {"tag": "son", "start": B[1], "end": B[2]},
          {"tag": "sync", "start": B[2], "end": B[3]}, {"tag": "idee", "start": B[3], "end": P["plan"][4]["out_start"]},
          {"tag": "cta", "start": P["plan"][4]["out_start"], "end": B[4]}, {"tag": "fin", "start": B[4], "end": TOTAL}]
G = {g["tag"]: g for g in groups}

FACE = (540, 560)
PIP = (600, 1270, 420, 420)
MODES = {
    "PIP": facecam_mode(PIP, FACE, crop_h=760, radius=210),
    "RECT": facecam_mode((24, 1000, 1032, 920), (540, 640), crop_h=920, radius=34),
    "CIRCLE": facecam_mode((220, 1100, 640, 640), FACE, crop_h=820, radius=320),
    "BIG": facecam_mode((160, 980, 760, 760), FACE, crop_h=820, radius=380),
}
MODE = {"hook": "PIP", "son": "RECT", "sync": "CIRCLE", "idee": "RECT", "cta": "BIG", "fin": "PIP"}

# clip placements (#clip is 1080x1920, transform-origin 0 0)
CS = 302 / 1080
SLOT = {"son": (738, 400), "sync": (60, 380)}

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


def kin(sel, t, stagger=0.03, d=0.4):
    js.append(f'tl.fromTo({json.dumps(sel + " .char")},{{opacity:0,y:46,scale:.6}},'
              f'{{opacity:1,y:0,scale:1,duration:{d},ease:"back.out(1.8)",stagger:{stagger},immediateRender:false}},{q(t)});')


def draw(sel, t, d=0.5, all_=False):
    pick = f"document.querySelectorAll({json.dumps(sel)})" if all_ else f"[document.querySelector({json.dumps(sel)})]"
    js.append(f'(function(){{var els={pick};for(var i=0;i<els.length;i++){{var el=els[i];if(!el)continue;var L=el.getTotalLength();'
              f'tl.fromTo(el,{{strokeDasharray:L,strokeDashoffset:L}},{{strokeDashoffset:0,duration:{d},ease:"power2.inOut",immediateRender:false}},{q(t)}+i*0.08);}}}})();')


def fb(call):
    js.append("FB." + call + ";")


def fc(m):
    f = MODES[m]
    return {"x": f["x"], "y": f["y"], "scale": f["scale"], "clipPath": f["clip"]}


# ------------------------------------------------------------------ facecam per block
S("#facecam", 0, dict(fc("PIP"), transformOrigin="0px 0px", zIndex=6))
for a, b in zip(groups, groups[1:]):
    if MODE[a["tag"]] == MODE[b["tag"]]:
        continue
    R("#facecam", b["start"] - 0.25, fc(MODE[a["tag"]]), fc(MODE[b["tag"]]), 0.5, "power3.inOut")
S("#facecam", G["son"]["start"] - 0.25, {"zIndex": 2})
S("#facecam", G["fin"]["start"] - 0.25, {"zIndex": 6})

# PiP ring + name tag (hook, finale)
px, py, pw, ph = PIP
S("#pip-ring", 0, {"x": px - 20, "y": py - 20})
S("#pip-tag", 0, {"x": px + pw / 2 - 70, "y": py + ph - 10})
for g in (G["hook"], G["fin"]):
    t_in = 0.0 if g["tag"] == "hook" else g["start"] + 0.2
    R("#pip-ring", t_in, {"opacity": 0, "scale": 0.7, "rotation": -90}, {"opacity": 1, "scale": 1, "rotation": 0}, 0.4, "back.out(1.8)")
    R("#pip-tag", t_in + 0.15, {"opacity": 0, "y": py + ph + 30}, {"opacity": 1, "y": py + ph - 10}, 0.3, "back.out(2)")
    if g["tag"] == "hook":
        R("#pip-ring", g["end"] - 0.3, {"opacity": 1}, {"opacity": 0}, 0.2, "power2.in")
        R("#pip-tag", g["end"] - 0.3, {"opacity": 1}, {"opacity": 0}, 0.2, "power2.in")

# neon ring (circle blocks), rect chrome (stacked blocks) - as autoboost-75
for g in groups:
    m = MODE[g["tag"]]
    if m in ("CIRCLE", "BIG"):
        S("#ring-pos", g["start"] - 0.3, {"y": -60, "scale": 1.1875} if m == "BIG" else {"y": 0, "scale": 1})
        R("#ring", g["start"] + 0.2, {"opacity": 0, "scale": 0.82}, {"opacity": 1, "scale": 1}, 0.45, "back.out(1.6)")
        R("#ring", g["end"] - 0.3, {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 1.15}, 0.3, "power2.in")
    if m == "RECT":
        R(".rect-fx", g["start"] + 0.2, {"opacity": 0}, {"opacity": 1}, 0.35, "power2.out")
        R(".rect-fx", g["end"] - 0.3, {"opacity": 1}, {"opacity": 0}, 0.3, "power2.in")
draw("#ring-main", G["sync"]["start"] + 0.2, 0.7)
R("#arc-a", 0, {"rotation": 0}, {"rotation": 720}, TOTAL, "none")
R("#arc-b", 0, {"rotation": 0}, {"rotation": -900}, TOTAL, "none")
R("#arc-c", 0, {"rotation": 30}, {"rotation": 510}, TOTAL, "none")
R("#glow-a", 0, {"x": 0, "y": 0}, {"x": 160, "y": 220}, TOTAL, "sine.inOut")
R("#glow-b", 0, {"x": 0, "y": 0}, {"x": -140, "y": -180}, TOTAL, "sine.inOut")
draw("#bg-curve", G["son"]["start"], 2.4)

# ------------------------------------------------------------------ the clip: full -> slot -> slot -> out -> full
full = {"x": 0, "y": 0, "scale": 1, "clipPath": "inset(0px 0px 0px 0px round 0px)", "opacity": 1}


def slot(tag):
    x, y = SLOT[tag]
    return {"x": x, "y": y, "scale": CS, "clipPath": "inset(0px 0px 0px 0px round 120px)", "opacity": 1}


S("#clip", 0, dict(full, transformOrigin="0px 0px"))
# hook visual: the clip slams in - punch zoom + flash + scanline glitch on frame 1
R("#clip", 0, {"scale": 1.18, "x": -97, "y": -173}, {"scale": 1, "x": 0, "y": 0}, 0.38, "power4.out")
R("#flash", 0, {"opacity": 0.75}, {"opacity": 0}, 0.3, "power2.out")
for k, op in enumerate([0.9, 0.2, 0.7, 0]):
    S("#rgb", k * 0.05, {"opacity": op, "x": [18, -26, 10, 0][k]})
ts = G["son"]["start"]
R("#clip", ts - 0.3, full, slot("son"), 0.55, "power3.inOut")
R("#clip-frame", ts + 0.2, {"opacity": 0, "x": SLOT["son"][0], "y": SLOT["son"][1], "scale": 1.1},
  {"opacity": 1, "x": SLOT["son"][0], "y": SLOT["son"][1], "scale": 1}, 0.3, "back.out(2)")
ty = G["sync"]["start"]
R("#clip", ty - 0.28, slot("son"), slot("sync"), 0.5, "power3.inOut")
R("#clip-frame", ty - 0.28, {"x": SLOT["son"][0], "y": SLOT["son"][1]}, {"x": SLOT["sync"][0], "y": SLOT["sync"][1]}, 0.5, "power3.inOut")
ti = G["idee"]["start"]
R("#clip, #clip-frame", ti - 0.28, {"opacity": 1}, {"opacity": 0}, 0.3, "power2.in")
tf = G["fin"]["start"]
R("#clip", tf - 0.22, {"x": 270, "y": 480, "scale": 0.5, "opacity": 0, "clipPath": "inset(0px 0px 0px 0px round 200px)"},
  full, 0.42, "power4.out")
R("#flash", tf - 0.02, {"opacity": 0.6}, {"opacity": 0}, 0.3, "power2.out")

# ------------------------------------------------------------------ screens slide in / out
SCREENS = ["son", "sync", "idee", "cta"]
for tag in SCREENS:
    g = G[tag]
    R(f"#sc-{tag}", g["start"] - 0.28, {"x": 1080}, {"x": 0}, 0.5, "power4.out")
    R(f"#sc-{tag}", g["end"] - 0.28, {"x": 0}, {"x": -1080}, 0.45, "power3.in")
    R("#streak", g["start"] - 0.34, {"x": 1300, "opacity": 1}, {"x": -1500, "opacity": 1}, 0.42, "power2.inOut")


def screen(tag, inner):
    g = G[tag]
    a, b = q(max(0, g["start"] - 0.3)), q(min(TOTAL, g["end"] + 0.3))
    track = 2 if SCREENS.index(tag) % 2 == 0 else 3
    return (f'<section id="sc-{tag}" class="screen clip" data-start="{a}" data-duration="{q(b - a)}" '
            f'data-track-index="{track}"><div class="inner">{inner}</div></section>')


def pill(text, kind="gold", ico=None, top=56):
    return f'<div class="row" style="top:{top}px"><div class="pill {kind}">{icon(ico, 30) if ico else ""}<span>{text}</span></div></div>'


def head(l1, l2, top=150, size=88, size2=None):
    return (f'<div class="row" style="top:{top}px"><div class="hd"><div class="l1" style="font-size:{size}px">{l1}</div>'
            f'<div class="l2" style="font-size:{size2 or size}px">{l2}</div></div></div>')


def wire(d, color, cls):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" '
            f'style="filter:drop-shadow(0 0 8px {color}) drop-shadow(0 0 18px {color})"/>')


def zig(x0, y0, x1, y1, amp=10, waves=5):
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


# real envelope of the song under the sync block (clip_track seg2.wav) - the timeline shows the true waveform
def envelope(path, n):
    import numpy as np
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.abs(np.frombuffer(raw, dtype=np.int16).astype(np.float32))
    ch = np.array_split(x, n)
    e = np.array([np.sqrt((c ** 2).mean()) for c in ch])
    e = e / (e.max() or 1)
    return e


ENV = envelope(os.path.join(CLIPTRACK, "seg2.wav"), 64)
ENV_SON = envelope(os.path.join(CLIPTRACK, "seg1.wav"), 22)

screens, overlays = [], []

# ---- hook: the clip full-bleed, Tony in the PiP ---------------------------------------
gh = G["hook"]
overlays.append(
    f'<section id="ov-hook" class="hook clip" data-start="0" data-duration="{q(gh["end"] + 0.3)}" data-track-index="4">'
    '<div id="shade" style="background:linear-gradient(180deg,rgba(10,10,15,.94) 0%,rgba(10,10,15,.7) 20%,transparent 36%)"></div>'
    f'<div class="row" style="top:96px"><div class="hd"><div id="h-l1" class="l1" style="font-size:96px">{chars("CE CLIP-LÀ", "w")}</div>'
    f'<div id="h-l2" class="l2" style="font-size:150px">{chars("PAS MONTÉ.", "g")}</div>'
    '<div id="h-l3" class="sub2">(quasiment)</div></div></div></section>')
kin("#h-l1", wt(0, 0), 0.025)
kin("#h-l2", wf(0, "pas") - 0.1, 0.035, 0.36)
R("#h-l3", wf(0, "quasiment"), {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0}, 0.3)
R("#shade", gh["end"] - 0.2, {"opacity": 1}, {"opacity": 0}, 0.25, "power2.out")

# ---- son: my sound -> an AI tool -> all the motion -------------------------------------
gs = G["son"]
bars_son = "".join(f'<i style="height:{int(14 + 56 * v)}px"></i>' for v in ENV_SON)
sx, sy = SLOT["son"]
screens.append(screen("son",
    pill("LA MÉTHODE", "gold", "bolt")
    + head(chars("MON SON", "w"), chars("TOUT LE MOTION", "g"), 150, 92, 84)
    + '<svg class="pw" width="1080" height="980" viewBox="0 0 1080 980" style="position:absolute;left:0;top:0;overflow:visible">'
    + wire(zig(310, 640, 400, 640, 8, 3), "#eab308", "w0") + wire(zig(630, 640, sx - 10, 640, 8, 3), "#8b5cf6", "w1")
    + '</svg>'
    + f'<div class="pnode p-son" style="left:40px;top:515px">{icon("feather", 44)}<div class="wave">{bars_son}</div><b>MON SON</b><small>fait maison</small></div>'
    + f'<div class="pnode p-ia" style="left:400px;top:535px">{icon("brain", 64)}<b>OUTIL IA</b></div>'
    + f'<div class="slot" style="left:{sx}px;top:{sy - 40}px"></div>'))
R("#sc-son .pill", gs["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
kin("#sc-son .l1", wf(1, "son"), 0.04)
kin("#sc-son .l2", wf(1, "motion") - 0.15, 0.03)
pop("#sc-son .p-son", wf(1, "créé"))
js.append(f'tl.fromTo("#sc-son .wave i",{{scaleY:.15}},{{scaleY:1,duration:.22,ease:"back.out(3)",stagger:.025,immediateRender:false}},{q(wf(1, "son"))});')
draw("#sc-son .w0", wf(1, "donné"), 0.35)
pop("#sc-son .p-ia", wf(1, "outil"))
R("#sc-son .p-ia", wf(1, "IA"), {"boxShadow": "0 0 50px rgba(139,92,246,.7)"}, {"boxShadow": "0 0 90px rgba(139,92,246,1)"}, 0.25, "power2.out")
draw("#sc-son .w1", wf(1, "généré"), 0.35)
R("#clip-frame", wf(1, "motion"), {"scale": 1}, {"scale": 1.06}, 0.15, "power2.out")
R("#clip-frame", wf(1, "motion") + 0.15, {"scale": 1.06}, {"scale": 1}, 0.3, "back.out(3)")
overlays.append(sticker("st-maison", "FAIT", "MAISON", "gold", None, "spark", left=40, top=1040))
fb(f'sticker(tl,"#st-maison",{q(wf(1, "moi-même"))},{q(wf(1, "outil") - 0.1)},-5)')

# ---- sync: animations, rythme, plans -> all locked on my sound -------------------------
gy = G["sync"]
LANE_W = 604
wave = "".join(f'<i class="wbar wb{i}" style="left:{i * LANE_W / 64:.1f}px;height:{int(6 + 58 * v)}px;margin-bottom:-{int(3 + 29 * v)}px"></i>'
               for i, v in enumerate(ENV))
# cuts and keyframes on the loudest onsets of the real song (deterministic)
import numpy as np  # noqa: E402
d = np.diff(ENV, prepend=ENV[0])
peaks = sorted(sorted(range(2, 62), key=lambda i: -d[i])[:5])
cuts = [0] + peaks + [64]
blocks = "".join(f'<i class="pblk pb{k}" style="left:{a * LANE_W / 64 + 2:.1f}px;width:{(b - a) * LANE_W / 64 - 4:.1f}px"></i>'
                 for k, (a, b) in enumerate(zip(cuts, cuts[1:])))
kfs = "".join(f'<i class="kf kf{k}" style="left:{p * LANE_W / 64 - 10:.1f}px"></i>' for k, p in enumerate(peaks))
slines = "".join(f'<i class="sl sl{k}" style="left:{18 + p * LANE_W / 64 - 1.5:.1f}px"></i>' for k, p in enumerate(peaks))
TR = [("ANIMATIONS", "t-anim", kfs, 58), ("RYTHME", "t-ryth", wave, 178), ("CHANGEMENTS DE PLANS", "t-plan", blocks, 298)]
screens.append(screen("sync",
    pill("LE SECRET", "violet", "bolt")
    + head(chars("TOUT EST CALÉ", "w"), chars("SUR MON SON", "g"), 150, 84, 92)
    + f'<div class="slot" style="left:{SLOT["sync"][0]}px;top:{SLOT["sync"][1] - 40}px"></div>'
    + '<div class="tlp" style="top:340px"><div class="hdr"><span>timeline · clip</span><b>AUTO</b></div>'
    + "".join(f'<div class="trk {cls}" style="top:{top}px"><span class="lab">{lab}</span><div class="lane">{lane}</div></div>'
              for lab, cls, lane, top in TR)
    + slines + '<i class="phd"></i></div>'))
R("#sc-sync .pill", gy["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
up("#sc-sync .tlp", gy["start"] + 0.05, 0.4, 50)
for (lab, cls, _, _), word in zip(TR, ["Animations", "rythme", "changements"]):
    t = wf(2, word)
    R(f"#sc-sync .{cls} .lab", t, {"color": "#6b6782"}, {"color": "#EDEDED"}, 0.2, "power2.out")
    if cls == "t-anim":
        js.append(f'tl.fromTo("#sc-sync .kf",{{scale:0,backgroundColor:"#3a3350"}},{{scale:1,backgroundColor:"#a78bfa",duration:.25,ease:"back.out(3)",stagger:.07,immediateRender:false}},{q(t)});')
    if cls == "t-ryth":
        js.append(f'tl.fromTo("#sc-sync .wbar",{{scaleY:.1,backgroundColor:"#3a3350"}},{{scaleY:1,backgroundColor:"#eab308",duration:.2,ease:"power2.out",stagger:.008,immediateRender:false}},{q(t)});')
    if cls == "t-plan":
        js.append(f'tl.fromTo("#sc-sync .pblk",{{opacity:0,x:-30,borderColor:"#3a3350"}},{{opacity:1,x:0,borderColor:"#8b5cf6",duration:.25,ease:"power3.out",stagger:.06,immediateRender:false}},{q(t)});')
# the playhead runs over the clip's own audio span: it is the song playing in the phone right now
R("#sc-sync .phd", gy["start"], {"opacity": 1, "x": 0}, {"opacity": 1, "x": LANE_W}, gy["end"] - gy["start"], "none")
tc = wf(2, "calé")
js.append(f'tl.fromTo("#sc-sync .sl",{{scaleY:0}},{{scaleY:1,duration:.3,ease:"power2.out",stagger:.06,immediateRender:false}},{q(tc - 0.1)});')
js.append(f'tl.fromTo("#sc-sync .kf, #sc-sync .pblk",{{boxShadow:"0 0 0px rgba(234,179,8,0)"}},{{boxShadow:"0 0 18px rgba(234,179,8,.9)",duration:.3,ease:"power2.out",immediateRender:false}},{q(tc + 0.2)});')
overlays.append(sticker("st-cale", "CALÉ", "SUR LE SON", "gold", "checkc", "spark", left=60, top=1000))
fb(f'sticker(tl,"#st-cale",{q(tc)},{q(gy["end"] - 0.35)},-5)')

# ---- idee: hours of editing -> time on the idea -----------------------------------------
gi = G["idee"]
screens.append(screen("idee",
    pill("CE QUI CHANGE", "gold", "bolt")
    + head(chars("MOINS DE MONTAGE", "w"), chars("PLUS D'IDÉES", "g"), 150, 78, 96)
    + '<div class="ba b-avant"><small>AVANT</small><div class="big">Des heures<br>à monter</div>'
      '<div class="mr"><span>Montage</span><div class="mt"><i class="i-red m-a1"></i></div></div>'
      '<div class="mr"><span>L\'idée</span><div class="mt"><i class="i-mute m-a2"></i></div></div>'
      '<svg class="xx" width="430" height="460" viewBox="0 0 430 460"><path d="M20 30 L410 430 M410 30 L20 430" stroke="#ff6b6b" stroke-width="10" stroke-linecap="round" fill="none"/></svg></div>'
    + f'<div class="ba b-apres"><small>MAINTENANT</small><i class="bulb">{icon("bulb", 70)}</i><div class="big">Le temps<br>sur l\'idée</div>'
      '<div class="mr"><span>Montage</span><div class="mt"><i class="i-mute m-b1"></i></div></div>'
      '<div class="mr"><span>L\'idée</span><div class="mt"><i class="i-gold m-b2"></i></div></div></div>'))
R("#sc-idee .pill", gi["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
kin("#sc-idee .l1", wf(3, "exactement"), 0.025)
kin("#sc-idee .l2", wf(3, "idée") - 0.2, 0.04)
overlays.append(sticker("st-change", "ÇA CHANGE", "TOUT", "violet", "rocket", "spark", left=40, top=1030))
fb(f'sticker(tl,"#st-change",{q(wf(3, "change"))},{q(wf(3, "Au") - 0.15)},-4)')
up("#sc-idee .b-avant", wf(3, "Au"), 0.4, 60)
R("#sc-idee .m-a1", wf(3, "heures"), {"scaleX": 0}, {"scaleX": 1}, 0.6, "power2.out")
R("#sc-idee .m-a2", wf(3, "heures") + 0.1, {"scaleX": 0}, {"scaleX": 0.16}, 0.4, "power2.out")
draw("#sc-idee .xx path", wf(3, "monter") + 0.1, 0.3)
R("#sc-idee .b-avant", wf(3, "monter") + 0.3, {"opacity": 1, "filter": "grayscale(0)"}, {"opacity": 0.45, "filter": "grayscale(1)"}, 0.3, "power2.out")
up("#sc-idee .b-apres", wf(3, "passe", 20) - 0.15, 0.4, 60)
R("#sc-idee .m-b1", wf(3, "temps"), {"scaleX": 0}, {"scaleX": 0.2}, 0.4, "power2.out")
R("#sc-idee .m-b2", wf(3, "temps") + 0.1, {"scaleX": 0}, {"scaleX": 1}, 0.6, "power2.out")
pop("#sc-idee .bulb", wf(3, "idée"))
R("#sc-idee .bulb", wf(3, "idée") + 0.36, {"filter": "drop-shadow(0 0 16px rgba(234,179,8,.9))"}, {"filter": "drop-shadow(0 0 40px rgba(234,179,8,1))"}, 0.3, "power2.out")

# ---- cta: commente MOTION -> DM ----------------------------------------------------------
gc = G["cta"]
tm = wf(4, "MOTION")
screens.append(screen("cta",
    f'<div class="row" style="top:50px"><div class="brand">{icon("rocket", 34)}<span>AUTOMATISATION<b>BOOST</b></span></div></div>'
    + head(chars("COMMENTE", "w"), elastic("MOTION", "tokc"), 160, 100, 170)
    + '<div class="row" style="top:560px"><div class="igc">'
      '<div class="pr"><div class="av">AB</div><div><b>automatisationboost</b><small>Claude Code · n8n · IA</small></div></div>'
      '<div class="cf"><span class="ph">Ajouter un commentaire…</span><span class="tc">' + chars("MOTION") + '</span>'
      f'<i class="snd">{icon("send", 36)}</i></div>'
      '<div class="sub">→ le nom de l\'outil + comment je l\'ai utilisé</div></div></div>'
    + f'<div class="dm"><div class="av">AB</div><div><b>automatisationboost</b><small>t\'a envoyé l\'outil + la méthode</small></div><i class="snd2">{icon("send", 40)}</i></div>'))
R("#sc-cta .brand", gc["start"] + 0.1, {"opacity": 0, "scale": .5}, {"opacity": 1, "scale": 1}, 0.36, "back.out(2.2)")
up("#sc-cta .igc", wf(4, "veux"), 0.4, 50)
up("#sc-cta .sub", wf(4, "nom"))
kin("#sc-cta .l1", wf(4, "utilisé"), 0.025)
R("#sc-cta .l2", tm - 0.05, {"opacity": 0, "scale": 2.4}, {"opacity": 1, "scale": 1}, 0.34, "power4.in")
fb(f'elastic(tl,"#sc-cta .l2",{q(tm + 0.4)},{q(min(2.6, gc["end"] - tm - 0.8))})')
R("#sc-cta .ph", tm - 0.1, {"opacity": 1}, {"opacity": 0}, 0.1, "power2.out")
fb(f'type(tl,"#sc-cta .tc",{q(tm)},0.07)')
pop("#sc-cta .snd", tm + 0.5)
fb(f'press(tl,"#sc-cta .snd",{q(wf(5, "envoie") - 0.3)})')
R("#sc-cta .igc", wf(5, "envoie") - 0.2, {"opacity": 1, "scale": 1}, {"opacity": 0, "scale": 0.94}, 0.2, "power2.in")
R("#sc-cta .dm", wf(5, "envoie") - 0.1, {"opacity": 0, "y": 60, "scale": 0.9}, {"opacity": 1, "y": 0, "scale": 1}, 0.35, "back.out(2)")

# ---- fin: the clip full-bleed again, runs into the hook ----------------------------------
gn = G["fin"]
overlays.append(
    f'<section id="ov-fin" class="finale clip" data-start="{q(gn["start"] - 0.25)}" data-duration="{q(TOTAL - gn["start"] + 0.25)}" data-track-index="5">'
    '<div id="fin-shade"></div><div class="row" style="top:110px"><div class="hd">'
    f'<div class="l1" style="font-size:104px">{chars("LE RÉSULTAT", "w")}</div>'
    f'<div class="l2" style="font-size:118px">{chars("LE PLUS FOU…", "g")}</div></div></div></section>')
R("#fin-shade", gn["start"] - 0.1, {"opacity": 0}, {"opacity": 1}, 0.3, "power2.out")
kin("#ov-fin .l1", wf(6, "résultat") - 0.15, 0.025, 0.32)
kin("#ov-fin .l2", wf(6, "plus") - 0.1, 0.03, 0.32)
# hand-off to the hook: the finale text clears on the last frames so frame 0 matches
R("#ov-fin .hd", TOTAL - 0.2, {"opacity": 1}, {"opacity": 0}, 0.15, "power2.in")
R("#fin-shade", TOTAL - 0.2, {"opacity": 1}, {"opacity": 0.6}, 0.15, "power2.in")

# ------------------------------------------------------------------ captions
KEY = {"clip-là,", "IA…", "motion", "son.", "son", "moi-même,", "Animations,", "rythme,", "changements", "plans,", "calé",
       "heures", "monter,", "l'idée.", "MOTION", "résultat,", "fou,"}
cap_html, cap_js = [], []
ci = 0
for c in P["plan"]:
    chunks, cur = [], []
    for w in c["words"]:
        probe = " ".join(x["w"] for x in cur + [w])
        ends = bool(cur) and re.search(r"[.,!?:…]$", cur[-1]["w"])
        if cur and (len(probe) > 24 or (ends and len(" ".join(x["w"] for x in cur)) >= 12)):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    end_c = c["out_start"] + c["dur"]
    for k, ch in enumerate(chunks):
        a = ch[0]["s"] - 0.04
        b = chunks[k + 1][0]["s"] - 0.04 if k + 1 < len(chunks) else end_c - 0.02
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

# ------------------------------------------------------------------ write
os.makedirs(os.path.join(HERE, "public", "kit"), exist_ok=True)
for f in ("kit.css", "kit.js"):
    shutil.copy(os.path.join(KIT, f), os.path.join(HERE, "public", "kit", f))
for src, dst in ((os.path.join(BUILD, "facecam.mp4"), "facecam.mp4"), (os.path.join(CLIPTRACK, "clip.mp4"), "clip.mp4")):
    shutil.copy(src, os.path.join(HERE, "public", dst))
TEMPLATE = open(os.path.join(HERE, "template.html")).read()
out = (TEMPLATE.replace("%%TOTAL%%", str(q(TOTAL)))
       .replace("%%SCREENS%%", "\n".join(screens))
       .replace("%%HOOK%%", "\n".join(overlays) + '\n<div id="flash"></div>')
       .replace("%%CAPTIONS%%", "\n".join(cap_html))
       .replace("%%JS%%", "\n".join(js + cap_js)))
open(os.path.join(HERE, "public", "index.html"), "w").write(out)
print(f"index.html: {ci} blocs de captions, {len(js)} animations, {q(TOTAL)} s")
print("  " + " | ".join(f"{g['tag']} {g['start']:.2f}-{g['end']:.2f}" for g in groups))

# ------------------------------------------------------------------ SFX events (facecam_audio.py)
EV = [[0.0, "sfx-glitch-hard.mp3", -17], [0.02, "sfx-impact-deep.mp3", -18]]
for g in groups[1:]:
    EV.append([round(g["start"] - 0.30, 3), "sfx-whoosh-v2.mp3", -18])
EV += [[round(wf(0, "pas") - 0.1, 3), "sfx-impact.mp3", -19],
       [round(wf(1, "moi-même"), 3), "sfx-thwip.mp3", -20],
       [round(wf(1, "outil"), 3), "sfx-pop.mp3", -20],
       [round(wf(1, "généré"), 3), "sfx-zoom.mp3", -21],
       [round(wf(2, "Animations"), 3), "sfx-click-soft.mp3", -20],
       [round(wf(2, "rythme"), 3), "sfx-click-soft.mp3", -20],
       [round(wf(2, "changements"), 3), "sfx-click-soft.mp3", -20],
       [round(tc, 3), "sfx-confirm.mp3", -18],
       [round(wf(3, "change"), 3), "sfx-thwip.mp3", -19],
       [round(wf(3, "monter") + 0.1, 3), "sfx-glitch-soft.mp3", -20],
       [round(wf(3, "idée"), 3), "sfx-chime-v2.mp3", -18],
       [round(tm - 0.05, 3), "sfx-impact-deep.mp3", -17],
       [round(tm, 3), "sfx-click-soft.mp3", -19],
       [round(wf(5, "envoie") - 0.1, 3), "sfx-notify.mp3", -17],
       [round(gn["start"] - 0.22, 3), "sfx-dolly-rush.mp3", -19]]
EV = sorted(e for e in EV if 0 <= e[0] < TOTAL - 0.1)
json.dump(EV, open(os.path.join(HERE, "events.json"), "w"))
print(f"events.json: {len(EV)} SFX")

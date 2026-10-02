#!/usr/bin/env python3
"""Kit gallery: a 12 s HyperFrames composition, three 4 s pages.

  page A  the 10 punch stickers
  page B  Notion #3 curve, #2 search -> results, #1 button -> panel, #7 elastic word
  page C  Notion #5 card pile, #6 dock, #4 tile zoom, #8 particle logo

Snapshot at 3.8 / 7.8 / 11.7 s for the kit board, or render it as a preview reel.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, KIT)
from kit import icon, chars, sticker, level, chart_svg, elastic  # noqa: E402

PUB = os.path.join(HERE, "public")
os.makedirs(os.path.join(PUB, "fonts"), exist_ok=True)
os.makedirs(os.path.join(PUB, "kit"), exist_ok=True)
os.makedirs(os.path.join(PUB, "vendor"), exist_ok=True)
for f in ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "DejaVuSansMono-Bold.ttf"):
    shutil.copy(f"/usr/share/fonts/truetype/dejavu/{f}", os.path.join(PUB, "fonts", f))
for f in ("kit.css", "kit.js"):
    shutil.copy(os.path.join(KIT, f), os.path.join(PUB, "kit", f))
GSAP = os.path.join(KIT, "..", "..", "..", ".claude", "skills", "graphic-overlays", "assets", "vendor", "gsap.min.js")
shutil.copy(os.path.abspath(GSAP), os.path.join(PUB, "vendor", "gsap.min.js"))

T = 12.0
STICKERS = [  # (a, b, variant, icon, deco) - the reference board, in the charter
    ("TROP", "LENT", "red", None, "spark"), ("DÉJÀ", "MIEUX", "violet", None, "spark"),
    ("PLUS", "SIMPLE", "gold", None, "spark"), ("GAIN", "TEMPS", "violet", "clock", None),
    ("NIVEAU", "MAX", "violet", "crown", "bar"), ("ÇA", "MONTE", "gold", "trend", "swoosh"),
    ("AUTOMATISE", "ÇA", "gold", "gear", None), ("PLUS", "CLAIR", "gold", "bulb", "spark"),
    ("BON", "SYSTÈME", "violet", "checkc", "swoosh"), ("ÇA", "PART", "violet", "rocket", "spark"),
]
st_html, js = [], []
for i, (a, b, v, ic, d) in enumerate(STICKERS):
    left = 60 if i % 2 == 0 else 330      # one column, staggered: long words never collide
    top = 270 + i * 158
    st_html.append(sticker(f"g{i}", a, b, v, ic, d, left=left, top=top).replace("font-size", "font-size"))
    js.append(f'FB.sticker(tl,"#g{i}",{0.3 + i * 0.22:.2f},3.85,{-6 if v == "red" else -4});')

CHART = chart_svg([(0, .08), (.2, .12), (.4, .34), (.6, .42), (.8, .72), (1, 1)], w=880, h=200, label="100 %")

html_b = f'''
<section id="pb" class="page clip" data-start="4" data-duration="4" data-track-index="3">
  <div class="ttl"><span class="fb-w">MOTIONS</span> <span class="fb-g">1/2</span></div>
  <div class="cardx" style="left:60px;top:250px;width:960px"><div class="lab">#3 COURBE DE PROGRESSION</div><div id="gchart">{CHART}</div></div>
  <div class="cardx" style="left:60px;top:640px;width:960px"><div class="lab">#2 RECHERCHE → RÉSULTATS</div>
    <div class="fb-search" id="gsearch">{icon("search", 40)}<span class="tc">{chars("délégation")}</span><i class="fb-caret"></i></div>
    <div class="res">
      <div class="fb-result"><div class="sq" style="background:#eab308"></div><div><b>Tâche simple → modèle léger</b><small>sous-agent</small></div></div>
      <div class="fb-result"><div class="sq" style="background:#8b5cf6"></div><div><b>Tâche complexe → Opus</b><small>puissance max</small></div></div>
    </div></div>
  <div class="cardx" style="left:60px;top:1240px;width:460px;height:300px"><div class="lab">#1 BOUTON → PANNEAU</div>
    <div class="fb-btn" id="gbtn">{icon("send", 34)}<span>COMMENTER</span></div>
    <div class="panel" id="gpanel"><div class="av">T</div><b>TOKEN</b></div></div>
  <div class="cardx" style="left:560px;top:1240px;width:460px;height:300px"><div class="lab">#7 TYPO ÉLASTIQUE</div>
    <div id="gel" class="el">{elastic("TOKEN", "tokc")}</div></div>
</section>'''
js += [
    'FB.chart(tl,"#gchart",4.3,1.2);',
    'FB.type(tl,"#gsearch",4.5,0.06);',
    'FB.results(tl,"#pb .fb-result",5.3);',
    'FB.press(tl,"#gbtn",5.6);',
    'tl.fromTo("#gbtn",{opacity:1,scale:1},{opacity:0,scale:1.3,duration:.18,ease:"power2.in",immediateRender:false},5.95);',
    'tl.fromTo("#gpanel",{opacity:0,scaleX:.35,scaleY:.6},{opacity:1,scaleX:1,scaleY:1,duration:.32,ease:"back.out(1.6)",immediateRender:false},6.0);',
    'FB.elastic(tl,"#gel",4.4,3.2);',
]

html_c = f'''
<section id="pc" class="page clip" data-start="8" data-duration="4" data-track-index="4">
  <div class="ttl"><span class="fb-w">MOTIONS</span> <span class="fb-g">2/2</span></div>
  <div class="cardx" style="left:60px;top:250px;width:960px;height:360px"><div class="lab">#5 PILE DE CARTES</div>
    <div class="fb-stack" style="position:absolute;left:40px;top:90px;width:880px;height:220px">
      <div class="fb-scard" id="gs3" style="transform:translateY(40px) scale(.9)"><b class="big fb-v">#03</b> Opus</div>
      <div class="fb-scard" id="gs2" style="transform:translateY(20px) scale(.95)"><b class="big fb-g">#02</b> Modèle léger</div>
      <div class="fb-scard" id="gs1"><b class="big fb-w">#01</b> CLAUDE.md</div>
    </div></div>
  <div class="cardx" style="left:60px;top:660px;width:960px;height:300px"><div class="lab">#6 DOCK</div>
    <div class="fb-dock" id="gdock" style="position:absolute;left:150px;top:120px">
      <div class="fb-di">{icon("doc", 46)}</div><div class="fb-di">{icon("feather", 46)}</div><div class="fb-di hot">{icon("brain", 46)}</div>
      <div class="fb-di">{icon("gear", 46)}</div><div class="fb-di">{icon("trend", 46)}</div><div class="fb-di">{icon("rocket", 46)}</div>
      <i class="fb-cursor"></i></div></div>
  <div class="cardx" style="left:60px;top:1010px;width:460px;height:520px"><div class="lab">#4 ZOOM TUILE</div>
    <div class="tiles6">{"".join(f'<i class="tl6{" hot" if k == 1 else ""}" id="gt{k}"></i>' for k in range(6))}</div></div>
  <div class="cardx" style="left:560px;top:1010px;width:460px;height:520px"><div class="lab">#8 LOGO PARTICULES</div>
    <canvas id="gpart" class="fb-particles" width="420" height="420" style="left:20px;top:80px"></canvas></div>
</section>'''
js += [
    'FB.stackFly(tl,"#gs1",8.6,"#gs2",{y:20,r:0,s:.95});',
    'FB.stackFly(tl,"#gs2",9.9,"#gs3",{y:40,r:0,s:.9});',
    'FB.dock(tl,"#gdock",8.4,3.2,40,700);',
    'FB.tileZoom(tl,"#gt1",9.0,-99.5,128,2.05,0.6);',
    'FB.particles(tl,"#gpart","AB",8.5,{font:"700 210px AB Sans",step:7,r:2.6,dIn:1.2,tOut:11.0,dOut:0.7,seed:11});',
]

PAGE_A = (f'<section id="pa" class="page clip" data-start="0" data-duration="4" data-track-index="2">'
          f'<div class="ttl"><span class="fb-w">STICKERS</span> <span class="fb-g">PUNCH</span></div>'
          + "".join(st_html) + "</section>")

doc = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8" />
<link rel="stylesheet" href="kit/kit.css" />
<style>
@font-face {{ font-family: "AB Sans"; src: url("fonts/DejaVuSans-Bold.ttf") format("truetype"); font-weight: 700; font-display: block; }}
@font-face {{ font-family: "AB Sans"; src: url("fonts/DejaVuSans.ttf") format("truetype"); font-weight: 400; font-display: block; }}
@font-face {{ font-family: "AB Mono"; src: url("fonts/DejaVuSansMono-Bold.ttf") format("truetype"); font-weight: 700; font-display: block; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0a0a0f; font-family: "AB Sans", "DejaVu Sans", sans-serif; font-weight: 700; color: #EDEDED; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0a0a0f;
  background-image: radial-gradient(circle at 15% 10%, rgba(234,179,8,.16), transparent 45%), radial-gradient(circle at 90% 85%, rgba(139,92,246,.22), transparent 50%),
  linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
  background-size: auto, auto, 60px 60px, 60px 60px; }}
.page {{ position: absolute; inset: 0; }}
.ttl {{ position: absolute; left: 60px; top: 90px; font-size: 96px; letter-spacing: -0.02em; }}
.page .fb-sticker {{ font-size: 54px; }}
.cardx {{ position: absolute; border-radius: 30px; padding: 30px 40px; background: linear-gradient(180deg, rgba(26,22,40,.95), rgba(14,12,22,.95));
  border: 2px solid rgba(139,92,246,.6); box-shadow: 0 0 40px rgba(139,92,246,.22); overflow: hidden; }}
.lab {{ font-size: 22px; letter-spacing: .16em; color: #eab308; margin-bottom: 18px; }}
.char {{ display: inline-block; opacity: 0; }}
.res {{ display: flex; flex-direction: column; gap: 16px; margin-top: 22px; }}
#gbtn {{ position: absolute; left: 70px; top: 130px; }}
.panel {{ position: absolute; left: 40px; top: 120px; width: 380px; height: 110px; border-radius: 55px; border: 3px solid #eab308; background: #111117;
  display: flex; align-items: center; gap: 20px; padding: 0 20px; opacity: 0; box-shadow: 0 0 30px rgba(234,179,8,.4); }}
.panel .av {{ width: 66px; height: 66px; border-radius: 50%; background: linear-gradient(135deg,#eab308,#8b5cf6); color: #0a0a0f; display: flex; align-items: center; justify-content: center; font-size: 30px; }}
.panel b {{ font-family: "AB Mono", monospace; font-size: 46px; color: #eab308; letter-spacing: .08em; }}
.el {{ position: absolute; left: 0; width: 460px; top: 120px; text-align: center; font-size: 92px; }}
.tokc {{ color: #eab308; text-shadow: 0 0 26px rgba(234,179,8,.7); }}
.fb-scard {{ font-size: 40px; display: flex; align-items: center; gap: 26px; height: 150px; }}
.fb-scard .big {{ font-size: 80px; }}
.fb-cursor {{ position: absolute; left: 0; bottom: -34px; width: 22px; height: 22px; border-radius: 50%; background: #EDEDED; box-shadow: 0 0 14px #fff; }}
.tiles6 {{ position: absolute; left: 40px; top: 100px; width: 380px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; }}
.tl6 {{ display: block; height: 110px; border-radius: 18px; background: #111117; border: 2px solid #3a3350; }}
.tl6.hot {{ border-color: #eab308; box-shadow: 0 0 24px rgba(234,179,8,.6); background: linear-gradient(180deg,#2a2410,#111117); position: relative; z-index: 2; }}
</style></head><body>
<div id="root" data-composition-id="fb-kit-gallery" data-start="0" data-width="1080" data-height="1920" data-duration="{T}" data-fps="30">
{PAGE_A}
{html_b}
{html_c}
<script src="vendor/gsap.min.js"></script>
<script src="kit/kit.js"></script>
<script>
(function () {{
  var tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["fb-kit-gallery"] = tl;
}})();
</script>
</div></body></html>'''
open(os.path.join(PUB, "index.html"), "w").write(doc)
print("gallery index.html ok")

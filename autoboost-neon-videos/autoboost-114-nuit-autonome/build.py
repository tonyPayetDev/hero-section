# -*- coding: utf-8 -*-
# Builder for autoboost-114-nuit-autonome — seedance style (gabarit autoboost-40)
# Emits public/index.html. All timing derived from the REAL voice.mp3 silences.
DUR = 34.58
S1, S2, S3, BROLL, S4, S5 = 0.0, 8.60, 15.16, 21.95, 24.05, 27.60
BROLL_END = 24.05

# captions: (start, TEXT_UPPER, "tag") where tag = "hot:WORD"|"vhot:WORD"|"ohot:WORD" or ""
caps = [
 [0.83,"CHAQUE SOIR",""],
 [1.56,"TU REFAIS TOUT","hot:TOUT"],
 [2.30,"MÊMES TÂCHES À",""],
 [3.16,"LA MAIN","ohot:MAIN"],
 [3.76,"LE TRI",""],
 [4.17,"LES RELANCES",""],
 [4.97,"LE MONTAGE","hot:MONTAGE"],
 [5.76,"ET SI TOUT",""],
 [6.31,"ÇA TOURNAIT","vhot:TOURNAIT"],
 [7.43,"QUE TU DORS ?","hot:DORS"],
 [8.62,"UN :",""],
 [9.00,"PLANIFIE UNE",""],
 [9.60,"UNE ROUTINE","hot:ROUTINE"],
 [10.30,"TU DÉCRIS LA",""],
 [10.90,"UNE SEULE FOIS","hot:SEULE"],
 [11.97,"ET CLAUDE CODE","vhot:CLAUDE"],
 [12.77,"LA RELANCE",""],
 [13.40,"CHAQUE JOUR","hot:CHAQUE JOUR"],
 [14.10,"À L'HEURE QUE",""],
 [14.83,"TU CHOISIS","hot:CHOISIS"],
 [15.62,"DEUX :",""],
 [16.11,"DONNE-LUI LES ACCÈS","hot:ACCÈS"],
 [17.35,"BRANCHÉ À TON",""],
 [18.14,"N8N ET À","hot:N8N"],
 [18.62,"TON DÉPÔT",""],
 [19.22,"IL AGIT VRAIMENT","vhot:AGIT"],
 [20.23,"IL NE SE",""],
 [20.66,"CONTENTE PAS DE",""],
 [21.52,"RÉPONDRE","ohot:RÉPONDRE"],
 [22.78,"UN GARDE-FOU","hot:GARDE-FOU"],
 [23.97,"IL PRÉPARE TOUT","hot:PRÉPARE"],
 [24.91,"MAIS IL NE",""],
 [25.46,"PUBLIE RIEN SANS","ohot:RIEN"],
 [26.37,"TA VALIDATION","vhot:VALIDATION"],
 [27.36,"RÉSULTAT :",""],
 [28.11,"TON TRAVAIL",""],
 [28.76,"EN PILOTE","hot:PILOTE"],
 [29.88,"AUTOMATIQUE","hot:AUTOMATIQUE"],
 [31.07,"LA NUIT","vhot:NUIT"],
 [31.66,"COMMENTE LE MOT",""],
 [32.53,"NUIT","hot:NUIT"],
 [32.87,"JE T'ENVOIE LE",""],
 [33.61,"LE GUIDE","hot:GUIDE"],
]

# ---- SFX (palette v1, roles transposed to THESE cuts) ----
# zooms start 1.2s before their cut so the whoosh peak lands on the cut.
sfx = [
 ("sfx-hook","sfx-glitch-hard.mp3",0.40,0.26),
 ("sfx-hook-imp","sfx-impact.mp3",0.40,0.20),
 ("sfx-verdict","sfx-notify.mp3",6.20,0.16),
 ("sfx-zoom-1","sfx-zoom.mp3",7.40,0.17),          # peak on cut1 8.60
 ("sfx-hook-2","sfx-glitch-soft.mp3",8.62,0.15),
 ("sfx-click-1","sfx-click.mp3",8.75,0.18),
 ("sfx-lock","sfx-notify.mp3",9.60,0.16),
 ("sfx-o1","sfx-click-soft.mp3",12.80,0.13),
 ("sfx-o2","sfx-click-soft.mp3",13.05,0.13),
 ("sfx-o3","sfx-click-soft.mp3",13.30,0.13),
 ("sfx-zoom-2","sfx-zoom.mp3",13.96,0.17),         # peak on cut2 15.16
 ("sfx-click-2","sfx-click.mp3",15.62,0.18),
 ("sfx-valid","sfx-confirm.mp3",16.30,0.18),       # good move ok
 ("sfx-ko-1","sfx-click-soft.mp3",17.40,0.13),
 ("sfx-ko-2","sfx-click-soft.mp3",18.70,0.13),
 ("sfx-strike-1","sfx-whoosh-lat.mp3",20.20,0.14),
 ("sfx-strike-2","sfx-whoosh-lat.mp3",20.50,0.14),
 ("sfx-zoom-3","sfx-zoom.mp3",20.75,0.17),         # peak on cut3 21.95
 ("sfx-arrow","sfx-whoosh-lat.mp3",22.10,0.16),    # broll enter
 ("sfx-zoom-4","sfx-zoom.mp3",22.85,0.19),         # peak on S4 24.05
 ("sfx-click-3","sfx-click.mp3",24.10,0.18),
 ("sfx-r1","sfx-click-soft.mp3",24.15,0.13),
 ("sfx-r2","sfx-click-soft.mp3",24.95,0.13),
 ("sfx-r3","sfx-click-soft.mp3",25.55,0.13),
 ("sfx-zoom-5","sfx-zoom.mp3",26.40,0.19),         # peak on cut5 27.60
 ("sfx-limit","sfx-notify.mp3",27.75,0.16),
 ("sfx-cta-pop","sfx-pop.mp3",30.00,0.24),
 ("sfx-cta-imp","sfx-impact.mp3",30.00,0.18),
 ("sfx-cta-sub","sfx-click-soft.mp3",32.00,0.13),
]

def caps_js():
    out=[]
    for s,t,tag in caps:
        out.append(f' [{s},{t!r},{tag!r}]')
    return "[\n"+",\n".join(out)+"\n]"

def sfx_html():
    L=[]
    for i,(sid,src,st,vol) in enumerate(sfx):
        L.append(f'  <audio id="{sid}" src="assets/{src}" data-start="{st}" data-volume="{vol}"></audio>')
    return "\n".join(L)

HTML = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<script src="assets/gsap.min.js"></script>
<style>
:root{{
  --bg:#060606; --accent-yellow:#FFE600; --violet:#A855F7; --orange:#FF8A3D;
  --ink:#f5f5f7; --muted:#9aa0aa; --bad:#ff5f57; --good:#28c840;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
#root{{position:absolute;width:1080px;height:1920px;overflow:hidden;background:var(--bg);
  font-family:'Inter','Helvetica Neue',Arial,sans-serif;color:var(--ink);}}

.scene{{position:absolute;top:0;left:0;width:1080px;height:1120px;opacity:0;overflow:hidden;}}
.scene-1{{background:linear-gradient(135deg,#0a0a0a 0%,#2a0a0a 100%);}}
.scene-2{{background:radial-gradient(circle at 50% 40%,#12081f 0%,#050505 74%);}}
.scene-3{{background:linear-gradient(135deg,#0a0a0a 0%,#12081f 100%);}}
.scene-4{{background:radial-gradient(circle at 50% 40%,#1a0a2a 0%,#050505 70%);}}
.scene-5{{background:linear-gradient(135deg,#0a0a0a 0%,#1a0a2a 100%);}}
.scene-broll{{height:1920px;background:#000;}}

.pad{{position:absolute;left:70px;right:70px;top:140px;}}
.kicker{{font-size:30px;font-weight:800;letter-spacing:4px;text-transform:uppercase;color:var(--violet);opacity:0;}}
.title{{font-size:80px;line-height:1.02;font-weight:800;letter-spacing:-1px;margin-top:22px;}}
.title .y{{color:var(--accent-yellow);}} .title .v{{color:var(--violet);}} .title .o{{color:var(--orange);}}

.tipnum{{position:absolute;right:70px;top:36px;width:88px;height:88px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:900;
  color:#060606;background:var(--accent-yellow);opacity:0;
  box-shadow:0 0 40px rgba(255,230,0,.45);}}

.card{{position:absolute;left:90px;right:90px;top:470px;background:#0d0d12;border:1px solid #2a2140;
  border-radius:26px;padding:32px 40px;box-shadow:0 30px 80px rgba(0,0,0,.6);opacity:0;}}
.card .bar{{display:flex;align-items:center;gap:12px;margin-bottom:22px;}}
.dot{{width:15px;height:15px;border-radius:50%;}} .dot.r{{background:#ff5f57;}} .dot.a{{background:#febc2e;}} .dot.g{{background:#28c840;}}
.card .file{{margin-left:14px;color:var(--muted);font-size:26px;font-weight:600;}}
.mono{{font-family:'DejaVu Sans Mono','Courier New',monospace;font-size:30px;line-height:1.6;}}
.mono .dim{{color:#6b7280;}} .mono .lit{{color:#fff;}}
.mono .lock{{color:#060606;background:var(--accent-yellow);border-radius:5px;padding:1px 6px;font-weight:700;}}
.verdict{{position:absolute;left:90px;right:90px;top:830px;text-align:center;font-size:44px;font-weight:900;
  color:var(--orange);opacity:0;letter-spacing:.5px;}}

.order{{position:absolute;left:90px;right:90px;top:800px;display:flex;gap:18px;justify-content:center;}}
.ochip{{padding:16px 26px;border-radius:16px;background:#0d0d12;border:1px solid #2a2140;
  font-size:28px;font-weight:800;color:#cfd2da;opacity:0;white-space:nowrap;}}
.ochip .n{{color:var(--accent-yellow);margin-right:10px;}}

.moves{{position:absolute;left:80px;right:80px;top:470px;display:flex;flex-direction:column;gap:20px;}}
.mv{{position:relative;display:flex;align-items:center;gap:22px;padding:24px 30px;border-radius:20px;
  background:#0d0d12;border:1px solid #2a2140;font-size:34px;font-weight:700;color:#cfd2da;opacity:0;}}
.mv .tag{{width:44px;height:44px;flex:0 0 44px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:26px;font-weight:900;}}
.mv.ko .tag{{background:rgba(255,95,87,.15);color:var(--bad);border:2px solid var(--bad);}}
.mv.ok{{border-color:var(--good);box-shadow:0 0 34px rgba(40,200,64,.18);}}
.mv.ok .tag{{background:rgba(40,200,64,.15);color:var(--good);border:2px solid var(--good);}}
.mv .strike{{position:absolute;left:30px;right:30px;top:50%;height:3px;background:var(--bad);
  transform:scaleX(0);transform-origin:left center;border-radius:2px;}}
.mv .dur{{margin-left:auto;font-size:28px;font-weight:900;color:var(--accent-yellow);}}

.refs{{position:absolute;left:70px;right:70px;top:440px;display:flex;flex-direction:column;gap:22px;}}
.ref{{display:flex;align-items:center;gap:24px;padding:26px 30px;border-radius:20px;
  background:#0d0d12;border:1px solid #2a2140;opacity:0;}}
.ref .at{{font-family:'DejaVu Sans Mono','Courier New',monospace;font-size:38px;font-weight:900;
  color:var(--accent-yellow);width:230px;flex:0 0 230px;}}
.ref .arw{{color:var(--violet);font-size:34px;font-weight:900;}}
.ref .what{{font-size:36px;font-weight:800;color:#fff;}}

#broll,.broll-vid{{position:absolute;top:0;left:0;width:1080px;height:1920px;object-fit:cover;filter:brightness(.5);opacity:0;z-index:1;}}
.broll-grad{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,.15) 40%,rgba(0,0,0,.75) 100%);}}

.limit{{position:absolute;left:150px;right:150px;top:400px;opacity:0;}}
.limit .lab{{display:flex;justify-content:space-between;font-size:28px;font-weight:800;color:var(--muted);margin-bottom:14px;}}
.limit .lab b{{color:var(--accent-yellow);}}
.limit .track{{height:16px;border-radius:99px;background:#16161e;border:1px solid #2a2140;overflow:hidden;}}
.limit .fill{{height:100%;width:200px;border-radius:99px;background:linear-gradient(90deg,var(--accent-yellow),var(--orange));
  transform-origin:left center;transform:scaleX(0);box-shadow:0 0 20px rgba(255,230,0,.5);}}
.cta-word{{position:absolute;left:0;right:0;top:540px;text-align:center;font-size:120px;font-weight:900;
  color:var(--accent-yellow);letter-spacing:2px;text-shadow:0 0 50px rgba(255,230,0,.6);opacity:0;}}
.cta-sub{{position:absolute;left:80px;right:80px;top:720px;text-align:center;font-size:40px;font-weight:700;color:#fff;opacity:0;line-height:1.3;}}
.cta-follow{{position:absolute;left:80px;right:80px;top:860px;text-align:center;font-size:30px;font-weight:700;color:var(--orange);opacity:0;letter-spacing:1px;}}

#caption-band{{position:absolute;top:930px;left:0;width:1080px;height:180px;z-index:8;}}
#cap-plate{{position:absolute;left:0;top:5px;width:1080px;height:104px;
  background:linear-gradient(90deg,rgba(6,6,8,0) 0%,rgba(6,6,8,.88) 10%,rgba(6,6,8,.88) 90%,rgba(6,6,8,0) 100%);}}
.cap-bar{{position:absolute;left:50%;width:800px;height:5px;margin-left:-400px;border-radius:3px;
  background:linear-gradient(90deg,rgba(255,230,0,0) 0%,var(--accent-yellow) 14%,var(--accent-yellow) 86%,rgba(255,230,0,0) 100%);
  box-shadow:0 0 16px rgba(255,230,0,.55);opacity:.85;}}
#cap-bar-top{{top:0;}}
#cap-bar-bot{{top:109px;}}
.caption{{position:absolute;left:50%;top:30px;transform:translateX(-50%);white-space:nowrap;
  font-size:27px;font-weight:700;text-transform:uppercase;letter-spacing:2px;line-height:1.2;color:#fff;
  text-shadow:-3px -3px 0 #000,3px -3px 0 #000,-3px 3px 0 #000,3px 3px 0 #000,-3px 0 0 #000,3px 0 0 #000,0 -3px 0 #000,0 3px 0 #000, 0 6px 18px rgba(0,0,0,.6);
  opacity:0;}}
.caption .hot{{color:var(--accent-yellow);text-shadow:-3px -3px 0 #000,3px -3px 0 #000,-3px 3px 0 #000,3px 3px 0 #000,-3px 0 0 #000,3px 0 0 #000,0 -3px 0 #000,0 3px 0 #000,0 0 22px rgba(255,230,0,.9);}}
.caption .vhot{{color:var(--violet);text-shadow:-3px -3px 0 #000,3px -3px 0 #000,-3px 3px 0 #000,3px 3px 0 #000,-3px 0 0 #000,3px 0 0 #000,0 -3px 0 #000,0 3px 0 #000,0 0 22px rgba(168,85,247,.9);}}
.caption .ohot{{color:var(--orange);text-shadow:-3px -3px 0 #000,3px -3px 0 #000,-3px 3px 0 #000,3px 3px 0 #000,-3px 0 0 #000,3px 0 0 #000,0 -3px 0 #000,0 3px 0 #000,0 0 22px rgba(255,138,61,.9);}}

#avatar-frame{{position:absolute;bottom:70px;left:50%;width:560px;height:560px;margin-left:-280px;
  border-radius:50%;overflow:hidden;background:var(--bg);border:5px solid var(--accent-yellow);
  box-shadow:0 0 0 2px rgba(6,6,6,.9),0 0 36px 4px rgba(255,230,0,.55),0 0 90px 20px rgba(255,230,0,.22);z-index:5;}}
#avatar-frame video{{position:absolute;top:50%;left:50%;width:560px;height:706px;transform:translate(-50%,-46%);
  object-fit:cover;object-position:center top;}}
#avatar-ring{{position:absolute;bottom:58px;left:50%;width:584px;height:584px;margin-left:-292px;border-radius:50%;
  border:3px solid var(--accent-yellow);opacity:0;pointer-events:none;box-shadow:0 0 40px rgba(255,230,0,.35);z-index:5;}}
#avatar-orbit{{position:absolute;bottom:52px;left:50%;width:596px;height:596px;margin-left:-298px;border-radius:50%;pointer-events:none;
  background:conic-gradient(from 0deg,transparent 0deg,transparent 280deg,rgba(255,230,0,.12) 320deg,var(--accent-yellow) 353deg,#fff8d6 360deg);
  -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 8px),#000 calc(100% - 8px));
  mask:radial-gradient(farthest-side,transparent calc(100% - 8px),#000 calc(100% - 8px));
  filter:drop-shadow(0 0 12px rgba(255,230,0,.9));z-index:5;}}
#avatar-orbit-v{{position:absolute;bottom:46px;left:50%;width:608px;height:608px;margin-left:-304px;border-radius:50%;pointer-events:none;
  background:conic-gradient(from 0deg,transparent 0deg,transparent 250deg,rgba(168,85,247,.10) 300deg,rgba(168,85,247,.75) 348deg,#e9d5ff 360deg);
  -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 6px),#000 calc(100% - 6px));
  mask:radial-gradient(farthest-side,transparent calc(100% - 6px),#000 calc(100% - 6px));
  filter:drop-shadow(0 0 14px rgba(168,85,247,.85));opacity:0;z-index:5;}}
audio{{display:none;}}
</style>
</head>
<body>
<!-- Timeline calée sur les silences RÉELS de public/assets/voice.mp3 (silencedetect=-40dB).
     Coupes de scène dans les silences : {S2} / {S3} / {BROLL} / {S4} / {S5} -->
<div id="root" data-composition-id="autoboost114nuit" data-start="0" data-width="1080" data-height="1920" data-duration="{DUR}">

  <!-- SCENE 1 — HOOK : le travail du soir, à la main -->
  <div class="scene scene-1" data-s="{S1}" data-d="{round(S2-0.01,2)}">
    <div class="pad">
      <div class="kicker" data-role="k1">Chaque soir</div>
      <div class="title" data-role="t1">Tu refais tout<br><span class="o">à la main.</span></div>
    </div>
    <div class="card" data-role="c1">
      <div class="bar"><span class="dot r"></span><span class="dot a"></span><span class="dot g"></span><span class="file">taches-du-soir.log</span></div>
      <div class="mono">
        <div class="dim" data-role="pl1">22:00  trier les mails</div>
        <div class="dim" data-role="pl2">23:00  relancer les prospects</div>
        <div class="lit" data-role="pl3">00:00  monter la vidéo…</div>
      </div>
    </div>
    <div class="verdict" data-role="v1">Et si ça tournait sans toi ?</div>
  </div>

  <!-- SCENE 2 — ASTUCE 1 : planifie une routine -->
  <div class="scene scene-2" data-s="{S2}" data-d="{round(S3-S2-0.01,2)}">
    <div class="tipnum" data-role="n2">1</div>
    <div class="pad">
      <div class="kicker" data-role="k2">Astuce 1</div>
      <div class="title" data-role="t2" style="font-size:74px;">Planifie <span class="y">une routine</span><br>une seule fois</div>
    </div>
    <div class="card" data-role="c2" style="top:490px;">
      <div class="bar"><span class="dot r"></span><span class="dot a"></span><span class="dot g"></span><span class="file">routine.cron</span></div>
      <div class="mono">
        <div data-role="pw1"><span class="lock">Chaque jour à 3h → lance la tâche</span></div>
        <div class="dim" data-role="pw2">puis elle tourne, sans toi…</div>
      </div>
    </div>
    <div class="order">
      <div class="ochip" data-role="o1"><span class="n">1</span>DÉCRIS</div>
      <div class="ochip" data-role="o2"><span class="n">2</span>PLANIFIE</div>
      <div class="ochip" data-role="o3"><span class="n">3</span>OUBLIE</div>
    </div>
  </div>

  <!-- SCENE 3 — ASTUCE 2 : donne-lui les accès -->
  <div class="scene scene-3" data-s="{S3}" data-d="{round(BROLL-S3-0.01,2)}">
    <div class="tipnum" data-role="n3">2</div>
    <div class="pad">
      <div class="kicker" data-role="k3">Astuce 2</div>
      <div class="title" data-role="t3" style="font-size:74px;">Donne-lui <span class="y">les accès</span></div>
    </div>
    <div class="moves">
      <div class="mv ok" data-role="mv1">
        <span class="tag">✓</span>Branché → il agit<span class="dur">n8n · git</span>
      </div>
      <div class="mv ko" data-role="mv2">
        <span class="tag">✕</span>Sans accès → il répond
        <span class="strike" data-role="sk2"></span>
      </div>
      <div class="mv ko" data-role="mv3">
        <span class="tag">✕</span>Tu copies à la main
        <span class="strike" data-role="sk3"></span>
      </div>
    </div>
  </div>

  <!-- BROLL — respiration avant l'astuce 3 -->
  <video id="broll" class="broll-vid" src="assets/broll-creator.mp4" data-start="{BROLL}" data-duration="{round(S4-BROLL,2)}" muted playsinline></video>
  <div class="scene scene-broll" data-s="{BROLL}" data-d="{round(S4-BROLL,2)}"><div class="broll-grad"></div></div>

  <!-- SCENE 4 — ASTUCE 3 : garde un garde-fou -->
  <div class="scene scene-4" data-s="{S4}" data-d="{round(S5-S4-0.01,2)}">
    <div class="tipnum" data-role="n4">3</div>
    <div class="pad">
      <div class="kicker" data-role="k4">Astuce 3</div>
      <div class="title" data-role="t4" style="font-size:74px;">Garde <span class="y">un garde-fou</span></div>
    </div>
    <div class="refs">
      <div class="ref" data-role="r1"><span class="at">PRÉPARE</span><span class="arw">→</span><span class="what">tout le travail</span></div>
      <div class="ref" data-role="r2"><span class="at">TU VALIDES</span><span class="arw">→</span><span class="what">d'un seul clic</span></div>
      <div class="ref" data-role="r3"><span class="at">PUBLIÉ</span><span class="arw">→</span><span class="what">jamais sans toi</span></div>
    </div>
  </div>

  <!-- SCENE 5 — RÉSULTAT + CTA -->
  <div class="scene scene-5" data-s="{S5}" data-d="{round(DUR-S5,2)}">
    <div class="pad" style="top:150px;text-align:center;">
      <div class="kicker" data-role="k5" style="color:var(--accent-yellow);">Résultat</div>
    </div>
    <div class="limit" data-role="lim">
      <div class="lab"><span>tes tâches du soir</span><span><b>0</b> à la main</span></div>
      <div class="track"><div class="fill" data-role="fill"></div></div>
    </div>
    <div class="cta-word" data-role="ctaword" data-layout-allow-overflow="true">NUIT</div>
    <div class="cta-sub" data-role="ctasub">Commente le mot <span style="color:var(--accent-yellow);">NUIT</span><br>je t'envoie le guide</div>
    <div class="cta-follow" data-role="ctafollow">— mais seulement si tu me suis</div>
  </div>

  <!-- AVATAR OVERLAY -->
  <div id="avatar-frame" data-layout-allow-overflow="true">
    <video id="avatar" src="assets/avatar-keyed.mp4" data-start="0" data-duration="{DUR}" data-layout-allow-overflow="true" muted playsinline></video>
  </div>
  <div id="avatar-ring" class="clip" data-layout-allow-overflow="true" data-start="0" data-duration="{DUR}"></div>
  <div id="avatar-orbit" class="clip" data-layout-allow-overflow="true" data-start="0" data-duration="{DUR}"></div>
  <div id="avatar-orbit-v" class="clip" data-layout-allow-overflow="true" data-start="0" data-duration="{DUR}"></div>

  <!-- CAPTIONS -->
  <div id="caption-band">
    <div id="cap-plate"></div>
    <div id="cap-bar-top" class="cap-bar"></div>
    <div id="cap-bar-bot" class="cap-bar"></div>
  </div>

  <!-- AUDIO -->
  <audio id="voice" src="assets/voice.mp3" data-start="0" data-duration="{DUR}" data-volume="1"></audio>
  <!-- BGM = "YOU CAN ASK THE FLOWERS (HORROR MIX)", -12.4 LUFS -> 0.05 (palette v1). -->
  <audio id="bgm" src="assets/flowers_horror.mp3" data-start="0" data-duration="{DUR}" data-volume="0.05"></audio>

  <!-- SFX — palette v1 (_shared/sfx-palette/v1), rôles transposés sur ces coupes -->
{sfx_html()}
</div>

<script>
const compId="autoboost114nuit";
const DUR={DUR};
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});
const $=s=>document.querySelector(s);
const R=r=>document.querySelector('[data-role="'+r+'"]');

/* SCENES auto fade */
document.querySelectorAll(".scene").forEach((el)=>{{
  const s=parseFloat(el.dataset.s), d=parseFloat(el.dataset.d);
  tl.to(el,{{opacity:1,duration:0.3,ease:"power2.out"}},s);
  tl.to(el,{{opacity:0,duration:0.3,ease:"power2.in"}},s+d-0.3);
}});
document.querySelectorAll(".broll-vid").forEach((el)=>{{
  const s=parseFloat(el.dataset.start), d=parseFloat(el.dataset.duration);
  tl.to(el,{{opacity:1,duration:0.3,ease:"power2.out"}},s);
  tl.to(el,{{opacity:0,duration:0.3,ease:"power2.in"}},s+d-0.3);
}});

/* SCENE 1 */
tl.fromTo(R("k1"),{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},0.10);
tl.fromTo(R("t1"),{{opacity:0,y:26}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},0.40);
tl.fromTo(R("c1"),{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},1.40);
tl.fromTo(R("pl1"),{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.3}},1.70);
tl.fromTo(R("pl2"),{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.3}},2.10);
tl.fromTo(R("pl3"),{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.3}},2.50);
tl.fromTo(R("v1"),{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.6)"}},6.10);

/* SCENE 2 */
tl.fromTo(R("n2"),{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.8)"}},{S2+0.05});
tl.fromTo(R("k2"),{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{S2+0.10});
tl.fromTo(R("t2"),{{opacity:0,y:26}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{S2+0.30});
tl.fromTo(R("c2"),{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{S2+0.85});
tl.fromTo(R("pw1"),{{opacity:0}},{{opacity:1,duration:0.35}},{S2+1.05});
tl.fromTo(R("pw2"),{{opacity:0}},{{opacity:1,duration:0.35}},{S2+2.20});
tl.fromTo(R("o1"),{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},12.80);
tl.fromTo(R("o2"),{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},13.05);
tl.fromTo(R("o3"),{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},13.30);

/* SCENE 3 */
tl.fromTo(R("n3"),{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.8)"}},{S3+0.05});
tl.fromTo(R("k3"),{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{S3+0.10});
tl.fromTo(R("t3"),{{opacity:0,y:26}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{S3+0.30});
tl.fromTo(R("mv1"),{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},16.20);
tl.fromTo(R("mv2"),{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},17.30);
tl.fromTo(R("mv3"),{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},18.60);
tl.fromTo(R("sk2"),{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.out"}},20.20);
tl.fromTo(R("sk3"),{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.out"}},20.50);

/* SCENE 4 */
tl.fromTo(R("n4"),{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.8)"}},{S4+0.05});
tl.fromTo(R("k4"),{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{S4+0.10});
tl.fromTo(R("t4"),{{opacity:0,y:26}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{S4+0.30});
tl.fromTo(R("r1"),{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{S4+0.10});
tl.fromTo(R("r2"),{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{S4+0.90});
tl.fromTo(R("r3"),{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{S4+1.50});

/* SCENE 5 */
tl.fromTo(R("k5"),{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{S5+0.10});
tl.fromTo(R("lim"),{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},{S5+0.10});
tl.fromTo(R("fill"),{{scaleX:0}},{{scaleX:1,duration:1.0,ease:"power2.out"}},{S5+0.30});
tl.fromTo(R("ctaword"),{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.6)"}},30.00);
tl.to(R("ctaword"),{{scale:1.06,duration:0.5,ease:"sine.inOut",repeat:5,yoyo:true}},31.00);
tl.fromTo(R("ctasub"),{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4}},31.90);
tl.fromTo(R("ctafollow"),{{opacity:0}},{{opacity:1,duration:0.4}},33.40);

/* CAPTIONS */
const caps={caps_js()};
const band=$("#caption-band");
caps.forEach((c,i)=>{{
  const [start,txt,tag]=c;
  const end=(i<caps.length-1)?caps[i+1][0]-0.02:{round(DUR-0.28,2)};
  const el=document.createElement("div");el.className="caption";
  if(tag){{
    const [cls,word]=tag.split(":");
    const cl=cls==="hot"?"hot":cls==="vhot"?"vhot":"ohot";
    if(txt===word){{el.innerHTML='<span class="'+cl+'">'+txt+'</span>';}}
    else{{el.innerHTML=txt.split(word).join('<span class="'+cl+'">'+word+'</span>');}}
  }} else {{el.textContent=txt;}}
  band.appendChild(el);
  tl.fromTo(el,{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.16,ease:"power2.out"}},start);
  tl.to(el,{{opacity:0,duration:0.12}},end-0.14);
}});

/* Rails */
tl.to("#cap-bar-top",{{opacity:0.5,duration:1.05,ease:"sine.inOut",repeat:32,yoyo:true}},0);
tl.to("#cap-bar-bot",{{opacity:0.5,duration:1.05,ease:"sine.inOut",repeat:32,yoyo:true}},0.52);

/* AVATAR ring/orbit — masqué pendant le broll */
const BROLL_START={BROLL}, BROLL_END={BROLL_END};
tl.to(["#avatar-frame","#avatar-orbit"],{{opacity:0,duration:0.3,ease:"power2.out"}},BROLL_START);
tl.to(["#avatar-frame","#avatar-orbit"],{{opacity:1,duration:0.3,ease:"power2.out"}},BROLL_END);
tl.to("#avatar-ring",{{opacity:0.8,scale:1.06,duration:0.5,ease:"sine.inOut",repeat:43,yoyo:true}},0);
tl.to("#avatar-ring",{{opacity:0.85,scale:1.06,duration:0.5,ease:"sine.inOut",repeat:21,yoyo:true}},BROLL_END);
tl.to("#avatar-orbit",{{rotation:"+=360",duration:2.2,repeat:9,ease:"none"}},0);
tl.to("#avatar-orbit",{{rotation:"+=360",duration:2.2,repeat:4,ease:"none"}},BROLL_END);
tl.to("#avatar-ring",{{opacity:1,scale:1.08,duration:0.5,ease:"power2.out"}},30.00);

/* PULSE VIOLET SUR LES DROPS de flowers_horror.mp3 : 2.34 / 10.36 / 18.38 / 26.40 */
var LEAD=0.12;
[2.34,10.36,18.38,26.40].forEach(function(t){{
  var s=t-LEAD;
  tl.fromTo("#avatar-orbit-v",{{rotation:0,scale:0.985}},{{rotation:360,scale:1.02,duration:1.45,ease:"power2.out"}},s);
  tl.fromTo("#avatar-orbit-v",{{opacity:0}},{{opacity:0.9,duration:LEAD,ease:"power2.out"}},s);
  tl.to("#avatar-orbit-v",{{opacity:0,duration:0.55,ease:"power2.in"}},s+0.90);
}});

tl.totalDuration(DUR);
window.__timelines[compId]=tl;
</script>
</body>
</html>
'''

open("public/index.html","w").write(HTML)
print("written public/index.html", len(HTML), "bytes ; caps:", len(caps), "; sfx:", len(sfx))

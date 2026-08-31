// Prompt Reveal builder — generates public/index.html for each autoboost-56-prompt-reveal-* project.
// Layout: Higgsfield clip FULL FRAME background (native audio stripped) + neon terminal console
// with the exact prompt scrolling (secret keywords redacted) + corner avatar bubbles + gated CTA.
import fs from 'fs';
import path from 'path';

const ROOT = '/work/autoboost-neon-videos';

export function buildHtml(cfg) {
  const {id, dur, kicker, keyword, mode, console: consoleHtml, tag, ctaStep, popTimes, beat} = cfg;
  const wide = mode === 'wide';
  const CTA_IN = +(dur - 2.6).toFixed(2);
  const POP = +(CTA_IN - 2.1).toFixed(2);
  const SCROLL_END = +(dur - 5.5).toFixed(2);

  return `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<style>
  @font-face { font-family: Inter; font-weight: 400; font-display: block; src: url(fonts/Inter-400-latin.woff2) format('woff2'); }
  @font-face { font-family: Inter; font-weight: 700; font-display: block; src: url(fonts/Inter-700-latin.woff2) format('woff2'); }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
    --bg: #060606; --gold: #FFE600; --violet: #A855F7; --orange: #FF8A3D;
    --ink: #F3F3F7; --dim: #9A9AA6; --card: #0b0710;
    --mono: ui-monospace, "DejaVu Sans Mono", "Courier New", monospace;
  }
  #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #050505;
          font-family: Inter, "DejaVu Sans", sans-serif; color: var(--ink); }

  /* ---------- CLIP HIGGSFIELD — PLEIN CADRE (son natif coupé) ---------- */
  #herobg { position: absolute; z-index: 0; inset: -60px; width: calc(100% + 120px); height: calc(100% + 120px);
     object-fit: cover; filter: blur(46px) brightness(.62) saturate(1.35); }
  #hero { position: absolute; z-index: 1; ${wide
      ? 'top: 236px; left: 0; width: 1080px; height: 608px;'
      : 'inset: 0; width: 100%; height: 100%;'} object-fit: cover; }
  ${wide ? `#hero-frame { position: absolute; z-index: 2; top: 236px; left: 0; width: 1080px; height: 608px;
     box-shadow: inset 0 0 0 2px rgba(255,230,0,.30), 0 26px 80px rgba(0,0,0,.65); pointer-events: none; }` : ''}
  #scrim { position: absolute; z-index: 3; inset: 0; pointer-events: none;
     background: linear-gradient(180deg, rgba(0,0,0,.72) 0%, rgba(0,0,0,.18) 16%, rgba(0,0,0,.06) 40%, rgba(5,4,8,.55) 56%, rgba(5,4,8,.9) 74%, rgba(5,4,8,.97) 100%); }
  #vignette { position: absolute; z-index: 3; inset: 0; pointer-events: none;
     background: radial-gradient(120% 78% at 50% 34%, transparent 44%, rgba(0,0,0,.55) 100%); }

  /* ---------- top kicker ---------- */
  #kicker { position: absolute; z-index: 8; top: 52px; left: 50%; transform: translateX(-50%);
     display: flex; align-items: center; gap: 14px; padding: 12px 26px; border-radius: 999px;
     background: rgba(10,8,16,.72); border: 1px solid rgba(168,85,247,.45);
     font-size: 26px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: #d9cffb; opacity: 0; white-space: nowrap; }
  #kicker .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--gold); box-shadow: 0 0 14px var(--gold); }

  #vid-tag { position: absolute; z-index: 8; left: 34px; top: ${wide ? '898px' : '150px'};
     display: flex; align-items: center; gap: 14px; opacity: 0;
     font-size: 25px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }
  #vid-tag .pill { padding: 8px 18px; border-radius: 10px; background: var(--gold); color: #0a0a0a; box-shadow: 0 0 22px rgba(255,230,0,.5); }
  #hf-credit { position: absolute; z-index: 8; right: 34px; top: ${wide ? '898px' : '150px'};
     display: flex; align-items: center; gap: 10px; padding: 8px 16px; border-radius: 999px;
     background: rgba(8,8,10,.62); border: 1px solid rgba(255,255,255,.18); opacity: 0;
     font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #e9e9ef; }
  #hf-credit small { color: var(--dim); font-size: 15px; letter-spacing: 3px; }

  /* ---------- PROMPT console (glass, le clip respire derrière) ---------- */
  #console { position: absolute; z-index: 4; top: 1004px; left: 24px; width: 1032px; height: 772px;
     border-radius: 24px; overflow: hidden; opacity: 0;
     background: linear-gradient(180deg, rgba(16,12,24,.80), rgba(8,7,12,.90));
     border: 1px solid rgba(255,255,255,.12); box-shadow: inset 0 0 70px rgba(168,85,247,.08), 0 -18px 60px rgba(0,0,0,.5); }
  #console-bar { position: absolute; top: 0; left: 0; width: 100%; height: 78px; z-index: 3;
     display: flex; align-items: center; gap: 14px; padding: 0 30px;
     background: linear-gradient(180deg, rgba(20,16,28,.98), rgba(20,16,28,.70));
     border-bottom: 1px solid rgba(255,255,255,.09); }
  #console-bar .tl { display: flex; gap: 10px; }
  #console-bar .tl i { width: 16px; height: 16px; border-radius: 50%; display: inline-block; }
  #console-bar .tl .r { background: #ff5f57; } #console-bar .tl .y { background: #febc2e; } #console-bar .tl .g { background: #28c840; }
  #console-bar .title { font-family: var(--mono); font-size: 25px; font-weight: 700; letter-spacing: 1px; color: #cfc7e6; }
  #console-bar .title b { color: var(--gold); }
  #console-view { position: absolute; top: 78px; left: 0; width: 100%; height: 694px; overflow: hidden; z-index: 1;
     -webkit-mask: linear-gradient(180deg, transparent 0, #000 54px, #000 calc(100% - 86px), transparent 100%);
             mask: linear-gradient(180deg, transparent 0, #000 54px, #000 calc(100% - 86px), transparent 100%); }
  #console-scroll { position: absolute; top: 0; left: 0; width: 100%; padding: 28px 40px 120px;
     font-family: var(--mono); font-size: 28px; line-height: 1.6; color: #7ff0d8; white-space: pre-wrap; letter-spacing: .3px; }
  #console-scroll .c { color: #63b3ff; }
  #console-scroll .k { color: var(--gold); }
  #console-scroll .m { color: var(--violet); }
  #console-scroll .o { color: #ff8a3d; }
  #console-scroll .redact { display: inline-block; position: relative; color: transparent;
     background: linear-gradient(90deg, rgba(255,230,0,.24), rgba(168,85,247,.24));
     border-radius: 6px; padding: 0 10px; filter: blur(.4px); }
  #console-scroll .redact::after { content: "${keyword}"; position: absolute; inset: 0; color: var(--gold);
     font-size: 19px; letter-spacing: 2px; display: flex; align-items: center; justify-content: center;
     text-shadow: 0 0 10px rgba(255,230,0,.6); filter: none; }
  #console-scroll .cursor { display: inline-block; width: 16px; height: 30px; background: var(--gold);
     vertical-align: -5px; margin-left: 4px; box-shadow: 0 0 12px var(--gold); }

  /* ---------- neon line (beat) ---------- */
  #neon-line { position: absolute; z-index: 6; top: 1806px; left: 0; width: 1080px; height: 5px; transform-origin: 50% 50%;
     background: linear-gradient(90deg, transparent, var(--gold) 18%, var(--violet) 50%, var(--gold) 82%, transparent);
     box-shadow: 0 0 16px rgba(255,230,0,.7), 0 0 40px rgba(168,85,247,.4); opacity: .9; }

  /* ---------- brand ---------- */
  #brand { position: absolute; z-index: 7; bottom: 58px; left: 50%; transform: translateX(-50%);
     display: flex; align-items: center; gap: 16px; opacity: 0; }
  #brand .mark { width: 60px; height: 60px; }
  #brand .wm { font-size: 38px; font-weight: 700; letter-spacing: 2px; }
  #brand .wm b { color: var(--gold); }

  /* ---------- AVATAR — petite bulle de coin, JAMAIS sur le clip ---------- */
  .apop { position: absolute; z-index: 25; left: 42px; bottom: 132px; width: 286px; height: 432px;
     border-radius: 22px; overflow: hidden; opacity: 0;
     background: var(--card); border: 3px solid var(--gold);
     box-shadow: 0 0 0 2px rgba(6,6,6,.9), 0 20px 50px rgba(0,0,0,.6), 0 0 44px rgba(255,230,0,.30); }
  .apop video { position: absolute; left: 50%; top: 0; height: 100%; width: auto; transform: translateX(-50%); }
  .apop .grad { position: absolute; inset: 0; pointer-events: none;
     background: linear-gradient(180deg, transparent 58%, rgba(11,7,16,.92) 100%); }
  .apop .role { position: absolute; z-index: 2; left: 0; bottom: 14px; width: 100%; text-align: center; padding: 0 10px;
     font-size: 17px; font-weight: 700; letter-spacing: 1.4px; text-transform: uppercase; color: var(--gold);
     text-shadow: 0 2px 14px rgba(0,0,0,.85); }
  #avatar-bubble { position: absolute; z-index: 26; left: 356px; bottom: 330px;
     display: flex; align-items: center; gap: 12px; padding: 16px 32px; border-radius: 999px;
     background: var(--gold); color: #0a0a0a; font-size: 32px; font-weight: 700; letter-spacing: 2px;
     text-transform: uppercase; box-shadow: 0 0 50px rgba(255,230,0,.55); opacity: 0; white-space: nowrap; }

  /* ---------- CTA overlay ---------- */
  #cta { position: absolute; z-index: 20; inset: 0; opacity: 0;
     background: radial-gradient(120% 90% at 50% 38%, #180b26 0%, #070707 70%); text-align: center; }
  #cta .wm { margin-top: 44px; font-size: 56px; font-weight: 700; letter-spacing: 1px; }
  #cta .wm b { color: var(--gold); } #cta .wm i { color: var(--violet); font-style: normal; }
  #cta .step { margin-top: 726px; font-size: 58px; font-weight: 700; text-transform: uppercase; line-height: 1.08; letter-spacing: -1px; }
  #cta .step .v { color: var(--violet); } #cta .step .g { color: var(--gold); }
  #cta .keyword { display: inline-block; margin: 22px 0 10px; background: var(--gold); color: #0a0a0a;
     font-weight: 700; font-size: ${keyword.length > 6 ? 108 : 126}px; letter-spacing: 6px; padding: 14px 64px; border-radius: 22px;
     box-shadow: 0 0 80px rgba(255,230,0,.6); text-transform: uppercase; }
  #cta .deliver { margin-top: 12px; font-size: 40px; font-weight: 700; color: var(--ink); }
  #cta .deliver .g { color: var(--gold); }

  /* ---------- faux champ de commentaire ---------- */
  #fakecomment { position: absolute; z-index: 27; left: 44px; bottom: 96px; width: 992px; height: 108px;
     display: flex; align-items: center; gap: 18px; padding: 0 22px 0 24px; border-radius: 999px;
     background: rgba(20,18,26,.94); border: 2px solid rgba(255,255,255,.16);
     box-shadow: 0 18px 50px rgba(0,0,0,.6), 0 0 40px rgba(168,85,247,.18); opacity: 0; }
  #fakecomment .ava { width: 62px; height: 62px; border-radius: 50%; flex: 0 0 62px;
     background: linear-gradient(135deg, var(--violet), var(--gold)); }
  #fakecomment .field { flex: 1; text-align: left; font-size: 34px; font-weight: 700; color: #efeff5; letter-spacing: 1px; }
  #fakecomment .field .typed { color: var(--gold); }
  #fakecomment .caret { display: inline-block; width: 4px; height: 36px; background: var(--gold); vertical-align: -6px; margin-left: 3px; }
  #fakecomment .send { flex: 0 0 auto; padding: 14px 30px; border-radius: 999px; background: var(--gold); color: #0a0a0a;
     font-size: 27px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
</style>
</head>
<body>
<div id="root" data-composition-id="${id}" data-start="0" data-width="1080" data-height="1920" data-duration="${dur}">

  ${wide ? `<video id="herobg" src="assets/hero.mp4" data-start="0" data-duration="${dur}" muted playsinline></video>` : ''}
  <video id="hero" src="assets/hero.mp4" data-start="0" data-duration="${dur}" muted playsinline></video>
  ${wide ? '<div id="hero-frame"></div>' : ''}
  <div id="scrim"></div>
  <div id="vignette"></div>

  <div id="kicker"><span class="dot"></span>${kicker}</div>
  <div id="vid-tag"><span class="pill">Résultat</span><span>${tag}</span></div>
  <div id="hf-credit"><small>généré&nbsp;avec</small>1&nbsp;prompt</div>

  <div id="console">
    <div id="console-bar">
      <span class="tl"><i class="r"></i><i class="y"></i><i class="g"></i></span>
      <span class="title">le_prompt_exact&nbsp;·&nbsp;<b>seedance_2.5</b></span>
    </div>
    <div id="console-view">
      <div id="console-scroll">${consoleHtml}</div>
    </div>
  </div>

  <div id="neon-line"></div>

  <div id="brand">
    <svg class="mark" viewBox="0 0 64 64" fill="none">
      <rect x="3" y="3" width="58" height="58" rx="16" fill="#0c0c0c" stroke="#FFE600" stroke-width="2.5"/>
      <path d="M35 12 L20 36 H31 L27 52 L44 26 H33 Z" fill="#FFE600"/>
    </svg>
    <div class="wm">AUTO<b>BOOST</b></div>
  </div>

  <div id="pop1" class="apop">
    <video src="assets/avatar-hook.mp4" data-start="${popTimes[0]}" data-duration="3.0" muted playsinline></video>
    <div class="grad"></div><div class="role">${cfg.roles[0]}</div>
  </div>
  <div id="pop3" class="apop">
    <video src="assets/avatar-card.mp4" data-start="${popTimes[1]}" data-duration="3.2" muted playsinline></video>
    <div class="grad"></div><div class="role">${cfg.roles[1]}</div>
  </div>
  <div id="pop5" class="apop">
    <video src="assets/avatar-cta.mp4" data-start="${POP}" data-duration="${(dur - POP).toFixed(2)}" muted playsinline></video>
    <div class="grad"></div>
  </div>
  <div id="avatar-bubble">Commente&nbsp;<span style="color:#7a1adf">${keyword}</span>&nbsp;<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0a0a0a" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-6px"><path d="M12 4v13"/><path d="M6 11l6 6 6-6"/></svg></div>

  <div id="fakecomment">
    <span class="ava"></span>
    <span class="field">Ajouter un commentaire… <span class="typed" id="typed"></span><span class="caret"></span></span>
    <span class="send">Envoyer</span>
  </div>

  <div id="cta">
    <div class="wm">AUTO<b>BOOST</b> <i>·</i> Video</div>
    <div class="step"><span class="v">Tu veux</span> le <span class="g">prompt exact</span> ?</div>
    <div class="keyword">${keyword}</div>
    <div class="deliver">→ commente <span class="g">${keyword}</span>, je te l'envoie en DM</div>
  </div>

  <audio id="voice" src="assets/mix.mp3" data-start="0" data-duration="${dur}" data-volume="1"></audio>
</div>

<script src="assets/gsap.min.js"></script>
<script>
  const DUR = ${dur};
  const tl = gsap.timeline({ paused: true });

  tl.fromTo("#kicker", { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 0.2);
  tl.fromTo("#vid-tag", { opacity: 0, x: -16 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.6);
  tl.fromTo("#hf-credit", { opacity: 0, x: 16 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.6);
  tl.fromTo("#console", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.75);
  tl.fromTo("#brand", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 1.0);

  // auto-scroll du prompt — passe linéaire unique
  const content = document.getElementById("console-scroll");
  const view = document.getElementById("console-view");
  const dist = Math.max(0, content.scrollHeight - view.clientHeight);
  const SCROLL_START = 1.7, SCROLL_END = ${SCROLL_END};
  tl.fromTo(content, { y: 0 }, { y: -dist, duration: SCROLL_END - SCROLL_START, ease: "none" }, SCROLL_START);
  tl.to("#console-scroll .cursor", { opacity: 0, duration: 0.5, repeat: 60, yoyo: true, ease: "steps(1)" }, 0);

  // ligne néon beat-sync
  const BEATP = ${beat}, BEAT0 = 0.30;
  for (let i = 0, t = BEAT0; t < DUR - 1.2; i++, t += BEATP) {
    const down = (i % 4 === 0);
    tl.to("#neon-line", { scaleY: down ? 3.2 : 2.0, opacity: 1, duration: 0.09, ease: "power2.out" }, t);
    tl.to("#neon-line", { scaleY: 1, opacity: 0.9, duration: BEATP * 0.6, ease: "power2.in" }, t + 0.09);
  }

  // AVATAR — petite bulle de coin, fondu doux, le clip reste visible
  function popWindow(sel, tIn, tOut) {
    tl.fromTo(sel, { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.42, ease: "power2.out" }, tIn);
    tl.to(sel, { opacity: 0, scale: 0.97, duration: 0.42, ease: "power2.in" }, tOut);
  }
  popWindow("#pop1", ${popTimes[0]}, ${(popTimes[0] + 2.6).toFixed(2)});
  popWindow("#pop3", ${popTimes[1]}, ${(popTimes[1] + 2.8).toFixed(2)});

  // 3e avatar = CTA
  const POP = ${POP};
  tl.fromTo("#pop5", { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.42, ease: "power2.out" }, POP);
  tl.fromTo("#avatar-bubble", { opacity: 0, scale: 0.7, y: 14 }, { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(2.4)" }, POP + 0.4);
  tl.to("#avatar-bubble", { scale: 1.08, duration: 0.28, repeat: 3, yoyo: true, ease: "sine.inOut" }, POP + 0.9);

  // faux champ de commentaire — le mot se tape lettre par lettre
  const WORD = "${keyword}";
  tl.fromTo("#fakecomment", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }, POP + 0.2);
  const typed = document.getElementById("typed");
  for (let i = 1; i <= WORD.length; i++) {
    tl.call(() => { typed.textContent = WORD.slice(0, i); }, null, POP + 0.7 + i * 0.11);
  }
  tl.to("#fakecomment .send", { scale: 1.12, duration: 0.2, repeat: 3, yoyo: true, ease: "sine.inOut" }, POP + 0.8 + WORD.length * 0.11);

  // CTA overlay
  const CTA_IN = ${CTA_IN};
  tl.to("#avatar-bubble", { opacity: 0, duration: 0.3 }, CTA_IN - 0.1);
  // le faux champ de commentaire RESTE sur la carte CTA (c'est le geste demandé)
  tl.to("#fakecomment", { scale: 1.04, duration: 0.35, ease: "power2.out" }, CTA_IN + 0.85);
  tl.to("#fakecomment", { scale: 1, duration: 0.35, ease: "power2.in" }, CTA_IN + 1.2);
  tl.fromTo("#cta", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.out" }, CTA_IN);
  tl.to("#pop5", { top: 140, left: 390, bottom: "auto", width: 300, height: 452, duration: 0.55, ease: "power3.inOut" }, CTA_IN);
  tl.fromTo("#cta .wm", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.4 }, CTA_IN + 0.25);
  tl.fromTo("#cta .step", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, CTA_IN + 0.45);
  tl.fromTo("#cta .keyword", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, CTA_IN + 0.7);
  tl.fromTo("#cta .deliver", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.4 }, CTA_IN + 1.0);

  window.__timelines = window.__timelines || {};
  window.__timelines["${id}"] = tl;
</script>
</body>
</html>
`;
}

// ---- run ----
const cfgPath = process.argv[2];
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const out = path.join(ROOT, cfg.dir, 'public', 'index.html');
fs.writeFileSync(out, buildHtml(cfg));
console.log('written', out, 'dur', cfg.dur);

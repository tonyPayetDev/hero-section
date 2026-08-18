/* =====================================================================
   CHAOS -> AUTOMATISER  --  reusable 10s visual hook (AutomatisationBoost)
   ---------------------------------------------------------------------
   100% procedural (DOM + CSS + GSAP). No image, no video, no font icon.
   Works MUTED: the story is carried entirely by motion.

   5 beats (locked, see README):
     0-2s  chaos      : dozens of task tiles pile up, counter climbs, shake
     2-4s  freeze     : everything stops dead. VISUAL SILENCE. Do not fill.
     4-6s  cursor     : a cursor walks to a button and clicks it
     6-8s  execution  : every task snaps to a grid and completes at once
     8-10s lockup     : brand + punchline

   USAGE (host composition):
     <script src="hooks/chaos-hook.js"></script>
     <script>
       ChaosHook.mount(document.getElementById('root'), HOOK_VARS); // vars = host file
       ChaosHook.build(tl, 0);                                      // tl = gsap timeline
     </script>

   NOTE ON ENCODING: this file is deliberately ASCII-only. All accented
   copy (tasks, labels, punchline) must be passed in from the host HTML,
   which declares <meta charset="utf-8">. Never hardcode accents here.
   ===================================================================== */
(function (global) {
  'use strict';

  var DUR = 10.0;

  /* --------------------------- DEFAULTS ---------------------------- */
  /* ASCII-safe fallbacks only. Override everything from the host. */
  var DEFAULTS = {
    tasks: [
      'Post Instagram', 'Script video', 'Relance client', 'Devis #1042',
      'Montage reel', 'Mail prospect', 'Facture', 'Planning semaine',
      'Newsletter', 'Article blog', 'Story du jour', 'Veille IA',
      'Retouche photo', 'Reponse DM', 'Miniature', 'Rapport mensuel'
    ],
    tileCount: 48,
    buttonLabel: 'AUTOMATISER',
    counterLabel: 'TACHES EN RETARD',
    counterDoneLabel: 'TACHES EXECUTEES',
    counterTarget: 128,
    punchLine1: 'Arrete de travailler comme une machine.',
    punchLine2: 'Construis-en une.',
    brandTop: 'AUTOMATISATION',
    brandBottom: 'BOOST',
    accent: '#FFE600',   /* primary neon (button, brand, done state) */
    accent2: '#A855F7',  /* secondary neon (punchline highlight)     */
    danger: '#FF3B30',   /* chaos state                              */
    ok: '#3DFF9E',       /* executed state                           */
    bg: '#050505',
    autoHide: true       /* hide the whole hook layer at t0 + 10s     */
  };

  /* ------------------------ deterministic rng ---------------------- */
  function rnd(i, k) {
    var x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453;
    return x - Math.floor(x);
  }

  var V = null, root = null;

  /* ------------------------------ CSS ------------------------------ */
  function css(v) {
    return [
      '#chaosHook{position:absolute;inset:0;z-index:40;overflow:hidden;',
      '  background:' + v.bg + ';font-family:Inter,"DejaVu Sans",sans-serif;}',
      '#chaosHook .ch-glow{position:absolute;left:50%;top:38%;width:1400px;height:1400px;',
      '  transform:translate(-50%,-50%);pointer-events:none;',
      '  background:radial-gradient(circle,rgba(255,59,48,.16) 0%,rgba(5,5,5,0) 62%);opacity:0;}',

      /* ---- tile field ---- */
      '#chaosField{position:absolute;inset:0;}',
      '#chaosHook .ch-tile{position:absolute;width:300px;height:76px;border-radius:11px;',
      '  background:#17171b;border:1px solid rgba(255,255,255,.10);',
      '  display:flex;align-items:center;gap:14px;padding:0 16px;opacity:0;',
      '  box-shadow:0 10px 26px rgba(0,0,0,.55);}',
      '#chaosHook .ch-tile .d{width:11px;height:11px;border-radius:50%;flex:0 0 auto;',
      '  background:' + v.danger + ';box-shadow:0 0 10px ' + v.danger + ';}',
      '#chaosHook .ch-tile .t{font-size:21px;font-weight:400;color:rgba(240,240,246,.80);',
      '  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
      '#chaosHook .ch-tile .bar{position:absolute;left:0;bottom:0;height:3px;width:0%;',
      '  background:' + v.ok + ';border-radius:0 0 11px 11px;}',
      '#chaosHook .ch-tile .ck{position:absolute;right:16px;width:20px;height:11px;',
      '  border-left:4px solid ' + v.ok + ';border-bottom:4px solid ' + v.ok + ';',
      '  transform:rotate(-45deg) scale(.2);opacity:0;}',

      /* ---- counter ---- */
      '#chaosCount{position:absolute;z-index:6;left:0;right:0;top:118px;text-align:center;opacity:0;}',
      '#chaosCount .n{font-size:150px;font-weight:700;line-height:1;color:' + v.danger + ';',
      '  text-shadow:0 0 46px rgba(255,59,48,.55);letter-spacing:-4px;}',
      '#chaosCount .l{margin-top:14px;font-size:25px;font-weight:700;letter-spacing:9px;',
      '  color:rgba(255,255,255,.52);text-transform:uppercase;}',
      '#chaosCount .l2{position:absolute;left:0;right:0;top:100%;margin-top:14px;font-size:25px;',
      '  font-weight:700;letter-spacing:9px;color:' + v.ok + ';text-transform:uppercase;opacity:0;}',

      /* ---- freeze layers ---- */
      '#chaosTint{position:absolute;inset:0;z-index:7;background:#070a12;opacity:0;pointer-events:none;}',
      '#chaosVig{position:absolute;inset:0;z-index:8;opacity:0;pointer-events:none;',
      '  background:radial-gradient(circle at 50% 46%,rgba(0,0,0,0) 34%,rgba(0,0,0,.86) 100%);}',
      '#chaosFlash{position:absolute;inset:0;z-index:20;background:#fff;opacity:0;pointer-events:none;}',
      '#chaosScrim{position:absolute;inset:0;z-index:9;background:rgba(4,4,6,.62);opacity:0;pointer-events:none;}',

      /* ---- button ---- */
      '#chaosBtn{position:absolute;z-index:11;left:50%;top:960px;transform:translate(-50%,-50%) scale(.86);',
      '  width:560px;height:140px;border-radius:20px;opacity:0;',
      '  background:' + v.accent + ';display:flex;align-items:center;justify-content:center;',
      '  box-shadow:0 0 0 rgba(255,230,0,0),0 22px 60px rgba(0,0,0,.6);}',
      '#chaosBtn span{font-size:47px;font-weight:700;letter-spacing:5px;color:#0b0b0b;}',
      '#chaosRing{position:absolute;z-index:10;left:50%;top:960px;width:560px;height:140px;',
      '  transform:translate(-50%,-50%) scale(1);border-radius:20px;opacity:0;',
      '  border:4px solid ' + v.accent + ';}',
      '#chaosCursor{position:absolute;z-index:14;left:940px;top:1720px;width:56px;height:56px;opacity:0;}',
      '#chaosCursor svg{width:56px;height:56px;filter:drop-shadow(0 6px 12px rgba(0,0,0,.7));}',

      /* ---- lockup ---- */
      '#chaosLock{position:absolute;z-index:16;inset:0;display:flex;flex-direction:column;',
      '  align-items:center;justify-content:center;gap:0;opacity:0;}',
      '#chaosLock .mark{width:150px;height:150px;opacity:0;}',
      '#chaosLock .wm{margin-top:34px;text-align:center;opacity:0;}',
      '#chaosLock .wm .a{font-size:40px;font-weight:700;letter-spacing:8px;color:#F3F3F7;}',
      '#chaosLock .wm .b{font-size:40px;font-weight:700;letter-spacing:8px;color:' + v.accent + ';}',
      '#chaosLock .p1{margin-top:96px;font-size:50px;font-weight:400;color:rgba(243,243,247,.80);',
      '  text-align:center;max-width:900px;line-height:1.3;opacity:0;}',
      '#chaosLock .p2{margin-top:20px;font-size:66px;font-weight:700;color:' + v.accent + ';',
      '  text-align:center;max-width:900px;line-height:1.2;opacity:0;',
      '  text-shadow:0 0 40px rgba(255,230,0,.35);}',
      '#chaosLock .rule{margin-top:38px;width:0px;height:5px;border-radius:3px;',
      '  background:linear-gradient(90deg,' + v.accent + ',' + v.accent2 + ');}'
    ].join('\n');
  }

  /* ----------------------------- MOUNT ----------------------------- */
  function mount(hostEl, vars) {
    V = {};
    for (var k in DEFAULTS) { V[k] = DEFAULTS[k]; }
    if (vars) { for (var j in vars) { if (vars[j] !== undefined) V[j] = vars[j]; } }

    var st = document.createElement('style');
    st.id = 'chaos-hook-style';
    st.textContent = css(V);
    document.head.appendChild(st);

    root = document.createElement('div');
    root.id = 'chaosHook';

    var html = '';
    html += '<div class="ch-glow" id="chaosGlow"></div>';
    html += '<div id="chaosField">';
    for (var i = 0; i < V.tileCount; i++) {
      var label = V.tasks[i % V.tasks.length];
      html += '<div class="ch-tile" data-i="' + i + '">' +
              '<span class="d"></span><span class="t"></span>' +
              '<span class="bar"></span><span class="ck"></span></div>';
      void label;
    }
    html += '</div>';
    html += '<div id="chaosCount"><div class="n">+0</div><div class="l"></div><div class="l2"></div></div>';
    html += '<div id="chaosTint"></div><div id="chaosVig"></div><div id="chaosScrim"></div>';
    html += '<div id="chaosRing"></div>';
    html += '<div id="chaosBtn"><span></span></div>';
    html += '<div id="chaosCursor"><svg viewBox="0 0 24 24" fill="#fff" stroke="#0a0a0a" ' +
            'stroke-width="1.1"><path d="M4 2l6 15 2.2-6.2L18.5 8.5 4 2z"/></svg></div>';
    html += '<div id="chaosFlash"></div>';
    html += '<div id="chaosLock">' +
            '<svg class="mark" viewBox="0 0 64 64" fill="none">' +
            '<rect x="3" y="3" width="58" height="58" rx="16" fill="#0c0c0c" stroke="' + V.accent + '" stroke-width="2.5"/>' +
            '<path d="M35 12 L20 36 H31 L27 52 L44 26 H33 Z" fill="' + V.accent + '"/></svg>' +
            '<div class="wm"><span class="a"></span><span class="b"></span></div>' +
            '<div class="p1"></div><div class="p2"></div><div class="rule"></div></div>';
    root.innerHTML = html;
    hostEl.appendChild(root);

    /* text injected as textContent -> accents safe whatever the host does */
    var tiles = root.querySelectorAll('.ch-tile');
    for (var n = 0; n < tiles.length; n++) {
      tiles[n].querySelector('.t').textContent = V.tasks[n % V.tasks.length];
    }
    root.querySelector('#chaosCount .l').textContent = V.counterLabel;
    root.querySelector('#chaosCount .l2').textContent = V.counterDoneLabel;
    root.querySelector('#chaosBtn span').textContent = V.buttonLabel;
    root.querySelector('#chaosLock .wm .a').textContent = V.brandTop;
    root.querySelector('#chaosLock .wm .b').textContent = V.brandBottom;
    root.querySelector('#chaosLock .p1').textContent = V.punchLine1;
    root.querySelector('#chaosLock .p2').textContent = V.punchLine2;

    /* --- layout: the messy pile (start) and the clean grid (end) --- */
    var COLS = 3, TW = 300, TH = 76;
    var gapX = (1080 - COLS * TW) / (COLS + 1);
    for (var m = 0; m < V.tileCount; m++) {
      var col = m % COLS, row = Math.floor(m / COLS);
      var jx = (rnd(m, 1) - 0.5) * 62;
      var jy = (rnd(m, 2) - 0.5) * 26;
      var rot = (rnd(m, 3) - 0.5) * 13;
      var px = gapX + col * (TW + gapX) + jx;
      var py = 1920 - 150 - row * 92 + jy;
      var t = tiles[m];
      t.__pile = { x: px, y: py, r: rot };
      /* clean grid: 8 rows x 3 cols centered, scrollable window of 24 */
      var gcol = m % COLS, grow = Math.floor(m / COLS) % 8;
      t.__grid = { x: gapX + gcol * (TW + gapX), y: 470 + grow * 118, r: 0 };
      gsap.set(t, { x: px, y: py + 240, rotation: rot, scale: 0.82, opacity: 0 });
    }
    return root;
  }

  /* ----------------------------- BUILD ----------------------------- */
  function build(tl, t0) {
    t0 = t0 || 0;
    var tiles = root.querySelectorAll('.ch-tile');
    var N = tiles.length;
    var numEl = root.querySelector('#chaosCount .n');

    /* ============ BEAT 1 : 0.00 -> 2.00  CHAOS ============ */
    tl.to('#chaosCount', { opacity: 1, duration: 0.25 }, t0 + 0.10);
    tl.to('#chaosGlow', { opacity: 1, duration: 1.6, ease: 'power1.in' }, t0 + 0.20);

    for (var i = 0; i < N; i++) {
      /* accelerating spawn: quadratic ease on the schedule itself */
      var f = i / N;
      var at = t0 + 0.05 + 1.86 * Math.pow(f, 0.72);
      var d = 0.20 + rnd(i, 4) * 0.10;
      var p = tiles[i].__pile;
      tl.to(tiles[i], {
        y: p.y, opacity: 1, scale: 1, duration: d, ease: 'power3.out'
      }, at);
    }

    /* counter climbing, frozen mid-flight at 2.00 */
    var steps = 34;
    for (var c = 0; c <= steps; c++) {
      (function (val, tt) {
        tl.call(function () { numEl.textContent = '+' + val; }, null, tt);
      })(Math.round(V.counterTarget * Math.pow(c / steps, 0.85)),
         t0 + 0.18 + 1.74 * (c / steps));
    }
    tl.fromTo('#chaosCount .n', { scale: 1 }, {
      scale: 1.07, duration: 0.22, yoyo: true, repeat: 7, ease: 'power1.inOut'
    }, t0 + 0.20);

    /* rising shake -- ends hard at 1.98, back to zero */
    var sh = 0.14;
    for (var s = 0; s < 26; s++) {
      var st = t0 + 0.20 + s * 0.068;
      var amp = 3 + 15 * (s / 26);
      tl.to('#chaosField', {
        x: (rnd(s, 7) - 0.5) * amp, y: (rnd(s, 8) - 0.5) * amp * 0.6,
        duration: 0.068, ease: 'none'
      }, st);
    }
    void sh;
    tl.to('#chaosField', { x: 0, y: 0, duration: 0.02, ease: 'none' }, t0 + 1.98);

    /* red alert pulses */
    [1.15, 1.52, 1.82].forEach(function (t) {
      tl.to('#chaosGlow', { opacity: 1, duration: 0.07 }, t0 + t);
      tl.to('#chaosGlow', { opacity: 0.55, duration: 0.16 }, t0 + t + 0.07);
    });

    /* ============ BEAT 2 : 2.00 -> 4.00  FREEZE ============ */
    /* Everything slams to a stop. 0.22s of settle, then NOTHING moves
       until 3.80. This silence is the most important beat -- do not fill. */
    tl.to('#chaosFlash', { opacity: 0.58, duration: 0.03, ease: 'none' }, t0 + 2.00);
    tl.to('#chaosFlash', { opacity: 0, duration: 0.11, ease: 'power2.in' }, t0 + 2.03);
    tl.to('#chaosGlow', { opacity: 0, duration: 0.18, ease: 'power2.in' }, t0 + 2.00);
    tl.to('#chaosTint', { opacity: 0.44, duration: 0.20, ease: 'power2.out' }, t0 + 2.00);
    tl.to('#chaosVig', { opacity: 1, duration: 0.22, ease: 'power2.out' }, t0 + 2.00);
    tl.to('#chaosCount .n', {
      color: 'rgba(150,150,158,1)', textShadow: '0 0 0 rgba(0,0,0,0)',
      duration: 0.20, ease: 'power2.out'
    }, t0 + 2.00);
    tl.to('.ch-tile .d', {
      backgroundColor: 'rgba(120,120,128,1)', boxShadow: '0 0 0 rgba(0,0,0,0)',
      duration: 0.20
    }, t0 + 2.00);
    /* --- 2.22 -> 3.80 : dead still. nothing is scheduled here. --- */

    /* ============ BEAT 3 : 4.00 -> 6.00  CURSOR + BUTTON ============ */
    tl.to('#chaosScrim', { opacity: 1, duration: 0.20, ease: 'power2.out' }, t0 + 3.80);
    tl.to('#chaosBtn', {
      opacity: 1, scale: 1, duration: 0.34, ease: 'back.out(1.9)'
    }, t0 + 4.00);
    tl.to('#chaosBtn', {
      boxShadow: '0 0 70px rgba(255,230,0,.45),0 22px 60px rgba(0,0,0,.6)',
      duration: 0.5, ease: 'power2.out'
    }, t0 + 4.20);

    tl.set('#chaosCursor', { left: 950, top: 1740 }, t0 + 4.30);
    tl.to('#chaosCursor', { opacity: 1, duration: 0.18 }, t0 + 4.35);
    tl.to('#chaosCursor', {
      left: 596, top: 992, duration: 0.86, ease: 'power2.inOut'
    }, t0 + 4.55);
    /* click */
    tl.to('#chaosCursor', { left: 590, top: 998, duration: 0.09, ease: 'power2.in' }, t0 + 5.36);
    tl.to('#chaosBtn', { scale: 0.93, duration: 0.09, ease: 'power2.in' }, t0 + 5.40);
    tl.to('#chaosBtn', { scale: 1, duration: 0.30, ease: 'back.out(3)' }, t0 + 5.49);
    /* immediateRender:false -> sinon la bague est visible des t=0 */
    tl.fromTo('#chaosRing', { opacity: 0.95, scale: 1 }, {
      opacity: 0, scale: 2.1, duration: 0.62, ease: 'power2.out', immediateRender: false
    }, t0 + 5.42);
    tl.to('#chaosCursor', { opacity: 0, duration: 0.16 }, t0 + 5.66);
    tl.to('#chaosBtn', { opacity: 0, scale: 1.14, duration: 0.26, ease: 'power2.in' }, t0 + 5.80);
    tl.to('#chaosScrim', { opacity: 0, duration: 0.28 }, t0 + 5.86);
    tl.to('#chaosTint', { opacity: 0.10, duration: 0.30 }, t0 + 5.86);
    tl.to('#chaosVig', { opacity: 0.42, duration: 0.30 }, t0 + 5.86);

    /* ============ BEAT 4 : 6.00 -> 8.00  EXECUTION ============ */
    /* every task snaps to a clean grid AT ONCE, then completes */
    for (var g = 0; g < N; g++) {
      var gg = tiles[g].__grid;
      var vis = (g < 24);
      tl.to(tiles[g], {
        x: gg.x, y: gg.y, rotation: 0, scale: 1,
        opacity: vis ? 1 : 0,
        duration: 0.46, ease: 'power3.out'
      }, t0 + 6.00);
    }
    tl.to('.ch-tile', {
      borderColor: 'rgba(255,230,0,.42)', backgroundColor: '#141418',
      duration: 0.30
    }, t0 + 6.02);
    /* progress bars + checks cascade -- the "all at once" wave */
    tl.to('.ch-tile .bar', {
      width: '100%', duration: 0.42, ease: 'power2.inOut', stagger: 0.012
    }, t0 + 6.44);
    tl.to('.ch-tile .d', {
      backgroundColor: V.ok, boxShadow: '0 0 12px ' + V.ok,
      duration: 0.20, stagger: 0.012
    }, t0 + 6.52);
    tl.to('.ch-tile .ck', {
      opacity: 1, scale: 1, duration: 0.22, ease: 'back.out(2.4)', stagger: 0.012
    }, t0 + 6.70);

    /* counter flips to executed */
    tl.call(function () { numEl.textContent = String(V.counterTarget); }, null, t0 + 6.60);
    tl.to('#chaosCount .n', {
      color: V.ok, textShadow: '0 0 40px rgba(61,255,158,.5)', scale: 1.12,
      duration: 0.26, ease: 'back.out(2)'
    }, t0 + 6.60);
    tl.to('#chaosCount .n', { scale: 1, duration: 0.24 }, t0 + 6.86);
    tl.to('#chaosCount .l', { opacity: 0, duration: 0.18 }, t0 + 6.60);
    tl.to('#chaosCount .l2', { opacity: 1, duration: 0.24 }, t0 + 6.72);

    /* clear out */
    for (var h = 0; h < N; h++) {
      if (h >= 24) continue;
      tl.to(tiles[h], {
        y: '-=70', opacity: 0, scale: 0.9, duration: 0.34, ease: 'power2.in'
      }, t0 + 7.38 + (h % 24) * 0.014);
    }
    tl.to('#chaosCount', { opacity: 0, duration: 0.26, ease: 'power2.in' }, t0 + 7.62);
    tl.to('#chaosVig', { opacity: 0.85, duration: 0.4 }, t0 + 7.60);
    tl.to('#chaosTint', { opacity: 0.5, duration: 0.4 }, t0 + 7.60);

    /* ============ BEAT 5 : 8.00 -> 10.00  LOCKUP ============ */
    tl.set('#chaosLock', { opacity: 1 }, t0 + 7.98);
    tl.fromTo('#chaosLock .mark', { opacity: 0, scale: 0.4 }, {
      opacity: 1, scale: 1, duration: 0.42, ease: 'back.out(2.2)'
    }, t0 + 8.04);
    tl.fromTo('#chaosLock .wm', { opacity: 0, y: 18 }, {
      opacity: 1, y: 0, duration: 0.34, ease: 'power3.out'
    }, t0 + 8.30);
    tl.fromTo('#chaosLock .p1', { opacity: 0, y: 22 }, {
      opacity: 1, y: 0, duration: 0.36, ease: 'power3.out'
    }, t0 + 8.62);
    tl.fromTo('#chaosLock .p2', { opacity: 0, y: 26, scale: 0.94 }, {
      opacity: 1, y: 0, scale: 1, duration: 0.40, ease: 'back.out(1.7)'
    }, t0 + 8.98);
    tl.to('#chaosLock .rule', { width: 320, duration: 0.44, ease: 'power3.out' }, t0 + 9.26);
    tl.to('#chaosLock .p2', {
      textShadow: '0 0 90px rgba(255,230,0,.75)', duration: 0.32, yoyo: true, repeat: 3
    }, t0 + 9.30);

    if (V.autoHide) {
      tl.to('#chaosHook', { opacity: 0, duration: 0.22, ease: 'power2.in' }, t0 + DUR - 0.22);
      tl.set('#chaosHook', { display: 'none' }, t0 + DUR + 0.01);
    }
    return t0 + DUR;
  }

  global.ChaosHook = {
    DURATION: DUR,
    DEFAULTS: DEFAULTS,
    mount: mount,
    build: build
  };
})(window);

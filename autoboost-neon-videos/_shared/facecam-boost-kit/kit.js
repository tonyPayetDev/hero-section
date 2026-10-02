/* FaceCam Boost kit - motion helpers for HyperFrames compositions.
 *
 * Every helper adds tweens to the composition's single paused GSAP timeline.
 * Contract kept everywhere: fromTo with immediateRender:false (the authored CSS
 * holds the "before" state), times quantized to the frame, finite repeats only,
 * no Math.random / Date.now (particles use a seeded PRNG).
 *
 * The motion vocabulary is adapted from "8 animations motion design" (CERËGA /
 * SKOOL) - never linear, timings in seconds, one idea per animation - but drawn
 * in the AutomatisationBoost charter instead of their blue / red on off-white.
 */
(function () {
  var FPS = 30;
  function q(t) { return Math.round(t * FPS) / FPS; }
  function ft(tl, target, from, to, t) {
    to.immediateRender = false;
    tl.fromTo(target, from, to, q(t));
  }
  function el(sel) { return typeof sel === "string" ? document.querySelector(sel) : sel; }

  var FB = {
    q: q,

    /* Punch badge slam: oversize + tilted -> lands on its resting tilt. */
    sticker: function (tl, sel, tin, tout, rot) {
      rot = rot == null ? -4 : rot;
      ft(tl, sel, { opacity: 0, scale: 2.1, rotation: rot - 10 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.34, ease: "back.out(2.2)" }, tin);
      if (el(sel + " .fb-spark")) ft(tl, sel + " .fb-spark", { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.26, ease: "back.out(3)" }, tin + 0.2);
      if (tout != null) ft(tl, sel, { opacity: 1, scale: 1 }, { opacity: 0, scale: 0.6, duration: 0.22, ease: "power2.in" }, tout);
    },

    /* Level chip: slides in, the newly reached segment fills. */
    level: function (tl, sel, tin, tout) {
      ft(tl, sel, { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, tin);
      if (el(sel + " .seg i.new")) ft(tl, sel + " .seg i.new", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out", transformOrigin: "0% 50%" }, tin + 0.3);
      if (tout != null) ft(tl, sel, { opacity: 1 }, { opacity: 0, duration: 0.2, ease: "power2.in" }, tout);
    },

    /* Notion #3 - progression curve: line draws, area fills, dot bounces, label pops. */
    chart: function (tl, root, t, d) {
      d = d || 1.2;
      var line = el(root + " .fb-line");
      if (line) {
        var L = line.getTotalLength();
        ft(tl, line, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: d, ease: "power2.inOut" }, t);
      }
      ft(tl, root + " .fb-area", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.out" }, t + d * 0.75);
      ft(tl, root + " .fb-dot", { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(3)", transformOrigin: "50% 50%" }, t + d);
      ft(tl, root + " .fb-label", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, t + d + 0.15);
    },

    /* Typewriter on .char spans (Notion #2 search bar, comment box). */
    type: function (tl, sel, t, step) {
      ft(tl, sel + " .char", { opacity: 0 }, { opacity: 1, duration: 0.04, stagger: step || 0.07, ease: "none" }, t);
    },

    /* Notion #2 - results slide up one after another, 0.13 s apart. */
    results: function (tl, sel, t) {
      ft(tl, sel, { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out", stagger: 0.13 }, t);
    },

    /* Notion #5 - card pile: the top card flies off left and spins, the next one steps forward. */
    stackFly: function (tl, topSel, t, nextSel, from) {
      ft(tl, topSel, { x: 0, rotation: 0, opacity: 1 }, { x: -1200, rotation: -32, opacity: 0, duration: 0.55, ease: "power3.in" }, t);
      if (nextSel) ft(tl, nextSel, { y: from.y, rotation: from.r, scale: from.s }, { y: 0, rotation: 0, scale: 1, duration: 0.5, ease: "back.out(1.4)" }, t + 0.28);
    },

    /* Notion #1 - button press (1 -> 0.92 -> 1) before it opens into a panel. */
    press: function (tl, sel, t) {
      ft(tl, sel, { scale: 1 }, { scale: 0.92, duration: 0.12, ease: "power2.in" }, t);
      ft(tl, sel, { scale: 0.92 }, { scale: 1, duration: 0.22, ease: "back.out(3)" }, t + 0.12);
    },

    /* Notion #7 - elastic word: each letter stretches then squashes, a wave left to right. */
    elastic: function (tl, sel, t, dur) {
      var chars = document.querySelectorAll(sel + " .fb-ech");
      var cyc = 0.32;
      var reps = Math.max(0, Math.floor((dur - chars.length * 0.08) / (cyc * 2)) - 1);
      for (var i = 0; i < chars.length; i++) {
        tl.fromTo(chars[i], { scaleY: 1, scaleX: 1 },
          { scaleY: 1.38, scaleX: 0.82, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: reps * 2 + 1, immediateRender: false },
          q(t + i * 0.08));
      }
    },

    /* Notion #6 - dock: a cursor sweeps, the nearest icon swells to 1.8x, neighbours less. */
    dock: function (tl, root, t, d, x0, x1) {
      var icons = document.querySelectorAll(root + " .fb-di");
      var cur = el(root + " .fb-cursor");
      var o = { x: x0 };
      function upd() {
        for (var i = 0; i < icons.length; i++) {
          var c = icons[i].offsetLeft + icons[i].offsetWidth / 2;
          var s = 1 + 0.8 * Math.max(0, 1 - Math.abs(o.x - c) / 200);
          icons[i].style.transform = "scale(" + s.toFixed(3) + ")";
        }
        if (cur) cur.style.transform = "translateX(" + o.x.toFixed(1) + "px)";
      }
      tl.fromTo(o, { x: x0 }, { x: x1, duration: d, ease: "sine.inOut", immediateRender: false, onUpdate: upd }, q(t));
    },

    /* Notion #4 - a dashboard tile zooms to fill its frame. dx/dy/s computed by the caller. */
    tileZoom: function (tl, sel, t, dx, dy, s, d) {
      ft(tl, sel, { x: 0, y: 0, scale: 1 }, { x: dx, y: dy, scale: s, duration: d || 0.6, ease: "power3.inOut" }, t);
    },

    /* Notion #8 - particles gather into a word, hold, scatter. Seeded, sampled lazily
       on first draw so the web font is already loaded. Bottom rows turn violet. */
    particles: function (tl, canvasSel, text, t, opts) {
      var cv = el(canvasSel);
      if (!cv) return;
      var ctx = cv.getContext("2d"), W = cv.width, H = cv.height, pts = null, seed = opts.seed || 7;
      function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
      function build() {
        var off = document.createElement("canvas"); off.width = W; off.height = H;
        var c = off.getContext("2d");
        c.fillStyle = "#fff"; c.font = opts.font; c.textAlign = "center"; c.textBaseline = "middle";
        c.fillText(text, W / 2, H / 2);
        var data = c.getImageData(0, 0, W, H).data, step = opts.step || 8, tg = [];
        for (var y = 0; y < H; y += step) for (var x = 0; x < W; x += step)
          if (data[(y * W + x) * 4 + 3] > 128) tg.push([x, y]);
        var ys = tg.map(function (p) { return p[1]; }), ymin = Math.min.apply(null, ys), ymax = Math.max.apply(null, ys);
        pts = tg.map(function (p) {
          return { tx: p[0], ty: p[1], sx: rnd() * W, sy: rnd() * H, low: (p[1] - ymin) / Math.max(1, ymax - ymin) > 0.72 };
        });
      }
      var o = { p: 0 };
      function draw() {
        if (!pts) build();
        ctx.clearRect(0, 0, W, H);
        for (var i = 0; i < pts.length; i++) {
          var a = pts[i], e = o.p;
          ctx.fillStyle = a.low ? "#8b5cf6" : "#eab308";
          ctx.beginPath();
          ctx.arc(a.sx + (a.tx - a.sx) * e, a.sy + (a.ty - a.sy) * e, opts.r || 2.8, 0, 6.2832);
          ctx.fill();
        }
      }
      tl.fromTo(o, { p: 0 }, { p: 1, duration: opts.dIn || 1, ease: "power3.inOut", immediateRender: false, onUpdate: draw }, q(t));
      if (opts.tOut != null)
        tl.fromTo(o, { p: 1 }, { p: 0, duration: opts.dOut || 0.8, ease: "power2.in", immediateRender: false, onUpdate: draw }, q(opts.tOut));
    },

    /* Facecam morph between two modes produced by kit.py facecam_mode(). */
    morph: function (tl, sel, a, b, t, d) {
      ft(tl, sel, { x: a.x, y: a.y, scale: a.scale, clipPath: a.clip },
        { x: b.x, y: b.y, scale: b.scale, clipPath: b.clip, duration: d || 0.5, ease: "power3.inOut" }, t);
    },
  };
  window.FB = FB;
})();

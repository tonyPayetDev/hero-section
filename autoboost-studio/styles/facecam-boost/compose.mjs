// Style « FaceCam Boost » (port of autoboost-74 motion v2, 9:16 only, the whole camera picture, no cutout).
// Each screen picks a camera layout: hook full screen, then neon circle / stacked rectangle / vertical split
// (for avant-maintenant), big circle for the CTA. Screens slide in from the right in the top zone.
import { kwSize, camMode, camTag, captions, chars, elastic, esc, headParts, icon, levelChips, q, sticker, timeline, wordsText, writeComposition } from "../../lib/kit.mjs";

export default function compose(scenes, words, opts) {
  const W = 1080, H = 1920;
  const tl = timeline();
  const { R, S, up, pop, kin, fb, sfx } = tl;
  const total = opts.total;

  // ---------------------------------------------------------------- camera layouts
  const src = [opts.camW, opts.camH];
  const face = [opts.camW / 2, opts.camH * 0.36];
  // how tight each shape frames the face: 1 = the whole width of the take, smaller = closer (0.88 keeps the shoulders)
  const ZOOM = { circle: 0.88, big: 0.92, rect: 1, split: 1 };
  const crop = (box, z) => Math.min(opts.camH, opts.camW / (box[2] / box[3])) * z;
  const B = { circle: [220, 1100, 640, 640], big: [160, 980, 760, 760], rect: [24, 1000, 1032, 920], split: [24, 420, 500, 1290] };
  const L = {
    full: camMode([0, 0, W, H], face, src),
    circle: camMode(B.circle, face, src, crop(B.circle, ZOOM.circle), 320),
    big: camMode(B.big, face, src, crop(B.big, ZOOM.big), 380),
    rect: camMode(B.rect, face, src, crop(B.rect, ZOOM.rect), 34),
    split: camMode(B.split, face, src, crop(B.split, ZOOM.split), 30),
  };
  let alt = 0;
  const layoutOf = (sc) => {
    if (sc.hook) return "full";
    if (sc.type === "cta") return "big";
    if (sc.type === "contrast") return "split";
    if (["list", "tools", "steps"].includes(sc.type)) return "rect";
    return (alt++ % 2) ? "rect" : "circle";
  };
  const lay = scenes.map(layoutOf);
  const camSet = (m) => ({ x: m.x, y: m.y, scale: m.scale, clipPath: m.clipPath });
  S("#cam", 0, { ...camSet(L[lay[0] || "full"]), transformOrigin: "0px 0px" });
  R("#cam", 0, { scale: L.full.scale * 1.12 }, { scale: L.full.scale }, 0.35, "expo.out");
  for (let i = 1; i < scenes.length; i++) {
    if (lay[i] === lay[i - 1]) continue;
    R("#cam", scenes[i].a - 0.25, camSet(L[lay[i - 1]]), camSet(L[lay[i]]), 0.5, "power3.inOut");
  }
  // chrome around each layout
  const spans = [];
  lay.forEach((l, i) => {
    const a = scenes[i].a, b = scenes[i].b;
    const last = spans[spans.length - 1];
    if (last && last.l === l) last.b = b; else spans.push({ l, a, b });
  });
  for (const s of spans) {
    const t0 = s.a + 0.25, t1 = s.b - 0.2;
    if (s.l === "circle" || s.l === "big") {
      S("#ring", t0, s.l === "big" ? { y: -60, scale: 1.1875 } : { y: 0, scale: 1 });
      R("#ring", t0, { opacity: 0 }, { opacity: 1 }, 0.4, "back.out(1.6)");
      R("#ring-main", t0, { strokeDashoffset: 2100 }, { strokeDashoffset: 0 }, 0.7, "power2.inOut");
      if (s.b < total - 0.1) R("#ring", t1, { opacity: 1 }, { opacity: 0 }, 0.25, "power2.in");
    } else if (s.l === "rect") {
      R("#rect-line,#rect-frame", t0, { opacity: 0 }, { opacity: 1 }, 0.35, "power2.out");
      R("#rect-line,#rect-frame", t1, { opacity: 1 }, { opacity: 0 }, 0.25, "power2.in");
    } else if (s.l === "split") {
      R("#split-frame", t0, { opacity: 0 }, { opacity: 1 }, 0.35, "power2.out");
      R("#split-frame", t1, { opacity: 1 }, { opacity: 0 }, 0.25, "power2.in");
    }
  }
  R("#bg-curve", 0.4, { strokeDashoffset: 2600 }, { strokeDashoffset: 0 }, 2.2, "power2.inOut");
  R("#flash", 0.12, { opacity: 0.35 }, { opacity: 0 }, 0.22, "power2.out");

  // ---------------------------------------------------------------- screens
  const sceneHTML = [], overlays = [];
  // the metal gradients are background-clip:text, so they go on every letter (a parent's gradient skips inline-blocks)
  const head2 = (pre, hi, cls = "g") => `<div class="hd">${pre ? `<div class="l1"><span class="p">${chars(pre, "w")}</span></div>` : ""}`
    + `<div class="l2"><span class="h">${chars(hi, cls)}</span></div></div>`;
  let side = 0;

  scenes.forEach((sc, i) => {
    const id = `s${i}`, a = sc.a, b = sc.b;
    const { pre, hi, hiAt } = headParts(sc);
    let inner = "", outer = "";
    const revealHead = (t0) => { kin(`#${id} .p`, t0, 0.02); kin(`#${id} .h`, hiAt, 0.03); };
    switch (sc.type) {
      case "cta": {
        const kw = sc.data.keyword;
        inner = `<div class="cta"><div class="a">${chars("COMMENTE", "w")}</div><div class="b" style="font-size:${kwSize(kw, 190, 900)}px">${elastic(kw)}</div>`
          + `<div class="cfield"><span class="pre">commente</span><span class="kw">${chars(kw)}</span><i class="snd">${icon("send", 40)}</i></div></div>`;
        kin(`#${id} .cta .a`, Math.max(a, sc.data.at - 0.6), 0.025);
        S(`#${id} .cta .b`, 0, { opacity: 0 });
        R(`#${id} .cta .b`, sc.data.at, { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1 }, 0.25, "power4.in");
        fb(`elastic(tl,"#${id} .cta .b",${q(sc.data.at + 0.35)},${q(Math.max(0.8, b - sc.data.at - 0.5))})`);
        up(`#${id} .cfield`, a + 0.1, 0.3, 30);
        fb(`type(tl,"#${id} .kw",${q(sc.data.at)},0.07)`);
        pop(`#${id} .snd`, sc.data.at + 0.45);
        sfx(sc.data.at, "sfx-impact-deep.mp3", -15); sfx(sc.data.at + 0.6, "sfx-notify.mp3", -19);
        break;
      }
      case "stat": {
        const val = sc.data.value, isInt = /^\d+$/.test(val);
        inner = `<div class="statc card"><div><span class="num g">${isInt ? "0" : esc(val)}</span><span class="unit v">${esc(sc.data.unit)}</span></div>`
          + `<div class="lab">${chars(wordsText(sc.data.label))}</div></div>`;
        up(`#${id} .statc`, a, 0.35, 50);
        if (isInt) tl.count(`#${id} .num`, sc.data.at, parseInt(val, 10));
        R(`#${id} .statc .num`, sc.data.at, { scale: 1.3 }, { scale: 1 }, 0.35, "back.out(2)");
        kin(`#${id} .lab`, sc.data.at + 0.2);
        sfx(sc.data.at, "sfx-impact.mp3", -18);
        break;
      }
      case "tools": {
        const tools = sc.data.tools;
        inner = head2(pre, hi) + `<div class="flow">` + tools.map((t, j) => (j ? `<div class="link l${j}"></div>` : "")
          + `<div class="node card n${j}"><div class="ic">${esc(t.name.slice(0, 2))}</div><b>${esc(t.name)}</b></div>`).join("") + "</div>";
        revealHead(sc.start);
        tools.forEach((t, j) => {
          R(`#${id} .n${j}`, t.at, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1 }, 0.28, "back.out(2.4)");
          if (j) R(`#${id} .l${j}`, t.at - 0.12, { scaleX: 0 }, { scaleX: 1 }, 0.15);
          sfx(t.at, "sfx-pop.mp3", -21);
        });
        break;
      }
      case "list": {
        const items = sc.data.items.slice(0, 6);
        inner = `<div class="tiles">` + items.map((it, j) =>
          `<div class="tile card t${j}"><i class="ic">${icon("check", 30)}</i><span>${esc(it.label.split(" ").slice(-3).join(" "))}</span></div>`).join("") + "</div>";
        items.forEach((it, j) => {
          R(`#${id} .t${j}`, it.at, { opacity: 0, y: 60 }, { opacity: 1, y: 0 }, 0.4, "power3.out");
          R(`#${id} .t${j} .ic`, it.at + 0.15, { backgroundColor: "rgba(139,92,246,.18)", color: "#a78bfa" }, { backgroundColor: "#eab308", color: "#0a0a0f" }, 0.2);
          sfx(it.at, "sfx-click.mp3", -22);
        });
        break;
      }
      case "steps": {
        inner = `<div class="center"><span class="pill gold stepn">ÉTAPE ${sc.data.n}</span></div>` + head2(pre, hi);
        pop(`#${id} .stepn`, sc.start);
        revealHead(sc.start + 0.1);
        sfx(sc.start, "sfx-pop.mp3", -20);
        break;
      }
      case "contrast": {
        inner = head2(pre, hi);
        outer = `<div class="colr"><div class="vc card bad"><small>AVANT</small><b>${esc(wordsText(sc.data.left))}</b><span class="stamp">FINI</span></div>`
          + `<div class="vc card good"><small>MAINTENANT</small><b>${esc(wordsText(sc.data.right))}</b></div></div>`;
        revealHead(sc.start);
        up(`#${id} .bad`, sc.start, 0.35, 40);
        R(`#${id} .stamp`, sc.data.at - 0.1, { opacity: 0, scale: 2.2, rotation: -18 }, { opacity: 1, scale: 1, rotation: -8 }, 0.3, "power4.in");
        up(`#${id} .good`, sc.data.at, 0.35, 40);
        R("#knob", a + 0.3, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1 }, 0.35, "back.out(2.4)");
        R("#knob", b - 0.2, { opacity: 1 }, { opacity: 0 }, 0.2, "power2.in");
        sfx(sc.data.at - 0.1, "sfx-impact.mp3", -20); sfx(sc.data.at, "sfx-confirm.mp3", -20);
        break;
      }
      default: {   // headline, question, hook
        inner = head2(pre, hi, sc.type === "question" ? "v" : "g");
        revealHead(sc.hook ? 0 : sc.start);
        sfx(hiAt, "sfx-pop.mp3", -22);
      }
    }
    const solo = !sc.hook && ["headline", "question", "steps"].includes(sc.type);   // a title alone: centred, bigger
    const cls = `screen clip${sc.hook ? " hook" : ""}${lay[i] === "split" ? " split" : ""}`;
    sceneHTML.push(`<section id="${id}" class="${cls}" data-start="${q(Math.max(0, a - 0.3))}" data-duration="${q(Math.min(total, b + 0.3) - Math.max(0, a - 0.3))}" `
      + `data-track-index="${2 + (i % 2)}">${sc.hook ? '<div class="shade"></div>' : ""}<div class="in${solo ? " solo" : ""}">${inner}</div>${outer}</section>`);
    if (i > 0) {
      R(`#${id} .in`, a - 0.12, { opacity: 0, x: 1080 }, { opacity: 1, x: 0 }, 0.42, "power3.out");
      R("#streak", a - 0.12, { opacity: 1, x: 0 }, { opacity: 0, x: -500 }, 0.4, "power2.out");
      sfx(a - 0.12, "sfx-whoosh-lat.mp3", -22);
    }
    if (i < scenes.length - 1) R(`#${id} .in`, b - 0.2, { opacity: 1, x: 0 }, { opacity: 0, x: -1080 }, 0.3, "power2.in");
    if (sc.sticker) {
      const st = sc.sticker, sid = `st${i}`;
      side = 1 - side;
      overlays.push(sticker(sid, st.a, st.b, st.v, st.ico, side ? 40 : 600, 880));
      fb(`sticker(tl,"#${sid}",${q(st.at)},${q(Math.min(b - 0.15, st.at + 2.6))},${side ? -5 : 4})`);
      sfx(st.at, "sfx-thwip.mp3", -21);
    }
  });
  sfx(0, "sfx-impact-deep.mp3", -17);

  const levels = levelChips(scenes, tl, total);
  const cap = captions(words, { x: W / 2, y: 1790, pill: false, charW: 31, pad: 40, pop: true });
  if (opts.bpm) {              // the ring breathes on the music
    const beat = 60 / opts.bpm;
    for (let t = 0.5; t < total - 0.3; t += beat * 2) R("#ring .halo", t, { opacity: 1 }, { opacity: 0.6 }, Math.min(0.5, beat * 1.6), "power2.out");
  }
  S("#flash", total - 0.5, { backgroundColor: "#0a0a0f" });
  R("#flash", total - 0.5, { opacity: 0 }, { opacity: 1 }, 0.45, "power2.in");

  writeComposition(opts.styleDir, opts.out, {
    TOTAL: q(total), CAMW: opts.camW, CAMH: opts.camH, CAM: camTag(opts), LEVELS: levels, SCENES: sceneHTML.join("\n"),
    CAPTIONS: cap.html, OVERLAYS: overlays.join("\n"), JS: [...tl.js, ...cap.js].join("\n"),
  });
  return { events: tl.ev, W, H };
}

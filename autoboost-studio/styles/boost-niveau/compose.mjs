// Style « boost niveau » : light cards with a neon border, NIVEAU 1 -> MAX chip, caption pill, camera in a
// framed box under the cards (or the matted cutout), neon tubes breathing on the beat.
import { kwSize, camMode, camTag, captions, chars, elastic, esc, headParts, icon, levelChips, q, sticker, timeline, wordsText, writeComposition } from "../../lib/kit.mjs";

export default function compose(scenes, words, opts) {
  const V = opts.format === "16:9";
  const W = V ? 1920 : 1080, H = V ? 1080 : 1920;
  const tl = timeline();
  const { R, S, up, pop, kin, hl, fb, sfx } = tl;
  const total = opts.total;
  const flash = (t, op = 0.4, d = 0.22) => R("#flash", t, { opacity: op }, { opacity: 0 }, d, "power2.out");

  // ---------------------------------------------------------------- camera
  const src = [opts.camW, opts.camH];
  const focus = [opts.camW / 2, opts.camH * 0.38];
  if (opts.cutout) {
    const s = V ? (H * 1.05) / opts.camH : (W * 0.94) / opts.camW;
    const x = V ? 1525 - (opts.camW * s) / 2 : (W - opts.camW * s) / 2;
    const y = H - opts.camH * s + (V ? 30 : 40);
    S("#camw", 0, { x, y, scale: s, transformOrigin: "0px 0px" });
    R("#camw", 0, { scale: s * 1.22, x: x - (opts.camW * s * 0.11), y: y + 60 }, { scale: s, x, y }, 0.32, "expo.out");
    let z = false;                       // punch-in on every cut of the take: hides the jump cuts
    for (const c of (opts.cuts || []).slice(1)) {
      z = !z;
      const zs = z ? s * 1.06 : s;
      S("#camw", c, { scale: zs, x: x - (opts.camW * (zs - s)) / 2, y: y - (opts.camH * (zs - s)) * 0.3 });
    }
  } else {
    const M = V
      ? { full: camMode([0, 0, W, H], focus, src), main: camMode([1295, 225, 460, 460], focus, src, opts.camH * 0.62, 230) }
      : { full: camMode([0, 0, W, H], focus, src), main: camMode([24, 790, 1032, 1106], focus, src, null, 34) };
    S("#cam", 0, { ...M.full, transformOrigin: "0px 0px" });
    const firstB = scenes[0]?.b ?? 3;
    R("#cam", firstB - 0.25, M.full, M.main, 0.5, "power3.inOut");
    R("#camframe", firstB + 0.2, { opacity: 0 }, { opacity: 1 }, 0.3);
    const cta = scenes.find((s) => s.type === "cta");
    if (cta && !V) {
      R("#cam", cta.a - 0.25, M.main, M.full, 0.5, "power3.inOut");
      R("#camframe", cta.a - 0.25, { opacity: 1 }, { opacity: 0 }, 0.2);
    }
    R("#cam", 0, { scale: M.full.scale * 1.15 }, { scale: M.full.scale }, 0.35, "expo.out");
  }
  flash(0.12, 0.35, 0.22);

  // ---------------------------------------------------------------- scenes
  const Z = V ? { x: 110, y: 140, w: 1080 } : { x: 46, y: 110, w: 988 };
  const sceneHTML = [], overlays = [];
  const brand = esc(opts.brand || "AUTOMATISATIONBOOST");
  const bsplit = brand.length > 6 ? [brand.slice(0, -5), brand.slice(-5)] : [brand, ""];
  const lbar = `<div class="lbar"><span>${bsplit[0]}<b>${bsplit[1]}</b></span><i class="d1"></i><i class="d2"></i><i class="d3"></i></div>`;
  let stickSide = 0;

  scenes.forEach((sc, i) => {
    const id = `s${i}`, a = sc.a, b = sc.b;
    const { pre, hi, hiAt } = headParts(sc);
    let inner = "";
    switch (sc.type) {
      case "cta": {
        const kw = sc.data.keyword;
        inner = `<div class="cta"><div class="a">${chars("COMMENTE")}</div><div class="b" style="font-size:${kwSize(kw, 210, V ? 1000 : 960)}px">${elastic(kw)}</div>`
          + `<div class="cfield"><span class="pre">commente</span><span class="kw">${chars(kw)}</span><i class="snd">${icon("send", 40)}</i></div>`
          + `<div class="sub">→ je te réponds en <b>DM</b></div></div>`;
        kin(`#${id} .cta .a`, Math.max(a, sc.data.at - 0.6), 0.025);
        R(`#${id} .cta .b`, sc.data.at, { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1 }, 0.25, "power4.in");
        S(`#${id} .cta .b`, 0, { opacity: 0 });
        fb(`elastic(tl,"#${id} .cta .b",${q(sc.data.at + 0.35)},${q(Math.max(0.8, b - sc.data.at - 0.5))})`);
        up(`#${id} .cfield`, a + 0.1, 0.3, 30);
        fb(`type(tl,"#${id} .kw",${q(sc.data.at)},0.07)`);
        pop(`#${id} .snd`, sc.data.at + 0.45);
        up(`#${id} .sub`, sc.data.at + 0.6, 0.25, 20);
        sfx(sc.data.at, "sfx-impact-deep.mp3", -15); sfx(sc.data.at + 0.05, "sfx-click-soft.mp3", -20); sfx(sc.data.at + 0.6, "sfx-notify.mp3", -19);
        break;
      }
      case "stat": {
        const val = sc.data.value, isInt = /^\d+$/.test(val);
        inner = `<div class="lcard">${lbar}<div class="stat"><span class="num" data-v="${esc(val)}">${isInt ? "0" : esc(val)}</span>`
          + `<span class="unit">${esc(sc.data.unit)}</span></div><div class="t2">${chars(wordsText(sc.data.label))}</div></div>`;
        up(`#${id} .lcard`, a, 0.3, 50);
        if (isInt) tl.count(`#${id} .num`, sc.data.at, parseInt(val, 10));
        R(`#${id} .stat`, sc.data.at, { scale: 1.25 }, { scale: 1 }, 0.35, "back.out(2)");
        kin(`#${id} .t2`, sc.data.at + 0.2);
        sfx(sc.data.at, "sfx-impact.mp3", -18);
        break;
      }
      case "tools": {
        const tools = sc.data.tools;
        inner = `<div class="lcard">${lbar}<div class="t1"><span class="p">${chars(pre)}</span> <span class="hl">${chars(hi)}</span></div><div class="chain">`
          + tools.map((t, k) => (k ? `<div class="arr r${k}"></div>` : "") + `<div class="app a${k}"><div class="tile">${esc(t.name.slice(0, 2))}</div><b>${esc(t.name)}</b></div>`).join("")
          + "</div></div>";
        up(`#${id} .lcard`, a, 0.3, 50);
        kin(`#${id} .p`, sc.start); kin(`#${id} .hl`, hiAt, 0.03); hl(`#${id} .hl`, hiAt + 0.1);
        tools.forEach((t, k) => {
          R(`#${id} .a${k}`, t.at, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1 }, 0.25, "back.out(2.5)");
          if (k) R(`#${id} .r${k}`, t.at - 0.12, { scaleX: 0 }, { scaleX: 1 }, 0.15);
          sfx(t.at, "sfx-pop.mp3", -21);
        });
        break;
      }
      case "list": {
        const items = sc.data.items;
        inner = `<div class="lcard">${lbar}<div class="chips">` + items.map((it, k) =>
          `<div class="chip c${k}"><i>${icon("check", 26)}</i><span>${esc(it.label.split(" ").slice(-3).join(" "))}</span></div>`).join("") + "</div></div>";
        up(`#${id} .lcard`, a, 0.3, 50);
        items.forEach((it, k) => {
          R(`#${id} .c${k}`, it.at, { opacity: 0, x: 40 }, { opacity: 1, x: 0 }, 0.25, "back.out(2)");
          R(`#${id} .c${k} i`, it.at + 0.12, { backgroundColor: "#262236", color: "#8A8A8A" }, { backgroundColor: "#eab308", color: "#0a0a0f" }, 0.2);
          sfx(it.at, "sfx-click.mp3", -22);
        });
        break;
      }
      case "contrast": {
        inner = `<div class="lcard">${lbar}<div class="duo"><div class="side bad"><small>AVANT</small><b>${esc(wordsText(sc.data.left))}</b>`
          + `<svg class="x" width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M6 10 L94 90 M94 10 L6 90"/></svg></div>`
          + `<div class="side good"><small>MAINTENANT</small><b>${esc(wordsText(sc.data.right))}</b></div></div></div>`;
        up(`#${id} .lcard`, a, 0.3, 50);
        up(`#${id} .bad`, sc.start, 0.28, 30);
        R(`#${id} .bad path`, sc.data.at - 0.15, { strokeDashoffset: 300 }, { strokeDashoffset: 0 }, 0.25);
        R(`#${id} .bad`, sc.data.at, { opacity: 1 }, { opacity: 0.5 }, 0.25);
        up(`#${id} .good`, sc.data.at, 0.28, 30);
        sfx(sc.data.at - 0.15, "sfx-glitch-soft.mp3", -21); sfx(sc.data.at, "sfx-confirm.mp3", -20);
        break;
      }
      case "steps": {
        inner = `<div class="lcard">${lbar}<div class="stepn"><span>ÉTAPE</span><b>${sc.data.n}</b></div>`
          + `<div class="t1"><span class="p">${chars(pre)}</span> <span class="hl">${chars(hi)}</span></div></div>`;
        up(`#${id} .lcard`, a, 0.3, 50);
        pop(`#${id} .stepn`, sc.start);
        kin(`#${id} .p`, sc.start + 0.1); kin(`#${id} .hl`, hiAt, 0.03); hl(`#${id} .hl`, hiAt + 0.1);
        sfx(sc.start, "sfx-pop.mp3", -20);
        break;
      }
      default: {   // headline, question, hook
        if (sc.hook || sc.type === "question") {
          inner = `<div class="dhead"><div class="p">${chars(pre)}</div><div><span class="hl">${chars(hi)}</span></div></div>`;
        } else {
          inner = `<div class="lcard">${lbar}<div class="t1"><span class="p">${chars(pre)}</span> <span class="hl">${chars(hi)}</span></div></div>`;
          up(`#${id} .lcard`, a, 0.3, 50);
        }
        kin(`#${id} .p`, sc.hook ? 0 : sc.start);
        kin(`#${id} .hl`, hiAt, 0.03);
        hl(`#${id} .hl`, hiAt + 0.1);
        sfx(hiAt, "sfx-pop.mp3", -22);
      }
    }
    const front = sc.hook || sc.type === "cta";      // over the full-screen camera
    sceneHTML.push(`<section id="${id}" class="scene clip${front ? " front" : ""}" data-start="${q(Math.max(0, a - 0.3))}" data-duration="${q(Math.min(total, b + 0.3) - Math.max(0, a - 0.3))}" `
      + `data-track-index="${2 + (i % 2)}">${front ? '<div class="shade"></div>' : ""}<div class="in" style="left:${Z.x}px;top:${Z.y}px;width:${Z.w}px">${inner}</div></section>`);
    if (i > 0) { R(`#${id} .in`, a - 0.12, { opacity: 0, x: 120 }, { opacity: 1, x: 0 }, 0.3); sfx(a - 0.12, "sfx-whoosh-lat.mp3", -22); }
    if (i < scenes.length - 1) R(`#${id} .in`, b - 0.2, { opacity: 1, x: 0 }, { opacity: 0, x: -120 }, 0.2, "power2.in");
    if (sc.sticker) {
      const st = sc.sticker, sid = `st${i}`;
      stickSide = 1 - stickSide;
      overlays.push(sticker(sid, st.a, st.b, st.v, st.ico, V ? 1290 : (stickSide ? 60 : 520), V ? 150 : 1250));
      fb(`sticker(tl,"#${sid}",${q(st.at)},${q(Math.min(b - 0.15, st.at + 2.6))},${stickSide ? -5 : 4})`);
      sfx(st.at, "sfx-thwip.mp3", -21);
    }
  });
  sfx(0, "sfx-impact-deep.mp3", -17);

  const levels = levelChips(scenes, tl, total);
  const cap = captions(words, { x: V ? 1525 : W / 2, y: V ? 760 : 1720, charW: V ? 27 : 30.5 });

  // neon tubes breathe on the music
  if (opts.bpm) {
    const beat = 60 / opts.bpm;
    for (let t = 0; t < total - 0.3; t += beat) R(".tube", t, { opacity: 1 }, { opacity: 0.55 }, Math.min(0.4, beat * 0.9), "power2.out");
  }
  S("#flash", total - 0.5, { backgroundColor: "#0a0a0f" });
  R("#flash", total - 0.5, { opacity: 0 }, { opacity: 1 }, 0.45, "power2.in");

  writeComposition(opts.styleDir, opts.out, {
    W, H, TOTAL: q(total), FORMAT: V ? "wide" : "tall", CUTOUT: opts.cutout ? "cutout" : "rect", CAMW: opts.camW, CAMH: opts.camH,
    BRAND: `${bsplit[0]}<b>${bsplit[1]}</b>`, LEVELS: levels, SCENES: sceneHTML.join("\n"),
    CAM: camTag(opts, '<div id="camframe"></div>'), CAPTIONS: cap.html, OVERLAYS: overlays.join("\n"), JS: [...tl.js, ...cap.js].join("\n"),
  });
  return { events: tl.ev, W, H };
}

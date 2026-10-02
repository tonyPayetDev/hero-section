// Scenes -> HyperFrames composition (index.html + assets), « boost niveau » style, 9:16 or 16:9.
// Every reveal is pinned to a spoken word; nothing random at render time.
import fs from "node:fs";
import path from "node:path";
import { ASSETS, ROOT, esc, q, FPS } from "./tools.mjs";

// ------------------------------------------------------------------ kit markup (port of facecam-boost-kit/kit.py)
const ICONS = JSON.parse(fs.readFileSync(path.join(ROOT, "templates", "icons.json"), "utf8"));
const icon = (n, s = 40) => (ICONS[n] || ICONS.bolt).replaceAll("{s}", String(s));
const chars = (text, cls = "") => String(text).split(" ").map((w) => `<span style="white-space:nowrap">${[...w].map(
  (c) => `<span class="char${cls ? " " + cls : ""}">${esc(c)}</span>`).join("")}</span>`).join('<span class="char sp">&nbsp;</span>');
const elastic = (text) => `<span class="fb-elastic">${[...text].map((c) => `<span class="fb-ech">${esc(c)}</span>`).join("")}</span>`;
const SPARK = '<svg class="fb-spark" viewBox="0 0 56 56" width="56" height="56"><path d="M10 46 L22 30 M24 50 L30 34 M36 44 L40 30" stroke="{c}" stroke-width="5" stroke-linecap="round"/></svg>';
function sticker(id, a, b, v = "gold", ico = null, left = 0, top = 0) {
  const c = { gold: "#eab308", violet: "#a78bfa", red: "#ff6b6b" }[v];
  return `<div id="${id}" class="fb-sticker fb-${v}" style="left:${left}px;top:${top}px">`
    + (ico ? `<i class="fb-ico">${icon(ico, 58)}</i>` : "") + `<span class="a">${esc(a)}</span>` + (b ? `<span class="b">${esc(b)}</span>` : "")
    + SPARK.replace("{c}", c) + "</div>";
}

/** port of kit.py facecam_mode: transform + clip-path showing a source region inside a canvas box */
export function camMode(box, focus, src, cropH = null, radius = 0) {
  const [sw, sh] = src, [bx, by, bw, bh] = box;
  const ar = bw / bh;
  const ch = cropH == null ? Math.min(sh, sw / ar) : Math.min(cropH, sh, sw / ar);
  const cw = ch * ar;
  const cx0 = Math.min(Math.max(focus[0] - cw / 2, 0), sw - cw), cy0 = Math.min(Math.max(focus[1] - ch / 2, 0), sh - ch);
  const s = bw / cw, r = radius / s;
  return { x: +(bx - cx0 * s).toFixed(2), y: +(by - cy0 * s).toFixed(2), scale: +s.toFixed(5),
    clipPath: `inset(${cy0.toFixed(1)}px ${(sw - cx0 - cw).toFixed(1)}px ${(sh - cy0 - ch).toFixed(1)}px ${cx0.toFixed(1)}px round ${r.toFixed(1)}px)` };
}

const MUSIC = JSON.parse(fs.readFileSync(path.join(ROOT, "templates", "music.json"), "utf8"));

/**
 * opts: { format: "9:16"|"16:9", brand, cutout: bool, cam: path, camW, camH, total, cuts, music, out }
 */
export function compose(scenes, words, opts) {
  const V = opts.format === "16:9";
  const W = V ? 1920 : 1080, H = V ? 1080 : 1920;
  const js = [];
  const R = (sel, t, from, to, d = 0.3, ease = "power3.out") =>
    js.push(`tl.fromTo(${JSON.stringify(sel)},${JSON.stringify(from)},${JSON.stringify({ ...to, duration: d, ease, immediateRender: false })},${q(t)});`);
  const S = (sel, t, p) => js.push(`tl.set(${JSON.stringify(sel)},${JSON.stringify(p)},${q(t)});`);
  const up = (sel, t, d = 0.3, dist = 40) => R(sel, t, { opacity: 0, y: dist }, { opacity: 1, y: 0 }, d);
  const pop = (sel, t, d = 0.3) => R(sel, t, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1 }, d, "back.out(2.2)");
  const kin = (sel, t, st = 0.022, d = 0.3) => js.push(`tl.fromTo(${JSON.stringify(sel + " .char")},{opacity:0,y:40},{opacity:1,y:0,duration:${d},ease:"back.out(1.8)",stagger:${st},immediateRender:false},${q(t)});`);
  const hl = (sel, t) => R(sel, t, { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%" }, 0.35, "power2.out");
  const fb = (c) => js.push("FB." + c + ";");
  const flash = (t, op = 0.4, d = 0.22) => R("#flash", t, { opacity: op }, { opacity: 0 }, d, "power2.out");
  const total = opts.total;
  const ev = [];   // SFX events [t, file, dB]

  // ---------------------------------------------------------------- camera
  const src = [opts.camW, opts.camH];
  const focus = [opts.camW / 2, opts.camH * 0.38];
  let camModes;
  if (opts.cutout) {
    const s = V ? (H * 1.05) / opts.camH : (W * 0.94) / opts.camW;
    const x = V ? 1525 - (opts.camW * s) / 2 : (W - opts.camW * s) / 2;
    const y = H - opts.camH * s + (V ? 30 : 40);
    camModes = { base: { x, y, scale: s } };
    S("#camw", 0, { x, y, scale: s, transformOrigin: "0px 0px" });
    R("#camw", 0, { scale: s * 1.22, x: x - (opts.camW * s * 0.11), y: y + 60 }, { scale: s, x, y }, 0.32, "expo.out");
    // punch-in on every cut of the take: hides the jump cuts
    let z = false;
    for (const c of (opts.cuts || []).slice(1)) {
      z = !z;
      const zs = z ? s * 1.06 : s;
      S("#camw", c, { scale: zs, x: x - (opts.camW * (zs - s)) / 2, y: y - (opts.camH * (zs - s)) * 0.3 });
    }
  } else {
    camModes = V
      ? { full: camMode([0, 0, W, H], focus, src), main: camMode([1295, 225, 460, 460], focus, src, opts.camH * 0.62, 230) }
      : { full: camMode([0, 0, W, H], focus, src), main: camMode([24, 790, 1032, 1106], focus, src, null, 34) };
    S("#cam", 0, { ...camModes.full, transformOrigin: "0px 0px" });
    const firstB = scenes[0]?.b ?? 3;
    R("#cam", firstB - 0.25, camModes.full, camModes.main, 0.5, "power3.inOut");
    R("#camframe", firstB + 0.2, { opacity: 0 }, { opacity: 1 }, 0.3);
    const cta = scenes.find((s) => s.type === "cta");
    if (cta && !V) {
      R("#cam", cta.a - 0.25, camModes.main, camModes.full, 0.5, "power3.inOut");
      R("#camframe", cta.a - 0.25, { opacity: 1 }, { opacity: 0 }, 0.2);
    }
    R("#cam", 0, { scale: camModes.full.scale * 1.15 }, { scale: camModes.full.scale }, 0.35, "expo.out");
  }
  flash(0.12, 0.35, 0.22);

  // ---------------------------------------------------------------- zone for content
  const Z = V ? { x: 110, y: 140, w: 1080, h: 820 } : { x: 46, y: 110, w: 988, h: 640 };
  const sceneHTML = [], overlays = [];
  const brand = esc(opts.brand || "AUTOMATISATIONBOOST");
  const bsplit = brand.length > 6 ? [brand.slice(0, -5), brand.slice(-5)] : [brand, ""];
  const lbar = `<div class="lbar"><span>${bsplit[0]}<b>${bsplit[1]}</b></span><i class="d1"></i><i class="d2"></i><i class="d3"></i></div>`;
  const wordsTxt = (ws) => ws.map((w) => w.w).join(" ").replace(/[,;:]$/, "");
  let stickSide = 0;

  scenes.forEach((sc, i) => {
    const id = `s${i}`;
    const a = sc.a, b = sc.b;
    let inner = "";
    const head = sc.head;
    const pre = head ? wordsTxt(head.words.slice(0, head.hi)) : "";
    const hiTxt = head ? wordsTxt(head.words.slice(head.hi)) : "";
    const hiAt = head ? head.words[head.hi].s : sc.start;
    switch (sc.type) {
      case "cta": {
        const kw = sc.data.keyword;
        inner = `<div class="cta"><div class="a">${chars("COMMENTE")}</div><div class="b">${elastic(kw)}</div>`
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
        ev.push([sc.data.at, "sfx-impact-deep.mp3", -15], [sc.data.at + 0.05, "sfx-click-soft.mp3", -20], [sc.data.at + 0.6, "sfx-notify.mp3", -19]);
        break;
      }
      case "stat": {
        const val = sc.data.value, isInt = /^\d+$/.test(val);
        const label = wordsTxt(sc.data.label || []);
        inner = `<div class="lcard">${lbar}<div class="stat"><span class="num" data-v="${esc(val)}">${isInt ? "0" : esc(val)}</span>`
          + `<span class="unit">${esc(sc.data.unit)}</span></div><div class="t2">${chars(label)}</div></div>`;
        up(`#${id} .lcard`, a, 0.3, 50);
        if (isInt) js.push(`tl.fromTo("#${id} .num",{innerText:0},{innerText:${parseInt(val, 10)},snap:{innerText:1},duration:0.7,ease:"power2.out",immediateRender:false},${q(sc.data.at)});`);
        R(`#${id} .stat`, sc.data.at, { scale: 1.25 }, { scale: 1 }, 0.35, "back.out(2)");
        kin(`#${id} .t2`, sc.data.at + 0.2);
        ev.push([sc.data.at, "sfx-impact.mp3", -18]);
        break;
      }
      case "tools": {
        const tl = sc.data.tools;
        inner = `<div class="lcard">${lbar}<div class="t1"><span class="p">${chars(pre)}</span> <span class="hl">${chars(hiTxt)}</span></div><div class="chain">`
          + tl.map((t, k) => (k ? `<div class="arr r${k}"></div>` : "") + `<div class="app a${k}"><div class="tile">${esc(t.name.slice(0, 2))}</div><b>${esc(t.name)}</b></div>`).join("")
          + "</div></div>";
        up(`#${id} .lcard`, a, 0.3, 50);
        kin(`#${id} .p`, sc.start); kin(`#${id} .hl`, hiAt, 0.03); hl(`#${id} .hl`, hiAt + 0.1);
        tl.forEach((t, k) => {
          R(`#${id} .a${k}`, t.at, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1 }, 0.25, "back.out(2.5)");
          if (k) R(`#${id} .r${k}`, t.at - 0.12, { scaleX: 0 }, { scaleX: 1 }, 0.15);
          ev.push([t.at, "sfx-pop.mp3", -21]);
        });
        break;
      }
      case "list": {
        const items = sc.data.items;
        inner = `<div class="lcard">${lbar}<div class="chips">` + items.map((it, k) => {
          const short = it.label.split(" ").slice(-3).join(" ");
          return `<div class="chip c${k}"><i>${icon("check", 26)}</i><span>${esc(short)}</span></div>`;
        }).join("") + "</div></div>";
        up(`#${id} .lcard`, a, 0.3, 50);
        items.forEach((it, k) => {
          R(`#${id} .c${k}`, it.at, { opacity: 0, x: 40 }, { opacity: 1, x: 0 }, 0.25, "back.out(2)");
          R(`#${id} .c${k} i`, it.at + 0.12, { backgroundColor: "#262236", color: "#8A8A8A" }, { backgroundColor: "#eab308", color: "#0a0a0f" }, 0.2);
          ev.push([it.at, "sfx-click.mp3", -22]);
        });
        break;
      }
      case "contrast": {
        const L = wordsTxt(sc.data.left), Rt = wordsTxt(sc.data.right);
        inner = `<div class="lcard">${lbar}<div class="duo"><div class="side bad"><small>AVANT</small><b>${esc(L)}</b>`
          + `<svg class="x" width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M6 10 L94 90 M94 10 L6 90"/></svg></div>`
          + `<div class="side good"><small>MAINTENANT</small><b>${esc(Rt)}</b></div></div></div>`;
        up(`#${id} .lcard`, a, 0.3, 50);
        up(`#${id} .bad`, sc.start, 0.28, 30);
        R(`#${id} .bad path`, sc.data.at - 0.15, { strokeDashoffset: 300 }, { strokeDashoffset: 0 }, 0.25);
        R(`#${id} .bad`, sc.data.at, { opacity: 1 }, { opacity: 0.5 }, 0.25);
        up(`#${id} .good`, sc.data.at, 0.28, 30);
        ev.push([sc.data.at - 0.15, "sfx-glitch-soft.mp3", -21], [sc.data.at, "sfx-confirm.mp3", -20]);
        break;
      }
      case "steps": {
        inner = `<div class="lcard">${lbar}<div class="stepn"><span>ÉTAPE</span><b>${sc.data.n}</b></div>`
          + `<div class="t1"><span class="p">${chars(pre)}</span> <span class="hl">${chars(hiTxt)}</span></div></div>`;
        up(`#${id} .lcard`, a, 0.3, 50);
        pop(`#${id} .stepn`, sc.start);
        kin(`#${id} .p`, sc.start + 0.1); kin(`#${id} .hl`, hiAt, 0.03); hl(`#${id} .hl`, hiAt + 0.1);
        ev.push([sc.start, "sfx-pop.mp3", -20]);
        break;
      }
      default: {   // headline, question, hook
        const dark = sc.hook || sc.type === "question";
        if (dark) {
          inner = `<div class="dhead"><div class="p">${chars(pre)}</div><div><span class="hl">${chars(hiTxt)}</span></div></div>`;
        } else {
          inner = `<div class="lcard">${lbar}<div class="t1"><span class="p">${chars(pre)}</span> <span class="hl">${chars(hiTxt)}</span></div></div>`;
          up(`#${id} .lcard`, a, 0.3, 50);
        }
        kin(`#${id} .p`, sc.hook ? 0 : sc.start);
        kin(`#${id} .hl`, hiAt, 0.03);
        hl(`#${id} .hl`, hiAt + 0.1);
        ev.push([hiAt, "sfx-pop.mp3", -22]);
      }
    }
    const front = sc.hook || sc.type === "cta";      // over the full-screen camera
    sceneHTML.push(`<section id="${id}" class="scene clip${front ? " front" : ""}" data-start="${q(Math.max(0, a - 0.3))}" data-duration="${q(Math.min(total, b + 0.3) - Math.max(0, a - 0.3))}" `
      + `data-track-index="${2 + (i % 2)}">${front ? '<div class="shade"></div>' : ""}<div class="in" style="left:${Z.x}px;top:${Z.y}px;width:${Z.w}px">${inner}</div></section>`);
    if (i > 0) { R(`#${id} .in`, a - 0.12, { opacity: 0, x: 120 }, { opacity: 1, x: 0 }, 0.3); ev.push([a - 0.12, "sfx-whoosh-lat.mp3", -22]); }
    if (i < scenes.length - 1) R(`#${id} .in`, b - 0.2, { opacity: 1, x: 0 }, { opacity: 0, x: -120 }, 0.2, "power2.in");
    if (sc.sticker) {
      const st = sc.sticker, sid = `st${i}`;
      stickSide = 1 - stickSide;
      const left = V ? 1290 : (stickSide ? 60 : 520), top = V ? 150 : 1250;
      overlays.push(sticker(sid, st.a, st.b, st.v, st.ico, left, top));
      fb(`sticker(tl,"#${sid}",${q(st.at)},${q(Math.min(b - 0.15, st.at + 2.6))},${stickSide ? -5 : 4})`);
      ev.push([st.at, "sfx-thwip.mp3", -21]);
    }
  });
  ev.push([0, "sfx-impact-deep.mp3", -17]);

  // ---------------------------------------------------------------- level chip (NIVEAU 1 -> MAX)
  const lv = [];
  const lvScenes = scenes.filter((s) => s.level);
  lvScenes.forEach((s, k) => {
    const n = s.level === "MAX" ? 5 : Math.min(+s.level, 4);
    lv.push(`<div class="lvl${s.level === "MAX" ? " max" : ""}" id="lv${k}"><span>NIVEAU ${s.level}</span><span class="seg">${[0, 1, 2, 3, 4].map((j) => `<i class="${j < n ? "on" : ""}"></i>`).join("")}</span></div>`);
    R(`#lv${k}`, s.a, { opacity: 0, x: -40 }, { opacity: 1, x: 0 }, 0.3, "back.out(2)");
    const next = lvScenes[k + 1];
    S(`#lv${k}`, next ? next.a : (scenes.find((x) => x.type === "cta")?.a ?? total), { opacity: 0 });
  });

  // ---------------------------------------------------------------- captions (mono pill, active word gold)
  const caps = [], cj = [];
  const chunks = [];
  let cur = [];
  for (const w of words) {
    if (cur.length && (w.s - cur[cur.length - 1].e > 0.35 || (cur.map((x) => x.w).join(" ") + " " + w.w).length > 20 || cur.length >= 3)) { chunks.push(cur); cur = []; }
    cur.push(w);
  }
  if (cur.length) chunks.push(cur);
  const capY = V ? 760 : 1720, capX = V ? 1525 : W / 2;
  chunks.forEach((ch, k) => {
    const a = ch[0].s - 0.03;
    const b = k + 1 < chunks.length ? Math.min(chunks[k + 1][0].s - 0.03, ch[ch.length - 1].e + 0.5) : ch[ch.length - 1].e + 0.5;
    const txt = ch.map((x) => x.w).join(" ");
    const width = Math.round(txt.length * (V ? 27 : 30.5) + 88);
    caps.push(`<div class="cap" id="c${k}" style="width:${width}px">` + ch.map((x, j) => `<span class="cw" id="c${k}w${j}">${esc(x.w)}</span>`).join(" ") + "</div>");
    cj.push(`tl.set("#cap",{width:${width},x:${Math.round(capX - width / 2)},opacity:1},${q(Math.max(0, a))});`);
    cj.push(`tl.fromTo("#c${k}",{opacity:0.5,y:6},{opacity:1,y:0,duration:.06,ease:"power2.out",immediateRender:false},${q(Math.max(0, a))});`);   // the pill never shows empty
    cj.push(`tl.set("#c${k}",{opacity:0},${q(b)});`);
    if (k + 1 === chunks.length || chunks[k + 1][0].s - 0.03 > b + 0.02) cj.push(`tl.set("#cap",{opacity:0},${q(b)});`);
    ch.forEach((x, j) => {
      const nxt = Math.min(j + 1 < ch.length ? ch[j + 1].s : b, b);
      cj.push(`tl.set("#c${k}w${j}",{color:"#eab308",textShadow:"0 0 16px rgba(234,179,8,.8)"},${q(x.s)});`);
      cj.push(`tl.set("#c${k}w${j}",{color:"#EDEDED",textShadow:"0 0 0px rgba(234,179,8,0)"},${q(nxt)});`);
    });
  });
  S("#cap", 0, { y: capY, opacity: 0 });

  // ---------------------------------------------------------------- beat: neon tubes breathe on the music
  const m = MUSIC[opts.music];
  if (m && m.bpm) {
    const beat = 60 / m.bpm;
    for (let t = 0; t < total - 0.3; t += beat) R(".tube", t, { opacity: 1 }, { opacity: 0.55 }, Math.min(0.4, beat * 0.9), "power2.out");
  }
  S("#flash", total - 0.5, { backgroundColor: "#0a0a0f" });
  R("#flash", total - 0.5, { opacity: 0 }, { opacity: 1 }, 0.45, "power2.in");

  // ---------------------------------------------------------------- write
  const tpl = fs.readFileSync(path.join(ROOT, "templates", "composition.html"), "utf8");
  const camTag = opts.cutout
    ? `<div id="camw"><video id="cam" src="cam.webm" muted playsinline data-start="0" data-media-start="0" data-duration="${q(total)}" data-track-index="6"></video></div>`
    : `<video id="cam" src="cam.mp4" muted playsinline data-start="0" data-duration="${q(total)}" data-track-index="6"></video><div id="camframe"></div>`;
  const html = tpl.replaceAll("%%W%%", String(W)).replaceAll("%%H%%", String(H)).replaceAll("%%TOTAL%%", String(q(total)))
    .replace("%%FORMAT%%", V ? "wide" : "tall").replace("%%CUTOUT%%", opts.cutout ? "cutout" : "rect")
    .replace("%%CAMW%%", String(opts.camW)).replace("%%CAMH%%", String(opts.camH))
    .replace("%%BRAND%%", `${bsplit[0]}<b>${bsplit[1]}</b>`)
    .replace("%%LEVELS%%", lv.join("\n")).replace("%%SCENES%%", sceneHTML.join("\n")).replace("%%CAM%%", camTag)
    .replace("%%CAPTIONS%%", caps.join("\n")).replace("%%OVERLAYS%%", overlays.join("\n")).replace("%%JS%%", [...js, ...cj].join("\n"));
  const out = opts.out;
  fs.mkdirSync(out, { recursive: true });
  for (const d of ["fonts", "vendor", "kit"]) fs.cpSync(path.join(ASSETS, d), path.join(out, d), { recursive: true });
  fs.writeFileSync(path.join(out, "index.html"), html);
  fs.writeFileSync(path.join(out, "hyperframes.json"), JSON.stringify({ media: { autoProxy: true } }, null, 1));
  return { events: ev.filter((e) => e[0] >= 0 && e[0] < total - 0.1).sort((x, y) => x[0] - y[0]), W, H };
}

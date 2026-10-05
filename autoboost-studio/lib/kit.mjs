// Shared building blocks for every style: markup helpers, the GSAP timeline writer, captions, file output.
// A style (styles/<id>/compose.mjs) imports what it needs from here; see AGENTS.md for the contract.
import fs from "node:fs";
import path from "node:path";
import { ASSETS, ROOT, esc, q } from "./tools.mjs";

export { esc, q };

// ------------------------------------------------------------------ markup
const ICONS = JSON.parse(fs.readFileSync(path.join(ROOT, "templates", "icons.json"), "utf8"));
export const icon = (n, s = 40) => (ICONS[n] || ICONS.bolt).replaceAll("{s}", String(s));

/** one <span class="char"> per letter, words kept together (wrap only between words) */
export const chars = (text, cls = "") => String(text).split(" ").map((w) => `<span style="white-space:nowrap">${[...w].map(
  (c) => `<span class="char${cls ? " " + cls : ""}">${esc(c)}</span>`).join("")}</span>`).join('<span class="char sp">&nbsp;</span>');

/** font size (px) so a CTA keyword of any length fits `width` px (bold caps ≈ 0.68 em per letter) */
export const kwSize = (kw, max, width) => Math.round(Math.min(max, width / (Math.max(1, [...String(kw)].length) * 0.68)));

export const elastic = (text) => `<span class="fb-elastic">${[...text].map((c) => `<span class="fb-ech">${esc(c)}</span>`).join("")}</span>`;

const SPARK = '<svg class="fb-spark" viewBox="0 0 56 56" width="56" height="56"><path d="M10 46 L22 30 M24 50 L30 34 M36 44 L40 30" stroke="{c}" stroke-width="5" stroke-linecap="round"/></svg>';
/** kit sticker (TROP LENT, ÇA MONTE…); animate it with fb(`sticker(tl,"#id",t0,t1,rot)`) */
export function sticker(id, a, b, v = "gold", ico = null, left = 0, top = 0) {
  const c = { gold: "#eab308", violet: "#a78bfa", red: "#ff6b6b" }[v];
  return `<div id="${id}" class="fb-sticker fb-${v}" style="left:${left}px;top:${top}px">`
    + (ico ? `<i class="fb-ico">${icon(ico, 58)}</i>` : "") + `<span class="a">${esc(a)}</span>` + (b ? `<span class="b">${esc(b)}</span>` : "")
    + SPARK.replace("{c}", c) + "</div>";
}

/** a source region shown inside a canvas box: transform + clip-path for the camera <video> (port of kit.py facecam_mode) */
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

/** the scene's headline split around its strongest word: { pre, hi, hiAt } */
export function headParts(sc) {
  const txt = (ws) => ws.map((w) => w.w).join(" ").replace(/[,;:]$/, "");
  const h = sc.head;
  if (!h) return { pre: "", hi: "", hiAt: sc.start };
  return { pre: txt(h.words.slice(0, h.hi)), hi: txt(h.words.slice(h.hi)), hiAt: h.words[h.hi].s };
}
export const wordsText = (ws) => (ws || []).map((w) => w.w).join(" ").replace(/[,;:]$/, "");

// ------------------------------------------------------------------ timeline writer
/**
 * Every tween is a fromTo with immediateRender:false at an absolute time: the render can seek anywhere.
 * tl.js holds the lines; tl.ev collects SFX events [t, file, dB] for the mixer.
 */
export function timeline() {
  const js = [], ev = [];
  const R = (sel, t, from, to, d = 0.3, ease = "power3.out") =>
    js.push(`tl.fromTo(${JSON.stringify(sel)},${JSON.stringify(from)},${JSON.stringify({ ...to, duration: d, ease, immediateRender: false })},${q(t)});`);
  const S = (sel, t, p) => js.push(`tl.set(${JSON.stringify(sel)},${JSON.stringify(p)},${q(t)});`);
  return {
    js, ev, R, S,
    up: (sel, t, d = 0.3, dist = 40) => R(sel, t, { opacity: 0, y: dist }, { opacity: 1, y: 0 }, d),
    pop: (sel, t, d = 0.3) => R(sel, t, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1 }, d, "back.out(2.2)"),
    /** letter-by-letter reveal of a chars() block */
    kin: (sel, t, st = 0.022, d = 0.3) => js.push(`tl.fromTo(${JSON.stringify(sel + " .char")},{opacity:0,y:40},{opacity:1,y:0,duration:${d},ease:"back.out(1.8)",stagger:${st},immediateRender:false},${q(t)});`),
    /** highlighter sweep on an element with a background-size gradient */
    hl: (sel, t) => R(sel, t, { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%" }, 0.35, "power2.out"),
    /** call into kit/kit.js (FB.sticker, FB.type, FB.elastic) */
    fb: (c) => js.push("FB." + c + ";"),
    /** counter that ends exactly on the value (innerText + snap) */
    count: (sel, t, to, d = 0.7) => js.push(`tl.fromTo(${JSON.stringify(sel)},{innerText:0},{innerText:${to},snap:{innerText:1},duration:${d},ease:"power2.out",immediateRender:false},${q(t)});`),
    sfx: (t, file, db) => ev.push([t, file, db]),
    raw: (line) => js.push(line),
  };
}

// ------------------------------------------------------------------ captions
/** words -> chunks of <= maxWords / maxChars, split on pauses */
export function captionChunks(words, { maxWords = 3, maxChars = 20, gap = 0.35 } = {}) {
  const chunks = [];
  let cur = [];
  for (const w of words) {
    if (cur.length && (w.s - cur[cur.length - 1].e > gap || (cur.map((x) => x.w).join(" ") + " " + w.w).length > maxChars || cur.length >= maxWords)) { chunks.push(cur); cur = []; }
    cur.push(w);
  }
  if (cur.length) chunks.push(cur);
  return chunks.map((ch, k) => ({
    words: ch, a: ch[0].s - 0.03,
    b: k + 1 < chunks.length ? Math.min(chunks[k + 1][0].s - 0.03, ch[ch.length - 1].e + 0.5) : ch[ch.length - 1].e + 0.5,
  }));
}

/**
 * Captions in a container #cap: each chunk is a .cap div, the spoken word gets the active colour.
 * pill: true resizes the #cap pill to the chunk (boost-niveau); false = free-floating words.
 * Returns { html, js } to drop into %%CAPTIONS%% and the timeline.
 */
export function captions(words, { x, y, pill = true, charW = 30.5, pad = 88, active = "#eab308", idle = "#EDEDED",
  glow = "rgba(234,179,8,.8)", maxWords = 3, maxChars = 20, pop = false } = {}) {
  const chunks = captionChunks(words, { maxWords, maxChars });
  const html = [], js = [];
  chunks.forEach((c, k) => {
    const txt = c.words.map((w) => w.w).join(" ");
    const width = Math.round(txt.length * charW + pad);
    html.push(`<div class="cap" id="c${k}" style="width:${width}px">` + c.words.map((w, j) => `<span class="cw" id="c${k}w${j}">${esc(w.w)}</span>`).join(" ") + "</div>");
    const a = Math.max(0, c.a);
    js.push(`tl.set("#cap",{width:${width},x:${Math.round(x - width / 2)},opacity:1},${q(a)});`);
    js.push(pop
      ? `tl.fromTo("#c${k}",{opacity:0.5,scale:0.8},{opacity:1,scale:1,duration:.12,ease:"back.out(2.5)",immediateRender:false},${q(a)});`
      : `tl.fromTo("#c${k}",{opacity:0.5,y:6},{opacity:1,y:0,duration:.06,ease:"power2.out",immediateRender:false},${q(a)});`);   // never shows empty
    js.push(`tl.set("#c${k}",{opacity:0},${q(c.b)});`);
    if (k + 1 === chunks.length || chunks[k + 1].a > c.b + 0.02) js.push(`tl.set("#cap",{opacity:0},${q(c.b)});`);
    c.words.forEach((w, j) => {
      const nxt = Math.min(j + 1 < c.words.length ? c.words[j + 1].s : c.b, c.b);
      js.push(`tl.set("#c${k}w${j}",{color:"${active}",textShadow:"0 0 16px ${glow}"},${q(w.s)});`);
      js.push(`tl.set("#c${k}w${j}",{color:"${idle}",textShadow:"0 0 0px rgba(0,0,0,0)"},${q(nxt)});`);
    });
  });
  js.unshift(`tl.set("#cap",{y:${y},opacity:0},0);`);
  return { html: html.join("\n"), js };
}

// ------------------------------------------------------------------ NIVEAU 1 -> MAX chip
export function levelChips(scenes, tl, total) {
  const html = [];
  const lv = scenes.filter((s) => s.level);
  lv.forEach((s, k) => {
    const n = s.level === "MAX" ? 5 : Math.min(+s.level, 4);
    html.push(`<div class="lvl${s.level === "MAX" ? " max" : ""}" id="lv${k}"><span>NIVEAU ${s.level}</span><span class="seg">${[0, 1, 2, 3, 4].map((j) => `<i class="${j < n ? "on" : ""}"></i>`).join("")}</span></div>`);
    tl.R(`#lv${k}`, s.a, { opacity: 0, x: -40 }, { opacity: 1, x: 0 }, 0.3, "back.out(2)");
    const next = lv[k + 1];
    tl.S(`#lv${k}`, next ? next.a : (scenes.find((x) => x.type === "cta")?.a ?? total), { opacity: 0 });
  });
  return html.join("\n");
}

/** the <video> tag(s) for the camera: matted (cam.webm in #camw) or plain (cam.mp4) */
export function camTag(opts, extra = "") {
  return opts.cutout
    ? `<div id="camw"><video id="cam" src="cam.webm" muted playsinline data-start="0" data-media-start="0" data-duration="${q(opts.total)}" data-track-index="6"></video></div>`
    : `<video id="cam" src="cam.mp4" muted playsinline data-start="0" data-duration="${q(opts.total)}" data-track-index="6"></video>${extra}`;
}

// ------------------------------------------------------------------ output
/**
 * Fills styles/<id>/composition.html: every %%KEY%% of `fill` is replaced, then the shared assets
 * (fonts, vendor/gsap, kit) and the style's own assets/ folder are copied next to index.html.
 */
export function writeComposition(styleDir, out, fill) {
  let html = fs.readFileSync(path.join(styleDir, "composition.html"), "utf8");
  for (const [k, v] of Object.entries(fill)) html = html.replaceAll(`%%${k}%%`, String(v));
  const left = html.match(/%%[A-Z_]+%%/g);
  if (left) throw new Error(`composition.html: champs non remplis ${[...new Set(left)].join(", ")}`);
  fs.mkdirSync(out, { recursive: true });
  for (const d of ["fonts", "vendor", "kit"]) fs.cpSync(path.join(ASSETS, d), path.join(out, d), { recursive: true });
  if (fs.existsSync(path.join(styleDir, "assets"))) fs.cpSync(path.join(styleDir, "assets"), path.join(out, "style"), { recursive: true });
  fs.writeFileSync(path.join(out, "index.html"), html);
  fs.writeFileSync(path.join(out, "hyperframes.json"), JSON.stringify({ media: { autoProxy: true } }, null, 1));
}

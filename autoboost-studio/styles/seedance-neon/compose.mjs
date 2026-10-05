// Style « Seedance néon » (from autoboost-100 / gabarit autoboost-40, 9:16).
// Hook on the full camera, then a dark top panel per screen (kicker + big title + one card) and the camera in a
// neon frame below. Numbered badge top-right, caption band on the joint. Works with or without background removal.
import { kwSize, camMode, camTag, captions, chars, elastic, esc, headParts, icon, q, sticker, timeline, wordsText, writeComposition } from "../../lib/kit.mjs";

const KICK = { stat: "LE CHIFFRE", tools: "LA CHAÎNE", list: "LA LISTE", contrast: "AVANT / MAINTENANT", question: "LA QUESTION" };

export default function compose(scenes, words, opts) {
  const W = 1080, H = 1920;
  const tl = timeline();
  const { R, S, up, pop, kin, fb, sfx } = tl;
  const total = opts.total;
  const hookEnd = scenes[0]?.hook ? scenes[0].b : 0;

  // ---------------------------------------------------------------- camera
  if (opts.cutout) {
    const s0 = Math.min(W / opts.camW, H / opts.camH), s1 = 960 / opts.camH;
    const full = { x: (W - opts.camW * s0) / 2, y: H - opts.camH * s0, scale: s0 };
    const low = { x: (W - opts.camW * s1) / 2, y: H - opts.camH * s1 + 20, scale: s1 };
    S("#camw", 0, { ...(hookEnd ? full : low), transformOrigin: "0px 0px" });
    if (hookEnd) R("#camw", hookEnd - 0.25, full, low, 0.5, "power3.inOut");
  } else {
    const src = [opts.camW, opts.camH], face = [opts.camW / 2, opts.camH * 0.38];
    const full = camMode([0, 0, W, H], face, src), low = camMode([30, 1090, 1020, 800], face, src, null, 36);
    const set = (m) => ({ x: m.x, y: m.y, scale: m.scale, clipPath: m.clipPath });
    S("#cam", 0, { ...set(hookEnd ? full : low), transformOrigin: "0px 0px" });
    if (hookEnd) R("#cam", hookEnd - 0.25, set(full), set(low), 0.5, "power3.inOut");
    R("#frame", hookEnd + 0.15, { opacity: 0 }, { opacity: 1 }, 0.35);
  }
  R("#flash", 0.1, { opacity: 0.3 }, { opacity: 0 }, 0.22, "power2.out");

  // ---------------------------------------------------------------- panels
  const sceneHTML = [], badges = [], overlays = [];
  const title = (pre, hi, cls = "y") => `<div class="title">${pre ? `<span class="p">${chars(pre)}</span> ` : ""}<span class="${cls} h">${chars(hi)}</span></div>`;
  const kicker = (t) => `<div class="kicker">${esc(t)}</div>`;
  let n = 0, side = 0;

  scenes.forEach((sc, i) => {
    const id = `s${i}`, a = sc.a, b = sc.b;
    const { pre, hi, hiAt } = headParts(sc);
    const reveal = (t0) => { kin(`#${id} .title .p`, t0, 0.02); kin(`#${id} .title .h`, hiAt, 0.03); };
    const kick = (t0) => R(`#${id} .kicker`, t0, { opacity: 0, x: -30 }, { opacity: 1, x: 0 }, 0.3);
    let inner;
    const solo = !sc.hook && ["headline", "question", "steps"].includes(sc.type);   // a title alone: bigger, centred in the panel
    switch (sc.type) {
      case "cta": {
        const kw = sc.data.keyword;
        inner = `<div class="ctaw">${kicker("Commente le mot")}<div class="kw" style="font-size:${kwSize(kw, 170, 920)}px">${elastic(kw)}</div>`
          + `<div class="sub">→ je t'envoie <b>tout</b> en DM</div><div class="gbar"><i></i></div></div>`;
        kick(a);
        S(`#${id} .kw`, 0, { opacity: 0 });
        R(`#${id} .kw`, sc.data.at, { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1 }, 0.25, "power4.in");
        fb(`elastic(tl,"#${id} .kw",${q(sc.data.at + 0.35)},${q(Math.max(0.8, b - sc.data.at - 0.5))})`);
        up(`#${id} .sub`, sc.data.at + 0.4, 0.3, 24);
        up(`#${id} .gbar`, sc.data.at + 0.5, 0.25, 16);
        R(`#${id} .gbar i`, sc.data.at + 0.6, { scaleX: 0 }, { scaleX: 1 }, Math.max(0.6, Math.min(1.6, b - sc.data.at - 0.8)), "power2.inOut");
        sfx(sc.data.at, "sfx-impact-deep.mp3", -15); sfx(sc.data.at + 0.4, "sfx-notify.mp3", -19);
        break;
      }
      case "stat": {
        const val = sc.data.value, isInt = /^\d+$/.test(val);
        inner = kicker(KICK.stat) + `<div class="card"><div class="big"><span class="num">${isInt ? "0" : esc(val)}</span><span class="u">${esc(sc.data.unit)}</span></div>`
          + `<div class="lab">${chars(wordsText(sc.data.label))}</div></div>`;
        kick(a); up(`#${id} .card`, a + 0.1, 0.35, 50);
        if (isInt) tl.count(`#${id} .num`, sc.data.at, parseInt(val, 10));
        R(`#${id} .big`, sc.data.at, { scale: 1.25 }, { scale: 1 }, 0.35, "back.out(2)");
        kin(`#${id} .lab`, sc.data.at + 0.2);
        sfx(sc.data.at, "sfx-impact.mp3", -18);
        break;
      }
      case "tools": {
        const tools = sc.data.tools;
        inner = kicker(KICK.tools) + title(pre, hi) + `<div class="order">` + tools.map((t, j) => (j ? `<span class="arw w${j}">→</span>` : "")
          + `<div class="ochip o${j}"><span class="n">${j + 1}</span>${esc(t.name)}</div>`).join("") + "</div>";
        kick(a); reveal(sc.start);
        tools.forEach((t, j) => {
          R(`#${id} .o${j}`, t.at, { opacity: 0, y: 30 }, { opacity: 1, y: 0 }, 0.3, "back.out(2)");
          if (j) R(`#${id} .w${j}`, t.at - 0.1, { opacity: 0 }, { opacity: 1 }, 0.2);
          sfx(t.at, "sfx-pop.mp3", -21);
        });
        break;
      }
      case "list": {
        const items = sc.data.items.slice(0, 5);
        inner = kicker(KICK.list) + `<div class="moves">` + items.map((it, j) =>
          `<div class="mv m${j}"><span class="tag">${icon("check", 24)}</span>${esc(it.label.split(" ").slice(-4).join(" "))}</div>`).join("") + "</div>";
        kick(a);
        items.forEach((it, j) => {
          R(`#${id} .m${j}`, it.at, { opacity: 0, x: 60 }, { opacity: 1, x: 0 }, 0.3, "power3.out");
          R(`#${id} .m${j} .tag`, it.at + 0.15, { backgroundColor: "rgba(0,0,0,0)", color: "#6b7280", borderColor: "#2a2140" },
            { backgroundColor: "#FFE600", color: "#060606", borderColor: "#FFE600" }, 0.2);
          sfx(it.at, "sfx-click.mp3", -22);
        });
        break;
      }
      case "contrast": {
        inner = kicker(KICK.contrast) + `<div class="refs"><div class="ref ko" style="position:relative"><small>AVANT</small><b>${esc(wordsText(sc.data.left))}</b><i class="strike"></i></div>`
          + `<div class="ref ok"><small>MAINTENANT</small><b>${esc(wordsText(sc.data.right))}</b></div></div>`;
        kick(a);
        up(`#${id} .ko`, sc.start, 0.3, 30);
        R(`#${id} .strike`, sc.data.at - 0.15, { scaleX: 0 }, { scaleX: 1 }, 0.25, "power2.out");
        up(`#${id} .ok`, sc.data.at, 0.3, 30);
        sfx(sc.data.at - 0.15, "sfx-glitch-soft.mp3", -21); sfx(sc.data.at, "sfx-confirm.mp3", -20);
        break;
      }
      case "steps": {
        inner = kicker(`ÉTAPE ${sc.data.n}`) + title(pre, hi).replace('class="title"', 'class="title xl"');
        kick(sc.start); reveal(sc.start + 0.1);
        sfx(sc.start, "sfx-pop.mp3", -20);
        break;
      }
      default: {   // headline, question, hook
        const k = sc.hook ? "" : (KICK[sc.type] || esc(opts.brand || "AUTOMATISATIONBOOST"));
        inner = (k ? kicker(k) : "") + title(pre, hi, sc.type === "question" ? "o" : "y").replace('class="title"', 'class="title xl"');
        if (k) kick(a);
        reveal(sc.hook ? 0 : sc.start);
        sfx(hiAt, "sfx-pop.mp3", -22);
      }
    }
    sceneHTML.push(`<section id="${id}" class="scene clip${sc.hook ? " hook" : ""}" data-start="${q(Math.max(0, a - 0.3))}" data-duration="${q(Math.min(total, b + 0.3) - Math.max(0, a - 0.3))}" `
      + `data-track-index="${2 + (i % 2)}"><div class="bgp p${i % 4}"></div><div class="pad${solo ? " mid" : ""}">${inner}</div></section>`);
    if (i > 0) {
      R(`#${id} .bgp`, a - 0.15, { opacity: 0 }, { opacity: 1 }, 0.25, "power2.out");
      R(`#${id} .pad`, a - 0.15, { opacity: 0, y: 40 }, { opacity: 1, y: 0 }, 0.35);
      sfx(a - 0.15, "sfx-whoosh-lat.mp3", -23);
    }
    if (!sc.hook && sc.type !== "cta") {
      n += 1;
      badges.push(`<div class="tipnum" id="tip${i}">#${n}</div>`);
      pop(`#tip${i}`, a + 0.05, 0.3);
      S(`#tip${i}`, b - 0.05, { opacity: 0 });
    }
    if (sc.sticker) {
      const st = sc.sticker, sid = `st${i}`;
      side = 1 - side;
      overlays.push(sticker(sid, st.a, st.b, st.v, st.ico, side ? 600 : 40, 1150));
      fb(`sticker(tl,"#${sid}",${q(st.at)},${q(Math.min(b - 0.15, st.at + 2.6))},${side ? 4 : -5})`);
      sfx(st.at, "sfx-thwip.mp3", -21);
    }
  });
  sfx(0, "sfx-impact-deep.mp3", -17);

  // captions: low on the full camera during the hook, then in the band on the joint
  const cap = captions(words, { x: W / 2, y: hookEnd ? 1560 : 960, pill: false, charW: 34, pad: 40, active: "#FFE600", idle: "#f5f5f7", glow: "rgba(255,230,0,.8)" });
  if (hookEnd) S("#cap", hookEnd, { y: 960 });
  R("#capband", hookEnd + 0.1, { opacity: 0 }, { opacity: 1 }, 0.3);
  S("#flash", total - 0.5, { backgroundColor: "#060606" });
  R("#flash", total - 0.5, { opacity: 0 }, { opacity: 1 }, 0.45, "power2.in");

  writeComposition(opts.styleDir, opts.out, {
    TOTAL: q(total), CAMW: opts.camW, CAMH: opts.camH, CUTOUT: opts.cutout ? "cutout" : "rect", CAM: camTag(opts),
    SCENES: sceneHTML.join("\n"), BADGES: badges.join("\n"), CAPTIONS: cap.html, OVERLAYS: overlays.join("\n"), JS: [...tl.js, ...cap.js].join("\n"),
  });
  return { events: tl.ev, W, H };
}

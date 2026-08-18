#!/usr/bin/env node
/**
 * build_html.mjs <edition.json> <timing.json> <out.html> [template.html]
 *
 * Injects the parsed edition + the measured voice timing into the locked
 * Journal IA composition template. Fully deterministic — no LLM, no network.
 *
 * The template owns the LOOK (neon charter, avatar window, countdown, captions).
 * This file owns the CONTENT (n briefs, n gags, date, CTA word) and the TIMELINE
 * (built from the real segment durations, so any script length works).
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const [, , EDITION, TIMING, OUT, TPL] = process.argv;
if (!EDITION || !TIMING || !OUT) {
  console.error('usage: build_html.mjs <edition.json> <timing.json> <out.html> [template]');
  process.exit(2);
}
const ed = JSON.parse(fs.readFileSync(EDITION, 'utf8'));
const tm = JSON.parse(fs.readFileSync(TIMING, 'utf8'));
const tplPath = TPL || path.join(HERE, '..', 'template', 'index.tpl.html');
let html = fs.readFileSync(tplPath, 'utf8');

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const seg = (id) => ed.segments.find((s) => s.id === id);
const has = (id) => !!tm.start[id];
const S = (id) => tm.start[id];
const E = (id) => +(tm.start[id] + tm.dur[id]).toFixed(3);

/* ---------------------------------------------------------- accent colors */
const PALETTE = {
  google: ['#8ab4ff', '74,130,255', '#4a82ff'],
  openai: ['#7fe9df', '37,220,205', '#25dccd'],
  deepseek: ['#ff8ac4', '255,90,160', '#ff5aa0'],
  dbx: ['#ffc06b', '255,160,60', '#ff8a3d'],
};
const accentCss = Object.entries(PALETTE).map(([k, [fg, rgb, dot]]) =>
  `  .src.${k}{ color:${fg}; background:rgba(${rgb},.14); border:1px solid rgba(${rgb},.45);} .src.${k} i{ background:${dot} }`
).join('\n');

/* --------------------------------------------------------------- brief DOM */
const TITLE_ACCENT = ['g', 'v', 'o'];
function titleHtml(title, i) {
  const words = esc(title).split(' ');
  if (words.length === 1) return `<span class="${TITLE_ACCENT[i % 3]}">${words[0]}</span>`;
  const split = Math.max(1, words.length - 2);
  return `${words.slice(0, split).join(' ')} <span class="${TITLE_ACCENT[i % 3]}">${words.slice(split).join(' ')}</span>`;
}
const briefsHtml = ed.briefs.map((b, i) => `    <div class="brief" id="b${b.n}">
      <div class="bar"><div class="live"><i></i>Live</div><div class="jt">JOURNAL <b>IA</b> · ${esc(ed.dateShort)}</div></div>
      <div class="body">
        <div class="num">${b.n}</div>
        <div class="src ${b.accent}"><i></i><span class="src-name">${esc(b.source)}</span></div>
        <h1>${titleHtml(b.title, i)}</h1>
        <div class="sub">${esc(b.sub)}</div>
        <div class="chips">${b.chips.map((c) => `<b>${esc(c)}</b>`).join('')}</div>
      </div>
    </div>`).join('\n');

/* ----------------------------------------------------------------- gag DOM */
const GAG_LABELS = ['La réalité', 'Ça va vite', 'Point final'];
const gagSegs = ed.segments.filter((s) => s.role === 'gag');
const gagsHtml = gagSegs.map((g, i) => `  <div class="gag" id="gag_${g.id}">
    <span class="lab">${esc(GAG_LABELS[i % GAG_LABELS.length])}</span>
    <div class="stack">
${(g.words || []).slice(0, 3).map((w, j) => `      <div class="w w${j + 1}">${esc(w)}</div>`).join('\n')}
    </div>
  </div>`).join('\n');

/* ------------------------------------------------------------- timeline JS */
const L = [];
const p = (s) => L.push('    ' + s);
const caps = (id) => {
  const s = seg(id);
  if (!s || !s.caps || !s.caps.length) return;
  p(`capSeq(${JSON.stringify(s.caps)}, ${(S(id) + 0.2).toFixed(3)}, ${E(id).toFixed(3)});`);
};

p('tl.fromTo("#brand",{opacity:0,y:-12},{opacity:1,y:0,duration:0.4},0.1);');
p('tl.fromTo("#kicker",{opacity:0,y:-12},{opacity:1,y:0,duration:0.4},0.2);');

/* background beats: one swap per third of the piece */
const third = tm.duration / 3;
p(`tl.to("#bg1",{opacity:0,duration:0.5},${(third).toFixed(2)}); tl.to("#bg2",{opacity:1,duration:0.5},${(third).toFixed(2)});`);
p(`tl.to("#bg2",{opacity:0,duration:0.5},${(third * 2).toFixed(2)}); tl.to("#bg3",{opacity:1,duration:0.5},${(third * 2).toFixed(2)});`);

/* --- INTRO --- */
p('show("#intro", 0.25, 0.4);');
p('tl.fromTo("#intro .jt",{opacity:0,scale:1.3},{opacity:1,scale:1,duration:0.5,ease:"back.out(1.8)"},0.3);');
p('tl.fromTo("#intro .date",{opacity:0,y:-14},{opacity:1,y:0,duration:0.4},0.5);');
p('tl.fromTo("#intro .tag",{opacity:0,y:16},{opacity:1,y:0,duration:0.4},0.9);');
p(`show("#avatarWin", ${S('intro').toFixed(3)}, 0.4);`);
p(`hide("#avatarWin", ${(E('intro') - 0.1).toFixed(3)}, 0.28);`);
caps('intro');

/* --- BRIEFS + GAGS --- */
const avatarWindows = [{ id: 'intro', in: S('intro'), out: E('intro') - 0.1 }];
ed.briefs.forEach((b, i) => {
  const id = b.segId;
  if (!has(id)) return;
  p('');
  p(`/* brief ${b.n} — ${b.source} */`);
  p(`show("#news", ${(S(id) - 0.2).toFixed(3)}, 0.3);`);
  p(`briefIn("#b${b.n}", ${(S(id) - 0.1).toFixed(3)});`);
  caps(id);
  p(`briefOut("#b${b.n}", ${(E(id) + 0.05).toFixed(3)});`);
  p(`hide("#news", ${(E(id) + 0.1).toFixed(3)}, 0.25);`);

  const g = gagSegs.find((s) => s.brief === i);
  if (g && has(g.id)) {
    p(`/* gag after brief ${b.n} */`);
    p(`show("#avatarWin", ${(S(g.id) - 0.05).toFixed(3)}, 0.28);`);
    p(`gagIn("#gag_${g.id}", ${S(g.id).toFixed(3)});`);
    caps(g.id);
    p(`hide("#gag_${g.id}", ${(E(g.id) - 0.05).toFixed(3)}, 0.3);`);
    p(`hide("#avatarWin", ${(E(g.id) - 0.05).toFixed(3)}, 0.28);`);
    avatarWindows.push({ id: g.id, in: S(g.id) - 0.05, out: E(g.id) - 0.05 });
  }
});

/* --- OUTRO --- */
if (has('outro')) {
  p('');
  p('/* outro */');
  p(`show("#avatarWin", ${(S('outro') - 0.05).toFixed(3)}, 0.28);`);
  p(`tl.fromTo("#outro",{opacity:0,y:22},{opacity:1,y:0,duration:0.4,ease:"power3.out"},${S('outro').toFixed(3)});`);
  p(`tl.to("#outro h2 b",{textShadow:"0 0 30px rgba(255,230,0,.9)",duration:0.3,yoyo:true,repeat:2},${(S('outro') + 0.7).toFixed(3)});`);
  caps('outro');
  p(`hide("#outro", ${(E('outro') - 0.1).toFixed(3)}, 0.3);`);
  p(`hide("#avatarWin", ${(E('outro') - 0.1).toFixed(3)}, 0.28);`);
  avatarWindows.push({ id: 'outro', in: S('outro') - 0.05, out: E('outro') - 0.1 });
}

/* --- CTA --- */
if (has('cta')) {
  p('');
  p('/* CTA */');
  p(`show("#avatarWin", ${(S('cta') - 0.05).toFixed(3)}, 0.28);`);
  p(`tl.fromTo("#cta",{opacity:0,y:20},{opacity:1,y:0,duration:0.4,ease:"power3.out"},${S('cta').toFixed(3)});`);
  p(`tl.fromTo("#cta .mot",{scale:0.6,opacity:0},{scale:1,opacity:1,duration:0.45,ease:"back.out(2)"},${(S('cta') + 0.1).toFixed(3)});`);
  p(`tl.to("#cta .mot",{boxShadow:"0 0 80px rgba(255,230,0,.9)",duration:0.3,yoyo:true,repeat:3},${(S('cta') + 0.6).toFixed(3)});`);
  caps('cta');
  p(`hide("#cta", ${(E('cta') + 0.05).toFixed(3)}, 0.25);`);
  p(`hide("#avatarWin", ${(E('cta') + 0.05).toFixed(3)}, 0.25);`);
  avatarWindows.push({ id: 'cta', in: S('cta') - 0.05, out: E('cta') + 0.05 });
}

/* --- COUNTDOWN --- */
if (has('cd')) {
  const t0 = S('cd');
  const step = tm.dur.cd / 3;
  p('');
  p('/* countdown 3-2-1 */');
  p(`show("#count", ${(t0 - 0.12).toFixed(3)}, 0.22);`);
  p(`const cds=[["#n3",${(t0 + 0.05).toFixed(3)}],["#n2",${(t0 + 0.05 + step).toFixed(3)}],["#n1",${(t0 + 0.05 + step * 2).toFixed(3)}]];`);
  p('cds.forEach(([id,t])=>{');
  p('  tl.fromTo("#ring",{opacity:0,scale:1.25},{opacity:1,scale:1,duration:0.24,ease:"power3.out"},t);');
  p(`  tl.to("#ring",{opacity:0,scale:0.85,duration:0.24,ease:"power2.in"},t+${(step * 0.9).toFixed(3)});`);
  p('  tl.fromTo(id,{opacity:0,scale:1.7},{opacity:1,scale:1,duration:0.22,ease:"back.out(2.4)"},t);');
  p(`  tl.to(id,{opacity:0,scale:0.6,duration:0.2,ease:"power2.in"},t+${(step * 0.92).toFixed(3)});`);
  p('});');
  p(`hide("#count", ${(S('tag') - 0.1).toFixed(3)}, 0.2);`);
}

/* --- FINAL TAG --- */
if (has('tag')) {
  const t = S('tag');
  p('');
  p('/* final */');
  p(`show("#finalCTA", ${(t - 0.08).toFixed(3)}, 0.25);`);
  p(`tl.fromTo("#finalCTA .ia",{opacity:0,scale:1.4},{opacity:1,scale:1,duration:0.34,ease:"back.out(2)"},${t.toFixed(3)});`);
  p(`tl.fromTo("#finalCTA .now",{opacity:0,y:20},{opacity:1,y:0,duration:0.3,ease:"power3.out"},${(t + 0.26).toFixed(3)});`);
  p(`tl.fromTo("#finalCTA .tag",{opacity:0,y:16},{opacity:1,y:0,duration:0.3},${(t + 0.46).toFixed(3)});`);
  p(`tl.to("#finalCTA .ia",{textShadow:"0 0 120px rgba(255,230,0,.7)",duration:0.4,yoyo:true,repeat:2},${(t + 0.4).toFixed(3)});`);
}

/* --- neon beat line (BGM ~134 BPM) --- */
p('');
p('const BEATP=0.448, BEAT0=0.04;');
p('for(let i=0,t=BEAT0;t<DUR-0.3;i++,t+=BEATP){');
p('  const down=(i%4===0);');
p('  tl.to("#neon-line",{scaleY:down?3.2:2.1,opacity:1,duration:0.07,ease:"power2.out"},t);');
p('  tl.to("#neon-line",{scaleY:1,opacity:0.82,duration:BEATP*0.62,ease:"power2.in"},t+0.07);');
p('}');

/* -------------------------------------------------------------- injection */
const outroH2 = (() => {
  const s = seg('outro');
  const txt = (s && s.display) || "L'IA avance chaque jour. Que tu suives ou pas.";
  const parts = txt.split(/(?<=[.!?])\s+/);
  const head = esc(parts[0] || txt);
  const tail = esc(parts.slice(1).join(' ') || '');
  return tail ? `${head}<br><b>${tail}</b>` : `<b>${head}</b>`;
})();

html = html
  .replace('/*{{ACCENT_CSS}}*/', accentCss)
  .replace('<!--{{BRIEFS}}-->', briefsHtml)
  .replace('<!--{{GAGS}}-->', gagsHtml)
  .replace('{{DATE_LABEL}}', esc(ed.dateLabel))
  .replace('{{OUTRO_H2}}', outroH2)
  .replace('{{MOT}}', esc(ed.mot))
  .replace('/*{{TIMING}}*/{}', JSON.stringify(tm.start))
  .replace('/*{{BUILD}}*/', L.join('\n'))
  .replace(/\{\{DURATION\}\}/g, String(tm.duration));

const left = html.match(/\{\{[A-Z_]+\}\}|<!--\{\{|\/\*\{\{/);
if (left) { console.error(`[build_html] placeholder non substitué: ${left[0]}`); process.exit(1); }

fs.writeFileSync(OUT, html);
/* avatar overlay plan consumed by pass 2 */
fs.writeFileSync(path.join(path.dirname(OUT), '..', 'work', 'avatar_windows.json'),
  JSON.stringify(avatarWindows.map((w) => ({ ...w, in: +w.in.toFixed(3), out: +w.out.toFixed(3) })), null, 2));
console.error(`[build_html] ${OUT} · ${ed.briefs.length} brèves · ${gagSegs.length} gags · ${avatarWindows.length} fenêtres avatar · ${tm.duration}s`);

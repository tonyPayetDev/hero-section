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
/* La carte d'intro n'était JAMAIS masquée : elle restait affichée sous la
   fenêtre avatar et le panneau d'actu pendant toute la vidéo. Invisible tant
   qu'un élément la couvrait, elle est réapparue le 29/08 dès qu'on a effacé
   l'avatar pour le coup à jouer. On la ferme là où elle se termine. */
p(`hide("#intro", ${(E('intro') - 0.15).toFixed(3)}, 0.3);`);
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

/* Le « coup à jouer » se DÉCOMPOSE en étapes, il ne se déverse plus en pavé.
 *
 * Le défaut corrigé (constaté sur l'édition du 29/08) : les trois phrases
 * étaient collées dans un seul <h2> à 60 px, posé à top:1480. Sur 45 mots ça
 * fait neuf lignes qui finissent vers 2080 px — le cadre s'arrête à 1920, donc
 * la phrase était coupée en plein milieu, à chaque édition, par construction.
 *
 * Maintenant : une phrase = une étape numérotée, et la taille s'adapte au
 * nombre de mots plutôt que de déborder. */
const outroPas = (() => {
  const s = seg('outro');
  const txt = (s && s.display) || "L'IA avance chaque jour. Que tu suives ou pas.";
  /* on coupe sur la ponctuation forte ; les tirets d'incise restent DANS
     l'étape, ils ne sont pas des séparateurs (une incise n'est pas une étape) */
  let parts = txt.split(/(?<=[.!?])\s+/).map((x) => x.trim()).filter(Boolean);
  /* une étape de plus de 26 mots est illisible : on la recoupe sur la virgule
     la plus proche du milieu plutôt que de la laisser déborder */
  parts = parts.flatMap((p) => {
    const mots = p.split(/\s+/);
    if (mots.length <= 26) return [p];
    /* Une incise entre tirets cadratins est INSÉCABLE. Couper dedans donne
       « … les agences immo de ta ville, » / « un secteur e-commerce — et … » :
       deux moitiés qui ne veulent rien dire (constaté le 29/08). On coupe donc
       en priorité juste APRÈS le tiret fermant. */
    const tirets = [...p.matchAll(/—/g)].map((m) => m.index);
    if (tirets.length >= 2) {
      /* L'incise devient sa PROPRE étape — elle porte les exemples concrets
         (« les agences immo de ta ville, un secteur e-commerce »), c'est-à-dire
         la partie la plus utile. Une première version la jetait purement et
         simplement : coupe silencieuse, aucune erreur levée. */
      const avant = p.slice(0, tirets[0]).trim().replace(/,$/, '');
      const incise = p.slice(tirets[0] + 1, tirets[1]).trim().replace(/^,|,$/g, '').trim();
      const apres = p.slice(tirets[1] + 1).trim().replace(/^et\s+/i, '');
      return [avant, incise ? `par exemple ${incise}` : '', apres].filter(Boolean);
    }
    /* sinon : la virgule la plus proche du milieu, mais jamais entre deux tirets */
    const dansIncise = (i) => tirets.length >= 2 && i > tirets[0] && i < tirets[1];
    const virgules = [...p.matchAll(/,\s+/g)].map((m) => m.index).filter((i) => !dansIncise(i));
    if (!virgules.length) return [p];
    const milieu = p.length / 2;
    const c = virgules.reduce((a, b) => (Math.abs(b - milieu) < Math.abs(a - milieu) ? b : a));
    return [p.slice(0, c + 1).trim(), p.slice(c + 1).trim()];
  });
  if (parts.length > 4) parts = parts.slice(0, 3).concat(parts.slice(3).join(' '));

  /* la taille suit la densité : plus il y a de mots, plus on descend, au lieu
     de garder 60 px et de sortir du cadre */
  const total = parts.join(' ').split(/\s+/).length;
  const taille = total > 55 ? 38 : total > 40 ? 44 : total > 26 ? 50 : 58;

  const li = parts.map((p, i) =>
    `<li class="pas" id="pas${i}"><span class="n">${i + 1}</span><span class="t">${esc(p)}</span></li>`).join('\n      ');
  return { html: `<ol class="pas-liste" style="font-size:${taille}px">\n      ${li}\n    </ol>`, n: parts.length };
})();
const outroH2 = outroPas.html;

/* --- OUTRO --- */
if (has('outro')) {
  p('');
  p('/* outro */');
  /* L'avatar SORT pendant le coup à jouer : c'est le moment où l'on montre le
     plan, pas le visage — et c'est lui qui occupait la bande dont les étapes
     ont besoin. Il revient sur le CTA. */
  p(`hide("#avatarWin", ${(S('outro') - 0.15).toFixed(3)}, 0.3);`);
  p(`tl.fromTo("#outro",{opacity:0,y:22},{opacity:1,y:0,duration:0.4,ease:"power3.out"},${S('outro').toFixed(3)});`);
  /* les étapes se posent une par une, réparties sur la durée du segment :
     on lit une consigne à la fois au lieu d'encaisser un pavé d'un coup */
  {
    const n = outroPas.n;
    const dispo = Math.max(0.9, (E('outro') - S('outro')) - 1.2);
    for (let i = 0; i < n; i++) {
      const t = S('outro') + 0.45 + (dispo * i) / n;
      p(`tl.fromTo("#pas${i}",{opacity:0,x:-26},{opacity:1,x:0,duration:0.34,ease:"back.out(1.5)"},${t.toFixed(3)});`);
    }
  }
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

html = html
  .replace('/*{{ACCENT_CSS}}*/', accentCss)
  .replace('<!--{{BRIEFS}}-->', briefsHtml)
  .replace('<!--{{GAGS}}-->', gagsHtml)
  .replace('{{DATE_LABEL}}', esc(ed.dateLabel))
  /* L'étiquette suit ce que le panneau porte vraiment : « Le coup à jouer »
     quand l'édition en propose un, « Ton résumé du jour » sinon. Annoncer un
     résumé au-dessus d'un conseil à appliquer trompe le spectateur. */
  .replace('{{OUTRO_LAB}}', seg('outro') && seg('outro').coup ? 'Le coup à jouer' : 'Ton résumé du jour')
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

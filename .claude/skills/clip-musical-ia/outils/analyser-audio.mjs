// Mesure la grille de beats ET les zones chantées du morceau.
//
// Deux mesures indépendantes, parce qu'elles répondent à deux questions
// différentes de Tony :
//   « la musique doit suivre l'avatar quand il chante »  → OÙ chante-t-il ?
//   « effets de saut d'écran quand il ne chante pas »     → et où NE chante-t-il pas ?
//
// Voix : on compare le canal MID (L+R, où la voix lead est mixée au centre)
// au canal SIDE (L-R, où vivent les nappes et les réverbs stéréo). Une voix
// lead pousse le ratio mid/side vers le haut ; un pont instrumental large le
// fait retomber. Ce n'est pas une séparation de sources, c'est un détecteur
// de présence — suffisant pour placer des coupes.
//
// Beats : énergie de la bande grosse caisse (< 160 Hz), pics détectés sur la
// dérivée positive de l'enveloppe, puis BPM par histogramme des intervalles.
import { readFileSync, writeFileSync } from 'node:fs';

const SR = 1000;                       // les .raw sont rééchantillonnés à 1 kHz
const lire = (f) => {
  const b = readFileSync(f);
  const n = Math.floor(b.length / 2);
  const x = new Float32Array(n);
  for (let i = 0; i < n; i++) x[i] = b.readInt16LE(i * 2) / 32768;
  return x;
};

// Enveloppe RMS par fenêtre de `ms` millisecondes.
const enveloppe = (x, ms) => {
  const w = Math.round((ms / 1000) * SR);
  const out = new Float32Array(Math.floor(x.length / w));
  for (let i = 0; i < out.length; i++) {
    let s = 0;
    for (let j = i * w; j < (i + 1) * w; j++) s += x[j] * x[j];
    out[i] = Math.sqrt(s / w);
  }
  return { env: out, pas: w / SR };
};

// ---------------------------------------------------------------- beats
const kick = lire('/work/clip-roule-kiki/work/kick.raw');
const { env: ek, pas: pasK } = enveloppe(kick, 10);   // 100 Hz de résolution

const flux = new Float32Array(ek.length);
for (let i = 1; i < ek.length; i++) flux[i] = Math.max(0, ek[i] - ek[i - 1]);

// Seuil adaptatif : médiane locale × facteur. Un seuil global raterait
// l'intro calme ou saturerait le drop.
const FEN = 100;                                       // ±1 s
const pics = [];
for (let i = 2; i < flux.length - 2; i++) {
  const a = Math.max(0, i - FEN), b = Math.min(flux.length, i + FEN);
  const loc = Array.from(flux.slice(a, b)).sort((p, q) => p - q);
  const med = loc[Math.floor(loc.length / 2)];
  const seuil = med * 3 + 0.0008;
  if (flux[i] > seuil && flux[i] >= flux[i - 1] && flux[i] > flux[i + 1]) {
    const t = i * pasK;
    if (!pics.length || t - pics[pics.length - 1] > 0.16) pics.push(t);
  }
}

// BPM : histogramme des intervalles, replié dans [0.3 s, 0.75 s] (80-200 BPM).
const inter = [];
for (let i = 1; i < pics.length; i++) {
  let d = pics[i] - pics[i - 1];
  while (d > 0.75) d /= 2;
  while (d < 0.3 && d > 0) d *= 2;
  if (d >= 0.3 && d <= 0.75) inter.push(d);
}
inter.sort((a, b) => a - b);
const periode = inter.length ? inter[Math.floor(inter.length / 2)] : 0.5;
const bpm = 60 / periode;

// ------------------------------------------------------------- voix
const mid = lire('/work/clip-roule-kiki/work/mid.raw');
const side = lire('/work/clip-roule-kiki/work/side.raw');
const { env: em, pas: pasV } = enveloppe(mid, 100);    // 10 Hz
const { env: es } = enveloppe(side, 100);

const ratio = new Float32Array(em.length);
for (let i = 0; i < em.length; i++) ratio[i] = em[i] / (es[i] + 1e-6);

// Lissage sur ~0,5 s : une syllabe isolée ne doit pas ouvrir un segment.
const liss = new Float32Array(ratio.length);
for (let i = 0; i < ratio.length; i++) {
  let s = 0, n = 0;
  for (let j = Math.max(0, i - 2); j <= Math.min(ratio.length - 1, i + 2); j++) { s += ratio[j]; n++; }
  liss[i] = s / n;
}

const tries = Array.from(liss).sort((a, b) => a - b);
const q = (p) => tries[Math.floor(tries.length * p)];
const seuilVoix = q(0.55);          // au-dessus de la médiane haute = chant

// Segments : on exige 1,2 s de continuité pour ouvrir, 1,2 s pour fermer.
const MIN = Math.round(1.2 / pasV);
const brut = Array.from(liss, (v) => (v > seuilVoix ? 1 : 0));
const seg = [];
let etat = brut[0], debut = 0;
for (let i = 1; i <= brut.length; i++) {
  if (i === brut.length || brut[i] !== etat) {
    const long = i - debut;
    if (long >= MIN || i === brut.length) {
      seg.push({ chante: !!etat, t0: +(debut * pasV).toFixed(2), t1: +(i * pasV).toFixed(2) });
      debut = i; etat = brut[i];
    }
  }
}
// Fusion des segments de même nature laissés côte à côte par la règle de durée.
const fusion = [];
for (const s of seg) {
  const p = fusion[fusion.length - 1];
  if (p && p.chante === s.chante) p.t1 = s.t1; else fusion.push({ ...s });
}

const chante = fusion.filter((s) => s.chante);
const instru = fusion.filter((s) => !s.chante);
const total = (a) => a.reduce((n, s) => n + (s.t1 - s.t0), 0);

console.log(`durée      ${(kick.length / SR).toFixed(2)} s`);
console.log(`BPM        ${bpm.toFixed(1)}  (période ${periode.toFixed(3)} s, ${pics.length} onsets)`);
console.log(`1er beat   ${pics[0]?.toFixed(3)} s`);
console.log(`\nchanté     ${chante.length} segments, ${total(chante).toFixed(1)} s`);
chante.forEach((s) => console.log(`   ${String(s.t0).padStart(6)} → ${String(s.t1).padStart(6)}   (${(s.t1 - s.t0).toFixed(1)} s)`));
console.log(`\ninstru     ${instru.length} segments, ${total(instru).toFixed(1)} s`);
instru.forEach((s) => console.log(`   ${String(s.t0).padStart(6)} → ${String(s.t1).padStart(6)}   (${(s.t1 - s.t0).toFixed(1)} s)`));

writeFileSync('/work/clip-roule-kiki/work/audio.json', JSON.stringify({
  duree: kick.length / SR, bpm, periode, premierBeat: pics[0] || 0,
  onsets: pics.map((t) => +t.toFixed(3)), segments: fusion,
}, null, 2));
console.log('\n→ work/audio.json');

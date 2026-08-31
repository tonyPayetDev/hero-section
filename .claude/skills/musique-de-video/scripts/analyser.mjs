// Mesure le tempo et la grille de temps d'une piste audio.
//
// C'est la sortie qui sert vraiment : caler des coupes, un texte ou un flash
// sur le beat demande la POSITION des temps, pas seulement le BPM.
//
// MÉTHODE : on ne mesure pas sur la bande complète mais sur la BANDE DU KICK
// (sous 150 Hz). La grosse caisse porte le temps ; les voix, les cuivres et les
// nappes ajoutent de l'énergie hors-tempo qui brouille la détection.
//
// ⚠️ DEUX PIÈGES FFMPEG QUI RENDENT UN RÉSULTAT FAUX SANS ERREUR :
//
// 1. `-ar` est une option de SORTIE : elle ne s'applique PAS avant
//    `asetnsamples`. Sur une source 44,1 kHz, des fenêtres de N échantillons
//    restent à 44,1 kHz — la cadence réelle n'est pas celle qu'on croit, et
//    la dérive atteint plusieurs secondes en fin de fichier. On met donc
//    `aresample=48000` DANS la chaîne de filtres, et surtout on REDÉDUIT la
//    cadence depuis le nombre de fenêtres obtenues.
// 2. Un filtre du type `=-?[0-9.]*$` ne matche pas `-inf` : les fenêtres de
//    silence sont SUPPRIMÉES au lieu d'être mises à zéro, et tous les index
//    suivants se décalent. On accepte explicitement `-inf` et on le mappe.
import { execSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const FF = '/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static';
const fichier = process.argv[2];
if (!fichier) { console.log('usage: analyser.mjs <audio.wav> [sortie.json]'); process.exit(1); }
const sortie = process.argv[3] || fichier.replace(/\.[^.]+$/, '') + '-analyse.json';

const duree = Number(execSync(
  `${FF}/ffprobe -v error -show_entries format=duration -of csv=p=0 "${fichier}"`).toString().trim());

// Enveloppe d'énergie sur la bande du kick, ~86 fenêtres par seconde.
const N = 512;
const brut = execSync(
  `${FF}/ffmpeg -v error -i "${fichier}" -map 0:a ` +
  `-af "aresample=44100,lowpass=f=150,asetnsamples=n=${N}:p=0,astats=metadata=1:reset=1,` +
  `ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null - 2>/dev/null`,
  { maxBuffer: 1 << 28 }).toString();

// On accepte -inf, sinon les silences disparaissent et tout se décale.
const vals = [...brut.matchAll(/=(-?inf|-?\d+(?:\.\d+)?)\s*$/gm)]
  .map((m) => (m[1].includes('inf') ? -99 : Number(m[1])));
if (vals.length < 20) { console.log('  trop peu de fenêtres — piste muette ?'); process.exit(1); }

// La cadence est DÉDUITE, jamais supposée.
const parSec = vals.length / duree;

// Détection d'attaques : une montée franche par rapport à la fenêtre glissante.
const moyGliss = [];
const W = Math.round(parSec * 0.6);
for (let i = 0; i < vals.length; i++) {
  const a = Math.max(0, i - W), b = Math.min(vals.length, i + W);
  moyGliss.push(vals.slice(a, b).reduce((x, y) => x + y, 0) / (b - a));
}
const attaques = [];
for (let i = 2; i < vals.length - 1; i++) {
  const monte = vals[i] - vals[i - 2];
  if (vals[i] > moyGliss[i] + 2.5 && monte > 3 && vals[i] >= vals[i + 1] && vals[i] > -45) {
    if (!attaques.length || i - attaques[attaques.length - 1] > parSec * 0.22) attaques.push(i);
  }
}

// Intervalles entre attaques → tempo. On prend la MÉDIANE des intervalles
// plausibles (0,3 à 1,2 s = 50 à 200 BPM) : une moyenne se fait emporter par
// un intervalle manqué, qui vaut le double des autres.
const ecarts = [];
for (let i = 1; i < attaques.length; i++) {
  const s = (attaques[i] - attaques[i - 1]) / parSec;
  if (s > 0.3 && s < 1.2) ecarts.push(s);
}
const med = (a) => { const s = [...a].sort((x, y) => x - y); const n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };

let bpm = null, periode = null;
if (ecarts.length >= 6) {
  periode = med(ecarts);
  bpm = 60 / periode;
  // Ramener dans la fourchette usuelle : un tempo mesuré à 65 est souvent
  // du 130 dont une attaque sur deux a été manquée.
  while (bpm < 70) bpm *= 2;
  while (bpm > 180) bpm /= 2;
  periode = 60 / bpm;
}

// Grille de temps : on cale la phase sur l'attaque qui minimise l'écart
// à l'ensemble des attaques détectées.
let phase = 0, grille = [];
if (bpm) {
  let meilleur = Infinity;
  for (const a of attaques.slice(0, 40)) {
    const t0 = a / parSec;
    let err = 0;
    for (const b of attaques) {
      const t = b / parSec;
      const d = Math.abs(((t - t0) % periode + periode) % periode);
      err += Math.min(d, periode - d);
    }
    if (err < meilleur) { meilleur = err; phase = t0; }
  }
  phase = phase % periode;
  for (let t = phase; t < duree; t += periode) grille.push(+t.toFixed(3));
}

// Courbe d'énergie par seconde — dit où sont les montées et les respirations.
const parSeconde = [];
for (let s = 0; s < Math.floor(duree); s++) {
  const a = Math.round(s * parSec), b = Math.round((s + 1) * parSec);
  const t = vals.slice(a, b).filter((x) => x > -90);
  parSeconde.push(t.length ? +(t.reduce((x, y) => x + y, 0) / t.length).toFixed(1) : -99);
}

const res = {
  fichier, duree: +duree.toFixed(2),
  fenetresParSeconde: +parSec.toFixed(2),
  attaquesDetectees: attaques.length,
  bpm: bpm ? +bpm.toFixed(1) : null,
  periodeBeat: periode ? +periode.toFixed(4) : null,
  phase: +phase.toFixed(3),
  grilleBeats: grille,
  energieParSeconde: parSeconde,
};
writeFileSync(sortie, JSON.stringify(res, null, 1));

console.log(`  durée ${res.duree}s · ${vals.length} fenêtres · cadence déduite ${res.fenetresParSeconde}/s`);
console.log(`  attaques détectées : ${res.attaquesDetectees}`);
if (bpm) {
  console.log(`  TEMPO : ${res.bpm} BPM · un temps toutes les ${res.periodeBeat}s · premier temps à ${res.phase}s`);
  console.log(`  grille : ${grille.length} temps écrits dans ${sortie}`);
} else {
  console.log('  tempo non déterminé — pas assez d attaques régulières (musique sans percussion ?)');
}
const max = Math.max(...parSeconde.filter((x) => x > -90));
const forts = parSeconde.map((v, i) => ({ v, i })).filter((x) => x.v > max - 3).map((x) => x.i);
if (forts.length) console.log(`  pics d énergie vers : ${forts.slice(0, 8).join('s, ')}s`);

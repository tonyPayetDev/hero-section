// Consolide la détection brute en structure de morceau exploitable au montage.
//
// Le détecteur de voix bascule à la moindre respiration : sur un chant
// scandé (« roule kiki » lancé par salves), il produit une alternance
// chanté/instru de 1,2 s qui n'a aucun sens de montage. Personne ne coupe
// toutes les 1,2 s pendant un couplet.
//
// On comble donc les trous instrumentaux courts (< 2,4 s = une mesure) : ce
// sont des respirations À L'INTÉRIEUR d'un couplet, pas des ponts. Ce qui
// survit est la vraie carte du morceau — et c'est elle qui décide où l'image
// suit le chant et où elle part en glitch.
import { readFileSync, writeFileSync } from 'node:fs';

const a = JSON.parse(readFileSync('/work/clip-roule-kiki/work/audio.json', 'utf8'));

// Le tempo mesuré (166,7) est du double-temps : les onsets comptent aussi les
// contretemps. Le pouls dansé est la moitié, et la mesure vaut 4 pouls.
const bpm = a.bpm / 2;
const pouls = 60 / bpm;
const mesure = pouls * 4;

const COMBLE = mesure;            // un trou d'une mesure ou moins = respiration

let s = a.segments.map((x) => ({ ...x }));
for (let i = 1; i < s.length - 1; i++) {
  if (!s[i].chante && s[i].t1 - s[i].t0 <= COMBLE && s[i - 1].chante && s[i + 1].chante) {
    s[i].chante = true;
  }
}
const bloc = [];
for (const x of s) {
  const p = bloc[bloc.length - 1];
  if (p && p.chante === x.chante) p.t1 = x.t1; else bloc.push({ ...x });
}

// On jette les miettes restantes (< 1 mesure) en les absorbant dans le voisin.
const net = [];
for (const x of bloc) {
  const d = x.t1 - x.t0;
  if (d < mesure && net.length) { net[net.length - 1].t1 = x.t1; continue; }
  net.push({ ...x });
}

const nom = (x, i) => {
  const d = x.t1 - x.t0;
  if (!x.chante && x.t0 === 0) return 'INTRO';
  if (!x.chante && x.t1 >= a.duree - 0.5) return 'OUTRO';
  if (!x.chante) return d > 5 ? 'BREAK' : 'PONT';
  return d > 8 ? 'REFRAIN' : 'COUPLET';
};

console.log(`BPM dansé  ${bpm.toFixed(1)}   pouls ${pouls.toFixed(3)} s   mesure ${mesure.toFixed(3)} s`);
console.log(`durée      ${a.duree.toFixed(2)} s  =  ${(a.duree / mesure).toFixed(1)} mesures\n`);
let chanteT = 0, instruT = 0;
net.forEach((x, i) => {
  const d = x.t1 - x.t0;
  x.chante ? (chanteT += d) : (instruT += d);
  console.log(`${String(nom(x, i)).padEnd(8)} ${String(x.t0.toFixed(1)).padStart(6)} → ${String(x.t1.toFixed(1)).padStart(6)}   ${d.toFixed(1).padStart(5)} s   ${(d / mesure).toFixed(1)} mes.`);
});
console.log(`\nchanté ${chanteT.toFixed(1)} s   ·   instru ${instruT.toFixed(1)} s`);

writeFileSync('/work/clip-roule-kiki/work/structure.json', JSON.stringify({
  bpm, pouls, mesure, duree: a.duree,
  blocs: net.map((x, i) => ({ nom: nom(x, i), chante: x.chante, t0: +x.t0.toFixed(2), t1: +x.t1.toFixed(2) })),
}, null, 2));
console.log('→ work/structure.json');

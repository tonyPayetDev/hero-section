// Déroule les SECTIONS en une liste de plans datés. Rien n'est rendu ici :
// cette étape existe pour pouvoir LIRE le montage avant de dépenser un rendu
// dessus — et la première lecture a justement fait jeter une première version.
//
// Ce qu'elle a montré : découper les refrains en cases égales d'une mesure
// (2,87 s) obligeait 26 plans sur 67 à passer en ralenti — jusqu'à 0,48× —
// parce que les extraits où il chante durent 1,1 à 1,6 s, pas 2,9. Un ralenti
// à 0,5× sur une bouche qui chante, ça se voit immédiatement : le playback
// décroche.
//
// Donc l'inverse : la durée de la SOURCE décide, et on l'aimante sur la
// grille rythmique la plus proche. La musique reste le métronome, mais elle
// ne force plus les plans à s'étirer.
//
//   CHANTÉ  → 3 à 6 demi-temps (1,08 à 2,15 s)
//   INSTRU  → 2 à 4 demi-temps (0,72 à 1,44 s) — le montage se resserre
//             pile là où il n'y a plus de voix à suivre
//
// La vitesse résiduelle reste dans [0,72 ; 1,00] : un ralenti léger passe
// inaperçu et flatte même une source générée. En dessous, non.
import { PLANS, SECTIONS, CLIPS, BEAT } from './edl.mjs';

const GRILLE = BEAT / 2;              // 0,3588 s — le demi-temps
const V_MIN = 0.72;                   // ralenti maximal toléré

// Choisit le nombre de demi-temps qui colle le mieux à la durée de la source.
function caser(source, kMin, kMax) {
  let best = null;
  for (let k = kMin; k <= kMax; k++) {
    const slot = k * GRILLE;
    const v = source / slot;                       // >1 : on coupe dans la source
    const vEff = Math.min(v, 1);
    if (vEff < V_MIN) continue;                    // trop de ralenti, on écarte
    const cout = Math.abs(Math.log(v));            // le plus proche de ×1
    if (!best || cout < best.cout) best = { k, slot, vitesse: +vEff.toFixed(3), cout };
  }
  // Aucune case ne convient (source très courte) : on prend la plus petite et
  // on assume le ralenti, en le signalant.
  if (!best) {
    const slot = kMin * GRILLE;
    best = { k: kMin, slot, vitesse: +Math.min(source / slot, 1).toFixed(3), cout: 9 };
  }
  return best;
}

// Pas de parcours du vivier de plans. Il doit être PREMIER avec la taille du
// vivier, sinon la suite dégénère : un pas de 3 sur un vivier de 3 renvoie
// toujours le même plan — c'est exactement ce qu'a produit la première
// version, qui affichait trois fois de suite le plan large de l'intro.
const pgcd = (a, b) => (b ? pgcd(b, a % b) : a);
function pas(n) {
  if (n <= 2) return 1;
  const co = [];
  for (let s = 1; s < n; s++) if (pgcd(s, n) === 1) co.push(s);
  // Le plus proche de n/2 : c'est celui qui éloigne le plus deux passages
  // successifs sur le même plan.
  return co.sort((a, b) => Math.abs(a - n / 2) - Math.abs(b - n / 2) || b - a)[0];
}

export function construirePlan() {
  const sortie = [];
  for (const s of SECTIONS) {
    const [kMin, kMax] = s.k || (s.chante ? [3, 6] : [2, 4]);
    const n = s.plans.length;
    let t = s.t0, i = 0;
    while (t < s.t1 - 0.12) {
      // Pas un simple `i % n` : une section plus longue que son vivier
      // rejouerait la même suite de plans dans le même ordre, et l'oeil
      // repère cette boucle bien avant la fin du refrain. Le pas de 3
      // combiné à la rotation par cycle donne un ordre différent à chaque
      // tour tout en gardant chaque plan à égalité de temps d'écran.
      let j = (i * pas(n) + Math.floor(i / n)) % n;
      // Garde-fou : sur un vivier de 2 ou 3, le terme de rotation peut
      // ramener le plan qui vient d'être posé. Deux fois la même image bout
      // à bout se lit comme un bug de montage, pas comme un effet.
      const prec = sortie[sortie.length - 1];
      if (n > 1 && prec && prec.id === s.plans[j]) j = (j + 1) % n;
      const id = s.plans[j];
      const p = PLANS[id];
      if (!p) throw new Error(`plan inconnu : ${id}`);
      const source = p.t1 - p.t0;
      let { slot, vitesse } = caser(source, kMin, kMax);

      // Le dernier plan de la section est rogné pour tomber pile sur t1 :
      // une section qui déborde décalerait toutes les suivantes.
      if (t + slot > s.t1) slot = s.t1 - t;
      if (slot < 0.25 && sortie.length) { sortie[sortie.length - 1].duree += slot; break; }

      sortie.push({
        id, section: s.nom, chante: s.chante,
        t0: +t.toFixed(3), duree: +slot.toFixed(3),
        fichier: CLIPS[p.clip], clip: p.clip,
        src0: p.t0, srcDuree: +source.toFixed(2),
        cadre: p.cadre || { type: 'portrait' },
        vitesse,
        traitement: s.chante ? (slot <= 4 * GRILLE ? 'punch' : 'net') : 'saut',
      });
      t += slot; i++;
    }
    // Recale au millième sur la fin de section : un reliquat de 90 ms laissé
    // par la boucle devient une image noire au montage, et décale tout ce qui
    // suit par rapport à la musique.
    const dernier = sortie[sortie.length - 1];
    dernier.duree = +(s.t1 - dernier.t0).toFixed(3);
  }
  return sortie;
}

if ((process.argv[1] || '').endsWith('plan.mjs')) {
  const p = construirePlan();
  let sec = null;
  for (const x of p) {
    if (x.section + x.t0 !== sec && (!sec || !sec.startsWith(x.section))) {
      console.log(`\n── ${x.section}  ${x.chante ? 'CHANTÉ' : 'instru'} `.padEnd(58, '─'));
    }
    sec = x.section + x.t0;
    const a = x.vitesse < V_MIN ? '  ⚠ ralenti' : '';
    console.log(
      `${String(x.t0.toFixed(2)).padStart(7)} +${x.duree.toFixed(2)}s  ${x.id.padEnd(5)} ` +
      `${x.clip} @${x.src0.toFixed(1)}  ${x.cadre.type.padEnd(11)} ${x.traitement.padEnd(6)} ×${x.vitesse}${a}`);
  }
  const fin = p[p.length - 1];
  console.log(`\n${p.length} plans · fin à ${(fin.t0 + fin.duree).toFixed(2)} s`);
  const parClip = {};
  p.forEach((x) => { parClip[x.clip] = (parClip[x.clip] || 0) + x.duree; });
  console.log('temps d\'écran par clip source :');
  Object.entries(parClip).sort((a, b) => b[1] - a[1])
    .forEach(([c, d]) => console.log(`   ${c}  ${String(d.toFixed(1)).padStart(5)} s  ${(d / 150 * 100).toFixed(0)} %`));
  const lents = p.filter((x) => x.vitesse < V_MIN);
  console.log(lents.length ? `\n⚠ ${lents.length} plans en ralenti fort : ${lents.map((x) => x.id).join(', ')}`
                           : '\n✓ aucun ralenti fort — tous les plans entre ×0,72 et ×1');
  // Contrôle de continuité : un trou entre deux plans = une image noire.
  let trous = 0;
  for (let i = 1; i < p.length; i++) {
    const d = p[i].t0 - (p[i - 1].t0 + p[i - 1].duree);
    if (Math.abs(d) > 0.005) { trous++; console.log(`  ⚠ trou de ${d.toFixed(3)}s à ${p[i].t0}`); }
  }
  if (!trous) console.log('✓ timeline continue, aucun trou');
}

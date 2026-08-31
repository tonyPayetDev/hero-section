// Rend le clip : un fichier par plan, puis concaténation.
//
// Un seul graphe ffmpeg de 109 plans serait impossible à déboguer — une
// erreur de syntaxe dans le 84e plan ferait perdre le rendu entier. Ici
// chaque plan est un MP4 autonome, encodé aux mêmes paramètres, donc la
// concaténation finale est une copie de flux : instantanée, et un plan raté
// se refait seul.
//
// Deux formats, deux traitements du cadre, pas un recadrage automatique :
//   9:16  les cinq clips portrait remplissent l'écran ; le clip de scène
//         (le seul en 16:9) passe en bandeau sur fond flouté.
//   16:9  l'inverse exactement — le clip de scène passe PLEIN CADRE, les
//         portraits sont posés en panneau central. Les moments « live »
//         s'ouvrent donc en grand sur YouTube et se resserrent sur TikTok.
//         C'est une intention de montage, pas un rattrapage de format.
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { construirePlan } from './plan.mjs';
import { BEAT } from './edl.mjs';

const RACINE = '/work/clip-roule-kiki';
const FFMPEG = '/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static/ffmpeg';
const FPS = 24;
const PREMIER_TEMPS = 6.40;      // relevé sur les pics d'énergie (cf. audio.sh)

const FORMATS = {
  '9x16': { L: 1080, H: 1920, dossier: 'seg916' },
  '16x9': { L: 1920, H: 1080, dossier: 'seg169' },
};

// Suite déterministe : deux rendus du même plan donnent le même mouvement.
const graine = (s) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return ((h >>> 0) % 10000) / 10000;
};

// ---------------------------------------------------------------- géométrie
// Amène la source à un cadre de travail plus grand que la sortie : c'est
// cette marge qui rend le mouvement possible sans jamais découvrir de bord.
function cadrage(p, F) {
  const marge = 1.15;
  const L = Math.round(F.L * marge / 2) * 2;
  const H = Math.round(F.H * marge / 2) * 2;

  if (p.cadre.type === 'portrait16') {
    // En 16:9 le plan de scène est déjà au bon format : il passe plein cadre.
    // (Sans ce test, la largeur calculée valait la largeur entière de la
    // source et ffmpeg ramenait x à 0 tout seul — même résultat, mais par
    // accident plutôt que par décision.)
    if (F.L > F.H) return `scale=${L}:${H}:flags=lanczos`;
    // En 9:16 : extrait portrait pris DANS le plan large. Le décalage x est
    // relevé image par image — cadrer au centre couperait le micro ou la
    // tête selon la seconde.
    const larg = Math.round((720 * F.L) / F.H / 2) * 2;
    return `crop=${larg}:720:${p.cadre.x}:0,scale=${L}:${H}:flags=lanczos,unsharp=5:5:0.7`;
  }
  if (p.cadre.type === 'bandeau16') {
    // Le plan large gardé large : fond flouté tiré de lui-même, bandeau net
    // par-dessus. En 16:9 la question ne se pose pas — il remplit l'écran.
    if (F.L > F.H) return `scale=${L}:${H}:flags=lanczos`;
    // Bandeau tiré d'un recadrage 4:3 et non du 16:9 entier : à pleine
    // largeur le bandeau ne fait que 608 px sur 1920, soit un tiers de
    // l'écran, et les deux tiers restants sont un fond flouté quasi noir —
    // vérifié sur la première image du clip, qui s'ouvrait sur du vide.
    // En 4:3 le bandeau monte à 810 px et la scène reste lisible.
    const hb = Math.round((F.L * 720) / 960 / 2) * 2;
    return `split[bg][fg];`
      + `[bg]scale=${L}:${H}:force_original_aspect_ratio=increase,crop=${L}:${H},`
      + `gblur=sigma=30,eq=brightness=-0.08:saturation=0.75[b];`
      + `[fg]crop=960:720:160:0,scale=${F.L}:${hb}:flags=lanczos,unsharp=5:5:0.5[f];`
      + `[b][f]overlay=x=(W-w)/2:y=(H-h)/2`;
  }
  // Source portrait.
  if (F.L > F.H) {
    // En 16:9 : panneau central à hauteur pleine + fond flouté. Un recadrage
    // en 16:9 dans une source 9:16 couperait la tête ou les pieds à tous les
    // coups — mesuré sur les six clips.
    const lp = Math.round((F.H * 720) / 1280 / 2) * 2;
    return `split[bg][fg];`
      + `[bg]scale=${L}:${H}:force_original_aspect_ratio=increase,crop=${L}:${H},`
      + `gblur=sigma=34,eq=brightness=-0.14:saturation=0.68[b];`
      + `[fg]scale=${lp}:${F.H}:flags=lanczos[f];`
      + `[b][f]overlay=x=(W-w)/2:y=(H-h)/2`;
  }
  return `scale=${L}:${H}:flags=lanczos`;
}

// ---------------------------------------------------------------- mouvement
function mouvement(p, F, i) {
  const g1 = graine(p.id + i), g2 = graine(i + p.id);
  const D = p.duree;
  // Décalage de phase : dans un segment, `t` repart de zéro. Sans ce report
  // du temps global, les sauts d'écran tomberaient à côté du beat.
  const off = ((p.t0 - PREMIER_TEMPS) % BEAT + BEAT) % BEAT;

  if (p.traitement === 'saut') {
    // « effets de saut d'écran stylé quand il ne chante pas » : l'image se
    // déplace d'un bloc à chaque temps et y RESTE — c'est un saut, pas une
    // vibration. floor(t/BEAT) tient la position pendant tout le temps.
    const s = (a) => `sin(floor((t+${off.toFixed(3)})/${BEAT})*${a}+${(g1 * 6).toFixed(2)})`;
    return `crop=${F.L}:${F.H}:`
      + `x='(iw-ow)*(0.5+0.42*${s(12.9)})':`
      + `y='(ih-oh)*(0.5+0.35*${s(7.7)})',`
      + `rgbashift=rh=18:bh=-18:enable='lt(mod(t+${off.toFixed(3)},${BEAT}),0.12)',`
      + `eq=brightness=0.16:contrast=1.2:enable='lt(mod(t+${off.toFixed(3)},${(BEAT * 2).toFixed(4)}),0.04)'`;
  }

  // Chanté : dérive lente et continue. Le regard reste sur la bouche.
  const amp = p.traitement === 'punch' ? 0.42 : 0.26;
  const ax = 0.5 + (g1 - 0.5) * amp, bx = 0.5 - (g1 - 0.5) * amp;
  const ay = 0.5 + (g2 - 0.5) * amp, by = 0.5 - (g2 - 0.5) * amp;
  const r = (v) => v.toFixed(3);
  return `crop=${F.L}:${F.H}:`
    + `x='(iw-ow)*(${r(ax)}+${r(bx - ax)}*min(1,t/${D.toFixed(3)}))':`
    + `y='(ih-oh)*(${r(ay)}+${r(by - ay)}*min(1,t/${D.toFixed(3)}))'`;
}

// ---------------------------------------------------------------- un plan
function rendrePlan(p, i, F, dossier) {
  const out = `${dossier}/${String(i).padStart(3, '0')}.mp4`;
  if (existsSync(out)) return out;

  const prise = p.duree * p.vitesse;                  // secondes de source consommées
  const geo = cadrage(p, F);
  const mvt = mouvement(p, F, i);
  const vit = p.vitesse === 1 ? '' : `,setpts=PTS/${p.vitesse}`;

  // Quand la géométrie contient un overlay, elle se termine par un flux
  // nommé implicite : on enchaîne avec une virgule, pas avec un point-virgule.
  const chaine = `[0:v]fps=${FPS}${vit},${geo},${mvt},format=yuv420p[v]`;

  execFileSync(FFMPEG, [
    '-v', 'error', '-y',
    '-ss', String(p.src0), '-t', String((prise + 0.2).toFixed(3)),
    '-i', `${RACINE}/${p.fichier}`,
    '-filter_complex', chaine, '-map', '[v]',
    '-t', String(p.duree.toFixed(3)),
    '-r', String(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17',
    '-pix_fmt', 'yuv420p', '-an', out,
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  return out;
}

// ---------------------------------------------------------------- pilote
const cible = process.argv[2] || '9x16';
const F = FORMATS[cible];
if (!F) throw new Error(`format inconnu : ${cible}`);
const dossier = `${RACINE}/work/${F.dossier}`;
mkdirSync(dossier, { recursive: true });

const plan = construirePlan();
console.log(`${cible} · ${plan.length} plans → ${F.L}x${F.H}`);
const t0 = Date.now();
const liste = [];
plan.forEach((p, i) => {
  try {
    liste.push(rendrePlan(p, i, F, dossier));
  } catch (e) {
    const err = (e.stderr || Buffer.from('')).toString().trim().split('\n').slice(-3).join(' | ');
    console.log(`✗ plan ${i} (${p.id} @${p.t0}) : ${err}`);
    throw e;
  }
  if ((i + 1) % 20 === 0) console.log(`   ${i + 1}/${plan.length}  (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
});

writeFileSync(`${dossier}/liste.txt`, liste.map((f) => `file '${f}'`).join('\n'));
const brut = `${RACINE}/work/brut-${cible}.mp4`;
execFileSync(FFMPEG, ['-v', 'error', '-y', '-f', 'concat', '-safe', '0',
  '-i', `${dossier}/liste.txt`, '-c', 'copy', brut], { stdio: 'inherit' });

const dur = execFileSync('/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static/ffprobe',
  ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', brut]).toString().trim();
console.log(`✓ ${brut}  ${dur} s  (${((Date.now() - t0) / 1000).toFixed(0)} s de rendu)`);

// Assemblage final : image brute + ligne réactive + cartons + son.
//
// La « ligne réactive » est la lecture littérale de la demande — « la music
// doit suivre l'avatar quand il chante ». Le montage y répond déjà par le
// choix des plans (aucun plan muet sur un bloc chanté) ; cette ligne le rend
// VISIBLE : une onde tirée de la bande son elle-même, allumée uniquement
// pendant les blocs chantés, éteinte pendant les breaks où le glitch prend
// le relais. Elle n'est pas décorative, elle est la forme d'onde du fichier.
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';

const R = '/work/clip-roule-kiki';
const FF = '/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static/ffmpeg';
const FP = '/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static/ffprobe';

// Relevés dans edl.mjs : les bornes des blocs où il y a de la voix.
const CHANTE = [
  [5.30, 8.90], [12.10, 35.50], [44.10, 50.90], [56.40, 77.30],
  [83.15, 106.55], [115.15, 121.95], [127.45, 148.35],
];
const allume = CHANTE.map(([a, b]) => `between(t,${a},${b})`).join('+');

const FORMATS = {
  '9x16': { L: 1080, H: 1920, onde: 130 },
  '16x9': { L: 1920, H: 1080, onde: 104 },
};

// Le titre s'installe sur l'intro instrumentale et sort avant la 1re phrase
// chantée (5,30 s) : un carton encore à l'écran quand la voix démarre vole
// l'attention au seul moment où on veut regarder sa bouche.
const T_IN = 0.55, T_OUT = 4.85, T_FADE = 0.55;
const A_IN = 1.55, A_OUT = 4.85;
// Le CTA monte pendant le dernier refrain, pas après : posé sur le silence
// final il n'aurait plus de musique pour le porter.
const C_IN = 143.6, C_FADE = 0.9;

const cible = process.argv[2] || '9x16';
const F = FORMATS[cible];
const brut = `${R}/work/brut-${cible}.mp4`;
if (!existsSync(brut)) throw new Error(`manque ${brut} — lancer rendre.mjs ${cible} d'abord`);

const sortie = `${R}/roule-kiki-${cible}.mp4`;
const fondu = (st, d, sens) => `fade=t=${sens}:st=${st}:d=${d}:alpha=1`;

const graphe = [
  // Onde tirée du VRAI fichier son, pas d'une animation générique.
  `[1:a]showwaves=s=${F.L}x${F.onde}:mode=cline:rate=24:colors=0xFF7A18|0xA855F7,`
  + `format=rgba,colorchannelmixer=aa=0.62[onde]`,
  // `screen` plutôt qu'un overlay : le noir de showwaves disparaît de
  // lui-même, sans détourage ni colorkey à régler.
  `[0:v][onde]overlay=x=0:y=H-h-${cible === '9x16' ? 26 : 14}:`
  + `enable='${allume}':format=auto[v1]`,

  `[2:v]format=rgba,${fondu(T_IN, T_FADE, 'in')},${fondu(T_OUT, T_FADE, 'out')}[t]`,
  `[3:v]format=rgba,${fondu(A_IN, T_FADE, 'in')},${fondu(T_OUT, T_FADE, 'out')}[a]`,
  `[4:v]format=rgba,${fondu(C_IN, C_FADE, 'in')}[c]`,
  `[v1][t]overlay=0:0:enable='between(t,${T_IN},${T_OUT + T_FADE})'[v2]`,
  `[v2][a]overlay=0:0:enable='between(t,${A_IN},${T_OUT + T_FADE})'[v3]`,
  `[v3][c]overlay=0:0:enable='gte(t,${C_IN})',format=yuv420p[v]`,
].join(';');

console.log(`assemblage ${cible}…`);
execFileSync(FF, [
  '-v', 'error', '-y',
  '-i', brut,
  '-i', `${R}/work/bande-son.wav`,
  '-loop', '1', '-framerate', '24', '-i', `${R}/work/cartons/titre-${cible}.png`,
  '-loop', '1', '-framerate', '24', '-i', `${R}/work/cartons/artiste-${cible}.png`,
  '-loop', '1', '-framerate', '24', '-i', `${R}/work/cartons/cta-${cible}.png`,
  '-filter_complex', graphe,
  '-map', '[v]', '-map', '1:a',
  '-t', '150',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
  '-profile:v', 'high', '-level', '4.1', '-pix_fmt', 'yuv420p',
  '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
  '-movflags', '+faststart', sortie,
], { stdio: 'inherit' });

const info = execFileSync(FP, ['-v', 'error',
  '-show_entries', 'format=duration,size', '-show_entries', 'stream=codec_type,width,height,r_frame_rate',
  '-of', 'default=nw=1', sortie]).toString().trim().replace(/\n/g, '  ');
console.log(`✓ ${sortie}\n  ${info}`);

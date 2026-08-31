// Fabrique les incrustations (titre, nom d'artiste, CTA) en PNG transparents.
//
// Pourquoi pas `drawtext` : ce build de ffmpeg est compilé SANS libfreetype —
// `ffmpeg -filters | grep drawtext` renvoie zéro. Aucune incrustation de
// texte n'est possible côté ffmpeg. On passe donc par Chromium, ce qui vaut
// mieux de toute façon : lueur néon, crénage, interlettrage et superposition
// de calques sont natifs en CSS et illisibles en paramètres drawtext.
//
// Chaque élément est un fichier séparé — titre, artiste, filet — pour que le
// montage puisse les faire entrer en décalé. Un carton unique entrerait d'un
// bloc, ce qui ne ressemble à rien sur un clip.
import pw from '/work/autoboost-neon-videos/autoboost-23-design/node_modules/playwright/index.js';
import { readFileSync, mkdirSync } from 'node:fs';

process.env.LD_LIBRARY_PATH = [
  '/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu',
  '/home/claude/tools/chromelibs/lib/x86_64-linux-gnu',
].join(':');
process.env.FONTCONFIG_PATH = '/home/claude/tools/chromelibs/etc/fonts';

const POLICES = '/home/claude/.agents/skills/embedded-captions/modes/standard/fonts/files';
const b64 = (f) => readFileSync(`${POLICES}/${f}`).toString('base64');
const ANTON = b64('anton-latin-400-normal.woff2');
const CHAKRA = b64('chakra-petch-latin-700-normal.woff2');

// Palette relevée sur les clips eux-mêmes : orange des enseignes, violet des
// néons de rue, cyan de l'orbe. Rien d'inventé, la charte est dans l'image.
const ORANGE = '#FF7A18';
const VIOLET = '#A855F7';
const CYAN = '#5FD8FF';

const base = (L, H) => `
<style>
@font-face{font-family:Anton;src:url(data:font/woff2;base64,${ANTON}) format('woff2')}
@font-face{font-family:Chakra;font-weight:700;src:url(data:font/woff2;base64,${CHAKRA}) format('woff2')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${L}px;height:${H}px;background:transparent;overflow:hidden}
body{display:flex;position:relative}
.bloc{position:absolute}
.titre{font-family:Anton;color:#fff;line-height:.86;text-transform:lowercase;
  /* Trois lueurs empilées, de la plus serrée à la plus large : une seule
     ombre donne un halo plat, trois donnent la profondeur d'un vrai néon. */
  text-shadow:0 0 12px rgba(255,255,255,.85),
              0 0 38px ${ORANGE},
              0 0 90px ${VIOLET},
              0 6px 0 rgba(0,0,0,.35)}
.artiste{font-family:Chakra;font-weight:700;color:${CYAN};text-transform:lowercase;
  text-shadow:0 0 10px rgba(95,216,255,.9),0 0 32px ${VIOLET}}
.filet{background:linear-gradient(90deg,${ORANGE},${VIOLET} 55%,transparent);
  box-shadow:0 0 18px ${ORANGE}}
.socle{position:absolute;left:0;right:0;bottom:0;
  background:linear-gradient(180deg,transparent,rgba(0,0,0,.55) 62%,rgba(0,0,0,.78))}
</style>`;

const CARTONS = {
  // ---- titre d'ouverture : tiers inférieur, il ne couvre jamais un visage
  titre: (L, H, v) => `${base(L, H)}
<div class="socle" style="height:${v ? 720 : 400}px"></div>
<div class="bloc" style="left:${v ? 82 : 130}px;bottom:${v ? 430 : 190}px">
  <div class="filet" style="width:${v ? 210 : 240}px;height:5px;margin-bottom:${v ? 34 : 26}px"></div>
  <div class="titre" style="font-size:${v ? 172 : 130}px;letter-spacing:-.01em">roule kiki</div>
</div>`,

  artiste: (L, H, v) => `${base(L, H)}
<div class="bloc" style="left:${v ? 88 : 134}px;bottom:${v ? 352 : 132}px">
  <div class="artiste" style="font-size:${v ? 46 : 36}px;letter-spacing:.42em">ouwa</div>
</div>`,

  // ---- carton de fin : centré, c'est le seul moment où on demande quelque chose
  cta: (L, H, v) => `${base(L, H)}
<div class="socle" style="height:100%;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.72))"></div>
<div class="bloc" style="left:0;right:0;top:50%;transform:translateY(-50%);text-align:center">
  <div class="artiste" style="font-size:${v ? 34 : 28}px;letter-spacing:.5em;margin-bottom:${v ? 30 : 22}px">roule kiki &middot; ouwa</div>
  <div class="titre" style="font-size:${v ? 158 : 128}px">abonne-toi</div>
  <div class="filet" style="width:${v ? 300 : 340}px;height:5px;margin:${v ? 42 : 32}px auto 0;
       background:linear-gradient(90deg,transparent,${ORANGE},${VIOLET},transparent)"></div>
</div>`,
};

const FORMATS = [
  { nom: '9x16', L: 1080, H: 1920, v: true },
  { nom: '16x9', L: 1920, H: 1080, v: false },
];

mkdirSync('/work/clip-roule-kiki/work/cartons', { recursive: true });
const nav = await pw.chromium.launch({ args: ['--no-sandbox'] });
for (const f of FORMATS) {
  const pg = await nav.newPage({ viewport: { width: f.L, height: f.H } });
  for (const [nom, gen] of Object.entries(CARTONS)) {
    await pg.setContent(gen(f.L, f.H, f.v));
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(180);
    const out = `/work/clip-roule-kiki/work/cartons/${nom}-${f.nom}.png`;
    await pg.screenshot({ path: out, omitBackground: true });
    console.log(`  ${out}`);
  }
  await pg.close();
}
await nav.close();
console.log('✓ cartons rendus');

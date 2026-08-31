// Résout les liens de partage Higgsfield (/s/<slug>) vers le vrai MP4.
//
// La page /s/... est une SPA : ni balise <video>, ni meta og:video. Mais le
// payload TanStack est sérialisé DANS le HTML, et il contient une référence
// canonique `https://higgsfield.ai/share/<uuid>` pointant sur LE job partagé.
// C'est cet uuid qui identifie le clip — pas le premier .mp4 croisé dans la
// page, qui peut appartenir à une vignette de la galerie voisine.
import { writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const LIENS = [
  'https://higgsfield.ai/s/-vGOyNIgEGg',
  'https://higgsfield.ai/s/slCLZzCem_I',
  'https://higgsfield.ai/s/pFzYUF-f5V8',
  'https://higgsfield.ai/s/p_-_X1eZgAA',
  'https://higgsfield.ai/s/S1u-u9N5hjE',
  'https://higgsfield.ai/s/NXfhfMCslpY',
];

mkdirSync('/work/clip-roule-kiki/work/pages', { recursive: true });
const sortie = [];

for (const lien of LIENS) {
  const slug = lien.split('/').pop();
  let html;
  try {
    html = execFileSync('curl', ['-sL', '--max-time', '40', lien], {
      maxBuffer: 40 * 1024 * 1024, encoding: 'utf8',
    });
  } catch (e) { console.log(`${slug}  ✗ curl: ${e.message}`); continue; }
  writeFileSync(`/work/clip-roule-kiki/work/pages/${slug}.html`, html);

  const canon = html.match(/higgsfield\.ai\\?\/share\\?\/([0-9a-f-]{36})/);
  if (!canon) { console.log(`${slug}  ✗ pas d'uuid canonique`); continue; }
  const uuid = canon[1];

  // Le MP4 porte l'uuid dans son nom : hf_<date>_<uuid>.mp4
  const re = new RegExp(`https?:[^"'\\\\ ]*${uuid}\\.mp4`);
  const mp4 = (html.match(re) || [])[0];

  // Le prompt est stocké échappé ; on prend le plus long candidat, les
  // vignettes voisines ayant des prompts tronqués.
  const prompts = [...html.matchAll(/\\"prompt\\":\\"((?:[^"\\]|\\.){20,4000}?)\\"/g)]
    .map((m) => m[1]);
  const prompt = prompts.sort((a, b) => b.length - a.length)[0] || '';

  sortie.push({ slug, uuid, mp4: mp4 || null, prompt: prompt.slice(0, 2000) });
  console.log(`${slug}  → ${uuid}  ${mp4 ? '✓ mp4' : '✗ mp4 introuvable'}`);
}

writeFileSync('/work/clip-roule-kiki/work/clips.json', JSON.stringify(sortie, null, 2));
console.log(`\n${sortie.length}/${LIENS.length} liens résolus → work/clips.json`);

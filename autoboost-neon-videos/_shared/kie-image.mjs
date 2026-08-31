#!/usr/bin/env node
// Génération d'images via Kie.ai — remplace Higgsfield (décision Tony 2026-08-21).
//
// Pourquoi : Higgsfield facture 2 cr/image sur un solde qui était tombé à 9 ;
// Kie.ai facture 4 cr/image sur un solde de ~374, soit ~93 images. Et le
// verrouillage d'identité marche aussi bien (`image_urls` = référence).
//
//   node kie-image.mjs sortie.png "prompt" [url_de_reference] [ratio]
//
// Ratio par défaut 16:9. Sans URL de référence, on passe en génération pure.
// Contrat vérifié 2026-08-21 : createTask -> recordInfo, ~50 s, 4 crédits.
import fs from 'fs';
import { execSync } from 'child_process';

const CLE = (fs.readFileSync('/work/.kie.env', 'utf8').match(/[A-Za-z0-9_-]{30,}/) || [])[0];
if (!CLE) { console.error('clé Kie.ai introuvable dans /work/.kie.env'); process.exit(1); }

const [sortie, prompt, ref, ratio = '16:9'] = process.argv.slice(2);
if (!sortie || !prompt) { console.error('usage: kie-image.mjs sortie.png "prompt" [ref_url] [ratio]'); process.exit(1); }

const api = async (url, opts = {}) => {
  const r = await fetch(url, {
    ...opts,
    headers: { Authorization: `Bearer ${CLE}`, 'Content-Type': 'application/json', ...(opts.headers || {}) },
  });
  return r.json();
};

// nano-banana-edit quand il y a une référence (verrouille le visage),
// nano-banana sinon.
const modele = ref ? 'google/nano-banana-edit' : 'google/nano-banana';
const input = { prompt, output_format: 'png', image_size: ratio };
if (ref) input.image_urls = [ref];

const cree = await api('https://api.kie.ai/api/v1/jobs/createTask', {
  method: 'POST',
  body: JSON.stringify({ model: modele, input }),
});
const tid = cree?.data?.taskId;
if (!tid) { console.error('createTask a échoué :', JSON.stringify(cree).slice(0, 300)); process.exit(1); }

// Le job met ~50 s. On sonde sans inonder l'API.
let url = null;
for (let i = 0; i < 40; i++) {
  await new Promise(r => setTimeout(r, 8000));
  const info = await api(`https://api.kie.ai/api/v1/jobs/recordInfo?taskId=${tid}`);
  const etat = info?.data?.state;
  if (etat === 'success') {
    // resultJson porte l'URL ; on la prend sans se fier à une forme exacte.
    const m = JSON.stringify(info).match(/https:\/\/[^"\\]+?\.(?:png|jpg|jpeg)/g) || [];
    url = m.find(u => !u.includes('cloudfront')) || m[0];
    break;
  }
  if (etat === 'fail' || etat === 'failed') {
    console.error('génération échouée :', JSON.stringify(info).slice(0, 400));
    process.exit(1);
  }
}
if (!url) { console.error('délai dépassé sans résultat'); process.exit(1); }

execSync(`curl -s -o "${sortie}" "${url}"`);
const o = fs.statSync(sortie).size;
// Un fichier trop petit est une page d'erreur, pas une image : ne jamais
// considérer ça comme un succès (piège déjà payé sur les TTS).
if (o < 20000) { console.error(`sortie suspecte (${o} octets) — traité comme un échec`); process.exit(1); }
console.log(`  ${sortie}  ${Math.round(o / 1024)} Ko`);

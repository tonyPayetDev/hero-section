// Sépare voix et instrumental via WaveSpeed.
//
// Le modèle rend DEUX pistes. L'ordre n'est pas garanti et rien dans la réponse
// ne dit laquelle est laquelle : on les télécharge toutes les deux et on les
// départage par la mesure (voir analyser.mjs) plutôt que par leur position.
import { readFileSync, writeFileSync } from 'node:fs';

const URL_AUDIO = process.argv[2];
const OUT = process.argv[3];
const CLE = (readFileSync('/work/.wavespeed.env', 'utf8').match(/[A-Za-z0-9_-]{20,}/) || [])[0];
const ent = { Authorization: `Bearer ${CLE}`, 'Content-Type': 'application/json' };
const dodo = (ms) => new Promise((r) => setTimeout(r, ms));

const r = await (await fetch('https://api.wavespeed.ai/api/v3/wavespeed-ai/audio-vocal-isolator', {
  method: 'POST', headers: ent, body: JSON.stringify({ audio: URL_AUDIO }),
})).json();
if (r.code !== 200) { console.log(`  ⚠️  isolation refusée : ${r.code} ${r.message || ''}`); process.exit(0); }

let sorties = null;
for (let i = 0; i < 60; i++) {
  await dodo(3000);
  const q = await (await fetch(`https://api.wavespeed.ai/api/v3/predictions/${r.data.id}/result`, { headers: ent })).json();
  const d = q.data || {};
  if (d.status === 'completed' && d.outputs?.length) { sorties = d.outputs; break; }
  if (/fail|error/i.test(d.status || '')) { console.log(`  ⚠️  ${d.status} ${d.error || ''}`); process.exit(0); }
}
if (!sorties) { console.log('  ⚠️  toujours rien après 180 s'); process.exit(0); }

const noms = ['piste-a.mp3', 'piste-b.mp3'];
for (let i = 0; i < Math.min(sorties.length, 2); i++) {
  const buf = Buffer.from(await (await fetch(sorties[i])).arrayBuffer());
  writeFileSync(`${OUT}/${noms[i]}`, buf);
  console.log(`  ${noms[i]} · ${(buf.length / 1024).toFixed(0)} ko`);
}
console.log('  → analyser.mjs dira laquelle est l\'instrumental');

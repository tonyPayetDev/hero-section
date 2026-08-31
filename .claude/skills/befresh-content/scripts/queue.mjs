// BeFresh queue helper — read the intake queue, claim a request, close it.
//
// The n8n PUBLIC API is read+insert only on data-table rows (PATCH/DELETE -> 405),
// so status writes go through the "BeFresh — file : statut" webhook (UjXxUajM0MLpg1NB).
//
//   node scripts/queue.mjs list
//   node scripts/queue.mjs next
//   node scripts/queue.mjs statut <request_id> <en_cours|livre|supprimer>
import fs from 'node:fs';

const N8N = 'https://n7n.automatisationboost.com';
const DT = 'jRBrp1yG1IvMF4Pe';
const STATUT_HOOK = `${N8N}/webhook/befresh-file-statut`;

function apiKey() {
  if (process.env.N8N_API_KEY) return process.env.N8N_API_KEY;
  const s = JSON.parse(fs.readFileSync('/work/.claude/settings.json', 'utf8'));
  const k = s?.env?.N8N_API_KEY;
  if (!k) throw new Error('N8N_API_KEY introuvable (env ou /work/.claude/settings.json)');
  return k;
}

async function rows() {
  const r = await fetch(`${N8N}/api/v1/data-tables/${DT}/rows`, {
    headers: { 'X-N8N-API-KEY': apiKey() },
  });
  if (!r.ok) throw new Error(`lecture file HTTP ${r.status}`);
  return (await r.json()).data || [];
}

async function setStatut(requestId, statut) {
  const r = await fetch(STATUT_HOOK, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ request_id: requestId, statut }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || !j.ok) throw new Error(`statut HTTP ${r.status} ${JSON.stringify(j)}`);
  // The webhook reports how many rows it touched. 0 means the id did not match.
  if (j.rows === 0) throw new Error(`aucune ligne pour request_id=${requestId}`);
  return j;
}

const [cmd, a, b] = process.argv.slice(2);

if (cmd === 'list') {
  const all = await rows();
  if (!all.length) { console.log('(file vide)'); process.exit(0); }
  for (const r of all) {
    console.log(`${r.request_id}  [${r.statut}]  ${r.format}  ${r.angle}`
      + `${r.produit ? `  produit=${r.produit}` : ''}${r.lieu ? `  lieu=${r.lieu}` : ''}`);
  }
} else if (cmd === 'next') {
  const todo = (await rows()).filter((r) => r.statut === 'a_faire');
  if (!todo.length) { console.log('(rien a faire)'); process.exit(0); }
  console.log(JSON.stringify(todo[0], null, 2));
} else if (cmd === 'statut') {
  if (!a || !b) { console.error('usage: queue.mjs statut <request_id> <statut>'); process.exit(1); }
  console.log(JSON.stringify(await setStatut(a, b)));
} else {
  console.error('usage: queue.mjs list | next | statut <request_id> <statut>');
  process.exit(1);
}

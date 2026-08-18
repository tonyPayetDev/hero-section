#!/usr/bin/env node
// /etat — collecte l'état réel du business en un digest compact.
// Sources : TASKLOG.md (local), Coolify API, n8n API, /proc (rendus), domaines HTTP, git.
// Tout est best-effort : une source qui tombe n'empêche pas les autres.
// Sortie : texte compact, sections à emoji, prêt à résumer par l'assistant.
import fs from 'fs';
import cp from 'child_process';

const WORK = '/work';
const now = Date.now();
const H = 3600e3;
const out = [];
const say = s => out.push(s);
const fetchT = (url, opts = {}, ms = 9000) =>
  fetch(url, { ...opts, signal: AbortSignal.timeout(ms) }).then(r => r);

// ── 1. Demandes ouvertes (TASKLOG) ─────────────────────────────────────────
function tasklog() {
  say('📋 DEMANDES OUVERTES (TASKLOG)');
  let md;
  try { md = fs.readFileSync(`${WORK}/TASKLOG.md`, 'utf8'); }
  catch { say('   (pas de TASKLOG.md)'); return; }
  const lines = md.split('\n');
  const open = [], done = [];
  let day = '';
  for (const l of lines) {
    const dm = l.match(/^##\s+(\d{4}-\d{2}-\d{2})/);
    if (dm) { day = dm[1]; continue; }
    const m = l.match(/^- \[([ x~!])\]\s+`(\d\d:\d\d)`\s+(.*?)\s*(?:<sub>|$)/);
    if (!m) continue;
    const [, st, time, txt] = m;
    (st === ' ' ? open : done).push({ day, time, txt: txt.slice(0, 80) });
  }
  const today = new Date().toISOString().slice(0, 10);
  const yst = new Date(now - 24 * H).toISOString().slice(0, 10);
  const recent = open.filter(o => o.day === today || o.day === yst);
  say(`   ${open.length} ouvertes au total · ${recent.length} sur 48h · ${done.length} clôturées`);
  recent.slice(0, 8).forEach(o => say(`   ⬜ ${o.day.slice(5)} ${o.time}  ${o.txt}`));
  if (recent.length === 0) say('   ✅ rien d\'ouvert sur les dernières 48h');
}

// ── 2. Rendus / process en cours ────────────────────────────────────────────
function renders() {
  say('\n🎬 RENDUS / PROCESS EN COURS');
  const hits = [];
  let pids = [];
  try { pids = fs.readdirSync('/proc').filter(p => /^\d+$/.test(p)); } catch {}
  for (const pid of pids) {
    if (pid === String(process.pid)) continue;
    let argv = [];
    try { argv = fs.readFileSync(`/proc/${pid}/cmdline`).toString().split('\0').filter(Boolean); } catch { continue; }
    if (!argv.length) continue;
    const exe = (argv[0].split('/').pop() || '').toLowerCase();
    const rest = argv.slice(1).join(' ');
    if (/^(bash|sh|dash|env|which)$/.test(exe)) continue;          // wrappers shell, pas des rendus
    if (/status\.mjs/.test(rest)) continue;                        // /etat lui-même
    let hit = null;
    if (exe.startsWith('ffmpeg')) hit = `ffmpeg ${rest.slice(0, 80)}`;
    else if (/^chrom|^headless/.test(exe) && /--headless|--type=renderer/.test(rest)) hit = 'chrome headless (rendu)';
    else if (exe === 'node' && /hyperframes|render|build\.(c|m)?js|\.mjs$/i.test(rest)) hit = `node ${rest.slice(0, 80)}`;
    else if (/hyperframes/.test(exe)) hit = `hyperframes ${rest.slice(0, 70)}`;
    if (hit) hits.push(hit);
  }
  if (hits.length) hits.slice(0, 6).forEach(h => say(`   ⏳ ${h}`));
  else say('   aucun rendu actif');

  // MP4 récents (< 3h) sous les dossiers vidéo
  const fresh = [];
  const walk = (dir, depth) => {
    if (depth < 0) return;
    let ents = [];
    try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
    for (const e of ents) {
      if (e.name === 'node_modules' || e.name === '.git') continue;
      const p = `${dir}/${e.name}`;
      if (e.isDirectory()) walk(p, depth - 1);
      else if (e.name.endsWith('.mp4')) {
        let st; try { st = fs.statSync(p); } catch { continue; }
        if (now - st.mtimeMs < 3 * H) fresh.push({ p: p.replace(WORK + '/', ''), age: (now - st.mtimeMs) / 60000, mb: st.size / 1048576 });
      }
    }
  };
  for (const d of ['autoboost-neon-videos', 'foodboost-videos']) walk(`${WORK}/${d}`, 3);
  fresh.sort((a, b) => a.age - b.age);
  if (fresh.length) {
    say(`   🆕 MP4 produits (<3h) :`);
    fresh.slice(0, 5).forEach(f => say(`      ${f.age.toFixed(0)}min  ${f.mb.toFixed(1)}Mo  ${f.p}`));
  }
}

// ── 3. Coolify + domaines ───────────────────────────────────────────────────
async function deploys() {
  say('\n🚀 DÉPLOIEMENTS');
  const base = process.env.COOLIFY_BASE_URL, tok = process.env.COOLIFY_ACCESS_TOKEN;
  if (base && tok) {
    try {
      const r = await fetchT(`${base}/api/v1/applications`, { headers: { Authorization: `Bearer ${tok}` } });
      const apps = await r.json();
      const bad = apps.filter(a => !/^running/.test(a.status || ''));
      const run = apps.length - bad.length;
      say(`   Coolify : ${run}/${apps.length} apps running`);
      bad.slice(0, 8).forEach(a => say(`   ⚠️  ${(a.name || a.uuid).slice(0, 44)} => ${a.status}`));
      if (bad.length > 8) say(`   … +${bad.length - 8} autres non-running`);
    } catch (e) { say(`   Coolify : injoignable (${e.name})`); }
  } else say('   Coolify : token absent de l\'env');

  const domains = [
    'https://automatisationboost.com',
    'https://tony.automatisationboost.com',
    'https://previsualisation.automatisationboost.com',
    'https://n7n.automatisationboost.com',
  ];
  const checks = await Promise.all(domains.map(async u => {
    try { const r = await fetchT(u, { method: 'GET' }, 8000); return `${r.status} ${u.replace('https://', '')}`; }
    catch { return `DOWN ${u.replace('https://', '')}`; }
  }));
  say('   Domaines : ' + checks.map(c => (c.startsWith('200') ? '✅' : '❌') + c.split(' ')[1]).join('  '));
}

// ── 4. n8n : santé des workflows ────────────────────────────────────────────
async function n8n() {
  say('\n⚙️  N8N (dernières exécutions)');
  const raw = process.env.N8N_API_URL, key = process.env.N8N_API_KEY;
  if (!raw || !key) { say('   token n8n absent'); return; }
  const base = /\/api\/v1$/.test(raw) ? raw : `${raw}/api/v1`;
  const H2 = { 'X-N8N-API-KEY': key };
  try {
    const r = await fetchT(`${base}/executions?limit=20&includeData=false`, { headers: H2 });
    const j = await r.json();
    const ex = j.data || j;
    let ok = 0, err = 0; const errIds = new Set(); const errList = [];
    for (const e of ex) {
      const status = e.status || (e.finished ? 'success' : 'unknown');
      if (status === 'success') ok++;
      else if (status === 'error' || status === 'crashed') { err++; errIds.add(e.workflowId); errList.push(e); }
    }
    say(`   20 dernières : ${ok} ✅  ${err} ❌`);
    // noms des workflows en erreur
    const names = {};
    await Promise.all([...errIds].slice(0, 6).map(async id => {
      try { const w = await (await fetchT(`${base}/workflows/${id}`, { headers: H2 }, 7000)).json(); names[id] = w.name || id; }
      catch { names[id] = id; }
    }));
    const seen = new Set();
    for (const e of errList) {
      if (seen.has(e.workflowId)) continue; seen.add(e.workflowId);
      say(`   ❌ ${(e.startedAt || '').slice(5, 16)}  ${names[e.workflowId] || e.workflowId}`);
    }
  } catch (e) { say(`   n8n : injoignable (${e.name})`); }
}

// ── 5. Git ──────────────────────────────────────────────────────────────────
function git() {
  say('\n📦 GIT (travail non commité)');
  try {
    const s = cp.execSync('git -C /work status --porcelain 2>/dev/null', { encoding: 'utf8' }).trim();
    const n = s ? s.split('\n').length : 0;
    const subs = cp.execSync('git -C /work submodule status 2>/dev/null | grep -c "^+" || true', { encoding: 'utf8' }).trim();
    say(`   ${n} fichiers modifiés · ${subs} sous-modules en avance`);
  } catch { say('   (git indisponible)'); }
}

// ── run ─────────────────────────────────────────────────────────────────────
tasklog();
renders();
await deploys();
await n8n();
git();
say('\n— fin état —');
console.log(out.join('\n'));

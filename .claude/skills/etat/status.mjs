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
  /* Les engagements en retard passent AVANT tout le reste.
     Règle de Tony, 2026-08-25 : « si le lendemain j'arrive ça doit être fini ».
     Le cas déclencheur : la vidéo Koytcha, demandée le 24/08 à 19h15, toujours
     pas montée le lendemain matin — il a fallu qu'il redemande.
     La liste vient de taches.json, pas de TASKLOG.md : ce dernier compte 1333
     lignes « ouvertes » dont l'immense majorité sont des `ls`. Une alarme
     branchée dessus crierait sans arrêt et serait ignorée en deux jours. */
  try {
    const r = cp.execSync('node /work/previsualisation/taches/retards.mjs 2>/dev/null || true',
      { encoding: 'utf8' }).trim();
    if (r && !/aucun engagement/.test(r)) {
      say('⏰ ENGAGEMENTS EN RETARD');
      r.split('\n').forEach((l) => say('  ' + l.trim()));
      say('');
    }
  } catch { /* best-effort : l'état s'affiche même si le contrôle échoue */ }

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
  /* Déclaré ici, pas dans le try : le balayage des sites clients plus bas en a
     besoin, et une const enfermée dans le bloc lui serait invisible. */
  let apps = null;
  if (base && tok) {
    try {
      const r = await fetchT(`${base}/api/v1/applications`, { headers: { Authorization: `Bearer ${tok}` } });
      apps = await r.json();
      const bad = apps.filter(a => !/^running/.test(a.status || ''));
      const run = apps.length - bad.length;
      say(`   Coolify : ${run}/${apps.length} apps running`);
      bad.slice(0, 8).forEach(a => say(`   ⚠️  ${(a.name || a.uuid).slice(0, 44)} => ${a.status}`));
      if (bad.length > 8) say(`   … +${bad.length - 8} autres non-running`);
    } catch (e) { say(`   Coolify : injoignable (${e.name})`); }
  } else say('   Coolify : token absent de l\'env');

  /* Chaque adresse porte le code qu'on ATTEND d'elle, pas 200 par défaut.
     La racine de previsualisation est protégée par mot de passe depuis le
     25/08 : elle DOIT répondre 401. La traiter comme une panne faisait crier
     le tableau de bord sur un site en parfait état — et, plus grave, un 200
     à cet endroit signifierait que le mot de passe est tombé. On veut le
     savoir dans les deux sens. */
  const domains = [
    { u: 'https://automatisationboost.com', attendu: 200, nom: 'automatisationboost.com' },
    { u: 'https://tony.automatisationboost.com', attendu: 200, nom: 'tony.automatisationboost' },
    { u: 'https://previsualisation.automatisationboost.com/', attendu: 401, nom: 'previsu(verrou)' },
    { u: 'https://previsualisation.automatisationboost.com/client-lunisson-scroll/', attendu: 200, nom: 'previsu(demos)' },
    { u: 'https://n7n.automatisationboost.com', attendu: 200, nom: 'n7n' },
    /* Sites clients relevés en 503 le 25/08 : ils tournent (leur adresse
       sslip.io rend 200) mais leur domaine n'est pas mappé dans Coolify.
       Tant que ce n'est pas corrigé, on veut les voir à chaque ronde. */
    { u: 'https://la-kaz-de-ben.automatisationboost.com', attendu: 200, nom: 'la-kaz-de-ben' },
    { u: 'https://ticoeur-store-v2.automatisationboost.com', attendu: 200, nom: 'ticoeur-store-v2' },
  ];
  const checks = await Promise.all(domains.map(async d => {
    try {
      const r = await fetchT(d.u + (d.u.includes('?') ? '&' : '?') + 'cb=' + Math.random(), { method: 'GET' }, 9000);
      return { nom: d.nom, code: r.status, ok: r.status === d.attendu, attendu: d.attendu };
    } catch { return { nom: d.nom, code: 'DOWN', ok: false, attendu: d.attendu }; }
  }));
  say('   Domaines : ' + checks.map(c => (c.ok ? '✅' : '❌') + c.nom).join('  '));
  const faux = checks.filter(c => !c.ok);
  faux.forEach(c => say(`   ⚠️  ${c.nom} rend ${c.code}, attendu ${c.attendu}`));

  /* ── TOUS les sites clients, pas une liste écrite à la main ─────────────
   *
   * La liste ci-dessus est tenue au doigt mouillé : on y ajoute un domaine le
   * jour où on le voit tomber. Conséquence mesurée le 25/08 :
   * `bloom.automatisationboost.com` rendait 503 depuis un moment sans que rien
   * ne le signale — son conteneur tournait, Coolify affichait « running », et
   * le tableau de bord ne testait tout simplement pas ce domaine.
   *
   * On balaie donc la liste RÉELLE des applications Coolify. Une seule requête
   * par site, en parallèle, sur la page d'accueil. */
  if (apps && apps.length) {
    const INTERNES = /^previsualisation\.|^tony\.|^videoboost\.|^facepuppet\.|^omniroute\.|^resto\./i;
    const dejaVus = new Set(domains.map(d => d.u.replace(/^https?:\/\//, '').replace(/\/.*$/, '')));
    const clients = [];
    for (const a of apps) {
      const f = String(a.fqdn || '').split(',')[0].trim();
      if (!f || !/automatisationboost\.com/i.test(f)) continue;
      const hote = f.replace(/^https?:\/\//, '').replace(/\/.*$/, '');
      if (hote === 'automatisationboost.com' || hote === 'www.automatisationboost.com') continue;
      if (INTERNES.test(hote) || dejaVus.has(hote)) continue;
      clients.push({ nom: a.name, hote });
    }
    const res = await Promise.all(clients.map(async c => {
      try {
        const r = await fetchT(`https://${c.hote}/?cb=` + Math.random(), { method: 'GET' }, 12000);
        return { ...c, code: r.status, ok: r.status >= 200 && r.status < 400 };
      } catch { return { ...c, code: 'DOWN', ok: false }; }
    }));
    const ko = res.filter(r => !r.ok);
    say(`   Sites clients : ${res.length - ko.length}/${res.length} répondent`);
    ko.forEach(r => say(`   ⚠️  ${r.nom} (${r.hote}) rend ${r.code}`));
  }
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
    // Une panne CHRONIQUE ne doit pas se lire comme un incident isolé.
    // Cas payé le 25/08 : « C31 | Vendre services restaurants » échouait tous
    // les soirs depuis le 11/08 — quota Apify épuisé, prospection restaurant à
    // zéro pendant 14 jours. La ligne affichée ne montrait que la dernière
    // erreur, donc elle se lisait comme un raté sans importance.
    const seen = new Set();
    for (const e of errList) {
      if (seen.has(e.workflowId)) continue; seen.add(e.workflowId);
      const nom = names[e.workflowId] || e.workflowId;
      let anciennete = '';
      try {
        const h = await (await fetchT(
          `${base}/executions?workflowId=${e.workflowId}&status=error&limit=60`,
          { headers: H2 }, 9000)).json();
        const jours = [...new Set((h.data || []).map(x => (x.startedAt || '').slice(0, 10)))]
          .filter(Boolean).sort();
        if (jours.length > 1) {
          anciennete = `  ⚠️  ${jours.length} jours d'échec, depuis le ${jours[0].slice(5)}`;
        }
      } catch { /* best-effort : l'ancienneté est un bonus, pas un bloquant */ }
      say(`   ❌ ${(e.startedAt || '').slice(5, 16)}  ${nom}${anciennete}`);
    }

    /* ── Ce que la fenêtre des 20 dernières NE PEUT PAS voir ────────────────
     *
     * Cas payé le 25/08 : « restaurant v5 demo + essai » (la publication
     * automatique FoodBoost) échouait à CHAQUE exécution depuis le 17/08 —
     * sept fois d'affilée, ChatGPT_0 en 429 « no credits remaining ». Et le
     * tableau de bord affichait « 20 dernières : 20 ✅ 0 ❌ ».
     *
     * Ce n'était pas un bug de lecture : l'Auto-DM tourne toutes les 10
     * minutes, soit 144 exécutions par jour. Un workflow programmé tous les
     * deux jours ne peut structurellement pas entrer dans les 20 dernières.
     * Plus un workflow est lent, plus il est invisible — exactement l'inverse
     * de ce qu'on veut.
     *
     * On pose donc l'autre question : non pas « une des 20 dernières a-t-elle
     * échoué » mais « qu'est-ce qui est EN PANNE maintenant ». On part des
     * erreurs elles-mêmes, puis on vérifie pour chacune que la dernière
     * exécution du workflow est bien encore un échec — sinon c'est réglé. */
    const enPanne = [];
    try {
      const he = await (await fetchT(`${base}/executions?status=error&limit=100&includeData=false`,
        { headers: H2 }, 15000)).json();
      const parWf = new Map();
      for (const e of (he.data || [])) {
        if (!parWf.has(e.workflowId)) parWf.set(e.workflowId, []);
        parWf.get(e.workflowId).push(e);
      }
      for (const [wid, errs] of [...parWf].slice(0, 25)) {
        try {
          const d = await (await fetchT(`${base}/executions?workflowId=${wid}&limit=1&includeData=false`,
            { headers: H2 }, 9000)).json();
          const derniere = (d.data || [])[0];
          if (!derniere || derniere.status === 'success') continue;   // rétabli depuis
          const w = names[wid] ? { name: names[wid] } : await (await fetchT(
            `${base}/workflows/${wid}`, { headers: H2 }, 9000)).json();
          if (w.active === false) continue;                            // désactivé, pas une panne
          const jours = [...new Set(errs.map((x) => (x.startedAt || '').slice(0, 10)))].filter(Boolean).sort();
          enPanne.push({ nom: w.name || wid, n: errs.length, depuis: jours[0], quand: (derniere.startedAt || '').slice(5, 16) });
        } catch { /* best-effort */ }
      }
    } catch { /* best-effort */ }

    if (enPanne.length) {
      say(`\n   🔴 EN PANNE MAINTENANT — dernière exécution en échec : ${enPanne.length}`);
      for (const p of enPanne.sort((a, b) => b.n - a.n)) {
        say(`   ❌ ${p.nom.slice(0, 46).padEnd(48)} ${String(p.n).padStart(2)} échecs`
          + (p.depuis ? ` depuis le ${p.depuis.slice(5)}` : '') + ` · dernier ${p.quand}`);
      }
      say(`   → un workflow lent (programmé aux heures/jours) n'entre jamais dans les 20 dernières :`);
      say(`     c'est cette ligne-ci qui le voit, pas celle du dessus.`);
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
/* Les mines : actif + déclenchable de l'extérieur + credential morte.
   Cette classe de panne n'apparaît dans AUCUNE alerte d'échec, puisque ces
   workflows n'ont jamais échoué — ils n'ont jamais été appelés. Découvert
   le 25/08 : 15 workflows concernés, dont 8 invisibles. */
say('\n💣 MINES (actifs + credential morte)');
try {
  const r = cp.execSync('node /work/.claude/skills/etat/mines.mjs 2>/dev/null || true',
    { encoding: 'utf8', timeout: 90000 });
  if (r.trim()) say(r.replace(/\n$/, ''));
} catch (e) { say('   (contrôle des mines interrompu)'); }

say('\n— fin état —');
console.log(out.join('\n'));

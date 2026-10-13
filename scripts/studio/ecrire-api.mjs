#!/usr/bin/env node
/* ecrire-api.mjs <skill> <dir> <modele> <b64 {sujet,consignes}>
   Writes <dir>/video.json by calling ONE model through OpenRouter's chat API (no agent, no tool use:
   the free agentic OpenCode runs never managed to write the file). The prompt carries the skill's
   SKILL.md, one validated example and the live CTA keywords; the validator's errors are fed back
   for up to 2 repair rounds. Progress goes to <dir>/.ecrire.json, read by etat-ecrire. */
import fs from 'node:fs';
import { execFileSync, spawn } from 'node:child_process';
const [, , SKILL, DIR, MODELE, B64] = process.argv;
const A = JSON.parse(Buffer.from(B64 || '', 'base64').toString() || '{}');
const ETAT = `${DIR}/.ecrire.json`, VJ = `${DIR}/video.json`;
const t0 = Date.now();
const ecrireEtat = (o) => fs.writeFileSync(ETAT, JSON.stringify({ skill: SKILL, modele: MODELE, debut: new Date(t0).toISOString(), ...o }));
const EXEMPLES = {
  'boost-niveau': '/work/autoboost-neon-videos/boost-niveau-01-quatre-heures/video.json',
  'split-preuve': '/work/autoboost-neon-videos/split-preuve/21-quatre-regles-boucle/video.json',
};
try {
  if (!EXEMPLES[SKILL]) throw new Error(`skill non pris en charge pour l'écriture : ${SKILL} (le Journal IA s'écrit tout seul chaque matin)`);
  ecrireEtat({ etat: 'en_cours', etape: 'préparation' });
  const skillMd = fs.readFileSync(`/work/.claude/skills/${SKILL}/SKILL.md`, 'utf8');
  const exemple = fs.readFileSync(EXEMPLES[SKILL], 'utf8');
  let mots = '';
  try {
    const csv = execFileSync('curl', ['-sL', '--max-time', '20', 'https://docs.google.com/spreadsheets/d/10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags/export?format=csv&gid=1778849664'], { encoding: 'utf8' });
    mots = [...new Set(csv.split('\n').slice(1).map((l) => l.split(',')[0].trim()).filter((m) => /^[A-ZÀ-Ü0-9]{2,20}$/.test(m)))].join(', ');
  } catch {}
  const KEY = fs.readFileSync(`${process.env.HOME}/.config/autoboost/openrouter.key`, 'utf8').trim();
  const systeme = `Tu écris le fichier video.json du skill « ${SKILL} » de Tony PAYET (AutomatisationBoost, La Réunion).
Réponds UNIQUEMENT par un objet JSON valide, sans texte autour, sans balises de code.
Respecte EXACTEMENT le schéma et les règles de la documentation du skill ci-dessous, et imite la forme de l'exemple validé.
Règles de Tony : français de tous les jours compris à la première écoute ; pas de jargon ; jamais « La Réunion » comme repère horaire ;
uniquement des chiffres mesurés et sourcés (sinon pas de chiffre) ; durée totale ≥ 30 s : le texte parlé (tous les textes dits par la voix, mis bout à bout) doit faire environ 110 à 140 mots au total, jamais moins de 110 ; ouverture « c'est Tony » si l'avatar se présente.
Mot-clé CTA : UN seul mot pris dans cette liste (onglet « Ressources CTA ») : ${mots || '(liste indisponible — choisis un mot du SKILL.md)'}.

=== DOCUMENTATION DU SKILL ===
${skillMd}

=== EXEMPLE VALIDÉ (forme à imiter, contenu à NE PAS recopier) ===
${exemple}`;
  const demande = `Sujet : ${A.sujet || '(aucun)'}\nConsignes : ${A.consignes || 'aucune'}\nÉcris le video.json complet.`;
  const messages = [{ role: 'system', content: systeme }, { role: 'user', content: demande }];
  let dernier = null, essais = 0;
  // 1) Free OpenCode models, in order: each gets 5 min, then the next one. Only a video.json the
  // skill's validator accepts counts. 2) If none does, the paid OpenRouter loop below.
  const valide = () => {
    try {
      const sortie = execFileSync('/work/scripts/studio/valider.sh', [SKILL, DIR.split('/').pop()], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
      return JSON.parse(sortie.trim().split('\n').pop());
    } catch (e) {
      try { return JSON.parse(String(e.stdout || '').trim().split('\n').pop()); } catch { return { ok: false, erreurs: [String(e.message).slice(0, 300)] }; }
    }
  };
  const essaiGratuit = (modele) => new Promise((resolve) => {
    fs.rmSync(VJ, { force: true });
    fs.writeFileSync(`${DIR}/.prompt.md`, `${systeme}\n\n${demande}`);
    ecrireEtat({ etat: 'en_cours', etape: `modèle gratuit ${modele.replace('-free', '')}`, modele });
    const p = spawn('/home/claude/.opencode/bin/opencode', ['run', '-m', `opencode/${modele}`, '--dir', '/work',
      `Lis ${DIR}/.prompt.md et écris le fichier ${VJ} : un seul objet JSON valide, rien d'autre.`], { stdio: ['ignore', 'ignore', 'ignore'] });
    const coupe = setTimeout(() => p.kill('SIGKILL'), 300000);
    // The model often writes a valid file and then keeps the process open: stop it as soon as the file validates.
    const surveille = setInterval(() => { if (fs.existsSync(VJ) && valide().ok) p.kill('SIGKILL'); }, 15000);
    p.on('exit', () => {
      clearTimeout(coupe);
      clearInterval(surveille);
      if (!fs.existsSync(VJ)) return resolve(null);
      const v = valide();
      resolve(v.ok ? { ...v, modele } : null);
    });
  });
  const GRATUITS = ['nemotron-3-ultra-free', 'mimo-v2.6-flash-free', 'nemotron-3.5-lightning-free', 'ling-3.1-flash-free', 'step-5-preview-free'];
  let gratuit = null;
  for (const modele of GRATUITS) {
    gratuit = await essaiGratuit(modele);
    if (gratuit) break;
  }
  if (gratuit) dernier = gratuit;
  for (essais = 1; !gratuit && essais <= 3; essais++) {
    ecrireEtat({ etat: 'en_cours', etape: `écriture (essai ${essais}/3)` });
    const r = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST', signal: AbortSignal.timeout(240000),
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json', 'X-Title': 'AutomatisationBoost studio-video' },
      body: JSON.stringify({ model: MODELE, messages, temperature: 0.4, max_tokens: 8000, response_format: { type: 'json_object' } }),
    });
    const j = await r.json();
    if (!r.ok || !j.choices) throw new Error(`OpenRouter ${r.status} : ${JSON.stringify(j).slice(0, 300)}`);
    let txt = j.choices[0].message.content || '';
    txt = txt.replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/, '').trim();
    const a = txt.indexOf('{'), b = txt.lastIndexOf('}');
    let obj;
    try { obj = JSON.parse(txt.slice(a, b + 1)); } catch (e) {
      messages.push({ role: 'assistant', content: txt.slice(0, 4000) }, { role: 'user', content: `Ce n'est pas du JSON valide (${e.message}). Renvoie l'objet JSON complet, rien d'autre.` });
      continue;
    }
    fs.mkdirSync(DIR, { recursive: true });
    fs.writeFileSync(VJ, JSON.stringify(obj, null, 2));
    ecrireEtat({ etat: 'en_cours', etape: `validation (essai ${essais}/3)` });
    let v;
    try {
      const sortie = execFileSync('/work/scripts/studio/valider.sh', [SKILL, DIR.split('/').pop()], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
      v = JSON.parse(sortie.trim().split('\n').pop());
    } catch (e) {
      const out = String(e.stdout || '').trim().split('\n').pop();
      try { v = JSON.parse(out); } catch { v = { ok: false, erreurs: [String(e.message).slice(0, 300)] }; }
    }
    dernier = v;
    if (v.ok) break;
    messages.push({ role: 'assistant', content: JSON.stringify(obj) },
      { role: 'user', content: `Le validateur refuse ce video.json :\n- ${(v.erreurs || []).join('\n- ')}\nCorrige ces points et renvoie le JSON complet.` });
  }
  const contenu = fs.existsSync(VJ) ? fs.readFileSync(VJ, 'utf8') : '';
  ecrireEtat({ etat: dernier && dernier.ok ? 'ok' : 'echec', fin: new Date().toISOString(), duree_s: Math.round((Date.now() - t0) / 1000),
    essais: Math.min(essais, 3), validation: dernier, contenu, erreur: dernier && dernier.ok ? null : 'le validateur refuse encore le video.json après 3 essais — corrige-le à la main dans la page' });
} catch (e) {
  ecrireEtat({ etat: 'echec', fin: new Date().toISOString(), duree_s: Math.round((Date.now() - t0) / 1000), erreur: String(e.message).slice(0, 500) });
}

// Rule engine (no LLM): transcript -> scenes, each with a template, its words, a headline,
// a highlight, optional data (numbers, steps, tools, list items, contrast) and a sticker.
import { sentences } from "./voice.mjs";

const STOP = new Set(("a à ai au aux avec c ça ce ces cet cette ci comme d dans de des du elle elles en est et être eu "
  + "fait faire il ils j je l la le les leur lui m ma mais me mes moi mon n ne ni nos notre nous on ou où par pas peu "
  + "plus pour qu que quel quelle qui s sa sans se ses si son sont sur t ta te tes toi ton tu un une vos votre vous y "
  + "c'est j'ai qu'il qu'on d'un d'une l'on n'est s'il là alors donc voilà bah euh hein bon ben aussi encore très tout "
  + "tous toute toutes juste vraiment même ici chaque certaines certains certain quoi dedans parce pourrait peut vient veux voir comment exactement après avant faut va vais être avoir").split(" "));
export const TOOLS = {
  n8n: "n8n", claude: "Claude", chatgpt: "ChatGPT", gpt: "GPT", openai: "OpenAI", gmail: "Gmail", notion: "Notion", slack: "Slack",
  make: "Make", zapier: "Zapier", sheets: "Sheets", excel: "Excel", hubspot: "HubSpot", whatsapp: "WhatsApp", instagram: "Instagram",
  tiktok: "TikTok", youtube: "YouTube", linkedin: "LinkedIn", canva: "Canva", capcut: "CapCut", hyperframes: "HyperFrames",
  airtable: "Airtable", stripe: "Stripe", shopify: "Shopify", calendly: "Calendly", telegram: "Telegram", gemini: "Gemini",
  cursor: "Cursor", wordpress: "WordPress", google: "Google", crm: "CRM", email: "Email", formulaire: "Formulaire", ia: "IA",
};
const NUMW = { un: 1, deux: 2, trois: 3, quatre: 4, cinq: 5, six: 6, sept: 7, huit: 8, neuf: 9, dix: 10, onze: 11, douze: 12,
  quinze: 15, vingt: 20, trente: 30, quarante: 40, cinquante: 50, soixante: 60, cent: 100, mille: 1000 };
const UNITS = /^(%|€|euros?|\$|dollars?|h|heures?|min|minutes?|secondes?|s|jours?|semaines?|mois|ans?|fois|clients?|vidéos?|leads?|abonnés?|vues|k)$/i;
const ORD = /^(d'abord|premièrement|premier|première|ensuite|puis|deuxièmement|deuxième|troisièmement|troisième|enfin|finalement|étape)$/i;
const STICKERS = [
  [/lent|perd|perte|galère|bloqu|problème|erreur|cher|trop|jamais/i, ["TROP", "LENT", "red", "clock"]],
  [/simple|facile|rapide|vite|minute/i, ["PLUS", "SIMPLE", "gold", "bolt"]],
  [/temps|heure|gagn/i, ["GAIN", "TEMPS", "violet", "clock"]],
  [/système|machine|automatis|workflow|process/i, ["BON", "SYSTÈME", "gold", "checkc"]],
  [/plus|monte|croiss|double|x\d|résultat|client/i, ["ÇA", "MONTE", "gold", "trend"]],
  [/idée|créa|cerveau|penser/i, ["DÉJÀ", "MIEUX", "violet", "bulb"]],
];

const clean = (w) => w.replace(/[.,!?;:…«»"()]/g, "").trim();
const norm = (w) => clean(w).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
const isStop = (w) => STOP.has(clean(w).toLowerCase()) || clean(w).length < 2;
const toolOf = (w) => TOOLS[norm(w)] || null;
function numOf(w) {
  const c = clean(w).toLowerCase();
  if (/^\d+([.,]\d+)?k?$/.test(c)) return c;
  if (NUMW[c] && c !== "un") return String(NUMW[c]);
  return null;
}
function score(w) {
  if (isStop(w)) return 0;
  const c = clean(w);
  return c.length + (toolOf(w) ? 6 : 0) + (numOf(w) ? 6 : 0) + (/^[A-ZÉ]{2,}/.test(c) ? 4 : 0);
}

/** best window of <= maxN words, and its strongest word */
export function headline(words, maxN = 4) {
  let best = [0, 1], bs = -1;
  for (let i = 0; i < words.length; i++) {
    for (let n = 1; n <= maxN && i + n <= words.length; n++) {
      const win = words.slice(i, i + n);
      if (isStop(win[0].w) && n > 1) continue;
      if (win.slice(0, -1).some((w) => /[,;:]$/.test(w.w))) continue;          // never across a clause
      // French puts the news at the end of the clause: later words weigh a little more
      const s = win.reduce((a, w, k) => a + score(w.w) * (1 + 0.5 * (i + k) / words.length), 0) - (n > 2 ? 1 : 0);
      if (s > bs) { bs = s; best = [i, n]; }
    }
  }
  let [i, n] = best;
  // let the window start on a natural word (extend left by one stop word: « une machine », « le script »)
  if (i > 0 && isStop(words[i - 1].w) && n < maxN) { i -= 1; n += 1; }
  const win = words.slice(i, i + n);
  const hi = win.reduce((b, w, k) => (score(w.w) > score(win[b].w) ? k : b), 0);
  return { words: win, hi, from: i };
}

/** an enumeration: 3+ comma-separated chunks of <= 5 words */
function listLike(text) {
  const items = text.split(",").map((x) => x.trim()).filter(Boolean);
  return items.length >= 3 && items.filter((x) => x.split(/\s+/).length <= 5).length >= items.length - 1;
}

function stickerFor(text, prev) {
  for (const [re, st] of STICKERS) if (re.test(text) && st[1] !== prev) return st;
  return null;
}

/**
 * words on the final timeline -> scenes
 * opts: { cta: keyword override, pace: target seconds per screen (from competitor), total }
 */
export function plan(words, { cta = "", pace = 3.6, total } = {}) {
  let sents = sentences(words);
  // pacing: merge very short sentences into the next, split long ones at the comma nearest the middle
  const merged = [];
  for (const s of sents) {
    const prev = merged[merged.length - 1];
    if (prev && prev[prev.length - 1].e - prev[0].s < 1.1 && !/\?$/.test(prev[prev.length - 1].w)) prev.push(...s); else merged.push([...s]);
  }
  sents = [];
  for (const s of merged) {
    const d = s[s.length - 1].e - s[0].s;
    if (d > pace * 2.1 && s.length > 6 && !listLike(s.map((w) => w.w).join(" "))) {
      const mid = s[0].s + d / 2;
      let k = s.findIndex((w, i) => i > 1 && i < s.length - 2 && /,$/.test(w.w) && w.e >= mid - d * 0.25);
      if (k < 0) k = s.findIndex((w) => w.e >= mid);
      sents.push(s.slice(0, k + 1), s.slice(k + 1));
    } else sents.push(s);
  }
  const scenes = [];
  let prevSticker = null, stepN = 0;
  sents.forEach((s, idx) => {
    const text = s.map((w) => w.w).join(" ");
    const sc = { start: s[0].s, end: s[s.length - 1].e, words: s, text, data: {} };
    const ctaM = text.match(/(?:^|[\s«"“])(commente|écris|ecris|tape|envoie[- ]moi|réponds)\s+[«"“]?\s*([A-Za-zÀ-ÿ0-9]+)/i);
    const tools = [...new Set(s.map((w) => toolOf(w.w)).filter(Boolean))];
    const nums = s.map((w, i) => ({ v: numOf(w.w), i })).filter((x) => x.v);
    const ord = s.findIndex((w) => ORD.test(clean(w.w)));
    const items = text.split(",").map((x) => x.trim()).filter(Boolean);
    if (ctaM || (cta && idx === sents.length - 1)) {
      sc.type = "cta";
      sc.data.keyword = (cta || ctaM[2]).toUpperCase();
      const kw = s.find((w) => norm(w.w) === norm(sc.data.keyword));
      sc.data.at = kw ? kw.s : sc.start + 0.3;
    } else if (ord >= 0 && ord < 3) {
      sc.type = "steps"; sc.data.n = ++stepN;
    } else if (tools.length >= 2) {
      sc.type = "tools"; sc.data.tools = tools.slice(0, 4).map((t) => ({ name: t, at: s.find((w) => toolOf(w.w) === t).s }));
    } else if (nums.length) {
      const n = nums[0];
      const unit = s[n.i + 1] && UNITS.test(clean(s[n.i + 1].w)) ? clean(s[n.i + 1].w) : "";
      sc.type = "stat"; sc.data = { value: n.v, unit, at: s[n.i].s, label: headline(s.filter((_, i) => i !== n.i && i !== n.i + 1), 4).words };
    } else if (listLike(text)) {
      sc.type = "list";
      let cursor = 0;
      sc.data.items = items.slice(0, 6).map((it) => {
        const n = it.split(/\s+/).length;
        const w0 = s[Math.min(cursor, s.length - 1)];
        cursor += n;
        return { label: clean(it), at: w0.s };
      });
    } else if (/\bau lieu de?\b|\bplutôt que\b|\bpas\b.*\bmais\b|\bavant\b.*\bmaintenant\b|\bsinon\b/i.test(text)) {
      sc.type = "contrast";
      const cut = s.findIndex((w, i) => i > 0 && /^(mais|maintenant|tu|alors)$/i.test(clean(w.w)) && i > s.length * 0.3);
      const k = cut > 0 ? cut : Math.floor(s.length / 2);
      sc.data = { left: headline(s.slice(0, k), 3).words, right: headline(s.slice(k), 3).words, at: s[k].s };
    } else if (/\?$/.test(text)) {
      sc.type = "question";
    } else {
      sc.type = "headline";
    }
    if (!sc.data.label) sc.head = headline(s, sc.type === "question" ? 5 : 4);
    if (idx === 0 && sc.type !== "cta") sc.hook = true;
    const st = idx === 0 ? ["ÇA", "PART", "gold", "bolt"] : sc.type === "cta" ? null : stickerFor(text, prevSticker);
    if (st && (idx === 0 || idx % 2 === 1 || st[2] === "red")) { sc.sticker = { a: st[0], b: st[1], v: st[2], ico: st[3], at: s[Math.min(1, s.length - 1)].s }; prevSticker = st[1]; }
    scenes.push(sc);
  });
  // scene windows: from the first word to the next scene's first word
  scenes.forEach((sc, i) => {
    sc.a = i === 0 ? 0 : Math.max(0, sc.start - 0.15);
    sc.b = i + 1 < scenes.length ? Math.max(0, scenes[i + 1].start - 0.15) : total;
  });
  const lvl = scenes.filter((s) => !s.hook && s.type !== "cta");
  lvl.forEach((s, k) => { s.level = k === lvl.length - 1 && lvl.length > 2 ? "MAX" : String(Math.min(k + 1, 5)); });
  return scenes;
}

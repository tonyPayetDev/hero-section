#!/usr/bin/env node
/**
 * parse_edition.mjs <edition.md> <out.json>
 *
 * Deterministic parser: journal-ia/<DATE>.md  ->  edition.json
 * No LLM, no network. Pure text transform.
 *
 * Expected markdown shape (written by the nightly cloud routine):
 *   # Journal IA — lundi 17 août 2026
 *   ## 🎙️ Script voix off ...
 *     **Journal IA, lundi 17 août. C'est parti.**
 *     **Un — Titre.** corps... *C'est indéniable. Irréfutable. Indiscutable.*
 *     ...
 *     **Voilà ton actu IA. Tu veux la veille chaque matin ? Commente VEILLE, ...**
 *   ## 📌 Brèves ...
 *     1. **Source — Titre.** corps...
 *   ## 📣 CTA
 *     - **Commente VEILLE** ...
 */
import fs from 'node:fs';

const [, , SRC, OUT] = process.argv;
if (!SRC) { console.error('usage: parse_edition.mjs <edition.md> [out.json]'); process.exit(2); }
const md = fs.readFileSync(SRC, 'utf8');

/* ------------------------------------------------------------------ utils */
const NUM_WORDS = ['Un', 'Deux', 'Trois', 'Quatre', 'Cinq', 'Six'];
const MONTHS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
  'août', 'septembre', 'octobre', 'novembre', 'décembre'];

const stripMd = (s) => s
  .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')   // links
  .replace(/\*\*/g, '').replace(/\*/g, '')
  .replace(/`/g, '')
  .replace(/\s+/g, ' ').trim();

function section(title) {
  const re = new RegExp('^##[^\\n]*' + title + '[^\\n]*$', 'mi');
  const m = md.match(re);
  if (!m) return '';
  const start = m.index + m[0].length;
  const rest = md.slice(start);
  const end = rest.search(/^##\s/m);
  return (end === -1 ? rest : rest.slice(0, end)).replace(/^\s*-{3,}\s*$/gm, '').trim();
}

const paras = (txt) => txt.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);

/* Protect "3.6" / "v1.1" / "S-1" style decimals from the sentence splitter. */
const DOT = '';
const protect = (s) => s.replace(/(\d)\.(\d)/g, `$1${DOT}$2`);
const unprotect = (s) => s.split(DOT).join('.');

/** Split into sentences, then (if still too long) into clauses. */
function clauses(raw) {
  const text = protect(raw);
  const sents = text.match(/[^.!?…]+[.!?…]+|\S[^.!?…]*$/g) || [text];
  const out = [];
  for (const s of sents) {
    const t = s.trim();
    if (t.length <= 90) { out.push(t); continue; }
    // split on strong clause boundaries, keeping the separator with the left part
    const parts = t.split(/(?<=[,;:—–…])\s+/);
    let buf = '';
    for (const p of parts) {
      if ((buf + ' ' + p).trim().length > 90 && buf) { out.push(buf.trim()); buf = p; }
      else buf = (buf + ' ' + p).trim();
    }
    if (buf) out.push(buf.trim());
  }
  return out;
}

/** Keep whole clauses up to `budget` chars, then close the sentence cleanly. */
function condense(text, budget) {
  const cs = clauses(text);
  let acc = '';
  let i = 0;
  for (; i < cs.length; i++) {
    const next = acc ? acc + ' ' + cs[i] : cs[i];
    if (next.length > budget && acc) break;
    acc = next;
    if (acc.length >= budget) { i++; break; }
  }
  // A clause that overflows would leave a stub: borrow words from it word by word.
  if (acc && i < cs.length && acc.length < budget * 0.72) {
    for (const w of cs[i].split(/\s+/)) {
      if ((acc + ' ' + w).length > budget) break;
      acc += ' ' + w;
    }
  }
  if (!acc) acc = cs[0] || text;
  acc = unprotect(acc).replace(/[\s,;:—–…]+$/, '');
  // never end on a dangling function word ("... et 559 millions de")
  const DANGLING = /\s+(de|du|des|d'|et|ou|à|au|aux|le|la|les|un|une|en|qui|que|pour|sur|avec|dans|par|il|elle|se|sa|son|ses|leur|plus|vient|est)$/i;
  while (DANGLING.test(acc)) acc = acc.replace(DANGLING, '');
  acc = acc.replace(/[\s,;:—–…]+$/, '');
  if (!/[.!?]$/.test(acc)) acc += '.';
  return acc;
}

const cap1 = (s) => s.replace(/^([a-zà-ÿ])/, (c) => c.toUpperCase());

/* --------------------------------------------------- TTS text normalizer */
const ACRONYM_KEEP = new Set(['ET', 'OU', 'EN', 'LE', 'LA', 'DE', 'DU', 'UN']);
function ttsText(s) {
  let t = ' ' + stripMd(s) + ' ';
  t = t.replace(/[«»"“”]/g, '');
  t = t.replace(/\s*[—–]\s*/g, ', ');
  t = t.replace(/\((.*?)\)/g, ', $1,');
  // units
  t = t.replace(/(\d)\s*%/g, '$1 pour cent');
  t = t.replace(/\bMd\$/g, ' milliards de dollars');
  t = t.replace(/\bM\$/g, ' millions de dollars');
  t = t.replace(/(\d)\s*\$/g, '$1 dollars');
  t = t.replace(/\bMd\b/g, 'milliards');
  // version numbers: 3.7 -> 3 point 7 ; 5,6 stays (French decimal reads fine)
  t = t.replace(/(\d)\.(\d)/g, '$1 point $2');
  // acronyms -> spaced letters (GPT -> G P T), but keep IA as I.A.
  t = t.replace(/\bIA\b/g, 'I.A.');
  t = t.replace(/\b([A-Z]{2,5})\b/g, (m0, w) => (ACRONYM_KEEP.has(w) ? w : w.split('').join(' ')));
  t = t.replace(/\s*,\s*,/g, ',').replace(/\s+([,.])/g, '$1');
  t = t.replace(/\.\.+/g, '.').replace(/\s*([?!;:])/g, ' $1');
  return t.replace(/\s+/g, ' ').trim();
}

/* ------------------------------------------------------------ 1. header */
const h1 = (md.match(/^#\s+(.+)$/m) || [, ''])[1];
const dm = h1.match(/(\d{1,2})\s+([a-zéûôA-Z]+)\s+(\d{4})/);
const dow = (h1.match(/—\s*([a-zéû]+)\s+\d/i) || [, ''])[1] || '';
let day = dm ? +dm[1] : 1;
let monthName = dm ? dm[2].toLowerCase() : 'janvier';
let year = dm ? +dm[3] : 2026;
const monthIdx = Math.max(0, MONTHS.indexOf(monthName));
const iso = `${year}-${String(monthIdx + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
const dowShort = dow ? dow.slice(0, 3).replace(/^./, (c) => c.toUpperCase()) + '.' : '';
const dateLabel = `${dowShort} ${day} ${monthName} ${year}`.trim();
const dateShort = `${String(day).padStart(2, '0')}.${String(monthIdx + 1).padStart(2, '0')}`;
const dateSpoken = `${dow} ${day} ${monthName}`.trim();

/* ------------------------------------------------------- 2. brèves cards */
const brevesRaw = section('Brèves');
const cards = [];
for (const line of brevesRaw.split(/\n/)) {
  const m = line.match(/^\s*(\d+)\.\s+\*\*(.+?)\s*[—–-]\s*(.+?)\.?\*\*\s*(.*)$/);
  if (!m) continue;
  cards.push({ n: +m[1], source: stripMd(m[2]), title: stripMd(m[3]), body: stripMd(m[4]) });
}

/** Hard facts (number + unit) usable as a neon chip. Dates are never chips. */
const DATE_RE = /\d{1,2}\s*(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)/i;
const CHIP_PATTERNS = [
  // ranges: "49,0 → 65,3 %"  /  "1538 → 1588"
  /\d[\d.,\s]*\s*(?:→|->|à)\s*\d[\d.,\s]*\s*(?:%|\$|Md\$?|M\$?)?/g,
  // number + explicit unit
  /\d[\d.,   ]*(?:%|\$|€|Md\$|M\$|\bMd\b|\bmilliards?\b(?:\s+de\s+\w+)?|\bmillions?\b(?:\s+de\s+\w+)?|\btokens?\b|\bparamètres?\b|\bElo\b|\bemplois\b)/g,
  // multipliers / factors : "×14", "divisé par deux", "2 400 Md"
  /(?:×|x)\s?\d+[\d.,]*/g,
  // product/version tokens : "Gemini 3.7", "GPT-5.6", "V4 Pro", "S-1"
  /\b[A-Z][A-Za-z]{1,14}[- ]?\d+(?:[.,]\d+)?(?:\s?(?:Pro|Max|Flash|Ultra|Mini))?\b/g,
];
const STOPCAP = new Set(['Le', 'La', 'Les', 'Un', 'Une', 'Des', 'Ce', 'Cette', 'Il', 'Elle',
  'Sur', 'Pour', 'Avec', 'Après', 'Dans', 'Lancé', 'Annoncé', 'Selon', 'Deux', 'Trois',
  'Quatre', 'Premier', 'Première', 'Alors', 'Mais', 'Quand', 'Son', 'Sa', 'Ses', 'Leur']);
const sig = (s) => (s.match(/\d+/g) || [])[0] || '';

function chipsFrom(body) {
  const found = [];
  const sigs = new Set();
  const push = (c) => {
    if (c.length < 3 || c.length > 20) return false;
    if (DATE_RE.test(c)) return false;
    if (/^\d{4}$/.test(c)) return false;                    // bare year
    const s = sig(c);
    if (s && sigs.has(s)) return false;
    if (found.some((f) => f.toLowerCase().includes(c.toLowerCase())
      || c.toLowerCase().includes(f.toLowerCase()))) return false;
    found.push(c); if (s) sigs.add(s);
    return found.length >= 3;
  };
  for (const re of CHIP_PATTERNS) {
    let m; re.lastIndex = 0;
    while ((m = re.exec(body))) {
      const c = m[0].replace(/\s+/g, ' ').trim().replace(/^[.,\-—–]+|[.,\-—–]+$/g, '');
      if (push(c)) return found;
    }
  }
  // Fallback: heads of proper nouns, so the chip row is never empty.
  if (found.length < 2) {
    const words = body.replace(/[«»"“”()]/g, ' ').split(/\s+/)
      .map((w) => w.replace(/^[^A-Za-zÀ-ÿ0-9]+|[^A-Za-zÀ-ÿ0-9]+$/g, ''));
    const target = found.length + 2;
    for (let i = 0; i < words.length; i++) {
      const w = words[i], prev = words[i - 1] || '';
      if (!/^[A-ZÀ-Ý][A-Za-zÀ-ÿ0-9.-]{2,13}$/.test(w)) continue;
      if (STOPCAP.has(w)) continue;
      if (/^[A-ZÀ-Ý]/.test(prev) && !STOPCAP.has(prev)) continue;  // keep only the head
      push(w);
      if (found.length >= target || found.length >= 3) break;
    }
  }
  return found;
}

/* -------------------------------------------------------- 3. voice script */
const scriptRaw = section('Script voix off');
const sp = paras(scriptRaw);
const BRIEF_BUDGET = +(process.env.JIA_BRIEF_CHARS || 140);

let intro = '';
const voiceBriefs = [];   // { idx, headline, body, gag:[..]|null }
let tail = '';

for (const p of sp) {
  const bm = p.match(/^\*\*\s*(Un|Deux|Trois|Quatre|Cinq|Six)\s*[—–-]\s*([\s\S]+?)\*\*\s*([\s\S]*)$/);
  if (bm) {
    let rest = bm[3];
    let gag = null;
    const gm = rest.match(/\*([^*]{10,120})\*\s*$/);
    if (gm) {
      gag = gm[1].split(/(?<=[.!?])\s+/).map((w) => w.trim()).filter(Boolean).slice(0, 3);
      rest = rest.slice(0, gm.index);
    }
    voiceBriefs.push({
      idx: NUM_WORDS.indexOf(bm[1]) + 1,
      headline: cap1(stripMd(bm[2]).replace(/\.$/, '')),
      body: stripMd(rest),
      gag,
    });
    continue;
  }
  if (!intro && /journal\s*ia/i.test(p)) { intro = stripMd(p); continue; }
  if (/voil[àa]|commente/i.test(p)) tail = stripMd(p);
}

/* CTA keyword */
const ctaSection = section('CTA') + '\n' + tail;
const motM = ctaSection.match(/[Cc]ommente\s+\*{0,2}([A-ZÉÈÀÂÎÔÛ][A-ZÉÈÀÂÎÔÛ0-9_-]{2,20})/);
const MOT = motM ? motM[1] : 'VEILLE';

/* split tail into outro + cta */
let outroTxt = '', ctaTxt = '';
if (tail) {
  const i = tail.search(/\bTu veux\b/i);
  if (i > 0) { outroTxt = tail.slice(0, i).trim(); ctaTxt = tail.slice(i).trim(); }
  else { outroTxt = tail; ctaTxt = `Tu veux ton propre Journal IA automatique chaque matin ? Commente ${MOT}.`; }
}
if (!intro) intro = `Journal IA, ${dateSpoken}. C'est parti.`;
if (!outroTxt) outroTxt = 'Voilà ton actu IA.';
/* The parsed outro is often a single short clause — give it the signature closing line. */
if (outroTxt.length < 55) outroTxt += " L'IA avance chaque jour, que tu suives ou pas.";

/* ---------------------------------------------------- running-gag pairs
 * Retour Tony 2026-08-17 : MAXIMUM 2 adjectifs empilés, jamais 3, et le
 * vocabulaire doit changer d'une édition à l'autre. On ignore donc le nombre
 * de mots écrit dans le .md et on pioche une paire par rotation déterministe
 * (jour de l'année × 2 + index du gag) : les deux gags d'une même édition
 * diffèrent toujours, et deux éditions consécutives ne réutilisent pas la même paire.
 */
const GAG_PAIRS = [
  ["C'est indéniable.", 'Irréfutable.'],
  ["C'est incontestable.", 'Imparable.'],
  ["C'est implacable.", 'Sans appel.'],
  ["C'est indiscutable.", 'Formel.'],
  ["C'est irréfutable.", 'Cash.'],
  ["C'est imparable.", 'Indiscutable.'],
];
const dayOfYear = Math.floor((Date.UTC(year, monthIdx, day) - Date.UTC(year, 0, 0)) / 86400000);
const gagPair = (i) => GAG_PAIRS[(dayOfYear * 2 + i) % GAG_PAIRS.length];

/* ------------------------------------------------- 4. assemble segments */
const ACCENTS = ['google', 'openai', 'deepseek', 'dbx'];
const segments = [];
let gagIdx = 0;
const briefs = [];

segments.push({ id: 'intro', role: 'intro', tempo: 1.12, text: ttsText(intro), display: intro });

voiceBriefs.forEach((vb, i) => {
  const card = cards[i] || {};
  const spokenBody = condense(vb.body || card.body || '', BRIEF_BUDGET - vb.headline.length);
  const spoken = `${NUM_WORDS[i]}. ${vb.headline}. ${spokenBody}`;
  const id = `b${i + 1}`;
  segments.push({ id, role: 'brief', brief: i, tempo: 1.12, text: ttsText(spoken), display: spoken });
  briefs.push({
    n: i + 1,
    source: card.source || vb.headline.split(' ')[0],
    title: cap1(card.title || vb.headline),
    accent: ACCENTS[i % ACCENTS.length],
    sub: condense((vb.body || card.body || '').replace(/[«»"“”]/g, ''), 82),
    chips: chipsFrom(`${card.body || ''} ${vb.body || ''} ${card.title || ''}`),
    segId: id,
  });
  if (vb.gag && vb.gag.length) {
    const gid = `g${i + 1}`;
    const words = gagPair(gagIdx++);          // 2 mots max, vocabulaire tournant
    const line = words.join(' ');
    segments.push({ id: gid, role: 'gag', brief: i, tempo: 1.12, text: ttsText(line), display: line, words });
  }
});

segments.push({ id: 'outro', role: 'outro', tempo: 1.12, text: ttsText(outroTxt), display: outroTxt });
segments.push({ id: 'cta', role: 'cta', tempo: 1.12, text: ttsText(ctaTxt), display: ctaTxt });
segments.push({ id: 'cd', role: 'countdown', tempo: 1.0, text: 'Trois. Deux. Un.' });
segments.push({ id: 'tag', role: 'tag', tempo: 1.05, text: 'Journal I.A. Chaque matin.' });

/* --------------------------------------------------------- 5. captions */
const HL = ['hot', 'violet', 'orange'];
function captionTokens(text) {
  const words = text.replace(/[«»"“”]/g, '')
    .replace(/^(Un|Deux|Trois|Quatre|Cinq|Six)\.\s+/, '')   // the card already shows the number
    .split(/\s+/).filter(Boolean);
  const toks = [];
  let buf = [];
  const flush = () => { if (buf.length) { toks.push(buf); buf = []; } };
  for (const w of words) {
    buf.push(w);
    const len = buf.join(' ').length;
    if (/[.!?:]$/.test(w) || buf.length >= 3 || len >= 15) flush();
  }
  flush();
  // a lone stub token ("?", "IA.") reads as a glitch — glue it to the previous chunk
  for (let i = toks.length - 1; i > 0; i--) {
    if (toks[i].join(' ').replace(/[.,;:!?]/g, '').length <= 2) {
      toks[i - 1] = toks[i - 1].concat(toks[i]); toks.splice(i, 1);
    }
  }
  let hi = 0;
  let sentenceStart = true;
  return toks.map((g) => g.map((w) => {
    const clean = w.replace(/[.,;:!?]+$/, '');
    const punct = w.slice(clean.length);
    const atStart = sentenceStart;
    sentenceStart = /[.!?]$/.test(w);
    const isCap = /^[A-ZÀ-Ý]/.test(clean) || /^[LDCJNSM]'[A-ZÀ-Ý]/.test(clean);
    const strong = /\d/.test(clean) || (isCap && !atStart && clean.length >= 4);
    const up = clean.toUpperCase().replace(/&/g, '&amp;').replace(/</g, '&lt;');
    if (strong) { const c = HL[hi++ % HL.length]; return `<span class="${c}">${up}</span>${punct}`; }
    return up + punct;
  }).join(' '));
}
for (const s of segments) {
  if (s.role === 'countdown' || s.role === 'tag') { s.caps = []; continue; }
  /* captions read the DISPLAY text, never the TTS text ("3.7", not "3 point 7") */
  s.caps = captionTokens(stripMd(s.display || s.text));
}

/* ------------------------------------------------------------- 6. output */
const edition = {
  date: iso, dateLabel, dateShort, dateSpoken,
  title: h1,
  mot: MOT,
  briefs,
  gagCount: segments.filter((s) => s.role === 'gag').length,
  segments,
  estChars: segments.reduce((a, s) => a + s.text.length, 0),
  estSpeechSec: +(segments.reduce((a, s) => a + s.text.length, 0) / 18).toFixed(1),
};

const json = JSON.stringify(edition, null, 2);
if (OUT) fs.writeFileSync(OUT, json);
console.error(`[parse] ${iso} · ${briefs.length} brèves · ${edition.gagCount} gags · ${segments.length} segments · ~${edition.estSpeechSec}s de parole estimée`);
if (!OUT) console.log(json);

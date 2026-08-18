#!/usr/bin/env node
/**
 * brain.mjs — file analysed posts as markdown cards, one file per theme, never duplicated.
 *
 *   cat cards.json | node brain.mjs --brain /work/second-cerveau
 *   node brain.mjs --brain /work/second-cerveau --list        # what is fetched but not yet filed
 *   node brain.mjs --brain /work/second-cerveau --stats
 *
 * cards.json is an array produced by Claude after reading _raw/<shortcode>/:
 *   [{ "shortcode": "...", "theme": "productivite",
 *      "hook": "...", "idea": "...", "why": "...", "structure": "..." }]
 *
 * Dedup is by the `<!-- post:SHORTCODE -->` marker, scanned across every theme file,
 * so re-running the pipeline can never file the same post twice.
 */

import { readFile, writeFile, mkdir, readdir, appendFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

function parseArgs(argv) {
  const out = { brain: null, list: false, stats: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--brain') out.brain = argv[++i];
    else if (a === '--list') out.list = true;
    else if (a === '--stats') out.stats = true;
  }
  if (!out.brain) {
    console.error('usage: brain.mjs --brain <dir> [--list|--stats]  (cards JSON on stdin)');
    process.exit(2);
  }
  return out;
}

const args = parseArgs(process.argv);
const BRAIN = path.resolve(args.brain);
const RAW = path.join(BRAIN, '_raw');
const STATE = path.join(BRAIN, '_state', 'index.json');

const slug = (s) =>
  s
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 48) || 'divers';

const titleCase = (s) => s.charAt(0).toUpperCase() + s.slice(1);

async function loadState() {
  if (!existsSync(STATE)) return { posts: {} };
  try {
    return JSON.parse(await readFile(STATE, 'utf8'));
  } catch {
    return { posts: {} };
  }
}

/** Every shortcode already written into any theme file. */
async function filedShortcodes() {
  const filed = new Map();
  if (!existsSync(BRAIN)) return filed;
  for (const e of await readdir(BRAIN, { withFileTypes: true })) {
    if (!e.isFile() || !e.name.endsWith('.md') || e.name === 'README.md') continue;
    const body = await readFile(path.join(BRAIN, e.name), 'utf8');
    for (const m of body.matchAll(/<!--\s*post:([A-Za-z0-9_-]+)\s*-->/g)) {
      filed.set(m[1], e.name);
    }
  }
  return filed;
}

async function readMeta(shortcode) {
  const f = path.join(RAW, shortcode, 'meta.json');
  if (!existsSync(f)) return null;
  try {
    return JSON.parse(await readFile(f, 'utf8'));
  } catch {
    return null;
  }
}

// ---- read-only modes -------------------------------------------------------

if (args.list || args.stats) {
  const state = await loadState();
  const filed = await filedShortcodes();
  const all = Object.keys(state.posts);
  const unfiled = all.filter((s) => !filed.has(s));

  if (args.stats) {
    const byTheme = {};
    for (const [, file] of filed) byTheme[file] = (byTheme[file] ?? 0) + 1;
    console.log(`second brain: ${BRAIN}`);
    console.log(`  fetched : ${all.length}`);
    console.log(`  filed   : ${filed.size}`);
    console.log(`  pending : ${unfiled.length}`);
    console.log('  themes  :');
    for (const [file, n] of Object.entries(byTheme).sort((a, b) => b[1] - a[1])) {
      console.log(`    ${String(n).padStart(3)}  ${file}`);
    }
  } else {
    for (const s of unfiled) {
      const meta = await readMeta(s);
      console.log(
        JSON.stringify({
          shortcode: s,
          url: state.posts[s].url,
          type: state.posts[s].type,
          owner: state.posts[s].owner,
          transcript_status: state.posts[s].transcript_status,
          has_transcript: existsSync(path.join(RAW, s, 'transcript.txt')),
          caption_preview: (meta?.caption ?? '').slice(0, 160),
        })
      );
    }
  }
  process.exit(0);
}

// ---- write mode ------------------------------------------------------------

const stdin = await new Promise((resolve) => {
  let buf = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (d) => (buf += d));
  process.stdin.on('end', () => resolve(buf));
});

if (!stdin.trim()) {
  console.error('[brain] nothing on stdin — expected a JSON array of cards');
  process.exit(2);
}

let cards;
try {
  cards = JSON.parse(stdin);
} catch (err) {
  console.error(`[brain] invalid JSON on stdin: ${err.message}`);
  process.exit(2);
}
if (!Array.isArray(cards)) cards = [cards];

const state = await loadState();
const filed = await filedShortcodes();
await mkdir(BRAIN, { recursive: true });

let written = 0;
let skipped = 0;

for (const card of cards) {
  const { shortcode } = card;
  if (!shortcode) {
    console.error('[brain] card without shortcode, skipped');
    skipped++;
    continue;
  }
  if (filed.has(shortcode)) {
    console.error(`[brain] − ${shortcode} already filed in ${filed.get(shortcode)}`);
    skipped++;
    continue;
  }

  const meta = (await readMeta(shortcode)) ?? {};
  const theme = slug(card.theme ?? 'divers');
  const file = path.join(BRAIN, `${theme}.md`);

  if (!existsSync(file)) {
    await writeFile(file, `# ${titleCase((card.theme ?? 'divers').trim())}\n\n_Fiches issues de mes posts Instagram enregistrés._\n`);
  }

  const stats = [
    meta.owner ? `@${meta.owner}` : null,
    meta.type ?? null,
    meta.like_count ? `${Intl.NumberFormat('fr-FR').format(meta.like_count)} likes` : null,
    meta.duration_s ? `${Math.round(meta.duration_s)}s` : null,
  ]
    .filter(Boolean)
    .join(' · ');

  const lines = [
    '',
    `<!-- post:${shortcode} -->`,
    `## ${card.hook ? `« ${card.hook.replace(/^«\s*|\s*»$/g, '')} »` : shortcode}`,
    '',
    `- **Idée** — ${card.idea ?? '—'}`,
    `- **Pourquoi ça marche** — ${card.why ?? '—'}`,
    card.structure ? `- **Structure** — ${card.structure}` : null,
    card.angle ? `- **Angle** — ${card.angle}` : null,
    `- **Source** — ${stats || 'instagram'} · [voir le post](${meta.url ?? `https://www.instagram.com/p/${shortcode}/`})`,
    '',
  ]
    .filter((l) => l !== null)
    .join('\n');

  await appendFile(file, lines);
  filed.set(shortcode, `${theme}.md`);

  if (state.posts[shortcode]) {
    state.posts[shortcode].filed = true;
    state.posts[shortcode].theme = theme;
    state.posts[shortcode].filed_at = new Date().toISOString();
  }
  written++;
  console.error(`[brain] ✓ ${shortcode} → ${theme}.md`);
}

await mkdir(path.dirname(STATE), { recursive: true });
await writeFile(STATE, JSON.stringify(state, null, 2));
console.error(`[brain] ${written} filed, ${skipped} skipped`);

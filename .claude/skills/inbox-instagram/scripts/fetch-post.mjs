#!/usr/bin/env node
/**
 * fetch-post.mjs — download + transcribe saved posts into the second brain's raw inbox.
 *
 *   node fetch-post.mjs --in posts.json --brain /work/second-cerveau [--limit 10] [--keep-video]
 *
 * For each post not already in _state/index.json it writes:
 *   _raw/<shortcode>/meta.json      normalized metadata + caption
 *   _raw/<shortcode>/transcript.txt spoken words (reels), when a backend succeeded
 *
 * Transcription cascade (first one that works wins):
 *   1. hyperframes transcribe  (local whisper-cpp)
 *   2. yt-dlp subtitles        (when Instagram exposes them)
 *   3. none -> transcript_status "pending", for Claude to fill via the tokscript MCP
 *
 * This script does NO analysis. Hook / angle / theme extraction is Claude's job,
 * reading the files this produces.
 */

import { readFile, writeFile, mkdir, readdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { homedir } from 'node:os';
import path from 'node:path';

const exec = promisify(execFile);

function parseArgs(argv) {
  const out = { in: null, brain: null, limit: 0, keepVideo: false, cookies: null };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--in') out.in = argv[++i];
    else if (a === '--brain') out.brain = argv[++i];
    else if (a === '--limit') out.limit = Number(argv[++i]);
    else if (a === '--cookies') out.cookies = argv[++i];
    else if (a === '--keep-video') out.keepVideo = true;
  }
  if (!out.in || !out.brain) {
    console.error('usage: fetch-post.mjs --in <posts.json> --brain <dir> [--limit N] [--keep-video]');
    process.exit(2);
  }
  return out;
}

const args = parseArgs(process.argv);
const BRAIN = path.resolve(args.brain);
const RAW = path.join(BRAIN, '_raw');
const STATE = path.join(BRAIN, '_state', 'index.json');

async function loadState() {
  if (!existsSync(STATE)) return { posts: {} };
  try {
    return JSON.parse(await readFile(STATE, 'utf8'));
  } catch {
    return { posts: {} };
  }
}

async function saveState(state) {
  await mkdir(path.dirname(STATE), { recursive: true });
  await writeFile(STATE, JSON.stringify(state, null, 2));
}

function cookieFile(explicit) {
  const c = [explicit, process.env.IG_COOKIES_FILE, path.join(homedir(), '.config', 'inbox-instagram', 'cookies.txt')];
  return c.find((f) => f && existsSync(f)) ?? null;
}

/** Locate a hyperframes binary from any sibling project (it is not installed globally). */
async function findHyperframes() {
  const roots = ['/work/autoboost-neon-videos', '/work'];
  for (const root of roots) {
    if (!existsSync(root)) continue;
    let entries;
    try {
      entries = await readdir(root, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const e of entries) {
      if (!e.isDirectory()) continue;
      const bin = path.join(root, e.name, 'node_modules', '.bin', 'hyperframes');
      if (existsSync(bin)) return bin;
    }
  }
  return null;
}

async function transcribeWithHyperframes(mediaFile) {
  const bin = await findHyperframes();
  if (!bin) return null;
  try {
    const { stdout } = await exec(bin, ['transcribe', mediaFile, '--json', '--optional'], {
      timeout: 10 * 60 * 1000,
      maxBuffer: 32 * 1024 * 1024,
    });
    const res = JSON.parse(stdout.trim().split('\n').pop());
    if (res.skipped || !res.ok) return null;
    const words = res.words ?? res.segments ?? [];
    const text = Array.isArray(words)
      ? words.map((w) => w.word ?? w.text ?? '').join(' ').replace(/\s+/g, ' ').trim()
      : '';
    return text || null;
  } catch {
    return null;
  }
}

/** Strip VTT/SRT markup down to plain spoken text. */
function subsToText(raw) {
  const lines = [];
  for (let line of raw.split('\n')) {
    line = line.trim();
    if (!line || line === 'WEBVTT' || /^\d+$/.test(line)) continue;
    if (line.includes('-->') || /^(Kind|Language|NOTE):/.test(line)) continue;
    line = line.replace(/<[^>]*>/g, '').trim();
    if (line && lines[lines.length - 1] !== line) lines.push(line);
  }
  return lines.join(' ').replace(/\s+/g, ' ').trim();
}

async function downloadPost(post, dir, cookies) {
  const ytdlp = ['/home/claude/tools/bin/yt-dlp', 'yt-dlp'].find(
    (p) => p.startsWith('/') ? existsSync(p) : true
  );
  const argv = [
    post.url,
    '-o', path.join(dir, '%(id)s.%(ext)s'),
    '--write-info-json',
    '--write-subs', '--write-auto-subs', '--sub-langs', 'all,-live_chat',
    '--no-warnings', '--no-progress',
  ];
  if (cookies) argv.push('--cookies', cookies);
  if (!post.is_video) argv.push('--skip-download');

  try {
    await exec(ytdlp, argv, { timeout: 5 * 60 * 1000, maxBuffer: 32 * 1024 * 1024 });
    return { ok: true };
  } catch (err) {
    return { ok: false, error: (err.stderr || err.message || '').slice(0, 400) };
  }
}

const posts = JSON.parse(await readFile(args.in, 'utf8'));
const state = await loadState();
const cookies = cookieFile(args.cookies);

// A post is pending if never seen, or seen but failed (transient IG errors are common).
const pending = posts.filter((p) => {
  const seen = state.posts[p.shortcode];
  return !seen || seen.failed === true;
});
const batch = args.limit ? pending.slice(0, args.limit) : pending;

console.error(
  `[fetch-post] ${posts.length} saved · ${pending.length} new · processing ${batch.length}` +
    (cookies ? ` · cookies ${cookies}` : ' · NO COOKIES (downloads will fail)')
);

let done = 0;
let failed = 0;

for (const post of batch) {
  const dir = path.join(RAW, post.shortcode);
  await mkdir(dir, { recursive: true });

  const dl = await downloadPost(post, dir, cookies);
  const files = existsSync(dir) ? await readdir(dir) : [];
  const media = files.find((f) => /\.(mp4|mkv|webm)$/.test(f));
  const subFile = files.find((f) => /\.(vtt|srt)$/.test(f));

  let transcript = null;
  let backend = null;

  if (subFile) {
    transcript = subsToText(await readFile(path.join(dir, subFile), 'utf8'));
    if (transcript) backend = 'yt-dlp-subs';
  }
  if (!transcript && media) {
    transcript = await transcribeWithHyperframes(path.join(dir, media));
    if (transcript) backend = 'whisper';
  }

  // yt-dlp's own info.json carries description/uploader even when our listing was thin.
  const infoFile = files.find((f) => /\.info\.json$/.test(f));
  let info = {};
  if (infoFile) {
    try {
      info = JSON.parse(await readFile(path.join(dir, infoFile), 'utf8'));
    } catch { /* ignore */ }
  }

  const meta = {
    ...post,
    caption: post.caption || info.description || '',
    owner: post.owner || info.uploader || info.channel || null,
    like_count: post.like_count ?? info.like_count ?? null,
    comment_count: post.comment_count ?? info.comment_count ?? null,
    duration_s: info.duration ?? null,
    downloaded: dl.ok,
    download_error: dl.ok ? null : dl.error,
    transcript_backend: backend,
    transcript_status: transcript ? 'ok' : post.is_video ? 'pending' : 'not_applicable',
    fetched_at: new Date().toISOString(),
  };

  await writeFile(path.join(dir, 'meta.json'), JSON.stringify(meta, null, 2));
  if (transcript) await writeFile(path.join(dir, 'transcript.txt'), transcript + '\n');

  if (media && !args.keepVideo) await rm(path.join(dir, media), { force: true });

  const hardFail = !dl.ok && !transcript && !meta.caption;
  const prev = state.posts[post.shortcode] ?? {};
  state.posts[post.shortcode] = {
    fetched_at: meta.fetched_at,
    type: post.type,
    owner: meta.owner,
    url: post.url,
    transcript_status: meta.transcript_status,
    failed: hardFail, // retried on the next run
    attempts: (prev.attempts ?? 0) + 1,
    filed: prev.filed ?? false, // brain.mjs flips this once a card is written
    theme: prev.theme ?? null,
  };

  if (hardFail) {
    failed++;
    console.error(`[fetch-post] ✗ ${post.shortcode} — ${dl.error?.split('\n')[0] ?? 'download failed'}`);
  } else {
    done++;
    console.error(`[fetch-post] ✓ ${post.shortcode} (${post.type}, transcript: ${meta.transcript_status}${backend ? `/${backend}` : ''})`);
  }

  await saveState(state);
  await new Promise((r) => setTimeout(r, 800 + Math.random() * 1200));
}

console.error(`[fetch-post] done: ${done} ok, ${failed} failed, ${pending.length - batch.length} still queued`);

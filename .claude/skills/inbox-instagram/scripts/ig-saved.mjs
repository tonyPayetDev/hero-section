#!/usr/bin/env node
/**
 * ig-saved.mjs — list Instagram saved posts.
 *
 * Two sources:
 *   --source session   (default) private API /api/v1/feed/saved/posts/ using session cookies
 *   --source export    parse a downloaded Instagram data export (saved_posts.json)
 *
 * Output: JSON array of normalized posts on stdout, or to --out <file>.
 *
 * Cookies (session mode) come from, in order:
 *   --cookies <netscape.txt>
 *   $IG_COOKIES_FILE
 *   ~/.config/inbox-instagram/cookies.txt
 *   $IG_COOKIE  (raw "sessionid=..; ds_user_id=..; csrftoken=.." string)
 */

import { readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';

const IG_APP_ID = '936619743392459';
const UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';

function parseArgs(argv) {
  const out = { source: 'session', limit: 0, out: null, cookies: null, export: null };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--source') out.source = argv[++i];
    else if (a === '--limit') out.limit = Number(argv[++i]);
    else if (a === '--out') out.out = argv[++i];
    else if (a === '--cookies') out.cookies = argv[++i];
    else if (a === '--export') { out.export = argv[++i]; out.source = 'export'; }
  }
  return out;
}

/** Netscape cookies.txt -> "k=v; k=v" for instagram.com */
function cookiesFromNetscape(text) {
  const jar = {};
  for (const line of text.split('\n')) {
    if (!line.trim() || line.startsWith('#')) continue;
    const f = line.split('\t');
    if (f.length < 7) continue;
    if (!f[0].includes('instagram.com')) continue;
    jar[f[5].trim()] = f[6].trim();
  }
  return jar;
}

async function loadCookies(explicit) {
  const candidates = [
    explicit,
    process.env.IG_COOKIES_FILE,
    path.join(homedir(), '.config', 'inbox-instagram', 'cookies.txt'),
  ].filter(Boolean);

  for (const file of candidates) {
    if (existsSync(file)) {
      const jar = cookiesFromNetscape(await readFile(file, 'utf8'));
      if (jar.sessionid) return { jar, file };
    }
  }
  if (process.env.IG_COOKIE) {
    const jar = {};
    for (const part of process.env.IG_COOKIE.split(';')) {
      const i = part.indexOf('=');
      if (i > 0) jar[part.slice(0, i).trim()] = part.slice(i + 1).trim();
    }
    if (jar.sessionid) return { jar, file: '$IG_COOKIE' };
  }
  throw new Error(
    'No Instagram session cookie found.\n' +
      'Export cookies.txt (Netscape format) from a logged-in browser and put it at\n' +
      '  ~/.config/inbox-instagram/cookies.txt\n' +
      'or set $IG_COOKIE="sessionid=...; ds_user_id=...; csrftoken=..."'
  );
}

const cookieHeader = (jar) => Object.entries(jar).map(([k, v]) => `${k}=${v}`).join('; ');

/** Normalize one media object from the private API. */
function normalize(media) {
  const type = media.media_type === 2 ? 'reel' : media.media_type === 8 ? 'carousel' : 'post';
  const caption = media.caption?.text ?? '';
  const shortcode = media.code;
  const children = (media.carousel_media || []).map((c) => ({
    is_video: c.media_type === 2,
    image_url: c.image_versions2?.candidates?.[0]?.url ?? null,
    video_url: c.video_versions?.[0]?.url ?? null,
  }));
  return {
    shortcode,
    url: `https://www.instagram.com/p/${shortcode}/`,
    type,
    is_video: media.media_type === 2,
    caption,
    owner: media.user?.username ?? null,
    owner_full_name: media.user?.full_name ?? null,
    taken_at: media.taken_at ? new Date(media.taken_at * 1000).toISOString() : null,
    like_count: media.like_count ?? null,
    comment_count: media.comment_count ?? null,
    play_count: media.play_count ?? media.view_count ?? null,
    image_url: media.image_versions2?.candidates?.[0]?.url ?? null,
    video_url: media.video_versions?.[0]?.url ?? null,
    children,
    source: 'session',
  };
}

async function fromSession({ cookies, limit }) {
  const { jar, file } = await loadCookies(cookies);
  console.error(`[ig-saved] cookies: ${file} (user ${jar.ds_user_id ?? '?'})`);

  const headers = {
    'User-Agent': UA,
    'X-IG-App-ID': IG_APP_ID,
    'X-CSRFToken': jar.csrftoken ?? '',
    Referer: 'https://www.instagram.com/',
    Accept: '*/*',
    Cookie: cookieHeader(jar),
  };

  const posts = [];
  let cursor = null;
  for (let page = 1; page <= 50; page++) {
    const url = new URL('https://www.instagram.com/api/v1/feed/saved/posts/');
    if (cursor) url.searchParams.set('max_id', cursor);

    const res = await fetch(url, { headers });
    if (res.status === 401 || res.status === 403) {
      throw new Error(`Instagram rejected the session (HTTP ${res.status}). Re-export your cookies.`);
    }
    if (!res.ok) throw new Error(`Instagram HTTP ${res.status}: ${(await res.text()).slice(0, 200)}`);

    const body = await res.json();
    const items = body.items ?? [];
    for (const it of items) {
      const media = it.media ?? it;
      if (media?.code) posts.push(normalize(media));
    }
    console.error(`[ig-saved] page ${page}: +${items.length} (total ${posts.length})`);

    if (limit && posts.length >= limit) break;
    if (!body.more_available || !body.next_max_id) break;
    cursor = body.next_max_id;
    await new Promise((r) => setTimeout(r, 1200 + Math.random() * 1800)); // be polite
  }
  return limit ? posts.slice(0, limit) : posts;
}

/** Instagram data export: saved_posts.json / saved_collections.json */
async function fromExport({ export: target, limit }) {
  let file = target;
  if (!existsSync(file)) throw new Error(`Export not found: ${file}`);

  const stat = await import('node:fs/promises').then((m) => m.stat(file));
  if (stat.isDirectory()) {
    const { readdir } = await import('node:fs/promises');
    const hit = [];
    const walk = async (dir, depth = 0) => {
      if (depth > 4) return;
      for (const e of await readdir(dir, { withFileTypes: true })) {
        const p = path.join(dir, e.name);
        if (e.isDirectory()) await walk(p, depth + 1);
        else if (/saved_posts\.json$/.test(e.name)) hit.push(p);
      }
    };
    await walk(file);
    if (!hit.length) throw new Error(`No saved_posts.json found under ${file}`);
    file = hit[0];
  }
  console.error(`[ig-saved] export: ${file}`);

  const raw = JSON.parse(await readFile(file, 'utf8'));
  const entries = raw.saved_saved_media ?? raw.saved_media ?? [];
  const posts = [];
  for (const e of entries) {
    const map = e.string_map_data ?? {};
    const key = Object.keys(map).find((k) => map[k]?.href) ?? 'Saved on';
    const href = map[key]?.href;
    if (!href) continue;
    const m = href.match(/instagram\.com\/(?:p|reel|tv)\/([^/?#]+)/);
    if (!m) continue;
    posts.push({
      shortcode: m[1],
      url: `https://www.instagram.com/p/${m[1]}/`,
      type: /\/reel\//.test(href) ? 'reel' : 'unknown',
      is_video: /\/reel\//.test(href),
      caption: '',
      owner: e.title || null,
      taken_at: map[key]?.timestamp ? new Date(map[key].timestamp * 1000).toISOString() : null,
      children: [],
      source: 'export',
    });
  }
  return limit ? posts.slice(0, limit) : posts;
}

const args = parseArgs(process.argv);

let posts;
try {
  posts = args.source === 'export' ? await fromExport(args) : await fromSession(args);
} catch (err) {
  // Operator-facing failure: show the message, not a Node stack trace.
  console.error(`\n[ig-saved] ${err.message}\n`);
  process.exit(1);
}

// Newest first, de-duplicated by shortcode.
const seen = new Set();
const unique = posts.filter((p) => !seen.has(p.shortcode) && seen.add(p.shortcode));

const json = JSON.stringify(unique, null, 2);
if (args.out) {
  await writeFile(args.out, json);
  console.error(`[ig-saved] wrote ${unique.length} posts -> ${args.out}`);
} else {
  process.stdout.write(json + '\n');
}

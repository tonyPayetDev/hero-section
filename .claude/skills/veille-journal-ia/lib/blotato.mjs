#!/usr/bin/env node
/**
 * blotato.mjs <video.mp4> <edition.json> <isoWhenUTC> [--dry]
 *
 * Binary upload (presigned URL + raw PUT — never the previsualisation URL,
 * Cloudflare 403s it) then one scheduled post per network.
 *
 * Auth: BLOTATO_API_KEY (env or /work/.blotato.env). Without it the script
 * writes work/blotato-plan.json and exits 3 so the caller (n8n, which holds the
 * Blotato credential) can do the scheduling itself.
 */
import fs from 'node:fs';
import path from 'node:path';

const [, , VIDEO, EDITION, WHEN, ...flags] = process.argv;
const DRY = flags.includes('--dry');
const API = process.env.BLOTATO_API_URL || 'https://backend.blotato.com';
let KEY = process.env.BLOTATO_API_KEY || '';
if (!KEY && fs.existsSync('/work/.blotato.env')) {
  KEY = (fs.readFileSync('/work/.blotato.env', 'utf8').match(/BLOTATO_API_KEY\s*=\s*"?([^"\n]+)/) || [, ''])[1];
}

const ed = JSON.parse(fs.readFileSync(EDITION, 'utf8'));
const D = ed.dateLabel;
const heads = ed.briefs.map((b) => `${b.source} — ${b.title}`);
const caption = [
  `📰 Journal IA — ${D}`,
  '',
  ...heads.map((h) => `• ${h}`),
  '',
  `Cette vidéo a été produite par VideoBoost. Tu veux le même système ? Commente ${ed.mot} — seulement si t'as un business.`,
  '',
  // 5 hashtags MAXIMUM : Instagram rejette le post au-delà ("Instagram allows a
  // maximum of 5 hashtags per post"). Il y en avait 6 — le post Instagram aurait
  // échoué même une fois le plan correctement écrit. Ne pas en rajouter.
  '#IA #veilleIA #automatisation #n8n #AutomationBoost',
].join('\n');

const TARGETS = [
  { platform: 'tiktok', accountId: '36488', targetType: 'tiktok',
    extra: { privacyLevel: 'PUBLIC_TO_EVERYONE', isAiGenerated: true, isYourBrand: true, isBrandedContent: false, disabledComments: false, disabledDuet: false, disabledStitch: false } },
  { platform: 'instagram', accountId: '54617', targetType: 'instagram', extra: { mediaType: 'reel', shareToFeed: true } },
  { platform: 'youtube', accountId: '45006', targetType: 'youtube',
    extra: { title: `Journal IA — ${D}`, privacyStatus: 'public', shouldNotifySubscribers: false } },
  { platform: 'facebook', accountId: '43538', targetType: 'facebook', extra: { pageId: '1288852254291983', mediaType: 'reel' } },
  { platform: 'linkedin', accountId: '25882', targetType: 'linkedin', extra: {} },
];

const plan = { when: WHEN, caption, video: VIDEO, targets: TARGETS };
const planPath = path.join(path.dirname(EDITION), 'blotato-plan.json');
fs.writeFileSync(planPath, JSON.stringify(plan, null, 2));

if (DRY) { console.error(`[blotato] DRY — plan écrit dans ${planPath}`); process.exit(0); }
if (!KEY) {
  console.error(`[blotato] BLOTATO_API_KEY absente — plan écrit dans ${planPath}, planification déléguée à l'appelant.`);
  process.exit(3);
}

const H = { 'blotato-api-key': KEY, 'Content-Type': 'application/json' };
const j = async (r) => { const t = await r.text(); try { return JSON.parse(t); } catch { return t; } };

/* 1. presigned upload + raw PUT of the binary */
const name = `journal-ia-${ed.date}.mp4`;
const pre = await j(await fetch(`${API}/v2/media/uploads`, {
  method: 'POST', headers: H, body: JSON.stringify({ fileName: name, contentType: 'video/mp4' }),
}));
const putUrl = pre.uploadUrl || pre.url || (pre.data && pre.data.uploadUrl);
const publicUrl = pre.publicUrl || pre.mediaUrl || (pre.data && (pre.data.publicUrl || pre.data.mediaUrl));
if (!putUrl || !publicUrl) { console.error('[blotato] presigned KO:', JSON.stringify(pre).slice(0, 400)); process.exit(1); }

const buf = fs.readFileSync(VIDEO);
const put = await fetch(putUrl, { method: 'PUT', headers: { 'Content-Type': 'video/mp4' }, body: buf });
if (!put.ok) { console.error('[blotato] PUT KO', put.status); process.exit(1); }
console.error(`[blotato] upload OK (${(buf.length / 1048576).toFixed(1)} Mo) → ${publicUrl}`);

/* 2. one scheduled post per network */
const results = [];
for (const t of TARGETS) {
  const body = {
    post: {
      accountId: t.accountId,
      content: { text: caption, platform: t.platform, mediaUrls: [publicUrl] },
      target: { targetType: t.targetType, ...t.extra },
    },
    scheduledTime: WHEN,
  };
  const r = await fetch(`${API}/v2/posts`, { method: 'POST', headers: H, body: JSON.stringify(body) });
  const out = await j(r);
  results.push({ platform: t.platform, ok: r.ok, status: r.status, id: (out && (out.id || (out.data && out.data.id))) || null });
  console.error(`[blotato] ${t.platform.padEnd(10)} ${r.ok ? 'OK' : 'FAIL ' + r.status} ${JSON.stringify(out).slice(0, 160)}`);
}
fs.writeFileSync(planPath, JSON.stringify({ ...plan, publicUrl, results }, null, 2));
process.exit(results.every((r) => r.ok) ? 0 : 1);

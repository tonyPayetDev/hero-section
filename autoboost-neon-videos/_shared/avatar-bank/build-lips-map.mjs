#!/usr/bin/env node
// Build the "lips active" map of every clip in the avatar bank.
//
// WHY: the bank clips are continuous takes in which Tony pauses between sentences.
// A shot cut from a pause looks like a freeze when a cloned-voice track is speaking
// over it. This map records, per clip, the intervals where the mouth actually moves,
// so the shot selector can refuse to place a silent window under an active voice.
//
// METHOD: decode at native fps, crop the mouth region, downscale to 48x48 gray,
// take the mean absolute inter-frame difference, smooth it, then threshold.
// Calibrated on the 3 original clips: speaking ~2-12, still ~0-1.2.
//
// usage: node build-lips-map.mjs [clipsDir] [outJson]
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const FFDIR = '/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static';
const ENV = { ...process.env, PATH: FFDIR + ':' + process.env.PATH };
const CLIPS = process.argv[2] || '/work/autoboost-neon-videos/_shared/avatar-bank/clips';
const OUT = process.argv[3] || '/work/autoboost-neon-videos/_shared/avatar-bank/lips-map.json';

// mouth box in the bank's native 720x1280 framing (measured: mouth sits near 360,470).
// Override with LIPS_CROP="w,h,x,y" when a batch of clips uses a different framing —
// a box tuned for one shot scale lands on the eyes (blinks) or the torso in another,
// which is exactly the false-positive trap documented in LIPS-MAP.md.
const CROP = (() => {
  const o = process.env.LIPS_CROP;
  if (!o) return { w: 300, h: 240, x: 280, y: 360 };
  const [w, h, x, y] = o.split(',').map(Number);
  return { w, h, x, y };
})();
const GW = 48, GH = 48;
const THRESH = Number(process.env.LIPS_THRESH ?? 1.6);   // mean abs diff below this = mouth effectively still
const MIN_ACTIVE = 0.30; // s — ignore shorter blips
const MIN_GAP = 0.20;    // s — bridge micro-pauses inside a sentence

const probe = (f, k) => Number(spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'v',
  '-show_entries', k, '-of', 'default=nk=1:nw=1', f], { env: ENV, encoding: 'utf8' }).stdout.trim().split('\n')[0]);

const out = { generated: new Date().toISOString().slice(0, 10), crop: CROP, thresh: THRESH, clips: {} };
for (const file of fs.readdirSync(CLIPS).filter(f => f.endsWith('.mp4')).sort()) {
  const f = path.join(CLIPS, file);
  const fpsRaw = spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'v', '-show_entries',
    'stream=r_frame_rate', '-of', 'default=nk=1:nw=1', f], { env: ENV, encoding: 'utf8' }).stdout.trim();
  const [nu, de] = fpsRaw.split('/').map(Number);
  const fps = de ? nu / de : nu;
  const dur = probe(f, 'format=duration') || Number(spawnSync('ffprobe', ['-v', 'error', '-show_entries',
    'format=duration', '-of', 'default=nk=1:nw=1', f], { env: ENV, encoding: 'utf8' }).stdout.trim());

  const r = spawnSync('ffmpeg', ['-v', 'error', '-i', f,
    '-vf', `crop=${CROP.w}:${CROP.h}:${CROP.x}:${CROP.y},scale=${GW}:${GH},format=gray`,
    '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], { env: ENV, maxBuffer: 1 << 28 });
  const buf = r.stdout, fsz = GW * GH, nf = Math.floor(buf.length / fsz);
  const m = [];
  for (let i = 1; i < nf; i++) {
    let s = 0; const a = i * fsz, b = (i - 1) * fsz;
    for (let p = 0; p < fsz; p++) s += Math.abs(buf[a + p] - buf[b + p]);
    m.push(s / fsz);
  }
  // 3-tap smoothing so a single duplicated frame does not cut a sentence in two
  const sm = m.map((_, i) => (m[Math.max(0, i - 1)] + m[i] + m[Math.min(m.length - 1, i + 1)]) / 3);

  const raw = [];
  let cur = null;
  sm.forEach((v, i) => {
    const t = (i + 1) / fps;
    if (v >= THRESH) { if (!cur) cur = { start: t, end: t }; else cur.end = t; }
    else if (cur && t - cur.end > MIN_GAP) { raw.push(cur); cur = null; }
  });
  if (cur) raw.push(cur);
  const act = raw.filter(s => s.end - s.start >= MIN_ACTIVE)
    .map(s => ({ start: +s.start.toFixed(2), end: +s.end.toFixed(2) }));

  out.clips[file] = {
    duration: +dur.toFixed(3), fps,
    active: act,
    activeTotal: +act.reduce((a, s) => a + s.end - s.start, 0).toFixed(2),
  };
  console.log(`${file}  dur=${dur.toFixed(2)}s  active=${out.clips[file].activeTotal}s  windows:`);
  act.forEach(s => console.log(`    ${s.start.toFixed(2)} -> ${s.end.toFixed(2)}  (${(s.end - s.start).toFixed(2)}s)`));
}
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log('\nwritten: ' + OUT);

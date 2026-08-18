// Turn the captured PNG states into timed video segments, exact frame counts.
// Uses the concat demuxer (per-image durations) for the typewriter, and a gentle
// zoompan push on the stills so nothing sits perfectly frozen.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';

const FFDIR = '/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static';
const ENV = { ...process.env, PATH: FFDIR + ':' + process.env.PATH };
const W = '/work/autoboost-neon-videos/autoboost-61-dix-questions/work';
const S = `${W}/screens`, C = `${W}/clips`, T = `${W}/tmp`;
fs.mkdirSync(T, { recursive: true });
const FPS = 30;

const run = (args, label) => {
  const r = spawnSync('ffmpeg', ['-y', '-v', 'error', ...args], { env: ENV, encoding: 'utf8' });
  if (r.status !== 0) { console.error(`FAIL ${label}\n${r.stderr}`); process.exit(1); }
};

// encode a list of {png, frames} as one segment with a slow push
function seq(id, items, zoomTo = 1.05) {
  const total = items.reduce((a, i) => a + i.frames, 0);
  const list = items.map(i => `file '${S}/${i.png}.png'\nduration ${(i.frames / FPS).toFixed(6)}`).join('\n')
    + `\nfile '${S}/${items[items.length - 1].png}.png'\n`;
  const lf = `${T}/${id}.txt`;
  fs.writeFileSync(lf, list);
  const zp = `zoompan=z='min(${zoomTo},1+${(zoomTo - 1).toFixed(4)}*on/${total})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=${FPS}`;
  run(['-f', 'concat', '-safe', '0', '-i', lf,
    '-vf', `fps=${FPS},${zp},setsar=1`, '-frames:v', String(total),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', `${C}/${id}.mp4`], id);
  return total;
}

// --- S3 : the two Claudes (right panel appears) -> 85 f
seq('S3', [{ png: 'deux_a', frames: 26 }, { png: 'deux_b', frames: 59 }], 1.04);

// --- S4 : the prompt typing out -> 149 f over 31 states
const PL = 90, STEP = 3;
const states = [];
for (let n = 0; n <= PL; n += STEP) states.push('prompt_' + n);
const base = Math.floor(149 / states.length);          // 4
let rem = 149 - base * states.length;                  // 149-124 = 25
const items = states.map((p, i) => ({ png: p, frames: base + (i >= states.length - rem ? 1 : 0) }));
// let the finished sentence hold a beat: move 10 frames onto the last state
items[items.length - 1].frames += 10;
let over = items.reduce((a, i) => a + i.frames, 0) - 149;
for (let i = 0; over > 0; i = (i + 1) % (items.length - 1)) { if (items[i].frames > 2) { items[i].frames--; over--; } }
seq('S4', items, 1.03);

// --- S6 : one by one -> 51 f
seq('S6', [{ png: 'unepar_a', frames: 16 }, { png: 'unepar_b', frames: 35 }], 1.04);

// --- S7 / S8 : the split -> 94 f / 89 f
seq('S7', [{ png: 'split_l', frames: 94 }], 1.05);
seq('S8', [{ png: 'split_r', frames: 89 }], 1.06);

// --- S11 : endcard -> 48 f
seq('S11', [{ png: 'endcard', frames: 48 }], 1.05);

for (const id of ['S3', 'S4', 'S6', 'S7', 'S8', 'S11']) {
  const n = spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'v', '-count_frames',
    '-show_entries', 'stream=nb_read_frames', '-of', 'default=nk=1:nw=1', `${C}/${id}.mp4`],
    { env: ENV, encoding: 'utf8' }).stdout.trim();
  console.log(`${id}  ${n} frames`);
}

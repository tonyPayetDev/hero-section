// Median F0 of a voice file, by autocorrelation on voiced frames.
// Guard rail: BeFresh must never ship Tony's cloned voice (median F0 ~114-133 Hz).
// Usage: node src/f0.mjs work/voice.mp3
import { execFileSync } from 'node:child_process';

const file = process.argv[2];
const SR = 16000;
const raw = execFileSync('ffmpeg', ['-v', 'error', '-i', file, '-ac', '1', '-ar', String(SR),
  '-f', 'f32le', '-'], { maxBuffer: 1 << 28 });
const x = new Float32Array(raw.buffer, raw.byteOffset, raw.length / 4);

const WIN = Math.round(0.040 * SR);   // 40 ms
const HOP = Math.round(0.010 * SR);   // 10 ms
const MINP = Math.floor(SR / 400);    // 400 Hz ceiling
const MAXP = Math.floor(SR / 70);     // 70 Hz floor

const f0s = [];
let rmsAll = 0, nAll = 0;
for (let i = 0; i + WIN < x.length; i += HOP) {
  let e = 0;
  for (let k = 0; k < WIN; k++) e += x[i + k] * x[i + k];
  rmsAll += e; nAll += WIN;
}
const globalRms = Math.sqrt(rmsAll / nAll);

for (let i = 0; i + WIN < x.length; i += HOP) {
  let e0 = 0;
  for (let k = 0; k < WIN; k++) e0 += x[i + k] * x[i + k];
  if (Math.sqrt(e0 / WIN) < globalRms * 0.7) continue;  // silence / low energy
  let best = 0, bestLag = 0;
  for (let lag = MINP; lag <= MAXP; lag++) {
    let s = 0;
    for (let k = 0; k + lag < WIN; k++) s += x[i + k] * x[i + k + lag];
    const norm = s / (WIN - lag);
    if (norm > best) { best = norm; bestLag = lag; }
  }
  if (bestLag && best / (e0 / WIN) > 0.35) f0s.push(SR / bestLag);
}

f0s.sort((a, b) => a - b);
const q = (p) => f0s[Math.floor(f0s.length * p)];
const dur = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
  '-of', 'csv=p=0', file]).toString().trim();
console.log(`${file}  dur=${Number(dur).toFixed(2)}s  voiced frames=${f0s.length}`);
console.log(`  F0  p25=${q(0.25).toFixed(1)}  MEDIAN=${q(0.5).toFixed(1)} Hz  p75=${q(0.75).toFixed(1)}`);
const med = q(0.5);
if (med >= 105 && med <= 145) console.log('  !! DANGER: median in Tony-clone range (114-133 Hz). Reject.');
else if (med >= 165) console.log('  OK: female register.');
else console.log('  ?? ambiguous register, listen before shipping.');

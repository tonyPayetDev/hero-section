// Diagnostic: comb-filter score of the KICK-band novelty curve across the whole BPM range.
// Prints the ranked local maxima so the tempo can be read off evidence, not from a manifest.
// Usage: node src/beatscan.mjs <file> [seconds] [lowHz] [highHz]
import { execFileSync } from 'node:child_process';

const file = process.argv[2];
const ANA = Number(process.argv[3] || 45);
const LO = process.argv[4] || 40;
const HI = process.argv[5] || 140;
const SR = 22050, HOP = 128;

const raw = execFileSync('ffmpeg', ['-v', 'error', '-i', file, '-t', String(ANA),
  '-ac', '1', '-ar', String(SR), '-af', `highpass=f=${LO},lowpass=f=${HI}`,
  '-f', 'f32le', '-'], { maxBuffer: 1 << 28 });
const x = new Float32Array(raw.buffer, raw.byteOffset, raw.length / 4);
const FPS = SR / HOP, nF = Math.floor(x.length / HOP);

const env = new Float64Array(nF);
for (let i = 0; i < nF; i++) {
  let e = 0; for (let k = 0; k < HOP; k++) e += x[i * HOP + k] ** 2;
  env[i] = Math.sqrt(e / HOP);
}
const nov = new Float64Array(nF);
for (let i = 1; i < nF; i++) {
  const d = Math.log(env[i] + 1e-9) - Math.log(env[i - 1] + 1e-9);
  nov[i] = d > 0 ? d : 0;
}
let mu = 0; for (const v of nov) mu += v; mu /= nF;
for (let i = 0; i < nF; i++) nov[i] = Math.max(0, nov[i] - mu);

const at = (t) => { const t0 = Math.floor(t), f = t - t0; return (nov[t0] || 0) * (1 - f) + (nov[t0 + 1] || 0) * f; };
const comb = (bpm, phase) => {
  const per = (60 / bpm) * FPS;
  let s = 0, n = 0;
  for (let t = phase; t < nF; t += per) { s += at(t); n++; }
  return n ? s / Math.sqrt(n) : 0;    // sqrt(n): does not reward more pulses linearly
};
const bestPhase = (bpm) => {
  const per = (60 / bpm) * FPS;
  let bp = 0, bs = -1;
  for (let p = 0; p < per; p += 0.02) { const s = comb(bpm, p); if (s > bs) { bs = s; bp = p; } }
  return [bp, bs];
};

const rows = [];
for (let bpm = 60; bpm <= 190.001; bpm += 0.1) {
  const [p, s] = bestPhase(bpm);
  rows.push({ bpm, phase: p / FPS, s });
}
// local maxima
const peaks = rows.filter((r, i) => i > 2 && i < rows.length - 3
  && r.s >= rows[i - 1].s && r.s >= rows[i + 1].s && r.s > rows[i - 3].s && r.s > rows[i + 3].s);
peaks.sort((a, b) => b.s - a.s);
console.log(`band ${LO}-${HI} Hz, ${ANA}s of ${file}`);
for (const p of peaks.slice(0, 12)) {
  console.log(`  ${p.bpm.toFixed(2).padStart(6)} BPM   beat ${(60 / p.bpm).toFixed(4)}s   phase ${p.phase.toFixed(3)}s   comb ${p.s.toFixed(4)}`);
}

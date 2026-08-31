// Measure the real beat grid on the KICK band of a music file (no assumed BPM).
//   1. decode mono 22.05 kHz, keep 40-140 Hz (kick fundamental) via a biquad bandpass
//   2. half-wave-rectified spectral-flux-ish envelope at 172 Hz frame rate
//   3. autocorrelation of the novelty curve over 60-180 BPM -> period
//   4. brute-force phase search: the offset that maximises novelty on the pulse train
// Usage: node src/beatgrid.mjs assets/bgm-bs.mp3 [analysis_seconds]
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';

const file = process.argv[2];
const ANA = Number(process.argv[3] || 45);
const SR = 22050;

const raw = execFileSync('ffmpeg', ['-v', 'error', '-i', file, '-t', String(ANA),
  '-ac', '1', '-ar', String(SR), '-af', 'highpass=f=40,lowpass=f=140',
  '-f', 'f32le', '-'], { maxBuffer: 1 << 28 });
const x = new Float32Array(raw.buffer, raw.byteOffset, raw.length / 4);

// envelope
const HOP = 128;                       // 172.3 fps
const FPS_ENV = SR / HOP;
const nF = Math.floor(x.length / HOP);
const env = new Float64Array(nF);
for (let i = 0; i < nF; i++) {
  let e = 0;
  for (let k = 0; k < HOP; k++) e += x[i * HOP + k] * x[i * HOP + k];
  env[i] = Math.sqrt(e / HOP);
}
// novelty = half-wave rectified first difference of log envelope
const nov = new Float64Array(nF);
for (let i = 1; i < nF; i++) {
  const d = Math.log(env[i] + 1e-9) - Math.log(env[i - 1] + 1e-9);
  nov[i] = d > 0 ? d : 0;
}
// normalise
let mu = 0; for (const v of nov) mu += v; mu /= nF;
for (let i = 0; i < nF; i++) nov[i] = Math.max(0, nov[i] - mu);

// autocorrelation over plausible beat periods
const lagFor = (bpm) => (60 / bpm) * FPS_ENV;
let best = { score: -1, bpm: 0 };
for (let bpm = 60; bpm <= 180.01; bpm += 0.05) {
  const lag = lagFor(bpm);
  let s = 0, n = 0;
  for (let i = 0; i + lag < nF; i++) {
    const j = i + lag, j0 = Math.floor(j), f = j - j0;
    const vj = nov[j0] * (1 - f) + (nov[j0 + 1] || 0) * f;
    s += nov[i] * vj; n++;
  }
  const score = s / n;
  if (score > best.score) best = { score, bpm };
}
// disambiguate half/double time by comb-filter strength on the pulse train
const combScore = (bpm, phase) => {
  const per = lagFor(bpm);
  let s = 0, n = 0;
  for (let t = phase; t < nF; t += per) {
    const t0 = Math.floor(t), f = t - t0;
    s += (nov[t0] || 0) * (1 - f) + (nov[t0 + 1] || 0) * f; n++;
  }
  return n ? s / Math.sqrt(n) : 0;
};
const bestPhase = (bpm) => {
  const per = lagFor(bpm);
  let bp = 0, bs = -1;
  for (let p = 0; p < per; p += 0.05) { const s = combScore(bpm, p); if (s > bs) { bs = s; bp = p; } }
  return { phase: bp, score: bs };
};

const cands = [best.bpm / 2, best.bpm, best.bpm * 2].filter((b) => b >= 60 && b <= 200);
let win = null;
for (const b of cands) {
  const { phase, score } = bestPhase(b);
  // penalise half-time (fewer pulses inflates nothing, but prefer 90-150 as the human tap range)
  const pref = (b >= 90 && b <= 150) ? 1.12 : 1.0;
  const s = score * pref;
  console.log(`  cand ${b.toFixed(2)} BPM  phase ${(phase / FPS_ENV).toFixed(3)}s  comb ${score.toFixed(4)}  weighted ${s.toFixed(4)}`);
  if (!win || s > win.s) win = { bpm: b, phase, s };
}

const BPM = win.bpm;
const PHASE = win.phase / FPS_ENV;
const BEAT = 60 / BPM;
console.log(`\nMEASURED  BPM=${BPM.toFixed(2)}  beat=${BEAT.toFixed(4)}s  first downbeat=${PHASE.toFixed(3)}s`);

const grid = [];
for (let t = PHASE, i = 0; t < ANA; t += BEAT, i++) grid.push({ i, t: Number(t.toFixed(4)) });
fs.writeFileSync('work/beatgrid.json', JSON.stringify({ file, bpm: BPM, beat: BEAT, phase: PHASE, grid }, null, 2));
console.log(`work/beatgrid.json  ${grid.length} beats`);
console.log('first 16 beats:', grid.slice(0, 16).map((g) => g.t.toFixed(3)).join(' '));

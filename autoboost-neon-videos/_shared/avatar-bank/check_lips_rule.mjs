// GATE — run this after every build, before assembling.
// Flags any avatar shot whose SOURCE window falls in a still (non-speaking) part of the
// bank clip while the voice track is active. Reads the shot params straight out of
// order.json (written by build_full.mjs) so it can never drift from the actual cut.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';

const FFDIR = '/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static';
const ENV = { ...process.env, PATH: FFDIR + ':' + process.env.PATH };
const P = process.argv[2] || '/work/autoboost-neon-videos/essai-ego-pourquoi-ce-format';
const MAXBAD = Number(process.argv[3] ?? 6);   // frames tolerated per shot (6f = 0.20s)

const { order, marks } = JSON.parse(fs.readFileSync(`${P}/work/order.json`, 'utf8'));
const LM = JSON.parse(fs.readFileSync(JSON.parse(fs.readFileSync(`${P}/work/order.json`,'utf8'))._lipsMap, 'utf8'));  // D wardrobe map, not the A/B/C default

const rms = spawnSync('bash', ['-c',
  `ffmpeg -v error -i "${P}/work/final_audio.wav" -ac 1 -ar 48000 -af "asetnsamples=n=1600,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null - 2>&1 | grep -oE '=-?(inf|[0-9.]+)$' | tr -d '='`],
  { env: ENV, maxBuffer: 1 << 28, encoding: 'utf8' }).stdout.trim().split('\n').map(v => v.includes('inf') ? -99 : Number(v));
const voicedAt = (t) => (rms[Math.round(t * 30)] ?? -99) > -34;

let bad = 0;
console.log('shot  srcWindow        lips-active zone      still&voiced');
for (const id of order) {
  const m = marks[id];
  if (m.kind !== 'avatar') continue;
  const act = LM.clips[m.src].active;
  const inActive = (ts) => act.some(w => ts >= w.start && ts <= w.end);
  let n = 0; const hits = [];
  for (let i = 0; i < m.frames; i++) {
    const tOut = m.start + i / 30;
    const tSrc = m.ss + (i / 30) * m.speed;
    if (!inActive(tSrc) && voicedAt(tOut)) { n++; hits.push(tOut); }
  }
  const srcEnd = m.ss + (m.frames / 30) * m.speed;
  const zone = act.map(w => w.start.toFixed(2) + '-' + w.end.toFixed(2)).join(',');
  const viol = n >= MAXBAD;
  if (viol) bad++;
  console.log(id.padEnd(5) + ' ' + `${m.ss.toFixed(2)}-${srcEnd.toFixed(2)}`.padEnd(14) + '  ' + zone.padEnd(20) +
    String(n).padStart(6) + (viol ? `   <== ${(n / 30).toFixed(2)}s @ ${hits[0].toFixed(2)}-${hits[hits.length - 1].toFixed(2)}` : ''));
}
console.log(bad ? `\nFAIL — ${bad} shot(s) violate the lips-active rule` : '\nPASS — no shot violates the lips-active rule');
process.exit(bad ? 1 : 0);

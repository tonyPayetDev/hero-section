// Prints every caption chunk next to the shot(s) it plays over, so word/image mismatches
// ("UNE SALLE" written over the beach bar) are caught on the table instead of in the render.
// Usage: node src/verify.mjs --tag a
import fs from 'node:fs';

const arg = (k, d) => { const i = process.argv.indexOf(`--${k}`); return i > -1 ? process.argv[i + 1] : d; };
const TAG = arg('tag', 'a');

const cfg = JSON.parse(fs.readFileSync(`src/shots-${TAG}.json`, 'utf8'));
const FPS = cfg.fps || 30;
let acc = 0;
const cuts = cfg.shots.map((s) => {
  const a = acc; acc += Math.round(s.dur * FPS) / FPS;
  return { a, b: acc, id: s.id, note: s.note };
});

const ct = JSON.parse(fs.readFileSync(`work/chunk-times-${TAG}.json`, 'utf8'));
console.log(`=== ${TAG} — ${acc.toFixed(2)}s, ${cfg.shots.length} plans, ${ct.length} chunks`);
for (const c of ct) {
  const over = cuts.filter((x) => x.b > c.start + 0.02 && x.a < c.end - 0.02);
  const flag = over.length > 2 ? ' <-- traverse 3 plans' : '';
  console.log(`${c.start.toFixed(2).padStart(6)}-${c.end.toFixed(2).padStart(6)} ${c.accent} ${(`"${c.text}"`).padEnd(34)} ${over.map((x) => x.note.split(' - ').pop()).join(' | ')}${flag}`);
}

#!/usr/bin/env node
/**
 * layout.mjs <edition.json> <procDir> <out timing.json>
 *
 * Probes the real duration of every processed voice segment and lays them out
 * sequentially with a fixed gap. The whole composition length falls out of the
 * measured audio — that is what makes any script length render correctly.
 */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const [, , EDITION, PROC, OUT] = process.argv;
const FFPROBE = process.env.FFPROBE || 'ffprobe';
const GAP = +(process.env.JIA_GAP || 0.40);
const LEAD = +(process.env.JIA_LEAD || 0.45);
const TAIL = +(process.env.JIA_TAIL || 0.55);

const ed = JSON.parse(fs.readFileSync(EDITION, 'utf8'));
const start = {}, dur = {};
let t = LEAD;
for (const s of ed.segments) {
  const f = path.join(PROC, `${s.id}.wav`);
  if (!fs.existsSync(f)) { console.error(`[layout] segment manquant: ${s.id}`); continue; }
  const d = parseFloat(execFileSync(FFPROBE,
    ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nk=1:nw=1', f]).toString().trim());
  if (!(d > 0)) { console.error(`[layout] durée nulle: ${s.id}`); continue; }
  start[s.id] = +t.toFixed(3);
  dur[s.id] = +d.toFixed(3);
  t += d + GAP;
}
const duration = +(t - GAP + TAIL).toFixed(2);
fs.writeFileSync(OUT, JSON.stringify({ duration, gap: GAP, start, dur }, null, 2));

const warn = duration < 40 || duration > 65 ? '  ⚠ hors cible 45-60s' : '';
console.error(`[layout] durée totale ${duration}s${warn}`);
for (const id of Object.keys(start)) {
  console.error(`   ${id.padEnd(6)} ${String(start[id]).padStart(7)} → ${(start[id] + dur[id]).toFixed(3).padStart(7)}  (${dur[id]}s)`);
}

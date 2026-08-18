#!/usr/bin/env node
// Clôture des entrées TASKLOG : passe `- [ ]` à `- [x]` (ou ~ / !) pour les lignes
// dont le texte contient l'un des motifs donnés. Dry-run par défaut ; --apply pour écrire.
//   node close.mjs "motif1" "motif2" [--state x|~|!] [--apply]
import fs from 'fs';
const FILE = '/work/TASKLOG.md';
const args = process.argv.slice(2);
let state = 'x', apply = false;
const pats = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--apply') apply = true;
  else if (args[i] === '--state') state = args[++i];
  else pats.push(args[i].toLowerCase());
}
if (!pats.length) { console.error('usage: close.mjs "motif" [...] [--state x|~|!] [--apply]'); process.exit(1); }

let md = fs.readFileSync(FILE, 'utf8');
const lines = md.split('\n');
let changed = 0;
const preview = [];
for (let i = 0; i < lines.length; i++) {
  const m = lines[i].match(/^- \[ \]\s+(`\d\d:\d\d`\s+)(.*)$/);
  if (!m) continue;
  const body = m[2].toLowerCase();
  if (pats.some(p => body.includes(p))) {
    preview.push(`  [${state}] ${m[2].replace(/\s*<sub>.*$/, '').slice(0, 70)}`);
    lines[i] = lines[i].replace('- [ ]', `- [${state}]`);
    changed++;
  }
}
console.log(`${changed} entrée(s) ${apply ? 'clôturée(s)' : 'à clôturer (dry-run)'} → [${state}]`);
preview.slice(0, 20).forEach(l => console.log(l));
if (apply && changed) { fs.writeFileSync(FILE, lines.join('\n')); console.log('✅ TASKLOG.md mis à jour'); }
else if (!apply && changed) console.log('(relancer avec --apply pour écrire)');

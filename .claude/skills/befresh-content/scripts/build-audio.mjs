// BeFresh — audio mix: VO + Mixkit bed (side-chain ducked) + whoosh/pop SFX.
// Generalized from befresh-01-decathlon/src/build-audio.mjs (proven on 2 renders).
//
// Reads src/shots.json for the cut grid, so the whooshes always land on real cuts.
// Usage: node scripts/build-audio.mjs [--voice work/voice.mp3] [--bgm assets/bgm.mp3] [--dur auto]
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const arg = (k, d) => {
  const i = process.argv.indexOf(`--${k}`);
  return i > -1 ? process.argv[i + 1] : d;
};

const cfg = JSON.parse(fs.readFileSync('src/shots.json', 'utf8'));
const FPS = cfg.fps || 30;

const VOICE = arg('voice', 'work/voice.mp3');
const BGM = arg('bgm', cfg.bgm || 'assets/bgm.mp3');
const WHOOSH = arg('whoosh', 'assets/sfx-whoosh-mixkit.wav');
const POP = arg('pop', 'assets/sfx-pop-mixkit.wav');
const OUT = arg('out', 'work/audio-mix.m4a');
const WHOOSH_PEAK = 0.35; // the sweep peaks 0.35s in -> land that on the cut

// Video length = sum of shot durations, unless overridden.
const durArg = arg('dur', 'auto');
const DUR = durArg === 'auto'
  ? cfg.shots.reduce((a, s) => a + Math.round(s.dur * FPS) / FPS, 0)
  : Number(durArg);

// Cumulative cut times, derived from the same rounding build-shots.mjs uses.
const cuts = [];
cfg.shots.reduce((acc, s) => {
  cuts.push(acc / FPS);
  return acc + Math.round(s.dur * FPS);
}, 0);

// Whooshes on section-opening cuts. Either listed in shots.json (`sectionStarts`)
// or every 4th cut as a sane default.
const sectionStarts = cfg.sectionStarts
  || cuts.map((_, i) => i).filter((i) => i > 0 && i % 4 === 0);
const WHOOSH_AT = sectionStarts.map((i) => cuts[i]).filter((t) => t != null && t < DUR);

// Pops on the single-word impact captions (written by gen-captions.mjs).
let POP_AT = [];
if (fs.existsSync('work/chunk-times.json')) {
  POP_AT = JSON.parse(fs.readFileSync('work/chunk-times.json', 'utf8'))
    .filter((c) => c.impact).map((c) => c.start).filter((t) => t < DUR);
}

console.log(`[audio] dur ${DUR.toFixed(2)}s  voice ${VOICE}  bgm ${BGM}`);
console.log('[audio] whoosh @', WHOOSH_AT.map((t) => t.toFixed(2)).join(' ') || '(none)');
console.log('[audio] pop    @', POP_AT.map((t) => t.toFixed(2)).join(' ') || '(none)');

const inputs = ['-i', VOICE, '-i', BGM];
const fc = [];

// Voice: light compression + presence, held at full level.
fc.push('[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,'
  + 'highpass=f=85,acompressor=threshold=0.08:ratio=3:attack=8:release=180,volume=1.5,'
  + `apad,atrim=0:${DUR}[vo]`);
fc.push('[vo]asplit=2[voMix][voKey]');

// Music bed: trimmed, faded, pushed well under the voice.
fc.push('[1:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,'
  + `atrim=0:${DUR},asetpts=N/SR/TB,afade=t=in:st=0:d=0.4,`
  + `afade=t=out:st=${(DUR - 1.4).toFixed(3)}:d=1.4,volume=0.30[bed]`);
fc.push('[bed][voKey]sidechaincompress=threshold=0.035:ratio=9:attack=15:release=320:makeup=1[bedDuck]');

let n = 2;
const sfx = [];
for (const t of WHOOSH_AT) {
  const st = Math.max(0, t - WHOOSH_PEAK);
  inputs.push('-i', WHOOSH);
  fc.push(`[${n}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,atrim=0:0.85,asetpts=N/SR/TB,`
    + `afade=t=out:st=0.6:d=0.25,volume=0.30,adelay=${Math.round(st * 1000)}|${Math.round(st * 1000)}[w${n}]`);
  sfx.push(`[w${n}]`); n++;
}
for (const t of POP_AT) {
  inputs.push('-i', POP);
  fc.push(`[${n}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,atrim=0:0.45,asetpts=N/SR/TB,`
    + `volume=0.34,adelay=${Math.round(t * 1000)}|${Math.round(t * 1000)}[p${n}]`);
  sfx.push(`[p${n}]`); n++;
}

fc.push(`[voMix][bedDuck]${sfx.join('')}amix=inputs=${2 + sfx.length}:duration=first:normalize=0,`
  + `atrim=0:${DUR},alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[out]`);

execFileSync('ffmpeg', ['-v', 'error', ...inputs, '-filter_complex', fc.join(';'),
  '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', OUT, '-y'],
{ stdio: ['ignore', 'inherit', 'inherit'] });

const d = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
  '-of', 'csv=p=0', OUT]).toString().trim();
console.log(`[audio] ${OUT} ${d}s`);

// Word-by-word captions, timed off each segment's own voiced envelope
// (so pauses inside a segment stretch the right word instead of drifting).
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';

const FFDIR = '/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static';
const ENV = { ...process.env, PATH: FFDIR + ':' + process.env.PATH };
const W = '/work/autoboost-neon-videos/autoboost-61-dix-questions/work';
const { voice } = JSON.parse(fs.readFileSync(`${W}/order.json`, 'utf8'));

// caption chunks, in order, per segment (1-2 words: TikTok word-by-word cadence)
const TEXT = {
  t01: "Écoute bien. | Tu crois | te connaître. | Tu te racontes | la même histoire | depuis des années.",
  t02: "Tu vas aller | sur Claude. | Et tu vas | le tester | deux fois. | Sur un Claude | VIDE. | Et sur celui | qui a déjà | toutes tes | conversations.",
  t03: "Tu lui demandes ça, | en dix questions. | Que pourrais-tu | me demander | sur moi-même | pour révéler | quelque chose | que moi-même | j'ignore ?",
  t04: "Et tu précises. | UNE PAR UNE. | Pas toutes | à la fois.",
  t05: "C'est ce détail | qui change tout.",
  t06: "Le Claude vide | te pose des questions | intelligentes. | Et froides.",
  t07: "Celui qui te connaît | te pose la question | que tu évites | depuis six mois.",
  t08: "Tu vas être choqué. | Tu vas être bluffé | par les questions. | Tu vas découvrir | comment tu es.",
  t09: "C'est indéniable. | Irréfutable. | Commente MIROIR, | je t'envoie | les dix questions.",
};

const HZ = 100, NS = 480;           // 100 envelope samples per second
const envelope = (f) => {
  const raw = spawnSync('bash', ['-c',
    `ffmpeg -v error -i "${f}" -ac 1 -ar 48000 -af "asetnsamples=n=${NS},astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null - 2>&1 | grep '^lavfi.astats.Overall.RMS_level='`],
    { env: ENV, maxBuffer: 1 << 28, encoding: 'utf8' }).stdout.trim().split('\n');
  return raw.map(l => { const v = l.split('=')[1]; return (v === '-inf' || v === undefined) ? -99 : Number(v); });
};

const tc = (t) => {
  if (t < 0) t = 0;
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), s = t % 60;
  return `${h}:${String(m).padStart(2, '0')}:${s.toFixed(2).padStart(5, '0')}`;
};

const esc = (s) => s.replace(/\{/g, '(').replace(/\}/g, ')');
const lines = [];

for (const [id, start] of Object.entries(voice)) {
  const f = `${W}/tts/proc/${id}.wav`;
  const env = envelope(f);
  const voiced = env.map(v => v > -42);
  const V = voiced.reduce((a, b) => a + (b ? 1 : 0), 0);
  const chunks = TEXT[id].split('|').map(s => s.trim()).filter(Boolean);
  const weights = chunks.map(c => c.replace(/\s/g, '').length + 2);
  const wsum = weights.reduce((a, b) => a + b, 0);

  let i = 0, carry = 0;
  chunks.forEach((c, k) => {
    const want = (weights[k] / wsum) * V;
    const a = i / HZ;
    let used = 0;
    while (i < env.length && used + carry < want) { if (voiced[i]) used++; i++; }
    carry = (used + carry) - want;
    // let the last chunk hang on a touch past the end of speech
    const b = (k === chunks.length - 1) ? (env.length / HZ) + 0.18 : i / HZ;
    lines.push({ a: start + a, b: start + Math.max(b, a + 0.20), t: esc(c) });
  });
}

lines.sort((x, y) => x.a - y.a);
// no caption may run into the next one
for (let k = 0; k < lines.length - 1; k++) if (lines[k].b > lines[k + 1].a) lines[k].b = lines[k + 1].a;

const head = `[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Outfit,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,5.0,0,2,70,70,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;
fs.writeFileSync(`${W}/captions.ass`,
  head + lines.map(l => `Dialogue: 0,${tc(l.a)},${tc(l.b)},Cap,,0,0,0,,${l.t}`).join('\n') + '\n');
console.log(`${lines.length} caption lines  (last ends ${lines[lines.length - 1].b.toFixed(2)}s)`);

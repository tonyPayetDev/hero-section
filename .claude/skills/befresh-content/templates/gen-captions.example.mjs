// Build the word-by-word ASS caption track for the BeFresh reel.
// One Dialogue event per word: the whole chunk stays on screen, the active word
// switches to the accent colour. Instagram-safe: captions sit >=330px off the bottom.
//
// BRAND (from the official BeFresh lookbook, assets.automatisationboost.com/Image Resto/befresh.png):
//   black ground + GOLD #E0AE3A accent + MAGENTA #E9268C section accent, white body text.
//   (v1 used green/orange — that was NOT the BeFresh charte.)
import fs from 'node:fs';

const VIDEO_END = 24.0;

// Whisper segment timings (work/whisper-v2.json -> text_details), last segment split in two.
const SEGS = [
  { t0: 0.20,  t1: 5.10,  w: ['ON', 'ÉTAIT', 'À', 'DECATHLON', 'CE', 'WEEK-END', 'ET', 'FRANCHEMENT', "C'ÉTAIT", 'CHAUD !'] },
  { t0: 5.10,  t1: 11.00, w: ['COCKTAILS', 'DE', 'FRUITS', 'FRAIS', 'MOJITO', 'MATCHA', 'ET', 'BIEN', 'SÛR', 'ALOUDA !'] },
  { t0: 11.00, t1: 14.16, w: ['LE', 'FOOD', 'TRUCK', 'BEFRESH', 'A', 'SERVI', 'NON-STOP'] },
  { t0: 14.80, t1: 19.20, w: ['MERCI', 'À', 'TOUS', 'CEUX', 'QUI', 'SONT', 'PASSÉS', 'VOUS', 'ÉTIEZ', 'INCROYABLES'] },
  { t0: 19.20, t1: 20.80, w: ['ON', 'REMET', 'ÇA', 'TRÈS', 'BIENTÔT'] },
  { t0: 21.00, t1: 23.22, w: ['SUIS-NOUS', 'POUR', 'SAVOIR', 'OÙ', 'ON', "S'INSTALLE !"] },
];

// [segIdx, firstWord, lastWord, fontSize, accent]  accent: 'g'=gold  'm'=magenta
const CHUNKS = [
  [0, 0, 2, 96, 'g'], [0, 3, 3, 126, 'm'], [0, 4, 5, 98, 'g'], [0, 6, 7, 92, 'g'], [0, 8, 9, 106, 'm'],
  [1, 0, 3, 88, 'g'], [1, 4, 4, 126, 'g'], [1, 5, 5, 126, 'g'], [1, 6, 8, 96, 'g'], [1, 9, 9, 134, 'm'],
  [2, 0, 2, 98, 'g'], [2, 3, 3, 130, 'm'], [2, 4, 6, 94, 'g'],
  [3, 0, 3, 90, 'g'], [3, 4, 6, 96, 'g'], [3, 7, 8, 100, 'g'], [3, 9, 9, 104, 'm'],
  [4, 0, 2, 102, 'g'], [4, 3, 4, 112, 'm'],
  [5, 0, 2, 88, 'g'], [5, 3, 5, 98, 'm'],
];

const GOLD = '&H003AAEE0&';     // #E0AE3A  BeFresh gold
const MAGENTA = '&H008C26E9&';  // #E9268C  BeFresh magenta
const WHITE = '&H00FFFFFF&';
const BLACK = '&H00000000&';

// Distribute word timings inside each segment, weighted by word length.
for (const s of SEGS) {
  const wts = s.w.map((x) => x.trim().length + 1);
  const tot = wts.reduce((a, b) => a + b, 0);
  let t = s.t0;
  s.times = wts.map((wt) => {
    const d = ((s.t1 - s.t0) * wt) / tot;
    const r = [t, t + d];
    t += d;
    return r;
  });
}

const ts = (x) => {
  const cs = Math.round(x * 100);
  const h = Math.floor(cs / 360000), m = Math.floor((cs % 360000) / 6000);
  const sec = Math.floor((cs % 6000) / 100), c = cs % 100;
  return `${h}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}.${String(c).padStart(2, '0')}`;
};

const ev = [];

// --- brand pill (top, clear of the ~120px Instagram header zone) ---
ev.push(`Dialogue: 0,${ts(0)},${ts(VIDEO_END)},Brand,,0,0,0,,  BE FRESH  ×  DECATHLON  `);

// --- word-by-word captions ---
CHUNKS.forEach(([si, a, b, fs_, acc], ci) => {
  const seg = SEGS[si];
  const accent = acc === 'm' ? MAGENTA : GOLD;
  const isLast = ci === CHUNKS.length - 1;
  for (let k = a; k <= b; k++) {
    const [ws, we] = seg.times[k];
    const end = isLast && k === b ? Math.min(VIDEO_END, we + 0.75) : we;
    const line = seg.w.slice(a, b + 1)
      .map((word, j) => (a + j === k ? `{\\c${accent}}${word}{\\c${WHITE}}` : word))
      .join(' ');
    const pop = `{\\fs${fs_}\\fscx100\\fscy100\\t(0,70,\\fscx105\\fscy105)\\t(70,150,\\fscx100\\fscy100)}`;
    ev.push(`Dialogue: 0,${ts(ws)},${ts(end)},Cap,,0,0,0,,${pop}${line}`);
  }
});

// --- brand signature on the CTA (gold chip, sits above the captions) ---
ev.push(`Dialogue: 0,${ts(20.9)},${ts(VIDEO_END)},Handle,,0,0,0,,{\\fad(200,0)}  @befresh.events  `);

const ass = `[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Outfit,96,${WHITE},${WHITE},${BLACK},&H96000000&,1,0,0,0,100,100,1,0,1,7,5,2,110,110,330,1
Style: Brand,Outfit,46,${WHITE},${WHITE},${GOLD},&HC0000000&,1,0,0,0,100,100,3,0,3,8,0,8,60,60,150,1
Style: Handle,Outfit,52,&H00101010&,&H00101010&,${GOLD},&H00000000&,1,0,0,0,100,100,2,0,3,10,0,2,60,60,660,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
${ev.join('\n')}
`;

fs.mkdirSync('work', { recursive: true });
fs.writeFileSync('work/captions.ass', ass);

// Chunk start times, so the audio pass can drop a "pop" on the impact words.
const chunkTimes = CHUNKS.map(([si, a, b, fs_, acc]) => ({
  text: SEGS[si].w.slice(a, b + 1).join(' '),
  start: SEGS[si].times[a][0],
  end: SEGS[si].times[b][1],
  impact: a === b,
  accent: acc,
}));
fs.writeFileSync('work/chunk-times.json', JSON.stringify(chunkTimes, null, 2));
console.log(`captions.ass written: ${ev.length} events, ${CHUNKS.length} chunks`);
console.log('impact words:', chunkTimes.filter((c) => c.impact).map((c) => `${c.text}@${c.start.toFixed(2)}`).join(', '));

// BeFresh — female preset-voice TTS via WaveSpeed qwen3-tts/text-to-speech (NOT the clone endpoint).
// Usage: node src/tts.mjs <voice> <outfile> [textfile]
import fs from 'node:fs';

const WS = process.env.WAVESPEED_KEY || 'wsk_live_qlVmihxhRYi56t7wZ6sNA6kAlLrMfsv7ygbvAEzvTMY';
const BASE = 'https://api.wavespeed.ai/api/v3';
const MODEL = 'wavespeed-ai/qwen3-tts/text-to-speech';

const voice = process.argv[2] || 'Vivian';
const out = process.argv[3] || 'work/voice.mp3';
const textFile = process.argv[4] || 'narration.txt';
const text = fs.readFileSync(textFile, 'utf8').replace(/\s+/g, ' ').trim();

console.log(`[tts] voice=${voice} chars=${text.length}`);

const r = await fetch(`${BASE}/${MODEL}`, {
  method: 'POST',
  headers: { Authorization: `Bearer ${WS}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ text, language: 'French', voice }),
});
const j = await r.json();
const id = j.data?.id;
if (!id) { console.error('submit failed:', JSON.stringify(j)); process.exit(1); }
console.log('[tts] job', id);

for (let i = 0; i < 90; i++) {
  await new Promise((s) => setTimeout(s, 3000));
  const jj = await (await fetch(`${BASE}/predictions/${id}/result`, { headers: { Authorization: `Bearer ${WS}` } })).json();
  const st = jj.data?.status;
  if (st === 'completed') {
    const url = jj.data.outputs[0];
    fs.writeFileSync(out.replace(/\.\w+$/, '') + '-url.txt', url);
    const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
    fs.mkdirSync(out.replace(/\/[^/]+$/, ''), { recursive: true });
    fs.writeFileSync(out, buf);
    console.log(`[tts] DONE ${out} ${buf.length}b`);
    console.log(`[tts] url ${url}`);
    process.exit(0);
  }
  if (st === 'failed') { console.error('FAILED', JSON.stringify(jj.data)); process.exit(1); }
}
console.error('timeout'); process.exit(1);

// Word-level timestamps via WaveSpeed openai-whisper.
// Usage: node src/whisper.mjs <audio-url> <out.json>
import fs from 'node:fs';

const WS = process.env.WAVESPEED_KEY || 'wsk_live_qlVmihxhRYi56t7wZ6sNA6kAlLrMfsv7ygbvAEzvTMY';
const BASE = 'https://api.wavespeed.ai/api/v3';

const audio = process.argv[2];
const out = process.argv[3] || 'work/whisper.json';

const r = await fetch(`${BASE}/wavespeed-ai/openai-whisper`, {
  method: 'POST',
  headers: { Authorization: `Bearer ${WS}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ audio, language: 'fr', enable_timestamps: true }),
});
const j = await r.json();
const id = j.data?.id;
if (!id) { console.error('submit failed:', JSON.stringify(j)); process.exit(1); }
console.log('[whisper] job', id);

for (let i = 0; i < 90; i++) {
  await new Promise((s) => setTimeout(s, 3000));
  const jj = await (await fetch(`${BASE}/predictions/${id}/result`, { headers: { Authorization: `Bearer ${WS}` } })).json();
  const st = jj.data?.status;
  if (st === 'completed') {
    fs.writeFileSync(out, JSON.stringify(jj.data, null, 2));
    console.log('[whisper] DONE', out);
    process.exit(0);
  }
  if (st === 'failed') { console.error('FAILED', JSON.stringify(jj.data)); process.exit(1); }
}
console.error('timeout'); process.exit(1);

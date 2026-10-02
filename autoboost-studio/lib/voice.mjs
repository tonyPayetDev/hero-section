// Voice: enhance the real voice locally, or re-voice every sentence with a cloned voice
// (WaveSpeed qwen3-tts/voice-clone, or the n8n tts-gen webhook) and re-cut the picture to it.
import fs from "node:fs";
import path from "node:path";
import { ff, run, FFMPEG, duration, FPS, sleep } from "./tools.mjs";
import { transcribe } from "./transcribe.mjs";

/** local polish: rumble out, denoise, de-ess, gentle compression, presence, then ONE two-pass loudnorm */
export async function enhance(inWav, outWav) {
  const pre = "highpass=f=80,afftdn=nr=10:nf=-40,deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,"
    + "equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=180:t=q:w=1:g=-1.5";
  // the measure pass must print at info level (ff() runs with -v error)
  const { stderr } = await run(FFMPEG, ["-nostdin", "-hide_banner", "-i", inWav, "-af", pre + ",loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], { ok: true });
  const m = JSON.parse(stderr.slice(stderr.lastIndexOf("{"), stderr.lastIndexOf("}") + 1));
  const ln = `loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}:linear=true`;
  await ff(["-i", inWav, "-af", `${pre},${ln},aresample=48000`, "-ar", "48000", "-ac", "1", outWav]);
  return outWav;
}

/** split the transcript into sentences (punctuation or a pause) */
export function sentences(words, pause = 0.7) {
  const out = [];
  let cur = [];
  words.forEach((w, i) => {
    cur.push(w);
    const next = words[i + 1];
    if (/[.?!…]$/.test(w.w) || !next || next.s - w.e > pause) { out.push(cur); cur = []; }
  });
  return out.filter((s) => s.length);
}

async function ttsWaveSpeed(text, { key, refUrl, refText }) {
  const BASE = "https://api.wavespeed.ai/api/v3";
  const r = await fetch(`${BASE}/wavespeed-ai/qwen3-tts/voice-clone`, {
    method: "POST", headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ text, audio: refUrl, language: "French", ...(refText ? { reference_text: refText } : {}) }),
  });
  const j = await r.json();
  const id = j.data?.id;
  if (!id) throw new Error("WaveSpeed: " + JSON.stringify(j).slice(0, 300));
  for (let i = 0; i < 120; i++) {
    await sleep(2000);
    const jj = await (await fetch(`${BASE}/predictions/${id}/result`, { headers: { Authorization: `Bearer ${key}` } })).json();
    const st = jj.data?.status;
    if (st === "completed") return Buffer.from(await (await fetch(jj.data.outputs[0])).arrayBuffer());
    if (["failed", "cancelled", "timeout", "deleted"].includes(st)) throw new Error("WaveSpeed " + st + ": " + JSON.stringify(jj.data?.error || ""));
  }
  throw new Error("WaveSpeed: timeout");
}

async function ttsWebhook(text, { webhook, refUrl }) {
  // the n8n webhook injects the text raw into JSON: no straight double quotes
  const r = await fetch(webhook, { method: "POST", headers: { "content-type": "application/json", "user-agent": "curl/8.5.0" },
    body: JSON.stringify({ text: text.replace(/"/g, ""), voixUrl: refUrl }) });
  if (!r.ok) throw new Error(`webhook ${r.status}`);
  const buf = Buffer.from(await r.arrayBuffer());
  if (buf.length < 1024) throw new Error("webhook: réponse vide");
  return buf;
}

/**
 * re-voice: each sentence of the take in the cloned voice, laid end to end (0.25 s apart);
 * the picture is rebuilt from the take - talking passages under speech, silent ones under pauses,
 * so the mouth only moves while words are heard. -> { cam, voice, words, total, cuts }
 */
export async function revoice(src, words, work, opts, log = () => {}) {
  const dir = path.join(work, "revoice");
  fs.mkdirSync(dir, { recursive: true });
  const sents = sentences(words);
  const clips = [];
  for (let i = 0; i < sents.length; i++) {
    const text = sents[i].map((w) => w.w).join(" ");
    let buf;
    for (let a = 1; a <= 3 && !buf; a++) {
      try { buf = opts.mode === "webhook" ? await ttsWebhook(text, opts) : await ttsWaveSpeed(text, opts); }
      catch (e) { log(`voix ${i + 1}: essai ${a}/3 - ${e.message}`); await sleep(3000 * a); }
    }
    if (!buf) throw new Error(`voix clonée: échec sur « ${text} »`);
    const raw = path.join(dir, `s${i}.audio`), wav = path.join(dir, `s${i}.wav`);
    fs.writeFileSync(raw, buf);
    await ff(["-i", raw, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
      "-ar", "48000", "-ac", "1", wav]);
    clips.push({ wav, d: await duration(wav) });
    log(`voix clonée ${i + 1}/${sents.length}`);
  }
  // timeline of the new voice
  const GAP = 0.25;
  let t = 0.15;
  const spans = clips.map((c) => { const s = { a: t, b: t + c.d }; t += c.d + GAP; return s; });
  const total = +(t - GAP + 0.3).toFixed(3);
  const NF = Math.round(total * FPS);
  const inputs = clips.flatMap((c) => ["-i", c.wav]);
  const flt = clips.map((c, k) => `[${k}:a]adelay=${Math.round(spans[k].a * 1000)}[d${k}]`).join(";") + ";"
    + clips.map((_, k) => `[d${k}]`).join("") + `amix=inputs=${clips.length}:normalize=0:duration=longest,apad=whole_dur=${total}[v]`;
  const voice = path.join(dir, "voice_raw.wav");
  await ff([...inputs, "-filter_complex", flt, "-map", "[v]", "-t", String(total), "-ar", "48000", "-ac", "1", voice]);

  // picture: talk / silence pools from the original take
  const srcDur = await duration(src);
  const talk = [], sil = [];
  for (const w of words) {
    const last = talk[talk.length - 1];
    if (last && w.s - last[1] < 0.3) last[1] = w.e; else talk.push([w.s, w.e]);
  }
  let cur = 0;
  for (const [a, b] of talk) { if (a - cur >= 0.5) sil.push([cur + 0.12, a - 0.12]); cur = b; }
  if (srcDur - cur >= 0.5) sil.push([cur + 0.12, srcDur - 0.05]);
  const pools = { talk: talk.filter(([a, b]) => b - a > 0.4).map(([a, b]) => [Math.round(a * FPS) + 2, Math.round(b * FPS) - 2]),
    sil: sil.map(([a, b]) => [Math.round(a * FPS), Math.round(b * FPS)]) };
  if (!pools.sil.length) pools.sil = pools.talk;
  const ptr = { talk: [0, null], sil: [0, null] };
  const segs = [];
  let f = 0;
  // frames [0, a0) silence, [a0, b0) talk, [b0, a1) silence ...
  const marks = [[0, "sil"], ...spans.flatMap((s) => [[Math.round(s.a * FPS), "talk"], [Math.round(s.b * FPS), "sil"]]), [NF, "end"]];
  const cuts = [];
  for (let m = 0; m < marks.length - 1; m++) {
    const [fa, kind] = marks[m];
    let need = marks[m + 1][0] - fa;
    while (need > 0) {
      const [i, pos0] = ptr[kind];
      const run = pools[kind][i % pools[kind].length];
      const pos = pos0 ?? run[0];
      const n = Math.min(need, run[1] - pos);
      if (n <= 0) { ptr[kind] = [i + 1, null]; continue; }
      cuts.push(+(f / FPS).toFixed(3));
      segs.push([pos, n]);
      f += n; need -= n;
      ptr[kind] = pos + n < run[1] ? [i, pos + n] : [i + 1, null];
    }
  }
  const files = [];
  for (let k = 0; k < segs.length; k++) {
    const out = path.join(dir, `v${String(k).padStart(3, "0")}.mp4`);
    await ff(["-ss", (segs[k][0] / FPS).toFixed(4), "-i", src, "-an", "-vf", `fps=${FPS}`, "-frames:v", String(segs[k][1]),
      "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-video_track_timescale", "30000", out]);
    files.push(out);
  }
  const list = path.join(dir, "list.txt");
  fs.writeFileSync(list, files.map((x) => `file '${path.resolve(x).replace(/\\/g, "/")}'`).join("\n"));
  const cam = path.join(dir, "cam.mp4");
  await ff(["-f", "concat", "-safe", "0", "-i", list, "-c:v", "libx264", "-crf", "18", "-g", String(FPS), "-keyint_min", String(FPS),
    "-pix_fmt", "yuv420p", "-frames:v", String(NF), "-movflags", "+faststart", cam]);
  log("transcription de la nouvelle voix…");
  const nw = await transcribe(voice, dir, { log });
  return { cam, voice, words: nw, total, cuts };
}

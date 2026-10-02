// Word-level transcription, fully local: `hyperframes transcribe` (whisper.cpp).
import fs from "node:fs";
import path from "node:path";
import { HF, ff, run } from "./tools.mjs";

/** -> [{w, s, e}] ; model "small" (multilingual) by default - never a ".en" model for French */
export async function transcribe(media, workDir, { model = "small", language = "fr", log = () => {} } = {}) {
  const dir = path.join(workDir, "asr-" + path.basename(media).replace(/\W+/g, "_"));
  fs.mkdirSync(dir, { recursive: true });
  const wav = path.join(dir, "a.wav");
  await ff(["-i", media, "-vn", "-ac", "1", "-ar", "16000", wav]);
  log(`transcription (whisper ${model}, ${language})…`);
  const { stdout } = await run(HF, ["transcribe", wav, "--model", model, "--language", language, "-d", dir, "--json"],
    { onData: () => {} });
  const res = JSON.parse(stdout.trim().split("\n").filter((l) => l.startsWith("{")).pop() || "{}");
  const tp = res.transcriptPath || path.join(dir, "transcript.json");
  const raw = JSON.parse(fs.readFileSync(tp, "utf8"));
  const arr = Array.isArray(raw) ? raw : raw.words || raw.segments?.flatMap((s) => s.words) || [];
  const words = arr.map((x) => ({ w: String(x.text ?? x.word ?? x.w).trim(), s: +(x.start ?? x.s), e: +(x.end ?? x.e) }))
    .filter((x) => x.w);
  // whisper splits "sous-titres", "l'IA": glue fragments that start with - or '
  const out = [];
  for (const x of words) {
    if (out.length && /^['’\-]/.test(x.w)) { out[out.length - 1].w += x.w; out[out.length - 1].e = x.e; }
    else out.push({ ...x });
  }
  return out;
}

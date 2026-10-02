// Word-level transcription, fully local: `hyperframes transcribe` (whisper.cpp).
import fs from "node:fs";
import path from "node:path";
import { HF, ff, run, duration } from "./tools.mjs";

/** -> [{w, s, e}] ; model "small" (multilingual) by default - never a ".en" model for French */
export async function transcribe(media, workDir, { model = "small", language = "fr", log = () => {} } = {}) {
  const dir = path.join(workDir, "asr-" + path.basename(media).replace(/\W+/g, "_"));
  fs.mkdirSync(dir, { recursive: true });
  const wav = path.join(dir, "a.wav");
  const cached = path.join(dir, "transcript.json");
  if (fs.existsSync(cached) && fs.statSync(cached).mtimeMs > fs.statSync(media).mtimeMs) {
    log("transcription déjà faite pour cette vidéo : réutilisée");
    return glue(JSON.parse(fs.readFileSync(cached, "utf8")));
  }
  await ff(["-i", media, "-vn", "-ac", "1", "-ar", "16000", wav]);
  log(`transcription (whisper ${model}, ${language})…`);
  // whisper.cpp on a busy or slow CPU can take minutes per minute of audio: give it room (60x real time, 10 min floor)
  const secs = await duration(wav);
  const timeout = String(Math.max(600000, Math.round(secs * 60000)));
  const res0 = await run(HF, ["transcribe", wav, "--model", model, "--language", language, "-d", dir, "--json", "--timeout", timeout],
    { ok: true });
  if (res0.code !== 0) throw new Error("transcription échouée : " + (res0.stdout + res0.stderr).trim().slice(-800));
  const stdout = res0.stdout;
  const res = JSON.parse(stdout.trim().split("\n").filter((l) => l.startsWith("{")).pop() || "{}");
  const tp = res.transcriptPath || path.join(dir, "transcript.json");
  if (tp !== cached) fs.copyFileSync(tp, cached);
  return glue(JSON.parse(fs.readFileSync(tp, "utf8")));
}

function glue(raw) {
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

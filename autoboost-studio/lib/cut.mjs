// Silence cutting + tempo, frame-exact, words remapped (port of face-cam-boost facecam_cut.py).
import fs from "node:fs";
import path from "node:path";
import { ff, duration, FPS } from "./tools.mjs";

/** words [{w,s,e}] -> phrases (cut on every silence > gap) */
export function phrases(words, gap = 0.55) {
  const out = [];
  for (const w of words) {
    const cur = out[out.length - 1];
    if (cur && w.s - cur[cur.length - 1].e <= gap) cur.push(w); else out.push([w]);
  }
  return out;
}

/**
 * cut the take: one encode per phrase (setpts / atempo), concat, re-measure, remap.
 * -> { cam: muted mp4 (keyframe each second), voice: wav, words: [{w,s,e}] on the new timeline, total, cuts: [t] }
 */
export async function cutTake(src, words, work, { tempo = 1.1, gap = 0.55, padIn = 0.1, padOut = 0.14, keepSilences = false, log = () => {} } = {}) {
  const dir = path.join(work, "cut");
  fs.mkdirSync(dir, { recursive: true });
  const srcDur = await duration(src);
  const ph = keepSilences ? [words] : phrases(words, gap);
  const files = [];
  const plan = [];
  for (let i = 0; i < ph.length; i++) {
    const p = ph[i];
    const a = keepSilences ? 0 : Math.max(0, p[0].s - padIn);
    const b = keepSilences ? srcDur : Math.min(srcDur, p[p.length - 1].e + padOut);
    const f = path.join(dir, `c${String(i).padStart(3, "0")}.mp4`);
    await ff(["-ss", a.toFixed(3), "-to", b.toFixed(3), "-i", src, "-vf", `setpts=PTS/${tempo},fps=${FPS}`,
      "-af", `atempo=${tempo},aresample=48000`, "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p",
      "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1", "-video_track_timescale", "30000", f]);
    files.push(f);
    plan.push({ a, b, words: p });
    log(`coupe ${i + 1}/${ph.length}`);
  }
  const list = path.join(dir, "list.txt");
  fs.writeFileSync(list, files.map((f) => `file '${path.resolve(f).replace(/\\/g, "/")}'`).join("\n"));
  const base = path.join(dir, "base.mp4");
  await ff(["-f", "concat", "-safe", "0", "-i", list, "-c", "copy", base]);
  // every cut rounds to whole frames: re-measure and remap so captions never drift
  let t = 0;
  const out = [], cuts = [];
  for (let i = 0; i < plan.length; i++) {
    const d = await duration(files[i]);
    const k = d / ((plan[i].b - plan[i].a) / tempo);
    for (const w of plan[i].words) out.push({ w: w.w, s: +(t + (w.s - plan[i].a) / tempo * k).toFixed(3), e: +(t + (w.e - plan[i].a) / tempo * k).toFixed(3) });
    cuts.push(+t.toFixed(3));
    t += d;
  }
  const cam = path.join(dir, "cam.mp4"), voice = path.join(dir, "voice_raw.wav");
  await ff(["-i", base, "-an", "-c:v", "libx264", "-crf", "18", "-g", String(FPS), "-keyint_min", String(FPS), "-pix_fmt", "yuv420p",
    "-movflags", "+faststart", cam]);
  await ff(["-i", base, "-vn", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", voice]);
  return { cam, voice, words: out, total: +t.toFixed(3), cuts };
}

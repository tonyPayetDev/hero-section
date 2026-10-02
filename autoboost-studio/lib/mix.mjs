// Final mix: voice (already normalised in its own pass) + music bed at a fixed level, ducked under
// the voice, + SFX on the motion events. Never normalise the sum (charter); amix normalize=0.
import fs from "node:fs";
import path from "node:path";
import { ASSETS, ROOT, ff, duration } from "./tools.mjs";

const MUSIC = JSON.parse(fs.readFileSync(path.join(ROOT, "templates", "music.json"), "utf8"));

/** voice wav -> -16 LUFS, padded to T (separate pass: loudnorm inside a sidechain graph ends early) */
async function normVoice(voice, T, out) {
  await ff(["-i", voice, "-af", `aformat=sample_fmts=fltp:channel_layouts=mono,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad,atrim=0:${T.toFixed(3)}`,
    "-ar", "48000", out]);
  return out;
}

/** the bed, T seconds long: from `start`, looping [loopA, loopB] with crossfades if the video is longer */
async function bed(music, customFile, T, work) {
  const out = path.join(work, "bed.wav");
  if (customFile) {
    // unknown track: measure it and sit it ~14 LU under the voice
    const { stderr } = await ff(["-i", customFile, "-af", "ebur128", "-f", "null", "-"], { ok: true });
    const I = parseFloat((stderr.match(/I:\s+(-?[\d.]+) LUFS/g) || ["I: -14 LUFS"]).pop().match(/-?[\d.]+/)[0]);
    await ff(["-stream_loop", "-1", "-t", T.toFixed(3), "-i", customFile, "-af", `volume=${(-30 - I).toFixed(1)}dB,afade=t=out:st=${(T - 1).toFixed(2)}:d=1`,
      "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", out]);
    return out;
  }
  const m = MUSIC[music];
  if (!m || !m.file) return null;
  const file = path.join(ASSETS, "music", m.file);
  const fileDur = await duration(file);
  const parts = [];
  let need = T, pos = m.start;
  while (need > 0.01) {
    const end = need + pos <= Math.min(m.loopB, fileDur) ? pos + need : Math.min(m.loopB, fileDur);
    parts.push([pos, end]);
    need -= end - pos;
    pos = m.loopA;
  }
  const inputs = parts.flatMap(([a, b]) => ["-ss", a.toFixed(3), "-t", (b - a + (parts.length > 1 ? 0.25 : 0)).toFixed(3), "-i", file]);
  let flt = "";
  if (parts.length === 1) flt = "[0:a]anull[x]";
  else {
    flt = "[0:a][1:a]acrossfade=d=0.25:c1=tri:c2=tri[x1]";
    for (let k = 2; k < parts.length; k++) flt += `;[x${k - 1}][${k}:a]acrossfade=d=0.25:c1=tri:c2=tri[x${k}]`;
    flt += `;[x${parts.length - 1}]anull[x]`;
  }
  flt += `;[x]atrim=0:${T.toFixed(3)},volume=${m.gain}dB,afade=t=in:d=0.04,afade=t=out:st=${(T - 0.8).toFixed(2)}:d=0.8[b]`;
  await ff([...inputs, "-filter_complex", flt, "-map", "[b]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", out]);
  return out;
}

export async function mix({ voice, events, total, music = "deep-urban", customMusic = null, work, out }) {
  const T = total;
  const vn = await normVoice(voice, T, path.join(work, "voice_norm.wav"));
  // SFX
  const sfx = path.join(work, "sfx.wav");
  const evs = events.filter((e) => fs.existsSync(path.join(ASSETS, "sfx", e[1])));
  if (evs.length) {
    const ins = evs.flatMap((e) => ["-i", path.join(ASSETS, "sfx", e[1])]);
    const parts = evs.map((e, k) => `[${k}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,volume=${e[2]}dB,adelay=${Math.round(e[0] * 1000)}[s${k}]`);
    await ff([...ins, "-filter_complex", parts.join(";") + ";" + evs.map((_, k) => `[s${k}]`).join("") + `amix=inputs=${evs.length}:normalize=0,apad,atrim=0:${T.toFixed(3)}[a]`,
      "-map", "[a]", "-ar", "48000", "-ac", "1", sfx]);
  } else {
    await ff(["-f", "lavfi", "-t", T.toFixed(3), "-i", "anullsrc=r=48000:cl=mono", sfx]);
  }
  const b = await bed(music, customMusic, T, work);
  const args = ["-i", vn, "-i", sfx];
  let flt = "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,asplit=2[v][key];";
  if (b) {
    args.push("-i", b);
    flt += "[2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono[bd];[bd][key]sidechaincompress=threshold=0.035:ratio=6:attack=12:release=320[duck];"
      + "[v][duck][1:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[a]";
  } else {
    flt += "[key]anullsink;[v][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]";
  }
  await ff([...args, "-filter_complex", flt, "-map", "[a]", "-ar", "48000", "-ac", "2", out]);
  return out;
}

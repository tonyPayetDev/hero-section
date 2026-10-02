// Competitor video, no LLM: measure its editing rhythm (shot changes) and copy the pacing.
import { ff, duration } from "./tools.mjs";

/** -> { duration, shots, medianShot, cutsPerMin } from ffmpeg scene detection */
export async function rhythm(file) {
  const d = await duration(file);
  const { stderr } = await ff(["-i", file, "-an", "-vf", "scale=320:-2,select='gt(scene,0.32)',showinfo", "-f", "null", "-"], { ok: true });
  const times = [...stderr.matchAll(/pts_time:([\d.]+)/g)].map((m) => +m[1]);
  const pts = [0, ...times.filter((t) => t > 0.2), d];
  const shots = pts.slice(1).map((t, i) => t - pts[i]).filter((x) => x > 0.15).sort((a, b) => a - b);
  const median = shots.length ? shots[Math.floor(shots.length / 2)] : 3;
  return { duration: +d.toFixed(2), shots: shots.length, medianShot: +median.toFixed(2), cutsPerMin: +(times.length / (d / 60)).toFixed(1) };
}

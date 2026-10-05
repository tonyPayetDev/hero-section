// Scenes -> HyperFrames composition, in the chosen style. Each style is a folder styles/<id>/ with
// style.json (name, formats, cutout support, default music), composition.html and compose.mjs.
// The scenes (what to show and when) come from lib/plan.mjs and are the same for every style.
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { ROOT } from "./tools.mjs";

export const STYLES_DIR = path.join(ROOT, "styles");
export const DEFAULT_STYLE = "boost-niveau";
const MUSIC = JSON.parse(fs.readFileSync(path.join(ROOT, "templates", "music.json"), "utf8"));

/** [{ id, name, description, formats, cutout, music }] sorted with the default first */
export function listStyles() {
  return fs.readdirSync(STYLES_DIR)
    .filter((d) => fs.existsSync(path.join(STYLES_DIR, d, "style.json")) && fs.existsSync(path.join(STYLES_DIR, d, "compose.mjs")))
    .map((id) => ({ id, ...JSON.parse(fs.readFileSync(path.join(STYLES_DIR, id, "style.json"), "utf8")) }))
    .sort((a, b) => (a.id === DEFAULT_STYLE ? -1 : b.id === DEFAULT_STYLE ? 1 : a.name.localeCompare(b.name)));
}

export function getStyle(id) {
  const all = listStyles();
  return all.find((s) => s.id === id) || all.find((s) => s.id === DEFAULT_STYLE);
}

/**
 * opts: { style, format: "9:16"|"16:9", brand, cutout, camW, camH, total, cuts, music, out }
 * returns { events: [[t, sfxFile, dB]...], W, H }
 */
export async function compose(scenes, words, opts) {
  const st = getStyle(opts.style);
  const styleDir = path.join(STYLES_DIR, st.id);
  const mod = await import(pathToFileURL(path.join(styleDir, "compose.mjs")).href);
  const format = st.formats.includes(opts.format) ? opts.format : st.formats[0];
  const res = await mod.default(scenes, words, {
    ...opts, format, cutout: !!(opts.cutout && st.cutout), styleDir, bpm: MUSIC[opts.music]?.bpm || null,
  });
  return { ...res, events: res.events.filter((e) => e[0] >= 0 && e[0] < opts.total - 0.1).sort((x, y) => x[0] - y[0]) };
}

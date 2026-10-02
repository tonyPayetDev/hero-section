// Shared helpers: ffmpeg / ffprobe / hyperframes binaries, process runner, small utils.
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const ASSETS = path.join(ROOT, "assets");

function resolveBin(envName, mod, fallback) {
  if (process.env[envName]) return process.env[envName];
  try {
    const m = require(mod);
    const p = typeof m === "string" ? m : m.path;
    if (p && fs.existsSync(p)) return p;
  } catch { /* not installed */ }
  return fallback;
}

export const FFMPEG = resolveBin("FFMPEG", "ffmpeg-static", "ffmpeg");
export const FFPROBE = resolveBin("FFPROBE", "ffprobe-static", "ffprobe");
export const FPS = 30;

// hyperframes needs ffmpeg/ffprobe on PATH (snapshot, render, remove-background)
const extraPath = [path.dirname(FFMPEG), path.dirname(FFPROBE), path.join(ROOT, "node_modules", ".bin")]
  .filter((p) => p && p !== ".").join(path.delimiter);
export const ENV = { ...process.env, PATH: extraPath + path.delimiter + (process.env.PATH || "") };
export const HF = process.platform === "win32"
  ? path.join(ROOT, "node_modules", ".bin", "hyperframes.cmd")
  : path.join(ROOT, "node_modules", ".bin", "hyperframes");

/** run a command; resolves {code, stdout, stderr}; rejects on non-zero unless opts.ok */
export function run(cmd, args, opts = {}) {
  return new Promise((resolve, reject) => {
    const p = spawn(cmd, args, { env: ENV, cwd: opts.cwd, shell: process.platform === "win32" && cmd.endsWith(".cmd") });
    let out = "", err = "";
    p.stdout.on("data", (d) => { out += d; opts.onData?.(String(d)); });
    p.stderr.on("data", (d) => { err += d; opts.onData?.(String(d)); });
    p.on("error", reject);
    p.on("close", (code) => {
      if (code !== 0 && !opts.ok) reject(new Error(`${path.basename(cmd)} ${args.slice(0, 6).join(" ")} -> exit ${code}\n${err.slice(-1500)}`));
      else resolve({ code, stdout: out, stderr: err });
    });
  });
}

export const ff = (args, opts) => run(FFMPEG, ["-nostdin", "-v", "error", "-y", ...args], opts);

export async function probe(file) {
  const { stdout } = await run(FFPROBE, ["-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
    "-of", "json", file]);
  const j = JSON.parse(stdout);
  const v = (j.streams || []).find((s) => s.codec_type === "video");
  const a = (j.streams || []).find((s) => s.codec_type === "audio");
  return { duration: parseFloat(j.format?.duration || "0"), width: v?.width || 0, height: v?.height || 0, hasAudio: !!a, hasVideo: !!v };
}

export async function duration(file) { return (await probe(file)).duration; }

export const q = (t) => Math.round(Math.round(t * FPS) / FPS * 10000) / 10000;
export const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
export const readJSON = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
export const writeJSON = (p, o) => fs.writeFileSync(p, JSON.stringify(o, null, 1));

/** deterministic PRNG (no Math.random in compositions) */
export function rng(seed) {
  let s = seed % 2147483647; if (s <= 0) s += 2147483646;
  return () => ((s = (s * 16807) % 2147483647) - 1) / 2147483646;
}

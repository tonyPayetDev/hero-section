// AutoBoost Studio - local web server. `npm start` then open http://localhost:4747
import express from "express";
import multer from "multer";
import fs from "node:fs";
import path from "node:path";
import { ROOT, readJSON } from "./lib/tools.mjs";
import { runJob } from "./lib/pipeline.mjs";

const PORT = +process.env.PORT || 4747;
const JOBS = path.join(ROOT, "jobs");
fs.mkdirSync(JOBS, { recursive: true });
const cfgPath = path.join(ROOT, "config.json");
const config = () => (fs.existsSync(cfgPath) ? readJSON(cfgPath) : readJSON(path.join(ROOT, "config.example.json")));

const app = express();
app.use(express.json());
app.use(express.static(path.join(ROOT, "web")));
app.use("/jobs", express.static(JOBS));
app.use("/assets", express.static(path.join(ROOT, "assets")));

// uploads land straight in the job folder
const upload = multer({
  storage: multer.diskStorage({
    destination: (req, _f, cb) => {
      req.jobId ||= new Date().toISOString().replace(/[-:T]/g, "").slice(0, 14) + "-" + Math.random().toString(36).slice(2, 6);
      const d = path.join(JOBS, req.jobId);
      fs.mkdirSync(d, { recursive: true });
      cb(null, d);
    },
    filename: (_req, f, cb) => cb(null, f.fieldname + path.extname(f.originalname || ".mp4").toLowerCase()),
  }),
  limits: { fileSize: 4 * 1024 ** 3 },
});

// one render at a time: the renderer and whisper already use every core
const queue = [];
let busy = false;
async function pump() {
  if (busy || !queue.length) return;
  busy = true;
  const job = queue.shift();
  try { await runJob(job); } finally { busy = false; pump(); }
}

app.get("/api/options", (_req, res) => {
  const music = readJSON(path.join(ROOT, "templates", "music.json"));
  const c = config();
  res.json({ music: Object.entries(music).map(([k, v]) => ({ id: k, label: v.label })), defaults: { ...c, wavespeedKey: c.wavespeedKey ? "••••" : "" } });
});

app.post("/api/config", (req, res) => {
  const c = { ...config(), ...req.body };
  if (req.body.wavespeedKey === "••••") c.wavespeedKey = config().wavespeedKey;
  fs.writeFileSync(cfgPath, JSON.stringify(c, null, 2));
  res.json({ ok: true });
});

app.post("/api/jobs", upload.fields([{ name: "video", maxCount: 1 }, { name: "competitor", maxCount: 1 }, { name: "music", maxCount: 1 }]), (req, res) => {
  const f = req.files || {};
  if (!f.video) return res.status(400).json({ error: "Ajoute ta vidéo." });
  const c = config();
  const b = req.body;
  const opts = {
    format: b.format || c.format, voice: b.voice || c.voice, cutout: b.cutout === "on" || b.cutout === "true",
    musicChoice: f.music ? "custom" : (b.music || c.music), cta: b.cta || "", tempo: b.tempo || c.tempo,
    cutSilences: b.cutSilences !== "off", brand: b.brand || c.brand, model: c.whisperModel,
    wavespeedKey: c.wavespeedKey, voiceRefUrl: b.voiceRefUrl || c.voiceRefUrl, webhook: c.webhook,
  };
  if (opts.voice === "clone-wavespeed" && (!opts.wavespeedKey || !opts.voiceRefUrl)) return res.status(400).json({ error: "Voix clonée WaveSpeed : renseigne ta clé et l'URL de ta voix de référence (Réglages)." });
  if (opts.voice === "clone-webhook" && !opts.webhook) return res.status(400).json({ error: "Voix clonée webhook : renseigne l'URL du webhook (Réglages)." });
  const dir = path.join(JOBS, req.jobId);
  const job = { id: req.jobId, dir, video: f.video[0].path, competitor: f.competitor?.[0]?.path, music: f.music?.[0]?.path, opts };
  fs.writeFileSync(path.join(dir, "job.json"), JSON.stringify({ id: job.id, status: "queued", step: "En attente", progress: 0, log: [] }));
  queue.push(job);
  pump();
  res.json({ id: job.id });
});

app.get("/api/jobs", (_req, res) => {
  const list = fs.readdirSync(JOBS).filter((d) => fs.existsSync(path.join(JOBS, d, "job.json")))
    .map((d) => { const j = readJSON(path.join(JOBS, d, "job.json")); return { id: d, status: j.status, step: j.step, progress: j.progress, result: j.result }; })
    .sort((a, b) => (a.id < b.id ? 1 : -1));
  res.json(list);
});

app.get("/api/jobs/:id", (req, res) => {
  const p = path.join(JOBS, path.basename(req.params.id), "job.json");
  if (!fs.existsSync(p)) return res.status(404).json({ error: "inconnu" });
  res.json(readJSON(p));
});

app.listen(PORT, () => console.log(`\n  AutoBoost Studio -> http://localhost:${PORT}\n`));

// One job = one video in, one MP4 out. Steps are logged to job.json so the web page can follow.
import fs from "node:fs";
import path from "node:path";
import { HF, ff, probe, run, writeJSON, FPS } from "./tools.mjs";
import { transcribe } from "./transcribe.mjs";
import { cutTake } from "./cut.mjs";
import { enhance, revoice } from "./voice.mjs";
import { rhythm } from "./competitor.mjs";
import { plan } from "./plan.mjs";
import { compose } from "./compose.mjs";
import { mix } from "./mix.mjs";

/**
 * job: { id, dir, video, competitor?, music?, opts: { format, voice, wavespeedKey, voiceRefUrl, webhook, cutout,
 *        musicChoice, cta, tempo, cutSilences, brand, model } }
 */
export async function runJob(job) {
  const st = { id: job.id, status: "running", step: "", progress: 0, log: [], result: null, error: null, started: Date.now() };
  const save = () => writeJSON(path.join(job.dir, "job.json"), st);
  const log = (m) => { st.log.push(`${new Date().toISOString().slice(11, 19)}  ${m}`); save(); };
  const step = (name, p) => { st.step = name; st.progress = p; log("▶ " + name); };
  const o = job.opts;
  try {
    const work = path.join(job.dir, "work");
    fs.mkdirSync(work, { recursive: true });
    const info = await probe(job.video);
    if (!info.hasVideo || !info.hasAudio) throw new Error("la vidéo doit contenir une image ET du son (ta voix)");
    log(`vidéo: ${info.width}x${info.height}, ${info.duration.toFixed(1)} s`);

    // 1. competitor pacing (optional)
    let pace = 3.6;
    if (job.competitor) {
      step("Analyse du rythme du concurrent", 5);
      const r = await rhythm(job.competitor);
      pace = Math.min(5, Math.max(2, r.medianShot * 1.4));
      st.competitor = r;
      log(`concurrent: ${r.shots} plans, plan médian ${r.medianShot} s, ${r.cutsPerMin} coupes/min -> un écran toutes les ~${pace.toFixed(1)} s`);
    }

    // 2. transcription
    step("Transcription (locale)", 10);
    const words0 = await transcribe(job.video, work, { model: o.model || "small", language: "fr", log });
    if (!words0.length) throw new Error("aucune parole détectée dans la vidéo");
    log(`${words0.length} mots : « ${words0.slice(0, 14).map((w) => w.w).join(" ")}… »`);
    fs.writeFileSync(path.join(job.dir, "transcription.txt"), words0.map((w) => w.w).join(" "));

    // 3. picture + voice on the final timeline
    let take;
    if (o.voice === "clone-wavespeed" || o.voice === "clone-webhook") {
      step("Voix clonée + recalage de l'image", 25);
      take = await revoice(job.video, words0, work, {
        mode: o.voice === "clone-webhook" ? "webhook" : "wavespeed", key: o.wavespeedKey, refUrl: o.voiceRefUrl, webhook: o.webhook,
      }, log);
      const vEnh = path.join(work, "voice.wav");
      await ff(["-i", take.voice, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000", "-ar", "48000", "-ac", "1", vEnh]);
      take.voice = vEnh;
    } else {
      step(o.cutSilences === false ? "Accélération" : "Coupe des silences", 25);
      take = await cutTake(job.video, words0, work, { tempo: +o.tempo || 1.1, keepSilences: o.cutSilences === false, log });
      step("Amélioration de la voix", 35);
      take.voice = await enhance(take.voice, path.join(work, "voice.wav"));
    }
    log(`durée finale : ${take.total.toFixed(1)} s`);

    // 4. background removal (optional, slow on CPU)
    const comp = path.join(job.dir, "composition");
    fs.mkdirSync(comp, { recursive: true });
    const cinfo = await probe(take.cam);
    let cutout = false;
    if (o.cutout) {
      step("Suppression du fond (long sur CPU)", 40);
      await run(HF, ["remove-background", take.cam, "-o", path.join(comp, "cam.webm"), "--quality", "balanced"], {
        onData: (d) => { const m = String(d).match(/Frame (\d+)\/(\d+)/g); if (m) { const [a, b] = m.pop().match(/\d+/g); st.progress = 40 + Math.round(20 * a / b); save(); } },
      });
      cutout = true;
    } else {
      fs.copyFileSync(take.cam, path.join(comp, "cam.mp4"));
    }

    // 5. plan + composition
    step("Motion design (modèles, sans IA)", 60);
    const scenes = plan(take.words, { cta: (o.cta || "").trim(), pace, total: take.total });
    writeJSON(path.join(job.dir, "plan.json"), scenes.map((s) => ({ type: s.type, a: +s.a.toFixed(2), b: +s.b.toFixed(2), text: s.text, sticker: s.sticker && `${s.sticker.a} ${s.sticker.b}`, level: s.level })));
    log(scenes.map((s) => `${s.a.toFixed(1)}s ${s.type}`).join(" · "));
    const { events } = compose(scenes, take.words, {
      format: o.format, brand: o.brand, cutout, camW: cinfo.width, camH: cinfo.height, total: take.total, cuts: take.cuts,
      music: o.musicChoice, out: comp,
    });

    // 6. render
    step("Rendu HyperFrames", 65);
    const silent = path.join(work, "silent.mp4");
    await run(HF, ["render", comp, "-o", silent, "--fps", String(FPS), "--quality", "delivery"], {
      onData: (d) => { const m = String(d).match(/frame (\d+)\/(\d+)/gi); if (m) { const [a, b] = m.pop().match(/\d+/g); st.progress = 65 + Math.round(27 * a / b); save(); } },
    });

    // 7. mix + mux
    step("Mixage voix + musique + bruitages", 93);
    const mixWav = path.join(work, "mix.wav");
    await mix({ voice: take.voice, events, total: take.total, music: o.musicChoice, customMusic: job.music, work, out: mixWav });
    const nf = Math.round(take.total * FPS);
    const final = path.join(job.dir, "video-finale.mp4");
    await ff(["-i", silent, "-i", mixWav, "-map", "0:v", "-map", "1:a", "-frames:v", String(nf), "-c:v", "libx264", "-crf", "20", "-preset", "medium",
      "-pix_fmt", "yuv420p", "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", take.total.toFixed(3), final]);
    st.result = "video-finale.mp4";
    st.status = "done"; st.progress = 100; st.step = "Terminé";
    log(`terminé en ${Math.round((Date.now() - st.started) / 1000)} s`);
  } catch (e) {
    st.status = "error"; st.error = String(e.message || e);
    log("ERREUR : " + st.error);
  }
  save();
  return st;
}

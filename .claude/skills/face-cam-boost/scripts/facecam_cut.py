#!/usr/bin/env python3
"""FaceCam Boost - from a raw facecam take to a cut, timed, composition-ready base.

Stages (run all, or one with --stage):
  transcribe  faster-whisper word timestamps          -> WORK/transcript.json
  plan        ASR fixes, merged tokens, cuts + beats   -> WORK/plan.json
  cut         one encode per cut (tempo), concat,
              durations re-measured, timeline remapped -> WORK/base.mp4, WORK/plan_actual.json,
                                                          WORK/voice.wav, WORK/facecam.mp4

  python3 facecam_cut.py take.mp4 --work build/ [--fixes fixes.json] [--tempo 1.14]

fixes.json (written after reading transcript.json - names and jargon are what
Whisper gets wrong):
  {"fix": {"3,6": "pas", "5,3": "CLAUDE"}, "drop": ["10,5", "10,6"],
   "start": 0.0, "end": null}
keys are "segment,word" indexes in transcript.json; "start"/"end" trim the take.
"""
import argparse, json, os, re, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or shutil.which("ffprobe") or "ffprobe"
FPS = 30


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print("\n".join(r.stderr.strip().splitlines()[-12:]), file=sys.stderr)
        raise SystemExit("ffmpeg failed: " + " ".join(args[:8]))


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]).decode().strip())


# ------------------------------------------------------------------ transcribe
def transcribe(src, work, model):
    from faster_whisper import WhisperModel
    wav = os.path.join(work, "audio16k.wav")
    run([FF, "-nostdin", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav, "-y"])
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, language="fr", word_timestamps=True, vad_filter=True,
                           initial_prompt="Claude Code, CLAUDE.md, Opus, n8n, sous-agents, tokens, automatisation.")
    out = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
            "words": [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for w in (s.words or [])]}
           for s in segs]
    json.dump(out, open(os.path.join(work, "transcript.json"), "w"), ensure_ascii=False, indent=1)
    for i, s in enumerate(out):
        print(f"{i:>2} [{s['start']:6.2f}-{s['end']:6.2f}] " + " | ".join(f"{k}:{w['w']}" for k, w in enumerate(s["words"])))


# ------------------------------------------------------------------ plan
def plan(work, fixes, tempo, gap, beat_max=3.6, beat_min=0.8, pad_in=0.10, pad_out=0.14):
    segs = json.load(open(os.path.join(work, "transcript.json")))
    fx = {tuple(map(int, k.split(","))): v for k, v in fixes.get("fix", {}).items()}
    drop = {tuple(map(int, k.split(","))) for k in fixes.get("drop", [])}
    t0, t1 = fixes.get("start") or 0.0, fixes.get("end")
    words = []
    for si, s in enumerate(segs):
        for wi, w in enumerate(s["words"]):
            if (si, wi) in drop or w["s"] < t0 or (t1 is not None and w["e"] > t1):
                continue
            words.append({"w": fx.get((si, wi), w["w"]), "s": w["s"], "e": w["e"]})
    # Whisper splits "sous-agents", "peut-être", "CLAUDE.md": merge so captions highlight whole words
    merged = [words[0]]
    for w in words[1:]:
        if re.match(r"^['\-.]", w["w"]):
            merged[-1] = {"w": merged[-1]["w"] + w["w"], "s": merged[-1]["s"], "e": w["e"]}
        else:
            merged.append(w)
    phrases, cur = [], [merged[0]]
    for prev, w in zip(merged, merged[1:]):
        if w["s"] - prev["e"] > gap:
            phrases.append(cur); cur = []
        cur.append(w)
    phrases.append(cur)

    cuts, t = [], 0.0
    for i, ph in enumerate(phrases):
        a, b = max(0.0, ph[0]["s"] - pad_in), ph[-1]["e"] + pad_out
        cuts.append({"i": i, "src_in": round(a, 3), "src_out": round(b, 3), "out_start": round(t, 3),
                     "dur": round((b - a) / tempo, 3), "text": " ".join(w["w"] for w in ph),
                     "words": [{"w": w["w"], "s": round((w["s"] - a) / tempo + t, 3),
                                "e": round((w["e"] - a) / tempo + t, 3)} for w in ph]})
        t += (b - a) / tempo
    total = t
    marks = {round(c["out_start"], 2) for c in cuts}
    for c in cuts:
        for w in c["words"]:
            if re.search(r"[.!?,]$", w["w"]):
                marks.add(round(w["e"], 2))
    marks = sorted(m for m in marks if m < total - 0.4)
    kept = []
    for m in marks:
        if not kept or m - kept[-1] >= beat_min:
            kept.append(m)
    beats = []
    for a, b in zip(kept, kept[1:] + [total]):
        n = max(1, round((b - a) / beat_max + 0.49))
        beats += [round(a + k * (b - a) / n, 3) for k in range(n)]
    out = {"total": round(total, 3), "tempo": tempo, "plan": cuts, "beats": sorted(set(beats))}
    json.dump(out, open(os.path.join(work, "plan.json"), "w"), ensure_ascii=False, indent=1)
    worst = max(b2 - b1 for b1, b2 in zip(out["beats"], out["beats"][1:] + [total]))
    print(f"{len(cuts)} coupes | {len(out['beats'])} battements | {total:.2f}s | plus long battement {worst:.2f}s")
    for c in cuts:
        print(f"  {c['i']:>2} [{c['out_start']:6.2f} +{c['dur']:5.2f}] {c['text']}")


# ------------------------------------------------------------------ cut
def cut(src, work):
    P = json.load(open(os.path.join(work, "plan.json")))
    tempo = P["tempo"]
    files = []
    for c in P["plan"]:
        out = os.path.join(work, f"cut{c['i']:02d}.mp4")
        run([FF, "-nostdin", "-v", "error", "-ss", str(c["src_in"]), "-to", str(c["src_out"]), "-i", src,
             "-vf", f"setpts=PTS/{tempo},fps={FPS}", "-af", f"atempo={tempo},aresample=48000",
             "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1", "-video_track_timescale", "30000", out, "-y"])
        files.append(os.path.abspath(out))  # concat resolves relative paths against the list file
    lst = os.path.join(work, "cuts.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    base = os.path.join(work, "base.mp4")
    run([FF, "-nostdin", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base, "-y"])

    # each cut rounds to a whole frame: re-measure and remap so captions never drift
    t, plan_a = 0.0, []
    for c in P["plan"]:
        d = dur(os.path.join(work, f"cut{c['i']:02d}.mp4"))
        k = d / c["dur"]
        plan_a.append(dict(c, out_start=round(t, 3), dur=round(d, 3), words=[
            {"w": w["w"], "s": round(t + (w["s"] - c["out_start"]) * k, 3), "e": round(t + (w["e"] - c["out_start"]) * k, 3)}
            for w in c["words"]]))
        t += d
    beats = []
    for b in P["beats"]:
        src_c = max((c for c in P["plan"] if c["out_start"] <= b + 1e-6), key=lambda c: c["out_start"])
        dst = plan_a[src_c["i"]]
        beats.append(round(dst["out_start"] + (b - src_c["out_start"]) * dst["dur"] / src_c["dur"], 3))
    json.dump({"total": round(t, 3), "tempo": tempo, "plan": plan_a, "beats": sorted(set(beats))},
              open(os.path.join(work, "plan_actual.json"), "w"), ensure_ascii=False, indent=1)

    run([FF, "-nostdin", "-v", "error", "-i", base, "-vn", "-c:a", "pcm_s16le", os.path.join(work, "voice.wav"), "-y"])
    # the composition's <video>: muted, a keyframe every frame-second so every seek is clean
    run([FF, "-nostdin", "-v", "error", "-i", base, "-an", "-c:v", "libx264", "-crf", "18", "-g", str(FPS),
         "-keyint_min", str(FPS), "-pix_fmt", "yuv420p", "-movflags", "+faststart", os.path.join(work, "facecam.mp4"), "-y"])
    print(f"base.mp4 / facecam.mp4 / voice.wav : {t:.2f}s (plan {P['total']:.2f}s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--work", required=True)
    ap.add_argument("--stage", default="all", choices=["all", "transcribe", "plan", "cut"])
    ap.add_argument("--model", default="medium")
    ap.add_argument("--fixes")
    ap.add_argument("--tempo", type=float, default=1.14)
    ap.add_argument("--gap", type=float, default=0.55)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    fixes = json.load(open(a.fixes)) if a.fixes else {}
    if a.stage in ("all", "transcribe"):
        transcribe(a.src, a.work, a.model)
    if a.stage in ("all", "plan"):
        plan(a.work, fixes, a.tempo, a.gap)
    if a.stage in ("all", "cut"):
        cut(a.src, a.work)

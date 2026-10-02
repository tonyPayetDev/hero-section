#!/usr/bin/env python3
"""Histoire du jour - build one episode end to end from its data folder.

    python3 tools/build.py M                     # everything
    python3 tools/build.py M --only compose,lint # some stages
    python3 tools/build.py B --no-whisper        # skip Whisper (cue times estimated)

Stages (in order):
  slice     master sheet -> assets/cut/*.png (tools/slice_sheet.py + tools/mouth.py), when a sheet exists
  tts       one Kokoro wav per narration segment (cached in build/tts/)
  timing    fit every scene to its window (atempo <= maxAtempo, else extend), build/vo_raw.wav + build/timeline.json
  whisper   word timings per scene (cached in build/whisper/) -> exact cue times
  mix       voice -16 LUFS + optional music bed -30 LUFS -> build/mix.wav
  compose   composition/index.html (+ assets, gsap, font, audio)
  lint      hyperframes lint
  snapshot  hyperframes snapshot at 8 key times + build/snapshots/contact.png
  render    output/histoire_du_jour_<L>.mp4 (+ ffprobe verification, AAC mux fallback)

Everything episode-specific comes from episodes/<L>/config/*.json; this file is the engine.
"""
import argparse
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import unicodedata

import numpy as np
import soundfile as sf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
ENGINE = os.path.join(ROOT, "engine")
FPS = 30
SR = 24000
W, H = 1080, 1920
SAFE = 120
XF = 0.4  # scene cross-fade
HF = os.environ.get("HDJ_HYPERFRAMES", f"npx --prefix {os.path.join(REPO, 'autoboost-studio')} hyperframes").split()
FFMPEG = os.environ.get("FFMPEG", shutil.which("ffmpeg") or "ffmpeg")
FFPROBE = os.environ.get("FFPROBE", shutil.which("ffprobe") or "ffprobe")

UI = {"letterOfDay": "La lettre du jour"}
STAGES = ["slice", "tts", "timing", "whisper", "mix", "compose", "lint", "snapshot", "render"]


# ---------------------------------------------------------------- helpers
def log(*a):
    print("[hdj]", *a, flush=True)


def run(cmd, check=True, **kw):
    log("$", " ".join(str(c) for c in cmd)[:220])
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if check and r.returncode != 0:
        sys.stderr.write(r.stdout[-3000:] + "\n" + r.stderr[-3000:] + "\n")
        raise SystemExit(f"command failed ({r.returncode}): {cmd[0]} ...")
    return r


def q(t):
    return round(round(t * FPS) / FPS, 4)


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9']", "", s)


def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def odd_repeat(total, cycle):
    """Finite, odd repeat count for a yoyo tween so it ends where it started (never -1)."""
    return max(1, 2 * int(total / (2 * cycle)) - 1)


def sha(*parts):
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:16]


class Episode:
    def __init__(self, letter):
        self.letter = letter
        self.dir = os.path.join(ROOT, "episodes", letter)
        if not os.path.isdir(self.dir):
            raise SystemExit(f"no episode folder: {self.dir}")
        cfg = os.path.join(self.dir, "config")
        self.project = json.load(open(os.path.join(cfg, "project.json")))
        self.scenes = json.load(open(os.path.join(cfg, "scenes.json")))
        self.ep = self.project["episode"]
        self.voice = {"engine": "kokoro", "voice": "ff_siwis", "speed": 0.92, "maxAtempo": 1.15, "leadSec": 0.35, "tailSec": 0.35}
        self.voice.update(self.project.get("voice", {}))
        self.audio = self.project.get("audio", {})
        self.theme = {"ink": "#1f3a8a", "accent": "#e53935", "accent2": "#1e6fd9", "card": "#fff8e7", "wood": "#7a4a22"}
        self.theme.update(self.project.get("theme", {}))
        self.ui = dict(UI, **self.project.get("ui", {}))
        self.build = os.path.join(self.dir, "build")
        self.comp = os.path.join(self.dir, "composition")
        self.out = os.path.join(self.dir, "output")
        for d in (self.build, self.comp, self.out):
            os.makedirs(d, exist_ok=True)
        hero_id = self.ep.get("hero", {}).get("id", "milo")
        self.hero_dir = os.path.join(ROOT, "heroes", hero_id)
        hp = os.path.join(self.hero_dir, "hero.json")
        self.hero = json.load(open(hp)) if os.path.exists(hp) else {"poses": {}}
        self.missing = []
        self.validate()

    def validate(self):
        need = ["letter", "upper", "lower", "sound", "hero", "quest", "words", "game", "recap", "outro"]
        miss = [k for k in need if k not in self.ep]
        if miss:
            raise SystemExit(f"project.json episode block misses: {miss}")
        types = [s.get("type") for s in self.scenes]
        if types != ["intro", "quest", "words", "game", "reward"]:
            log(f"warning: scene types are {types} (expected intro, quest, words, game, reward)")
        ans = self.ep["game"]["answer"]
        if ans not in [c["word"] for c in self.ep["game"]["choices"]]:
            raise SystemExit("game.answer must be one of game.choices")

    def asset(self, stem):
        """Resolve an asset stem (no extension) -> absolute path or None."""
        for d in (os.path.join(self.dir, "assets", "cut"), os.path.join(self.dir, "assets"), self.hero_dir, os.path.join(ROOT, "shared")):
            for ext in (".png", ".jpg", ".jpeg", ".webp"):
                p = os.path.join(d, stem + ext)
                if os.path.exists(p):
                    return p
        return None


# ---------------------------------------------------------------- stage: slice
def stage_slice(E, force=False):
    sheet = os.path.join(E.dir, "assets", "source", "assets_master_sheet.png")
    cut = os.path.join(E.dir, "assets", "cut")
    if not os.path.exists(sheet):
        log("no master sheet -> skipping slice (assets resolved from assets/, heroes/ or placeholders)")
        return
    if os.path.isdir(cut) and os.listdir(cut) and not force:
        log("assets/cut already present (use --reslice to redo)")
        return
    print(run([sys.executable, os.path.join(HERE, "slice_sheet.py"), E.letter]).stdout)


# ---------------------------------------------------------------- stage: tts + timing
def tts(E, text):
    d = os.path.join(E.build, "tts")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, sha(E.voice["voice"], E.voice["speed"], text) + ".wav")
    if not os.path.exists(p):
        run(HF + ["tts", text, "-v", E.voice["voice"], "-s", str(E.voice["speed"]), "-o", p, "--json"])
    return p


def read_mono(p):
    a, sr = sf.read(p, dtype="float32", always_2d=True)
    a = a.mean(1)
    if sr != SR:
        raise SystemExit(f"unexpected sample rate {sr} in {p}")
    return a


def trim_silence(a, thr_db=-42, keep=0.03):
    if not len(a):
        return a
    fr = 240
    n = len(a) // fr
    if n == 0:
        return a
    rms = np.sqrt((a[: n * fr].reshape(n, fr) ** 2).mean(1) + 1e-12)
    loud = np.nonzero(20 * np.log10(rms) > thr_db)[0]
    if not len(loud):
        return a
    s = max(0, loud[0] * fr - int(keep * SR))
    e = min(len(a), (loud[-1] + 1) * fr + int(keep * SR))
    return a[s:e]


def atempo(E, a, factor, tag):
    """Pitch-preserving tempo change through ffmpeg (factor > 1 = faster)."""
    if abs(factor - 1) < 0.005:
        return a
    d = os.path.join(E.build, "tts")
    src = os.path.join(d, f"_at_{tag}_in.wav")
    dst = os.path.join(d, f"_at_{tag}_out.wav")
    sf.write(src, a, SR)
    chain, f = [], factor
    while f < 0.5:
        chain.append("atempo=0.5")
        f /= 0.5
    while f > 2.0:
        chain.append("atempo=2.0")
        f /= 2.0
    chain.append(f"atempo={f:.5f}")
    run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-filter:a", ",".join(chain), "-ar", str(SR), "-ac", "1", dst])
    out = read_mono(dst)
    os.remove(src)
    os.remove(dst)
    return out


LEAD = {"intro": 0.55, "quest": 0.9, "words": 0.45, "game": 1.0, "reward": 0.6}


def stage_timing(E):
    ep = E.ep
    total = 0.0
    tl_scenes = []
    clips = []
    for si, sc in enumerate(E.scenes):
        typ = sc.get("type", "intro")
        lead = sc.get("leadSec", LEAD.get(typ, E.voice["leadSec"]))
        segs = []
        for gi, seg in enumerate(sc["segments"]):
            kind = seg.get("kind", "say")
            if kind == "sound":
                say, text = ep["sound"]["say"], ep["sound"]["display"]
            else:
                say, text = seg["say"], seg.get("text", seg["say"])
            pause = seg.get("pause", 0.25)
            if pause == "think":
                pause = float(ep["game"].get("thinkSec", 2.0))
            a = trim_silence(read_mono(tts(E, say)))
            if kind == "sound":
                hold = float(ep["sound"].get("holdSec", 1.0))
                a = atempo(E, a, len(a) / SR / hold, f"s{si}_{gi}")
            segs.append({"kind": kind, "say": say, "text": text, "pause": float(pause), "audio": a,
                         "cues": seg.get("cues", {}), "bubble": seg.get("bubble", True)})
        window = sc["end"] - sc["start"]
        speech = sum(len(s["audio"]) / SR for s in segs if s["kind"] != "sound")
        natural = lead + sum(len(s["audio"]) / SR + s["pause"] for s in segs)
        factor = 1.0
        if natural > window + 0.02 and speech > 0:
            excess = natural - window
            factor = min(E.voice["maxAtempo"], speech / max(0.1, speech - excess))
            for gi, s in enumerate(segs):
                if s["kind"] != "sound":
                    s["audio"] = atempo(E, s["audio"], factor, f"f{si}_{gi}")
            natural = lead + sum(len(s["audio"]) / SR + s["pause"] for s in segs)
        dur = q(max(window, natural))
        t = total + lead
        out_segs = []
        for s in segs:
            d = len(s["audio"]) / SR
            clips.append((t, s["audio"]))
            out_segs.append({"kind": s["kind"], "say": s["say"], "text": s["text"], "t0": round(t, 4), "t1": round(t + d, 4),
                             "pause": s["pause"], "cues": s["cues"], "bubble": s["bubble"]})
            t += d + s["pause"]
        tl_scenes.append({"id": sc["id"], "type": typ, "start": q(total), "dur": dur, "window": window, "atempo": round(factor, 3),
                          "lead": lead, "segments": out_segs})
        log(f"scene {sc['id']} {typ:6s} window {window:.2f}s -> {dur:.2f}s (natural {natural:.2f}s, atempo {factor:.3f})")
        total += dur
    total = q(total)
    vo = np.zeros(int(math.ceil(total * SR)) + SR, np.float32)
    for t0, a in clips:
        i = int(round(t0 * SR))
        vo[i:i + len(a)] += a[: max(0, len(vo) - i)]
    vo = vo[: int(round(total * SR))]
    sf.write(os.path.join(E.build, "vo_raw.wav"), vo, SR)
    for s in tl_scenes:
        a, b = int(s["start"] * SR), int((s["start"] + s["dur"]) * SR)
        sf.write(os.path.join(E.build, f"scene_{s['id']}.wav"), vo[a:b], SR)
    timeline = {"letter": E.letter, "total": total, "fps": FPS, "scenes": tl_scenes}
    json.dump(timeline, open(os.path.join(E.build, "timeline.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(E.build, "narration_timed.txt"), "w") as f:
        for sc in tl_scenes:
            f.write(f"# scene {sc['id']} {sc['type']} {sc['start']:.2f}-{sc['start'] + sc['dur']:.2f}s\n")
            for g in sc["segments"]:
                f.write(f"[{g['t0']:6.2f}-{g['t1']:6.2f}] {g['text']}\n")
    log(f"total {total:.2f}s")
    return timeline


# ---------------------------------------------------------------- stage: whisper + cues
def stage_whisper(E, timeline, enabled=True, allow_run=True):
    wdir = os.path.join(E.build, "whisper")
    os.makedirs(wdir, exist_ok=True)
    for sc in timeline["scenes"]:
        words = []
        if enabled and any(s["cues"] for s in sc["segments"]):
            wav = os.path.join(E.build, f"scene_{sc['id']}.wav")
            key = hashlib.sha1(open(wav, "rb").read()).hexdigest()[:16]
            cache = os.path.join(wdir, key + ".json")
            if not os.path.exists(cache) and allow_run:
                tmp = os.path.join(wdir, "tmp_" + key)
                os.makedirs(tmp, exist_ok=True)
                r = run(HF + ["transcribe", wav, "--model", "small", "--language", "fr", "--json", "--timeout", "900000", "-d", tmp], check=False)
                tj = os.path.join(tmp, "transcript.json")
                if r.returncode == 0 and os.path.exists(tj):
                    shutil.copy(tj, cache)
                shutil.rmtree(tmp, ignore_errors=True)
            if os.path.exists(cache):
                words = [{"w": w["text"], "s": sc["start"] + w["start"], "e": sc["start"] + w["end"]} for w in json.load(open(cache))]
        sc["words"] = words
        for s in sc["segments"]:
            s["triggers"] = []
            last = s["t0"] - 0.3
            for k, target in s["cues"].items():
                nk = norm(k)
                cand = [w for w in words if s["t0"] - 0.3 <= w["s"] <= s["t1"] + 0.3 and w["s"] >= last and (nk in norm(w["w"]) or (len(norm(w["w"])) >= 3 and norm(w["w"]) in nk))]
                if cand:
                    t, src = cand[0]["s"], "whisper"
                else:  # proportional estimate inside the segment
                    idx = norm(s["say"].replace(" ", "_")).find(nk)
                    frac = (idx / max(1, len(norm(s["say"].replace(" ", "_"))))) if idx >= 0 else 0.0
                    t, src = s["t0"] + (s["t1"] - s["t0"]) * frac, "estimate"
                last = t
                s["triggers"].append({"word": k, "target": target, "t": round(t, 3), "src": src})
    json.dump(timeline, open(os.path.join(E.build, "timeline.json"), "w"), indent=1, ensure_ascii=False)
    return timeline


# ---------------------------------------------------------------- mouth track
def mouth_track(E, timeline):
    vo = read_mono(os.path.join(E.build, "vo_raw.wav"))
    n = int(round(timeline["total"] * FPS))
    hop = SR // FPS
    rms = np.array([np.sqrt((vo[i * hop:(i + 1) * hop] ** 2).mean() + 1e-12) if i * hop < len(vo) else 0 for i in range(n)])
    voiced = rms[rms > 1e-3]
    ref = np.percentile(voiced, 95) if len(voiced) else 1.0
    hi, lo = 0.30 * ref, 0.17 * ref
    force = np.zeros(n, np.int8)  # 0 free, -1 closed, 1 open
    talk = np.zeros(n, bool)
    sound_mouth = E.ep["sound"].get("mouth", "closed")
    for sc in timeline["scenes"]:
        for s in sc["segments"]:
            a, b = int(s["t0"] * FPS), min(n, int(math.ceil(s["t1"] * FPS)))
            if s["kind"] == "sound" and sound_mouth in ("closed", "open"):
                force[a:b] = -1 if sound_mouth == "closed" else 1
            else:  # "energy": the sound is lip-synced like speech (plosives b/d/k/t…)
                talk[a:b] = True
    state = np.zeros(n, bool)
    cur, hold, peak, valley = False, 0, 0.0, 0.0
    for i in range(n):
        r = rms[i]
        if cur:
            peak = max(peak, r)
        else:
            valley = min(valley, r)
        if force[i] == -1 or (force[i] == 0 and not talk[i]):
            want = False
        elif force[i] == 1:
            want = r > lo
        elif cur:  # close on silence or on a syllable valley (energy well below the syllable peak)
            want = not (r < lo or r < 0.55 * peak)
        else:      # open on a new syllable onset
            want = r > hi and r > valley * 1.35 + 0.05 * ref
        if want != cur and (hold >= 2 or force[i] == -1):
            cur, hold = want, 0
            peak, valley = r, r
        hold += 1
        state[i] = cur
    return state


# ---------------------------------------------------------------- stage: mix
def stage_mix(E, timeline):
    total = timeline["total"]
    vo_raw = os.path.join(E.build, "vo_raw.wav")
    vo = os.path.join(E.build, "vo.wav")
    run([FFMPEG, "-y", "-loglevel", "error", "-i", vo_raw, "-af", f"loudnorm=I={E.audio.get('voiceLufs', -16)}:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", vo])
    mix = os.path.join(E.build, "mix.wav")
    music = E.audio.get("music")
    mpath = os.path.normpath(os.path.join(E.dir, music)) if music else None
    if mpath and os.path.exists(mpath):
        bgm = os.path.join(E.build, "bgm.wav")
        run([FFMPEG, "-y", "-loglevel", "error", "-stream_loop", "-1", "-t", f"{total:.3f}", "-i", mpath, "-af",
             f"loudnorm=I={E.audio.get('musicLufs', -30)}:TP=-6,afade=t=in:d=1.0,afade=t=out:st={max(0, total - 1.8):.3f}:d=1.8",
             "-ar", "48000", "-ac", "2", bgm])
        run([FFMPEG, "-y", "-loglevel", "error", "-i", vo, "-i", bgm, "-filter_complex",
             f"[0:a][1:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95,atrim=0:{total:.3f}", "-ar", "48000", mix])
        log(f"mix: voice {E.audio.get('voiceLufs', -16)} LUFS + music {os.path.basename(mpath)} {E.audio.get('musicLufs', -30)} LUFS")
    else:
        shutil.copy(vo, mix)
        log("mix: voice only (no music file)")


# ---------------------------------------------------------------- compose
class Comp:
    def __init__(self, E, timeline):
        self.E = E
        self.tl = timeline
        self.js = []
        self.used = {}
        self.ep = E.ep
        hlw = set(norm(w) for w in self.ep.get("highlight", []))
        hlw |= {norm(self.ep["upper"]), norm(self.ep["sound"]["display"])}
        self.hl = hlw
        self.prng = 1234567
        self.cs = 0.0

    # deterministic PRNG (no Math.random in the page)
    def rnd(self):
        self.prng = (1103515245 * self.prng + 12345) % 2147483648
        return self.prng / 2147483648

    def R(self, sel, t, frm, to, d=0.4, ease="power2.out", hold=False, **extra):
        """fromTo at global time t. hold=True also applies the from-state at the scene clip start,
        so an element that pops in later is hidden (not visible-then-jumping) before its entrance."""
        if hold and q(t) > q(self.cs):
            self.S(sel, self.cs, frm)
        to = dict(to, duration=d, ease=ease, immediateRender=False, **extra)
        self.js.append(f"tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(to)},{q(t)});")

    def S(self, sel, t, props):
        self.js.append(f"tl.set({json.dumps(sel)},{json.dumps(props)},{q(t)});")

    def img(self, stem, cls, style, id_=None, h=None, w=None):
        """<img> sized from the asset's real aspect, or a clearly named placeholder."""
        p = self.E.asset(stem)
        idattr = f' id="{id_}"' if id_ else ""
        if not p:
            if stem not in self.E.missing:
                self.E.missing.append(stem)
            ww, hh = (w or (h or 300)), (h or (w or 300))
            return (f'<div class="{cls} ph"{idattr} style="{style};width:{ww:.0f}px;height:{hh:.0f}px">'
                    f'<span style="display:block">PLACEHOLDER {html.escape(stem)}.png</span></div>'), ww, hh
        iw, ih = Image.open(p).size
        if h and not w:
            w = h * iw / ih
        elif w and not h:
            h = w * ih / iw
        elif not w and not h:
            w, h = iw, ih
        name = os.path.basename(p)
        self.used[name] = p
        return f'<img class="{cls}"{idattr} src="assets/{name}" style="{style};width:{w:.0f}px;height:{h:.0f}px" alt="">', w, h

    def rich(self, text):
        out = []
        text = re.sub(r"\s+([!?:;»])", " \\1", text)
        for tok in re.split(r"(\s+)", text):
            if not tok.strip():
                out.append(tok)
                continue
            core = norm(tok)
            parts = [p for p in re.split(r"'", core) if p]
            if core in self.hl or (parts and parts[-1] in self.hl):
                out.append(f'<span class="hl">{html.escape(tok)}</span>')
            else:
                out.append(html.escape(tok))
        return "".join(out)

    def first_letter_label(self, word):
        n = len(self.ep.get("labelPrefix", {}).get(word, word[:1]))
        return f'<span class="f">{html.escape(word[:n])}</span>{html.escape(word[n:])}'

    # -------------------------------------------------------------- hero
    def hero(self, sid, sc, pose, ax, ay, height, flip=False, walk=None, mouth=None):
        """Builds the hero stack: every pose frame x {closed, open}; only opacity of the stack changes,
        the wrapper (.hero/.bob) carries all motion, so mouth swaps never move the body."""
        poses = self.E.hero.get("poses", {})
        pc = poses.get(pose) or {"frames": [pose]}
        frames = pc["frames"]
        imgs, ids = [], {}
        ref_h = None
        for fi, stem in enumerate(frames):
            for st in ("closed", "open"):
                p = self.E.asset(f"{stem}__{st}") or self.E.asset(stem)
                key = f"{sid}-h{fi}{st[0]}"
                ids[(fi, st == "open")] = key
                if not p:
                    tag, _, _ = self.img(f"{stem}__{st}", "pose", "left:-200px", key, h=height)
                    imgs.append(tag)
                    continue
                iw, ih = Image.open(p).size
                if ref_h is None:
                    ref_h = ih
                hh = height * ih / ref_h  # keep relative scale between frames of a cycle
                ww = hh * iw / ih
                name = os.path.basename(p)
                self.used[name] = p
                op = 1 if (fi == 0 and st == "closed") else 0
                imgs.append(f'<img class="pose" id="{key}" src="assets/{name}" style="left:{-ww / 2:.0f}px;width:{ww:.0f}px;height:{hh:.0f}px;opacity:{op}" alt="">')
        flip_css = "transform:scaleX(-1);" if flip else ""
        shadow = '<i class="shadow"></i>' if pose != "sit" else ""
        htm = (f'<div class="hero" id="{sid}-hero" style="left:{ax}px;top:{ay}px">'
               f'<div class="bob" id="{sid}-bob"><div style="position:absolute;left:0;top:0;{flip_css}">{shadow}{"".join(imgs)}</div></div></div>')
        # per-frame image choice
        a = int(round(sc["start"] * FPS))
        b = int(round((sc["start"] + sc["dur"]) * FPS))
        cur = (0, False)
        cyc = pc.get("cycleSec", 0.26)
        for f in range(a, b):
            t = f / FPS
            fi = 0
            if walk and len(frames) > 1 and walk[0] <= t < walk[1]:
                fi = int((t - walk[0]) / cyc) % len(frames)
            op = bool(mouth[f]) if (mouth is not None and f < len(mouth) and pc.get("talk", True)) else False
            nxt = (fi, op)
            if nxt != cur:
                self.S("#" + ids[cur], t, {"opacity": 0})
                self.S("#" + ids[nxt], t, {"opacity": 1})
                cur = nxt
        # micro-bob 3 px while speaking (whole hero, never the mouth alone)
        for s in sc["segments"]:
            if s["kind"] == "sound":
                continue
            d = s["t1"] - s["t0"]
            n = max(1, int(d / 0.36))
            self.R(f"#{sid}-bob", s["t0"], {"y": 0}, {"y": -3}, 0.18, "sine.inOut", yoyo=True, repeat=2 * n - 1)
        return htm

    # -------------------------------------------------------------- bubbles
    def bubbles(self, sid, sc, top, tail=True):
        out = []
        segs = [s for s in sc["segments"] if s.get("bubble", True)]
        end = sc["start"] + sc["dur"]
        for i, s in enumerate(segs):
            bid = f"{sid}-b{i}"
            if s["kind"] == "sound":
                inner = f'<span class="snd">{html.escape(s["text"])}</span>'
                fs = 72
            else:
                L = len(s["text"])
                fs = 76 if L <= 18 else 66 if L <= 32 else 58 if L <= 48 else 52
                inner = self.rich(s["text"])
            out.append(f'<div class="bub{"" if tail else " top"}" id="{bid}" style="top:{top}px"><div class="b" style="font-size:{fs}px">{inner}</div></div>')
            t_in = s["t0"] - 0.08
            self.R("#" + bid, t_in, {"opacity": 0, "scale": 0.86, "y": 24}, {"opacity": 1, "scale": 1, "y": 0}, 0.28, "back.out(2)")
            nxt = segs[i + 1]["t0"] - 0.1 if i + 1 < len(segs) else None
            if nxt is not None:
                self.R("#" + bid, nxt - 0.02, {"opacity": 1}, {"opacity": 0}, 0.1, "power1.in")
            elif sc["type"] != "reward":
                self.R("#" + bid, end - 0.25, {"opacity": 1}, {"opacity": 0}, 0.2, "power1.in")
        return "".join(out)

    def sparkle_svg(self, cls, sid, k, x, y, size, color="#ffe680"):
        return (f'<svg class="{cls}" id="{sid}-sp{k}" style="left:{x - size / 2:.0f}px;top:{y - size / 2:.0f}px;width:{size:.0f}px;height:{size:.0f}px" viewBox="-50 -50 100 100">'
                f'<path d="M0,-50 C5,-9 9,-5 50,0 C9,5 5,9 0,50 C-5,9 -9,5 -50,0 C-9,-5 -5,-9 0,-50Z" fill="{color}"/></svg>')

    def twinkle(self, sel, t0, t1, delay):
        d = 0.5
        n = max(0, int((t1 - t0 - delay) / (2 * d)) - 1)
        self.R(sel, t0 + delay, {"opacity": 0, "scale": 0.3, "rotation": 0}, {"opacity": 1, "scale": 1, "rotation": 45}, d, "sine.inOut", yoyo=True, repeat=2 * n + 1)

    def triggers(self, sc):
        out = {}
        for s in sc["segments"]:
            for tr in s.get("triggers", []):
                out.setdefault(tr["target"], []).append(tr["t"])
        return out

    # -------------------------------------------------------------- scenes
    def scene(self, i, sc, mouth):
        sid = f"s{i + 1}"
        cfg = self.E.scenes[i]
        start, dur = sc["start"], sc["dur"]
        cstart = start - XF if i > 0 else 0
        cdur = dur + (start - cstart)
        self.cs = cstart
        body = []
        bg, _, _ = self.img(cfg.get("background", f"background_0{i + 1}"), "bgimg", "display:block", h=2133, w=1200)
        body.append(f'<div class="bgw" id="{sid}-bgw">{bg}</div><div class="shade"></div>')
        if i > 0:
            self.R("#" + sid, cstart, {"opacity": 0}, {"opacity": 1}, XF, "power1.inOut")
        typ = sc["type"]
        trig = self.triggers(sc)
        segs = sc["segments"]
        end = start + dur
        pan = {"quest": ({"x": 50, "scale": 1.0}, {"x": -50, "scale": 1.0})}.get(typ, ({"x": 0, "y": 0, "scale": 1.0}, {"x": -18, "y": -24, "scale": 1.04}))
        self.R(f"#{sid}-bgw", cstart, pan[0], pan[1], cdur, "none")
        getattr(self, "s_" + typ)(sid, sc, body, trig, segs, start, end, mouth)
        return (f'<section id="{sid}" class="scene clip" data-start="{q(cstart)}" data-duration="{q(cdur)}" data-track-index="{1 + i % 2}" '
                f'style="z-index:{i + 1}">{"".join(body)}</section>')

    def s_intro(self, sid, sc, body, trig, segs, start, end, mouth):
        ep = self.ep
        body.append(f'<div class="pill" id="{sid}-pill" style="top:{SAFE + 20}px"><span>{html.escape(self.E.ui["letterOfDay"])}</span></div>')
        self.R(f"#{sid}-pill", start + 0.1, {"opacity": 0, "y": -30}, {"opacity": 1, "y": 0}, 0.4, "back.out(2)")
        cx, cy = 540, 520
        for k in range(5):
            ang = k / 5 * 6.283 + 0.5
            body.append(self.sparkle_svg("spark", sid, k, cx + math.cos(ang) * 430, cy + math.sin(ang) * 270, 50 + 22 * (k % 2)))
            self.twinkle(f"#{sid}-sp{k}", start + 0.8, end, 0.17 * k)
        for k in range(3):
            body.append(f'<i class="ring" id="{sid}-r{k}" style="left:{cx - 330}px;top:{cy - 330}px;width:660px;height:660px"></i>')
        up, uw, uh = self.img(f"letter_{ep['upper']}_upper", "letter", "", f"{sid}-U", h=380)
        lo, lw, lh = self.img(f"letter_{ep['lower']}_lower", "letter", "", f"{sid}-u", h=300)
        if uw + lw + 40 > W - 2 * SAFE:  # keep the letters inside the safe zone
            k = (W - 2 * SAFE - 40) / (uw + lw)
            up, uw, uh = self.img(f"letter_{ep['upper']}_upper", "letter", "", f"{sid}-U", h=380 * k)
            lo, lw, lh = self.img(f"letter_{ep['lower']}_lower", "letter", "", f"{sid}-u", h=300 * k)
        gap = 40
        x0 = (W - (uw + lw + gap)) / 2
        body.append(up.replace('style="', f'style="left:{x0:.0f}px;top:{cy + 200 - uh:.0f}px', 1))
        body.append(lo.replace('style="', f'style="left:{x0 + uw + gap:.0f}px;top:{cy + 200 - lh:.0f}px', 1))
        self.R(f"#{sid}-U", start + 0.25, {"opacity": 0, "scale": 0, "rotation": -14}, {"opacity": 1, "scale": 1, "rotation": 0}, 0.7, "back.out(2.2)", hold=True)
        self.R(f"#{sid}-u", start + 0.55, {"opacity": 0, "scale": 0, "rotation": 14}, {"opacity": 1, "scale": 1, "rotation": 0}, 0.7, "back.out(2.2)", hold=True)
        for s in segs:
            if s["kind"] == "sound":
                for k in range(3):
                    self.R(f"#{sid}-r{k}", s["t0"] + k * 0.28, {"opacity": 0.85, "scale": 0.55}, {"opacity": 0, "scale": 1.3}, 0.95, "power1.out")
                for sel in (f"#{sid}-U", f"#{sid}-u"):
                    self.R(sel, s["t0"], {"scale": 1.1}, {"scale": 1}, 0.6, "elastic.out(1,0.45)")
        body.append(self.bubbles(sid, sc, 800))
        body.append(self.hero(sid, sc, "sit", 330, 1945, 620, mouth=mouth))
        self.R(f"#{sid}-hero", start + 0.15, {"y": 700}, {"y": 0}, 0.75, "back.out(1.3)", hold=True)

    def s_quest(self, sid, sc, body, trig, segs, start, end, mouth):
        ep = self.ep
        # floating leaves (parallax, behind the bubbles)
        for k in range(2):
            x0, y0 = 760 + self.rnd() * 160, 380 + self.rnd() * 200
            lf, _, _ = self.img("feuilles", "leaf", f"left:{x0:.0f}px;top:{y0:.0f}px", f"{sid}-lf{k}", w=130 + 40 * k)
            body.append(lf)
            t0 = start - XF + 0.4 * k
            self.R(f"#{sid}-lf{k}", t0, {"opacity": 0}, {"opacity": 1}, 0.5, "power1.out")
            self.R(f"#{sid}-lf{k}", t0, {"x": 0, "y": 0, "rotation": 0},
                   {"x": -700 - 100 * k, "y": 520 + 140 * k, "rotation": -50 + 30 * k}, end - t0, "sine.inOut")
        body.append(self.bubbles(sid, sc, SAFE + 10, tail=False))
        # thought bubble with the quest object (appears on the quest word)
        t_q = (trig.get("sign") or [segs[-1]["t0"]])[0]
        tw, th, tx, ty = 440, 400, 540, 400
        qimg, qw, qh = self.img(ep["quest"]["asset"], "", "", f"{sid}-qo", h=190)
        qimg = qimg.replace('style="', f'style="left:{tw / 2 - qw / 2:.0f}px;top:40px;', 1)
        label = ep["quest"]["label"]
        lfs = min(44, int(330 / max(1, len(label)) * 1.9))
        puffs = (f'<i class="puff" style="left:30px;top:{th - 14}px;width:56px;height:56px"></i>'
                 f'<i class="puff" style="left:-16px;top:{th + 46}px;width:34px;height:34px"></i>')
        body.append(f'<div class="think" id="{sid}-think" style="left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px"><i class="cloud"></i>{puffs}{qimg}'
                    f'<div class="qlab" style="top:{th - 150}px;font-size:{lfs}px">{html.escape(label)}</div></div>')
        self.R(f"#{sid}-think", t_q - 0.1, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.55, "back.out(1.8)", hold=True)
        self.R(f"#{sid}-qo", t_q + 0.45, {"rotation": -8}, {"rotation": 8}, 0.5, "sine.inOut", yoyo=True, repeat=odd_repeat(end - t_q - 0.6, 0.5))
        for k in range(4):
            ang = k * 1.7 + 0.4
            body.append(self.sparkle_svg("spark", sid, k, tx + tw / 2 + math.cos(ang) * 250, ty + th / 2 + math.sin(ang) * 215, 60 + 20 * (k % 2)))
            self.twinkle(f"#{sid}-sp{k}", t_q + 0.3, end, 0.15 * k)
        walk = (start - XF, end)
        body.append(self.hero(sid, sc, "walk", 0, 1880, 610, walk=walk, mouth=mouth))
        self.R(f"#{sid}-hero", start - XF, {"x": -120}, {"x": 470}, end - start + XF, "none")

    def cards(self, sid, items, top, cw, ch, labels=True):
        out = []
        gap = (W - 2 * SAFE - 3 * cw) / 2
        for k, it in enumerate(items):
            x = SAFE + k * (cw + gap)
            im, _, _ = self.img(it["asset"], "", "", None, h=ch * 0.6)
            out.append(f'<i class="glow" id="{sid}-g{k}" style="left:{x + cw / 2 - cw:.0f}px;top:{top + ch / 2 - cw:.0f}px;width:{2 * cw:.0f}px;height:{2 * cw:.0f}px"></i>')
            lab = f'<div class="lab" id="{sid}-l{k}" style="opacity:{1 if labels else 0}">{self.first_letter_label(it["word"])}</div>'
            out.append(f'<div class="card" id="{sid}-c{k}" style="left:{x:.0f}px;top:{top}px;width:{cw}px;height:{ch}px"><div class="im">{im}</div>{lab}</div>')
        return "".join(out)

    def s_words(self, sid, sc, body, trig, segs, start, end, mouth):
        ep = self.ep
        body.append(self.cards(sid, ep["words"], SAFE + 40, 270, 330))
        first = {}
        for k in range(3):
            times = trig.get(f"word{k}") or [segs[0]["t0"] + 0.6 * k]
            first[k] = times[0]
            self.R(f"#{sid}-c{k}", times[0] - 0.12, {"opacity": 0, "scale": 0.4, "y": 40}, {"opacity": 1, "scale": 1.05, "y": 0}, 0.36, "back.out(2)")
            self.R(f"#{sid}-c{k}", times[0] + 0.3, {"scale": 1.05}, {"scale": 1}, 0.35, "power2.out")
            self.R(f"#{sid}-g{k}", times[0] - 0.05, {"opacity": 0, "scale": 0.6}, {"opacity": 0.85, "scale": 1}, 0.3, "power2.out")
            self.R(f"#{sid}-g{k}", times[0] + 0.7, {"opacity": 0.85}, {"opacity": 0}, 0.4, "power1.in")
            for t in times[1:]:
                self.R(f"#{sid}-c{k}", t - 0.05, {"scale": 1.12}, {"scale": 1}, 0.6, "elastic.out(1,0.5)")
                self.R(f"#{sid}-g{k}", t - 0.05, {"opacity": 0, "scale": 0.7}, {"opacity": 0.9, "scale": 1.05}, 0.3, "power2.out")
                self.R(f"#{sid}-g{k}", t + 0.8, {"opacity": 0.9}, {"opacity": 0}, 0.4, "power1.in")
        for s in segs:
            if s["kind"] == "sound":  # every word starts with the sound: wave over the cards
                for k in range(3):
                    if first[k] < s["t0"]:
                        self.R(f"#{sid}-c{k}", s["t0"] + 0.18 * k, {"y": 0}, {"y": -26}, 0.18, "power1.out", yoyo=True, repeat=1)
        body.append(self.bubbles(sid, sc, 700))
        body.append(self.hero(sid, sc, "point", 280, 1885, 660, flip=True, mouth=mouth))
        self.R(f"#{sid}-hero", start - XF, {"x": -520}, {"x": 0}, 0.8, "back.out(1.2)")

    def s_game(self, sid, sc, body, trig, segs, start, end, mouth):
        ep = self.ep
        ch = ep["game"]["choices"]
        ans = [c["word"] for c in ch].index(ep["game"]["answer"])
        top, cw, chh = 500, 270, 360
        body.append(self.cards(sid, ch, top, cw, chh, labels=False))
        gap = (W - 2 * SAFE - 3 * cw) / 2
        ax = SAFE + ans * (cw + gap) + cw / 2
        burst, bw, bh = self.img("pop", "burst", f"left:{ax - 260:.0f}px;top:{top + chh / 2 - 260:.0f}px", f"{sid}-burst", w=520)
        body.insert(1, burst)
        rays, rw, rh = self.img("rayons", "rays", "", f"{sid}-rays", w=300)
        body.insert(1, rays.replace('style="', f'style="left:{ax - rw / 2:.0f}px;top:{top - rh + 10:.0f}px;', 1))
        for k in range(3):
            self.R(f"#{sid}-c{k}", start + 0.15 + 0.18 * k, {"opacity": 0, "scale": 0.5, "y": 60}, {"opacity": 1, "scale": 1, "y": 0}, 0.5, "back.out(1.8)")
        say_segs = [s for s in segs if s["kind"] == "say"]
        reveal = [s for s in segs if s["kind"] == "answer"]
        t_rev = reveal[0]["t0"] - 0.05 if reveal else end - 1.2
        think_from = (say_segs[-1]["t1"] if say_segs else t_rev - 2) + 0.05
        # question mark + thinking dots during the pause
        body.append(f'<div class="qmark" id="{sid}-qm" style="left:{W / 2 - 60:.0f}px;top:{top - 135}px">?</div>')
        q_t = say_segs[1]["t0"] if len(say_segs) > 1 else start + 0.5
        self.R(f"#{sid}-qm", q_t, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.4, "back.out(2.5)")
        self.R(f"#{sid}-qm", q_t + 0.4, {"rotation": -10}, {"rotation": 10}, 0.45, "sine.inOut", yoyo=True, repeat=odd_repeat(t_rev - q_t - 0.5, 0.45))
        self.R(f"#{sid}-qm", t_rev, {"opacity": 1}, {"opacity": 0}, 0.25)
        body.append(f'<div class="dots" id="{sid}-dots" style="top:{top + chh + 50}px">' + "".join(f'<i id="{sid}-d{k}"></i>' for k in range(3)) + "</div>")
        for k in range(3):
            n = max(1, int((t_rev - think_from - 0.15 * k) / 0.6))
            self.R(f"#{sid}-d{k}", think_from, {"opacity": 0}, {"opacity": 1}, 0.2)
            self.R(f"#{sid}-d{k}", think_from + 0.15 * k, {"y": 0}, {"y": -26}, 0.3, "sine.inOut", yoyo=True, repeat=2 * n - 1)
            self.R(f"#{sid}-d{k}", t_rev - 0.1, {"opacity": 1}, {"opacity": 0}, 0.2)
        # reveal: gentle glow + bounce, no stress
        self.R(f"#{sid}-g{ans}", t_rev, {"opacity": 0, "scale": 0.5}, {"opacity": 1, "scale": 1.1}, 0.5, "power2.out")
        self.R(f"#{sid}-rays", t_rev + 0.1, {"opacity": 0, "scale": 0.3, "y": 40}, {"opacity": 1, "scale": 1, "y": 0}, 0.5, "back.out(2)")
        self.R(f"#{sid}-burst", t_rev, {"opacity": 0.95, "scale": 0.2, "rotation": 0}, {"opacity": 0, "scale": 1.15, "rotation": 20}, 0.8, "power2.out")
        self.R(f"#{sid}-c{ans}", t_rev, {"scale": 1, "y": 0}, {"scale": 1.12, "y": -40}, 0.35, "back.out(3)")
        self.R(f"#{sid}-c{ans}", t_rev + 0.4, {"y": -40}, {"y": 0}, 0.6, "bounce.out")
        self.R(f"#{sid}-l{ans}", t_rev + 0.1, {"opacity": 0, "scale": 0.5}, {"opacity": 1, "scale": 1}, 0.4, "back.out(2.5)")
        for k in range(3):
            if k != ans:
                self.R(f"#{sid}-c{k}", t_rev, {"opacity": 1, "scale": 1}, {"opacity": 0.45, "scale": 0.9}, 0.45)
        for k in range(4):
            ang = k * 1.6 + 0.3
            body.append(self.sparkle_svg("spark", sid, k, ax + math.cos(ang) * 190, top + chh / 2 + math.sin(ang) * 230, 56 + 16 * (k % 2)))
            self.twinkle(f"#{sid}-sp{k}", t_rev + 0.2, end, 0.12 * k)
        body.append(self.bubbles(sid, sc, SAFE + 10, tail=False))
        body.append(self.hero(sid, sc, "sit", 300, 1945, 560, mouth=mouth))
        self.R(f"#{sid}-hero", start - XF, {"y": 650}, {"y": 0}, 0.75, "back.out(1.3)", hold=True)
        self.R(f"#{sid}-hero", think_from, {"rotation": 0}, {"rotation": -4}, 0.5, "sine.inOut", yoyo=True, repeat=odd_repeat(t_rev - think_from, 0.5))

    def s_reward(self, sid, sc, body, trig, segs, start, end, mouth):
        ep = self.ep
        # warm glow + Milo with the quest object
        body.append(f'<i class="glow" id="{sid}-glow" style="left:{540 - 520}px;top:{1440 - 520}px;width:1040px;height:1040px"></i>')
        self.R(f"#{sid}-glow", start, {"opacity": 0, "scale": 0.5}, {"opacity": 0.9, "scale": 1}, 0.9, "power2.out")
        self.R(f"#{sid}-glow", start + 0.9, {"scale": 1}, {"scale": 1.08}, 0.8, "sine.inOut", yoyo=True, repeat=odd_repeat(end - start - 1, 0.8))
        for k in range(10):
            ang = k / 10 * 6.283 + self.rnd() * 0.4
            rad = 360 + self.rnd() * 140
            body.append(self.sparkle_svg("spark", sid, k, 540 + math.cos(ang) * rad, 1400 + math.sin(ang) * rad * 0.9, 50 + 40 * self.rnd()))
            self.twinkle(f"#{sid}-sp{k}", start + 0.3, end, 0.13 * k)
        pose = self.E.scenes[self.tl["scenes"].index(sc)].get("pose", "quest")
        frames = self.E.hero.get("poses", {}).get(pose, {}).get("frames") or [f"{self.E.hero.get('id', 'milo')}_{slug(ep['quest'].get('asset', ep['quest']['word']))}_open"]
        holding = all(self.E.asset(f) for f in frames)
        if holding:  # hero holds the quest object (pose drawn on the sheet)
            body.append(self.hero(sid, sc, pose if pose in self.E.hero.get("poses", {}) else frames[0], 540, 1870, 760, mouth=mouth))
        else:  # fallback: sitting hero + the quest object floating in the glow
            qo, qw, qh = self.img(ep["quest"]["asset"], "", "left:620px;top:1160px", f"{sid}-qo", w=300)
            body.append(qo.replace('<img class=""', '<img class="letter"', 1))
            self.R(f"#{sid}-qo", start + 0.3, {"opacity": 0, "scale": 0.3, "y": 0}, {"opacity": 1, "scale": 1, "y": 0}, 0.6, "back.out(2)", hold=True)
            self.R(f"#{sid}-qo", start + 0.9, {"y": 0}, {"y": -24}, 0.7, "sine.inOut", yoyo=True, repeat=odd_repeat(end - start - 1, 0.7))
            body.append(self.hero(sid, sc, "sit", 340, 1945, 620, mouth=mouth))
        self.R(f"#{sid}-hero", start - XF, {"y": 500, "scale": 0.8}, {"y": 0, "scale": 1}, 0.8, "back.out(1.4)")
        # recap: letters + words
        up, uw, uh = self.img(f"letter_{ep['upper']}_upper", "letter", "", f"{sid}-U", h=150)
        lo, lw, lh = self.img(f"letter_{ep['lower']}_lower", "letter", "", f"{sid}-u", h=120)
        x0 = (W - uw - lw - 24) / 2
        rt = 400
        body.append(up.replace('style="', f'style="left:{x0:.0f}px;top:{rt + 150 - uh:.0f}px', 1))
        body.append(lo.replace('style="', f'style="left:{x0 + uw + 24:.0f}px;top:{rt + 150 - lh:.0f}px', 1))
        recap_seg = next((s for s in segs if any(tr["target"].startswith("recap") for tr in s.get("triggers", []))), segs[min(2, len(segs) - 1)])
        self.R(f"#{sid}-U", recap_seg["t0"] - 0.1, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.5, "back.out(2.2)", hold=True)
        self.R(f"#{sid}-u", recap_seg["t0"] + 0.05, {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1}, 0.5, "back.out(2.2)", hold=True)
        chips = "".join(f'<span class="chip" id="{sid}-k{k}" style="position:relative">{self.first_letter_label(w)}</span>' for k, w in enumerate(ep["recap"]))
        body.append(f'<div style="position:absolute;left:{SAFE}px;top:{rt + 175}px;width:{W - 2 * SAFE}px;display:flex;justify-content:center;gap:22px">{chips}</div>')
        for k in range(len(ep["recap"])):
            t = (trig.get(f"recap{k}") or [recap_seg["t0"] + 0.5 + 0.5 * k])[0]
            self.R(f"#{sid}-k{k}", t - 0.08, {"opacity": 0, "scale": 0.3, "y": 30}, {"opacity": 1, "scale": 1, "y": 0}, 0.45, "back.out(2.4)")
        # outro: big signature
        outro = next((s for s in segs if s["kind"] == "outro"), segs[-1])
        logo, lw2, lh2 = self.img("histoire_du_jour", "biglogo", f"left:{540 - 290}px;top:760px", f"{sid}-logo", w=580)
        body.append(logo)
        self.R(f"#{sid}-logo", outro["t0"] - 0.1, {"opacity": 0, "scale": 0.5, "y": 40}, {"opacity": 1, "scale": 1, "y": 0}, 0.6, "back.out(1.8)")
        self.R("#logo", outro["t0"] - 0.1, {"opacity": 0.9}, {"opacity": 0}, 0.3)
        body.append(self.bubbles(sid, sc, SAFE + 10, tail=False))

    def build(self, mouth):
        scenes = [self.scene(i, sc, mouth) for i, sc in enumerate(self.tl["scenes"])]
        total = self.tl["total"]
        logo, _, _ = self.img("histoire_du_jour", "", "left:0;top:0", "logo-img", w=230)
        glob = (f'<div id="logo" class="clip" data-start="0" data-duration="{total}" data-track-index="3" style="left:{W - SAFE - 230}px;top:{H - SAFE - 100}px;width:230px;height:100px;z-index:20">'
                f'{logo}</div>'
                f'<audio id="narration" src="assets/mix.wav" data-start="0" data-duration="{total}" data-track-index="10" data-volume="1"></audio>')
        tpl = open(os.path.join(ENGINE, "template.html")).read()
        th = self.E.theme
        out = (tpl.replace("%%TITLE%%", html.escape(self.E.project.get("name", "Histoire du jour")))
               .replace("%%TOTAL%%", str(total)).replace("%%SCENES%%", "\n".join(scenes)).replace("%%GLOBAL%%", glob)
               .replace("%%JS%%", "\n".join(self.js)).replace("%%INK%%", th["ink"]).replace("%%ACCENT%%", th["accent"])
               .replace("%%ACCENT2%%", th["accent2"]).replace("%%CARD%%", th["card"]).replace("%%WOOD%%", th["wood"]))
        return out


def stage_compose(E, timeline):
    mouth = mouth_track(E, timeline)
    C = Comp(E, timeline)
    page = C.build(mouth)
    comp = E.comp
    for sub in ("assets", "vendor", "fonts"):
        os.makedirs(os.path.join(comp, sub), exist_ok=True)
    shutil.copy(os.path.join(ENGINE, "vendor", "gsap.min.js"), os.path.join(comp, "vendor", "gsap.min.js"))
    shutil.copy(os.path.join(ENGINE, "fonts", "Outfit-Bold.ttf"), os.path.join(comp, "fonts", "Outfit-Bold.ttf"))
    for f in os.listdir(os.path.join(comp, "assets")):
        if f not in C.used and f != "mix.wav":
            os.remove(os.path.join(comp, "assets", f))
    for name, p in C.used.items():
        shutil.copy(p, os.path.join(comp, "assets", name))
    if os.path.exists(os.path.join(E.build, "mix.wav")):
        shutil.copy(os.path.join(E.build, "mix.wav"), os.path.join(comp, "assets", "mix.wav"))
    open(os.path.join(comp, "index.html"), "w").write(page)
    json.dump({"open_frames": int(mouth.sum()), "frames": len(mouth), "switches": int(np.abs(np.diff(mouth.astype(int))).sum())},
              open(os.path.join(E.build, "mouth_stats.json"), "w"))
    log(f"compose: {len(C.js)} tweens, {len(C.used)} assets, mouth open {mouth.mean() * 100:.0f}% of frames")
    if E.missing:
        log(f"PLACEHOLDERS used for missing assets: {', '.join(E.missing)}")


def snap_times(timeline):
    ts = []
    for sc in timeline["scenes"]:
        segs = sc["segments"]
        ts.append(sc["start"] + min(1.6, sc["dur"] * 0.4))
        if sc["type"] in ("words", "game", "reward"):
            ts.append(segs[-1]["t0"] + 0.9)
    return sorted(set(round(min(t, timeline["total"] - 0.1), 2) for t in ts))[:9]


def stage_snapshot(E, timeline, at=None):
    times = at or snap_times(timeline)
    out = os.path.join(E.build, "snapshots")
    shutil.rmtree(out, ignore_errors=True)
    run(HF + ["snapshot", E.comp, "--at", ",".join(str(t) for t in times), "--no-end", "-o", out, "--timeout", "20000", "--no-browser-gpu", "--describe", "false"])
    pngs = sorted([f for f in os.listdir(out) if f.endswith(".png")])
    if pngs:
        ims = [Image.open(os.path.join(out, f)).convert("RGB").resize((270, 480)) for f in pngs]
        cols = 4
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 280, rows * 490), (0, 0, 0))
        for k, im in enumerate(ims):
            sheet.paste(im, ((k % cols) * 280, (k // cols) * 490))
        sheet.save(os.path.join(out, "contact.png"))
        log(f"snapshots: {len(pngs)} frames -> {os.path.join(out, 'contact.png')} (times {times})")


def stage_render(E, timeline):
    mp4 = os.path.join(E.out, f"histoire_du_jour_{E.letter}.mp4")
    extra = ["--workers", os.environ["HDJ_RENDER_WORKERS"]] if os.environ.get("HDJ_RENDER_WORKERS") else []
    run(HF + ["render", E.comp, "-o", mp4, "--no-browser-gpu", "--quality", "delivery", "--fps", str(FPS), "--quiet"] + extra)
    info = json.loads(run([FFPROBE, "-v", "error", "-show_streams", "-show_format", "-of", "json", mp4]).stdout)
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    if not has_audio:
        log("render has no audio stream -> muxing build/mix.wav (AAC)")
        tmp = mp4 + ".tmp.mp4"
        run([FFMPEG, "-y", "-loglevel", "error", "-i", mp4, "-i", os.path.join(E.build, "mix.wav"), "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", tmp])
        os.replace(tmp, mp4)
        info = json.loads(run([FFPROBE, "-v", "error", "-show_streams", "-show_format", "-of", "json", mp4]).stdout)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    nb = run([FFPROBE, "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", mp4]).stdout.strip()
    rep = {"file": mp4, "size": f"{v['width']}x{v['height']}", "fps": v.get("r_frame_rate"), "frames": int(nb or 0),
           "expected_frames": int(round(timeline["total"] * FPS)), "duration": float(info["format"]["duration"]),
           "audio": [s["codec_name"] for s in info["streams"] if s["codec_type"] == "audio"]}
    json.dump(rep, open(os.path.join(E.out, "render_report.json"), "w"), indent=1)
    log(f"render: {rep}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("letter")
    ap.add_argument("--only", help="comma-separated stages: " + ",".join(STAGES))
    ap.add_argument("--skip", help="comma-separated stages to skip")
    ap.add_argument("--no-whisper", action="store_true")
    ap.add_argument("--reslice", action="store_true")
    ap.add_argument("--at", help="snapshot times, comma-separated")
    a = ap.parse_args()
    E = Episode(a.letter.upper() if len(a.letter) == 1 else a.letter)
    stages = a.only.split(",") if a.only else list(STAGES)
    if a.skip:
        stages = [s for s in stages if s not in a.skip.split(",")]
    tl_path = os.path.join(E.build, "timeline.json")
    timeline = json.load(open(tl_path)) if os.path.exists(tl_path) else None
    if "slice" in stages:
        stage_slice(E, a.reslice)
    if "tts" in stages or "timing" in stages or timeline is None:
        timeline = stage_timing(E)
    # cue resolution always runs (cheap, uses the Whisper cache); Whisper itself only in the whisper stage
    timeline = stage_whisper(E, timeline, enabled=not a.no_whisper, allow_run="whisper" in stages)
    if "mix" in stages or "timing" in stages or not os.path.exists(os.path.join(E.build, "mix.wav")):
        stage_mix(E, timeline)
    if "compose" in stages:
        stage_compose(E, timeline)
    if "lint" in stages:
        r = run(HF + ["lint", E.comp], check=False)
        print(r.stdout[-2500:], r.stderr[-1500:])
    if "snapshot" in stages:
        stage_snapshot(E, timeline, [float(x) for x in a.at.split(",")] if a.at else None)
    if "render" in stages:
        stage_render(E, timeline)
    for s in timeline["scenes"]:
        for g in s["segments"]:
            for tr in g.get("triggers", []):
                log(f"cue {tr['word']:10s} -> {tr['target']:7s} @ {tr['t']:.2f}s ({tr['src']})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""FaceCam Boost - dialogue mode: Tony + his IA avatar, from a tournage take and a [MOI]/[IA] script.

Tony films the whole script reading every line, IA lines included (prompteur).
This script:
  align  aligns the script on WORK/transcript.json (facecam_cut.py --stage transcribe)
         word by word - the prompteur timestamps of the session drift by seconds,
         the transcript does not
  tts    renders each IA line in Tony's cloned voice (n8n tts-gen webhook, charter s.5)
  build  three frame-exact tracks: tony.mp4 (MOI lines, frozen during IA), avatar.mp4
         (BUREAU bank, lips-active ranges only), voice.wav, + timeline.json

  python3 facecam_dialogue.py --src take.mp4 --script script.md --work build/ [--stage all]

script.md - the format Tony writes:
  [MOI — facecam]            a MOI block (a note after the dash is kept as block note;
  Si Claude te donne…         "accélération" in it speeds that block up)
  [IA — apparaît brusquement]
  « Peut-être que ton prompt est éclaté aussi. »
  [VISUEL : …]               ignored (a cue for the composition), speaker unchanged
  [BOUCLE → …]               end of the script: what follows is the loop line, not cut
"""
import argparse, difflib, json, os, re, shutil, subprocess, sys, time, unicodedata, urllib.request

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "ffmpeg"
FP = os.environ.get("FFPROBE") or shutil.which("ffprobe") or "ffprobe"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BANK = os.path.join(REPO, "autoboost-neon-videos", "_shared", "avatar-bank", "clips")
LIPS = {"C2_commente_motcle": (0.08, 4.83), "B1_principe": (0.08, 4.88), "A1_hook_frontal": (0.67, 4.58)}  # LIPS-MAP.md
ROT = ["C2_commente_motcle", "B1_principe", "A1_hook_frontal"]
TTS_URL = "https://n7n.automatisationboost.com/webhook/tts-gen"
VOIX = "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3"
FPS, SR, GAP = 30, 48000, 0.50
NUM = {"quinze": "15", "six": "6", "dix": "10", "douze": "12", "vingt": "20", "trente": "30", "cent": "100"}
ENC = ["-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-g", "30", "-r", "30",
       "-video_track_timescale", "30000"]


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print("\n".join(r.stderr.strip().splitlines()[-10:]), file=sys.stderr)
        raise SystemExit("ffmpeg failed: " + " ".join(args[:10]))


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())


# ------------------------------------------------------------------ script
def parse_script(path):
    lines, who, block, note = [], None, -1, ""
    for raw in open(path, encoding="utf-8"):
        s = raw.strip().replace("**", "")
        if not s:
            continue
        m = re.match(r"^\[(MOI|IA|VISUEL|BOUCLE)\b(.*?)\]?$", s, re.I)
        if m:
            kind = m.group(1).upper()
            if kind == "BOUCLE":
                break
            if kind in ("MOI", "IA"):
                who, block, note = kind.lower(), block + 1, m.group(2).strip(" —-:]").strip()
            continue
        if who is None:
            continue
        text = re.sub(r"[\U0001F300-\U0001FAFF☀-➿]", "", s).strip()
        if who == "ia":
            text = text.strip("«» ").strip()
        lines.append({"li": len(lines), "who": who, "block": block, "note": note, "text": text})
    return lines


def norm_tokens(word):
    w = unicodedata.normalize("NFKD", word.lower()).encode("ascii", "ignore").decode()
    return [NUM.get(t, t) for t in re.split(r"[^a-z0-9]+", w) if t]


def align(lines, transcript):
    asr = [w for seg in transcript for w in seg["words"]]
    words = [(L["li"], w) for L in lines for w in L["text"].split()]
    st, own = [], []
    for i, (_, w) in enumerate(words):
        for t in norm_tokens(w):
            st.append(t); own.append(i)
    at, atime = [], []
    for w in asr:
        toks = norm_tokens(w["w"]) or ["_"]
        span = (w["e"] - w["s"]) / len(toks)
        for k, t in enumerate(toks):
            at.append(t); atime.append((w["s"] + k * span, w["s"] + (k + 1) * span))
    tt = [None] * len(st)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, st, at, autojunk=False).get_opcodes():
        if op in ("equal", "replace") and j2 > j1:
            for k in range(i2 - i1):
                tt[i1 + k] = atime[j1 + min(j2 - j1 - 1, int(k * (j2 - j1) / (i2 - i1)))]
    times = [None] * len(words)
    for k, t in enumerate(tt):
        if t:
            i = own[k]
            times[i] = t if times[i] is None else (min(times[i][0], t[0]), max(times[i][1], t[1]))
    for i, t in enumerate(times):  # interpolate holes inside a line
        if t is None:
            li = words[i][0]
            p = next((times[j] for j in range(i - 1, -1, -1) if words[j][0] == li and times[j]), None)
            n = next((times[j] for j in range(i + 1, len(times)) if words[j][0] == li and times[j]), None)
            if p and n:
                times[i] = (p[1], max(p[1] + 0.05, n[0]))
    for L in lines:
        ws = [(w, times[i]) for i, (li, w) in enumerate(words) if li == L["li"]]
        if not any(t for _, t in ws):
            L.update(s=None, e=None, words=[]); continue
        last = max(i for i, (_, t) in enumerate(ws) if t)
        ws = [(w, t) for w, t in ws[:last + 1] if t]
        L.update(s=ws[0][1][0], e=ws[-1][1][1], words=[{"w": w, "s": t[0], "e": t[1]} for w, t in ws])
    return lines


# ------------------------------------------------------------------ IA voice
def f0_median(path):
    import numpy as np
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    f0 = []
    for i in range(0, len(x) - 640, 320):
        w = x[i:i + 640] * np.hanning(640)
        if np.sqrt((w ** 2).mean()) < 0.02:
            continue
        ac = np.correlate(w, w, "full")[639:]
        k = 53 + int(np.argmax(ac[53:228]))
        if ac[k] > 0.35 * ac[0]:
            f0.append(16000 / k)
    return float(np.median(f0)) if f0 else 0.0


def tts(lines, work):
    os.makedirs(os.path.join(work, "ia"), exist_ok=True)
    for L in (x for x in lines if x["who"] == "ia"):
        out = os.path.join(work, "ia", f"ia{L['li']:02d}.mp3")
        if os.path.exists(out) and os.path.getsize(out) > 1024:
            continue
        text = L["text"].replace('"', "").replace("«", "").replace("»", "").strip()  # raw JSON on the n8n side
        body = json.dumps({"text": text, "voixUrl": VOIX}).encode()
        for attempt in range(1, 5):
            try:
                req = urllib.request.Request(TTS_URL, data=body, headers={"content-type": "application/json",
                                                                          "user-agent": "curl/8.5.0"})  # Cloudflare 403s Python-urllib
                data = urllib.request.urlopen(req, timeout=240).read()
                if len(data) < 1024:
                    raise RuntimeError(f"{len(data)} octets")
                open(out, "wb").write(data)
                f = f0_median(out)
                if f > 170:
                    raise RuntimeError(f"F0 {f:.0f} Hz = repli OpenAI")
                print(f"ia{L['li']:02d} ok F0 {f:.0f} Hz  {text}", flush=True)
                break
            except Exception as e:  # noqa: BLE001
                print(f"ia{L['li']:02d} essai {attempt}/4 : {e}", flush=True)
                if os.path.exists(out):
                    os.remove(out)
                time.sleep(4 * attempt)
        else:
            raise SystemExit(f"ia{L['li']:02d} : échec")


# ------------------------------------------------------------------ build
def build(src, lines, work, tempo, fast):
    out = os.path.join(work, "asm"); os.makedirs(out, exist_ok=True)
    src_voice = os.path.join(out, "src_voice.wav")
    if not os.path.exists(src_voice):  # light denoise + ONE two-pass loudnorm over the whole take
        pre = "highpass=f=70,afftdn=nr=8:nf=-42"
        r = subprocess.run([FF, "-nostdin", "-i", src, "-vn", "-af", pre + ",loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                            "-f", "null", "-"], capture_output=True, text=True)
        m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
        ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
              f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
        run([FF, "-nostdin", "-v", "error", "-i", src, "-vn", "-af", pre + "," + ln, "-ar", str(SR), "-ac", "1", src_voice, "-y"])

    items, i = [], 0
    while i < len(lines):
        L = lines[i]
        if L["who"] == "ia":
            items.append({"kind": "ia", "line": L}); i += 1; continue
        runl = []
        while i < len(lines) and lines[i]["who"] == "moi":
            if lines[i]["words"]:
                runl.append(lines[i])
            i += 1
        if not runl:
            continue
        pia = next((x for x in reversed(lines[:runl[0]["li"]]) if x["who"] == "ia" and x["e"]), None)
        nia = next((x for x in lines[runl[-1]["li"] + 1:] if x["who"] == "ia" and x["s"]), None)
        lo, hi = (pia["e"] + 0.03 if pia else 0.0), (nia["s"] - 0.03 if nia else 1e9)
        ws = [dict(w, li=R["li"], block=R["block"], note=R["note"]) for R in runl for w in R["words"]]
        ph, cur = [], [ws[0]]
        for a, b in zip(ws, ws[1:]):
            if b["s"] - a["e"] > GAP or b["block"] != a["block"]:
                ph.append(cur); cur = []
            cur.append(b)
        ph.append(cur)
        for p in ph:
            items.append({"kind": "moi", "cin": max(lo, p[0]["s"] - 0.10), "cout": min(hi, p[-1]["e"] + 0.14),
                          "tempo": fast if "accél" in p[0]["note"].lower() else tempo, "words": p,
                          "block": p[0]["block"], "note": p[0]["note"]})

    lists, frames, rot, timeline, last = {"tony": [], "avatar": [], "voice": []}, 0, 0, [], None
    for k, it in enumerate(items):
        tv, av, vo = (os.path.join(out, f"{x}{k:03d}.{e}") for x, e in (("t", "mp4"), ("a", "mp4"), ("v", "wav")))
        if it["kind"] == "moi":
            N = round((it["cout"] - it["cin"]) / it["tempo"] * FPS)
            run([FF, "-nostdin", "-v", "error", "-ss", f"{it['cin']:.3f}", "-i", src, "-an", "-vf",
                 f"setpts=(PTS-STARTPTS)/{it['tempo']},fps={FPS},format=yuv420p", "-frames:v", str(N), *ENC, tv, "-y"])
            run([FF, "-nostdin", "-v", "error", "-ss", f"{it['cin']:.3f}", "-t", f"{it['cout'] - it['cin'] + 0.3:.3f}", "-i", src_voice,
                 "-af", f"atempo={it['tempo']},apad,atrim=end_sample={N * SR // FPS}", "-ar", str(SR), "-ac", "1", vo, "-y"])
            run([FF, "-nostdin", "-v", "error", "-f", "lavfi", "-i", f"color=black:s=720x1280:r={FPS}", "-frames:v", str(N), *ENC, av, "-y"])
            last, start = tv, frames / FPS
            timeline.append({"k": k, "kind": "moi", "block": it["block"], "note": it["note"], "start": round(start, 4), "frames": N,
                             "dur": round(N / FPS, 4), "words": [{"w": w["w"], "li": w["li"],
                             "s": round(start + (w["s"] - it["cin"]) / it["tempo"], 3),
                             "e": round(start + (w["e"] - it["cin"]) / it["tempo"], 3)} for w in it["words"]]})
        else:
            L = it["line"]
            wav = os.path.join(out, f"ia{L['li']:02d}.wav")
            run([FF, "-nostdin", "-v", "error", "-i", os.path.join(work, "ia", f"ia{L['li']:02d}.mp3"), "-af",
                 "highpass=f=110,lowpass=f=9000,aecho=0.85:0.5:9:0.14,loudnorm=I=-16:TP=-1.5:LRA=9", "-ar", str(SR), "-ac", "1", wav, "-y"])
            dv = dur(wav)
            N = round((0.12 + dv + 0.20) * FPS)
            png = os.path.join(out, f"freeze{k:03d}.png")
            run([FF, "-nostdin", "-v", "error", "-sseof", "-0.1", "-i", last, "-frames:v", "1", "-update", "1", png, "-y"])
            run([FF, "-nostdin", "-v", "error", "-loop", "1", "-i", png, "-vf", f"fps={FPS},format=yuv420p", "-frames:v", str(N), *ENC, tv, "-y"])
            run([FF, "-nostdin", "-v", "error", "-i", wav, "-af", f"adelay=120,apad,atrim=end_sample={N * SR // FPS}",
                 "-ar", str(SR), "-ac", "1", vo, "-y"])
            shots, left = [], N
            while left > 0:
                clip = ROT[rot % len(ROT)]; rot += 1
                z0, z1 = LIPS[clip]
                n = min(left, int((z1 - z0) * FPS) - 1)
                if left - n < 12 and left > n:
                    n = left // 2
                shots.append((clip, z0 + max(0.0, ((z1 - z0) - n / FPS) / 2), n)); left -= n
            parts = []
            for j, (clip, ss, n) in enumerate(shots):
                pth = os.path.join(out, f"a{k:03d}_{j}.mp4")
                run([FF, "-nostdin", "-v", "error", "-ss", f"{ss:.3f}", "-i", os.path.join(BANK, clip + ".mp4"), "-an",
                     "-vf", f"fps={FPS},scale=720:1280,format=yuv420p", "-frames:v", str(n), *ENC, pth, "-y"])
                parts.append(pth)
            open(av + ".txt", "w").write("".join(f"file '{p}'\n" for p in parts))
            run([FF, "-nostdin", "-v", "error", "-f", "concat", "-safe", "0", "-i", av + ".txt", "-c", "copy", av, "-y"])
            timeline.append({"k": k, "kind": "ia", "li": L["li"], "block": L["block"], "note": L["note"], "text": L["text"],
                             "start": round(frames / FPS, 4), "frames": N, "dur": round(N / FPS, 4), "voice_at": 0.12,
                             "voice_dur": round(dv, 3), "shots": [{"clip": c, "ss": round(s, 3), "frames": n} for c, s, n in shots]})
        for key, p in (("tony", tv), ("avatar", av), ("voice", vo)):
            lists[key].append(p)
        frames += N
    for key, ext in (("tony", "mp4"), ("avatar", "mp4"), ("voice", "wav")):
        lst = os.path.join(out, f"{key}.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in lists[key]))
        run([FF, "-nostdin", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", os.path.join(out, f"{key}.{ext}"), "-y"])
    json.dump({"frames": frames, "total": round(frames / FPS, 4), "items": timeline},
              open(os.path.join(out, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{len(items)} éléments, {frames} images = {frames / FPS:.2f} s -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--stage", default="all", choices=["all", "align", "tts", "build"])
    ap.add_argument("--tempo", type=float, default=1.10)
    ap.add_argument("--fast", type=float, default=1.18, help="tempo for blocks noted 'accélération'")
    a = ap.parse_args()
    lines = parse_script(a.script)
    lines = align(lines, json.load(open(os.path.join(a.work, "transcript.json"))))
    json.dump(lines, open(os.path.join(a.work, "aligned.json"), "w"), ensure_ascii=False, indent=1)
    for L in lines:
        span = "   (non entendu)   " if L["s"] is None else f"{L['s']:7.2f} -> {L['e']:7.2f}"
        print(f"{L['li']:>2} {L['who']:3} b{L['block']:<2} {span}  {L['text']}")
    if a.stage in ("all", "tts"):
        tts(lines, a.work)
    if a.stage in ("all", "build"):
        build(a.src, lines, a.work, a.tempo, a.fast)

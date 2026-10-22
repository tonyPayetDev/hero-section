#!/usr/bin/env python3
"""Cloned voice for every line of a duo script, straight from WaveSpeed (qwen3-tts voice-clone).

  WAVESPEED_API_KEY=... python3 tts_wavespeed.py session/script.json OUT_DIR [--ref URL]

script.json: {"lines": [["moi"|"ia", "text", ...], ...]}  ->  OUT_DIR/l00.mp3, l01.mp3, ...
The key comes from the environment only (never written in a file of the repo). Lines already present are kept.
Checks the median F0 of each file: Tony's clone sits at 110-135 Hz; ~200 Hz means a wrong voice.
"""
import argparse, json, os, subprocess, time, urllib.request

REF = ("https://raw.githubusercontent.com/tonyPayetDev/hero-section/claude/top-3-anime-women-1ewnco/"
       "autoboost-neon-videos/_shared/voix/reference-tony.mp3")
API = "https://api.wavespeed.ai/api/v3"
ap = argparse.ArgumentParser()
ap.add_argument("script"); ap.add_argument("out"); ap.add_argument("--ref", default=REF)
a = ap.parse_args()
KEY = os.environ.get("WAVESPEED_API_KEY") or exit("WAVESPEED_API_KEY manquant (variable d'environnement)")
H = {"Authorization": f"Bearer {KEY}", "content-type": "application/json", "user-agent": "curl/8.5.0"}


def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def f0(path):
    import numpy as np
    x = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]), np.float32)
    out = []
    for i in range(0, len(x) - 1024, 512):
        fr = x[i:i + 1024]
        if np.sqrt((fr ** 2).mean()) < 0.02:
            continue
        ac = np.correlate(fr, fr, "full")[1023:]
        lo, hi = 16000 // 300, 16000 // 70
        lag = lo + int(np.argmax(ac[lo:hi]))
        out.append(16000 / lag)
    return float(np.median(out)) if out else 0.0


os.makedirs(a.out, exist_ok=True)
for i, line in enumerate(json.load(open(a.script))["lines"]):
    out = os.path.join(a.out, f"l{i:02d}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 1024:
        continue
    text = line[1].replace('"', "").replace("«", "").replace("»", "").strip()
    pid = call(f"{API}/wavespeed-ai/qwen3-tts/voice-clone", {"text": text, "audio": a.ref, "language": "French"})["data"]["id"]
    for _ in range(150):
        time.sleep(2)
        d = call(f"{API}/predictions/{pid}/result")["data"]
        if d["status"] == "completed":
            urllib.request.urlretrieve(d["outputs"][0], out)
            break
        if d["status"] == "failed":
            raise SystemExit(f"l{i:02d}: {d.get('error')}")
    else:
        raise SystemExit(f"l{i:02d}: délai dépassé")
    print(f"l{i:02d} F0 {f0(out):.0f} Hz  {text[:60]}", flush=True)

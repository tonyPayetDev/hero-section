#!/usr/bin/env python3
"""IA lines -> cloned voice via the n8n tts-gen webhook (charter section 5).

4 attempts per line, files under 1 KB rejected, F0 median measured: 114-133 Hz is
Tony's clone, ~200 Hz means the OpenAI fallback answered -> retried.
"""
import json, os, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ia")
os.makedirs(OUT, exist_ok=True)
FF = "/tmp/claude-0/-home-user-hero-section/25c114f9-7c32-5b84-b3ea-354b9cf49fbf/scratchpad/bin/ffmpeg"
URL = "https://n7n.automatisationboost.com/webhook/tts-gen"
VOIX = "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3"

# text is injected raw into a JSON body on the n8n side: no straight double quotes
LINES = {
    2: "Peut-être que ton prompt est éclaté aussi.",
    4: "Oui, ça c'est ta technique depuis six mois.",
    6: "Attends… tu vas vraiment nous faire nous battre entre nous ?",
    9: "Donc réunion Teams… mais sans Gérard qui parle pendant quarante-cinq minutes.",
    11: "Attends… éliminent ?",
    13: "J'espère.",
    15: "Donc maintenant, même mes réponses ont des entretiens d'embauche.",
    17: "Ah… donc tu vas arrêter de m'écrire encore mieux, douze fois ?",
    19: "Enfin.",
    21: "Et évidemment, tu ne vas pas mettre le lien directement dans la vidéo…",
    23: "Et follow-le… sinon il va encore venir se plaindre à moi.",
    25: "Maintenant, laisse-moi tranquille.",
}


def f0_median(path):
    import numpy as np
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    fr, hop, f0s = 640, 320, []
    for i in range(0, len(x) - fr, hop):
        w = x[i:i + fr] * np.hanning(fr)
        if np.sqrt((w ** 2).mean()) < 0.02:
            continue
        ac = np.correlate(w, w, "full")[fr - 1:]
        lo, hi = 16000 // 300, 16000 // 70
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.35 * ac[0]:
            f0s.append(16000 / k)
    return float(np.median(f0s)) if f0s else 0.0


def tts(n, text):
    out = os.path.join(OUT, f"ia{n:02d}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 1024:
        return out
    body = json.dumps({"text": text, "voixUrl": VOIX}).encode()
    for attempt in range(1, 5):
        try:
            req = urllib.request.Request(URL, data=body, headers={"content-type": "application/json", "user-agent": "curl/8.5.0"})
            data = urllib.request.urlopen(req, timeout=240).read()
            if len(data) < 1024:
                raise RuntimeError(f"{len(data)} octets")
            open(out, "wb").write(data)
            f0 = f0_median(out)
            if f0 > 170:
                raise RuntimeError(f"F0 {f0:.0f} Hz: repli OpenAI")
            print(f"ia{n:02d} ok  {len(data)/1024:.0f} Ko  F0 {f0:.0f} Hz  « {text} »", flush=True)
            return out
        except Exception as e:  # noqa: BLE001
            print(f"ia{n:02d} essai {attempt}/4 : {e}", flush=True)
            if os.path.exists(out):
                os.remove(out)
            time.sleep(4 * attempt)
    raise SystemExit(f"ia{n:02d} : échec après 4 essais")


for n, text in LINES.items():
    tts(n, text)
print("toutes les répliques IA sont prêtes")

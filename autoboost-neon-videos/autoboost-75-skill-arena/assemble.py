#!/usr/bin/env python3
"""Skill Arena - align Tony's script on the take, then assemble three frame-exact tracks.

  tony.mp4    1080x1440: his MOI lines (silences cut, tempo), frozen on his last
              frame while the IA speaks
  avatar.mp4  720x1280: the BUREAU avatar during IA lines (lips-active ranges only),
              black elsewhere
  voice.wav   his voice on MOI lines, the cloned IA voice on IA lines
  timeline.json  items + caption words (script text, aligned timings)

Tony read the IA lines himself in the take: the script alignment tells which of
his words are IA lines, and those spans are dropped from his track.
"""
import difflib, json, os, re, subprocess, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "video.mp4")
OUT = os.path.join(HERE, "asm")
os.makedirs(OUT, exist_ok=True)
SP = "/tmp/claude-0/-home-user-hero-section/25c114f9-7c32-5b84-b3ea-354b9cf49fbf/scratchpad"
FF, FP = f"{SP}/bin/ffmpeg", f"{SP}/bin/ffprobe"
BANK = "/home/user/hero-section/autoboost-neon-videos/_shared/avatar-bank/clips"
FPS = 30
TEMPO, TEMPO_FAST = 1.10, 1.18
GAP = 0.50

# (who, text, tag) - Tony's script, the truth for captions
S = [
 ("moi", "Si Claude te donne encore une réponse éclatée…", "hook"),
 ("ia", "Peut-être que ton prompt est éclaté aussi.", 2),
 ("moi", "Merci. Personne t'a demandé ton avis.", ""),
 ("moi", "Bref.", ""),
 ("moi", "Au lieu de redemander quinze fois à Claude :", "redemande"),
 ("moi", "« améliore ça… »", "redemande"),
 ("moi", "« recommence… »", "redemande"),
 ("moi", "« sois plus intelligent… »", "redemande"),
 ("ia", "Oui, ça c'est ta technique depuis six mois.", 4),
 ("moi", "…tu peux faire combattre plusieurs versions de Claude sur le même problème.", "arena"),
 ("moi", "Ça s'appelle Skill Arena.", "arena"),
 ("ia", "Attends… tu vas vraiment nous faire nous battre entre nous ?", 6),
 ("moi", "Exactement.", "flow"),
 ("moi", "Tu donnes une seule tâche.", "flow"),
 ("moi", "Et l'Arena lance une armée de sous-agents.", "flow"),
 ("moi", "Certains cherchent la solution la plus simple.", "agents"),
 ("moi", "D'autres cherchent les failles.", "agents"),
 ("moi", "D'autres testent une stratégie complètement différente.", "agents"),
 ("ia", "Donc réunion Teams… mais sans Gérard qui parle pendant 45 minutes.", 9),
 ("moi", "Exactement.", "duel"),
 ("moi", "Ensuite, les réponses sont comparées.", "duel"),
 ("moi", "Les agents se critiquent.", "duel"),
 ("moi", "Ils éliminent les solutions les plus faibles.", "duel"),
 ("ia", "Attends… éliminent ?", 11),
 ("moi", "Façon de parler.", "duel"),
 ("ia", "J'espère.", 13),
 ("moi", "Et à la fin…", "fast"),
 ("moi", "au lieu d'avoir la première réponse que Claude a trouvée…", "fast"),
 ("moi", "tu récupères une réponse qui a été :", "fast"),
 ("moi", "challengée, comparée et améliorée.", "fast"),
 ("ia", "Donc maintenant même mes réponses ont des entretiens d'embauche.", 15),
 ("moi", "Bienvenue en 2026.", "lance"),
 ("moi", "Et le meilleur ?", "lance"),
 ("moi", "Quand une réponse ne me plaît pas…", "lance"),
 ("moi", "je ne passe plus dix minutes à reformuler mon prompt.", "lance"),
 ("moi", "Je lance l'Arena.", "lance"),
 ("ia", "Ah… donc tu vas arrêter de m'écrire « encore mieux » douze fois ?", 17),
 ("moi", "Oui.", "lance"),
 ("ia", "Enfin.", 19),
 ("moi", "Pour l'installer, tu colles le lien dans Claude…", "install"),
 ("moi", "puis tu lui donnes simplement le prompt d'installation.", "install"),
 ("ia", "Et évidemment tu ne vas pas mettre le lien directement dans la vidéo…", 21),
 ("moi", "Évidemment que non.", "cta"),
 ("moi", "Si tu veux le lien + le prompt prêt à copier-coller :", "cta"),
 ("moi", "commente ARENA sous la vidéo.", "cta"),
 ("ia", "Et follow-le… sinon il va encore venir se plaindre à moi.", 23),
 ("moi", "Commente ARENA, follow le compte…", "cta"),
 ("moi", "et je te l'envoie.", "cta"),
 ("ia", "Maintenant laisse-moi tranquille.", 25),
 ("moi", "Jusqu'à la prochaine Arena.", "fin"),
]
NUM = {"quinze": "15", "six": "6", "dix": "10", "douze": "12"}


def norm_tokens(word):
    w = unicodedata.normalize("NFKD", word.lower()).encode("ascii", "ignore").decode()
    toks = [t for t in re.split(r"[^a-z0-9]+", w) if t]
    return [NUM.get(t, t) for t in toks]


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print("\n".join(r.stderr.strip().splitlines()[-10:]), file=sys.stderr)
        raise SystemExit("ffmpeg failed: " + " ".join(args[:10]))


def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())


def align(script_words, asr_words):
    """script_words: [str]; asr_words: [{w,s,e}] -> per script word (s, e) or None."""
    st, s_owner = [], []
    for i, w in enumerate(script_words):
        for t in norm_tokens(w):
            st.append(t); s_owner.append(i)
    at, a_time = [], []
    for w in asr_words:
        toks = norm_tokens(w["w"]) or ["_"]
        span = (w["e"] - w["s"]) / len(toks)
        for k, t in enumerate(toks):
            at.append(t); a_time.append((w["s"] + k * span, w["s"] + (k + 1) * span))
    tok_time = [None] * len(st)
    sm = difflib.SequenceMatcher(None, st, at, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace"):
            n, m = i2 - i1, j2 - j1
            for k in range(n):
                jj = j1 + min(m - 1, int(k * m / n)) if m else None
                if jj is not None:
                    tok_time[i1 + k] = a_time[jj]
    out = [None] * len(script_words)
    for k, tt in enumerate(tok_time):
        if tt is None:
            continue
        i = s_owner[k]
        out[i] = (tt[0], tt[1]) if out[i] is None else (min(out[i][0], tt[0]), max(out[i][1], tt[1]))
    return out


# ------------------------------------------------------------------ align the take
asr = [w for seg in json.load(open(os.path.join(HERE, "build", "transcript.json"))) for w in seg["words"]]
words = []  # (line index, word)
for li, (_, text, _) in enumerate(S):
    for w in text.split():
        words.append((li, w))
times = align([w for _, w in words], asr)
# fill gaps inside a line by interpolation between known neighbours
for i, t in enumerate(times):
    if t is None:
        li = words[i][0]
        prev = next((times[j] for j in range(i - 1, -1, -1) if words[j][0] == li and times[j]), None)
        nxt = next((times[j] for j in range(i + 1, len(times)) if words[j][0] == li and times[j]), None)
        if prev and nxt:
            times[i] = (prev[1], nxt[0]) if nxt[0] > prev[1] else (prev[1], prev[1] + 0.05)
lines = []
for li, (who, text, tag) in enumerate(S):
    ws = [(w, times[i]) for i, (l, w) in enumerate(words) if l == li]
    timed = [(w, t) for w, t in ws if t]
    if not timed:
        lines.append({"li": li, "who": who, "text": text, "tag": tag, "s": None, "e": None, "words": []})
        continue
    # drop untimed trailing words (said differently, e.g. "prochaine Arena" -> "prochaine")
    last = max(i for i, (w, t) in enumerate(ws) if t)
    ws = ws[:last + 1]
    lines.append({"li": li, "who": who, "text": text, "tag": tag, "s": timed[0][1][0], "e": timed[-1][1][1],
                  "words": [{"w": w, "s": t[0], "e": t[1]} for w, t in ws if t]})
for L in lines:
    span = "   (non entendu)   " if L["s"] is None else f"{L['s']:7.2f} -> {L['e']:7.2f}"
    print(f"{L['li']:>2} {L['who']:3} {span}  {L['text']}")
json.dump(lines, open(os.path.join(OUT, "aligned.json"), "w"), ensure_ascii=False, indent=1)

# ================================================================== build (python3 assemble.py --build)
if "--build" not in sys.argv:
    sys.exit(0)

IA_DIR = os.path.join(HERE, "ia")
LIPS = {"C2_commente_motcle": (0.08, 4.83), "B1_principe": (0.08, 4.88), "A1_hook_frontal": (0.67, 4.58)}
ROT = ["C2_commente_motcle", "B1_principe", "A1_hook_frontal"]
SR = 48000
ENC = ["-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-g", "30",
       "-r", "30", "-video_track_timescale", "30000"]

# ---- the take's voice: light denoise, then ONE two-pass loudnorm over the whole take
src_voice = os.path.join(OUT, "src_voice.wav")
if not os.path.exists(src_voice):
    pre = "highpass=f=70,afftdn=nr=8:nf=-42"
    r = subprocess.run([FF, "-nostdin", "-i", SRC, "-vn", "-af", pre + ",loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run([FF, "-nostdin", "-v", "error", "-i", SRC, "-vn", "-af", pre + "," + ln, "-ar", str(SR), "-ac", "1", src_voice, "-y"])

# ---- the IA voice: same level, a touch of "digital" colour so it reads as the avatar
def ia_voice(n):
    out = os.path.join(OUT, f"ia{n:02d}.wav")
    if not os.path.exists(out):
        run([FF, "-nostdin", "-v", "error", "-i", os.path.join(IA_DIR, f"ia{n:02d}.mp3"), "-af",
             "highpass=f=110,lowpass=f=9000,aecho=0.85:0.5:9:0.14,loudnorm=I=-16:TP=-1.5:LRA=9",
             "-ar", str(SR), "-ac", "1", out, "-y"])
    return out

# ---- items, in script order
items, i = [], 0
ia_lines = [L for L in lines if L["who"] == "ia"]
while i < len(lines):
    L = lines[i]
    if L["who"] == "ia":
        items.append({"kind": "ia", "line": L}); i += 1; continue
    run_lines = []
    while i < len(lines) and lines[i]["who"] == "moi":
        run_lines.append(lines[i]); i += 1
    prev_ia = next((x for x in reversed(lines[:run_lines[0]["li"]]) if x["who"] == "ia" and x["e"]), None)
    next_ia = next((x for x in lines[run_lines[-1]["li"] + 1:] if x["who"] == "ia" and x["s"]), None)
    lo = prev_ia["e"] + 0.03 if prev_ia else 0.0
    hi = next_ia["s"] - 0.03 if next_ia else 10_000
    ws = [dict(w, li=R["li"], tag=R["tag"]) for R in run_lines for w in R["words"]]
    ph, cur = [], [ws[0]]
    for a, b in zip(ws, ws[1:]):
        if b["s"] - a["e"] > GAP:
            ph.append(cur); cur = []
        cur.append(b)
    ph.append(cur)
    for p in ph:
        cin, cout = max(lo, p[0]["s"] - 0.10), min(hi, p[-1]["e"] + 0.14)
        tempo = TEMPO_FAST if any(w["tag"] == "fast" for w in p) else TEMPO
        items.append({"kind": "moi", "cin": round(cin, 3), "cout": round(cout, 3), "tempo": tempo, "words": p,
                      "tag": p[0]["tag"], "lis": sorted({w["li"] for w in p})})

# ---- encode every item to an exact frame count, the three tracks in lockstep
lists = {"tony": [], "avatar": [], "voice": []}
t_frames, rot, timeline = 0, 0, []
last_tony = None
for k, it in enumerate(items):
    tv, av, vo = (os.path.join(OUT, f"{x}{k:03d}.{e}") for x, e in (("t", "mp4"), ("a", "mp4"), ("v", "wav")))
    if it["kind"] == "moi":
        N = round((it["cout"] - it["cin"]) / it["tempo"] * FPS)
        run([FF, "-nostdin", "-v", "error", "-ss", f"{it['cin']:.3f}", "-i", SRC, "-an",
             "-vf", f"setpts=(PTS-STARTPTS)/{it['tempo']},fps={FPS},format=yuv420p", "-frames:v", str(N), *ENC, tv, "-y"])
        run([FF, "-nostdin", "-v", "error", "-ss", f"{it['cin']:.3f}", "-t", f"{it['cout'] - it['cin'] + 0.3:.3f}", "-i", src_voice,
             "-af", f"atempo={it['tempo']},apad,atrim=end_sample={N * SR // FPS}", "-ar", str(SR), "-ac", "1", vo, "-y"])
        run([FF, "-nostdin", "-v", "error", "-f", "lavfi", "-i", f"color=black:s=720x1280:r={FPS}", "-frames:v", str(N), *ENC, av, "-y"])
        last_tony = tv
        start = t_frames / FPS
        caps = [{"w": w["w"], "li": w["li"], "s": round(start + (w["s"] - it["cin"]) / it["tempo"], 3),
                 "e": round(start + (w["e"] - it["cin"]) / it["tempo"], 3)} for w in it["words"]]
        timeline.append({"k": k, "kind": "moi", "tag": it["tag"], "lis": it["lis"], "start": round(start, 4), "frames": N,
                         "dur": round(N / FPS, 4), "words": caps})
    else:
        L = it["line"]
        wav = ia_voice(L["tag"])
        d_voice = dur(wav)
        N = round((0.12 + d_voice + 0.20) * FPS)
        png = os.path.join(OUT, f"freeze{k:03d}.png")
        run([FF, "-nostdin", "-v", "error", "-sseof", "-0.1", "-i", last_tony, "-frames:v", "1", "-update", "1", png, "-y"])
        run([FF, "-nostdin", "-v", "error", "-loop", "1", "-i", png, "-vf", f"fps={FPS},format=yuv420p", "-frames:v", str(N), *ENC, tv, "-y"])
        run([FF, "-nostdin", "-v", "error", "-i", wav, "-af", f"adelay=120,apad,atrim=end_sample={N * SR // FPS}",
             "-ar", str(SR), "-ac", "1", vo, "-y"])
        # avatar: every shot sits entirely inside a lips-active range (LIPS-MAP.md)
        shots, left = [], N
        while left > 0:
            clip = ROT[rot % len(ROT)]; rot += 1
            z0, z1 = LIPS[clip]
            n = min(left, int((z1 - z0) * FPS) - 1)
            if left - n < 12 and left > n:      # never leave a sliver shot under 0.4 s
                n = left // 2
            ss = z0 + max(0.0, ((z1 - z0) - n / FPS) / 2)
            shots.append((clip, ss, n)); left -= n
        parts = []
        for j, (clip, ss, n) in enumerate(shots):
            pth = os.path.join(OUT, f"a{k:03d}_{j}.mp4")
            run([FF, "-nostdin", "-v", "error", "-ss", f"{ss:.3f}", "-i", os.path.join(BANK, clip + ".mp4"), "-an",
                 "-vf", f"fps={FPS},scale=720:1280,format=yuv420p", "-frames:v", str(n), *ENC, pth, "-y"])
            parts.append(pth)
        open(av + ".txt", "w").write("".join(f"file '{p}'\n" for p in parts))
        run([FF, "-nostdin", "-v", "error", "-f", "concat", "-safe", "0", "-i", av + ".txt", "-c", "copy", av, "-y"])
        timeline.append({"k": k, "kind": "ia", "tag": L["tag"], "li": L["li"], "text": L["text"], "start": round(t_frames / FPS, 4),
                         "frames": N, "dur": round(N / FPS, 4), "voice_at": 0.12, "voice_dur": round(d_voice, 3),
                         "shots": [{"clip": c, "ss": round(s, 3), "frames": n} for c, s, n in shots]})
    for key, p in (("tony", tv), ("avatar", av), ("voice", vo)):
        lists[key].append(p)
    t_frames += N

for key, ext in (("tony", "mp4"), ("avatar", "mp4"), ("voice", "wav")):
    lst = os.path.join(OUT, f"{key}.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in lists[key]))
    run([FF, "-nostdin", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
         os.path.join(OUT, f"{key}.{ext}"), "-y"])
json.dump({"frames": t_frames, "total": round(t_frames / FPS, 4), "items": timeline},
          open(os.path.join(OUT, "timeline.json"), "w"), ensure_ascii=False, indent=1)
print(f"{len(items)} éléments, {t_frames} images = {t_frames / FPS:.2f} s")
for x in (os.path.join(OUT, f) for f in ("tony.mp4", "avatar.mp4", "voice.wav")):
    print(f"  {os.path.basename(x)} {dur(x):.3f}s")

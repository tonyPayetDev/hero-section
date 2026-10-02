#!/usr/bin/env python3
"""Cut plan + caption text + visual beat grid for autoboost-74.

Two independent grids:
  * cuts  - built on silences > GAP_SPLIT; removes dead air, creates jump cuts.
  * beats - a visual change every 2-4s (zoom step, keyword pop, b-roll), so a
            long uncut phrase still respects the yapping pattern-interrupt rule.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/tmp/claude-0/-home-user-hero-section/25c114f9-7c32-5b84-b3ea-354b9cf49fbf/scratchpad"
GAP_SPLIT = 0.55
PAD_IN, PAD_OUT = 0.10, 0.14
TEMPO = 1.14
BEAT_MAX = 3.6        # s - a visual beat may never be longer than this

FIXES = {
    (3, 6): "pas", (5, 3): "CLAUDE", (5, 4): ".md", (6, 1): "simple,",
    (6, 6): "Opus.", (7, 10): "clou.", (9, 6): "Commente", (9, 7): "TOKEN",
    (9, 9): "je", (9, 10): "t'envoie",
}
DROP = {(10, 5), (10, 6)}

def join(ws):
    out = ""
    for w in ws:
        if out and not re.match(r"^['\-.,!?]", w):
            out += " "
        out += w
    return out

segs = json.load(open(os.path.join(SCRATCH, "transcript_med.json")))
words = []
for si, s in enumerate(segs):
    for wi, w in enumerate(s["words"]):
        if (si, wi) in DROP:
            continue
        words.append({"w": FIXES.get((si, wi), w["w"]), "s": w["s"], "e": w["e"]})

# Whisper splits "sous-agents" and "peut-etre" into two tokens; merged here so
# the word-by-word highlight lands on whole words.
merged_w = [words[0]]
for w in words[1:]:
    if re.match(r"^['\-.]", w["w"]):
        merged_w[-1] = {"w": merged_w[-1]["w"] + w["w"], "s": merged_w[-1]["s"], "e": w["e"]}
    else:
        merged_w.append(w)
words = merged_w

phrases, cur = [], [words[0]]
for prev, w in zip(words, words[1:]):
    if w["s"] - prev["e"] > GAP_SPLIT:
        phrases.append(cur); cur = []
    cur.append(w)
phrases.append(cur)

plan, t = [], 0.0
for i, ph in enumerate(phrases):
    a, b = max(0.0, ph[0]["s"] - PAD_IN), ph[-1]["e"] + PAD_OUT
    ws = [{"w": w["w"], "s": round((w["s"]-a)/TEMPO + t, 3), "e": round((w["e"]-a)/TEMPO + t, 3)} for w in ph]
    plan.append({"i": i, "src_in": round(a, 3), "src_out": round(b, 3),
                 "out_start": round(t, 3), "dur": round((b-a)/TEMPO, 3),
                 "text": join([w["w"] for w in ph]), "words": ws})
    t += (b - a) / TEMPO
TOTAL = t

# --- beat grid -------------------------------------------------------------
# A beat starts at every cut, at every sentence end, and is force-split so no
# beat ever runs longer than BEAT_MAX.
marks = set()
for p in plan:
    marks.add(round(p["out_start"], 2))
    for w in p["words"]:
        if re.search(r"[.!?,]$", w["w"]):
            marks.add(round(w["e"], 2))
marks = sorted(m for m in marks if 0.0 <= m < TOTAL - 0.4)

BEAT_MIN = 0.8        # s - two marks closer than this are the same beat
merged = []
for m in marks:
    if not merged or m - merged[-1] >= BEAT_MIN:
        merged.append(m)

beats = []
for a, b in zip(merged, merged[1:] + [TOTAL]):
    n = max(1, round((b - a) / BEAT_MAX + 0.49))
    step = (b - a) / n
    beats.extend(round(a + k*step, 3) for k in range(n))
beats = sorted(set(beats))

json.dump({"total": round(TOTAL, 3), "tempo": TEMPO, "plan": plan, "beats": beats},
          open(os.path.join(HERE, "plan.json"), "w"), ensure_ascii=False, indent=1)

print(f"{len(plan)} coupes | {len(beats)} battements | duree {TOTAL:.2f}s (tempo {TEMPO})\n")
for p in plan:
    print(f"coupe {p['i']} [{p['out_start']:>5.2f} +{p['dur']:>5.2f}]  {p['text']}")
print("\nbattements:", " ".join(f"{b:.1f}" for b in beats))
worst = max(b2-b1 for b1, b2 in zip(beats, beats[1:] + [TOTAL]))
print(f"plus long battement sans changement : {worst:.2f}s")

#!/usr/bin/env python3
"""Builds captions.ass: word-by-word captions in the bottom band plus the
top-band keyword that changes at every section (the pattern interrupt)."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "plan_actual.json")))
TOTAL = P["total"]

INK, GOLD, VIOLET, SHADOW = "&H00EDEDED", "&H0008B3EA", "&H00F65C8B", "&H000F0A0A"
MAXCHARS = 26

# top band: what the viewer reads while he talks. Times follow the real word
# timings in plan_actual.json.
POPS = [
    (0.20,  3.77, "UN SIMPLE FICHIER"),
    (3.77,  8.70, "TA LIMITE DE TOKENS"),
    (8.70, 13.00, "MAUVAISE QUESTION"),
    (13.00, 15.00, "QUEL MODÈLE ?"),
    (15.00, 18.90, "CLAUDE.md"),
    (18.90, 20.90, "DES SOUS-AGENTS"),
    (20.90, 23.00, "SIMPLE → MODÈLE LÉGER"),
    (23.00, 24.60, "COMPLEXE → OPUS"),
    (24.60, 28.40, "PAS DE BAZOOKA"),
    (28.40, 33.30, "MOINS DE TOKENS"),
    (33.30, TOTAL, "COMMENTE : TOKEN"),
]
# words the caption line puts in gold even when they are not the active word
KEY = {"CLAUDE.md", "CLAUDE", ".md", "sous-agents.", "Opus.", "TOKEN", "tokens", "token",
       "Commente", "clou.", "Astra,", "fichier."}

def ts(t):
    t = max(0.0, t)
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

def esc(s):
    return s.replace("{", "(").replace("}", ")")

def glue(parts, words):
    """Rejoins rendered words, keeping apostrophes and hyphens tight."""
    out = ""
    for part, w in zip(parts, words):
        if out and not re.match(r"^['\-.,!?]", w):
            out += " "
        out += part
    return out

def cont(w):
    """A token that must stay glued to the one before it."""
    return bool(re.match(r"^['\-.,!?]", w))

chunks = []
for p in P["plan"]:
    cur = []
    for w in p["words"]:
        txt = glue([x["w"] for x in cur], [x["w"] for x in cur])
        probe = glue([x["w"] for x in cur + [w]], [x["w"] for x in cur + [w]])
        # break on a full stop once the line has enough body, or when the next
        # word would overflow - but never between a word and its continuation
        ends_clause = bool(cur) and re.search(r"[.,!?:]$", cur[-1]["w"])
        if cur and not cont(w["w"]) and (len(probe) > MAXCHARS or (ends_clause and len(txt) >= 15)):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)

lines = []
for ci, ch in enumerate(chunks):
    end = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else min(ch[-1]["e"] + 0.45, TOTAL)
    for wi, w in enumerate(ch):
        a = w["s"]
        b = ch[wi + 1]["s"] if wi + 1 < len(ch) else end
        if b - a < 0.04:
            continue
        out = []
        for xi, x in enumerate(ch):
            t = esc(x["w"])
            if xi == wi:
                out.append(r"{\c" + GOLD + r"\3c" + SHADOW + "}" + t + r"{\c" + INK + "}")
            elif x["w"] in KEY:
                out.append(r"{\c" + VIOLET + "}" + t + r"{\c" + INK + "}")
            else:
                out.append(t)
        lines.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{glue(out, [x['w'] for x in ch])}")

for a, b, txt in POPS:
    fade = r"{\fad(120,120)}"
    lines.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{fade}{esc(txt)}")
    lines.append(f"Dialogue: 0,{ts(a)},{ts(b)},Tag,,0,0,0,,{fade}AUTOMATISATION BOOST")

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,60,{INK},&H000000FF,{SHADOW},&H64000000,-1,0,0,0,100,100,0.6,0,1,5,4,2,56,56,96,1
Style: Pop,DejaVu Sans,54,{GOLD},&H000000FF,{SHADOW},&H00000000,-1,0,0,0,100,100,2.4,0,1,3,0,8,40,40,78,1
Style: Tag,DejaVu Sans,19,&H005A5A5A,&H000000FF,{SHADOW},&H00000000,-1,0,0,0,100,100,5.0,0,1,2,0,8,40,40,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(os.path.join(HERE, "captions.ass"), "w").write(head + "\n".join(lines) + "\n")
print(f"{len(chunks)} blocs de captions, {len(lines)} evenements ASS, {len(POPS)} mots-cles en bandeau")

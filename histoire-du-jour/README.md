# Histoire du jour — alphabet story engine

Reusable, data-driven HyperFrames engine for the kids' series **« Histoire du jour »**
(French, children 5-7 with a parent): one letter per episode, 9:16 1080x1920, 30 fps, ~34-38 s,
5 scenes, the hero **Milo** (little monkey) with a two-state OPEN/CLOSED lipsync.

A new episode = a new `episodes/<LETTER>/` data folder + one master sheet image. No engine code changes.

```
histoire-du-jour/
├── engine/                 template.html (CSS + timeline shell), vendor/gsap.min.js, fonts/Outfit-Bold.ttf (OFL)
├── tools/
│   ├── build.py            episode data -> sliced assets -> TTS -> timings -> composition -> lint/snapshot -> MP4
│   ├── slice_sheet.py      master sheet -> individual PNG/JPG assets (checkerboard keyed out)
│   └── mouth.py            two-state mouth variants (only the mouth changes, the body never moves)
├── heroes/milo/            Milo library (all poses x {closed, open}), reused by every letter
├── shared/                 letter-independent assets cut from the M sheet (logo, leaves, pop, rays, sparkles, decor)
├── docs/SHEET_PROMPT_TEMPLATE.md   image-generation prompt for a new letter's master sheet
└── episodes/<L>/
    ├── config/project.json episode block (letter, sound, hero, quest, words, game, recap…), voice, audio, theme
    ├── config/scenes.json  the 5 scenes: type, timecode window, background, pose, narration segments + cues
    ├── config/assets.json  asset manifest (from the original pack; informative)
    ├── config/lipsync.json lipsync rules (informative; implemented by build.py)
    ├── sheet_map.json      cells of every asset on the master sheet + mouth boxes (M: measured by hand)
    ├── audio/narration.txt human-readable narration
    ├── docs/               STORYBOARD.md, CLAUDE_PROMPT.md (M pack), SHEET_PROMPT.md (image prompt for new letters)
    ├── assets/source/assets_master_sheet.png   the generated sheet (input)
    ├── assets/cut/         sliced assets (generated) + _preview.png contact sheet
    ├── build/              tts cache, whisper cache, vo/mix wav, timeline.json, snapshots/ (generated)
    ├── composition/        index.html + assets/ (generated HyperFrames project)
    └── output/histoire_du_jour_<L>.mp4 (+ render_report.json)
```

## Commands

```bash
cd histoire-du-jour
export PATH=<dir with ffmpeg/ffprobe>:$PATH
export PRODUCER_HEADLESS_SHELL_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
pip install kokoro-onnx soundfile pillow          # once (local TTS + image tools)

python3 tools/build.py M                          # full build: slice, tts, timing, whisper, mix, compose, lint, snapshot, render
python3 tools/build.py M --only compose,lint,snapshot   # iterate on visuals (uses caches)
python3 tools/build.py M --only render
python3 tools/build.py B --no-whisper             # skip Whisper (cue times estimated inside each segment)
python3 tools/build.py M --reslice                # redo the cut-out from the sheet
python3 tools/slice_sheet.py M [--publish-hero milo]    # slicing alone (+ refresh heroes/milo)
python3 tools/mouth.py M                          # mouth variants alone
```

The HyperFrames CLI is called as `npx --prefix ../autoboost-studio hyperframes` (override with
`HDJ_HYPERFRAMES`); ffmpeg/ffprobe via `FFMPEG`/`FFPROBE` or `PATH`.
Render flags used: `--no-browser-gpu --quality delivery --fps 30`.

## Episode schema

### `config/project.json`

Original pack fields (`name`, `format`, `safeZonePx`, `language`, `audience`, `visualStyle`, `signature`) plus:

```jsonc
"episode": {
  "letter": "M", "upper": "M", "lower": "m",
  "sound": {
    "display": "mmm…",   // what the bubble shows for the sound
    "say": "Mmm.",       // what the TTS reads for the sound (tune per letter: "Sss.", "Rrr.", "Ffff."…)
    "holdSec": 1.0,      // the sound clip is time-stretched (pitch kept) to this length
    "mouth": "closed"    // closed for m/b/p (lips together), "open" otherwise
  },
  "highlight": ["m", "mmm", "milo", "mangue", "maison", "moto", "montagne"],  // words drawn in the accent colour
  "labelPrefix": {"chocolat": "ch"},   // optional: letters coloured at the start of a card label (default 1st letter)
  "hero":  {"id": "milo", "name": "Milo", "intro": "le petit singe"},
  "quest": {"word": "mangue", "label": "Mangue magique", "asset": "mangue", "sign": "sign_mangue"},
  "words": [{"word": "maison", "asset": "maison"}, {"word": "moto", "asset": "moto"}, {"word": "montagne", "asset": "montagne"}],
  "game":  {"choices": [{"word": "lune", "asset": "lune"}, {"word": "maison", "asset": "maison"}, {"word": "chat", "asset": "chat"}],
            "answer": "maison", "thinkSec": 2.0},
  "recap": ["Milo", "mangue", "maison"],
  "outro": "À demain pour une nouvelle aventure !"
},
"voice": {"engine": "kokoro", "voice": "ff_siwis", "speed": 0.92, "maxAtempo": 1.15},
"audio": {"voiceLufs": -16, "music": "<path relative to the episode folder or null>", "musicLufs": -30},
"theme": {"ink": "#1f3a8a", "accent": "#e53935", "accent2": "#1e6fd9", "card": "#fff8e7", "wood": "#7a4a22"},
"ui":    {"letterOfDay": "La lettre du jour"}
```

Asset values are file **stems** (no extension), resolved in `assets/cut/`, `assets/`, `heroes/<hero>/`, then `shared/`.
A missing asset renders as a red dashed box labelled `PLACEHOLDER <name>.png` and is listed by `build.py`.

### `config/scenes.json` — exactly 5 scenes, in this order of `type`

| type | default window | what the engine draws |
|---|---|---|
| `intro`  | 0-6 s   | "La lettre du jour" pill, big upper/lower letters pop + bounce, sparkles, sound rings on every `sound` segment, Milo (sitting) rises from the bottom, speech bubble |
| `quest`  | 6-12 s  | jungle parallax, Milo walks across (walk_1/walk_2 cycle + lipsync), floating leaves, a thought bubble with the quest object + label pops on the quest cue |
| `words`  | 12-20 s | three object cards pop one by one on their spoken word (scale 1.05 -> 1 + glow), card wave on the sound, re-pulse on repeat, Milo points at them |
| `game`   | 20-26 s | three cards (no labels), "?" badge, thinking dots during `thinkSec`, then gentle reveal: glow + bounce + rays + burst on the answer, others dim |
| `reward` | 26-34 s | warm glow + twinkling stars, Milo holding the quest object, recap letters + word chips on their cues, big "Histoire du jour" signature on the outro |

Each scene: `id`, `type`, `start`, `end` (target window), `background` (stem), `pose` (hero pose: `sit`, `walk`,
`point`, `mangue`/`quest`), `elements` (informative), optional `leadSec`, and `segments`:

```jsonc
{"say": "Milo découvre une maison, une moto, et une montagne.",   // TTS text (may differ from display)
 "text": "Milo découvre une maison, une moto et une montagne.",   // bubble text
 "cues": {"maison": "word0", "moto": "word1", "montagne": "word2"}, // spoken word -> visual target
 "pause": 0.35}                                                    // silence after (or "think" = game.thinkSec)
{"kind": "sound", "pause": 0.4}        // the letter sound (episode.sound), mouth forced per sound.mouth
{"kind": "answer", "say": "Maison !", "text": "maison !", "pause": 1.4}   // game reveal
{"kind": "outro", "say": "À demain pour une nouvelle aventure !", "pause": 0.6}
```

Cue targets: `sign` (quest), `word0..2` (words; first hit = pop, next hits = pulse), `recap0..2` (reward chips).
Cue times come from Whisper word timings (`hyperframes transcribe --model small --language fr`, cached per scene
audio); if a word is not found the time is estimated from its position in the segment (logged as `estimate`).

### `sheet_map.json`

`items.<stem>.box = [x, y, w, h]` on the sheet (reference size `reference_size`; other sizes are scaled),
`kind` = `background` | `cutout` | `glow` | `opaque`, options `focusX` (background crop centre), `halo`
(glossy letters/effects with a pastel glow), `holes: false` (subjects with large white areas: cat, snow),
`hero: true` (published to `heroes/<id>/`). `mouths.<stem>` = mouth boxes in **cut** coordinates (2x the sheet):
`{"mode": "pair", "open_from": "milo_open", "register_region": [...], "box": [...]}` or `{"mode": "close", "box": [...]}`.

## How it works

1. **Slicing** — the sheet's "transparent" areas are a printed light checkerboard. Each cell is keyed by
   flood-filling the light, desaturated card colour from the cell borders (subject whites that the flood cannot
   reach — teeth, eyes, snow, the white cat — survive), checker visible through enclosed gaps is removed when it
   matches the card colour, the edge ring gets a soft alpha with colour un-mixing, stray neighbour fragments
   are dropped, the result is trimmed and upscaled 2x (Lanczos + light unsharp). Backgrounds are cropped under
   the "SCÈNE N - FOND" header, cropped to 9:16 around `focusX` and upscaled to 1080x1920 (~5.6x: soft, painterly).
2. **Mouth** — see "Lipsync" below.
3. **Narration** — one Kokoro TTS clip per segment (`ff_siwis`, speed 0.92, cached by text hash), silence-trimmed;
   sound clips are stretched to `holdSec`. Each scene = lead + segments + pauses. If it overflows its window the
   spoken segments are sped up (atempo <= `maxAtempo`, 1.15); if it still overflows the scene is extended, if it
   is shorter the scene keeps its window. Voice is loudness-normalised to -16 LUFS, the optional music bed (house
   "Valse des fleurs" arrangement) to -30 LUFS with fades, mixed into `build/mix.wav`, played by an `<audio>` clip.
4. **Mouth track** — RMS of the voice per video frame (p95-normalised). OPEN on a syllable onset (above 30% and
   35% above the last valley), CLOSED on silence (< 17%) or on a syllable valley (< 55% of the current syllable
   peak), minimum hold 2 frames, forced CLOSED on the letter sound when `sound.mouth = closed` (the "mmm") and
   in silences (M: ~3.7 openings per second of speech, mouth open 30% of frames). The hero is a stack of `<img>`
   (every pose frame x closed/open, same size); the timeline only switches their opacity (hard cuts, no fades).
   Motion (entrance, walk, 3 px micro-bob while speaking) lives on the wrapper, so a mouth change can never
   shift the body. Timed narration: `build/narration_timed.txt`.
5. **Composition** — `build.py` writes a single standalone `composition/index.html`: one `.clip` section per scene
   (0.4 s cross-fade, alternating tracks), a global logo clip, the audio clip, one paused GSAP timeline registered as
   `window.__timelines["main"]`, `fromTo(..., {immediateRender:false})` / `tl.set` only, no randomness at runtime
   (sparkle layout uses a seeded PRNG in Python), finite repeats. Text stays inside the 120 px safe zone; the small
   "Histoire du jour" signature sits bottom-right and hands over to the big one on the outro.

## Lipsync on poses (what is real, what is generated)

| pose | closed | open |
|---|---|---|
| `sit` (milo_closed) | original drawing | original + mouth patch from `milo_open`, registered (scale 1.04, offset -49/-7 px) and feathered |
| `walk` (walk_1/2), `point`, `mangue` | **procedural**: the drawn mouth is detected (red interior/tongue/teeth), in-painted with muzzle skin, a soft smile line is drawn between the corners | original drawing |
| `wave` | procedural result is weak (remnants of the upper lip) | — the pose is flagged `talk: false` and is not used while speaking |

The procedural closed mouths are convincing at video size (the hero is ~600-760 px tall) but not pixel-perfect
up close. Best quality: ask the image generator for real `*_closed.png` / `*_open.png` pairs per pose.

## Limitations

- Assets come from one ~1214x1295 sheet: characters/props are upscaled 2x from ~150-230 px cells, backgrounds
  ~5.6x — fine on a phone, soft on a big screen. Higher-resolution sheets (2048+) are used as is (boxes scale).
- Keying is colour-based: pale glows (stars, magic swirl on the M sheet) cut poorly, so the engine draws its own
  SVG sparkles; `etoiles`/`magie` are sliced but unused. A few light specks remain on some edges.
- Each new sheet is a new AI image: the layout will drift a little. `sheet_map.json` is copied from M and its
  boxes (and mouth boxes) must be checked on `assets/cut/_preview.png` and adjusted.
- Kokoro French (`ff_siwis`) is a clear, neutral female voice, not a cloned or child voice; letter names and
  sounds may need phonetic spelling in `say` ("Q" -> "ku", sounds like "Sss.").
- Whisper `small` on this machine needs ~2 min per scene; use `--no-whisper` for quick iterations.
- `background_02` of the M sheet already paints the "Mangue magique" sign; the engine shows the quest in a
  thought bubble instead of stacking a second sign (`sign_mangue` is sliced but not used).

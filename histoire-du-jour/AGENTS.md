# AGENTS.md — Histoire du jour

Instructions for coding agents (OpenCode, Claude Code, Codex…) working in this folder. When Tony says
« histoire du jour : lettre X » (or « fais la lettre X »), follow the procedure below.

## Setup on Tony's PC (once)

```bash
cd ../autoboost-studio && npm install && cd ../histoire-du-jour   # brings HyperFrames, ffmpeg and ffprobe
pip install kokoro-onnx soundfile pillow numpy       # local French voice (free) + image tools
```
- ffmpeg/ffprobe: if they are not on PATH, point `FFMPEG` / `FFPROBE` at `autoboost-studio/node_modules/ffmpeg-static/ffmpeg`
  and the binary inside `autoboost-studio/node_modules/ffprobe-static/bin/<os>/<arch>/`.
- HyperFrames is called as `npx --prefix ../autoboost-studio hyperframes` (the build script does it).
- Run `npx --prefix ../autoboost-studio hyperframes doctor` if the render or the snapshots fail (Chrome headless).
- Everything is local and free: Kokoro voice, Whisper timings, HyperFrames render. Only the master sheet image
  is generated outside (ChatGPT / Higgsfield), by Tony.

## Self-checks a weaker model must not skip

- Say every chosen word out loud in your head: its FIRST SOUND must be the target sound (A: « avion », not « ange »).
- The 2 mini-game distractors must not start with the sound, nor with its voiced/unvoiced twin (b/p, d/t, f/v, s/z, m/n).
- JSON must stay valid: `python3 -c "import json;json.load(open('episodes/X/config/project.json'));json.load(open('episodes/X/config/scenes.json'))"`.
- Diff your files against `episodes/M/` before running: same keys, same scene types and windows, only the content changes.
- Never report « done » without running the validation command and reading its output.

You produce episodes of **« Histoire du jour »** for Tony PAYET: French alphabet stories for children aged 5-7
watched with a parent. The engine is this folder (`histoire-du-jour/`) — read its `README.md`
first (episode schema, commands, limitations). Episode M (`episodes/M/`) is the reference: copy its structure.

**Always reply to Tony in French.** Code, comments and file docs stay in English; narration and on-screen text
are French. Never spend paid image/video credits (ChatGPT, Higgsfield, WaveSpeed…) without Tony's explicit OK.
Never git commit or push unless Tony asks.

## Input
A letter X (optionally: another hero, a theme, a quest object, words Tony wants). Default hero: **Milo** (continuity).

## Step A — write the episode data (`episodes/X/`)

1. `mkdir -p episodes/X/{config,docs,audio,assets/source}`; copy `episodes/M/config/lipsync.json`.
2. Choose the pedagogy (French phonetics — the INITIAL SOUND must be the target sound, not just the letter):
   - **Sound** (`episode.sound`): `display` (bubble), `say` (what Kokoro reads; test it), `holdSec` ~1.0,
     `mouth`: `closed` only for a hummable bilabial (M); `open` for held vowels (A « aaa », O « ooo », I, U « uuu »);
     `energy` for everything else (plosives B/D/P/T/K/G and fricatives F/S/V/Z/J/CH, liquids L/R, N).
     Held consonants: « fff », « sss », « vvv », « zzz », « jjj », « lll », « rrr », « nnn ». Plosives cannot be held:
     use a short syllable (« beu », « deu », « peu », « teu », « keu », « gueu ») and `holdSec` ~0.6.
   - **Traps**: C hard /k/ only before a/o/u (canard, cadeau, cochon — not cerise/citron); G hard /g/ only
     before a/o/u (gâteau, gorille, guitare — not girafe); H is silent → do an « h muet » episode (hibou, hérisson,
     hamac) and say so in the narration (« le H ne fait pas de bruit ») — ask Tony first; Q → « qu » /k/
     (quille, queue, quatre); W is ambiguous (/w/ wapiti vs /v/ wagon) — pick one, say which; X rarely starts
     a word → teach /ks/ « comme dans taxi, boxe, saxophone » and change « commence par » into « on entend »
     (ask Tony); Y → /j/ (yoyo, yaourt, yack); vowels: avoid nasals and digraphs that change the sound
     (A: avion/ananas/arbre, not ange; O: orange/os/olive, not oiseau/ours; E: prefer « é »: école, éléphant,
     étoile, and display « é »; I: île/igloo, not indien; U: usine/uniforme, not un).
   - **Quest object** (starts with the sound, concrete, drawable, can be held by Milo): sign label
     « <Objet> magique » (mind gender: « sa mangue », « son ballon »).
   - **3 example words** with the target initial sound, 1-3 syllables, concrete, drawable, known by a 5-year-old.
   - **Mini-game**: answer = one of the 3 words; 2 distractors that do NOT start with the sound (nor a similar one:
     no b/p, d/t, f/v, s/z, m/n pairs). Vary the answer position (not always the middle).
   - **Recap**: 3 words (hero name only if it starts with the sound, else quest + 2 words).
   - Outro, always: « À demain pour une nouvelle aventure ! »
3. `config/project.json`: copy M's file and change `name`, `output`, the `episode` block (letter, upper, lower,
   sound, highlight = every displayed word with the sound + the sound + the letter, hero, quest, words, game,
   recap, outro), keep `voice`, `audio`, `theme`. Asset stems = slugs (lowercase, no accents, `_`).
4. `config/scenes.json`: copy M's 5 scenes (same `type`, windows 0-6/6-12/12-20/20-26/26-34) and rewrite the
   segments with the same pedagogy:
   1. intro: « Aujourd'hui, découvre la lettre X. » / « X fait le son… » / sound / « Répète avec moi : » / sound
   2. quest (`pose: walk`): « Voici Milo, le petit singe. » / « Il cherche son|sa <objet> magique ! » (cue the
      object word → `sign`)
   3. words (`pose: point`): « Milo découvre un/une w1, un/une w2, et un/une w3. » (cues → `word0..2`) /
      « Répète : » / sound / « W1 ! » (cue → `word0`)
   4. game (`pose: sit`, `leadSec` 0.8): « Regarde bien… » / « Quel mot commence par <sound> ? » /
      « Dis-le à voix haute ! » with `"pause": "think"` / answer segment `{"kind": "answer", "say": "<Mot> !", "pause": 1.3}`
   5. reward (`pose: quest`): « Bravo ! » / « Milo a retrouvé son|sa <objet>. » / « X comme r1, r2, et r3. »
      (cues → `recap0..2`) / outro segment `{"kind": "outro", …, "pause": 0.6}`
   Keep each sentence short (bubble ≤ ~40 characters). `say` may add commas for rhythm or phonetic spelling;
   `text` is what is displayed. Write `audio/narration.txt` (timecoded lines) and `docs/STORYBOARD.md`.
5. Validate quickly: `python3 tools/build.py X --only timing,mix,compose,lint --no-whisper` (works without any
   sheet: missing images become red PLACEHOLDER boxes; Milo comes from `heroes/milo/`). Check durations
   (total 30-38 s) and that `say` texts sound right: transcribe one doubtful clip from `build/tts/` with
   `npx --prefix ../autoboost-studio hyperframes transcribe <wav> --model small --language fr --json`.

## Step B — the master sheet prompt
Fill `docs/SHEET_PROMPT_TEMPLATE.md` into `episodes/X/docs/SHEET_PROMPT.md` (all `{{…}}` replaced; scene
backgrounds that match the words, e.g. a farm for « vache », the sea for « bateau »). Then tell Tony, in French:
- paste the prompt in ChatGPT (image) or Higgsfield, **attaching `episodes/M/assets/source/assets_master_sheet.png`
  as reference**;
- save the result as `histoire-du-jour/episodes/X/assets/source/assets_master_sheet.png`;
- you will not generate it yourself without his OK (paid credits).
Stop here and report (the episode data + the prompt path) until the sheet exists.

## Step C — build once the sheet exists
1. `cp episodes/M/sheet_map.json episodes/X/sheet_map.json`, then edit it: rename item keys to X's stems
   (`letter_X_upper`, `letter_x_lower`, `sign_<quest>`, the 8 objects in row order, `milo_<quest>_open`);
   add `"skip": true` to `milo_closed`, `milo_open`, `milo_wave_open`, `milo_walk_1`, `milo_walk_2`,
   `milo_point_open` (the hero library is used) and, unless the new sheet's versions look better, to the
   letter-independent items `histoire_du_jour`, `etoiles`, `magie`, `rayons`, `pop`, `feuilles`, `fleurs`,
   `rocher_plantes`, `frame_overlay` (`histoire-du-jour/shared/` is used); `mouths`: keep only
   `milo_<quest>_open` with `"mode": "close"`.
2. Look at the sheet (open the image). If its size/grid differs, fix the boxes (zoom crops:
   `python3 - <<EOF` with PIL, or `ffmpeg -vf crop=w:h:x:y`), then
   `python3 tools/slice_sheet.py X` and **look at `episodes/X/assets/cut/_preview.png`**: every item complete,
   no label text, no neighbour fragments, letters clean. Iterate on boxes / `halo` / `holes:false` (white
   subjects) until clean. Measure the mouth box of `milo_<quest>_open` on the cut PNG (cut px = 2x sheet px) and
   check `<stem>__closed.png`.
3. `python3 tools/build.py X` (full: tts, timing, whisper, mix, compose, lint, snapshot, render). Environment: see
   « Setup on Tony's PC » below. `HDJ_RENDER_WORKERS=2` on a busy machine. Whisper takes ~2 min per scene with cues
   (cached afterwards).
4. Lint must report 0 errors (the `nested_structure_needs_subcomposition` / `composition_file_too_large`
   warnings are expected). Open `build/snapshots/contact.png` and the frames (open the image files and look at them): text readable
   and inside the 120 px safe zone, nothing clipped, cards/letters/hero not overlapping text, mouth swaps
   not moving the body, the mini-game pause (~2 s) before the reveal. Fix data (shorter texts, `leadSec`,
   pauses) or boxes, re-run `--only compose,lint,snapshot`, then `--only render`.
5. Check `output/render_report.json` (1080x1920, frames = 30 x duration, audio `aac`).
6. Report to Tony in French: MP4 path, duration, the words chosen and why (phonetics), anything approximate
   (cut-outs, procedural closed mouth on the quest pose, estimated cues), and what he could improve
   (higher-resolution sheet, real closed/open pairs for the quest pose).

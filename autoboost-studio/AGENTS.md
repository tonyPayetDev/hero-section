# AGENTS.md — AutoBoost Studio

Instructions for coding agents (OpenCode, Claude Code, Codex…) working in this folder.
Tony runs the tool with `npm start` (http://localhost:4747). It turns a face-cam video into a branded MP4
with **no LLM at run time**: whisper transcription → rule engine → HyperFrames HTML → render → mix.

## Map

| Path | Role |
|---|---|
| `lib/pipeline.mjs` | One job: transcribe, cut silences, voice, optional background removal, plan, compose, render, mix |
| `lib/plan.mjs` | Rule engine: words → scenes `{ type, a, b, start, words, head, data, sticker, level, hook }`. Shared by every style. |
| `lib/compose.mjs` | Loads the chosen style from `styles/<id>/` and calls it |
| `lib/kit.mjs` | Shared helpers every style uses: `timeline()`, `chars()`, `headParts()`, `captions()`, `levelChips()`, `sticker()`, `camMode()`, `camTag()`, `kwSize()`, `writeComposition()` |
| `styles/<id>/` | One visual style: `style.json` + `composition.html` + `compose.mjs` (+ optional `assets/`) |
| `templates/` | Shared data: `icons.json` (SVG icons), `music.json` (beds) |
| `assets/` | Shared files copied into every render: fonts, `vendor/gsap.min.js`, `kit/` (kit.css, kit.js), `sfx/`, `music/` |

Scene types produced by `plan.mjs`: `headline`, `question`, `stat`, `tools`, `list`, `contrast`, `steps`, `cta`.
The first scene has `hook: true`. A style **must** render every type (fall back to the headline look if unsure).

## Add a new style (the usual task)

1. Copy the closest existing style: `cp -r styles/seedance-neon styles/my-style`.
2. Edit `styles/my-style/style.json`:
   ```json
   { "name": "Shown in the UI", "description": "One sentence for Tony",
     "formats": ["9:16"], "cutout": true, "music": "valse" }
   ```
   `formats`: `"9:16"` and/or `"16:9"`. `cutout`: true only if the layout works with the matted person (`#camw`).
   `music`: a key of `templates/music.json`.
3. Change the look in `composition.html` (CSS) and the layout/animation in `compose.mjs`.
4. Test (below). The UI lists the style automatically; nothing else to register.

## Add a new scene type (a new screen)

1. `lib/plan.mjs`: add the detection rule (a regex or word test) **before** the `headline` fallback and fill `sc.data`.
2. In **every** `styles/*/compose.mjs`: add a `case "my-type":` in the `switch`. Copy the closest existing case.
3. CSS for it in every `styles/*/composition.html`.

## HyperFrames rules (breaking one gives a render that jumps, flickers or stays black)

- One GSAP timeline, created **paused**, registered as `window.__timelines["autoboost-studio"]`. Never call `play()`.
- Only add tweens through the `timeline()` helpers (`R`, `S`, `up`, `pop`, `kin`, `count`…). They write
  `tl.fromTo(..., { immediateRender: false }, time)` at an **absolute time**. No `gsap.to` outside the timeline,
  no `setTimeout`, no `Math.random()`, no `Date.now()`, no CSS `animation`/`transition`: the renderer seeks frame by frame.
- The CSS holds the "before" state (`opacity: 0`); the timeline reveals it.
- Timed elements (`<section class="scene clip">`, `<video>`) carry `data-start`, `data-duration`, `data-track-index`.
  Animate a **wrapper** (`.in`, `#camw`, `.pad`), never the timed element's own opacity.
- Text that animates letter by letter is built with `chars(text, cls)`. A gradient text (`background-clip: text`)
  must be put on each letter (`chars(text, "g")`), not on the parent span: the gradient skips inline-blocks.
- Every reveal is pinned to a spoken word time (`sc.start`, `headParts(sc).hiAt`, `sc.data.at`, `item.at`).
- Charter: gold `#eab308`, violet `#8b5cf6`, red `#ff6b6b` only for « bad »; ink background. **No green, no emoji.**
- Text must fit: 1080 px wide in 9:16. Use `kwSize()` for the CTA keyword; keep lines ≤ ~16 characters at 100 px.

## Test (always, before saying it works)

```bash
npm install
node -e "import('./lib/compose.mjs').then(m => console.log(m.listStyles().map(s => s.id)))"   # the style is listed
# full run on a real video: npm start, open http://localhost:4747, pick the style, drop a face-cam mp4
npx hyperframes lint jobs/<job-id>/composition            # must say 0 error(s) (warnings are fine)
npx hyperframes snapshot jobs/<job-id>/composition --at 1,5,10,15,20,25 --no-end -o /tmp/snap
```
Open the PNGs in `/tmp/snap` and check: the text is visible and inside the frame, the face is not cut,
captions do not cover the face, the CTA keyword fits on one line. Fix and re-run until it is clean.

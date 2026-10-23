# autoboost-84 — Défi piment (Tony + Tony IA)

Tony's own take (spicy noodles challenge, 6 min 18 s, shared from his Drive) cut to ~65 s on his words,
dressed with his « Piment Power » kit, with Tony IA stepping in five times in the chili ring (cloned voice).

- `session/edit.json` — the Tony segments kept (raw times) and the IA lines, in order
- `build.py TAKE.mp4 TRANSCRIPT.json IA_VO_DIR BUILD/` — base.mp4 (jump cuts on words, IA over the muted bites),
  tony.wav, ia.wav, avatar.mp4 (BUREAU avatar, lips only on IA lines), vo.json
- `motion/gen.py` + `motion/template.html` — HyperFrames: hook title + flames, chili meter 0→5 on the bites,
  kit stickers, IA ring (kit `cadre-06`), word-by-word captions (orange Tony / violet IA), like + subscribe
- `motion/public/piment/` — kit assets with their black matte turned into real alpha

```bash
python3 ../../.claude/skills/duo-ia-remake/scripts/tts_wavespeed.py session/ia.json VO/      # IA lines (WAVESPEED_API_KEY)
python3 build.py VID_20261023_200555.mp4 transcript.json VO/ BUILD/
BUILD=BUILD python3 motion/gen.py && npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery
# mix: tony.wav + ia.wav (each -18 LUFS) -> facecam_audio.py --bed valse -> mux
```

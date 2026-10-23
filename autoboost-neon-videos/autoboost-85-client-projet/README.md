# autoboost-85 — Quand le client décrit son projet (Tony + Tony IA)

Tony's own lip-sync take (the « palais » scene of *Astérix & Obélix : Mission Cléopâtre*, 35 s) framed as
« POV freelance : quand le client décrit son projet ». The lip-sync is never cut: Tony IA speaks on freeze frames
(« Moi, j'imagine surtout le devis. », « Un mois ? Avec Claude, c'est livré ce soir. ») and closes with the
« montée 100 % avec Claude — commente MONTAGE » card (same outro as autoboost-84). No music bed: the take carries its own sound.

```bash
python3 ../../.claude/skills/duo-ia-remake/scripts/tts_wavespeed.py session/ia.json VO/      # IA lines (WAVESPEED_API_KEY)
python3 build.py 2026-10-23-235513765.mp4 VO/ BUILD/
BUILD=BUILD python3 motion/gen.py && npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery
# mix: tony.wav + ia.wav (each -18 LUFS) -> facecam_audio.py --bed none -> mux
```

# autoboost-75 — Skill Arena (Tony + avatar IA)

9:16 · 1080×1920 · 30 fps · **108,6 s** (3 258 images) · −15,8 LUFS

Session `/tournage/2026-10-02-134234`: Tony films the whole **Skill Arena** script in
front of the prompteur, IA lines included. His IA lines are cut out of his track and
replaced by his **IA avatar** (BUREAU bank) speaking with his **cloned voice**.
Built with `/face-cam-boost` in dialogue mode. The `_moteur/monter-tournage.mjs`
engine named in the request is not in this repository.

## Pipeline

```bash
S=.claude/skills/face-cam-boost/scripts
python3 $S/facecam_cut.py video.mp4 --work build/ --stage transcribe          # faster-whisper medium, word level
python3 $S/facecam_dialogue.py --src video.mp4 --script session/script.md --work build/   # align + tts + build
ASM=build/asm python3 motion/gen.py && npx hyperframes lint motion/public
npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery --no-browser-gpu
python3 $S/facecam_audio.py --voice build/asm/voice.wav --events motion/events.json --frames 3258 --out mix.wav --bed valse
```

`assemble.py` and `tts.py` are the first, project-specific versions (scratch paths
hard-coded). `facecam_dialogue.py` reproduces the same alignment line for line.

- The **prompteur repères** (`reperes.json`) drift by up to 5 s from the real take, so
  they are not used for timing. The script is aligned word by word on the transcript
  (`session/aligned.json`). One IA line, « Enfin. », was skipped at the shoot. It is
  generated anyway and placed after Tony's « Oui. ».
- MOI lines: silences > 0,5 s cut, `atempo` 1,10, block 14 (« accélération ») 1,18.
- IA lines: Tony's frame is frozen and dimmed. The avatar card slams in (glitch on the
  first one), alternating right/left. A bubble types the line word by word.
  Avatar clips are taken from their lips-active ranges only (LIPS-MAP.md).
- Voices: Tony's take is normalized once over the whole take. The IA clone is matched to
  it (±1,5 dB). F0 is checked between 114 and 133 Hz, so no OpenAI fallback slipped in.

## Screens

| Bloc | Face cam | Écran du haut | Stickers |
|---|---|---|---|
| Hook | plein écran | « RÉPONSE ÉCLATÉE » qui se fissure | — |
| Redemande | rectangle | REDEMANDER 15 FOIS, trois bulles de relance | BREF. · TROP LENT (vanne IA) |
| Arena | cercle néon | PLUSIEURS CLAUDE, MÊME PROBLÈME | — |
| Flow | rectangle | UNE SEULE TÂCHE → UNE ARMÉE D'AGENTS, câbles or/violet | — |
| Agents | rectangle | CHACUN SA STRATÉGIE (simple / failles / autre voie) | SANS GÉRARD (vanne IA) |
| Duel | cercle | COMPARÉES, ÉLIMINÉES (tampon rouge) | FAÇON DE PARLER |
| Accélération | rectangle | PAS LA PREMIÈRE, LA MEILLEURE | CHALLENGÉE · COMPARÉE · AMÉLIORÉE |
| Relance | cercle | FINI DE REFORMULER → je lance l'Arena | BIENVENUE EN 2026 |
| Install | rectangle | chaîne lien → Claude → prompt → installée | — |
| CTA | grand cercle | COMMENTE ARENA (mot élastique), champ commentaire tapé | — |
| Fin | plein écran | « À LA PROCHAINE / ARENA » (boucle gardée) | — |

Workflow-node references (green in the originals) are redrawn in gold/violet, as the
charter requires: no green, no emoji.

## Before publishing

- **CTA ARENA**: no Blotato DM gate exists for this keyword. It has to be created with the
  resource URL (Skill Arena link + install prompt) before the video goes out.
- The IA voice uses the WaveSpeed clone through the n8n `tts-gen` webhook. It costs a few
  credits per line.

## Files

- `assemble.py`, `tts.py`: first project-specific alignment/assembly, generalized into
  `.claude/skills/face-cam-boost/scripts/facecam_dialogue.py`.
- `session/`: script, transcript, alignment, timeline, the 12 cloned IA lines.
- `motion/gen.py` + `motion/template.html`: the HyperFrames composition (`public/` is generated).
- `motion/events.json`: 54 SFX cues for `facecam_audio.py`.

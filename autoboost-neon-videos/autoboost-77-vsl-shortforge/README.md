# autoboost-77 — VSL ShortForge (pdoom × charte AutomatisationBoost)

9:16 · 1080×1920 · 30 fps · **32,0 s** (960 images, 16 mesures à 120 BPM) · −15,6 LUFS · CTA **FORGE**

A short video sales letter for **ShortForge** (skill Claude Code, 67 € founder price, then 97 €,
one-time payment, 14-day guarantee). It follows the structure of
[vsl-motion-design](https://automatisationboost.com/ressources/vsl-motion-design.html) (30 s grid:
hook + relance, problem + cost, method in 3 steps, real proof, what you get, action). The look and
beat-sync come from [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video), redrawn in the
charter. The hooks follow `hook-puissant-branded` (visual hook + verbal hook, countdown climax).
Every claim on screen comes from the sales page (`session/NOTES.md` §3).

## Pipeline

```bash
S=.claude/skills/face-cam-boost/scripts
# 15 VO lines in the cloned voice (n8n tts-gen, F0 checked) -> VO/ia/iaNN.mp3 + VO/lines.json
python3 vo.py VO/ build/          # each line on its scene beat, atempo <= 1.15, word timings -> voice.wav, vo.json
python3 assets.py build/          # avatar.mp4 (BUREAU B1, muted), bed.wav (drums 30 -> 62 s), proof/p0-5.jpg
BUILD=build python3 motion/gen.py && npx hyperframes lint motion/public
npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery --no-browser-gpu
python3 $S/facecam_audio.py --voice build/voice.wav --events motion/events.json --frames 960 \
        --out mix.wav --bed-file build/bed.wav --bed-gain -14.5
```

## Following the music

`hook-epical-drums-02-80.mp3` (Mixkit). It was measured with `beats.py` at **120 BPM** (the
library's "80" is wrong): beat 0,5 s, bar 2 s, downbeats of the 30 → 62 s window on every even
video second. The track drops to near silence from video 25,5 s and comes back in full at
**28,0 s**: the countdown sits in that silence and the detonation lands on the re-entry.

- Every scene cut is a downbeat: 0 · 1 · 4 · 6 · 10 · 12 · 14 · 16 · 18 · 20 · 22 · 26 · 28. The 1-second visual hook is the only cut off a downbeat.
- 3 · 2 · 1 lands on beats 26,0 / 26,5 / 27,0, then nothing moves for 0,6 s (the VSL page's freeze), then **Action !** and the flash on 28,0.
- A light pulse on every beat (stronger on downbeats), and FORGE pulses on each beat of the climax.
- Every word slam lands on the cloned voice's word (faster-whisper timings), never ahead of it.
- The music is +16 dB where no one speaks (first second, after « Action ! »), at a fixed level under the voice, and ducked.

## Scenes

| t | pdoom piece | Écran | Voix |
|---|---|---|---|
| 0-1 | slam + spark « fuse » | **2 H** rouge coupé en deux par l'étincelle, braises | — |
| 1-4 | typographic hook slam, dense stack | TU SAIS / QU'IL FAUT / **POSTER** / TOUS LES JOURS. | Tu sais qu'il faut poster tous les jours. |
| 4-6 | inverted paper plate + rubber stamp | TU NE LE FAIS **PAS.** (tampon) | Tu ne le fais pas. |
| 6-10 | Gantt + playhead + readout | 6 étapes tamponnées sur la voix, horloge 0 h 00 → **2 h 00**, TROP LENT | Écrire, filmer… Deux heures. |
| 10-12 | collapse + accent flash (violet instead of acid green) | **SHORTFORGE** élastique, skill Claude Code | Short Forge fait les six étapes. |
| 12-18 | prompt field, scope, spark-drawn outline | 1 brief tapé · 2 voix / avatar / captions (ton avatar BUREAU) · 3 téléphone + PRÊT À POSTER | Tu colles un brief… |
| 18-20 | rewind montage | 6 vraies images de tes vidéos avatar, puis 6 FORMATS DÉJÀ PUBLIÉS | Six formats, déjà publiés. |
| 20-22 | the number readout blown up | coût / vidéo : ~~80–150 €~~ → **≈ 0,50 €** | Environ cinquante centimes par vidéo. |
| 22-26 | — | ~~97 €~~ **67 €** · prix fondateur · paiement unique · garantie 14 jours · champ « commente FORGE » | Soixante-sept euros… Commente FORGE… |
| 26-28 | stacked numerals | 3 · 2 · 1, gel | Trois. Deux. Un. |
| 28-32 | outro detonation, crop marks | flash, burst, **COMMENTE FORGE** tenu, pulsé au tempo | Action ! |

pdoom's orange → gold `#eab308`, its mono machine voice → violet, its acid green → a violet
flash. Deadpan mono footnotes (`fig. N · …`) carry the meta lines so they take no voice time.

## Before publishing

- **CTA FORGE: no Blotato DM gate exists for this keyword.** It needs to be created on IG and FB,
  with the DM leading to the ShortForge sales page. Alternative: reuse STAR, which exists on IG only.
- The founder-price wording differs across pages (« 20 places » / « 10 premiers »). The video only
  says « prix fondateur ».
- Proof frames: autoboost-61, 62, 63, 09, 08 and 10 (real renders from the repo).

# autoboost-76 — « Ce clip-là, je l'ai quasiment pas monté » (CTA MOTION)

9:16 · 1080×1920 · 30 fps · **31,1 s** (932 images)

Session `/tournage/2026-10-02-140117` (49 s take, 3:4) + `anime_1.mp4`, the clip being
showcased: Tony's own song with the motion an AI tool generated around it (150 s, 9:16).
Built with `/face-cam-boost`, in the same branding as autoboost-75. The
`_moteur/monter-tournage.mjs` engine named in the request is not in this repository.

## Pipeline

```bash
S=.claude/skills/face-cam-boost/scripts
python3 $S/facecam_cut.py video.mp4 --work build/ --stage transcribe
python3 $S/facecam_cut.py video.mp4 --work build/ --stage plan --fixes session/fixes.json
python3 $S/facecam_cut.py video.mp4 --work build/ --stage cut                 # 7 cuts, atempo 1.14 -> 31.07 s
python3 clip_track.py anime_1.mp4 build/plan_actual.json cliptrack/            # the clip, frame-exact on the cut
BUILD=build CLIPTRACK=cliptrack python3 motion/gen.py && npx hyperframes lint motion/public
npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery --no-browser-gpu
python3 $S/facecam_audio.py --voice build/voice.wav --events motion/events.json --frames 932 \
        --out mix.wav --bed-file cliptrack/clip_song.wav --bed-gain -13
```

- **ASR fixes** (`session/fixes.json`): « outil à imaginer avec motion » → « outil IA… et il
  m'a généré tout le motion » (re-checked with a context prompt), « rig » → « rythme »,
  « comment je m'enchaîne » → « commente MOTION », « je te donne l'envoi » → « je te l'envoie ».
- **The clip is the music.** `clip_track.py` cuts the clip to the timeline, picture and
  song together, so what plays in the phone is what you hear. The finale ends on clip
  frame 26,83 s and the hook starts there, so the loop is seamless in both picture and sound.
  The song sits under the voice at a fixed level (−13 dB on a −13 LUFS track), ducked.

## Screens

| Bloc | Face cam | Écran | Clip | Sticker |
|---|---|---|---|---|
| Hook | PiP cercle néon + tag TONY | CE CLIP-LÀ / PAS MONTÉ. (quasiment) | plein écran, punch zoom + flash | — |
| La méthode | rectangle | MON SON → OUTIL IA → TOUT LE MOTION, câbles or/violet | dans un cadre téléphone « LE CLIP » | FAIT MAISON |
| Le secret | cercle néon | timeline ANIMATIONS / RYTHME / CHANGEMENTS DE PLANS : la vraie forme d'onde du passage, coupes et keyframes sur ses attaques, tête de lecture synchro | téléphone (passage MI MI MI) | CALÉ SUR LE SON |
| Ce qui change | rectangle | AVANT des heures à monter (barré) / MAINTENANT le temps sur l'idée | — | ÇA CHANGE TOUT |
| CTA | grand cercle | COMMENTE MOTION (élastique), champ commentaire tapé, DM reçu | — | — |
| Fin | PiP | LE RÉSULTAT / LE PLUS FOU… | plein écran (refrain ROULE / OULALA) → boucle | — |

The clip's own orange is kept: it is the product being shown. Every overlay stays in
the charter (gold, violet, no green, no emoji).

## Before publishing

- **CTA MOTION**: check that a Blotato DM gate exists for this keyword (tool name +
  how-to). Without it, people comment and get nothing.

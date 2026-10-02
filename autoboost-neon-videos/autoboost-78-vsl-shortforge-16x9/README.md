# autoboost-78 — VSL ShortForge v2 (16:9, style « boost niveau »)

16:9 · 1920×1080 · 30 fps · **44,5 s** (1336 images, 23 mesures de Deep Urban) · −16 LUFS · CTA **FORGE**

v2 of `autoboost-77-vsl-shortforge`, after Tony's notes:
- **no price** anywhere: no offer price and no cost per video;
- **16:9** instead of 9:16;
- closer to the **boost niveau** reels (`ref-0-07-dollar`): a NIVEAU 1 → MAX chip, neon side
  tubes, the avatar in a neon circle with a caption pill, and punch stickers;
- a **stylish track** and a **minimalist font** (Inter, plus JetBrains Mono for labels);
- **the value and real examples on screen**: real renders play inside phones, and the value is
  shown as « 2 h → quelques minutes » plus what you get;
- **no glitches**: each panel slides in while the previous one leaves, so no cut shows an empty
  frame, and the caption pill only exists while words are spoken.

## Pipeline

```bash
# VO: 15 lines of v1 (no price) + 3 new lines in the cloned voice (tts-gen webhook, F0 checked)
python3 build.py VO/ build/            # voice.wav + vo.json, avatar.mp4, ex0-3.mp4, bed.wav
BUILD=build python3 motion/gen.py && npx hyperframes lint motion/public
npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery --no-browser-gpu
python3 .claude/skills/face-cam-boost/scripts/facecam_audio.py --voice build/voice.wav \
        --events motion/events.json --frames 1336 --out mix.wav --bed-file build/bed.wav --bed-gain -22.4
```

## Music

`food-deep-urban-122.mp3`, the library's « VSL formation » house bed. It measures **124 BPM**
(the manifest says 122): beat 0,484 s, bar 1,936 s. The window starts on a downbeat (file
45,227 s), so the video's downbeats are k × 1,936 s.

- Every scene cut is a downbeat (bars 2, 5, 7, 12, 15, 20).
- The tubes breathe on every beat and the avatar ring kicks on every downbeat.
- The track's **breakdown** (video 29,0 → 38,7) carries « ce que tu reçois » and the 3-2-1 countdown, with every number on a beat.
- The **re-drop** at 38,71 s is « Action ! » and the flash.

## Scenes

| Bars | Niveau | Panel | Sticker |
|---|---|---|---|
| 0-2 | — | TU SAIS QU'IL FAUT **POSTER** TOUS LES JOURS · semaine cochée 2/7 · TU NE LE FAIS PAS. | ÇA PART |
| 2-5 | 1 | les 6 étapes s'allument sur la voix, horloge 0 h 00 → **2 h 00** | TROP LENT |
| 5-7 | 2 | **SHORTFORGE** · ton paragraphe → les 6 étapes cochées | PLUS SIMPLE |
| 7-12 | 3 | 1 brief tapé · 2 voix / avatar / captions · 3 prête à poster + **une vraie vidéo qui tourne** dans le téléphone | GAIN TEMPS |
| 12-15 | 4 | **3 vraies vidéos** côte à côte · 6 formats déjà publiés · ~~2 h~~ → quelques minutes | ÇA MONTE |
| 15-20 | MAX | ce que tu reçois : le skill complet · 10 formats × 10 directions artistiques · un seul tournage · puis 3 · 2 · 1 | BON SYSTÈME |
| 20-23 | MAX | **COMMENTE FORGE**, champ commentaire, « je t'envoie le lien en DM » | — |

The avatar is Tony's BUREAU bank. Its lips-active ranges play only while a line is spoken,
with a still frame in between. The examples are real renders from the repo: autoboost-61
(in the phone), then 62, 63 and 10. Each plays only during its window, muted.

## Before publishing

- **CTA FORGE: no Blotato DM gate yet.** It has to be created on IG and FB, with the DM leading
  to the ShortForge sales page.

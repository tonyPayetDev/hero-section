# VSL ShortForge x pdoom — research notes (2026-10-02)

Scratch: `/tmp/claude-0/-home-user-hero-section/25c114f9-7c32-5b84-b3ea-354b9cf49fbf/scratchpad/vsl/`
- `vsl-motion-design.html` (+ `vsl-page.txt` text extract) — the VSL resource page
- `site/` — home.html, formation.html, audit.html, ressources.html, skills.html, videoboost-vente.html
- `pdoom-video/` — clone of github.com/mexicat/pdoom-video (commit bdbad53)
- `beats.py` — numpy-only beat grid tool (validated on pdoom: 132.0 BPM vs their 132.007; phase 0.225 vs 0.238)
- `audio/*.grid.json` — grids of the candidate tracks

## 1. The VSL page (https://automatisationboost.com/ressources/vsl-motion-design.html, keyword VSL)

Short VSL = 7, 15 or 30 s, motion design (no camera), one target, one problem in their words, one promise
you can SHOW, one action ("deux choix, c'est zéro choix"). Sentence test: « Je montre à [qui] que
[résultat] et je lui demande de [action]. » Logic always: accroche -> problème -> preuve -> action.
- 7 s: 0-1 image forte + 3-5 mots (no logo/intro) · 1-3 problème mot par mot · 3-5 résultat montré
  (avant/après) · 5-7 action, un verbe + un mot, reste jusqu'à la fin.
- 15 s: 0-2 situation · 2-5 problème · 5-10 solution en action (2-3 plans) · 10-12 preuve réelle (jamais un
  chiffre inventé) · 12-15 action seule.
- 30 s: 0-3 accroche + relance à 2 s · 3-8 problème + coût · 8-18 méthode en 3 étapes (un plan par étape)
  · 18-24 preuve réelle · 24-27 ce que la personne reçoit · 27-30 action.
- Extend by adding boxes, never by slowing down.
Motion rules: (1) something moves on frame 1, no black/logo/Bonjour; (2) one idea per shot, triggered by a
precise word (literal image: « rapide » -> something fast); (3) 3-6 words per screen, big, centred away from
the UI edges, ONE accent colour only on the word that matters; (4) one transition direction for the whole
video (exit left / enter right), no filler animation, a short freeze before the strong moment, a click on
transitions and music ducked under the voice.
Build: `npx hyperframes init ma-vsl --example kinetic-type`, then lint -> inspect -> preview -> render.
Prompt template given for a 7 s VSL (offer, target, problem in their words, action, images; 4-row table
with text ≤ 6 words, visual, motion, trigger word; tutoiement; no number not provided; 3 hooks to choose).
Credit: derived from Agence OOO's long VSL guide.

## 2. pdoom-video (https://github.com/mexicat/pdoom-video)

What it is: a generative music video for the song "I'm Upping My P(doom)" (Suno "Claude-Pop" version),
made with Claude in Claude Code. **TypeScript + three.js (bun + Vite), not Remotion, not HyperFrames.**
Every frame is a pure function of song time; offline render = headless Chrome -> raw frames -> ffmpeg,
1920x1080 60 fps (or 4K), with adaptive motion blur (4..324 sub-frames per frame). 17 scene modules
("plates"), `src/timeline.ts` anchors cuts to lyric lines snapped to the beat grid
(`cut(q)` = last beat at/before the first word of a line; `after(q)` = nearest downbeat to a line end).
Python analysis (Demucs stems, CTC forced alignment + Whisper, librosa) produced `data/audio.json`
(132.007 BPM, beats, downbeats, 14 sections, 100 fps envelopes rms/low/mid/high/stems, kick/snare/hat/vocal
onsets) and `data/lyrics.json` (word/syllable timings).
Style ("plates from an illustrated treatise on the end of the world"): ink #0A0A0B, bone #EEE9DF, ONE signal
orange #FF4D12 (+ ember #FF8A3D, blood #C21D0B), one 2-second acid #D8FF3C accent; Archivo (width axis
62-125, weight 300-900), IBM Plex Mono (machine voice, footnotes, HUD), Cormorant italic (rare), plotter
single-stroke fonts; engraving/hatching shaders, bloom only on the signal colour, halation, grain 0.055,
vignette 0.35, chromatic aberration 1.2 px, flash/shake/zoom post params. Recurring motifs: the spark
(orange point dragging a line through every plate), the number readout that blows up full-screen on each
hook, the prompt field with next-token distributions, deadpan footnotes, bureaucratic stamps, crop marks
only at the bookends, last frame == first frame (seamless loop via a "Regenerate" rewind).
Beat sync: hard cuts on downbeats, hits on kicks/snares (`audio.hit(kind, t, halfLife)` decaying pulses),
camera moves easing INTO downbeats, karaoke words highlighted exactly at their start (dim anticipation
<= 0.4 s allowed, never ahead of the voice). Strong eases (outExpo, inOutCubic), hold then snap.
License: code MIT (Giacomo Magnanini 2026); fonts OFL; **the song, lyrics and data/lyrics.json are NOT
covered** (belong to osmarks / MusicPerson / Suno version by @slimer48484). => do not use `audio/pdoom.mp3`
in a brand video.

### What ports to HyperFrames (our house: gen.py -> template.html, GSAP paused timeline, kit FB.*)
| pdoom piece | HyperFrames port |
|---|---|
| `timeline.ts` cut()/after() | Python helpers in gen.py: `cut(word_t)` = floor to beat grid, `after(t)` = nearest downbeat; scene starts from TTS words |
| `audio.json` schema + `hit()` pulses | `beats.py` -> grid.json; gen.py emits `tl.to(..., {scale:1.03, duration:4/30})` at each beat / kick |
| HOOK slam (one word per hit, width stretch, number blow-up) | DOM text + GSAP fromTo scale/scaleX (DejaVu has no width axis -> scaleX + letter-spacing) |
| P(doom) instrument (maths label, rolling digits, tick bar, footnote) | DOM digit drums (translateY per digit column) -> cost readout 80-150 € -> ≈ 0,50 € |
| the spark + fuse burn | SVG circle + gradient halo + path with stroke-dashoffset; seeded ember particles (mulberry32 in gen.py, positions baked) |
| prompt field + token distributions | kit `FB.type` + small bar rows (bars only, no invented numbers) |
| leftturn Gantt + stamps | kit `FB.sticker`/stamp() on beats |
| dense (typographic pressure) | stacked copies with scaleX squeeze on each beat |
| bureau invert plate | swap a full-frame paper div (#EDEDED) with ink type |
| post: flash/shake/zoom/vignette/grain | #flash div, stepped x/y on #stage, scale punch, radial-gradient vignette, grain = noise PNG tile with per-frame stepped background-position (deterministic) |
| crop marks + loop seam | 4 SVG corner marks, last second recomposes frame 0 |
Not portable / skip: three.js raymarched rooms, GLSL engraving/hatching, adaptive sub-frame motion blur
(use a short CSS blur on whips), Demucs/CTC pipeline (~4 GB models, too heavy for this box).
Determinism rules are the same as HyperFrames' (no Math.random / Date.now at render time; seed everything).

### Palette mapping into CHARTE.md
| pdoom | role | charter |
|---|---|---|
| ink #0A0A0B / ink2 #151517 | bg / panels | #0a0a0f / #111117 |
| bone #EEE9DF | type, paper plates | #EDEDED |
| graphite #5E5B57 / ash #9C978F | hairlines / dim text | #232330 / #8A8A8A |
| signal #FF4D12 | the spark, the stressed word | **gold #eab308** |
| ember #FF8A3D | hot core | gradient #fff3b0 -> #eab308 (#FF8A3D is a DEAD charter value, never use) |
| blood #C21D0B | shadow of the accent | #b7791f (dark gold, already in template `.g`) |
| Plex Mono machine voice | HUD, footnotes | DejaVu Sans Mono Bold in **violet #8b5cf6** |
| acid #D8FF3C (one-off accent) | **banned (green)** -> one violet full-field flash at the offer reveal |
| (no red in pdoom except blood) | | #ff6b6b only for slow / false (2 H, TROP LENT, struck 80-150 €) |

## 3. Offers (only what is stated on the pages, fetched 2026-10-02)

**Chosen: ShortForge** — skill Claude Code. Sources: https://automatisationboost.com/ (block "L'outil") and
https://videoboost.automatisationboost.com/vente.html
- Promise: paste a text brief, get a complete vertical video (cloned voice, animated avatar, synced
  captions), 1080x1920 30 fps, 25-35 s, ready for TikTok/Reels/Shorts. "ShortForge fait les six étapes
  (écrire, filmer, monter, sous-titrer, exporter, publier) à partir d'un paragraphe" — vs "deux heures".
- Deliverables: full skill, 10 formats x 10 art directions, solved pitfalls, config.json (colours, voice, CTA).
  One-time shoot: 30 s of voice + 45 s face cam.
- Price: **67 € prix fondateur, puis 97 €**, paiement unique, mises à jour incluses, garantie 14 jours.
- Numbers stated: ≈ 0,50 € API per video vs 80-150 € freelance editor; 100 € (2 h at 50 €/h);
  "rentabilisé après 2 vidéos". Render 3-8 min per 30 s. Needs Claude Code, Node 20+, ffmpeg, WaveSpeed key.
- Target: freelances & consultants, agences & studios, créateurs & formateurs.
- Why it is the best VSL subject: it is literally the "Option 2" of the VSL page, it sells a VIDEO tool with
  a VIDEO (the format is the proof), it has a public price, a guarantee and a sales page to DM.
Alternatives:
- Formation IA « 6 défis, 6 livrables » — 29,90 € (97 € barré), paiement unique, accès à vie, remboursé
  14 jours — https://automatisationboost.com/formation.html (gate FORMATION already exists IG+FB).
- Audit gratuit (7 questions, 2 min, rappel sous 48 h) — https://automatisationboost.com/audit.html
  (best for local-business targets; free, so no price slide).
- /horror-beatsync-video skill — 19,90 € — https://automatisationboost.com/skills.html
  (the page's "+20 % de viralité" claim should NOT be repeated: not substantiated in the sources).
Repo: `automationboost/` submodule is empty in this checkout; no other price source in the repo.

## 4. Music (measured with beats.py; ffmpeg 16 kHz mono decode)

| track | license | BPM / beat | first beat / downbeat | notes |
|---|---|---|---|---|
| **hook-epical-drums-02-80** (chosen) | Mixkit free | **120.0 / 0.500 s, bar 2.000 s** | beat 0.495, downbeat 1.995 (+2k) | manifest says 80 BPM: measured grid is 120 (energy jumps at 49.995, 57.995, 69.995, 113.995 are all multiples of 4 s from the downbeat, not of 3 s). **Decay 55.5 -> 57.5 s (-43 dB) then full hit at 57.995** = countdown + detonation. Voice band share -18.7 dB (very transparent). start_gain_db -14.5 |
| food-cat-walk-128 | Mixkit free | 130.0 / 0.4616 s, bar 1.846 s | beat 0.215, downbeat ambiguous (0.677?) | kick enters ~14.5 s, medium fills from 28.4 s, breakdown 59.8-87.5, re-drop 88.37. Voice band -13.0 dB (busier) |
| journal-digital-clouds-128 | Mixkit free | 129.0 / 0.4651 s, bar 1.860 s | 0.145 | jumps 29.9, 67.1, 95.0; nappes 950-1900 Hz (manifest warns) |
| bgm-cyberpunk-city | Mixkit free | 100.0 / 0.600 s, bar 2.400 s | 0.110 | headroom -9.3, needs sidechain |
| pendant-que-tu-dors-v1 (Tony) | Tony's own | 132.0 / 0.4545 s | beat 0.225 (same grid as pdoom!) | full song with vocals (voice band -10.1 dB): unusable under VO; usable for a pdoom-style karaoke cut without VO |
| pendant-que-tu-dors-v2 (Tony) | Tony's own | 133.0 / 0.4512 s | 0.070 | same remark; drops 14.5, 43.4, 104.7 |
| pdoom.mp3 | **not licensed** | 132.0 (ref 132.007) / 0.4545 | 0.238 | validation only |
| valse-des-fleurs-maison-* | house phonogram | 180 (3/4), **bar = 1.000 s exactly** (from score.mjs) | 0.000 | 35.4 s; tutti for a hook without speech, évidée = most transparent bed; waltz, not "energetic" |

Chosen window: file 30.000 -> 62.000 s = video 0 -> 32 s; video downbeats at every even second.
Mix (bgm README): +8 dB during the voiceless first second, ramp to start_gain_db (-14.5) in 400 ms,
sidechain under the voice, voice at -16 LUFS, master -16 LUFS; `amix normalize=0`; `-nostdin`.

## 5. Blotato gates (read-only listing, 33 automations, 2026-10-02)
Existing keywords: GPT, WAN, LINKEDIN, EFFACER, PROMPT, INVISIBLE, LOOKS, FORMATION, PFA, MEMOIRE, BOOST,
SKILLZ, STAR (IG -> ShortForge vente.html, "67 €"), CHAOS, ECOM, TRAILER, TELE, SITE, HOOK, YAPPING, CONTENU,
TURBO, MACHINE, VIDEOBOOST (IG -> ShortForge, but FB -> a Seedance template: inconsistent), SEEDANCE.
No gate for FORGE or VSL. Proposed: **FORGE** -> vente.html, to create on IG 54617 + FB 43538 before posting.

## Open questions for Tony
1. Offer OK = ShortForge? (alternatives: Formation 29,90 €, Audit gratuit).
2. Founder price wording conflicts: home says "20 places, puis 97 €"; vente.html hero says "10 premiers",
   its footer says "20 premiers acheteurs". Which one goes on screen? (storyboard says only "prix fondateur").
3. Keyword FORGE (new gate IG + FB) or reuse STAR (exists on IG only, its DM has a MrBeast joke)?
4. "Combinant pdoom": style only (our plan), or did you want the pdoom SONG? It is not licensed for a brand
   video. Your own track `pendant-que-tu-dors` sits on the exact same 132 BPM grid but has vocals, so it only
   works as a pdoom-style karaoke cut with no VO (lyrics needed).
5. Length: 32 s (VSL page caps short VSLs at 30 s) or the 46 s variant?
6. Avatar: pure motion design (VSL page: "sans tournage"), or the BUREAU neon circle (A1/B1) on step 2 /
   C2_commente_motcle on the CTA? One decor only (CHARTE §4); lips must move only while the voice speaks.
7. Proof frames: six real frames from published ShortForge videos (Veille, Storytime, Démo produit,
   Comparatif, Étude de cas, Vitrine) — which renders/paths?
8. Music: hook-epical-drums-02 (chosen, house "hook puissant" track) — please listen to 30-62 s once
   (the library was qualified by measurement, never listened to, per the bgm README).

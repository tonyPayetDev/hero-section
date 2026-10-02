# VSL ShortForge x pdoom — storyboard v1 (pre-production, not rendered)

- Format: 9:16, 1080x1920, 30 fps, HyperFrames (HTML + one paused GSAP timeline).
- Length: **32.000 s = 16 bars = 960 frames.** Why not 45-75 s: the VSL page itself caps the short VSL at
  7 / 15 / 30 s ("quand il faut rassurer" = 30 s) and hook-puissant-branded is a ~30 s structure.
  We use the 30 s grid + a 4 s CTA hold after the climax (VSL rule: the action stays on screen to the end).
  A 46 s variant is described at the bottom.
- Offer: **ShortForge** (skill Claude Code) — source https://videoboost.automatisationboost.com/vente.html
  and home https://automatisationboost.com/ (block "L'outil"). Every number on screen comes from those pages.
- Music: `autoboost-neon-videos/_shared/bgm/hook-epical-drums-02-80.mp3` (Mixkit Free License, house track
  for "hook puissant / action"), **window 30.000 -> 62.000 s of the file** (`-ss 30 -t 32`).
  Measured grid: **120.0 BPM, beat 0.500 s (15 frames), bar 2.000 s (60 frames)**, downbeats of the file at
  1.995 + 2k s, so in the window **video downbeats fall on 0, 2, 4 ... 30 s** (-5 ms, inside one frame).
  Key event: the music decays from video 25.5 s (file 55.5) to near silence at 27.5 (-43 dB) and
  **re-enters full at video 28.000 (file 57.995)** -> countdown in the decay, detonation on the re-entry.
  Energy: steady -16/-17 dB bars 0-13 s, softer -19/-21 dB 14-26 s (under the dense VO), silence, hit at 28.
- CTA keyword: **FORGE** (free: not in the 33 existing Blotato gates checked 2026-10-02). The gate must be
  created on IG (account 54617) AND FB (account 43538) BEFORE publishing, DM -> vente.html.
- Charter: bg #0a0a0f, gold #eab308 = the pdoom "signal" colour, violet #8b5cf6 = machine/mono voice,
  #EDEDED type, red #ff6b6b only for "slow / false" (2 H, TROP LENT, 80-150 EUR struck). No green, no emoji.
  Type: DejaVu Sans Bold (display, "AB Sans"), DejaVu Sans Mono Bold ("AB Mono") for the pdoom machine voice.
- Notation below: `t` = video seconds. `b` = beat index (t / 0.5). Word-level slams are pinned to the
  **TTS word starts** (transcribe after TTS), never ahead of the voice; scene cuts are pinned to downbeats.

## Grid of the window (video time)

| bar | t start | file t | energy | role |
|---|---|---|---|---|
| 0 | 0.0 | 30.0 | -17 dB | visual hook + verbal hook |
| 1 | 2.0 | 32.0 | -16 | verbal hook |
| 2 | 4.0 | 34.0 | -17 | relance |
| 3-4 | 6.0-10.0 | 36-40 | -16/-15 | problem + cost |
| 5 | 10.0 | 40.0 | -16 | offer reveal |
| 6-8 | 12.0-18.0 | 42-48 | -17/-19/-21 | method 3 steps (music softens) |
| 9-10 | 18.0-22.0 | 48-52 | -20/-17 | proof + cost instrument |
| 11-12 | 22.0-26.0 | 52-56 | -20/-19 | price + CTA |
| 12.75-13 | 25.5-28.0 | 55.5-58 | -22 -> -43 | countdown in the decay, 27.5-28.0 = freeze |
| 14-15 | 28.0-32.0 | 58-62 | -15/-17 | DETONATION + CTA hold + loop seam |

## Scenes

### S0 — Hook visuel · 0.000-1.000 (b0-b1)
- Frame 0 is already moving (VSL rule 1). Full-frame **"2 H"** in red #ff6b6b, DejaVu Bold 900 px, mid-slam
  (scale 1.18 -> 1, 8 frames, `expo.out`), shake 6 px decaying, crop marks at the 4 corners (pdoom bookend frame).
- t 0.500 (b1): the **gold spark** (pdoom motif: white-hot core, gold halo, 1 px trail) streaks in from the top
  edge and cuts "2 H" horizontally; the two halves slide apart and char to ash (pdoom `fuse`: glyph opacity
  wipes behind the spark + 12 ember particles, seeded).
- Mono footnote bottom-left, 26 px violet: `fig. 1 · hook visuel` (deadpan pdoom footnote = the light "meta").
- On-screen text: `2 H`
- VO: none (music +8 dB on this second, ramp down 400 ms into the voice — bgm README trap).
- SFX: `sfx-impact-deep` @0.000, `sfx-glitch-hard` @0.500.
- pdoom: hook slam + fuse. VSL page: "l'accroche se joue dans la première seconde", image forte + 3-5 mots max.

### S1 — Hook verbal · 1.000-4.000 (b2-b7)
- pdoom **HOOK slam**: one word (or group) per sung word, full-frame, white #EDEDED on ink; the stressed word
  in gold. Groups: `TU SAIS` / `QU'IL FAUT` / `POSTER` / `TOUS LES JOURS.` — each lands on its TTS word start;
  POSTER rises (letters shoot upward, pdoom "UPPING"); TOUS LES JOURS condenses under pressure
  (scaleX 1.15 -> 0.82 with tracking -0.04 em, pdoom `dense`).
- Hard cut on downbeat 2.000 between groups 2 and 3 (camera reframe: zoom 1.0 -> 1.08 punch).
- VO: « Tu sais qu'il faut poster tous les jours. » (8 words)
- SFX: `sfx-thwip` on each slam (-20 dB).
- pdoom: hook typographic slam, width/pressure animation. VSL: problème dit avec les mots de la cible.

### S2 — Relance · 4.000-6.000 (b8-b11)
- Hard cut on downbeat 4.000 to the **inverted plate** (pdoom bone-paper / ink rhythm): paper #EDEDED, ink
  #0a0a0f type. `TU NE LE FAIS PAS.` — `PAS.` stamped like the pdoom "SAFE ENOUGH" rubber stamp:
  rotation -7 deg, ink texture, shake 10 px, on its word start.
- Mono footnote: `fig. 2 · la relance (hook n°2)` — this is the hook-stacking "explication légère", told
  as a footnote so it costs no VO time.
- VO: « Tu ne le fais pas. » (5 words — the site's own headline)
- SFX: `sfx-landing-thud` on PAS.
- pdoom: invert + bureau stamp. VSL 30 s: "relance au bout de 2 secondes (un deuxième mot fort, un changement
  d'image)". Hook skill: verbal hook stacked within 3-4 s.

### S3 — Problème + coût · 6.000-10.000 (b12-b19)
- Back to ink. pdoom **leftturn Gantt strip**, vertical for 9:16: six milestones stacked top -> bottom
  `ÉCRIRE · FILMER · MONTER · SOUS-TITRER · EXPORTER · PUBLIER`, each stamped on a beat
  (6.0, 6.5, 7.0, 7.5, 8.0, 8.5) while the spark (playhead) runs down the strip.
  A mono clock readout (violet) rolls `0:00 -> 2:00` = "deux heures" (source: vente.html).
- t 9.000 (b18): kit sticker **TROP LENT** (variant red) slams, rot -6.
- VO: « Écrire, filmer, monter, sous-titrer, exporter, publier. Deux heures. » (8 words)
- SFX: `sfx-click` per milestone (-22 dB), `sfx-impact` @9.0.
- pdoom: Gantt / roadmap stamped per beat, deadpan instrument. VSL: "le problème, puis ce qu'il coûte".

### S4 — Révélation de l'offre · 10.000-12.000 (b20-b23)
- Downbeat 10.000: the spark pulls the six milestones into ONE block (they collapse, `power4.in`, 10 frames),
  then a **violet full-field flash** (replaces pdoom's one-time "acid" accent, which is green and banned) and
  `SHORTFORGE` assembles: letters widen scaleX 0.6 -> 1 with an elastic wave (kit `FB.elastic`), gold gradient.
  Mono tag under it: `skill Claude Code`.
- VO: « ShortForge fait les six étapes. » (5 words)
- SFX: `sfx-whoosh-v2` @9.7, `sfx-chime-v2` @10.0.
- pdoom: collapse to the spark, single-accent moment. VSL: une seule couleur d'accent sur le mot qui compte.

### S5 — La méthode en 3 étapes · 12.000-18.000 (bars 6-8, one bar per step)
- Same transition direction every time (VSL rule 4): everything exits LEFT, enters from RIGHT.
- 12.000-14.000 **Étape 1** — pdoom **prompt field**: one thin field, a brief typed in mono token by token;
  above each new token a tiny distribution of 3-4 candidate tokens with bars **(bars only, no numbers:
  invented probabilities would break the "aucun chiffre inventé" rule)**; caret, `⏎` on beat 13.5.
  Label `1 · TU COLLES UN BRIEF`. VO « Tu colles un brief. » (4) — SFX `sfx-click-soft` per token, `sfx-confirm` @13.5.
- 14.000-16.000 **Étape 2** — three layers stack on beats 14.0 / 14.5 / 15.0: an oscilloscope trace that
  rides the VO (pdoom `spacetime` scope, gold), the neon avatar circle (kit layout 1, clip A1 or B1 muted —
  optional, see open questions), a caption plate with word-by-word highlight.
  Label `2 · VOIX · AVATAR · CAPTIONS`. VO « Ta voix clonée, ton avatar, les captions. » (7) — SFX `sfx-pop` x3.
- 16.000-18.000 **Étape 3** — a 9:16 phone outline drawn by the spark (stroke-dashoffset), `1080 × 1920`
  mono label, stamp `PRÊT À POSTER` on 17.0. Label `3 · UN MP4 VERTICAL`.
  VO « Un MP4 vertical, prêt à poster. » (6) — SFX `sfx-web-latch` @17.0.
- pdoom: prompt/token template, scope, spark drawing outlines. VSL 30 s: "la méthode en 3 étapes, un plan par étape".

### S6 — Preuve · 18.000-22.000 (bars 9-10)
- 18.000-19.500: pdoom **outro rewind montage**: six REAL frames of published videos (Veille, Storytime, Démo
  produit, Comparatif, Étude de cas, Vitrine — the six of the sales page), one per half-beat
  (18.0, 18.25 ... 19.25), slight zoom each, crop marks; 19.5-20.0 hold + mono `6 formats · vidéos publiées`.
- 20.000-22.000: pdoom **P(doom) instrument blown up full-screen**, repurposed as a cost readout:
  top-left maths label `coût / vidéo`, big digits roll from `80-150 €` (red, struck through on 20.5:
  "un monteur freelance") down to **`≈ 0,50 €`** (gold) landing on beat 21.0; tick bar underneath;
  mono footnote `API vocale · à ton compte` (deadpan footnote, sourced: vente.html "Le calcul").
- VO: « Six formats, déjà publiés. » (18.0-19.5) + « Environ cinquante centimes par vidéo. » (20.0-22.0)
- SFX: `sfx-zoom` per montage frame (-26 dB), `sfx-glitch-soft` @20.5, `sfx-confirm` @21.0.
- VSL: preuve = un exemple réel, jamais un chiffre inventé (needs Tony's six real frames).

### S7 — Ce que tu reçois + appel · 22.000-25.000 (b44-b49)
- 22.000: price card (kit stack card style, surface #111117, 1 px #232330): `97 €` struck (red) -> `67 €`
  gold, mono lines `prix fondateur · paiement unique · garantie 14 jours`.
- 24.000: kit **comment field**: `commente` + `FORGE` typed letter by letter (gold), cursor.
- VO: « Prix fondateur : 67 euros. Commente FORGE, je t'envoie le lien. » (11 words)
- SFX: `sfx-impact` @22.0, `sfx-click-soft` per letter of FORGE.
- Hook skill CTA « commente [MOT] ». VSL: une seule action.

### S8 — Compte à rebours · 25.000-28.000 (b50-b55)
- Music is decaying (the measured silence). Full-frame numerals `3` (25.0) `2` (26.0) `1` (27.0), pdoom hook
  n=4 "maximal": each numeral stamps with 3 stacked copies in alternating flat tones (gold / violet / ink,
  no outlines), zoom punch 1.12 and shake, the previous numeral shatters into lines.
- **27.500-28.000: freeze** — 15 frames, nothing moves, only the spark breathes at frame centre
  (VSL rule: "un court temps d'arrêt avant le moment fort").
- VO: « Trois. » @25.0 « Deux. » @26.0 « Un. » @27.0
- SFX: `sfx-impact-deep` on each numeral (-18, -16, -14 dB rising), nothing at 27.5.

### S9 — Climax + CTA tenu · 28.000-32.000 (bars 14-15)
- 28.000 = file 57.995, music re-enters: the spark **detonates** (pdoom outro): white flash 0.8 -> 0 over
  6 frames, radial line burst (seeded 64 lines), shake 14 px, then `COMMENTE` (white) / `FORGE` (gold,
  huge, 300 px) alone on screen, centred, kept clear of the TikTok/IG UI zones, held to the end.
- 28.0-31.0: subtle beat pulse on FORGE (scale 1.00 -> 1.03 on every beat, 4 frames) = "suit le rythme".
- 31.000-32.000: crop marks close back in from the corners and the frame settles on the exact layout of
  frame 0 (pdoom "Regenerate" loop seam), so the reel loops cleanly.
- VO: « Action. » @28.0 (hook skill: « 3, 2, 1, action »)
- SFX: `sfx-impact-deep` + `sfx-glass-break` @28.0, `sfx-whoosh-lat` @31.0. Music fade-out 31.5-32.0.

## Full VO script (French, for the TTS clone — no straight double quotes)

```
Tu sais qu'il faut poster tous les jours.
Tu ne le fais pas.
Écrire, filmer, monter, sous-titrer, exporter, publier. Deux heures.
ShortForge fait les six étapes.
Tu colles un brief.
Ta voix clonée, ton avatar, les captions.
Un MP4 vertical, prêt à poster.
Six formats, déjà publiés.
Environ cinquante centimes par vidéo.
Prix fondateur : 67 euros. Commente FORGE, je t'envoie le lien.
Trois. Deux. Un.
Action.
```
~66 words over ~27 s of speech windows (2.6 w/s target from the formation, atempo 1.09 per CHARTE).
Generate line by line (one TTS call per scene) so each line can be placed on its scene start; then
transcribe for word timings and pin the slams to them.

## Source check for every on-screen claim

| Claim | Source |
|---|---|
| Tu sais qu'il faut poster tous les jours. Tu ne le fais pas. | home + vente.html headline |
| écrire, filmer, monter, sous-titrer, exporter, publier · deux heures | vente.html |
| fait les six étapes à partir d'un paragraphe | vente.html |
| voix clonée, avatar, captions, 1080x1920, prêt pour TikTok/Reels/Shorts | home + vente.html |
| six formats (Veille, Storytime, Démo produit, Comparatif, Étude de cas, Vitrine) réellement publiés | vente.html |
| 80-150 € monteur freelance · ≈ 0,50 € API par vidéo | home + vente.html "Le calcul" |
| 97 € -> 67 € prix fondateur · paiement unique · garantie 14 jours | home + vente.html |

## Variant 46 s (if Tony wants the longer cut)
Window file 16.0 -> 62.0 (still landing the detonation on file 57.995 = video 41.995 ≈ 42.0). Add 7 bars
before S3: a pdoom `dense` scene (the six steps repeated until the title-safe box is a solid slab), the
"Pour qui" trio from vente.html (freelances & consultants / agences & studios / créateurs & formateurs),
and the "Un seul tournage, à vie : 30 s de voix, 45 s face caméra" plate.

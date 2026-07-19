# SFX palette v1 — Autoboost Neon Video

Reusable sound-design palette, extracted from **#37 Fable** (render `public_2026-07-19_15-09-59.mp4`,
scheduled 2026-07-26). Validated by Tony on 2026-07-19.

**This folder is frozen.** Do not edit the files or the volumes below — later tweaks go into
a new `../v2/` folder so every past video keeps the exact palette it was rendered with.

## How to reuse

1. Copy `assets/sfx-*.mp3` into the new project's `public/assets/`.
2. Add one `<audio>` tag per hit in the composition, using the roles and volumes below.
3. Re-time `data-start` to the new video's own cuts — the roles carry over, the timestamps do not.

```html
<audio id="sfx-hook" src="assets/sfx-glitch-hard.mp3" data-start="0.10" data-volume="0.26"></audio>
```

## Roles → sound → volume

| Role | File | Volume | Notes |
|---|---|---|---|
| Hook puissant (0s) | `sfx-glitch-hard.mp3` + `sfx-impact.mp3` | 0.26 / 0.20 | layered, the two fire together |
| Hook propre (2nd hook) | `sfx-glitch-soft.mp3` | 0.15 | softer variant, avoids fatigue |
| Apparition d'un chiffre | `sfx-notify.mp3` | 0.16 | interface hint |
| Début de phrase / point clé | `sfx-click.mp3` | 0.18 – 0.20 | sci-fi click |
| Transition principale (coupe) | `sfx-zoom.mp3` | 0.17 – 0.19 | air zoom vacuum, see re-cut note |
| Transition latérale | `sfx-whoosh-lat.mp3` | 0.16 | arrow whoosh |
| Éléments en cascade | `sfx-click-soft.mp3` ×N | 0.13 | ~0.25 s apart |
| Validation / preuve | `sfx-confirm.mp3` | 0.18 | |
| CTA final | `sfx-pop.mp3` + `sfx-impact.mp3` | 0.24 / 0.18 | layered |
| Sous-titre du CTA | `sfx-click-soft.mp3` | 0.13 | |
| (spare) | `sfx-whoosh-v2.mp3`, `sfx-chime-v2.mp3` | — | unused in v1, kept as alternates |

## Two things that took a while to get right

**Whoosh alignment.** The raw cinematic whooshes are 5.5 s long with their peak at 2.5 s.
Dropped in as-is, the impact lands well after the cut. They are re-cut so the peak falls
*exactly* on the cut — i.e. start the clip ~1.2 s before the cut, not on it.

**Volume ceiling.** Everything sits between 0.13 and 0.26 so the SFX never eat the voice.
If Tony says "je n'entends pas les SFX", this is the first knob to raise — raise the whole
table proportionally rather than individual hits.

**BGM interaction.** With the trend track `flowers_horror.mp3` (-12.4 LUFS) the music itself sits
at `data-volume="0.05"`. A quieter bed like `bgm-ascension.mp3` (-19.1 LUFS) can go to ~0.09.
Measure the track before choosing — the two are 7 dB apart.

## Superseded version (kept for reference, not deleted)

**v0 — the 4-SFX pass** used on `public_2026-07-18_14-38-56.mp4` and earlier renders:
whoosh at 3.80, 10.90, 16.40 and a chime at 20.40. Those renders still live in
`autoboost-37-fable/renders/` and in the `/fable-sfx` preview page as "avant". Nothing was
overwritten — v0 is simply not carried forward into new videos.

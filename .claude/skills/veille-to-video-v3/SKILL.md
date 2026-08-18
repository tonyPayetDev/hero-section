---
name: veille-to-video-v3
description: VideoBoost v3 — génère une vidéo sociale 9:16 en ASSEMBLANT des micro-clips d'une banque d'avatar Tony (24 clips talking-head réutilisables, identité verrouillée Seedance) sélectionnés par rôle narratif (hook/explication/CTA), avec voix clonée ElevenLabs (lip-sync conservé), captions et habillage. NE REMPLACE PAS veille-to-video (v2) — c'est un pipeline distinct basé sur une banque de clips réels, pas une compo HTML avatar-still.
---

# veille-to-video-v3 — Assemblage par banque d'avatar

**Distinct de v2 (`veille-to-video`)** : v2 = compo HyperFrames néon + avatar en cercle (image fixe).
v3 = **vraie vidéo de Tony** découpée en 24 micro-clips réutilisables, réassemblés par rôle. Ne pas
modifier v2.

## Principe

`Sujet → Hook (A) → [B-roll] → Explication(s) (B) → CTA (C) → voix ElevenLabs → captions/DA → montage → 9:16 final`

Une vidéo = une séquence de clips de la banque dont les phrases forment le script, cuts invisibles
grâce à la **seconde neutre** en début/fin de chaque clip. L'audio de chaque clip est remplacé par
le **clone voix ElevenLabs** de Tony (le mouvement des lèvres reste calé car même texte).

## La banque

`/work/autoboost-neon-videos/_shared/avatar-bank/`
- `manifest.json` — 24 clips taggés `role / gesture / energy` + specs (voir clés `role`, `energy`, `spoken`, `targetDuration`).
- `seedance-prompts.md` — MASTER PROMPT + 24 blocs PERFORMANCE prêts à générer.
- `refs/` — 2 avatars de référence (`hf-avatar-2-portrait.png` = hooks/dramatique ; `hf-avatar-1-desk.png` = explications). **Utiliser UNE seule réf par vidéo** pour la continuité visuelle.
- `clips/` — les .mp4 générés (`A1_*.mp4`, `B1_*.mp4`, ...).

Catégories : **A** = hooks (6, énergie haute), **B** = explications (12, moyenne), **C** = CTA (6).

## Générer les 24 clips — SUR LE WEB (gratuit)

⚠️ Économie (2026-08-14) : Seedance 2.5 via l'API Higgsfield = **32,5 crédits/clip** et l'**unlim
n'est PAS supporté par l'API** (erreur `Unlimited generations aren't supported for seedance_2_5`) →
24 clips = ~780 cr, hors budget. **Seedance Unlimited est gratuit uniquement sur le web.**
→ Tony génère les 24 sur son web Seedance Unlimited avec `seedance-prompts.md`, les nomme
(`A1_hook_frontal.mp4`…), et les dépose dans `clips/`.

Depuis l'API (test/dépannage seulement), la recette qui MARCHE (validée job `7be338a9`) :
`generate_video` model `seedance_2_5`, **`mode: "omni_reference"`** (obligatoire, sinon 422
`t2v does not accept reference media`), `medias:[{role:"start_image", value:<media_id de la réf>}]`,
`duration:5`, `aspect_ratio:"9:16"`. Importer la réf via `media_import_url`. Sortie 720×1280 avec
audio Seedance (à remplacer par ElevenLabs).

## Voix — ElevenLabs (clone Tony)

Enregistrement source 3-5 min (script dans le protocole). `voiceId` à stocker dans
`manifest.json > voice.voiceId` une fois le clone créé. En attendant, fallback = voix de marque
WaveSpeed (webhook `tts-gen`, voir v2) — lip-sync approximatif.

## Assemblage (ffmpeg)

1. Sélectionner 1 A + N B + 1 C selon le sujet (tags du manifest).
2. Trim chaque clip pour retirer ~0,5 s de neutre en tête et ~0,6 s en queue (garder 3-4 s parlés).
3. Concat (cut sec — les frames neutres rendent la coupe invisible).
4. Remplacer l'audio par la voix ElevenLabs du script complet (ou garder l'audio Seedance pour un
   proof of concept).
5. Captions (lower-third), BGM basse sous la voix, habillage léger (marque AutoBoost).
6. Upscale 720×1280 → 1080×1920, export h264+aac.
7. Publier sur previsualisation, puis Blotato (mêmes règles que v2, voir son SKILL.md Étape 8).

## Pièges compositing HyperFrames + ffmpeg (PROUVÉS 2026-08-14, veille-to-avatar-v3)

Archi validée = **2 passes** (car HyperFrames fige sur toute balise `<video>`) :
1. **Passe 1 — HyperFrames rend l'habillage, `videoCount:0`** : fond néon, ligne néon beat-sync,
   captions mot-à-mot 27px, cartons, **b-roll en CSS natif** (schémas à nœuds, mockups fenêtre/terminal),
   + une **fenêtre média** placeholder noire (rectangle fixe) où l'avatar sera posé. Captions placées
   HORS de la fenêtre média (ex. bande à `top:1400`, fenêtre média `top:176→1326`).
2. **Passe 2 — ffmpeg** overlay les vrais clips avatar dans la fenêtre au bon timing.

Pièges confirmés :
- **`</style>` manquant = body avalé par le CSS** → rendu blanc + erreur trompeuse
  `window.__hf not ready / player=false` (ressemble à un bug de timeline). Vérifier la fermeture des balises AVANT de suspecter le runtime.
- **`audioCount:0`** possible (renderer 0.7.5 ignore les `<audio>` de la comp) → gérer **TOUT l'audio en passe 2 ffmpeg** (voix + BGM 0.09 + SFX), plus fiable.
- **`snapshot` inutilisable ici** (runtime jamais ready, frames blanches) alors que `render` marche → vérifier via frames extraites du vrai mp4, jamais via snapshot.
- Root sans `class="clip"` (le StaticGuard le réclame en warning mais les comps qui rendent l'omettent).
- **Recette de sync** : trim `ss` de chaque clip pour aligner clip-time et voix concaténée ; overlay
  `setpts=PTS-STARTPTS+OFFSET/TB` + `enable='between(t,a,b)'` ; outro figé `tpad=stop_mode=clone`.
  Le b-roll rendu nativement dans la base est "révélé" en n'overlayant PAS l'avatar sur sa fenêtre.
- Détail : ~0,55s de fenêtre noire au tout début (avatar pas encore là) → pré-rouler la tête neutre de A1 pour supprimer.

### ⚠️ Lèvres immobiles sous une voix active (PIÈGE PAYÉ 2026-08-18, `videoboost-dialogue`)

Tony a rejeté un montage validé par ailleurs : *« à 10 secondes et 23 secondes petit blanc,
la voix parle mais les lèvres ne bougent pas »*. **Les clips de la banque sont des prises continues :
ils ne parlent PAS de bout en bout.** `A1_hook_frontal` — le plus utilisé — est muet sur
**0,00–0,67 s et 4,58–5,06 s**. Trois plans débordaient dans ces zones mortes sous une voix active
(0,33 à 0,37 s chacun). Invisible en relisant le script, très visible à l'écran.

**Règle** : un plan avatar posé sous une voix active doit tenir **entièrement** dans une plage
« lèvres actives » du clip source :

```
ss >= zone.start   et   ss + (N_images/30)*vitesse <= zone.end
```

Les zones mortes restent utilisables **quand la voix se tait**, sous une réplique d'extrait tiers,
ou sous un plan de coupe.

**Outils** (dans `/work/autoboost-neon-videos/_shared/avatar-bank/`, voir `LIPS-MAP.md`) :
- `build-lips-map.mjs` → régénère `lips-map.json`. **À relancer à chaque ajout de clip dans la banque.**
- `check_lips_rule.mjs` → garde-fou : lit les params de plans dans `order.json`, croise avec la carte
  et l'enveloppe RMS de la voix, **exit 1** si un plan dépasse 6 images fautives.
  **À lancer après le build, avant l'assemblage.**

**Correction sans tout refaire** : ne bouge que `ss`, jamais le nombre d'images → aucun décalage
de timeline, piste audio réutilisée telle quelle (vérifié bit à bit via l'empreinte PCM décodée).

**Deux pièges de MESURE, à ne pas refaire** :
1. Ne mesure jamais la bouche dans une **boîte fixe du cadre de sortie** : le zoom/offset change à
   chaque plan, donc sur les plans larges tu mesures le torse et tu conclus à tort à une immobilité.
   Mesure la **fenêtre source**, ou recalcule la boîte depuis le zoom/offset du plan.
2. Banque en **24 fps**, rendus en **30 fps** → une image sur cinq est dupliquée, du mouvement `0.00`
   isolé est normal. Seules les **séries continues** (> ~6 images) sont des défauts.

## STYLE VERROUILLÉ (réf `veille-to-avatar-v3-v3`, validé 2026-08-15)

Tony a validé `previsualisation/veille-to-avatar-v3-v3` (« c'est ok nickel, verrouillé »).
C'est LE standard reproductible du pipeline v3. Projet source complet et rejouable :
`/work/autoboost-neon-videos/veille-to-avatar-v3-v3/` (scripts `work/*.sh` + `public/index.html`).
Toute nouvelle vidéo v3 REPRODUIT ces valeurs par défaut.

**Archi = 2 passes** (HyperFrames fige sur toute balise `<video>`) :
- **Passe 1** : HyperFrames rend l'habillage néon + démo HTML + captions + countdown + CTA,
  avec une **fenêtre média placeholder** (`#avatarWin`, rectangle) où l'avatar sera posé. `videoCount:0`.
- **Passe 2** : ffmpeg overlay les vrais clips avatar dans la fenêtre + muxe TOUT l'audio.

### Voix — clone Tony, DYNAMIQUE (verrouillé)  [[feedback_avatar_mute_overlay_voice]]
- Segments générés via webhook **`tts-gen`** (`https://n7n.automatisationboost.com/webhook/tts-gen`),
  **`voixUrl` OBLIGATOIRE** = `https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3`
  (sans voixUrl la branche OpenAI est HS). Consentement voix = standing, ne pas re-demander.
- **Post-traitement par segment** (`proc_voice.sh`) :
  `silenceremove` en tête ET en queue (start_threshold `-45dB`, detection `peak`)
  → **`atempo=1.12`** sur les segments parlés (countdown à `1.0`, tag final ~`1.05`)
  → `dynaudnorm=f=200:g=5`, sortie mono 48 kHz.
- **Audio natif des clips avatar COUPÉ** (`-an` au prep) : on n'entend QUE la voix clonée.
- Voix bien au 1er plan (~-13 dB / +16 dB au-dessus de la musique).

### Avatar v3 (verrouillé)
- Banque `/work/autoboost-neon-videos/_shared/avatar-bank/clips/` (A1 hook / B1 principe / C2 CTA).
- L'avatar **ponctue ~5×** (1,5–3,3 s chacun) par rôle : hook, intro-démo, punch, réalité, action/CTA.
- Fenêtre néon `#avatarWin` : `648×1152`, bord `3px rgba(255,230,0,.60)`, radius 30, badge « Live » rouge.
- Prep : `scale=648:1152 force_original_aspect_ratio=increase, crop, fps=30, -an, crf 18`.
- Overlay passe 2 : `scale=642:1146`, `overlay=219:153`, `setpts=PTS-STARTPTS+OFFSET/TB`,
  `enable='between(t,a,b)'`. Cuts invisibles grâce aux `ss`/durées choisis par clip.

### Démo reconstituée en HTML, synchronisée au script (verrouillé)
- Panneau app `#app` (titlebar mac + chip néon) avec vues qui s'enchaînent au rythme de la voix :
  **input tapé (typewriter) → clic curseur → cartes de résultat qui pop → calendrier/planif qui se remplit**.
  Chaque vue est calée sur le segment de voix correspondant (typewriter borné `typeStart→typeEnd`,
  pop des cartes en cascade `back.out`, remplissage jour par jour). Adapter le CONTENU au sujet,
  garder la MÉCANIQUE.

### Countdown 3-2-1 + claque finale (verrouillé)
- `#count` plein écran néon : ring qui pulse + chiffre `640px` `back.out(2.4)`, un chiffre par 0,55 s
  calé sur les segments `cd3/cd2/cd1` (voix « Trois. Deux. Un. » à `1.0×`).
- `#finalCTA` : lockup géant + baseline + logo AUTOBOOST, apparition `back.out`.

### Audio final (verrouillé, `build_audio.sh`)
1. **Voice bed** : chaque segment posé à son offset absolu via `adelay`, `amix normalize=0`, `apad`, `atrim`.
2. **BGM énergique en boucle** (`-stream_loop -1`), **duckée en sidechain sous la voix**
   (`sidechaincompress threshold=0.03:ratio=8:attack=8:release=320`, puis `volume=0.34`) ≈ **16 dB d'écart**.
3. **SFX sur les temps forts** : whoosh (intro), notify/pop (résultats), impacts (countdown) — volumes 0.16→0.30.
- Muxé en passe 2 : `-map "[vout]" -map "<audio>:a" -c:a aac -b:a 192k -movflags +faststart`.

### Charte & format (verrouillé)
- 9:16 `1080×1920`, matte black + néon jaune `#FFE600` / violet `#A855F7` / orange `#FF8A3D`, police Inter 700.
- **Ligne néon beat-sync** en bas (BGM ~134 BPM, `BEATP≈0.448`), captions mot-à-mot 40px contour noir.
- Durée cible **~30 s (25–40 s)**. Réf = 34,6 s.

### Env de rendu (OBLIGATOIRE, sinon texte invisible / crash)
```
export PATH="/home/claude/tools/node/bin:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/chromelibs/usr/bin:$PATH"
export LD_LIBRARY_PATH="/home/claude/tools/chromelibs/lib/x86_64-linux-gnu:/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export FONTCONFIG_PATH="/home/claude/tools/chromelibs/etc/fonts"
```
`--out` est ignoré (sortie = `public/video.mp4` après pass2). `snapshot` inutilisable ici
(runtime jamais ready) → vérifier via frames extraites du vrai mp4, jamais via snapshot.

### Diffusion (verrouillé)
- Publier d'abord sur **previsualisation** (route dédiée par variante, ne pas écraser), Tony valide au tel.
- Planifier ensuite sur **5 réseaux** (pas 3) via Blotato. [[feedback_always_5_social_networks]]

## Statut (2026-08-14)

- Banque : manifest + prompts figés, C2 = mot-clé AUTOMATION (corrigé).
- Recette Seedance API validée (1 clip test A1 OK, identité + lèvres parfaites).
- Mini-démo 3 clips (A1+B1+C2) en cours d'assemblage comme preuve du pipeline.
- Reste : Tony génère la banque complète sur le web + crée le clone ElevenLabs.

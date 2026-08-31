---
name: veille-to-video-v3
description: VideoBoost v3 — génère une vidéo sociale 9:16 en ASSEMBLANT des micro-clips d'une banque d’avatar Tony (7 clips exploitables en 2 décors, voir MANIFESTE.md, identité verrouillée Seedance) sélectionnés par rôle narratif (hook/explication/CTA), avec voix clonée ElevenLabs (lip-sync conservé), captions et habillage. REMPLACE veille-to-video (v2), mis en pause le 2026-08-20 : plus d’avatar détouré sur compo HTML. Deux décors au choix — bureau (tuto/technique) ou voiture (humour/mindset), jamais les deux dans la même vidéo. Le cercle néon jaune de la v2 est conservé comme cadrage.
---

## Toute vidéo porte son prompt — lire `FICHE-VIDEO.md`

Règle de Tony du 2026-08-25 : chaque vidéo livrée doit être accompagnée de son
prompt intégral, de ses images de référence, et de la ligne qui dit quel marqueur
remplacer par son avatar. Voir `FICHE-VIDEO.md` dans ce dossier. Une vidéo sans
son prompt ne peut être ni refaite ni déclinée.

## Charte — ne pas la redéfinir ici

**Lire `/work/autoboost-neon-videos/_shared/CHARTE.md` avant toute production.**
Palette, typographie, avatar, voix, musique, CTA et pièges de rendu y sont fixés
une seule fois. Ce skill ne redéclare aucune couleur.

**Fonds animés : piocher dans `_shared/broll-abstrait/` avant d’en créer un.**
Dix motifs existent — reseau, flux, grille, planetes, workflow, constellation,
onde, circuit, spirale, tunnel. Le README du dossier dit ce que chacun signifie.
N’en dessiner un nouveau que si aucun des dix ne dit ce qu’il faut dire.

# veille-to-video-v3 — Assemblage par banque d'avatar

**Distinct de v2 (`veille-to-video`)** : v2 = compo HyperFrames néon + avatar en cercle (image fixe).
v3 = **vraie vidéo de Tony** découpée en 24 micro-clips réutilisables, réassemblés par rôle. Ne pas
modifier v2.

## Principe

`Sujet → Hook (A) → [B-roll] → Explication(s) (B) → CTA (C) → voix ElevenLabs → captions/DA → montage → 9:16 final`

Une vidéo = une séquence de clips de la banque dont les phrases forment le script, cuts invisibles
grâce à la **seconde neutre** en début/fin de chaque clip. L'audio de chaque clip est remplacé par
le **clone voix ElevenLabs** de Tony (le mouvement des lèvres reste calé car même texte).

## ✅ C'est CE pipeline qui produit les nouvelles vidéos (décision Tony, 2026-08-20)

`veille-to-video` (v2) est **en pause** : plus de nouvelle vidéo en avatar détouré sur
compo HTML. Les agents `script-writer` et `social-analytics` pointent désormais ici.

## La banque

> ⚠️ **Le compte de 24 clips est faux.** Il y en a 7 exploitables, en deux
> tournages distincts (bureau / voiture). Lire
> `_shared/avatar-bank/MANIFESTE.md` avant de choisir : un décor par vidéo,
> et le décor doit correspondre au propos.

### Choisir le décor — c'est la première décision, avant d'écrire un plan

**La règle décide, pas le goût du moment :**

| décor | dossier | quand | clips | lèvres actives |
|---|---|---|---|---|
| **BUREAU** | `clips/` | tuto, technique, démonstration, « voilà comment on fait » | A1, B1, C2 · 5,06 s | 3,91 / 4,80 / 4,75 s → **13,5 s au total** |
| **VOITURE** | `clips-new/` | humour, mindset, opinion, « je te parle entre nous » | D1, D2, D3, D4 · 10,08 s + `D2_pointe_boucle` 3,25 s | 8,5 à 9,7 s par clip |

**Un seul décor par vidéo, jamais les deux.** Une erreur déjà payée : un storytime
technique tourné avec le set voiture — il a fallu tout refaire sur le set bureau.

**Le bureau est court.** 13,5 s exploitables sous voix active, en tout. Au-delà il faut
rejouer des segments différents du même clip (c'est ce que fait `veille-to-avatar-v3-v3` :
B1 et A1 servent deux fois, sur des plages distinctes). Si le propos demande beaucoup de
présence avatar, soit c'est un sujet voiture, soit il faut tourner du bureau en plus.

**Cartes de lèvres, une par décor** (voir `LIPS-MAP.md`) :
- `lips-map.json` → set bureau
- `lips-map-voiture.json` → set voiture, généré avec `LIPS_CROP="240,180,225,430"`
  (le cadrage bouche du studio ne convient pas : en voiture le visage est plus petit et plus haut)

⚠️ **`D1` et `D2` ont une zone morte INTERNE** vers 4,63→4,96 s, pas seulement aux
extrémités comme les clips bureau. Un plan qui la traverse sous une voix active reproduit
le défaut rejeté le 2026-08-18. Le set spider (`clips-spider/`) n'est **pas cartographié** :
ne pas l'utiliser sous voix active tant qu'il ne l'est pas.

### Cadrage de l'avatar : le cercle néon jaune est repris de la v2

Tony l'a explicitement gardé au moment de mettre la v2 en pause. Anneau jaune autour de
l'avatar en médaillon, pulse sur le beat, typiquement sur le hook. Différence avec la v2 :
il encadre ici un **clip réel**, pas un détourage sur fond vert. Spécification d'origine
dans `veille-to-video/SKILL.md`, section « Choré avatar + ligne néon ».

Autres cadrages disponibles : plein cadre, et **écran scindé vertical** (avatar 42 % à
gauche pleine hauteur, contenu à droite, filet jaune à la séparation) — voir
`autoboost-top3-outils/work/build_split.sh`. Le split exige un clip où le geste tient sur
toute la durée du plan : découper la portion utile et la boucler, sinon le clip reboucle
et le geste disparaît en cours de plan.

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

### ⚠️ Le défaut INVERSE : la bouche parle pendant le silence (PAYÉ 2026-08-28, `autoboost-serie-2-avatar`)

Tony a rejeté le split MOTEUR alors que la règle ci-dessus était **respectée** — le contrôle
avant rendu disait « tous les plans conformes », et c'était vrai. Mesuré sur le rendu :
**1,47 s où l'avatar articule sans aucune voix**, en trois moments nets (7,57 · 13,67 · 26,17 s).

La cause : chaque segment durait `voix + GAP` (0,25 s de respiration), et le plan avatar était
coupé sur cette durée totale. La voix s'arrêtait, la bouche continuait. Sur un médaillon ça
passe ; sur une **bande pleine largeur** c'est ce qui se lit comme « pas synchro ».

**Règle** : le plan sous voix s'arrête **pile à la fin de la voix**. Le silence de fin de segment
est tenu par la dernière image gelée :

```
-vf "…,tpad=stop_mode=clone:stop_duration=<GAP>"
```

Et le contrôle avant rendu doit lire **le même découpage que le rendu** (une seule fonction
partagée), sinon les deux divergent en silence — ici le contrôle validait une durée que le
rendu n'utilisait pas.

**Piège de mesure, encore un.** Pour comparer avant/après, ne recalcule **jamais** les bornes de
segments depuis les mp3 : le rendu arrondit chaque segment à l'image, la dérive atteint 0,4 s en
fin de vidéo et la mesure **invente des défauts** (elle en a signalé deux qui n'existaient pas).
Lis les bornes sur les **coupes réelles de l'image** — le plus gros saut inter-images de la bande
avatar — ou sur les durées des segments effectivement rendus.

### ⚠️ Enveloppes RMS ffmpeg — deux pièges qui faussent TOUT (PAYÉS 2026-08-18, `matrix-formation`)

Ces deux-là valent pour **toute** analyse audio par enveloppe (`astats` + `ametadata`) :
repérage de dialogue, spans de captions, garde-fou lèvres, détection de pauses.
Ils ne plantent jamais — ils rendent un résultat **plausible et faux**.

1. **`-ar` est une option de SORTIE : elle ne s'applique PAS avant `asetnsamples`.**
   Sur une source **44,1 kHz**, `ffmpeg -i src -ar 48000 -af "asetnsamples=n=4000,astats=…"`
   produit des fenêtres de 4000 échantillons **à 44,1 kHz**, donc **11,02 fenêtres/s au lieu de 12** —
   soit jusqu'à **15 s de dérive** en fin de fichier. Conclusion obtenue : « le personnage ne parle
   quasiment jamais ». Entièrement fausse.
   **Parade** : `aresample=48000` **DANS la chaîne de filtres**, et surtout **redéduire la cadence**
   du nombre de fenêtres obtenues (`rate = nWindows / duration`) au lieu de la supposer.
   Détection : recouper une fenêtre annoncée « 0 % de voix » avec `volumedetect` — si elle sort
   à `mean -41 dB / max -20 dB`, ce n'est pas du silence, l'indexation ment.

2. **`grep -o '=-\?[0-9.]*$'` ne matche pas `-inf` → les fenêtres de silence sont SUPPRIMÉES**,
   pas mises à zéro. Tous les index suivants se décalent. Sur un montage de 56 s, 355 fenêtres à
   `-inf` = jusqu'à **11,8 s de dérive** entre le temps réel et le temps mesuré.
   **Parade** : `grep -oE '=(-?inf|-?[0-9.]+)$'` puis mapper `-inf` → `-99` côté JS.

3. **`silencedetect` sans `-map 0:a` renvoie 0 plage** : sans le map il analyse le flux vidéo et ne
   dit rien, ce qui se lit à tort comme « aucun silence dans ce fichier ». Avec `-map 0:a` sur la même
   source : **58 plages** sous −45 dB. Mettre `-map 0:a` sur **toute** analyse audio.

4. **Le garde-fou lèvres doit lire une piste VOIX SEULE**, jamais `final_audio.wav`. Sur le mix complet,
   le lit d'ambiance, la musique et l'audio d'origine des extraits franchissent le seuil −34 dBFS et
   comptent comme « voix active » : le contrôleur crie alors sur des plans de coupe légitimes.
   `build_audio_caps.mjs` écrit `voice_only.wav` (mêmes gains, mêmes placements, ni lit ni extraits)
   exprès pour ça.

### 🎙️ Il Y A un STT ici — Whisper via WaveSpeed

Ne conclus plus « pas de STT disponible » (les `.pt` de `~/.cache/whisper` sont inutilisables faute
de Python, mais ce n'est pas la seule voie). Endpoint
`https://api.wavespeed.ai/api/v3/wavespeed-ai/openai-whisper`, body
`{audio, language:'fr', enable_timestamps:true}` → renvoie `srt`, `text` et `text_details`
(segments `{start,end,text}`). Modèle de référence :
`/work/.claude/skills/foodboost-vitrine-video/scripts/whisper.mjs` (clé en dur dedans, à lire depuis
ce fichier). Il attend une **URL** : pour du local, uploader d'abord en multipart sur
`https://api.wavespeed.ai/api/v3/media/upload/binary` (champ `file`), qui rend un `download_url`
directement consommable. Une passe sur le fichier entier coûte quelques centimes et remplace des
heures de repérage à l'aveugle — et surtout elle sert de **seconde source indépendante** pour
savoir qui parle : si Whisper place du texte là où la bouche est fermée, c'est une voix **hors champ**.

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
- 9:16 `1080×1920`, matte black + néon jaune `#eab308` / violet `#8b5cf6` / orange `#8b5cf6`, police Inter 700.  ← valeurs fixées dans `_shared/CHARTE.md`, ne pas les redéfinir ici
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

## 🔒 BARRE DE QUALITÉ VERROUILLÉE (Tony, 2026-08-29) — « ne produire QUE cette qualité »

Référence désignée par Tony : la vidéo **hook stacking** du 18/08
(`hook-puissant/public/video.mp4`, https://www.tiktok.com/@automationboost7/video/7675417737430240514).
Toute nouvelle vidéo Autoboost reproduit CETTE structure — le gabarit codé est
`/work/secteurs-workflows/v2/template.mjs` (+ `monter2.mjs`) :

1. **Hook plein cadre** : l'avatar occupe TOUT l'écran sur le hook (pas de fenêtre),
   titre en bas. Jamais d'ouverture sur un b-roll abstrait seul.
2. **Ensuite cadre travaillé** : header AUTOBOOST + kicker pilule, fenêtre néon
   648×1152 à (216,150), **captions SOUS la fenêtre** (top:1392), jamais dessus.
3. **Toute démonstration de workflow = CANVAS n8n animé** : fond grille pointée,
   nœuds réels du workflow (icône + nom + type + puce d'explication) qui apparaissent
   **quand la voix les nomme**, fils jaune→violet qui se tirent entre eux.
   Les b-rolls abstraits ne suffisent plus pour une démo — exigence explicite de Tony
   (« il me fallait vraiment une démonstration du workflow avec les nœuds n8n qui expliquent »).
4. **Carton transformation** avant→après (« RÉSERVATION PERDUE ▼ 4 nœuds ») façon
   « DES HEURES → 3 SECONDES » de la référence.
5. **CTA** : pilule jaune COMMENTE <MOT> sous la fenêtre, avatar en fenêtre.
6. **Musique : douce, orchestrale** — `/work/chansons-3/autoboost-aventure.mp3`
   (générée voix-clonée sunoapi, style « Jurassic Park » demandé par Tony), fade-in 1,2 s,
   volume 0.30 ducké en sidechain sous la voix. **Plus de BGM agressive ni de ligne
   néon beat-sync dure** sur ce format : une lueur lente remplace la ligne.
7. Les règles lèvres/plans/gel du silence de ce skill s'appliquent inchangées
   (plans depuis plan.json, bouche gelée pendant les silences).

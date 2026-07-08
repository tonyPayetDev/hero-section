---
name: veille-to-video
description: Autoboost Neon Video — transforme un script/brief texte en vidéo promo sociale 9:16 (matte black + accents néon jaune/violet/orange), avec avatar/setup, voix clonée WaveSpeed, captions TikTok mot-à-mot, et publie sur Blotato. Source des vidéos à produire = Google Sheet de suivi.
---

# veille-to-video — Autoboost Neon Video

**Input :** script/brief texte (ou une ligne du Google Sheet de suivi) + voix + avatar
**Output :** projet HyperFrames (`public/index.html`) + MP4 rendu 1080x1920 + post publié sur Blotato

**Sheet source des vidéos à faire :**
`https://docs.google.com/spreadsheets/d/10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags/edit`
Colonnes : `# | Workflow | Lien n8n | Script Voix Off (20s) | Texte TikTok + Hashtags | Mot-clé CTA | Lien Screen Record | Statut Tournage | Vidéo Finale | Date Publication`
Toujours relire cette feuille en premier pour choisir la prochaine vidéo `⬜ À faire` et récupérer son script, ses hashtags et son mot-clé CTA — ne pas régénérer un brief à la main si la feuille en a déjà un.

---

## Goal

Créer une vidéo promo sociale française au format 9:16 à partir d'un script ou d'un brief. Sortie : un projet HyperFrames + un MP4 rendu.

## Style obligatoire

- **Format** : 1080x1920 vertical, 30 fps sauf indication contraire du projet.
- **Palette** : fond noir mat, accent global jaune `#FFE600`, plus violet `#A855F7` et orange `#FF8A3D` en highlights. Ne jamais revenir au bleu comme accent dominant.
- **Voix** : utiliser la voix clonée de l'utilisateur uniquement après accord explicite pour cette vidéo précise. Préférer `C:\Users\User\Work\Video IA AUTOBOOST\audio\voice-reference-clean.wav` avec WaveSpeed `wavespeed-ai/qwen3-tts/voice-clone`.
- **Captions** : style TikTok, centrées autour de la bande de sécurité médiane quand le bas contient l'avatar/setup, une seule ligne, trois mots maximum si possible. Surligner exactement un mot actif/puissant par caption en néon jaune/violet/orange. Ne pas mettre de boîte/fond visible derrière chaque mot ; texte blanc avec contour/ombre noire, et glow néon coloré pour le mot actif.
- **Avatar/setup** : quand on utilise le fond setup réaliste, retirer les filtres vert/noir et le flou latéral. L'avatar ne doit jamais cligner des yeux au début et ne doit jamais chevaucher les captions ou le texte qui slide.
- **Visuels** : utiliser de vrais schémas, icônes, dashboards, graphes, flèches de flux, panneaux UI. Éviter les slides façon PowerPoint/cartes seules, les filtres noirs sur le texte, la double exposition et les écrans statiques.
- **CTA** : pour les modèles/templates gratuits, dire que le modèle est gratuit et demander de commenter le mot-clé (colonne `Mot-clé CTA` du Sheet — RESTO, FREELANCE, LEADS, AGENT, VIDEO, PROSPECTION, NOTION, PINTEREST, IDEAS, LIVRE, SITE, AVATAR, WHATSAPP, REPURPOSE, BLOG, VEILLE, CREATEUR, PAGE, DEVIS, SEO, SEEDANCE...) plutôt que de donner l'URL du site directement.

---

## Workflow

### Étape 0 — Choisir la vidéo dans le Sheet

1. Lire le Google Sheet (export CSV : `.../export?format=csv`, suivre la redirection `googleusercontent.com` si besoin).
2. Filtrer les lignes `Statut Tournage = ⬜ À faire`, proposer la prochaine à l'utilisateur (ex. actuellement lignes #3–20 : Freelance Auto-Bidding, Lead Generation, AI Telegram Agent, Video Creation, Pinterest Automation, Children's Book Generator, Website Updates, Viral Reel Cloning, Blog Article Generation, SEO Analysis...).
3. Récupérer : `Script Voix Off (20s)`, `Texte TikTok + Hashtags`, `Mot-clé CTA`, `Lien Screen Record` (capture du workflow n8n si dispo), `Lien n8n`.
4. Si l'utilisateur donne un brief/script en direct au lieu d'une ligne du Sheet, l'utiliser à la place — mais toujours proposer d'écrire le résultat dans la colonne `Vidéo Finale` / `Statut Tournage` du Sheet une fois terminé (mise à jour manuelle, ce skill ne modifie pas le Sheet automatiquement).

### Étape 1 — Parser le script

Découper en hook / corps / CTA / durée cible. Supprimer les blocs de script collés en double.

### Étape 2 — Réécrire la narration si besoin

Réécrire uniquement pour le timing/la prononciation TTS. Garder le sens de l'utilisateur, texte de slide en français.

### Étape 3 — Consentement voix clonée

**Avant tout envoi de l'échantillon de voix à WaveSpeed**, exiger un texte explicite de l'utilisateur du type :
`J'autorise l'envoi de mon échantillon de voix à WaveSpeed pour générer l'audio de cette vidéo ...`
Sans ce texte, ne pas appeler l'API voice-clone. Ne jamais lire ni afficher les clés API.

### Étape 4 — Générer l'audio

WaveSpeed Qwen3 TTS voice-clone : `/api/v3/wavespeed-ai/qwen3-tts/voice-clone` avec `audio` (référence locale ci-dessus), `text`, `language: "French"`. Narration énergique et concise, proche du découpage des captions.

Sauvegarder le MP3 sous `C:\Users\User\Work\Video IA AUTOBOOST\audio\` et copier vers `public/assets/voice.mp3`.

**Depuis ce sandbox (pas d'accès direct à l'API WaveSpeed) : deux webhooks n8n actifs font le travail.**
Testés et fonctionnels le 2026-07-08 :
- `POST https://n7n.automatisationboost.com/webhook/tts-gen` — body `{voixUrl, text}` (voix de
  marque : `https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3`). Attend un délai
  fixe (~40s) puis fait un seul poll WaveSpeed — répond en fixant `Content-Type: audio/mpeg` même
  si le poll échoue, donc **une réponse HTTP 200 ne garantit pas un vrai MP3** : vérifier la taille
  du fichier téléchargé (`ls -la`/`ffprobe`) avant de continuer. En cas de corps vide malgré un
  `status: success` sur l'exécution n8n (`search_executions` + `get_execution includeData:true`),
  l'audio réel est quand même généré côté WaveSpeed/CloudFront — regarder le node `Poll WaveSpeed
  Result`/`Extract Audio URL` dans les données d'exécution pour récupérer l'URL CloudFront directe
  et la télécharger toi-même.
- `POST https://n7n.automatisationboost.com/webhook/avatar-webhook-v2` — body `{voixUrl, avatarUrl,
  description}` (`description` = le script). Fait le même voice-clone WaveSpeed **et** une vraie
  transcription Whisper mot-à-mot (OpenAI `whisper-1`, `timestamp_granularities: word`), renvoie
  `{voiceUrl, transcripts}` (transcripts groupés par paquets de 3 mots avec `start`/`end`). C'est la
  méthode à préférer pour avoir de vrais timestamps de captions (voir Étape 5). Boucle en interne
  sur des attentes de 20s tant que WaveSpeed n'a pas fini — peut dépasser une minute, **le timeout
  client curl n'annule pas l'exécution côté n8n** : si le call time out, chercher l'exécution la
  plus récente avec `search_executions({workflowId})` puis `get_execution({includeData:true})` une
  fois qu'elle passe à `status:"success"` pour récupérer `voiceUrl`/`transcripts` a posteriori.

### Étape 5 — Construire `public/index.html` (HyperFrames)

- Racine explicite `width:1080px; height:1920px;` et `data-duration` correspondant au plan final vidéo/audio.
- `<audio id="voice" src="assets/voice.mp3" data-start="0" data-duration="...">` en enfant direct de la racine si audio utilisé.
- Une seule timeline GSAP en pause, enregistrée dans `window.__timelines[compositionId]`.

**Captions** — spans TikTok mot-à-mot : mots neutres en texte plein sans rectangle/fond visible ; un seul mot actif `.hot`, `.violet` ou `.orange` en texte coloré/glow, jamais en pastille dure sauf demande explicite. Garder les captions loin des lignes de séparation et de la zone avatar/setup. Si `inspect` signale un dépassement, réduire la taille de police avant de faire du wrap. Synchroniser manuellement sur la narration si pas de timestamps mot-à-mot.

**Transcription mot-à-mot** : `npx hyperframes transcribe <audio> --language fr --json` échoue
proprement (`{"ok":false,"skipped":true,"reason":"whisper_unavailable"}`) dans ce sandbox — ni
`whisper-cpp` ni `parakeet-mlx` ne sont installés. Utiliser le webhook `avatar-webhook-v2`
ci-dessus (Étape 4) pour obtenir de vrais timestamps Whisper au lieu d'estimer manuellement.

**Slides SaaS/automatisation premium** — zone d'explication en haut + avatar/setup en bas si demandé. Texte court, en français. Pour le slide du flow d'automatisation, préférer un schéma horizontal stable : `Gmail -> Agent IA -> n8n -> Base -> Dashboard`, avec cartes icônes, flèches, point pulsé animé, petit panneau data/schéma. Éviter les layouts diagonaux qui se chevauchent.

Quand la demande est "premium SaaS", style Apple/Linear/Arc/Vercel/Raycast, explainer automatisation, vrais schémas/icônes/dashboards/graphes, ou explainer produit haut de gamme → lire `references/premium-saas-launch.md`. Override local : le jaune remplace le bleu comme accent global.

### Étape 6 — Valider avant rendu

Dans ce sandbox, `node`/`ffmpeg`/Chrome existent mais ne sont pas dans le `$PATH`, et **surtout
`FONTCONFIG_PATH` n'est pas configuré** — sans ça, Chrome headless ne rasterise **aucun texte**
(même les polices embarquées en base64), alors que les formes/boîtes s'affichent normalement. Ce
bug est silencieux : `validate`/`inspect` passent `ok:true` quand même, il faut vérifier
visuellement le rendu (frames `ffmpeg` + `Read`) pour l'attraper. Toujours exporter ces variables
avant toute commande `hyperframes` ici :

```bash
export PATH="/home/claude/tools/node/bin:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/chromelibs/usr/bin:$PATH"
export LD_LIBRARY_PATH="/home/claude/tools/chromelibs/lib/x86_64-linux-gnu:/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export FONTCONFIG_PATH="/home/claude/tools/chromelibs/etc/fonts"

npx -p node@22 -p hyperframes hyperframes validate public --json
npx -p node@22 -p hyperframes hyperframes inspect public
```

Confirmer 0 problème de layout, en particulier captions vs ligne de séparation/avatar/texte.

**Emoji = à éviter.** Ce sandbox n'a aucune police emoji couleur installée (seulement DejaVu) —
tout emoji (📲🤖🗂️🌐✔) utilisé comme icône s'affiche en tofu `NO GLYPH` dans le rendu final, même
si `validate`/`inspect` ne le détectent pas. Utiliser de vraies icônes SVG inline
(`viewBox="0 0 24 24" fill="none" stroke="currentColor"`) à la place — plus fiable de toute façon,
ne dépend d'aucune police, rendu identique partout. Les flèches/symboles Unicode simples
(`→`, `✓` basique) passent en général bien avec DejaVu, mais en cas de doute préférer aussi un SVG.

### Étape 7 — Rendre et vérifier

Rendre avec HyperFrames (avec les mêmes variables d'environnement qu'à l'étape 6 — le rendu final
échoue silencieusement au niveau du texte sans elles, pas au niveau du process). Le rendu d'une
comp de ~17s prend ~3-4min sur cette machine : lancer en arrière-plan (`nohup ... &`, `disown`) et
surveiller le log plutôt que d'attendre en bloquant.

Toujours **vérifier visuellement** après rendu, pas seulement `ffprobe` : extraire quelques frames
à des timestamps clés avec `ffmpeg -ss <t> -frames:v 1` puis les regarder (`Read`). `ffprobe`
confirme la durée/résolution/codecs mais ne dit rien sur le texte/les captions/les icônes qui
peuvent être invisibles à cause du bug fontconfig ci-dessus.

Vérifier avec `ffprobe` (durée, résolution, streams, taille plausible).

Si l'espace disque bloque le rendu, ne nettoyer QUE : cache Chrome Puppeteer/HyperFrames, anciens MP4 générés par ce même projet, anciens dossiers frames/checks. Ne jamais supprimer les échantillons de voix source, les uploads utilisateur, ou les assets de référence.

### Étape 8 — Publier sur Blotato

1. `blotato_list_accounts` pour retrouver le bon compte (ex. `automatisationboost` sur Instagram, comptes TikTok existants) — **toujours confirmer avec l'utilisateur quel compte/plateforme cibler** avant de publier, la publication est visible publiquement et irréversible.
2. Uploader le MP4 rendu (`blotato_create_presigned_upload_url` + upload, ou `blotato_create_visual` selon le cas) pour obtenir une URL média Blotato.
3. `blotato_create_post` avec la légende = `Texte TikTok + Hashtags` de la ligne du Sheet, en respectant les champs requis par plateforme (ex. TikTok : `privacyLevel`, `disabledComments`, etc. — voir `requiredFields` renvoyés par `blotato_list_accounts`).
4. Rapporter l'URL/ID du post à l'utilisateur.

### Étape 9 — Mettre à jour le Sheet (Statut/Vidéo Finale/Date)

Ce skill n'a pas d'outil d'écriture Google Sheets directe — mais un vrai workflow n8n existe déjà
pour ce pipeline complet : **"🎬 Script Sheet → Vidéo Avatar → Validation → Réseaux"**
(id `WFqUJ2g2btf976cd`, onglet Sheet `30 Vidéos` gid `1576933581`). Il utilise un pipeline
`/avatar-reel` (SSH) différent de celui-ci, et ses 3 nœuds de publication sont désactivés par
défaut — ne pas le lancer tel quel en pensant publier automatiquement.

Pour juste écrire dans le Sheet (sans repasser par tout ce pipeline), créer un petit workflow
n8n ponctuel via `create_workflow_from_code` (SDK) : `Manual Trigger` → un node
`n8n-nodes-base.googleSheets` (`operation: "update"`, `documentId` = l'ID du Sheet, `sheetName`
en mode `list` avec le gid, `columns.mappingMode: "defineBelow"`, `columns.matchingColumns:
["row_number"]`, `columns.value` avec `row_number` = le numéro de ligne physique réel (1 = header,
2 = première ligne de données), plus `Statut Tournage`/`Vidéo Finale`/`Date Publication`).
Réutiliser la credential Google Sheets déjà connectée (`list_credentials({type:
"googleSheets"})` → id credential), puis `execute_workflow({workflowId, executionMode:
"manual"})` pour l'exécuter une fois. Vérifier ensuite en relisant le CSV export du Sheet
(`.../export?format=csv&gid=<gid>`) que les bonnes colonnes ont changé.

---

## Règles Captions

- Maximum trois mots par phrase de caption si possible.
- Un seul mot actif surligné par phrase.
- Jaune néon pour les mots de force/valeur, violet pour transformation/IA, orange pour actions/CTA.
- Doit rester lisible sur mobile et passer `hyperframes inspect` avec 0 dépassement/occlusion de texte.
- Style renforcé validé (à proposer par défaut sauf préférence contraire) : `text-transform: uppercase`,
  `font-weight: 700` (poids max disponible avec Inter 400/700 embarqué). Positionner la bande de captions
  plus haut que le centre bas de l'écran (ex. `top: ~960px` sur une comp 1080×1920) plutôt que juste
  au-dessus de l'avatar — plus lisible, mieux séparé visuellement du cadre avatar. Toujours revalider
  `inspect` après un changement de taille/position (l'uppercase + police plus grosse peut faire déborder
  les captions les plus longues).
- **Ne JAMAIS combiner `-webkit-text-stroke` avec un contour en `text-shadow` sur le même texte.**
  Repéré (2026-07-08) sur autoboost-04 : les deux techniques de contour superposées produisent un
  effet de "double contour"/lettres dédoublées visible à l'œil sur le rendu final, sous le rasterizer
  logiciel Chrome headless (SwiftShader) utilisé pour le rendu dans ce sandbox — invisible en
  inspectant juste le CSS/le DOM, seulement visible en vérifiant des frames réelles du MP4 rendu.
  Utiliser **une seule** des deux méthodes pour le contour des captions : soit `-webkit-text-stroke`
  seul, soit un `text-shadow` 8 directions (`-Npx -Npx`, `Npx -Npx`, `-Npx Npx`, `Npx Npx`, `-Npx 0`,
  `Npx 0`, `0 -Npx`, `0 Npx`, tous `0 #000`) + une ombre douce pour la profondeur — le `text-shadow`
  seul suffit largement et rend proprement en headless.

## Sound design (BGM + SFX)

- **Ne jamais synthétiser le sound design par défaut (ffmpeg sinusoïdes/bruit filtré)** si une
  vraie source libre de droits est accessible — un pad/whoosh/chime synthétisé "fait maison" est
  perceptiblement moins bon qu'une vraie piste, même courte. Ne l'utiliser qu'en dernier recours
  documenté (aucune source dispo) et le remplacer dès qu'une devient disponible.
- **Epidemic Sound MCP** (`mcp__epidemic-sound__*`, si configuré dans `.claude/settings.json`) :
  `SearchRecordings`/`SearchSoundEffects` fonctionnent pour explorer le catalogue, mais
  `DownloadRecording`/`DownloadSoundEffect` peuvent renvoyer `FORBIDDEN` — recherche et
  téléchargement sont deux permissions séparées côté API, indépendantes du fait que le serveur MCP
  soit bien chargé. Vérifier qu'un téléchargement réussit réellement avant de t'appuyer dessus, et
  ne jamais utiliser les `lqmp3Url` de preview renvoyés par la recherche comme substitut dans une
  vidéo publiée (previews non licenciées pour du contenu final).
- **HeyGen** (skill `media-use`, `resolve.mjs --type bgm/sfx`) : nécessite le CLI `heygen` installé
  (`curl -fsSL https://static.heygen.ai/cli/install.sh | bash`) + `HEYGEN_API_KEY` en env — ni l'un
  ni l'autre n'est présent par défaut dans ce sandbox. Si absent, `resolve.mjs` échoue proprement
  ("no provider could resolve"), ne pas essayer de contourner.
- **Mixkit.co — méthode vérifiée et fonctionnelle, sans clé API, recherche + téléchargement OK**
  (musique, SFX, et vidéo stock — voir section broll plus bas). Licence "Mixkit Free" : usage
  commercial libre, sans attribution requise. Méthode (testée 2026-07-08) :
  1. `curl -s -A "Mozilla/5.0" "https://mixkit.co/free-stock-music/<tag>/"` (ou `free-sound-effects/<tag>/`)
     → parser le JSON-LD `<script type="application/ld+json">` embarqué dans le HTML pour les
     morceaux de musique : chaque entrée `MusicRecording` a un champ `"url"` = lien mp3 direct
     (`https://assets.mixkit.co/music/<id>/<id>.mp3`), déjà téléchargeable tel quel.
  2. Pour un SFX, la page catégorie n'expose que l'URL de preview (`.../active_storage/sfx/<id>/<id>-preview.mp3`,
     souvent suffisante) ; pour le fichier "download" officiel (souvent `.wav`), appeler
     `curl "https://mixkit.co/free-sound-effects/download/<id>/?context=item+grid"` et lire
     `data-download--modal-url-value="https://assets.mixkit.co/active_storage/sfx/<id>/<id>.wav"`
     dans la réponse — c'est le vrai fichier, pas une preview.
  3. Retirer toute pochette/cover art embarquée avec `ffmpeg -vn` avant d'utiliser le fichier comme
     `<audio>` (une pochette mjpeg attachée peut ajouter un flux vidéo parasite au fichier).
  - **Pexels bloque ce type de scraping direct** (testé : `curl` sur une page de recherche vidéo
    renvoie `403`, protection anti-bot) — ne pas perdre de temps à réessayer sans clé API officielle
    (`api.pexels.com`, inscription gratuite requise, pas configurée dans ce sandbox). Mixkit est la
    source par défaut tant que Pexels n'a pas de clé.
- **Piste de marque fournie par l'utilisateur** (ex. `assets.automatisationboost.com/music/...`) :
  toujours prioritaire sur une source tierce si l'utilisateur en donne une — télécharger, retirer
  la cover art (`-vn`), trim/fade sur la durée de la vidéo.

## Règles Avatar

- Avatar keyé propre ou composite setup sans filtres latéraux vert/noir.
- Toujours sous la bande de sécurité des captions pour les vidéos split verticales.
- **Cadre circulaire + anneau néon permanent (pattern recommandé)** : si la vidéo source de
  l'avatar a un fond quasi-noir mais pas identique au `--bg` de la comp (rectangle visible en
  différence de nuance), ne pas chercher à re-keyer — plus simple et robuste de masquer l'avatar
  dans un cercle (`border-radius:50%; overflow:hidden` sur un conteneur, vidéo en `object-fit:cover`
  dedans avec `data-layout-allow-overflow="true"`) avec une bordure + `box-shadow` néon jaune en
  dur sur ce conteneur. Le crop circulaire élimine le rectangle sans dépendre de la qualité du
  fond source. Ajouter un anneau externe séparé qui pulse en continu (`opacity`/`scale`, GSAP
  `yoyo:true` avec un `repeat` **fini** dimensionné pour tenir dans la comp — jamais `repeat:-1`
  dans une timeline seek-based/déterministe) pour un effet "néon vivant", avec un beat plus fort
  (rotation 360°, scale plus grand) réservé au moment CTA.
- **Broll plein écran sans avatar (pattern optionnel)** : pour varier, masquer l'avatar (fade
  opacity du conteneur circulaire, pas de `display:none`) pendant une scène choisie et étendre
  cette scène à la hauteur totale (1920px au lieu de 1120px) pour qu'elle remplisse tout le cadre
  — bon candidat : le schéma d'automatisation ou tout visuel dense qui bénéficie de plus d'espace.
  Refaire apparaître l'avatar en fondu au début de la scène suivante.
  - **Si un vrai clip vidéo (pas juste un schéma motion-design) est nécessaire pour ce broll** :
    Mixkit a aussi une section vidéo stock (`https://mixkit.co/free-stock-video/<tag>/`), scrapable
    avec la même méthode que la musique/SFX (voir section "Sound design" plus haut) — le JSON-LD de
    la page contient un champ `"contentUrl"` par clip avec un lien mp4 direct
    (`https://assets.mixkit.co/videos/<id>/<id>-1080.mp4` ou `-720`), licence Mixkit Free (usage
    commercial libre, sans attribution). Pexels a un catalogue plus large mais bloque le scraping
    direct (`403` testé) — n'y recourir que via leur clé API officielle si l'utilisateur en fournit
    une ; sinon Mixkit reste la source par défaut. Poser le clip en `<video>` plein cadre
    (`object-fit:cover`, `muted`, `data-start`/`data-duration` sur la fenêtre de la scène), loopé
    avec `-stream_loop -1 -t <durée>` côté ffmpeg si le clip source est plus court que la scène
    (jamais via `trim` dans le filter graph, voir CLAUDE.md racine).
- Valider que l'avatar ne recouvre jamais les captions ni le texte important de la scène.

---

## Checklist finale

- [ ] Ligne du Sheet identifiée et infos récupérées (script, hashtags, mot-clé CTA)
- [ ] Consentement voix clonée obtenu explicitement avant tout appel WaveSpeed
- [ ] Palette noir mat + jaune/violet/orange respectée, pas de bleu dominant
- [ ] Captions TikTok mot-à-mot validées (0 dépassement `inspect`)
- [ ] Avatar sans filtre vert/noir, ne recouvre jamais captions/texte
- [ ] `validate` + `inspect` = 0 problème avant rendu
- [ ] Rendu vérifié via `ffprobe` (durée, résolution, taille)
- [ ] Compte Blotato confirmé avec l'utilisateur avant publication
- [ ] Post publié sur Blotato, URL/ID rapporté à l'utilisateur
- [ ] Sheet à mettre à jour manuellement (statut, vidéo finale, date de publication)

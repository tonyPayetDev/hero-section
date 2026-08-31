---
name: foodboost-vitrine-video
description: FoodBoost — génère une vidéo vitrine sociale 9:16 pour restaurateurs où TOUT est créé par IA à moindre coût (WaveSpeed). N'importe quels plats (créole, burger, sandwich, pizza, sushi, pâtisserie...) : images seedream-v4 → cinemagraphs vidu start-end (boucle 8s) → voix clonée qwen3-tts → titres + captions animés HyperFrames → MP4 1080x1920. Puis prévisualisation + planif Blotato @foodboost. À utiliser dès qu'on demande une vidéo FoodBoost / vitrine food IA / "menu du jour" animé.
---

# foodboost-vitrine-video

**Input :** une liste de plats (n'importe quelle cuisine) + un angle. **Output :** projet HyperFrames (`public/index.html`) + MP4 rendu 1080x1920 avec voix + captions, prévisualisé et prêt à planifier sur `@foodboost`.

Distinct de `veille-to-video` (Autoboost néon, produit Tony) et de `foodboost-01-demo` (avatar+broll). Ici : **100% généré, food-porn, ~0,45 $/vidéo, aucun tournage.**

---

## Quand l'utiliser
Demande de vidéo pour **@foodboost** / vitrine restaurant / "menu du jour" animé / cinemagraph de plats. **Les plats sont libres** : ne PAS supposer du créole — burger, sandwich, pizza, sushi, pâtisserie, poké, tacos… selon la demande. Si l'utilisateur ne précise pas, demander la cuisine/les plats.

## Style FoodBoost (à conserver)
- **Format** 1080×1920, 30 fps. **Durée** ~18–22 s (calée sur la voix, jamais du remplissage).
- **Look food-porn** : fond sombre, bois/surface rustique, éclairage chaud rasant, vapeur, garniture fraîche, faible profondeur de champ. (C'est le `style` dans `config.json`.)
- **Palette UI** : `--mangue #FFB020` (accent principal), `--lagon #2EC4B6`, `--piment #FF3B30`, fond `#070503`, texte blanc.
- **Structure** : 1 scène plein-cadre par plat (badge n°, nom du plat, sous-titre) → 1 scène preuve+CTA (« généré automatiquement / chaque jour / sans photographe » → **Commente MENU**).
- **Captions** style TikTok, 2–4 mots, un mot surligné (`.hot`/`.lagon`/`.piment`), synchro voix.
- **CTA** : toujours « Commente le mot **MENU** » (mot-clé FoodBoost par défaut).

---

## Pipeline (tout via WaveSpeed — clé partagée en dur dans les scripts, override `WAVESPEED_KEY`)

Travailler dans un nouveau dossier projet `foodboost-videos/foodboost-NN-<slug>/`.

### 0. Config
Copier `templates/config.example.json` → `config.json` dans le projet et l'adapter (style + 3 plats + narration). Copier aussi `templates/composition.html` → `public/index.html`.

### 1. Images (seedream-v4, 9:16, ~0,01–0,03 $/img)
```
node scripts/gen-images.mjs      # lit config.json → assets/<id>.png + image-urls.json
```
**Toujours vérifier les images** (Read sur les .png) avant d'animer.

### 2. Cinemagraphs (vidu start-end, boucle 8s, ~0,08 $/clip)
```
node scripts/gen-videos.mjs      # lit config.json + image-urls.json → public/assets/<id>.mp4
```
Même image en `image` ET `last_image` = boucle parfaite. `bgm:false` obligatoire. Clips = **8,125 s** ⇒ ne jamais afficher un clip plus longtemps que ça dans la timeline (voir piège coverage).

### 3. Voix clonée (qwen3-tts, ~40 s–5 min)
```
echo "…narration…" > narration.txt   # ou copier config.narration
node scripts/tts.mjs                  # → public/assets/voice.mp3 + voice-url.txt
```
Consentement voix = **standing** (Tony l'a donné une fois pour toutes) — ne pas redemander à chaque vidéo. Le job peut être lent : poller jusqu'à ~7 min (le 1er job peut sembler bloqué ; en resoumettre un en parallèle si besoin).

### 4. (option) Transcription pour caler les captions
```
node scripts/whisper.mjs   # → whisper-res.json (timings)
```
`openai-whisper` renvoie souvent **un seul segment** pour <20 s → pas de mot-à-mot. Dans ce cas, **timer les captions à la main** par proportion de caractères sur la durée totale de la voix (méthode dans la note du template). `language` = code ISO (`fr`, pas "french").

### 5. Composition HyperFrames
Éditer `public/index.html` (copié du template) : remplacer noms de plats, sous-titres, `<img>/<video src>`, la narration des captions et leurs `data-start/data-end`, et les fenêtres de scène `S1..S4` dans le script GSAP. Contrat clé :
- racine `<div id="root" data-composition-id="<slug>" data-start="0" data-duration="<sec>" data-fps="30" data-width="1080" data-height="1920">`
- vidéos : `<video data-start data-duration muted playsinline>` — **data-duration ≤ 8.0** (longueur du clip)
- captions : `.caption data-start data-end`
- audio : `<audio data-start data-duration data-volume>` (voice 1.0, bgm 0.08)
- timeline GSAP `paused`, enregistrée sur `window.__timelines["<slug>"]`.

### 6. Snapshot AVANT rendu (obligatoire), puis rendu
Toujours snapshoter 3–4 frames texte-lourdes d'abord (le rendu complet fait plusieurs minutes) :
```
export PATH="/home/claude/tools/node/bin:$PATH:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static"
export LD_LIBRARY_PATH="/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu:/home/claude/tools/chromelibs/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export FONTCONFIG_PATH=/home/claude/tools/chromelibs/etc/fonts
export FONTCONFIG_FILE=/home/claude/tools/chromelibs/etc/fonts/fonts.conf
export PUPPETEER_EXECUTABLE_PATH=/home/claude/.cache/hyperframes/chrome/chrome-headless-shell/linux-131.0.6778.85/chrome-headless-shell-linux64/chrome-headless-shell

node_modules/.bin/hyperframes snapshot public --at 2.5,6,9,18 --no-end -o public/snapshots
# vérifier public/snapshots/contact-sheet.jpg (Read) : le TEXTE doit être visible
node_modules/.bin/hyperframes render public -q high -o "renders/foodboost-NN_$(date +%H-%M-%S).mp4"
```
(Installer d'abord hyperframes : `package.json` avec `"hyperframes": "^0.7.5"` puis `npm install` — node dans le PATH.)

### 7. Prévisualisation (donner un lien à Tony)
Repo `tonyPayetDev/previsualisation` (app Coolify `previsualisation`, uuid `in9lww2r6zmrxdgubz4w09iq`). PAT dans le remote git de `/work`. Ajouter un dossier `foodboost-NN/` (`index.html` carte + `video.mp4`), ajouter un `<li>` à la racine, commit/push, puis :
```
curl -s -X POST "http://158.220.127.234:8000/api/v1/deploy?uuid=in9lww2r6zmrxdgubz4w09iq&force=true" -H "Authorization: Bearer 32|EHh0msiQ6mFH6RdD3w7PRNMswA07HD3WXN7nZiW940ba2077"
```
Lien = `https://previsualisation.automatisationboost.com/foodboost-NN/` (la vidéo `no-cache` peut mettre ~1 min).

### 8. Planif Blotato (après validation de Tony)
Compte **Instagram @foodboost = accountId `55611`** (IG only, pas de TikTok FoodBoost). Reel, `shareToFeed:true`. **Limite Instagram = 5 hashtags max** (Blotato rejette au-delà). Héberger le média via l'URL de prévisualisation (publique). Heure = Réunion (UTC+4) ; vérifier `date -u` car « ce soir » peut déjà être passé.

---

## Pièges déjà payés (NE PAS refaire)
1. **Texte invisible au rendu** si FONTCONFIG mal réglé. Valeur EXACTE : `FONTCONFIG_PATH=/home/claude/tools/chromelibs/etc/fonts` + `FONTCONFIG_FILE=.../fonts.conf`. Sans ça, images/SVG/bordures s'affichent mais **tous les glyphes sont blancs** — un rendu "réussi" mais inutilisable. D'où le snapshot obligatoire.
2. **Chrome libs manquantes** (`libglib-2.0.so.0`) → `LD_LIBRARY_PATH=/home/claude/tools/chromelibs/...`. Épingler Chrome 131 via `PUPPETEER_EXECUTABLE_PATH` (le 152 par défaut marche aussi une fois `LD_LIBRARY_PATH` posé).
3. **Coverage gate** : le rendu ABORTE si une `<video>` est affichée plus longtemps que sa vraie durée (clip = 8,125 s). Pour un fond de scène long (>8 s), utiliser une **`<img>` statique** avec un léger zoom GSAP (identique à l'œil derrière un voile sombre), pas la vidéo.
4. `hyperframes validate` a tendance à hang sur cet env → utiliser `snapshot` (ou `check`).
5. Le CLI opère sur le **dossier composition** = `public` (contient `index.html`), pas sur le fichier html.
6. `enable_timestamps:true` requis pour Whisper, et `language:"fr"` (code ISO, pas "french").
7. Ne pas coder les plats en dur : tout passe par `config.json`.

## Coût type
3 images + 3 vidéos (~0,24 $) + voix + whisper ≈ **0,45 $/vidéo**. Solde WaveSpeed : `GET /api/v3/balance`.

## Assets du skill
- `scripts/gen-images.mjs` · `scripts/gen-videos.mjs` · `scripts/tts.mjs` · `scripts/whisper.mjs`
- `templates/config.example.json` (exemple burger/sandwich/frites) · `templates/composition.html` (compo 4 scènes prouvée)

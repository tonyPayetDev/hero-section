# Autoboost Neon Video — #4 Telegram Agent IA

## ✅ SOUND DESIGN v4 + FIX CAPTIONS (2026-07-08, suite 6)

Retours utilisateur sur le rendu v3 : SFX "moyens", musique de marque à utiliser à la place de
Mixkit, et captions "un peu bizarres".

- **BGM** : remplacé "Close Up" (Mixkit) par **"Ascension Protocol"** (piste de marque fournie
  par l'utilisateur : `assets.automatisationboost.com/music/Ascension%20Protocol.mp3`, générée
  via Suno). Trim 0–16.73s (intro la plus discrète, -18.8dB vs -13 à -16dB plus loin dans le
  morceau), `-vn` pour retirer la cover art mjpeg attachée (aurait ajouté un flux vidéo parasite
  au fichier audio), fade in 0.3s / fade out 0.6s → `assets/bgm-ascension.mp3`.
- **SFX** : remplacés par des picks plus premium sur Mixkit (mêmes méthode/licence que la suite
  précédente) : whoosh "Fast whoosh transition" → **"Cinematic whoosh fast transition"**
  (`sfx-whoosh-v2.mp3`, 1.38s) ; chime "Positive notification" (bell générique) →
  **"Sci-Fi confirmation"** (`sfx-chime-v2.mp3`, 1.07s), mieux thématisé pour une vidéo Agent IA.
- **Fix captions** : `.caption .line` combinait `-webkit-text-stroke: 3px #000` **et** un contour
  simulé en `text-shadow` 4 directions — les deux techniques superposées produisaient un effet de
  double-contour/lettres dédoublées sous le rasterizer logiciel Chrome headless (SwiftShader),
  confirmé visuellement via des captures Playwright du MP4 rendu (voir méthode ci-dessous) sur
  quasi toutes les captions ("TU PAIES CHATGPT", "CHERCHE SUR LE", "COMMENTE AGENT", etc.). Le bug
  était invisible à l'inspection du DOM/CSS ou à `hyperframes validate/inspect` (`ok:true` quand
  même) — seule une vérification visuelle de frames réelles l'a révélé. Fix : retrait du
  `-webkit-text-stroke`, contour porté intégralement par un `text-shadow` étendu à 8 directions
  (4 diagonales + 4 axes) au lieu de 4. Règle ajoutée au skill `veille-to-video` pour ne plus
  répéter cette combinaison.
- **Vérification visuelle** : capture d'écran du MP4 rendu via `playwright-skill` — méthode :
  ouvrir une page HTML locale (`file://`) avec un `<video>` pointant vers le MP4 (le player mp4
  refuse le chargement si la page est ouverte via `page.setContent()`/origine non-file:// —
  `MEDIA_ELEMENT_ERROR: Media load rejected by URL safety check` ; il faut naviguer vers un vrai
  fichier `.html` en `file://`), puis `video.currentTime = t` + attendre l'event `seeked` + screenshot
  de l'élément vidéo. Confirmé le bug sur le rendu v3, confirmé le fix sur le rendu v4. En bonus,
  a confirmé que le warning de contraste `hyperframes validate` sur `.free-pill` ("Modèle gratuit")
  était un faux positif (frame de transition mid-fade, pas un vrai problème visuel — le badge
  s'affiche bien avec son fond orange une fois stabilisé).

Revalidé (`ok:true`, seul warning préexistant sans lien : slot voix) et re-rendu. `ffprobe` :
H.264 1080×1920, AAC, 16.77s, 6.76MB. `volumedetect` : mean -26.2dB / max -5.9dB, cohérent avec
les passes précédentes.

**Uploadé sur Blotato (lien media only, PAS publié)** :
`https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/8e96c554-971f-4851-ba4c-a6ec66f4074d.mp4`

---

## ✅ SOUND DESIGN v3 — vraie musique/SFX libres de droits (2026-07-08, suite 5)

Suite au blocage Epidemic Sound (recherche OK mais `DownloadRecording`/`DownloadSoundEffect`
renvoient `FORBIDDEN` — voir section dédiée plus bas) et HeyGen (CLI absent du sandbox, `resolve.mjs`
du skill `media-use` échoue proprement en "no provider could resolve"), décision utilisateur :
contourner avec de la **vraie musique libre de droits (Mixkit, licence "Mixkit Free" — usage
commercial libre, sans attribution)** plutôt qu'utiliser les previews basse qualité Epidemic Sound
(refusé par principe, ce sont des previews non licenciées pour du contenu publié).

Scrapé `mixkit.co` en HTTP direct (`curl` + parsing du JSON-LD embarqué dans les pages catégorie,
et de l'endpoint `/free-sound-effects/download/<id>/` qui renvoie l'URL réelle `assets.mixkit.co/.../<id>.wav`
derrière le bouton "Download") :
- **BGM** : "Close Up" (Michael Ramir C., Corporate Music, mood positif/futuriste) —
  `assets/bgm-mixkit.mp3`, trim 0–16.73s + fade in 0.3s / fade out 0.6s, volume 0.12.
- **Whoosh transition** : "Fast whoosh transition" — `assets/sfx-whoosh-mixkit.mp3`, trim 0.8s +
  fade out, aux 3 mêmes repères (4.68s/10.32s/13.44s).
- **Chime CTA** : "Positive notification" — `assets/sfx-chime-mixkit.mp3`, trim 2.4s + fade out,
  à 13.72s (le CTA a assez de marge — 3s restantes — pour laisser sonner tout le chime).

Anciens fichiers synthétisés (`bgm-pad.mp3`, `sfx-whoosh.mp3`, `sfx-chime.mp3`) laissés sur disque
mais plus référencés par `public/index.html`.

Revalidé (`ok:true`, seul warning préexistant sans lien : slot voix 16.73s vs média 15.96s) et
re-rendu. Vérifié `ffprobe` (H.264 1080×1920, AAC, 16.77s, 6.83MB) et `volumedetect` sur le mix
complet : mean -26.7dB / max -6.5dB — quasi identique à la balance de la passe synthétisée
précédente (-26/-7.6dB), donc la vraie musique ne casse pas l'équilibre sous la voix.

**Uploadé sur Blotato (lien media only, PAS publié)** :
`https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/f6d60e14-4a26-4d97-9d5e-6f4b0cb49c2f.mp4`

---

## ✅ RETOUCHES SUPPLÉMENTAIRES (2026-07-08, suite 4) — anneau rapproché + comète néon + son v2

Retour utilisateur sur le rendu précédent : le sound design "pas ouf", l'anneau néon trop loin de
l'avatar, et vouloir un vrai effet "néon qui tourne en cercle".

**Découverte clé** : `#avatar-ring` avait déjà une `rotation: 360` sur le beat CTA depuis la
passe précédente, mais comme c'est un anneau de couleur unie (`border` plein), une rotation ne
produit **aucun changement visuel** — un cercle uniforme est identique à n'importe quel angle.
D'où l'impression que "l'effet neon ne tourne pas".

`public/index.html` :
- `#avatar-ring` rapproché : 680px → 644px (anneau presque collé au cadre avatar 620px).
- Nouvel élément `#avatar-orbit` (656px) : anneau fin en `conic-gradient` (transparent sur la
  majorité du tour, tête de comète jaune/blanche sur les derniers ~40°) découpé en anneau via
  `mask: radial-gradient(...)`. GSAP fait tourner cet élément en continu
  (`rotation: "+=360"`, `repeat:7`, sans yoyo) — **c'est ce dégradé directionnel qui rend la
  rotation visible**, contrairement à `#avatar-ring`. Inclus dans le fondu de la scène broll
  (masqué avec `#avatar-frame` pendant 6.46–10.32s).
- Sound design régénéré (toujours synthétisé ffmpeg, pas de vraie musique — voir plus bas) :
  nappe passée de 4 à 5 couches (ajout d'un scintillement aigu discret), `vibrato` léger +
  `volume` automatisé en expression (`0.5+0.14*sin(2*PI*t/7.5)`) pour un swell lent façon
  "epic", lowpass remonté 1600→2400Hz (moins étouffé), highpass 50Hz (nettoie le sub-bass).
  Whoosh reconstruit avec un vrai balayage de fréquence via `aevalsrc` (chirp descendant
  3200→400Hz sur 0.55s) au lieu d'un simple bruit filtré statique — beaucoup plus crédible
  comme "whoosh". Chime passé à 3 tons (880/1318/1760Hz) + echo pour une queue plus naturelle.

Revalidé (`ok:true`, 0 issue `inspect`), re-rendu, vérifié visuellement (comète confirmée en
mouvement entre deux frames à 0.5s et 1.5s) et à l'oreille (`volumedetect` : mean -26dB/max
-7.6dB, cohérent).

**Uploadé sur Blotato (lien media only, PAS publié)** :
`https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/f76d7328-9d44-4da7-8a38-9c5561e2b687.mp4`

### Epidemic Sound MCP — actif mais téléchargement refusé (2026-07-08, suite 5)

Nouvelle session : les outils MCP (`SearchRecordings`, `SearchSoundEffects`, `DownloadRecording`,
`DownloadSoundEffect`, etc.) sont bien chargés cette fois (confirmation qu'il fallait juste
redémarrer Claude Code, comme prévu). **Recherche fonctionnelle** : trouvé "Floating Point"
(Isaac Larson, id `5f127b1b-d694-3dc8-b122-96aa4e6c4eab`) — électro/ambient, mood "hopeful",
31.8s, sans voix — bon candidat pour remplacer le pad synthétisé "epic léger".

**Mais `DownloadRecording` et `DownloadSoundEffect` renvoient tous les deux `FORBIDDEN`**
("You don't have permission to download this asset"), testé sur 2 pistes musicales différentes
et 1 SFX. Recherche et téléchargement sont donc deux permissions distinctes côté API Epidemic
Sound — le token actuel permet de chercher le catalogue mais pas de récupérer les fichiers
(probablement un abonnement/plan qui n'inclut pas les droits de licence, ou une clé sans scope
download). Le token expire de toute façon ~07-08 août 2026 (30 jours depuis le 2026-07-08).

**Ne pas contourner** en utilisant les `lqmp3Url` de preview renvoyés par la recherche : ce sont
des previews basse qualité non licenciées pour usage commercial, pas des fichiers utilisables
dans une vidéo publiée.

**Sound design du render actuel inchangé** : toujours le pad synthétisé ffmpeg (`assets/bgm-pad.mp3`)
décrit dans la suite 4 ci-dessus — aucune vraie piste Epidemic Sound intégrée. À reprendre une
fois l'abonnement/droits de téléchargement confirmés côté compte Epidemic Sound de l'utilisateur.

**Fallback HeyGen tenté et bloqué aussi** : skill `media-use` (`resolve.mjs --type bgm`) échoue
proprement avec "no provider could resolve" — le CLI `heygen` n'est pas installé dans ce sandbox
et aucune `HEYGEN_API_KEY` n'est configurée (ni en env, ni documentée dans un CLAUDE.md du repo).
Pas de faux résultat/preview utilisé en substitut — refusé par principe (voir décision utilisateur
ci-dessous, pas de contournement avec un asset non licencié).

**Décision utilisateur (2026-07-08)** : Tony va vérifier/régler son abonnement Epidemic Sound
(droits de download, ou régénérer le token) plutôt que de fournir une clé HeyGen. **Prochaine
étape dès confirmation** : relancer `SearchRecordings`/`DownloadRecording` sur "Floating Point"
(id `5f127b1b-d694-3dc8-b122-96aa4e6c4eab`, électro/ambient/hopeful, 31.8s) ou équivalent,
remplacer `assets/bgm-pad.mp3`, re-render, re-vérifier (`ffprobe`/`volumedetect`), re-upload Blotato.

---

## ✅ RETOUCHES SUPPLÉMENTAIRES (2026-07-08, suite 3) — captions, anneau pulsé, sound design

Demandes utilisateur après la passe circulaire/broll :
1. Remonter les captions plus haut à l'écran, police plus forte, texte en majuscules.
2. L'anneau néon doit *pulser* (pas juste être statique/pulser seulement au CTA).
3. Ajouter du sound design + une musique de fond "epic léger".
4. Mettre à jour le skill `veille-to-video` avec les apprentissages de la session.
5. Publier les modifications sur git.

`public/index.html` :
- `.caption` remonté de `top:1130px` à `top:960px`. `.caption .line` : `font-size` 52→60px,
  `text-transform:uppercase`, `-webkit-text-stroke` 2px→3px (contour plus marqué).
- `#avatar-ring` : `data-start`/`data-duration` étendus de la fenêtre CTA-only (13.44–16.73) à
  toute la vidéo (0–16.73). Timeline GSAP : pulse continu (`opacity`/`scale`, `yoyo:true`) en deux
  segments bornés — 0→~6s (`repeat:11`) et 10.32→~13.3s (`repeat:5`) — choisis pour se terminer
  *avant* la fenêtre broll (6.46–10.32, avatar cité caché) et avant le beat CTA (13.44s), sans
  jamais utiliser `repeat:-1` (romprait le calcul de durée totale d'une timeline seek-based/
  déterministe). Le beat CTA (rotation 360° + scale) reste un `tl.to` distinct par-dessus.
- Sound design ajouté (tracks 11–13) : `assets/bgm-pad.mp3` (pad synthétisé ffmpeg, accord La
  mineur sur 4 sinusoïdes + lowpass + echo + fade in/out, volume 0.15 sous la voix),
  `assets/sfx-whoosh.mp3` (bruit blanc filtré passe-bande, joué à 3 transitions de scène : 4.68s,
  10.32s, 13.44s), `assets/sfx-chime.mp3` (deux sinusoïdes 880/1760Hz, au reveal du mot-clé CTA
  à 13.72s). **Pas de vraie musique "epic"** : aucun accès dispo dans ce sandbox (pas de clé
  HeyGen/Gemini fournie, pas d'abonnement Splice actif sur le compte). Voir section MCP
  Epidemic Sound plus bas.

Revalidé (`ok:true`, 0 issue `inspect`) et re-rendu, vérifié visuellement (frames + `volumedetect`
ffmpeg confirmant l'audio mixé, mean -27.9dB / max -11.1dB).

**Uploadé sur Blotato (lien media only, PAS publié)** :
`https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/e7d21ed7-77a5-48b0-bed9-7e13afa1c28d.mp4`

### MCP Epidemic Sound ajouté (pas encore actif dans cette session)

L'utilisateur a fourni la config MCP + un token Bearer JWT Epidemic Sound (collé en clair dans le
chat). Ajouté à `.claude/settings.json` → `mcpServers.epidemic-sound` (même convention que les
autres serveurs déjà présents dans ce fichier — `21st-dev-magic`, `wordpress` — qui stockent
aussi leurs clés en clair, donc cohérent avec l'existant). **Nécessite un redémarrage de Claude
Code pour devenir utilisable** (les nouveaux serveurs MCP dans settings.json ne se chargent pas
en cours de session). Une fois actif : régénérer `assets/bgm-pad.mp3` avec une vraie piste
Epidemic Sound à la place du pad synthétisé.

**Sécurité** : ce token a été collé en clair dans la conversation — recommandé à l'utilisateur de
le régénérer côté Epidemic Sound. Je ne l'ai pas réutilisé ailleurs que dans ce fichier.

### Sheet "avatar-reel" — lien toujours manquant

L'utilisateur a signalé que la vidéo devrait être trackée sur une sheet "avatar-reel" différente
de celle de veille-to-video (`10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags`) référencée en haut de
ce fichier et du skill. Aucun lien valide reçu jusqu'ici (le lien fourni était en fait une page
Epidemic Sound, sans rapport). **À redemander à l'utilisateur** avant de considérer la référence
Sheet de ce projet comme correcte.

---

## ✅ RETOUCHES VISUELLES (2026-07-08, suite 2) — avatar circulaire + broll plein écran

Demande utilisateur après visionnage du rendu précédent : fond noir "en carré" visible derrière
l'avatar, envie d'un anneau néon jaune autour de l'avatar, et un peu de broll plein écran sans
avatar par moments.

`public/index.html` modifié :
- **Avatar → cadre circulaire permanent** : `<video id="avatar">` déplacée dans un nouveau
  `#avatar-frame` (620px de diamètre, `border-radius:50%`, `overflow:hidden`, bordure jaune
  5px + triple `box-shadow` néon). Le crop circulaire rogne le rectangle de fond de la source
  `avatar-keyed.mp4` (fond quasi-noir mais pas identique au `--bg` de la comp — d'où le carré
  visible avant) ; plus robuste qu'un re-keying puisque ça ne dépend pas de la qualité du fond
  vidéo source. `data-layout-allow-overflow="true"` ajouté sur `#avatar` car la vidéo dépasse
  intentionnellement le cadre (780px de haut dans un cadre de 620px) pour remplir le cercle sans
  bande vide — confirmé attendu via `hyperframes inspect` (0 warning après l'attribut).
- **`#avatar-ring`** (l'ancien anneau CTA-only) gardé pour l'effet de pulse/rotation pendant la
  scène 5 (13.44–16.73s), redimensionné à 680px pour se superposer proprement autour du nouveau
  cadre 620px — donne un double anneau au moment CTA.
- **Scène 3 (schéma d'automatisation Telegram→Agent IA→Notion→Web) devient un broll plein écran** :
  `#scene-3 { height: 1920px }` (au lieu de 1120px comme les autres scènes) + `#avatar-frame`
  passé à `opacity:0` via GSAP au `data-start` de la scène 3 (6.46s) et remis à `opacity:1` à la
  fin (10.32s, début scène 4). Le flow diagram + panel occupent alors tout le cadre vertical,
  sans l'avatar, avant qu'il ne revienne en fondu pour scène 4 (badges souveraineté).

Revalidé (`validate` ok:true, `inspect` 0 issue) et re-rendu. Vérifié visuellement (frames extraites
à plusieurs timestamps, y compris les transitions 6.3–6.6s et 9.6–10.5s) : cercle propre sans
rectangle de fond visible, anneau néon permanent, disparition/réapparition fluide de l'avatar
autour de la scène 3, double anneau pulsé au CTA. `ffprobe` : H.264 1080×1920, AAC, 16.77s, ~5.4MB.

**Uploadé sur Blotato (lien media only, PAS publié)** :
`https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/41e87d8a-e807-47c1-90a3-3990c5138aa5.mp4`

---

## ✅ CORRECTIF RENDU (2026-07-08, suite) — texte/captions/icônes invisibles → corrigé

Le rendu "FINAL" listé ci-dessous (envoyé sur Blotato le 2026-07-08 après-midi) avait un bug
critique invisible à l'inspection du code : **tout le texte du rendu vidéo était vide** (titres,
bulles de chat, les 18 captions TikTok, labels des icônes) — seules les formes (pastilles,
cartes, anneau CTA) s'affichaient. Diagnostiqué en extrayant des frames du MP4 avec `ffprobe`/`ffmpeg`.

**Cause racine (environnement, pas le composition HTML) :** ce sandbox n'a ni `/etc/fonts` ni
`FONTCONFIG_PATH` configuré, et `/home/claude/tools/fonts` (référencé par le fontconfig local
`/home/claude/tools/chromelibs/etc/fonts/local.conf`) est vide. Sans fontconfig fonctionnel,
Chrome headless (`headless-shell` avec SwiftShader logiciel) ne rasterise **aucun texte**, même
les polices `@font-face` embarquées en base64 dans le HTML — un fontconfig cassé désactive tout
le moteur de police, pas seulement les polices système.

**Fix** : passer `FONTCONFIG_PATH=/home/claude/tools/chromelibs/etc/fonts` (qui référence
`chromelibs/usr/share/fonts/truetype/dejavu`, déjà présent sur la machine) à `hyperframes
validate|inspect|render`. Nécessaire à chaque commande hyperframes dans ce sandbox, pas
seulement pour ce projet — à retenir pour tous les futurs rendus ici.

**Bug secondaire trouvé pendant la vérification** : les emoji (📲🤖🗂️🌐✔) utilisés comme icônes
dans `public/index.html` s'affichaient en tofu "NO GLYPH" (DejaVu n'a pas de glyphes emoji couleur,
et aucune police emoji n'est installée dans ce sandbox). Remplacés par des icônes SVG inline
(trait jaune néon `var(--yellow)`, `stroke="currentColor"`) : avion en papier (Telegram), robot
(Agent IA), dossier (Notion), globe (Web), coche (statuts "envoyé"/"répondu"). Plus robuste que
les emoji de toute façon — ne dépend d'aucune police, rendu identique partout.

Polices Inter embarquées en base64 dans `@font-face` (`font-display: block`) pour éviter toute
race de chargement — gardé même si la vraie cause était fontconfig, ça reste une bonne pratique.

Nouveau rendu vérifié visuellement (frames extraites à plusieurs timestamps) : texte, captions
mot-à-mot, icônes SVG, badges souveraineté, CTA — tout s'affiche correctement. `ffprobe` : H.264
1080×1920, AAC, durée 16.77s, ~7.1MB.

**Uploadé sur Blotato (lien media only, PAS publié)** :
`https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/b784d6ed-953a-4f0a-b16b-6bb02080c114.mp4`

Prochaine étape inchangée : publication Blotato, compte à confirmer avec l'utilisateur.

---

## ✅ RENDU FINAL COMPLET (2026-07-08) — ⚠️ voir correctif ci-dessus, ce rendu avait le texte invisible

`public/renders/telegram-agent-ia-FINAL-hyperframes.mp4` — **le vrai rendu de `public/index.html`**,
toutes scènes de motion design incluses (hook ChatGPT→Mon IA, mockup message Telegram, schéma
d'automatisation Telegram→Agent IA→Notion→Web, badges souveraineté, carte CTA "Modèle gratuit / AGENT"),
avec les 18 captions TikTok mot-à-mot et l'audio réel synchronisé.

Confirmé via `ffprobe` :
- vidéo H.264, **1080×1920**, 30fps
- audio AAC
- durée **16.77s**
- taille 6.87MB, bitrate ~3.28Mbps

Rendu réalisé avec `npx hyperframes@0.7.5 render public` en utilisant un toolchain node/ffmpeg/Chrome
présent sur cette machine mais absent du `$PATH` par défaut (`/home/claude/tools/node/bin`,
`/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static`, libs Chrome headless dans
`/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu`) — une précédente note de session affirmant
"pas de node/ffmpeg ici" était erronée/obsolète.

Corrections apportées à `public/index.html` avant que `validate` passe (`ok:true`, 0 erreur) :
ajout de `data-start="0"` manquant sur `#root`, et réduction de ~0.01s sur 4 clips dont la fin
tombait exactement sur le début du clip suivant (chevauchement dû à l'arrondi flottant : scene-4,
cap-3, cap-11, cap-15, cap-17).

**Uploadé sur Blotato (2026-07-08, lien média seulement, PAS publié)** :
`https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/55ac48ce-ac1a-4198-a0fc-05f5f127af61.mp4`
— utilisable pour prévisualiser la vidéo/faire des retouches avant de décider de publier. Aucun
`blotato_create_post` n'a été appelé, rien n'est parti sur un réseau social.

**Prochaine étape : publication Blotato** (section plus bas, compte à confirmer avec l'utilisateur
avant tout post public).

## Vidéo alternative générée plus tôt (2026-07-08, via service distant) — ⚠️ pas la composition HyperFrames

`public/renders/telegram-agent-ia-avatar-composed.mp4` (8.5MB, MP4 valide, durée mesurée ~16.25s)
a été généré **réellement** en appelant directement `https://ffmpeg.tonypayet.com/avatar-video-background`
(le service HTTP derrière le nœud n8n "Compose Video FFmpeg", débranché du graphe mais
accessible en curl indépendamment de n8n) avec l'avatar, la vraie voix et les vrais transcripts
de l'execution `63818`.

**Important : ce n'est PAS un rendu de `public/index.html`.** C'est une composition différente,
plus simple, faite par ce service : avatar en chromakey + sous-titres mot-à-mot incrustés
directement sur la vidéo avatar (pas de fond). Elle n'a **aucune** des scènes de motion design
construites dans `public/index.html` (pas de schéma d'automatisation Telegram→Agent IA→Notion→Web,
pas de badges souveraineté, pas de carte CTA "Modèle gratuit / AGENT"). Utilisable comme vidéo de
secours/rapide, mais pour la vraie version premium Autoboost Neon Video il faut toujours rendre
`public/index.html` via `npm run render` sur une machine avec node+ffmpeg (section suivante,
toujours valable).

## État de la session (2026-07-08) — mise à jour

**Fait depuis les notes du 2026-07-07 :**
- Le bug 1 (polling TTS) est confirmé corrigé et **testé avec succès en conditions réelles** :
  execution n8n `63818` (2026-07-07T16:34-16:38, workflow `S85QlXjhIO6nBvzY`) a tourné sur le
  vrai payload de cette vidéo (#4 Telegram Agent IA) et a réussi de bout en bout.
- Audio réel récupéré et copié dans `public/assets/voice.mp3` :
  `https://d2h7xmz5gqybh9.cloudfront.net/output/ecf36bdb-71ae-4e74-863c-61bc63363684-u2_f154bc96-c0b1-4e3c-80bd-e84ee28c6394.mp3`
  (durée réelle Whisper : **15.89s**, débit narration plus rapide que l'estimation initiale de 22.09s).
- **`public/index.html` entièrement resynchronisé** sur les vrais timestamps mot-à-mot Whisper de
  cette exécution (durée totale recalée à **16.73s** = narration 15.89s + tenue CTA ~2s) :
  scènes, 18 captions, avatar, anneau CTA — tout resitué sur les nouveaux repères (voir le fichier).
  Attention : Whisper a mal entendu "ChatGPT" (scindé en "chaque"+"GPT") et "Notion" (transcrit
  "notions") dans son texte brut — le texte affiché à l'écran garde l'orthographe correcte, seuls
  les timestamps de ces mots ont servi à caler `data-start`/`data-duration`.
- Ce qui reste bloquant : toujours pas de node/npm/ffmpeg dans ce sandbox → `validate`/`inspect`/
  `render` doivent se faire **sur une machine avec ce toolchain** (voir section plus bas, inchangée).

## État de la session (2026-07-07) — à reprendre ici

**Fait :**
- Projet HyperFrames complet ci-dessous (`public/index.html`) — scènes, captions, avatar, palette.
- Diagnostic complet du webhook n8n `avatar-webhook-v2` (workflow `S85QlXjhIO6nBvzY`, actif, MCP maintenant activé) :
  - **Bug 1 (bloquant)** : le node `Wait Voice Clone` attend un temps fixe (20s) puis vérifie **une seule fois** le statut WaveSpeed via `Get Voice Clone Result` → `Extract Audio URL` échoue avec `"Qwen TTS: pas URL audio"` si la synthèse vocale n'est pas terminée (ce qui arrive souvent pour un texte de cette longueur — confirmé sur 2 tentatives réelles, executions `63804`/`63805`). Exécutions passées réussies (`61961` MenuAuto, `61922`) ont eu de la chance avec un texte plus court/API plus rapide ce jour-là.
  - **Bug 2 (important)** : même quand ça réussit, le node `Compose Video FFmpeg` (censé assembler avatar + captions + voix via `ffmpeg.tonypayet.com/avatar-video-background`) est **déconnecté du graphe** (aucune connexion entrante/sortante). Donc ce webhook ne produit **jamais** de vidéo composée actuellement — il renvoie seulement `{transcripts: [...timestamps mot-par-mot...], voiceUrl: "...mp3"}` via `Respond to Webhook`. Confirmé sur l'execution réussie `61961`.
  - **Sécurité** : le node `Get Voice Clone Result` contient une clé API WaveSpeed **en clair** dans ses paramètres (`Authorization: Bearer wsk_live_...`) au lieu d'une credential n8n chiffrée. À faire tourner et déplacer vers une credential — je n'ai pas d'outil `manage_credentials` dans cette session pour le faire moi-même (seulement `list_credentials`).
- Voix de marque confirmée utilisable : `https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3` (accessible, 200 OK).
- Avatar par défaut confirmé utilisable : `https://assets.automatisationboost.com/video/avatar/auto%20avatar%20(online-video-cutter.com).mp4` (accessible, 200 OK).
- Accès MCP activé sur le workflow `S85QlXjhIO6nBvzY` (fait par l'utilisateur en cours de session).

**En cours / prochaine étape :**
- Tu as demandé de corriger le Bug 1 dans le workflow n8n (remplacer le Wait fixe par une vraie boucle de polling : `Init Poll State` (code) → `Poll Wait` (wait ~5s) → `Poll TTS Status` (HTTP GET) → `Merge Poll Result` (code, incrémente attempts) → IF "prêt ?" → si oui: `Extract Audio URL` (adapté) → suite inchangée ; si non → IF "attempts >= 24 (~2min) ?" → si oui: erreur timeout ; si non: reboucle sur `Poll Wait`). Conception validée mentalement, **pas encore appliquée** via `update_workflow` au moment de cette sauvegarde.
- Une fois corrigé : rappeler le webhook `avatar-webhook-v2` avec le payload déjà utilisé (avatarUrl/voixUrl ci-dessus + description = script narration ci-dessous), récupérer `voiceUrl` (vrai MP3) + `transcripts` (timestamps réels), puis :
  1. Télécharger `voiceUrl` → `public/assets/voice.mp3`.
  2. Resynchroniser `data-start`/`data-duration` des 18 captions + durée totale de `#root`/`#avatar`/`#voice` sur les vrais timestamps `transcripts`.
  3. Rendre via `npx hyperframes` **sur ta machine** (toujours impossible ici, pas de node/ffmpeg).
  4. Publier sur Blotato (voir section plus bas, compte à confirmer).
- Bug 2 (Compose Video FFmpeg déconnecté) n'a pas besoin d'être réparé pour ce plan — on utilise le HyperFrames local pour l'assemblage final, pas ce node.

Source : ligne #4 du [Sheet de suivi](https://docs.google.com/spreadsheets/d/10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags/edit) — CTA `AGENT`.

## Ce qui est déjà fait

- `public/index.html` — composition HyperFrames complète (1080x1920, 22.09s provisoire) :
  hook "ChatGPT → Mon IA", mockup message Telegram, schéma automation
  (Telegram → Agent IA → Notion → Web), badges souveraineté ("Mon IA / Mes données / Mon serveur"),
  CTA "Modèle gratuit — Commente AGENT".
- Captions TikTok mot-à-mot (18 captions, 3 mots max, un mot actif jaune/violet/orange par phrase).
- `public/assets/avatar-keyed.mp4` — avatar déjà keyé, réutilisé depuis le projet
  `autoboost-03-lead-generation` (mets à jour ce fichier si tu veux un nouveau take pour cette vidéo).
- Palette Autoboost Neon Video (noir mat + jaune `#FFE600` / violet `#A855F7` / orange `#FF8A3D`) respectée.

## Ce qu'il te reste à faire (dans l'ordre)

### ~~1. Consentement voix clonée~~ — fait

L'audio livré par l'execution `63818` utilise la **voix de marque** `archiviste_ZIl7EoOf.mp3`
(pas un clone de la voix personnelle de l'utilisateur), donc pas de consentement voix-clonée
à obtenir pour cette prise-là. Si tu régénères avec ta propre voix clonée, redemande le
consentement explicite avant l'appel WaveSpeed.

### ~~2. Générer l'audio~~ — fait

`public/assets/voice.mp3` contient déjà le rendu réel (15.89s, voir section "État de la session
2026-07-08" plus haut pour l'URL source CloudFront).

### ~~3. Resynchroniser les timings~~ — fait

`public/index.html` est resynchronisé sur les vrais timestamps Whisper de l'execution `63818`
(durée totale 16.73s). Si l'avatar (`avatar-keyed.mp4`, réutilisé du projet #03) est plus court
que 16.73s au render, boucle-le avec `ffmpeg -stream_loop -1 -t 16.73` (jamais via `trim` dans
le filter graph, voir CLAUDE.md racine).

### 4. Valider puis rendre

```bash
cd autoboost-04-telegram-agent-ia
npx -p node@22 -p hyperframes hyperframes validate public --json
npx -p node@22 -p hyperframes hyperframes inspect public
# Corriger tout dépassement de captions avant de rendre (voir règles captions du skill)
npx hyperframes@0.7.5 render
ffprobe -v quiet -show_entries format=duration,size -of default=noprint_wrappers=1 public/renders/*.mp4
```

### 5. Publier sur Blotato

1. `blotato_list_accounts` pour confirmer le compte cible (ex. Instagram `automatisationboost`,
   ou un compte TikTok) — **toujours confirmer avec l'utilisateur** avant de publier.
2. Upload du MP4 rendu → obtenir une URL média Blotato (`blotato_create_presigned_upload_url` + upload).
3. `blotato_create_post` avec :
   - légende = texte TikTok + hashtags de la ligne #4 du Sheet :
     > 🤖 J'ai créé mon assistant IA personnel sur Telegram avec n8n. Il répond, gère Notion,
     > cherche sur le web. Mes données. Mon serveur. Pas ChatGPT. Commente AGENT pour le workflow 👇
     > #agentia #telegram #n8n #automatisation #intelligenceartificielle
   - `mediaType`: `reel` (ou équivalent plateforme)
4. Rapporte l'URL/ID du post — je peux le faire depuis Claude si tu me passes le MP4 final (upload ou URL publique).
5. Mets à jour manuellement le Sheet : `Statut Tournage` → ✅ Fait, `Vidéo Finale`, `Date Publication`.

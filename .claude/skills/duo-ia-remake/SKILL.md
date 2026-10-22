---
name: duo-ia-remake
description: Duo « Tony + Tony IA » — refait un reel (concurrent, actu IA, démo) dans le style de Tony sous forme de dialogue entre Tony et son avatar IA qui le taquine, en vidéo 9:16 HyperFrames. Récupère le script du reel, le réécrit avec humour en répliques moi / ia, génère chaque réplique avec la voix clonée de Tony, monte la vraie prise de Tony re-synchronisée sur la voix (ou l'avatar de la banque), l'avatar IA dans un cercle néon violet dont les lèvres ne bougent que sur ses répliques, les animations calées au mot, la Valse des fleurs et le CTA « commente MOT ». Déclencheurs - « refais ce reel avec moi et mon IA », « remake dans mon style », « mon avatar IA qui réagit », « dialogue avec mon IA », « fais comme Claude monte comme un pro », Tony envoie un lien Instagram/TikTok et veut sa version.
---

# Duo IA remake — Tony + Tony IA

Référence complète, déjà livrée et validée : **`autoboost-neon-videos/autoboost-80-claude-monte-comme-un-pro/`**
(remake de « Claude can finally edit like a pro », 53 s). **Partir de ce projet, ne pas réécrire de zéro.**
Deuxième exemple, sans vraie prise (avatar seul) : `autoboost-82-robots-nvidia/`.

Répondre à Tony en français ; code, commentaires et commits en anglais. Charte : or `#eab308`, violet `#8b5cf6`,
rouge `#ff6b6b` seulement pour « faux / lent », fond encre. **Aucun vert, aucun emoji.**

## Ce qu'on ne fait jamais
- Reposter la vidéo d'un autre en effaçant son nom, son logo ou son filigrane. Un remake = **le script réécrit**,
  aucune image du reel d'origine. Pour montrer ses images, c'est une **réaction** (extraits courts + crédit visible).
- Inventer un chiffre ou un fait : tout fait affiché vient du reel ou d'une source vérifiée (sinon, le formuler prudemment).
- Écrire une clé API dans un fichier du dépôt. La clé WaveSpeed passe par la variable `WAVESPEED_API_KEY`.

## 1 · Le script (dans la conversation)
1. Récupérer le texte du reel : `mcp__tokscript__get_instagram_transcript` (ou TikTok). Le téléchargement de la vidéo
   demande un abonnement tokscript : pour une réaction, demander le mp4 à Tony.
2. Vérifier le sujet (nom exact du projet / de l'outil) par une recherche web rapide.
3. Écrire `session/script.json` : `{"source": "...", "lines": [["moi", "..."], ["ia", "..."], ...]}`.
   - 10 à 15 répliques, 35-55 s au total. Tony explique, l'IA le taquine (1 réplique IA toutes les 2-3 de Tony).
   - Si Tony a dicté des répliques, **les garder mot pour mot** (juste la ponctuation).
   - Une info nouvelle ou une vanne toutes les 2-4 s. Phrases courtes.
   - Fin : CTA « commente MOT ». Si le mot n'a pas de message automatique (Auto-DM), le signaler à Tony.
   - Pas d'humour forcé si Tony dit « pas toujours drôle » : l'IA réagit, elle ne fait pas un sketch.

## 2 · Les voix
```bash
export WAVESPEED_API_KEY=...        # donnée par Tony, jamais commitée
python3 .claude/skills/duo-ia-remake/scripts/tts_wavespeed.py session/script.json build/vo
```
- Voix de référence : `autoboost-neon-videos/_shared/voix/reference-tony.mp3` (servie en raw GitHub ; le dépôt est public).
- F0 attendue 110-135 Hz par réplique. ~200 Hz = mauvaise voix → régénérer.
- Plan B : le webhook n8n `tts-gen` via `face-cam-boost/scripts/facecam_dialogue.py` (fonction `tts`), s'il répond.
- Les répliques IA reçoivent la couleur « machine » au montage (+1 demi-ton, petit écho) :
  `aresample=48000,asetrate=48000*1.06,aresample=48000,atempo=0.9434,aecho=0.8:0.5:14:0.22,highpass=f=140`.
  **Toujours `aresample=48000` avant `asetrate`** : les mp3 WaveSpeed sont en 24 kHz, sinon la voix part en accéléré.

## 3 · L'image de Tony
**Avec une vraie prise de Tony** (cas de la vidéo 80) :
1. `build.py` (copier celui de la 80) : place les répliques bout à bout, transcrit les mots (faster-whisper),
   écrit `voice.wav` + `vo.json`, monte l'avatar IA (lèvres actives seulement sur ses répliques) et la musique.
2. La prise à 30 fps fixes, puis le détourage **une seule fois** sur la prise entière :
   `npx hyperframes remove-background take30.mp4 -o take_alpha.webm` (~0,5 s / image sur CPU).
3. **Synchro des lèvres** : `resync.py take30.mp4 take30.mkv take_alpha.webm build/`. Pour chaque bloc de répliques de Tony,
   il cherche le passage de la prise dont le rythme de voix colle le mieux, coupe dans les pauses, puis cale chaque syllabe
   (DTW, gel max 2 images). Il affiche l'écart bouche/voix par réplique : **viser ≤ 6 %** (l'ancienne méthode : 27-49 %).
   Il écrit `tony_src.mp4` (non détouré), `tony.webm` (détouré) et `tony_cuts.json` (les coupes → punch-ins).
4. Vérifier : planches des lèvres autour de chaque réplique (bouche ouverte quand la voix parle, fermée dans les pauses).

**Sans prise de Tony** (avatar seul, cas de la 82) : `autoboost-82-robots-nvidia/avatar_take.py` construit une prise
« face cam » avec la banque avatar VOITURE (`_shared/avatar-bank/clips-new`, fenêtres lèvres de `lips-map-d.json`)
sous les répliques, puis on l'habille avec AutoBoost Studio (style Seedance néon) ou le motion de la 80.
Un décor par vidéo : VOITURE pour humour / opinion, BUREAU pour tuto (`_shared/avatar-bank/MANIFESTE.md`).

## 4 · Le motion design
Copier `autoboost-80…/motion/` (`gen.py` + `template.html`) et réécrire les scènes :
- Tony détouré en bas (`TY, BASE = 640, 0.94`), la prise non détourée dessous pour un effet « révélation ».
- L'avatar IA dans le cercle néon violet sur l'épaule de Tony (`IAX, IAY, IAS = 590, 1200, 0.5`) avec l'étiquette
  « TONY IA ». Quand l'IA parle, Tony s'assombrit (brightness .72) et se décale de −70 px.
- Une scène par idée, chaque apparition calée sur un mot de `vo.json`. Gags visuels qui illustrent la vanne de l'IA.
- Sous-titres : bord or pour Tony, bord violet + pastille « IA » pour l'IA.
- Pièges déjà rencontrés : halo gris si `brightness` et `drop-shadow` sont sur le même élément (mettre la luminosité
  sur un conteneur intérieur) ; mots coupés en deux (couper seulement entre les mots) ; tête de Tony sur les cartes ;
  cercle IA hors cadre ou sur le visage ; bouton CTA visible trop tôt.
```bash
BUILD=build python3 motion/gen.py && npx hyperframes lint motion/public          # 0 erreur exigé
npx hyperframes snapshot motion/public --at <un instant par scène> --no-end --no-browser-gpu
npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery --no-browser-gpu
```
Regarder chaque planche avant le rendu.

## 5 · Le son et la livraison
- Musique : la Valse des fleurs maison, `bed_valse.py build/` (version évidée sous les voix, orchestre complet qui conclut
  juste après la dernière réplique). Autre musique sur demande de Tony.
- Mixage : `face-cam-boost/scripts/facecam_audio.py --voice build/voice.wav --events motion/events.json --frames N
  --out mix.wav --bed-file build/bed.wav --bed-gain -6` (voix normalisée à part, puis −16 LUFS).
- Mux : `ffmpeg -i silent.mp4 -i mix.wav -map 0:v -map 1:a -c:v libx264 -crf 21 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart`.
- Vérifier : durée, 1080×1920, −16 LUFS ±1, et regarder la vidéo aux moments de chaque réplique.
- Livrer : le mp4 dans `autoboost-neon-videos/autoboost-NN-sujet/`, un aperçu à Tony, README court, commit + push.
  Ne pas publier sur les réseaux sans son accord explicite pour cette vidéo.

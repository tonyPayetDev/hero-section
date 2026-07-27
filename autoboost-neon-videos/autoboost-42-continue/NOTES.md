# autoboost-42-continue — Continue, l'alternative gratuite à Cursor

**Statut : DRAFT bloqué — composition prête, voix non générée (blocage réseau).**
Créé par la routine planifiée du 2026-07-27. Aucune vidéo rendue, aucune publication.

## Sujet (Google Sheet, onglet "30 Vidéos")
Première ligne `Statut Tournage = ⬜ À faire` (par ordre de ligne) :
- **Workflow** : « Alternative gratuite à Cursor (Continue) »
- **Mot-clé CTA** : `CODEUR`
- **Hashtags** : `#IA #codeur #devweb #opensource #productivite`
- **Texte TikTok** : « L'alternative gratuite à Cursor que personne ne montre. Follow pour plus
  de comparatifs IA + commente CODEUR pour la config. »

## Ce qui BLOQUE (à débloquer pour finir)
La politique d'egress réseau de cet environnement planifié **refuse (HTTP 403 CONNECT) tout
`*.automatisationboost.com`**. Confirmé via `$HTTPS_PROXY/__agentproxy/status` — refus de politique
organisationnelle, à ne pas contourner (cf `/root/.ccr/README.md`). Conséquences :

1. **Voix clonée impossible** — `POST https://n7n.automatisationboost.com/webhook/avatar-webhook-v2`
   injoignable (403). Donc pas de `voice.mp3` ni de transcripts Whisper mot-à-mot.
2. **Fallback MCP n8n indisponible** — le serveur MCP n8n exige une auth OAuth, impossible en
   session planifiée non-interactive.
3. **Report Sheet impossible** — `POST .../webhook/sheet-video-update` (étape 5) également en 403.
4. **Vérif publication (étape 4bis) impossible** — `previsualisation.automatisationboost.com` en 403.

Aucune voix locale off-brand n'a été substituée (ce serait l'erreur type du 22/07). Rien n'a été
inventé ni faussement déclaré disponible.

## Ce qui MARCHE dans cet environnement
- Toolchain : node v22, **ffmpeg 6.1.1 installé** (`apt-get install ffmpeg`, libx264+aac OK),
  **Chrome headless installé** (`npx hyperframes browser ensure`), hyperframes 0.7.76, fontconfig
  système natif (59 polices, pas besoin de `FONTCONFIG_PATH` dans ce sandbox cloud).
- Lecture Google Sheet (MCP Google-Drive) OK.
- git / GitHub OK.

## Travail déjà fait (récupérable à 100 %)
- `public/index.html` — composition complète, fidèle au gabarit **seedance #40** (1080x1920,
  matte black + néon jaune/violet/orange, avatar overlay persistant, badges/jauge, captions néon
  mot-à-mot, 5 scènes + broll + CTA). `hyperframes check` : **Layout 0 problème / 9 échantillons,
  Runtime & Motion 0 erreur** ; seule erreur = `voice.mp3` absent (le blocage ci-dessus).
- Assets déjà copiés dans `public/assets/` :
  - `flowers_horror.mp3` (BGM palette, `data-volume=0.05`, -12,4 LUFS) — **PAS** bgm-ascension.
  - 12 SFX palette v1 (`sfx-*.mp3`) — rôles transposés du gabarit, volumes 0.13–0.26 figés.
  - `avatar-keyed.mp4` (réutilisé de autoboost-41, 37s, couvre la timeline).
  - `broll-creator.mp4`, `gsap.min.js`.
- Narration finalisée (106 mots, ~31s au débit archiviste, formule hook→3 étapes→CTA), voir
  `.work/script.txt`. CTA écrit « Commente le mot CODEUR » (jamais « Commente CODEUR »).

## Pour finir (dès que le réseau autorise automatisationboost.com, OU en session interactive)
1. Générer la voix : `POST avatar-webhook-v2` avec le payload déjà prêt dans `.work/payload.json`
   (`voixUrl` archiviste + `avatarUrl` défaut + `description` = script). Récupérer `voiceUrl` +
   `transcripts`. Si timeout : `search_executions` + `get_execution(includeData:true)` via MCP n8n.
2. Télécharger `voiceUrl` → `public/assets/voice.mp3`. Vérifier taille + `ffprobe` (vrai MP3).
3. **Recaler le timing** (actuellement PROVISOIRE = scaffold seedance) :
   - `ffmpeg -i voice.mp3 -af silencedetect=noise=-40dB:d=0.18 -f null -` → poser les coupes de
     scène (`data-s`/`data-d`) dans les silences.
   - Remplacer les timestamps du tableau `caps` (dans `index.html`) par les `transcripts` Whisper.
   - Ajuster `DUR` / `data-duration` sur la durée réelle du MP3.
4. `npx hyperframes check public` (0 erreur attendu) puis rendre (fond, ~3-4 min).
5. **Vérifier visuellement** des frames extraites du MP4 (pas seulement ffprobe).
6. Publier dans le dépôt `previsualisation` (nouvelle route `autoboost-42-continue`, ne rien
   écraser) : `video.mp4` + `index.html`, commit/push `main`.
7. Vérifier que c'est servi (cache-buster) :
   `curl -s -o /dev/null -w '%{http_code} %{size_download}' -L "https://previsualisation.automatisationboost.com/autoboost-42-continue/video.mp4?cb=$RANDOM"`
   → attendu 200 + plusieurs Mo. Si 404 : Coolify ne redéploie pas au push, déclencher le deploy.
8. Report Sheet : `POST .../webhook/sheet-video-update` avec
   `{cta:"CODEUR", statut:"🟡 En attente validation", videoUrl:"<url previsualisation>"}`.

## Note de style
Le gabarit seedance utilise des captions à **40px** (`.caption{font-size:40px}`) et layout validé
sans débordement — reproduit tel quel. La consigne « 27px » de la routine diverge du gabarit
mandaté ; le gabarit fait foi (« reproduis-le »). À confirmer avec Tony si besoin.

# autoboost-135-vps-coolify-seedance — recette de reproduction

Variante **style seedance** (gabarit `autoboost-40-seedance`) du sujet #135, produite parce que la
ligne Sheet était encore `⬜ À faire` et que la version existante `autoboost-135-vps-coolify` avait été
montée en pipeline **v3** (assemblage banque avatar), pas dans le style néon seedance demandé.

## Source

- Sheet `10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags`, onglet `30 Vidéos`, **row_number 137** (colonne `#` = 135, décalée — ne pas viser par elle).
- Lu via workflow n8n one-off (`docs.google.com` bloqué par la politique réseau du sandbox : `CONNECT tunnel failed 403`).
- **Sujet** : VPS + Claude Code + Coolify — 3 étapes pour héberger soi-même ses automatisations.
- **Mot-clé CTA** : `TERMINAL`.
- **Hashtags** : `#claudecode #n8n #vps #automatisation #freelance`.

## Style — gabarit seedance (non négociable)

- Gabarit : `autoboost-neon-videos/autoboost-40-seedance/public/index.html` (1080×1920, matte black + néon jaune/violet/orange, avatar overlay circulaire persistant + b-roll plein écran, badges/cartes UI, captions néon mot-à-mot).
- **Captions à 27 px** (instruction explicite de la tâche, `top ~960px`, un seul mot coloré par phrase).
- BGM : `_shared/bgm/flowers_horror.mp3` (« YOU CAN ASK THE FLOWERS (HORROR MIX) », −12,4 LUFS → `data-volume=0.05`). « horror » = nom du morceau, pas une ambiance.
- SFX : palette figée `_shared/sfx-palette/v1` — rôles/volumes du README, `data-start` recalés sur MES coupes.

## Voix

Réutilisée **à l'identique** du projet `autoboost-135-vps-coolify` (même `voice.mp3`, 33,984 s, voix clonée
archiviste via `avatar-webhook-v2`/qwen3-tts, consentement permanent). Whisper avait renvoyé `transcripts: []`
(quota OpenAI épuisé) → captions estimées manuellement dans le projet 135, **reprises telles quelles ici**
puisque c'est le même MP3. Coupes de scène posées dans les silences réels (`silencedetect -40dB`) :
`3.73 / 6.73 / 9.10 / 12.52 / 17.17 / 22.90 / 27.83 / 30.76`.

## Avatar

Set **BUREAU** de la banque (`_shared/avatar-bank/clips/` A1+B1+C2, décor studio sombre — décor
« je t'apprends quelque chose », adapté au sujet technique). Concat + boucle → `assets/avatar-loop.mp4`
(muet, 34 s, GOP 15 seek-safe), posé dans le cercle néon du gabarit. Pas de détourage `geq` (les clips
BUREAU n'en ont pas besoin, contrairement au vieux `avatar-hq/`).

## B-roll

`_shared/broll-abstrait/circuit-9x16.mp4` (circuit = matériel/serveur), réencodé seek-safe → `assets/broll.mp4`,
fenêtre 22,90 → 27,83 s (respiration « le setup que j'utilise »), avatar masqué pendant cette fenêtre.

## Structure (7 scènes + b-roll)

1. HOOK — VPS à 5€/mois, sans agence (carte coût agence vs VPS)
2. 3 ÉTAPES — chips Coolify / Claude Code / 24-7
3. ÉTAPE 1 — Coolify déploie tout seul (carte coolify.app)
4. ÉTAPE 2 — Claude Code branché en MCP (carte terminal — renforce le mot-clé TERMINAL)
5. ÉTAPE 3 — tout tourne 24/7 (liste n8n / sites / vidéos + « même PC éteint »)
6. SETUP — jauge « 3 à 7h la 1ʳᵉ fois → plus rien ensuite »
7. CTA — Freelance ? → mot `TERMINAL` + « je t'envoie le guide gratuit »

## Rendu

`npx hyperframes render public -o public/renders/video.mp4` (ffmpeg + Chrome headless installés en début
de session ; `apt-get install --no-install-recommends ffmpeg` + `hyperframes browser ensure`). Vérifié
visuellement sur frames extraites.

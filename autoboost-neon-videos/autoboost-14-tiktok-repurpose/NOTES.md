# Autoboost Neon Video — #14 TikTok vers YouTube et Instagram

Source : ligne #14 du [Sheet de suivi](https://docs.google.com/spreadsheets/d/10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags/edit) — CTA `REPURPOSE`.
Workflow n8n : https://n7n.automatisationboost.com/workflow/puHoAu9N5SkLofiy

## Narration

103 mots, 32,42 s d'audio. Le script du Sheet (40 mots ≈ 12 s) a été étoffé pour tenir la
règle des 25-35 s : ajout du détail de process (réécriture IA des descriptions), d'une preuve
concrète ("hier soir / ce matin") et du bénéfice chiffré (×3 vues).

Voix : webhook n8n `avatar-webhook-v2` (workflow `S85QlXjhIO6nBvzY`, exécution **64061**),
voix de marque `archiviste_ZIl7EoOf.mp3`, WaveSpeed `qwen3-tts/voice-clone`.
Le webhook renvoie HTTP 524 (timeout Cloudflare) mais l'exécution n8n aboutit — récupérer
`voiceUrl` + `transcripts` via `get_execution({includeData:true})`.

**À noter** : Whisper transcrit le CTA en « répropose ». Le mot est bien affiché `REPURPOSE`
en caption et dans la scène CTA, mais la prononciation TTS du mot anglais reste approximative.

## Structure (33 s, 1080×1920, 30 fps)

| Fenêtre | Scène | Avatar |
|---|---|---|
| 0 – 6,04 | Hook « Une vidéo TikTok. Une seule plateforme. » | visible |
| 6,04 – 13,72 | 4 étapes du workflow (récupère / watermark / format / IA) | visible |
| 13,72 – 17,46 | **Broll B** — triptyque YouTube / Instagram / TikTok (Mixkit 42283) | masqué |
| 17,46 – 22,66 | Fan-out 1 → 3 plateformes | visible |
| 22,66 – 26,76 | **Broll A** — créatrice qui filme + « ×3 plus de vues » (Mixkit 50406) | masqué |
| 26,76 – 30,42 | Stat 1 → 3, « Zéro effort supplémentaire » | visible |
| 30,42 – 33,0 | CTA « Commente REPURPOSE » | visible |

Broll : Mixkit, licence Mixkit Free (usage commercial, sans attribution).

## Parité du ring avatar

Les trois tweens de respiration de `#avatar-ring` utilisent `repeat: 25 / 9 / 5` — tous
**impairs**, pour que le yoyo retombe à `opacity: 0` avant chaque coupure broll (voir le piège
documenté dans le skill `veille-to-video`).

## Captions

36 groupes, timestamps Whisper mot-à-mot réels (pas d'estimation). Bande à `top: 960px`.
La bande de texte du broll B a dû être descendue à `top: 1090px` : à 960px elle chevauchait
les captions (`inspect` → `content_overlap`).

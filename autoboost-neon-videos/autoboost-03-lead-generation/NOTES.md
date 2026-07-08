# Autoboost Neon Video — #3 Lead Generation & Cold Email

Préparé par Claude dans un environnement **sans Node.js** (validate/inspect/render sont impossibles ici).
Ce dossier est prêt à être ouvert et rendu **sur ta machine locale**.

Source : ligne #3 du [Sheet de suivi](https://docs.google.com/spreadsheets/d/10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags/edit) — CTA `LEADS`.

## Ce qui est déjà fait

- `public/index.html` — composition HyperFrames complète (1080x1920, 18s provisoire) :
  hook, dashboard "entreprises cibles", schéma automation (Contacts → Agent IA → n8n → Email),
  compteur 100% automatique, CTA "Modèle gratuit — Commente LEADS".
- Captions TikTok mot-à-mot (3 mots max, un mot actif jaune/violet/orange par phrase).
- `public/assets/avatar-keyed.mp4` — avatar déjà keyé, copié depuis
  `automationboost/assets/video/seedance-2-prompts/avatar-keyed.mp4`.
- Palette Autoboost Neon Video (noir mat + jaune `#FFE600` / violet `#A855F7` / orange `#FF8A3D`) respectée.
- Les workflows n8n `tts-gen` et `avatar-webhook-v2` ont été corrigés pour appeler
  `wavespeed-ai/qwen3-tts/voice-clone` (au lieu de l'ancien `omnivoice`, déprécié) — voir historique de session.

## Ce qu'il te reste à faire (dans l'ordre)

### 1. Consentement voix clonée (obligatoire avant tout appel)

Avant d'appeler le webhook TTS avec ta voix, confirme explicitement, par exemple :
> "J'autorise l'envoi de mon échantillon de voix à WaveSpeed pour générer l'audio de cette vidéo Lead Generation."

### 2. Générer l'audio (narration ci-dessous, ~18s à un débit énergique)

```
Arrête de prospecter à la main comme en 2010. Ce workflow trouve les entreprises
cibles, enrichit les contacts, rédige un email personnalisé pour chacun, et envoie
tout, cent pour cent automatique. C'est gratuit. Commente LEADS pour le récupérer.
```

Appelle le webhook n8n (déjà corrigé pour qwen3-tts) :

```bash
curl -s -X POST "https://n7n.automatisationboost.com/webhook/avatar-webhook-v2" \
  -H "Content-Type: application/json" \
  -d '{
    "avatarUrl": "<URL de ton avatar/setup>",
    "voixUrl": "<URL de ton échantillon de voix .wav>",
    "description": "Arrête de prospecter à la main comme en 2010. Ce workflow trouve les entreprises cibles, enrichit les contacts, rédige un email personnalisé pour chacun, et envoie tout, cent pour cent automatique. C'est gratuit. Commente LEADS pour le récupérer.",
    "userEmail": "tony.payet.professionnel@gmail.com"
  }'
```

`voixUrl` doit être une URL accessible (pas un chemin local `C:\...`) — héberge ton
`voice-reference-clean.wav` quelque part (assets.automatisationboost.com, Coolify, etc.)
si ce n'est pas déjà fait, ou utilise le webhook `tts-gen` séparément si tu veux juste
l'audio sans le montage avatar+background fait par n8n.

Place le résultat sous `public/assets/voice.mp3`.

### 3. Resynchroniser les timings

La durée `data-duration="18"` sur `#root` et sur `#voice`, et les 14 captions
(`data-start`/`data-duration` de `cap-1` à `cap-14`), sont calées sur une estimation
(38 mots ≈ 18s). Une fois `voice.mp3` généré :

- Mesure sa durée réelle (`ffprobe -show_entries format=duration voice.mp3`).
- Ajuste `data-duration` sur `#root`, `#voice`, `#avatar`, et les 5 scènes + 14 captions
  proportionnellement (ou reprends les timestamps mot-à-mot si tu as une transcription).

### 4. Valider puis rendre

```bash
cd autoboost-03-lead-generation
npx -p node@22 -p hyperframes hyperframes validate public --json
npx -p node@22 -p hyperframes hyperframes inspect public
# Corriger tout dépassement de captions avant de rendre (voir règles captions du skill)
npx hyperframes@0.7.5 render
ffprobe -v quiet -show_entries format=duration,size -of default=noprint_wrappers=1 public/renders/*.mp4
```

### 5. Publier sur Blotato

Compte cible confirmé : **Instagram `automatisationboost`** (id `54617`, `mediaType: reel`).

1. Upload du MP4 rendu → obtenir une URL média Blotato (`blotato_create_presigned_upload_url` + upload, ou équivalent).
2. `blotato_create_post` avec :
   - `accountId`: `54617`
   - légende = texte TikTok + hashtags de la ligne #3 du Sheet (à relire, colonne "Texte TikTok + Hashtags")
   - `mediaType`: `reel`
3. Rapporte-moi l'URL/ID du post, je peux le faire depuis Claude si tu me passes le MP4 final (upload ou URL publique).
4. Mets à jour manuellement le Sheet : `Statut Tournage` → ✅ Fait, `Vidéo Finale`, `Date Publication`.

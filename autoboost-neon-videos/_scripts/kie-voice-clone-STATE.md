# État — Clone voix chantée Tony (Kie.ai / Suno)

Mis à jour le **2026-08-16**. But : créer un `voiceId` Suno de la voix chantée de Tony, réutilisable pour toutes les chansons.

## STATUT : bloqué sur un réenregistrement (1 prise à refaire, ~1 min de travail)

La phrase de vérification est **générée par une IA à chaque tâche** — elle n'est JAMAIS la même.
L'échantillon fourni par Tony le 2026-08-16 (« Chantons ensemble sous les étoiles et respire la musique »)
a été **refusé** : `It didn't sound like you said the phrase. Please try reading it more clearly.`
La voix et la qualité audio ne sont pas en cause — seulement le texte chanté.

### Tâche fraîche en attente
- `taskId` = **`4c33762b7ff40413f7d38d8874987d6e`** — status `wait_validating`
- Phrase à CHANTER : **« Chantons ensemble sous les reflets de la lumière musicale »**
- Consignes : a cappella, chanté (pas parlé — contrôle anti-fraude), 8-15 s, articulation nette.
- Dès réception du fichier : uploader → `POST /api/v1/voice/generate` → `voiceId` en ~1 min.
- ⚠️ Si la tâche a expiré entre-temps (`processing_validate_fail`), relancer un `validate` (gratuit, ~20 s)
  et **redonner la nouvelle phrase à Tony** avant qu'il enregistre. Idéalement : rouler la phrase
  pendant que Tony est dispo, il enregistre dans la foulée.

## Procédure qui marche (vérifiée de bout en bout)

Base `https://api.kie.ai`, auth `Authorization: Bearer $KIE_API_KEY` (clé dans `/work/.kie.env`).

1. **Générer la phrase** — `POST /api/v1/voice/validate`
   ```json
   { "voiceUrl":"https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3",
     "vocalStartS":0, "vocalEndS":8, "language":"fr" }
   ```
   → `{ "data": { "taskId": "..." } }` · **coût : 0 crédit**
2. **Lire la phrase** — `GET /api/v1/voice/validate-info?taskId=…`
   → statut `processing_validate` (~20 s) puis `wait_validating` + `validateInfo` = la phrase.
3. **Tony chante la phrase**, on convertit et on héberge :
   ```bash
   ffmpeg -y -i sample.m4a -ac 1 -ar 44100 -c:a libmp3lame -b:a 192k out.mp3
   ```
   puis `blotato_create_presigned_upload_url` + `curl -X PUT "<presignedUrl>" --data-binary "@out.mp3"`
   → la `publicUrl` sert de `verifyUrl`.
   (ffmpeg est ici : `/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static/`, pas dans le PATH.)
4. **Créer la voix** — `POST /api/v1/voice/generate`
   ```json
   { "taskId":"<taskId de l'étape 1>", "verifyUrl":"<publicUrl>",
     "voiceName":"Tony Payet Chant", "description":"...", "style":"pop",
     "singerSkillLevel":"intermediate" }
   ```
5. **Récupérer le voiceId** — `GET /api/v1/voice/record-info?taskId=…`
   → `status: success` + `voiceId`. Puis `POST /api/v1/voice/check-voice` `{"task_id":"…"}` pour confirmer.
6. **Utiliser la voix** — `POST /api/v1/generate` avec `personaId: <voiceId>` + `personaModel: "voice_persona"`.

## Pièges confirmés (ne pas les refaire)

- **`POST /api/v1/voice/regenerate` ne sert à rien ici** : renvoie `422 The record is not found or does not
  need to be rebuilt` aussi bien sur une tâche morte que sur une tâche `wait_validating`. Toujours refaire
  un `validate` complet.
- **Une tâche `processing_validate_fail` est définitivement morte** — `voice/generate` répond
  `422 Validate record is not in valid status`.
- **Rerouler la phrase pour retomber sur une phrase déjà enregistrée est inutile** : 8 tirages ont donné
  8 phrases différentes (LLM, variété illimitée). Ne pas retenter cette loterie.
- **La vérification compare bien le texte chanté** — testé avec une prise « proche mais différente », refusée.
- `check-voice` sur une tâche sans voix répond `422 suno_user_id is missing`.
- `validate`, `validate-info`, `record-info`, un `voice/generate` refusé : **tous à 0 crédit**.

## Chanson générée (sans la voix clonée, en attendant)

- `POST /api/v1/generate` — modèle **V5**, `customMode: true`, `instrumental: false`, `vocalGender: "m"`,
  paroles complètes en `prompt`, style en `style`, `callBackUrl` obligatoire.
- Polling : `GET /api/v1/generate/record-info?taskId=…` — `TEXT_SUCCESS` (~1 min) puis `SUCCESS` (~1 min 15).
- Retourne **2 variantes** avec `audioUrl` (mp3) + `imageUrl` (cover).
- **Coût mesuré : 12 crédits** pour la paire (707,92 → 695,92).
- Titre « Pendant Que Tu Dors » (FR, thème « l'IA qui bosse pendant que tu dors »),
  2 min 10 / 2 min 12 → `/work/autoboost-neon-videos/_shared/music-tony/`
- Prévisualisation : https://previsualisation.automatisationboost.com/chanson-voix-tony
- À refaire avec `personaId` = voiceId dès que le clone est validé.

## Historique

- 2026-08-12 : `validate` OK, taskId `7fe30a0bb77c838224fe6229d26c5c93`,
  phrase « Chantons ensemble sous les étoiles et respire la musique », statut `wait_validating`.
- 2026-08-16 : Tony fournit l'échantillon chanté de cette phrase — mais la tâche est entre-temps passée
  en `processing_validate_fail` (timeout upstream) et n'est plus récupérable. Nouvelle tâche
  `4c33762b7ff40413f7d38d8874987d6e` ouverte avec une nouvelle phrase.

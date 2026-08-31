---
name: chanson-ma-voix
description: Génère une chanson chantée par la VRAIE voix clonée de Tony via sunoapi.org (clone Suno). Ta voix clonée chante des paroles neuves dans le style demandé. Gère aussi : générer un instrumental seul, écrire les paroles (français/créole réunionnais), masteriser au mix (ffmpeg), et sortir une version 9:16 pour les réseaux. Utilise ce skill dès que Tony dit : « fais une chanson avec ma voix », « chanson avec ma voix clonée », « un morceau avec ma voix », « clone ma voix et chante », « refais une chanson », « ma voix qui chante X », ou décrit un morceau (rap, dancehall, ragga, séga, pop…) à chanter avec sa voix.
---

# Chanson avec la voix clonée de Tony

Pipeline complet : **voix clonée → paroles → génération → mix/master → (option) vidéo 9:16.**
La voix est clonée UNE fois puis réutilisée via son `voiceId` (stocké dans `config.json`).

## 0. Accès API

- Plateforme : **sunoapi.org** (clone de voix Suno qui marche depuis ce sandbox — contrairement à kie.ai dont le clone exige un flux de validation lourd).
- Clé : dans **`/work/.sunoapi.env`** (`SUNOAPI_KEY=...`), jamais l'afficher.
- Base : `https://api.sunoapi.org`, auth `Authorization: Bearer $SUNOAPI_KEY`.
- Fallback instrumental / cover : **kie.ai** (clé `/work/.kie.env`, base `https://api.kie.ai`, même structure d'endpoints). Voir la note mémoire `reference_kie_ai_api_access`.
- Node/ffmpeg hors PATH : préfixer `export PATH=/home/claude/tools/node/bin:/home/claude/tools/bin:$PATH`.

Charger la clé : `K=$(grep -oE '[A-Za-z0-9]{20,}' /work/.sunoapi.env | head -1)`

## 1. Récupérer / stocker le voiceId (une seule fois)

Le `voiceId` de Tony est dans **`config.json`** de ce skill. S'il est absent :
1. Demander à Tony son `voiceId` (depuis son dashboard sunoapi.org) OU le `taskId` de la création de voix.
2. Avec un `taskId` : `GET /api/v1/voice/record-info?taskId=...` → renvoie `data.voiceId` quand `status=success`.
3. Vérifier dispo : `GET /api/v1/voice/check-voice` (voiceId).
4. Écrire le voiceId dans `config.json` : `{"voiceId":"...","note":"clone Suno de Tony via sunoapi.org"}`.

**Cloner une NOUVELLE voix from scratch** (si besoin) :
- `POST /api/v1/voice/validate` avec `voiceUrl` (échantillon voix hébergé), `vocalStartS`,`vocalEndS`,`language` → `taskId`.
- `GET /api/v1/voice/validate-info?taskId=...` → **phrase de validation** à lire.
- Tony chante la phrase → héberger l'audio (voir §5 Blotato) → `POST /api/v1/voice/generate` `{taskId, verifyUrl, singerSkillLevel}` → poll `voice/record-info` → `voiceId`.

## 2. Écrire les paroles

- Français avec un peu de **créole réunionnais** (ex. « Nou lé la », « an avan », « la fèt »). Prévenir Tony qu'on n'est pas natif kréol → il ajuste.
- Calibrer la longueur au format voulu (hook + couplet ≈ 40-60 s ; morceau complet = 2 couplets + hooks).
- Structure Suno possible avec balises `[Verse]`, `[Chorus]`, `[Outro]` dans le `prompt`.

## 3. Générer la chanson avec sa voix clonée

`POST https://api.sunoapi.org/api/v1/generate` :
```json
{
  "customMode": true,
  "instrumental": false,
  "prompt": "<paroles exactes, max 5000 char>",
  "style": "<ex: ragga dancehall techno, Reunion 974, energetic, ~95 BPM>",
  "title": "<titre, max 100 char>",
  "model": "V5_5",
  "personaId": "<voiceId de config.json>",
  "personaModel": "voice_persona",
  "vocalGender": "m",
  "callBackUrl": "https://previsualisation.automatisationboost.com/kie-callback"
}
```
→ `data.taskId`. **Poll** : `GET /api/v1/generate/record-info?taskId=...` jusqu'à obtenir `audioUrl` (2 variantes dans `data.response.sunoData[]`). Télécharger les mp3.

**Instrumental seul** (pour que Tony chante lui-même par-dessus) : même appel avec `instrumental:true`, sans `prompt`/persona. (Historique : instru dancehall/afro/ragga déjà générés, voir scratchpad.)

## 4. Mix / Master (ffmpeg, `/home/claude/tools/bin/ffmpeg`)

**Master d'un morceau déjà mixé** (voix+beat collés, ex. export CapCut) :
```
highpass=f=30,equalizer=f=300:t=q:w=1.2:g=-2.5,equalizer=f=180:t=q:w=1.4:g=1.5,
equalizer=f=4000:t=q:w=2:g=4,equalizer=f=12000:t=h:g=2.5,
acompressor=threshold=-18dB:ratio=2.6:attack=12:release=180:makeup=2,
loudnorm=I=-10:TP=-1:LRA=9,alimiter=limit=0.98
```
**Delay/écho dub dancehall sur la voix** (split bande médium-aigu, écho parallèle, basses propres) :
`asplit=3[low][dry][wet]; [low]lowpass=f=180; [dry]highpass=f=180; [wet]highpass=f=200,aecho=0.85:0.45:340|680:0.4|0.22,aecho=0.9:0.9:48:0.25,volume=-3dB; amix=inputs=3:normalize=0` puis loudnorm+alimiter.

**Mixer voix seule + instru** : voix devant (2× acompressor + gain), instru `-10dB` + `sidechaincompress` ducké par la voix, `amix duration=first`, loudnorm -14. (La voix brute de Tony est souvent basse ~-28dB → compresser fort.)

Toujours vérifier `volumedetect` avant/après. Remuxer dans la vidéo : `-c:v copy -c:a aac`.

## 5. Héberger un fichier (pour les endpoints qui veulent une URL)

Via Blotato MCP : `blotato_create_presigned_upload_url(filename)` → `publicUrl`+`presignedUrl` ; puis `curl -X PUT "<presignedUrl>" --data-binary "@fichier"`. Le `publicUrl` est fetchable par les API musique.

## 6. Livrer

- Envoyer les mp3 (SendUserFile). Demander les réglages (voix devant, basses, écho, loudness).
- **Ne pas prétendre entendre** le résultat — dépendre de l'oreille de Tony, vérifier via `volumedetect`/`ffprobe`.
- Consentement clonage voix : **standing** (voir mémoire `feedback_voice_clone_standing_consent`), ne pas redemander à chaque fois.
- Option : version **9:16** avec visuel néon + paroles animées (skill vidéo/hyperframes) pour poster.

## Pièges connus

- kie.ai « Cover » et « Upload-Cover » **ne gardent pas le timbre** (revoice IA) → pour la vraie voix de Tony, TOUJOURS le clone sunoapi.org (personaId).
- Les `streamAudioUrl` apparaissent avant la fin mais donnent souvent déjà le morceau complet — vérifier la durée avec ffprobe.
- Pas de séparateur IA local (pas de Demucs/python) → impossible d'extraire proprement la voix d'un fichier externe ; régénérer un instrumental « cover » à la place.

---
name: mon-style-musical
description: Reproduit le STYLE musical de Tony (Tony OuWa) — son flow, son tempo, son écriture créole/français — pour générer de nouveaux morceaux ou re-produire ses textes/chansons avec sa voix clonée. Maintient un CORPUS de ses chansons (paroles + style + tempo) qui grandit à chaque nouveau son ajouté. Utilise ce skill quand Tony dit : « reproduis mon style », « fais un son dans mon style », « ajoute cette chanson à mon corpus », « refais mon texte », « un morceau comme les miens », « complète mon style », ou envoie un de ses sons/acapellas à intégrer. Complémentaire de [[chanson-ma-voix]] (qui gère la génération voix clonée pure).
---

# Reproduire le style musical de Tony (Tony OuWa)

Objectif : capturer **le style, le tempo et l'écriture** de Tony à partir de ses propres sons, et générer de nouveaux morceaux (ou re-produire ses textes) **avec sa voix clonée**, fidèles à sa patte.

## Le corpus (`corpus/`)

Un fichier `.md` par chanson : titre, **vibe/style**, **tempo (BPM)**, **paroles** (brouillon à corriger), réf audio. Le corpus GRANDIT : à chaque son que Tony ajoute, créer/mettre à jour un fichier. Fichiers actuels : voir `corpus/`. Style global observé : **dancehall / ragga / trap / love 974**, voix **baryton** posée, créole réunionnais + français, ad-libs ("aouh", "a ou", "oui oui"), thèmes amour + vie + fierté péi.

### Ajouter une chanson au corpus
1. Tony envoie le son (ou une **acapella** — bien meilleure pour la transcription).
2. Héberger (Blotato `blotato_create_presigned_upload_url` + PUT) → URL publique.
3. **Mesurer le tempo** si possible + noter la vibe.
4. **Paroles :**
   - Acapella / voix seule → transcrire via `blotato_create_source` (sourceType audio).
   - **Morceau produit (voix+musique) → la transcription auto ÉCHOUE souvent** (la musique masque la voix, l'outil refuse). Dans ce cas, demander à Tony de **coller les paroles** ou d'envoyer l'acapella.
5. Écrire `corpus/<slug>.md` (vibe, BPM, paroles corrigées, réf audio). Marquer les paroles auto comme « brouillon à corriger ».

## Reproduire son style / ses textes (génération)

Deux leviers, combinables :

**A. Sa chanson comme référence audio (garde tempo + vibe)**
`POST https://api.sunoapi.org/api/v1/generate/upload-cover` avec :
- `uploadUrl` = un de ses sons (hébergé), `customMode:true`, `model:"V5_5"`,
- `personaId` = son voiceId (voir [[chanson-ma-voix]] / config), `personaModel:"voice_persona"` → **sa voix clonée**,
- `instrumental:false` + `prompt` = paroles (les siennes corrigées, ou nouvelles dans son style),
- `style` = descripteur distillé du corpus, `vocalGender:"m"`.
→ Reprend le tempo/l'ambiance du morceau réf, mais chanté par sa voix clonée avec de nouvelles paroles.

**B. Génération pure dans son style**
`POST /api/v1/generate` `customMode:true`, `personaId`+`personaModel:"voice_persona"`, `prompt`=paroles, `style`=descripteur du corpus (ex. "dancehall lovers 974, baryton, créole réunionnais, ~92 BPM"), `title`, `model:"V5_5"`.

Poll : `GET /api/v1/generate/record-info?taskId=`. Clé : `/work/.sunoapi.env`. Crédits `GET /api/v1/generate/credit`.

## Reproduire un TEXTE précis
- Prendre les paroles du corpus (corrigées) → levier A ou B avec ces paroles exactes → sa voix clonée re-chante son texte, éventuellement dans un nouveau style/tempo.

## Notes
- ffmpeg/node hors PATH : `export PATH=/home/claude/tools/node/bin:/home/claude/tools/bin:$PATH`.
- Consentement clonage = standing [[feedback_voice_clone_standing_consent]].
- La voix clonée **re-performe** (ne copie pas la mélodie exacte) : pour garder SA mélodie/flow exact → utiliser sa vraie voix (mix, voir [[chanson-ma-voix]] §mix).
- Auto-transcription fiable seulement sur acapella/voix seule.
- Mix/master + écho dub + version 9:16 : recettes dans [[chanson-ma-voix]].

## Presets de style (`styles/`)

Chaque fichier `styles/*.md` = un **style prêt à l'emploi** (descripteur Suno + repères d'écriture). Pour générer dans un style : lire le preset, écrire des paroles ORIGINALES de Tony dans ce style, générer via [[chanson-ma-voix]] avec sa voix clonée.
Presets actuels : voir `styles/`. Ajouter un preset quand Tony montre une nouvelle référence de style (« fais-moi ce style »). **Ne jamais reproduire des paroles d'une chanson existante d'un autre artiste** — style/ambiance seulement, paroles originales.

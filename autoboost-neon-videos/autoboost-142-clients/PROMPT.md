# autoboost-142-clients — prompt & recette (pipeline v3, décor BUREAU)

Pas de génération d'image/vidéo IA dans cette vidéo : le pipeline v3 assemble des
micro-clips RÉELS de la banque avatar (décor BUREAU — studio, fond sombre, chemise
noire). Ce qui suit est donc la recette complète et reproductible — l'équivalent du
« prompt » pour ce pipeline. Sujet choisi : ligne 144 du Sheet `30 Vidéos`
(`Statut Tournage` = ⬜ À faire, `#` = 142), mot-clé CTA `CLIENTS`.

## 1. Script (voix off intégrale envoyée à avatar-webhook-v2, raccourci à 109 mots
pour tenir 30-35s — le script brut du Sheet faisait 130 mots)

```
N8N m'a rapporté trois clients de plus ce mois-ci, et un seul agent
d'automatisation en est responsable. L'agent surveille les formulaires remplis
sur mon site, qualifie chaque demande avec Claude en quelques secondes, et
répond immédiatement avec un créneau d'appel. Il relance automatiquement si la
personne ne répond pas sous quarante-huit heures. Avant, je répondais parfois
douze heures plus tard, et la moitié des prospects avaient déjà trouvé
quelqu'un d'autre. Maintenant la première réponse part en moins de deux
minutes, jour et nuit, week-end compris. C'est un seul workflow n8n, pas un
logiciel à mille euros par mois. Follow-moi et commente le mot CLIENTS, je
t'envoie le workflow complet gratuitement.
```

Appel exact (relayé via un workflow n8n ponctuel, `n7n.automatisationboost.com`
étant bloqué en direct depuis ce sandbox) : `POST
https://n7n.automatisationboost.com/webhook/avatar-webhook-v2`
```json
{
  "voixUrl": "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3",
  "avatarUrl": "https://assets.automatisationboost.com/video/avatar/auto%20avatar%20(online-video-cutter.com).mp4",
  "description": "<script ci-dessus>"
}
```
Réponse : `voiceUrl` (mp3 CloudFront, 32,66s brut) — `transcripts` vide (quota
Whisper OpenAI épuisé côté webhook). Timings mot-à-mot obtenus séparément via
**WaveSpeed Whisper** (`api.wavespeed.ai/api/v3/wavespeed-ai/openai-whisper`,
`language:"fr"`, `enable_timestamps:true`, relayé via n8n), transcription
parfaite à 122 tokens, décalage -0,326s appliqué pour compenser le silence de
tête coupé au post-traitement.

## 2. Post-traitement voix

```
silenceremove tête (start_threshold -45dB, peak) → silenceremove queue (areverse/areverse,
même seuil) → dynaudnorm=f=200:g=5 → mono 48kHz
```
Durée brute 32,66s → durée traitée 32,14s. Pas d'`atempo` : la durée tombait déjà
dans la cible 30-35s.

## 3. Références avatar — DÉCOR BUREAU (clips/, wardrobe chemise-noire-studio)

Trois fenêtres avatar, tirées de `_shared/avatar-bank/clips/`, même garde-robe :

| # | Rôle | Clip source | ss → ss+durée | Placement timeline | Zone lèvres actives (lips-map.json) |
|---|---|---|---|---|---|
| AV1 | Hook plein cadre | `A1_hook_frontal.mp4` | 0.67 → 4.27 | 0.00 → 3.60 | 0.67–4.58 |
| AV2 | Explication (fenêtre) | `B1_principe.mp4` | 0.08 → 3.71 | 3.60 → 7.23 | 0.08–4.88 |
| AV3 | CTA (fenêtre) | `C2_commente_motcle.mp4` | 0.08 → 4.83 | 24.81 → 29.56 | 0.08–4.83 |

Budget bureau total utilisé : 3.60 + 3.63 + 4.75 ≈ 11,98s sur les 13,5s
exploitables.

### Correction du défaut inverse (lèvres qui bougent pendant un silence voix)

Le `silencedetect` sur la voix traitée a révélé 3 silences > 0,2s tombant
**à l'intérieur** des fenêtres avatar (AV2 à 1,72s depuis son début ; AV3 dès
son ouverture et à nouveau à 3,36s). Les clips de la banque sont des prises
continues qui ne s'arrêtent pas aux pauses de la voix concaténée : sans
correction, la bouche aurait continué à bouger pendant ces silences — défaut
inverse déjà payé le 2026-08-28 (`autoboost-serie-2-avatar`).

**Correction** : image gelée (dernière frame avant le silence) tenue pendant
exactement la durée du silence, lecture reprise ensuite au même `ss` — jamais
de saut d'image, jamais de décalage de la piste voix.
- AV2 : lecture 0,08→1,80 (1,724s) → **gel 0,439s** → lecture 1,80→3,27 (1,470s)
- AV3 : **gel 0,405s** (silence en tout début de fenêtre) → lecture 0,08→3,03
  (2,954s) → **gel 0,278s** → lecture 3,03→4,15 (1,113s)

Vérifié à l'image (frames extraites aux deux bornes de chaque gel : identiques
pixel pour pixel) — aucune bouche en mouvement sous un silence restant.

## 4. Montage (2 passes)

- **Passe 1** — HyperFrames rend l'habillage (fond grille + glow néon, header
  AUTOBOOST + kicker « Agent de qualification n8n », fenêtre néon 648×1152 @
  (216,150), démo **canvas n8n animé** à 4 nœuds (Formulaire reçu → Qualifié
  par Claude → Réponse + créneau → Relance automatique, fils jaune/violet qui
  se tirent au rythme de la voix), statcard « AVANT — 12h+ de délai », punch
  « MAINTENANT : < 2 MIN », pilule CTA jaune pulsante, captions mot-à-mot 40px)
  avec la zone avatar vide. `public/index.html`.
- **Passe 2** — ffmpeg overlay les 3 clips ci-dessus (plein cadre 1080×1920
  pour AV1, 642×1146 @ (219,153) pour AV2/AV3, avec gel d'image aux silences
  ci-dessus) + mixage audio final (voix + BGM
  `journal-digital-clouds-128.mp3` duckée en sidechain, volume 0.30,
  fade-in 1,2s).

## 5. Réglages

- Format 1080×1920, 30 fps, h264 (crf18) + aac 192k
- Durée finale : 32,17s
- Cercle néon jaune (repris de la v2) : bordure pulsante 3px `rgba(255,230,0,.6)`
  autour de la fenêtre avatar réelle (AV1/AV2/AV3), pas de détourage
- CTA : commente le mot **CLIENTS**
- Musique : `_shared/bgm/journal-digital-clouds-128.mp3`

# autoboost-72-desamorce — prompt & recette (pipeline v3, décor VOITURE)

Pas de génération d'image/vidéo IA dans cette vidéo : le pipeline v3 assemble des
micro-clips RÉELS de la banque avatar. Ce qui suit est donc la recette complète
et reproductible — l'équivalent du « prompt » pour ce pipeline.

## 1. Script (voix off intégrale envoyée à avatar-webhook-v2)

```
Ethan Hunt a une mission impossible toutes les cinq minutes dans le film. Moi
j'avais un client difficile toutes les semaines, et à chaque fois la même
scène : un message énervé à vingt-deux heures, et moi qui découvre ça le
lendemain matin, furieux d'avoir raté la fenêtre de réponse. Avant, résultat,
trois relances manuelles et un client qui doute de moi. Maintenant, un agent
IA lit le message dès qu'il arrive, répond avec le bon ton en moins de deux
minutes, et me prévient seulement si la situation dépasse ce qu'il peut gérer
seul. Le client ne voit jamais l'attente, moi je dors tranquille et je garde
le contrat. Follow pour la suite, lien en bio — et si tu veux voir comment j'ai
construit cet agent, commente le mot DESAMORCE.
```

Appel exact : `POST https://n7n.automatisationboost.com/webhook/avatar-webhook-v2`
```json
{
  "voixUrl": "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3",
  "avatarUrl": "https://assets.automatisationboost.com/video/avatar/auto%20avatar%20(online-video-cutter.com).mp4",
  "description": "<script ci-dessus>"
}
```
Réponse : `voiceUrl` (mp3 CloudFront) — `transcripts` vide (Whisper OpenAI du
webhook à court de crédit, note déjà connue). Timings de scène/captions
reconstruits par détection de silence sur la voix traitée (`silencedetect`,
`-map 0:a`, seuil −28dB), pas par transcription mot-à-mot.

## 2. Post-traitement voix (recette verrouillée)

```
silenceremove (tête+queue, -45dB, peak) → atempo=1.12 → dynaudnorm=f=200:g=5 → mono 48kHz
```
Durée brute 35,38 s → durée traitée 31,01 s.

## 3. Références avatar — DÉCOR VOITURE (clips-new/, wardrobe chemise-noir-jaune)

Aucune image de référence à substituer : ce sont déjà des prises réelles de
Tony (pas de génération, pas d'avatar à remplacer). Cinq fenêtres avatar,
toutes tirées de `_shared/avatar-bank/clips-new/`, toutes dans la même
garde-robe (jamais mélangée avec le set bureau) :

| # | Rôle | Clip source | ss → ss+durée | Placement timeline | Zone lèvres actives utilisée |
|---|---|---|---|---|---|
| AV1 | Hook plein cadre | `D1_hook_frontal.mp4` | 0.54 → 3.41 | 0.00 → 2.87 | 0.54–4.63 |
| AV2 | Pain / frustration | `D4_relance_barbe.mp4` | 1.00 → 4.50 | 8.00 → 11.50 | 0.54–9.67 |
| AV3 | Canvas « Maintenant » | `D2_insistance_doigts.mp4` | 5.04 → 8.04 | 17.50 → 20.50 | 5.04–9.75 |
| AV4 | Après | `D3_cta_lunettes.mp4` | 0.50 → 3.00 | 23.00 → 25.50 | 0.04–9.75 |
| AV5 | CTA | `D3_cta_lunettes.mp4` | 3.50 → 8.20 | 26.30 → 31.00 | 0.04–9.75 |

Vérifié par `check_lips_rule.mjs` (variante locale, voix seule) : **PASS — 0
plan en violation** sur les 5.

## 4. Montage (2 passes)

- **Passe 1** — HyperFrames rend l'habillage (fond néon, header AUTOBOOST,
  fenêtre néon 648×1152 @ (216,150), démo canvas n8n, cartons avant/après,
  CTA, captions sous la fenêtre) avec la zone avatar vide. `public/index.html`.
- **Passe 2** — ffmpeg overlay les 5 clips ci-dessus (plein cadre pour AV1,
  642×1146 @ (219,153) pour AV2-5) + mixage audio final (voix + BGM
  `valse-des-fleurs-maison-tutti.mp3` duckée en sidechain + 5 SFX).

## 5. Réglages

- Format 1080×1920, 30 fps, h264 (crf18) + aac 192k
- Durée finale : 31,03 s
- CTA : commente le mot **DESAMORCE**

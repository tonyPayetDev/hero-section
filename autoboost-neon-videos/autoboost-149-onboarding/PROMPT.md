# autoboost-149-onboarding — prompt & recette (pipeline v3, décor BUREAU)

Pas de génération d'image/vidéo IA : le pipeline v3 assemble des micro-clips RÉELS
de la banque avatar (décor BUREAU — studio, fond sombre, chemise noire). Sujet :
ligne 149 du Sheet `30 Videos` (`Statut Tournage` = ⬜ À faire), mot-clé CTA
`ONBOARDING`.

## 1. Script (voix off envoyée à avatar-webhook-v2, raccourci à 114 mots pour
tenir 30-35s — le script brut du Sheet faisait 137 mots)

```
Claude Code m'a fait économiser trois cent cinquante euros par mois sur
l'onboarding de mes nouveaux clients. Avant, je perdais une demi-journée à
chaque signature : contrat, accès aux outils, mail de bienvenue, premier
rendez-vous. Je payais même une coordination freelance pour ne rien oublier.
Maintenant, un workflow n8n piloté par Claude Code déclenche tout
automatiquement dès que le devis est signé : contrat généré, accès créés,
mail personnalisé, rendez-vous calé, en moins de cinq minutes. Zéro oubli,
zéro coordination à payer, un client qui démarre avec une impression beaucoup
plus professionnelle. Si tu factures encore des clients sans process
d'onboarding clair, follow-moi et commente le mot ONBOARDING, je t'envoie le
workflow complet gratuitement.
```

Appel exact : `POST https://n7n.automatisationboost.com/webhook/avatar-webhook-v2`
```json
{
  "voixUrl": "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3",
  "avatarUrl": "https://assets.automatisationboost.com/video/avatar/auto%20avatar%20(online-video-cutter.com).mp4",
  "description": "<script ci-dessus>"
}
```
Réponse : `voiceUrl` (mp3 CloudFront, 37,61s brut) — `transcripts` vide (quota
Whisper OpenAI épuisé côté webhook, piège déjà documenté). `n7n.automatisationboost.com`
et le CloudFront de sortie sont bloqués en direct par le proxy réseau de cette
session : les deux appels (génération + téléchargement) ont été relayés par
des workflows n8n ponctuels (`[Oneoff] Gen Voice - Autoboost 149 Onboarding`,
`[Oneoff] Download Voice MP3 - Autoboost 149`), le MP3 récupéré en base64 via
`get_execution(includeData:true)` puis décodé localement.

## 2. Post-traitement voix

```
silenceremove tête (start_threshold -45dB, peak) → silenceremove queue (même
seuil, via areverse/areverse) → atempo=1.12 → dynaudnorm=f=200:g=5 → mono 48kHz
```
Durée brute 37,61s → durée traitée 33,05s (cible 30-35s atteinte).

## 3. Références avatar — DÉCOR BUREAU (clips/, wardrobe chemise-noire-studio)

Sujet technique/démonstration (automatisation n8n + Claude Code) → décor
BUREAU, jamais voiture. 5 fenêtres avatar, toutes tirées de
`_shared/avatar-bank/clips/`, mêmes garde-robe :

| # | Rôle | Clip source | ss → ss+durée | Placement timeline | Zone lèvres actives (lips-map.json) |
|---|---|---|---|---|---|
| AV1  | Hook           | `A1_hook_frontal.mp4`    | 0.67 → 4.47 | 0.00 → 3.80  | 0.67–4.58 |
| AV2a | Explication 1  | `B1_principe.mp4`        | 0.08 → 1.68 | 16.04 → 17.64 | 0.08–4.88 |
| AV2b | Explication 2  | `B1_principe.mp4`        | 1.68 → 4.38 | 18.20 → 20.90 | 0.08–4.88 |
| AV3a | CTA 1          | `C2_commente_motcle.mp4` | 0.08 → 0.98 | 28.30 → 29.20 | 0.08–4.83 |
| AV3b | CTA 2          | `C2_commente_motcle.mp4` | 0.98 → 3.98 | 29.75 → 32.75 | 0.08–4.83 |

Budget bureau total utilisé : 3.80 + 1.60 + 2.70 + 0.90 + 3.00 = **13,00s**
sur les 13,5s exploitables. AV2 et AV3 sont scindés en deux parce que des
pauses réelles de la voix (silencedetect −30dB/0.15s : 17,75→18,13s et
29,35→29,66s) traversaient la fenêtre d'un seul tenant — en rester un seul
plan aurait reproduit le défaut inverse documenté dans le skill (« la bouche
parle pendant le silence »). Chaque demi-plan s'arrête avant la pause réelle
et reprend juste après.

Vérifié par `work/check_lips.mjs` (adapté de `check_lips_rule.mjs` — chemins
`/home/claude/...` de l'original inexistants dans cet environnement — piste
voix seule `public/assets/voice.mp3`, enveloppe RMS lissée ~12 fenêtres/s,
violation = run consécutif > 6 frames) : **PASS — aucun plan en violation**
(zone containment + voix sous avatar), voir `work/order.json`.

## 4. Montage (1 passe, HyperFrames gère les `<video>` nativement dans cette
version du CLI — confirmé par les rendus récents autoboost-140/141/143)

- Fond + habillage charte (grille/radial sombre selon scène), header kicker +
  titre, 7 scènes calées sur les silences réels de la voix (0 / 4.59 / 7.02 /
  13.20 / 18.20 / 22.78 / 27.30s), carte checklist "avant" (4 items qui
  popent sur les micro-pauses d'énumération réelles), flow n8n animé (4
  nœuds "Contrat généré → Accès créés → Mail personnalisé → RDV calé" qui
  popent au rythme de la voix), jauge de résultat "−95% temps par client",
  CTA pilule jaune `ONBOARDING`.
- Avatar : 5 `<video>` séparés superposés dans `#avatar-frame` (cercle néon
  jaune 560×560, bordure pulsante + anneau orbital), chacun opacity 0 par
  défaut, fade in/out GSAP exactement sur sa fenêtre (`WINDOWS` dans le
  script). Le cadre lui-même (anneau + orbite) ne s'affiche que sur l'union
  des 5 fenêtres — bug corrigé en cours de build (l'anneau restait visible
  pendant la scène "résultat" sans aucun avatar affiché : l'animation de
  pulse touchait l'opacité indépendamment du planning des fenêtres).
- Captions mot-à-mot (30px, 2 couleurs seulement — jaune `hot` / violet
  `vhot`, pas de 3e teinte orange, charte oblige), timings reconstruits par
  pondération longueur de mot + bonus ponctuation sur les 7 segments
  délimités par les silences réels (même méthode que autoboost-140,
  documentée dans `veille-to-video/SKILL.md`).

## 5. Réglages

- Format 1080×1920, 30 fps, h264 (crf par défaut `looks`) + aac
- Durée finale rendue : **33,07s** (cible 30-35s)
- Palette strictement `_shared/CHARTE.md` : `#eab308` jaune, `#8b5cf6` violet,
  `#7c3aed` violet profond, fond `#0a0a0f`, surface `#111117`. **Aucune**
  valeur de l'ancienne palette morte (`#FFE600`/`#A855F7`/`#FF8A3D`) —
  autoboost-141 (16/10) utilisait encore ces valeurs mortes, corrigé ici.
  Aucun vert nulle part (dots de carte recolorés en jaune/neutre).
- Musique : `_shared/bgm/journal-digital-clouds-128.mp3` (même morceau que
  autoboost-140 « Claude Code vs Cursor », profil d'énergie déjà validé pour
  un sujet technique), volume 0.30 dans la comp (ducking géré par le mix
  HyperFrames natif, pas de passe ffmpeg séparée dans cette version)
- SFX : palette `_shared/sfx-palette/v2` (click, notify, confirm, glitch,
  zoom, whoosh, pop, impact, chime) sur les coupes de scène et les pops de
  cartes
- CTA : commente le mot **ONBOARDING**

## 6. Contrôle visuel avant livraison

Frames extraites à 1.5 / 5.5 / 6 / 8.5 / 11 / 12.5 / 14 / 16.5 / 19 / 20.5 /
21 / 23.5 / 25.5 / 26 / 28.5 / 30 / 31.5s : décor bureau correct sur toutes
les fenêtres avatar, bouche ouverte en plein milieu de chaque plan (pas de
plan figé pendant la voix), captions lisibles et jamais invisibles, palette
charte respectée, aucun vert, anneau néon correctement masqué hors fenêtre
avatar après correction.

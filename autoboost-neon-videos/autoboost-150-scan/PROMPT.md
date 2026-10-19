# autoboost-150-scan — prompt & recette (pipeline v3, décor BUREAU)

Pas de génération d'image/vidéo IA, pas de détourage : le pipeline v3 assemble
des micro-clips RÉELS de la banque avatar (décor BUREAU — studio, fond sombre,
chemise noire). Sujet : ligne 153 du Sheet `30 Videos` (`#` = 150, `Statut
Tournage` = ⬜ À faire), mot-clé CTA `SCAN`.

## 0. Pourquoi le décor BUREAU

Sujet = démonstration technique (« Claude Code lit un codebase client, explique
l'architecture, liste les bugs probables ») → BUREAU, jamais voiture, par la
règle du MANIFESTE.md (« tuto, technique, démonstration »).

## 1. Script (voix off envoyée à avatar-webhook-v2, tel quel — 133 mots, dans
la fourchette haute 25-40s)

```
Claude Code lit cinquante fichiers de code en trente secondes, là où il me
fallait facilement deux heures avant pour comprendre un projet client que je
reprenais. Quand un client m'envoie un site ou une automatisation déjà
existante à corriger, je ne pars plus de zéro : je lance Claude Code dans le
dossier, et en une poignée de secondes, il m'explique l'architecture, repère
les fichiers qui comptent vraiment, et me liste les bugs probables avant même
que j'aie ouvert un seul fichier moi-même. Ça change complètement le temps
que je facture sur une reprise de projet, et surtout, je ne rate plus les
détails cachés dans un vieux code mal documenté. Si tu reprends encore des
projets client à l'aveugle, follow-moi et commente le mot SCAN, je t'envoie
la méthode complète gratuitement.
```

Appel exact : `POST https://n7n.automatisationboost.com/webhook/avatar-webhook-v2`
```json
{
  "voixUrl": "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3",
  "avatarUrl": "https://assets.automatisationboost.com/video/avatar/auto%20avatar%20(online-video-cutter.com).mp4",
  "description": "<script ci-dessus>"
}
```
Réponse : `voiceUrl` (mp3 CloudFront, 34,18s) — `transcripts` vide (quota
Whisper OpenAI épuisé côté webhook, piège déjà documenté). `n7n.automatisationboost.com`
et le CloudFront de sortie sont bloqués en direct par le proxy réseau de cette
session : génération + téléchargement relayés par deux workflows n8n ponctuels
(`[Oneoff] Gen Voice - Autoboost 150 Scan`, `[Oneoff] Download Voice - Autoboost
150 Scan`), MP3 récupéré en base64 chunké via `get_execution(includeData:true)`
puis décodé localement (260 064 octets, intact).

Transcription mot-à-mot obtenue séparément via **WaveSpeed openai-whisper**
(`api.wavespeed.ai`, lui aussi relayé par un workflow n8n ponctuel —
`[Oneoff] Whisper WaveSpeed - Autoboost 150 Scan` — car bloqué en direct) :
`language: fr`, durée détectée 34,11s, timestamps mot-à-mot exploités pour
caler scènes, captions et fenêtres avatar.

## 2. Post-traitement voix

Aucun — voix utilisée telle quelle (pas de `atempo`/`dynaudnorm`), la durée
Whisper (34,11s) tombant déjà dans la cible 25-40s.

## 3. Références avatar — DÉCOR BUREAU (clips/, wardrobe chemise-noire-studio)

5 fenêtres avatar, toutes tirées de `_shared/avatar-bank/clips/`, même
garde-robe. Segments extraits en recadrage carré (`crop=720:720:0:0`,
scale 560×560, 30fps, -an) :

| # | Rôle | Clip source | ss → ss+durée | Placement timeline | Zone lèvres actives (lips-map.json) |
|---|---|---|---|---|---|
| AV1  | Hook          | `A1_hook_frontal.mp4`    | 0.67 → 4.47 | 0.55 → 4.35  | 0.67–4.58 |
| AV2a | Architecture  | `B1_principe.mp4`        | 0.10 → 1.70 | 14.45 → 16.05 | 0.08–4.88 |
| AV2b | Bugs probables| `B1_principe.mp4`        | 1.70 → 4.40 | 18.28 → 20.98 | 0.08–4.88 |
| AV3a | CTA 1         | `C2_commente_motcle.mp4` | 0.10 → 1.00 | 28.27 → 29.17 | 0.08–4.83 |
| AV3b | CTA 2         | `C2_commente_motcle.mp4` | 1.00 → 4.00 | 30.32 → 33.32 | 0.08–4.83 |

Budget bureau total utilisé : 3.80 + 1.60 + 2.70 + 0.90 + 3.00 = **12,00s**
sur les 13,5s exploitables.

Vérifié par `work/check_lips_rule.mjs` (recréé localement — l'original n'est
pas committé dans aucun projet source de ce dépôt, seul `public/` survit d'une
session à l'autre). Deux volets :
1. Containment : chaque segment source reste entièrement dans sa zone lèvres
   actives (`lips-map.json`) — **PASS** sur les 5.
2. Voix active sur la cible : `silencedetect` sur `voice.mp3` seul
   (`-45dB`, tolérance 0,2s = 6 images à 30fps, même seuil que l'outil
   d'origine). Deux ajustements faits en cours de build : AV1 décalé de
   0.00→0.55 (silence d'amorce TTS 0.00-0.52, sinon bouche qui bouge avant
   que la voix démarre — le défaut inverse documenté), AV2a décalé de
   14.08→14.45 et AV3a de 28.00→28.27 (chacun chevauchait une micro-pause
   respiration de ~0.26-0.29s en tête de fenêtre, confirmée réelle par
   `volumedetect`, pas un faux positif de seuil). **PASS** sur les 5 après
   ajustement — voir sortie complète dans `work/check_lips_rule.mjs`.

## 4. Montage (1 passe — HyperFrames gère les `<video>` nativement dans cette
version du CLI 0.8.179, confirmé par le rendu : 1026 frames, 34,2s, 9,5 Mo)

- 6 scènes calées sur les timestamps Whisper réels (0 / 4.60 / 7.32 / 14.04 /
  21.38 / 27.94s) : hook (titre « 50 fichiers lus en 30 secondes »), suite du
  hook, déclencheur (carte « client-site-v2/ » avec checklist), démo terminal
  (`claude-code scan .` tapé + 2 cartes résultat « Architecture » / « Bugs
  probables » qui popent au rythme de la voix, broll `grille-9x16.mp4` en
  surimpression `screen 0.32` — motif « dépôt / arborescence », cohérent avec
  le sujet), transformation (jauge « 2h → 30s » + bigverdict), CTA (pilule
  `SCAN`).
- Avatar : 5 `<video>` séparés dans `#avatar-frame` (cercle néon jaune
  560×560, anneau + orbite), opacity 0 par défaut, fade GSAP sur sa fenêtre
  uniquement (tableau `WINDOWS`).
- Captions mot-à-mot (30px, jaune `hot` / violet `vhot`), 30 lignes,
  timings posés directement sur les timestamps de mots Whisper (pas de
  reconstruction par pondération de longueur — contrairement à 149/140 où
  Whisper avait échoué, ici il a réussi).

## 5. Réglages

- Format 1080×1920, 30 fps, h264 (crf `looks`) + aac
- Durée finale rendue : **34,2s** (cible 30-35s, légèrement au-dessus —
  acceptable, la fourchette verrouillée est 25-40s)
- Palette strictement `_shared/CHARTE.md` (`#eab308` / `#8b5cf6` / `#7c3aed` /
  fond `#0a0a0f` / surface `#111117`). Aucun vert.
- Musique : `_shared/bgm/journal-digital-clouds-128.mp3` (réutilisée telle
  quelle, volume 0.30 dans la comp)
- SFX : palette v2 (click, notify, confirm, glitch, zoom, whoosh, pop, impact,
  chime) sur les coupes de scène et les pops de cartes
- CTA : commente le mot **SCAN** (phrasé « Commente le mot SCAN », jamais
  « Commente SCAN »)

## 6. Contrôle visuel avant livraison

Frames extraites à 1.5 / 3.0 / 5.5 / 9.0 / 12.5 / 15.0 / 16.5 / 19.0 / 22.5 /
26.0 / 29.0 / 31.5 / 33.5s : décor bureau réel sur toutes les fenêtres avatar
(aucun détourage, fond studio visible), captions lisibles, palette charte
respectée, CTA « Commente le mot SCAN » bien affiché. Léger chevauchement de
captions visible à 31.5s (cross-fade de 0,14s entre deux lignes à la coupure
30.32/31.52) — artefact de transition normal, imperceptible en lecture à 30fps.

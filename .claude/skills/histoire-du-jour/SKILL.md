---
name: histoire-du-jour
description: "« Histoire du jour » — vidéo enfant 9:16 (5-7 ans) qui apprend une lettre de l'alphabet avec Milo le petit singe : 5 scènes (lettre, quête, 3 mots, mini-jeu, récompense), voix française, lipsync deux états, ~35 s. Utilise ce skill dès que Tony dit « histoire du jour », « nouvelle lettre », « lettre B », « fais l'épisode de la lettre X », « vidéo alphabet », ou dépose une planche d'assets d'une nouvelle lettre."
---

# Histoire du jour

Moteur réutilisable : `histoire-du-jour/` (lire `histoire-du-jour/README.md`).
Agent dédié : `.claude/agents/histoire-du-jour.md` — **le lancer pour toute nouvelle lettre**.

## Ce que fait le moteur
- Un épisode = des données (`histoire-du-jour/episodes/<LETTRE>/config/*.json`) + une planche d'assets.
- `python3 histoire-du-jour/tools/build.py <LETTRE>` : découpe la planche, voix Kokoro (gratuite, locale),
  timings Whisper, mixage (voix -16 LUFS, musique -30 LUFS), composition HyperFrames, lint, snapshots, rendu MP4.
- Sortie : `histoire-du-jour/episodes/<LETTRE>/output/histoire_du_jour_<LETTRE>.mp4`.
- Référence : la lettre **M** (`episodes/M/`), déjà rendue.

## Nouvelle lettre en 3 temps
1. **Données** — l'agent choisit l'objet de quête, 3 mots qui commencent par le SON de la lettre
   (attention : C/G durs, H muet, QU, X, Y, W, voyelles nasales), un mini-jeu avec 2 intrus, le récap,
   et écrit la narration des 5 scènes.
2. **Planche** — l'agent écrit `episodes/<LETTRE>/docs/SHEET_PROMPT.md`. Tony le colle dans ChatGPT / Higgsfield
   en joignant la planche M comme référence, puis dépose l'image dans
   `episodes/<LETTRE>/assets/source/assets_master_sheet.png`. (Aucun crédit payant sans l'accord de Tony.)
3. **Vidéo** — l'agent découpe, vérifie les snapshots, rend le MP4 et donne le chemin.

Milo vient de la bibliothèque `histoire-du-jour/heroes/milo/` (identique d'une lettre à l'autre) ;
seule la pose « Milo tient l'objet de quête » est prise sur la nouvelle planche.

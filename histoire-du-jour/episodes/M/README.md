# Histoire du jour — Lettre M — Hyperframe Pack

Pack de production pour transformer l'épisode « Lettre M » en vidéo verticale animée 9:16.

## Objectif
Créer une vidéo enfant de 25–35 s, 1080×1920, avec 5 scènes, narration française, animation douce et lipsync simple de Milo.

## Important sur les assets
`assets/source/assets_master_sheet.png` est la planche source générée. Elle contient les références visuelles des décors, poses, objets, effets et branding. Pour une production finale, recréer/exporter chaque élément indiqué dans `config/assets.json` en PNG transparent individuel (personnages/props/FX) et chaque décor en 1080×1920. Ne pas considérer le damier visible de la planche comme une vraie transparence.

## Règles Milo / lipsync
Pour chaque pose parlante, fournir deux fichiers parfaitement alignés : `*_closed.png` et `*_open.png`. Même cadrage, même corps, mêmes yeux, même position ; seule la bouche change. Sur le phonème /m/ (« mmm »), privilégier la bouche fermée.

## Fichiers clés
- `config/project.json` : format et paramètres globaux
- `config/scenes.json` : timeline des 5 scènes
- `config/assets.json` : manifeste des assets attendus
- `config/lipsync.json` : règles de bouche
- `docs/CLAUDE_PROMPT.md` : prompt prêt à coller à Claude
- `docs/STORYBOARD.md` : storyboard humain
- `audio/narration.txt` : texte voix-off

## Sortie attendue
`output/histoire_du_jour_M.mp4`, H.264, 1080×1920, 30 fps.

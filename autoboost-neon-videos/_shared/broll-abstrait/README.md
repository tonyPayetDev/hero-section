# Banque de fonds animés — 10 motifs réutilisables

Charte : jaune `#eab308`, violet `#8b5cf6`, fond `#0a0a0f`. **Aucun vert.**
Boucle parfaite de 8 s à 30 fps — `draw(0) == draw(1)`, donc tout est en
`sin`/`cos` de `2π·p` ou en modulo sur `p`, jamais en compteur qui avance.

## Les dix motifs, et quand s'en servir

| # | Motif | Ce qu'il dit | À utiliser sur |
|---|---|---|---|
| 01 | **reseau** | des points qui respirent et se relient | graphe, structure, « tout est lié » |
| 02 | **flux** | des traits qui traversent l'écran | tokens, données, coût qui défile |
| 03 | **grille** | grille en perspective qui avance | dépôt, échelle, arborescence |
| 04 | **planetes** | orbites autour d'un soleil, lunes sur les violettes | écosystème, « tout tourne autour de » |
| 05 | **workflow** | nœuds reliés, liaisons qui se tracent, jeton qui circule | n8n, automatisation, chaîne d'étapes |
| 06 | **constellation** | des points se rassemblent en figure puis se dispersent | les pièces s'assemblent, révélation |
| 07 | **onde** | anneaux concentriques qui se propagent | portée, diffusion, viralité |
| 08 | **circuit** | pistes orthogonales qui s'allument par tronçon | infrastructure, « sous le capot » |
| 09 | **spirale** | spirale de points en rotation | montée en puissance, accumulation |
| 10 | **tunnel** | cadres qui foncent vers le spectateur | avancée, entrée, transition de fin |

## Fichiers

- `reseau.mp4`, `flux.mp4`, `grille.mp4` — 1920×1080
- `planetes-9x16.mp4`, `workflow-9x16.mp4`, `constellation-9x16.mp4`,
  `onde-9x16.mp4`, `circuit-9x16.mp4`, `spirale-9x16.mp4`, `tunnel-9x16.mp4` — 1080×1920

## Regénérer

```sh
export PATH=/home/claude/tools/node/bin:$PATH
# paysage
node gen_broll.mjs
# vertical
BW=1080 BH=1920 BSUF=-9x16 node gen_broll2.mjs
```

Puis assembler chaque dossier de frames :

```sh
ffmpeg -framerate 30 -i <motif>/f%04d.png -c:v libx264 -crf 20 -pix_fmt yuv420p <motif>.mp4
```

## Comment les poser dans une vidéo

**Derrière un plan opaque**, en mode `screen` : l'animation transparaît dans les
noirs sans jamais toucher au texte clair.

```
[plan][broll]blend=all_mode=screen:all_opacity=0.55
```

Monter l'intensité avant le mélange si le motif se perd :
`eq=brightness=0.04:saturation=1.35`.

**En fond direct**, quand le plan est du texte sur transparent : poser le b-roll
en base et le texte par-dessus, sans mélange.

## Règles apprises

- **Un motif par section**, jamais deux dans le même plan : ils se battent.
- **Le motif doit dire quelque chose.** `workflow` sur un passage qui parle de
  chaîne d'étapes, `onde` sur un passage qui parle de portée. Un motif choisi
  au hasard se voit autant qu'une image de stock.
- **Opacité 0,5 à 0,6 maximum** sous du texte. Au-delà on lit le fond, plus le
  propos.
- Les frames intermédiaires sont conservées : c'est ce qui permet de changer la
  durée ou le format sans tout regénérer.

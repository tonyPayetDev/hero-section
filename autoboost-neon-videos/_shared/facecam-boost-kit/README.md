# FaceCam Boost kit

Composants réutilisables pour habiller une **vraie face cam** de Tony en motion
design HyperFrames, dans la charte AutomatisationBoost (`../CHARTE.md`).
Utilisé par le skill `/face-cam-boost`. Première vidéo construite avec :
`autoboost-74-claude-md-sous-agents/motion/` (v2).

| Fichier | Rôle |
|---|---|
| `kit.css` | le look : stickers, puce niveau, crochets, tubes néon, séparateur, courbe, recherche, pile, dock, typo élastique, bouton, plaque de captions |
| `kit.js` | les motions (`window.FB.*`), toutes déterministes, à poser sur la timeline GSAP unique |
| `kit.py` | le balisage côté générateur Python + `facecam_mode()` (cadrages de la face cam) |
| `gallery/` | composition de démonstration 12 s (3 pages) — `python3 gallery/gen.py` |
| `boards/` | les 3 planches figées : stickers, motions 1/2, motions 2/2 |

## Les 4 layouts (références de Tony)

`facecam_mode(box, focus, crop_h, radius)` renvoie le `transform` + `clip-path`
qui place la face cam dans une boîte du canvas 1080×1920. Tous les modes
s'interpolent entre eux (`FB.morph`) parce qu'ils ont tous la forme
`inset(... round R)`.

| Layout | Boîte | Quand |
|---|---|---|
| **1 · contenu en haut, avatar en bas** — cercle néon | `(220,1100,640,640)`, `radius=320` | explication, démo, tuto |
| **1 bis · rectangle empilé** | `(24,1000,1032,920)`, `radius=34` | idem, plus de visage |
| **2 · split vertical** | `(24,420,500,1290)` + `.fb-divider` + `.fb-knob` | comparaison, avant / après |
| **3 · split horizontal** | rectangle empilé + carte stats en haut + sticker « ÇA MONTE » | chiffre, résultat |
| **4 · plein écran** | `(0,0,1080,1920)` | hook, punchline, CTA final |

## Les 10 stickers

`sticker(id, a, b, variant, icon, deco)` — variantes `gold` / `violet` / `red`
(rouge seulement pour ce qui est **faux ou lent**), décor `spark` / `bar` /
`swoosh`. Entrée : `FB.sticker(tl, "#id", tIn, tOut, rot)` — arrive surdimensionné
et penché, se pose sur son angle.

TROP LENT · DÉJÀ MIEUX · PLUS SIMPLE · GAIN TEMPS · NIVEAU MAX · ÇA MONTE ·
AUTOMATISE ÇA · PLUS CLAIR · BON SYSTÈME · ÇA PART — le texte est libre
(« ÇA BLOQUE » dans autoboost-74).

## Les 8 motions (CERËGA / SKOOL, repassées dans la charte)

| # | Motion | Helper |
|---|---|---|
| 1 | bouton qui s'enfonce puis s'ouvre en panneau | `FB.press` + fromTo du panneau |
| 2 | recherche tapée → résultats décalés de 0,13 s | `FB.type` + `FB.results` |
| 3 | courbe qui se dessine, aire, point, étiquette | `chart_svg()` + `FB.chart` |
| 4 | tuile de tableau de bord qui zoome plein cadre | `FB.tileZoom` |
| 5 | pile de cartes, celle du dessus s'envole | `FB.stackFly` |
| 6 | dock façon Mac, l'icône survolée grossit ×1,8 | `FB.dock` |
| 7 | typo élastique, onde gauche → droite | `elastic()` + `FB.elastic` |
| 8 | particules qui forment le logo puis se dispersent | `<canvas>` + `FB.particles` |

Leurs 5 règles restent vraies ici : timings en secondes, jamais linéaire,
palette verrouillée, une idée par animation, (la boucle parfaite ne s'applique
pas à une vidéo narrée).

## Règles du kit

- **Aucun chiffre inventé.** Les références affichent « +247 % » : les
  composants prennent les valeurs en paramètre, et ces valeurs doivent venir de
  ce qui est dit dans la vidéo.
- **Aucun vert** (coches or, pastilles de fenêtre rouge / or / violet).
- **Pas d'emoji** : toutes les icônes sont des SVG de `kit.ICON`.
- Les classes du kit sont préfixées `fb-` ; dans un projet, ne pas réutiliser
  des noms de classe génériques (`.qa`, `.qb`…) d'un écran à l'autre — un
  `box-shadow` global sur une boîte 1080×980 a donné un trait parasite dans
  autoboost-74.

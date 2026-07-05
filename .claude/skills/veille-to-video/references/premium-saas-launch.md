# Premium SaaS Launch — preset visuel (Autoboost Neon Video)

Utilisé quand la demande évoque : premium SaaS, style Apple/Linear/Arc/Vercel/Raycast, explainer automatisation, vrais schémas/icônes/dashboards/graphes, ou explainer produit haut de gamme.

**Override local obligatoire** : le jaune `#FFE600` remplace le bleu comme accent global de ce type de preset. Violet `#A855F7` pour tout ce qui est IA/transformation, orange `#FF8A3D` pour les CTA/actions. Fond noir mat, jamais blanc pur.

## Structure d'écran (split vertical)

```
┌──────────────────────────────┐
│  Zone d'explication (haut)   │  ~55–60% de la hauteur
│  - titre court FR (2-4 mots) │
│  - schéma / dashboard / icônes
│  - captions TikTok mot-à-mot │
├──────────────────────────────┤
│  Bande de sécurité captions  │  ~10% — rien d'autre ici
├──────────────────────────────┤
│  Avatar / setup (bas)        │  ~30-35% de la hauteur
└──────────────────────────────┘
```

- Ne jamais laisser une caption ou un texte de slide descendre dans la zone avatar/setup.
- Le schéma/dashboard vit uniquement dans la zone haute.

## Slide "flow d'automatisation" (le plus utilisé — n8n / agents)

Toujours un **schéma horizontal stable**, jamais diagonal :

```
[Gmail] --arrow--> [Agent IA] --arrow--> [n8n] --arrow--> [Base] --arrow--> [Dashboard]
```

- Chaque nœud = carte icône (fond `#111111` légèrement plus clair que le fond, bord 1px `rgba(255,230,0,0.25)`, icône simple ligne blanche/jaune).
- Flèches : trait fin blanc/gris avec un **point pulsé animé** (glow jaune ou violet) qui voyage le long de la flèche pour suggérer le flux de données en temps réel — pas d'animation clignotante agressive.
- Petit panneau data/schéma en overlay discret (ex. mini JSON, mini table, mini graphe en barres) proche du dernier nœud (Dashboard), pour ancrer le "réel" plutôt qu'une icône abstraite.
- Espacement horizontal égal entre les 5 nœuds, alignés sur une seule ligne médiane — évite tout chevauchement à l'inspection HyperFrames.

## Dashboards / graphes

- Cartes UI avec vrais chiffres plausibles (%, compteurs, mini sparklines) plutôt que des blocs vides.
- Un seul accent chromatique par graphe (jaune OU violet OU orange), pas de dégradé multicolore façon confetti.
- Contours fins, coins arrondis modérés (8–12px), pas de skeuomorphisme.

## À éviter systématiquement

- Slides façon PowerPoint (titre + puces + rien d'autre).
- Cartes seules sans contexte (icône flottante sur fond noir sans schéma/flèche).
- Filtres noirs opaques posés sur du texte pour "assurer la lisibilité" — préférer un léger scrim `rgba(0,0,0,0.35)` maximum ou repositionner le texte.
- Double exposition, écrans statiques sans micro-mouvement (au moins un élément vivant par scène : pulse dot, compteur, curseur).
- Layouts diagonaux pour les flows — toujours horizontal ou vertical stable.

## Checklist rapide preset

- [ ] Accent global = jaune (pas de bleu dominant)
- [ ] Flow automatisation horizontal, 5 nœuds max, flèches + pulse dot
- [ ] Dashboard/graphe avec vrais chiffres, un seul accent par graphe
- [ ] Zone avatar/setup jamais envahie par schéma ou caption
- [ ] Au moins un élément animé vivant par scène

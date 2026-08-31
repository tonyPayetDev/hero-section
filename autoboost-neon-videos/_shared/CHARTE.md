# Charte vidéo AutomatisationBoost — source unique

> **Tout skill vidéo lit ce fichier au lieu de redéfinir la charte.**
> Avant ce fichier, sept skills portaient deux palettes concurrentes
> (`#FFE600`/`#A855F7` contre `#eab308`/`#8b5cf6`) et il fallait redire la
> direction artistique à chaque demande. C'est fini : la charte est ici, et
> nulle part ailleurs.

---

## 1. Palette — non négociable

| Rôle | Valeur | Usage |
|---|---|---|
| Jaune de marque | `#eab308` | accent principal, titres, chiffres qui comptent |
| Jaune clair | `#BEF264` | rehaut ponctuel, jamais un aplat |
| Violet | `#8b5cf6` | second accent : numéros, fonds de logs, liaisons |
| Violet profond | `#7c3aed` | violet sur fond clair (contraste) |
| Fond | `#0a0a0f` | le noir de référence |
| Surface | `#111117` | panneaux, cartes, terminaux |
| Filet | `#232330` | bordures d'un pixel |
| Texte | `#EDEDED` | corps |
| Texte sourd | `#8A8A8A` | légendes |
| Erreur | `#ff6b6b` | **couleur de sens, pas de charte** — garder telle quelle |

**Autorité** : ces valeurs viennent de `automationboost/assets/css/style.css`
(`--gold`, `--violet`, `--bg-dark`, `--bg-card`, `--border`), relevées le
2026-08-20. Si le site change, ce fichier change ; pas l'inverse.

### Valeurs mortes — ne jamais réintroduire

`#FFE600` · `#A855F7` · `#FF8A3D` — ancienne palette « néon Autoboost ».
`#a3e635` (vert acide) — vient des **pages ressources**, pas de la charte.
**Aucun vert nulle part**, y compris les pastilles de fenêtre dans les
captures terminal (`#28C840`) : c'est là qu'il se cache et Tony le voit.

---

## 2. Typographie

- Affichage : Sora (site) ou DejaVu Sans en rendu local — gras 800, interlettrage serré
- Corps : même famille, graisse normale
- Donnée, libellés, références : capitales espacées `.14em`, `font-variant-numeric: tabular-nums`
- **Pas d'emoji comme icône** : aucune police emoji dans le sandbox, ils sortent en carrés

---

## 3. Fonds animés — piocher avant de créer

**Dix motifs existent déjà dans `_shared/broll-abstrait/`. Les regarder AVANT
d'en dessiner un nouveau.** Le détail complet est dans le README de ce dossier.

| Motif | Ce qu'il dit |
|---|---|
| `reseau` | structure, « tout est lié » |
| `flux` | tokens, données, coût qui défile |
| `grille` | dépôt, échelle, arborescence |
| `planetes` | écosystème, « tout tourne autour de » |
| `workflow` | n8n, chaîne d'étapes, automatisation |
| `constellation` | les pièces s'assemblent, révélation |
| `onde` | portée, diffusion, viralité |
| `circuit` | infrastructure, « sous le capot » |
| `spirale` | montée en puissance, accumulation |
| `tunnel` | avancée, entrée, transition de fin |

Composition : `[plan][broll]blend=all_mode=screen:all_opacity=0.55`.
Un seul motif par section. **Le motif doit dire quelque chose** — choisi au
hasard, il se voit autant qu'une image de stock.

Un nouveau motif ne se crée que si aucun des dix ne dit ce qu'il faut dire.
Dans ce cas il rejoint la banque et ce tableau.

---

## 4. Avatar — deux décors, deux usages

**Lire `_shared/avatar-bank/MANIFESTE.md` avant de choisir un clip.**
La banque ne contient pas 24 clips : elle en contient **7 exploitables**, en
**deux tournages qui ne se mélangent jamais**.

| Set | Décor | Clips | Pour quoi |
|---|---|---|---|
| **BUREAU** | studio, fond sombre, chemise noire | A1, B1, C2 — 5,1 s | tuto, démonstration, technique |
| **VOITURE** | intérieur voiture, liseré jaune | D1, D2, D3, D4 — 10,1 s | humour, opinion, mindset, storytime |

**Un décor par vidéo, jamais les deux** — deux tenues et deux lumières dans le
même montage se voient immédiatement.
**Le décor doit correspondre au propos** : une histoire technique tournée dans
la voiture sonne faux. Erreur commise le 2026-08-20 sur le storytime.

L'avatar sur fond vert de `avatar-hq/` appartient à l'ancien pipeline et
demandait un détourage `geq`. Ne plus l'utiliser dans une nouvelle vidéo.

- Recadrage **carré depuis le haut** (`crop=720:720:0:0`), masque circulaire
- **Audio natif coupé**, voix clonée posée par-dessus — sinon Tony n'entend pas sa voix
- Deux plans maximum sur un format court : l'accroche et l'appel
- Poser hors de la zone de texte : coin bas, jamais au centre d'un tableau

---

## 5. Voix

- Webhook n8n `tts-gen`, champ **`text`** (pas `texte`), **`voixUrl` obligatoire**
- `voixUrl` : `https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3`
- Contrôle par la mesure : **F0 médian 114–133 Hz**. Vers 200 Hz c'est le repli OpenAI, à refaire
- Débit : `atempo=1.09` sur les formats rythmés, jamais sur un essai contemplatif
- Le webhook lâche par intermittence (502) : **quatre tentatives, et ne jamais garder un fichier < 1 Ko**

---

## 6. Musique

- Nappe **stable** : vérifier le profil d'énergie avant de choisir. Plus de 10 dB
  d'écart sur le morceau = une musique qui monte toute seule sous la voix
- `au-bord-des-etoiles` convient (−13 à −17 dB sur toute la durée)
- **Normaliser la voix d'abord, poser la musique dessous à niveau fixe.**
  Normaliser la somme remonte la musique avec la voix : c'est l'erreur qui rend
  une musique « trop forte » quoi qu'on baisse en amont
- Cible : plancher musical à environ −33 dB sous la parole

---

## 7. Le CTA

- **Un mot-clé annoncé doit avoir sa porte Blotato active AVANT le tournage.**
  Sinon les gens commentent et ne reçoivent rien
- Un seul mot, jamais deux : les variantes tapées ne déclenchent pas
- Vérifier la liste des portes existantes — plusieurs mots sont déjà pris
- Sur YouTube et LinkedIn, Blotato ne gère rien : réponse à la main ou lien en description

---

## 8. Rendu

- `FONTCONFIG_PATH` + chromelibs obligatoires, sinon le texte est invisible
- Vérifier la RAM avant un rendu long ; tuer les `ffmpeg` orphelins
- Monter **segment par segment puis concaténer** : un filtre géant qui échoue
  donne un fichier de 0 octet sans dire où
- `ffmpeg` consomme l'entrée standard : `-nostdin` dans toute boucle shell
- `amix` divise par le nombre d'entrées : `normalize=0` sinon le mix sort plus faible
- Séparateur d'options dans un filtre : `:` et non `,` — la virgule sépare les filtres
- **Regarder l'image avant de livrer.** Un rendu techniquement parfait peut
  masquer le chiffre le plus important derrière l'avatar

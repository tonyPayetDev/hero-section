---
name: essai-long-ego
description: Produit un essai vidéo long (8-12 min) en 16:9 dans la grammaire d'EGO — voix off posée, escalade concret → existentiel, visuel procédural généré par code, atterrissage dans le blanc. À utiliser quand Tony demande une vidéo longue de réflexion, un format YouTube, ou « refais un truc comme après l'IA ».
---

# Essai long — format EGO, produit par VideoBoost

Format **long** (8 à 12 min), **16:9**, destiné à YouTube. Voix off posée, aucun cut nerveux,
visuel entièrement **généré par code** et non par des images achetées ou prompt-ées une par une.

Production de référence : **« Mais après l'IA, il va vraiment se passer quoi ? »** —
9 min 12, 278 plans, script → film livré **dans la même journée** (narration écrite à 14:14,
rendu final à 21:54). Route : `/essai-apres-ia-v3/`.

Ce chiffre est l'argument commercial du format, et il est vérifiable : c'est l'horodatage
des fichiers, pas une estimation. Ne jamais l'arrondir vers le bas pour faire joli.

---

## 0. Ce qui distingue ce format des autres skills vidéo

| | Autoboost / veille-to-video | **Essai long EGO** |
|---|---|---|
| Durée | 18-25 s | **8-12 min** |
| Format | 9:16 | **16:9** |
| Montage | coupe au demi-temps | coupe au **bloc de voix** (20-40 s) |
| Visuel | clips générés (Seedance, Kie) | **procédural, en code** |
| Son | SFX à 0,17-0,26 | **SFX à 0,05-0,09** |
| Sortie | TikTok / Reels | **YouTube**, les autres réseaux renvoient dessus |

⚠️ **Le piège numéro un** : reprendre la palette SFX d'Autoboost telle quelle. Elle est
réglée pour accrocher en 20 secondes. Sur 9 minutes, elle transforme la contemplation en
bande-annonce. Tout est **trois fois plus bas**.

---

## 1. La chaîne, dans l'ordre

```
narration.txt  (17 blocs, un par paragraphe)
   ↓ tts-clone.mjs / tts-eleven.mjs      la voix (clonée de Tony)
   ↓ audio.mjs                            marques.json = début/fin de chaque bloc
   ↓ frames2.mjs                          278 images, une toutes les 2 s
   ↓ emotions.mjs                         les mots d'émotion, en ASS
   ↓ sfx.sh                               la couche de sound design
   ↓ monter.sh                            assemblage : images → film
```

Tous les scripts sont dans `/work/essai-apres-ia/src/`. **Copier ce dossier** pour un
nouvel essai plutôt que de repartir de zéro.

### Le point qui porte tout

`marques.json` donne le **début et la fin réels de chaque bloc de voix**. Le montage se
rattache à ces marques, jamais à des secondes écrites à la main. Sur le projet de
référence la voix a changé de durée deux fois — un montage calé en dur aurait été à
refaire intégralement à chaque fois.

---

## 2. Le visuel : trois natures de plan, pas une de plus

**La sphère** (`scene.html`) — l'objet récurrent, le fil du film.
**Les schémas** (`graphe.html`) — un par idée du script, animés par leur avancement.
**Le b-roll** — images libres passées en bichromie, cadre 1920 qui dérive dans une source
2400 pour que le plan bouge même quand rien ne bouge dedans.

### La sphère : ce qui a marché et ce qui n'a pas marché

Première version : trame plate remplie de bruit fractal. Refusée par Tony — « change
l'image de planète ». Le défaut n'était **pas la texture**, c'était l'absence de **volume** :
elle dessinait un disque en espérant qu'on y voie une boule.

Deuxième version, celle à reprendre : les points existent réellement sur une **sphère 3D**
(répartition en spirale de Fibonacci, pas en latitude/longitude — une grille régulière
entasse les points aux pôles) et sont projetés. Trois conséquences que le plat ne donne pas :

- elle **tourne** — une seule rotation lente sur toute la durée (`ang = T * 0.95`) ;
- elle a un **terminateur**, donc une source de lumière ;
- la densité se resserre d'elle-même vers le limbe, ce qui creuse le volume gratuitement.

⚠️ **La lumière doit être RASANTE.** Un premier essai la posait à `z = 0,73` : la composante
frontale éclairait toute la face visible et le terminateur n'existait pas à l'image.
Valeur qui marche : `L = [-0.86, -0.22, 0.26]`.

La face nuit vire au **violet**, avec un plancher d'opacité forcé. Sans ce plancher,
l'accent secondaire est mathématiquement présent et visuellement absent — le défaut mesuré
sur les Autoboost, où le violet pesait 0,00 % des pixels malgré la charte.

---

## 3. Les mots d'émotion — pas un sous-titrage

`emotions.mjs`. **Dix à douze moments sur 550 secondes**, pas davantage.

Neuf minutes de texte permanent transforment une vidéo qu'on regarde en article qu'on lit,
et la voix passe au second plan. Le texte n'apparaît que quand la phrase frappe.

**Le calage** : `marques.json` donne les bornes du bloc, pas la position du mot. On estime
l'instant par la **position en caractères** de la phrase dans son bloc. Approximation, mais
bornée : sur un bloc de 30 s, une erreur de 5 % du texte fait 1,5 s et le mot reste dans sa
phrase.

**Le motif des trois répétitions** : quand le script martèle un mot (« Pourquoi. Pourquoi.
Pourquoi. »), les afficher empilés, 1,15 s d'écart, chacun légèrement plus bas. D'un bloc,
on rate le martèlement — qui est l'effet même de la répétition.

⚠️ `MarginV` en ASS se compte **depuis le bas**. Partir de 76 et retrancher 46 par ligne
donne −16 au troisième : le mot sort du cadre. Valeurs qui tiennent : `232 - k * 54`.
Ce défaut est invisible en relisant le code et évident sur une image — **toujours extraire
une image du rendu avant de publier**.

---

## 4. Les formes pures

Un cercle qui se trace avec un point qui le mène, un triangle qui se construit sommet par
sommet. Elles ne représentent rien : c'est leur fonction. Après plusieurs minutes de
schémas qui démontrent, l'œil a besoin d'un plan qui ne demande rien.

**Quatre inserts de 10 s maximum**, soit ~7 % de la durée. Au-delà, la forme cesse d'être
une respiration et devient un motif.

**Toujours sur du b-roll, jamais sur un schéma** — remplacer une démonstration par une
décoration est une perte sèche.

---

## 5. Le son

`sfx.sh`. Palette : `/work/autoboost-neon-videos/_shared/sfx-palette/v1/assets/`.

| Rôle | Fichier | Volume |
|---|---|---|
| Entrée d'une forme pure | `sfx-click-soft` | **0,07** |
| Martèlement d'une répétition | `sfx-click` | **0,06** |
| Les phrases qui portent la chute | `sfx-chime-v2` | **0,08** |

Onze impacts sur 552 s. Un toutes les 50 secondes, aucun là où la voix porte seule.

⚠️ `amix` avec `normalize=1` (défaut) **baisse la voix** à chaque démarrage d'effet, ce qui
s'entend beaucoup plus que l'effet. Toujours `normalize=0:dropout_transition=0`.
Et `adelay=...:all=1`, sinon seul le canal gauche est décalé.

---

## 6. Le montage final

`monter.sh`. Deux étapes, et il faut savoir laquelle relancer :

1. **images → `fond.mp4`** : `-framerate 0.5` puis `minterpolate=mi_mode=blend`. Le fondu,
   pas l'estimation de mouvement — qui coûterait des heures et inventerait des artefacts
   sur du procédural. Plus un zoom lent de 1,00 à 1,09 : sans lui l'œil perçoit une suite
   d'images fixes ; avec, le fondu devient invisible.
2. **`fond.mp4` + ASS + audio → le film**. C'est l'étape lente (preset slow).

**Une correction de sous-titre ou de son ne demande QUE l'étape 2.** Relancer l'étape 1
pour ça, c'est doubler l'attente pour rien.

---

## 7. La publication

**YouTube reçoit le film. Les quatre autres réseaux renvoient dessus.**

Ce n'est pas un choix éditorial, c'est une contrainte : Instagram et TikTok plafonnent en
durée et sont verticaux. Un 16:9 de neuf minutes y échoue ou s'y effondre.

Donc : couper un **extrait vertical de 45 s** sur le passage le plus fort, recadré au
centre (la sphère, les schémas et le texte sont tous centrés — le 9:16 ne coupe que du
vide), et le publier sur IG / TikTok / Facebook / LinkedIn avec un renvoi vers YouTube.

Comptes Blotato : YouTube `45006` · Facebook `43538` (page `1288852254291983`) ·
Instagram `54617` (automatisationboost) · LinkedIn `25882` · TikTok `36488` (tonypayet4).

⚠️ **`isAiGenerated: true` sur TikTok** et `containsSyntheticMedia: true` sur YouTube : la
voix est clonée et l'image est générée. Le déclarer est la règle des plateformes, et c'est
aussi ce qui protège le compte.

### Ce qu'on dit, et ce qu'on ne dit pas

- **Citer EGO comme inspiration.** Le format lui doit sa grammaire, le dire est honnête et
  ça situe la vidéo pour ceux qui connaissent.
- **Donner le temps réel de production**, pas un chiffre gonflé vers le bas. « Dans la
  journée » est vérifiable ; « en dix minutes » ne l'est pas et se retourne au premier
  commentaire.
- Ne jamais publier sans accord explicite de Tony.

---

## 8. Vérifications avant publication

- [ ] Une **image extraite du rendu final** à chaque moment sous-titré — pas une relecture du code
- [ ] Les trois répétitions empilées **tiennent dans le cadre**
- [ ] La sphère **tourne** (comparer deux images éloignées) et son terminateur a bougé
- [ ] Le film **se vide vers le blanc** sur le dernier tiers
- [ ] Crête audio ≤ −1,0 dB (`astats` avec `-v info`)
- [ ] Le MP4 est **complet** : `ffprobe` doit rendre une durée. Avec `+faststart` l'index
      s'écrit à la fin — un fichier en cours d'écriture est illisible, pas tronqué, et une
      notification de tâche de fond ne prouve pas que ffmpeg a fini
- [ ] Vidéo sur **R2**, jamais dans le dépôt previsualisation

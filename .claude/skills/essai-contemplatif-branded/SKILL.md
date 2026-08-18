---
name: essai-contemplatif-branded
description: >
  Produit un essai vidéo contemplatif (style "video essay" minimaliste type EGO / Kurzgesagt
  sobre) qui part d'un objet banal et monte vers l'existentiel, puis se termine par un fondu
  au blanc. Livre DEUX choses : (1) le PROMPT UNIQUE à coller dans VideoBoost pour générer
  toute la vidéo sans montage manuel, et (2) la VOIX OFF en registre essayiste. Sert aussi de
  démo de puissance pour Automation Boost / VideoBoost ("le format le plus dur, un seul prompt").
  Utilise ce skill dès que Tony dit : "essai contemplatif", "vidéo dans le style EGO", "video
  essay", "vidéo lente/introspective", "mon pourquoi en vidéo", "vidéo manifeste", "vidéo qui
  finit en blanc", "vidéo philosophique", "prouve que VideoBoost peut faire ce style", "vidéo
  qui part d'un truc banal et monte vers l'existentiel", ou décrit une vidéo posée, voix off
  calme, escalade concret → abstrait → existentiel, fin melancolique/blanche. Déclenche aussi
  quand il partage une réf de video essay et veut la refaire en un prompt.
---

# Essai Contemplatif — Branded (VideoBoost / Automation Boost)

Format long ou moyen **posé, hypnotique, essayiste**. On part d'un **objet banal**, on
**escalade** vers l'abstrait puis l'existentiel, on **atterrit dans le blanc**. Zéro hype,
zéro cut nerveux. La force est dans la patience et la montée de sens.

**Double objectif :**
1. Produire la vidéo (script VO + prompt VideoBoost unique).
2. **Preuve de puissance** : montrer que VideoBoost tient ce style — le plus dur à produire —
   à partir d'**un seul prompt**, sans montage à la main. C'est un argument de vente Automation Boost.

**Réf modèle (la grammaire à copier) :** EGO — *"L'horreur existentielle de l'usine à trombones"*
(6,1M vues, oct. 2024). Part d'un jeu web débile (compteur de trombones) → monte vers l'alignement
IA / la superintelligence → finit dans le cosmos, seuls dans l'univers, à baisser les yeux vers
ce qu'on vient de créer. C'est CET arc qu'on modélise.

---

## 0. Avant de commencer — récolter les 3 inputs

Ne jamais partir sans ça. Si un manque, demander à Tony (une question à la fois) :

1. **L'objet banal de départ** — le point d'entrée concret et sous-estimé.
   (ex : un workflow qui tourne dans le noir, un écran vide, un curseur qui clignote).
2. **Le "pourquoi" / la thèse** — l'idée existentielle vers laquelle on monte.
   (ex : le plafond de verre, le vide, la limite qu'on cherche tous).
3. **La dernière phrase** — le gut-punch qui tombe juste avant le blanc. Elle doit retourner.

Défauts si Tony ne précise pas :
- Format **16:9** (essai) ou **9:16** si destiné TikTok/Reels — demander.
- Durée cible : **45–75s** en court, jusqu'à plusieurs min en long. Défaut **60s**.
- Fin **toujours** en fondu au blanc + silence.

---

## 1. La grammaire EGO (les 5 lois du style)

Non négociables. C'est ce qui distingue l'essai contemplatif d'une vidéo "motivation" banale.

1. **Ouverture banale, sous-estimée.** On commence petit : « ça a l'air de rien, mais... ».
   Jamais d'accroche criée. L'understatement crée la curiosité.
2. **Voix off calme, essayiste.** Débit posé, phrases courtes, **respirations** entre elles.
   On explique, on ne vend pas. Zéro musique-vidéo, zéro punchline forcée.
3. **Escalade continue, sans retour.** Concret → conceptuel → existentiel. Chaque palier
   monte d'un cran. On ne redescend jamais expliquer, on avance.
4. **Visuel minimaliste + désaturation.** Écrans sombres, zooms lents sur détails, diagrammes
   abstraits simples, grain léger. La palette **se désature progressivement vers le blanc**.
5. **Atterrissage cosmique/melancolique + fondu blanc.** La fin n'est pas une conclusion, c'est
   une **ouverture sur l'inconnu**. Le blanc EST le message (le vide, la limite). Puis silence.

---

## 2. Structure (timeline 60s — à étirer pour le long)

| Temps | Bloc | Contenu | Note |
|---|---|---|---|
| 0–8s | **BANAL** | L'objet de départ, plein cadre. « Ça a l'air de rien, mais... » | Understatement. Input §0.1. |
| 8–20s | **LA VRAIE QUESTION** | On pivote du *comment* vers le *pourquoi*. | Pose la thèse (§0.2) en creux. |
| 20–38s | **ESCALADE** | Montée par paliers : désir → doute → combat. Répétition du "pourquoi". | Cœur émotionnel. Jamais de retour. |
| 38–52s | **LE PLAFOND / LE VIDE** | On touche la limite. L'image s'ouvre, respiration. | Le pivot existentiel. |
| 52–58s | **LA LIMITE COMME QUÊTE** | « peut-être que c'est ça qu'on cherche tous. » | Retourne le sens. Input §0.3. |
| 58–60s | **BLANC** | Fondu au blanc total + silence. | Le blanc = le vide. Pas de logo dessus. |

Règle d'or : **le blanc tombe pile quand le spectateur croit qu'il va avoir une réponse.**
On lui donne le vide à la place. C'est ça qui laisse la trace.

---

## 3. La voix off (registre essayiste)

Écrire la VO en suivant ces contraintes :
- Phrases **courtes**. Une idée par phrase. Des *[temps]* marqués entre les paliers.
- **Répétition rythmique** autorisée et encouragée sur le mot pivot (« Pourquoi. Pourquoi. »).
- Vocabulaire simple, concret d'abord, abstrait ensuite. On ne surexplique jamais.
- La dernière ligne (§0.3) est **isolée**, suivie du blanc.

Squelette réutilisable (à remplir avec les inputs) → `assets/vo-template.md`.

---

## 4. Le prompt VideoBoost UNIQUE (le flex)

Tout l'intérêt : **une seule instruction** génère la vidéo entière. Pas de timeline montée à
la main. Le prompt encode la grammaire (§1) + la timeline (§2) + la VO (§3).

Template prêt à coller → `assets/master-prompt.txt`.
Le remplir avec : l'objet banal, la thèse, la VO complète, la durée, le ratio.

Vérifs avant d'envoyer le prompt :
- [ ] Le prompt dit explicitement « voix off calme, essayiste, respirations ».
- [ ] Il impose « escalade continue, jamais de retour en arrière ».
- [ ] Il impose « désaturation progressive vers le blanc » + « fondu au blanc final + silence ».
- [ ] La VO exacte est **collée dans le prompt** (pas résumée).
- [ ] Aucun cut nerveux, aucune musique "hype" demandée — nappe ambient minimale seulement.

---

## 5. Si Tony filme / veut du contrôle (convention 2 plans)

Pour ce format, la face-cam est optionnelle (l'essai marche souvent en pur voix off + b-roll).
Si Tony veut filmer, garder sa convention :
`[PLAN A — écran]` = ce qui est capturé/généré (b-roll, détails, diagrammes).
`[PLAN B — produit final]` = Tony face caméra ou voix off posée.

---

## 6. Charte — ENTORSE ASSUMÉE

⚠️ Ce format **ne suit pas** la charte sombre + or habituelle. La désaturation vers le blanc
est le cœur du concept.
- Palette : sombre au départ → **se vide vers le blanc**. L'or est à **proscrire** ici (il casse
  le côté melancolique).
- Un seul rappel de marque toléré : un **wordmark discret** (VideoBoost / Automation Boost) en
  toute fin, **après** le blanc, sur un carton séparé — jamais par-dessus le blanc lui-même.
- Titres si besoin : **Bebas Neue** UPPERCASE, mais en gris clair, pas en or.

Contrainte perso : si Tony demande un **prompt d'image** en sortie (ex : pour un plan précis),
le rendre entièrement en noir sans éléments or, format `prompt:"..."`.

---

## 7. Workflow d'exécution

1. Récolter les 3 inputs (§0). Demander ratio (16:9 / 9:16) et durée.
2. Écrire la **VO** depuis `assets/vo-template.md`, en respectant les 5 lois (§1).
3. Remplir le **prompt unique** depuis `assets/master-prompt.txt` (coller la VO en entier).
4. Passer les 5 vérifs (§4). Livrer VO + prompt unique.
5. Si Tony veut monter/sous-titrer après coup : relais vers `supermonteur` (sous-titres) ou
   `ffmpeg-node-expert` (fondu blanc, désaturation, nappe audio).
6. Angle démo Automation Boost : rappeler la punchline de vente — *« le format le plus dur à
   produire, un seul prompt, zéro montage »* — s'il compte en faire un post.

---

## 8. Checklist qualité avant publication

- [ ] Ouverture **banale et sous-estimée** (pas d'accroche criée).
- [ ] Voix off **calme**, phrases courtes, respirations marquées.
- [ ] Escalade **continue** concret → existentiel, **aucun retour en arrière**.
- [ ] Palette qui **se désature vers le blanc** au fil de la vidéo.
- [ ] Dernière phrase **isolée** + **fondu au blanc + silence**.
- [ ] Aucun logo/or **par-dessus** le blanc final.
- [ ] Nappe ambient minimale, coupée net sur le blanc (pas de drop, pas de hype).

---

## 9. Motif « trois pourquoi » + avatar-univers

Quand la VO répète **« Pourquoi. Pourquoi. Pourquoi. »**, afficher chaque mot au moment où il est
prononcé, en colonne, avec un décalage vertical croissant (0 px, 14 px, 28 px). Ne pas afficher les
trois lignes d'un seul coup : chaque ligne doit entrer avec un fondu court de 0,45 s. Exemple HTML :

```html
<div class="why-stack">
  <span class="why-line">POURQUOI.</span>
  <span class="why-line">POURQUOI.</span>
  <span class="why-line">POURQUOI.</span>
</div>
```

Le fond peut utiliser un avatar généré à partir de la référence utilisateur : portrait capuché, fond
noir, faible luminosité, contour jaune néon. Faire entrer l'image avant le pivot, puis remplacer ou
prolonger ce plan par un clip Higgsfield avec un travelling accéléré vers l'oeil. Le visage, les
lunettes et la coiffure restent verrouillés ; le zoom doit aboutir sur l'oeil avant la sortie du pivot.

La nappe musicale doit être un élément séparé des voix : lui appliquer `loop`, démarrer une seule fois
au clic utilisateur et ne jamais la mettre en pause quand une piste VO démarre. Les pistes VO peuvent
se couper entre elles, mais pas la nappe. Respecter `data-volume` lors de l'initialisation audio.

Cette recette est le **template premium VideoBoost « Essai contemplatif — Pourquoi »** : objet banal →
question → trois pourquoi décalés → avatar-univers → plafond / vide → fondu au blanc.
Après le fondu au blanc, ajouter un CTA court sur le carton final : **« Commente VIDEOBOOST pour soutenir
mon pourquoi — et sûrement le tien. »** Afficher `VIDEOBOOST` en accent jaune, sans recouvrir le blanc
pendant le fondu et sans ajouter de CTA commercial avant la dernière phrase.
Ajouter à l'ouverture un titre plein écran `POURQUOI`, très grand, jaune néon, visible de 0,08 s à 1,62 s
(environ 1,5 s), avec une entrée courte puis une sortie avant la première phrase de voix off.

---

## Fichiers du skill

- `assets/master-prompt.txt` — le prompt VideoBoost unique à remplir et coller.
- `assets/vo-template.md` — squelette de voix off en registre essayiste.

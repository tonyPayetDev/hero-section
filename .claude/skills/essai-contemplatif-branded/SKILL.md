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

⚠️ **CE PARAGRAPHE EST PÉRIMÉ — voir §8.2.** Il portait la décision du matin du 2026-08-21
(« aucune couleur d'accent : ni jaune, ni or, ni violet, ni néon »). Tony est revenu dessus
le soir même : « non c'était le contraire », et a fourni une image de référence en jaune
néon et violet sur noir. **C'est le §8.2 qui fait foi.**

Ce qui survit de ce paragraphe et reste vrai :
- Le **fondu au blanc final** et le silence sont la chute du format, quelle que soit la palette.
- **Aucun logo par-dessus le blanc** — le wordmark va sur un carton séparé, après.
- L'or chaud `#EAB308` reste à éviter **au profit du jaune néon `#FFE600`** : c'est le jaune
  froid et lumineux de la référence, pas le doré.

Note pour plus tard : deux instructions opposées ont coexisté dans ce fichier pendant quelques
heures et se sont contredites section contre section. Quand une décision change, corriger
**l'ancienne section**, ne pas se contenter d'en ajouter une nouvelle plus bas.

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
noir, faible luminosité, contour gris clair très discret (JAMAIS de néon). Faire entrer l'image avant le pivot, puis remplacer ou
prolonger ce plan par un clip Higgsfield avec un travelling accéléré vers l'oeil. Le visage, les
lunettes et la coiffure restent verrouillés ; le zoom doit aboutir sur l'oeil avant la sortie du pivot.

La nappe musicale doit être un élément séparé des voix : lui appliquer `loop`, démarrer une seule fois
au clic utilisateur et ne jamais la mettre en pause quand une piste VO démarre. Les pistes VO peuvent
se couper entre elles, mais pas la nappe. Respecter `data-volume` lors de l'initialisation audio.

Cette recette est le **template premium VideoBoost « Essai contemplatif — Pourquoi »** : objet banal →
question → trois pourquoi décalés → avatar-univers → plafond / vide → fondu au blanc.
Après le fondu au blanc, ajouter un CTA court sur le carton final : **« Commente VIDEOBOOST pour soutenir
mon pourquoi — et sûrement le tien. »** Afficher `VIDEOBOOST` en gris clair, sans recouvrir le blanc
pendant le fondu et sans ajouter de CTA commercial avant la dernière phrase.
Ajouter à l’ouverture un titre plein écran `POURQUOI`, très grand, en gris clair sur noir, visible de 0,08 s à 1,62 s
(environ 1,5 s), avec une entrée courte puis une sortie avant la première phrase de voix off.

---

## Fichiers du skill

- `assets/master-prompt.txt` — le prompt VideoBoost unique à remplir et coller.
- `assets/vo-template.md` — squelette de voix off en registre essayiste.

---

## 7. Ce que l'analyse d'EGO ajoute — et qui change la fabrication

Source : analyse de la chaîne EGO par *Le coin des youtubeurs* (agence VideoBiz), transcript
fourni par Tony le 2026-08-21. Ce qui suit ne remplace pas les §1-§4, ça les corrige sur
trois points où la version d'origine se trompait de cible.

### 7.1 L'arme n'est pas l'intro, c'est l'OUTRO

C'est le point qui retourne la méthode habituelle. La règle courante — « 50 % de l'énergie
sur l'intro, 50 % sur le reste » — est **l'inverse** de ce que fait EGO.

Les chiffres, sur ses vidéos réelles :

| Vidéo | Durée | Outro | Part |
|---|---|---|---|
| Le jeu de la vie | — | 2 min | le tournant |
| L'usine à trombones | 38 min | **18 min** | ~47 % |
| Le musée de l'oubli | — | la vidéo entière EST une outro | 100 % |

Sur *l'usine à trombones*, presque la moitié de la vidéo ne parle plus du jeu du tout :
c'est une réflexion sur l'IA et l'avenir de l'humanité.

Le raisonnement derrière : la courbe de rétention descend, donc la plupart des créateurs
investissent en décroissant. EGO fait le contraire — il ne pense pas à ceux qui sont partis,
il pense à ceux qui sont **restés**, et il leur donne le morceau le plus fort.

**Conséquence sur la timeline du §2 :** l'ancienne répartition donne 8 s au dernier bloc et
2 s au blanc, soit 17 % de la fin. C'est un format court, donc on ne monte pas à 47 % — mais
on ne descend plus sous **35 %**. Sur 60 s, ça veut dire que le bloc PLAFOND + LIMITE + BLANC
occupe au minimum 21 s, pas 10.

### 7.2 Le mouvement de bascule (à faire, littéralement)

La fin d'EGO sur *le jeu de la vie* n'est pas une conclusion : c'est un **retournement de
l'attention**. Il prend toute la fascination que le spectateur vient d'investir dans le sujet,
et il la retourne contre le sujet lui-même : *« tout ça est mille fois moins intéressant que
la vraie vie, dehors. »*

Le patron réutilisable :
1. Faire investir le spectateur dans un objet petit et clos (le §0.1).
2. Nommer cet investissement à voix haute.
3. Le retourner : ce n'était pas le sujet.

C'est plus fort qu'une morale, parce que le spectateur se surprend lui-même.

### 7.3 Le martèlement lexical, mesurable

EGO choisit **trois mots** par vidéo et les fait revenir **toutes les ~2 minutes**. Ce ne sont
pas des mots choisis au hasard : ils portent la température de la vidéo.

- *Le plus grand serveur Minecraft* → chaos, destruction, anarchie
- *Trackmania / Geometry Dash* → impossible, infaisable, inhumain

À faire à l'écriture : choisir le triplet AVANT d'écrire, puis vérifier la densité sur le
script fini. Sur un format 60 s, viser **une occurrence toutes les 12-15 s** — l'échelle
change, pas le principe. Un triplet absent du script signifie que la vidéo n'a pas de
température ; c'est vérifiable en comptant, pas en ressentant.

### 7.4 La structure en 5 phases, à ~20 % chacune

EGO équilibre ses récits en cinq blocs quasi égaux — c'est le chemin du héros, reformulé :

| Phase | Part | Sur 60 s |
|---|---|---|
| Tension initiale | 20 % | 0–12 s |
| Complexification | 20 % | 12–24 s |
| Point de non-retour | 20 % | 24–36 s |
| Accélération finale | 20 % | 36–48 s |
| Résolution | 20 % | 48–60 s |

À croiser avec le §2 : les deux découpages doivent tomber d'accord. Si le « point de
non-retour » arrive à 45 s, la vidéo est déséquilibrée — et ça se voit sans instrument.

### 7.5 L'avertissement à ne pas escamoter

Le transcript dit une chose que ce skill, dans sa version d'origine, laissait croire l'inverse :
**on ne peut pas copier EGO en copiant sa surface.** Les miniatures minimalistes, la voix posée,
les fondus au noir de 4 secondes — tous ceux qui ont copié ça se sont plantés, avec des taux de
clic et des rétentions mauvais.

Ce qui rend ces choix possibles chez lui : il a d'abord été **artisan**. Ses premières vidéos
suivaient toutes les règles — titres à double sens, structures optimisées, miniatures aux codes.
Il a bâti une base, une réputation, un nom. Aujourd'hui les gens cliquent **pour lui**, pas pour
le titre. Un inconnu qui sort un morceau appelé « Titre 1 » n'intéresse personne ; Taylor Swift
qui fait pareil fait des millions d'écoutes.

**Ce que ça veut dire concrètement pour Tony**, et il faut le dire avant de lancer la production :
ses comptes sont petits (131 abonnés TikTok sur le compte principal, 0 sur celui qui reçoit
réellement les publications). Une vidéo en format essai contemplatif **fera moins de vues** qu'une
vidéo Autoboost classique. Ce n'est pas un échec du format, c'est sa mécanique.

Donc :
- Ce format se produit **entre** les vidéos d'artisanat, jamais à leur place.
- Son indicateur n'est pas la vue, c'est le **commentaire qui raconte quelque chose** et le
  partage. Si on juge un essai contemplatif à ses vues, on l'abandonnera à tort.
- La formule à garder : **rêver comme un artiste, travailler comme un artisan.**

### 7.6 Vérifications supplémentaires avant d'envoyer le prompt

- [ ] Le bloc final (plafond + limite + blanc) fait **au moins 35 %** de la durée.
- [ ] Le **triplet lexical** est choisi et présent toutes les 12-15 s.
- [ ] Le **retournement** du §7.2 est écrit explicitement dans la VO, pas sous-entendu.
- [ ] Les cinq phases du §7.4 tombent à ±3 s de leur repère.
- [ ] Tony a été prévenu que ce format vise l'impact, pas la vue.

---

## 8. La palette — et la contradiction à trancher

### 8.1 Le thème Automation Boost, relevé dans les fichiers

Confirmé le 2026-08-21 en comptant les occurrences réelles dans
`/work/autoboost-neon-videos/_shared/` et les skills vidéo — pas déclaré de mémoire :

| Rôle | Valeur | Occurrences |
|---|---|---|
| Fond | `#0A0A0F` / `#0A0A0A` | 31 |
| **Jaune néon** — accent principal | `#FFE600` | 11 |
| **Violet** — accent secondaire | `#8B5CF6`, `#A855F7` | 16 |
| Or (variante chaude du jaune) | `#EAB308` | 7 |

Le cercle néon jaune autour de l'avatar est conservé explicitement depuis la mise en pause
de la v2. Voir `_shared/CHARTE.md` avant toute production.

### 8.2 La contradiction, en clair

Ces deux instructions de Tony coexistent et ne peuvent pas être vraies en même temps
pour un même rendu :

- **2026-08-21, sur l'essai ego :** « pas de jaune ou effet néon et violet ».
  La version livrée (`/essai-ego-tom-odell-v2/`) a été vérifiée à **0 pixel doré** sur toute
  la durée. C'était une demande explicite, répétée après un premier rendu refusé.
- **2026-08-21, plus tard :** « mon thème c'est jaune violet néon, valide bien ça ».

**Tranché par Tony le 2026-08-21 : c'est le néon qui gagne, y compris ici.** Il est revenu
sur le « pas de jaune » du matin — ses mots : « non c'était le contraire ». L'essai
contemplatif se produit donc **dans la charte Automation Boost**, jaune néon et violet
compris, comme tout le reste.

Ce qui reste vrai malgré ce choix, et qu'il faut tenir ensemble :
- Le **fondu au blanc final** et le **silence** ne sont pas une question de palette, c'est la
  chute du format (§1.5). On les garde.
- La **désaturation progressive** (§1.4) devient une désaturation *depuis* le néon vers le
  blanc, au lieu de partir d'une image déjà éteinte. L'accent jaune s'efface au fil de la
  montée — c'est plus fort que l'absence de couleur, parce que la perte se voit.
- Le néon reste un **accent**, pas un fond. Le plancher mesuré est 0,20 % des pixels (§8.4) ;
  un essai contemplatif vise le bas de la fourchette, pas prompt-reveal à 1,39 %.

**Leçon de méthode, à ne pas perdre :** deux rendus complets ont été produits sur une
consigne de palette qui a fini par s'inverser. Avant de lancer un rendu de ce format,
montrer **une image fixe** de test — pas une vidéo — et faire valider la palette dessus.
Trente secondes de vérification contre dix-sept minutes de rendu.

### 8.3 Vérifier la palette au lieu de la supposer

Un rendu « avec du jaune » ou « sans jaune » se mesure. Compter les pixels dans la teinte
cible sur des images extraites, jamais juger à l'œil sur une vignette :

```bash
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
ffmpeg -v error -i rendu.mp4 -vf fps=1,scale=160:-1 -f rawvideo -pix_fmt rgb24 - \
| /home/claude/tools/node/bin/node -e '
let b=[];process.stdin.on("data",d=>b.push(d)).on("end",()=>{
  const x=Buffer.concat(b); let jaune=0,violet=0;
  // Lire le flux comme un buffer RGB, 3 octets par pixel. Ne JAMAIS parser une
  // sortie texte de `od` en avançant de 3 : od coupe à 16 octets par ligne et
  // l alignement RVB se perd — faux positif garanti (constaté le 2026-08-21).
  for(let i=0;i+2<x.length;i+=3){
    const r=x[i],g=x[i+1],bl=x[i+2];
    if(r>170&&g>150&&bl<110) jaune++;
    if(r>110&&r<190&&g<110&&bl>190) violet++;
  }
  const n=Math.floor(x.length/3);
  console.log(`  jaune ${(jaune/n*100).toFixed(2)} %  ·  violet ${(violet/n*100).toFixed(2)} %`);
})'
```

### 8.4 Les seuils, mesurés sur les vidéos réelles

Un premier jet de ce skill proposait « ≥ 1,5 % de jaune ». Ce seuil était **inventé** : mesuré
sur la production réelle, il aurait recalé quatre vidéos Autoboost sur cinq. Valeurs relevées
le 2026-08-21 :

| Vidéo | Jaune | Violet |
|---|---|---|
| autoboost-top3-split | 0,25 % | 0,00 % |
| autoboost neon (63 · zapier-n8n) | 0,47 % | 0,01 % |
| veille-to-avatar-v3 | 0,84 % | 0,01 % |
| prompt-reveal-02 | 1,39 % | 0,00 % |
| **essai-ego-tom-odell-v2** (palette désaturée) | **0,00 %** | **0,00 %** |

Seuils qui en découlent :
- Palette **néon** demandée : jaune **≥ 0,20 %**. C'est le plancher observé, pas un souhait.
- Palette **désaturée** demandée : jaune **< 0,05 %**. La v2 validée est à 0,00 %.

### 8.5 Ce que la mesure révèle, et qu'il faut dire à Tony

**Le violet n'existe quasiment pas dans les vidéos.** Il est déclaré dans la charte
(`#8B5CF6`, `#A855F7`, 16 occurrences dans les fichiers) mais il pèse **0,00 à 0,01 %** des
pixels sur les cinq rendus mesurés. Autrement dit : « jaune violet néon » est aujourd'hui,
en pratique, **du jaune néon sur noir**. Le violet est dans les feuilles de style, pas à l'écran.

Ce n'est pas forcément un défaut — mais si Tony dit « mon thème c'est jaune violet néon », il
décrit une intention que la production ne réalise pas. Deux réponses possibles, à lui poser :
soit on introduit vraiment le violet (accent secondaire, dégradé, halo), soit on assume le
jaune seul et on retire le violet de la charte pour qu'elle cesse de mentir.

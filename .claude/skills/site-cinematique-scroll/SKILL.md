---
name: site-cinematique-scroll
description: >
  Produit un brief de build complet, copier-coller, pour un site cinématique « 3D scroll »
  (scrub de séquence d'images sur canvas) généré avec Seedance 2.5 sur le MCP Higgsfield
  puis construit par Claude Code. Sort le prompt entier : image hero, réglages du modèle,
  découpage des plans, structure du site, direction artistique, élément fonctionnel, et
  estimation de crédits. Utilise ce skill dès que Tony dit : « site cinématique », « site
  scroll », « 3D scroll », « scroll-driven », « site qui scrolle comme une vidéo »,
  « scroll scrub », « site Seedance », « site pour [client] avec de la vidéo IA »,
  « refais le pack sites cinématiques pour X », « site vitrine haut de gamme », « site
  qui déroule un plan », ou demande un site pour un restaurant, une agence, un bien
  immobilier, un produit ou son personal brand avec un effet vidéo au scroll. Déclenche
  aussi quand il évoque un devis ou une offre de site vitrine premium pour un client
  HoReCa, immo ou e-commerce, même sans nommer Seedance.
---

# Site cinématique scroll — Seedance 2.5 × Claude Code

Ce skill transforme une demande floue (« un site pour le resto de Badats ») en **un seul
prompt complet** que Tony colle dans Claude Code, plus le plan de génération vidéo et le
budget en crédits.

Langue de sortie : **français**. Ton : direct, technique, zéro superlatif.

---

## Ce que tu produis

Toujours ces quatre blocs, dans cet ordre :

1. **LE PLAN** — 3 lignes : forme de parcours choisie, nombre de clips, durée totale.
2. **LE PROMPT** — un seul bloc de code, copier-coller, sans commentaire dedans.
3. **LE BUDGET** — crédits estimés, calcul visible.
4. **CE QU'IL FAUT VÉRIFIER** — 2 à 3 points de contrôle avant livraison client.

Ne livre jamais une liste de scènes sans le prompt rédigé. Un brief sans prompt copiable
est un livrable raté — c'est l'erreur numéro un sur ce format.

---

## Étape 1 — Récupérer le brief

Il te faut cinq choses. Si trois ou plus manquent, demande-les en une seule fois, en une
liste courte. Si une ou deux manquent, choisis une valeur par défaut plausible et
signale-la en une ligne sous le prompt.

| Élément | Exemple |
|---|---|
| Le sujet | « Be Fresh, traiteur healthy à Saint-Denis » |
| La verticale | agence / HoReCa / e-commerce / personal brand / immobilier / machine |
| Le sujet visuel constant | le plat, le produit, le bâtiment, la personne |
| La couleur d'accent | une seule, jamais deux |
| L'élément fonctionnel | calculateur, sélecteur, configurateur, réservation |

L'élément fonctionnel n'est pas optionnel. Un site sans fonction se lit comme un
showreel et ne se vend pas.

---

## Étape 2 — Choisir la forme de parcours

Trois formes, une seule par site :

- **Plan unique (26-30 s)** — le parcours entier en une génération. Le plus propre, le
  plus rapide, propre à 2.5. À privilégier quand le sujet est un lieu ou un système qu'on
  traverse. Coût : 169 à 195 crédits.
- **Plans chaînés (3-4 clips de 8-12 s)** — quand le site a des chapitres distincts qui
  ne se traversent pas (le feu, la salle, l'assiette). Chaîne en passant la dernière
  frame d'un clip en `start_image` du suivant.
- **Extension** — un clip de 12 s prolongé deux fois en `video_extension`,
  `extension_mode forward`. Pour tout ce qui se déplace, ou quand un clip est parfait
  mais trop court.

---

## Étape 3 — Écrire le prompt

Le prompt suit toujours cette ossature. Les gabarits complets par verticale sont dans
`references/gabarits.md` — lis-les avant d'écrire, et adapte plutôt que de repartir de zéro.

```
Construis-moi un site cinématique « 3D scroll » pour [SUJET] — [UNE LIGNE DE CONTEXTE].

VISUELS — modèle seedance_2_5 sur le MCP Higgsfield. Réglages : mode omni_reference,
resolution 720p, aspect_ratio 16:9, generate_audio false. Génère d'abord UNE image hero
avec GPT Image 2 : [DESCRIPTION PRÉCISE]. Passe ce job id en start_image sur toutes les
générations.

[LE OU LES CLIPS, avec duration et le mouvement entre guillemets]

Upscale le clip retenu en 2K avec le preset AIGC avant de découper.

SITE — découpe le clip en 180 frames à 1600 px et scrub-le en une seule séquence canvas
sur [N] chapitres épinglés : [NOMS DES CHAPITRES]. Le texte de chaque chapitre se fond
dans le suivant selon la progression du scroll.

Puis les sections normales : [3 à 5 SECTIONS].

Donne au site un vrai travail, pas seulement une ambiance : ajoute [ÉLÉMENT FONCTIONNEL
DÉTAILLÉ].

Design : [FOND], un seul accent [COULEUR], [TYPOGRAPHIE], grain fin, scroll lissé.
Ton des textes : [TON].

Lance sur localhost et vérifie que [LES 2 CHOSES QUI PEUVENT CASSER] avant de me dire
que c'est fini.
```

### Règles non négociables dans le prompt

1. `generate_audio false` — on récolte des frames, on ne publie pas une vidéo.
2. Une seule image hero, référencée partout en `start_image`. C'est ce qui garde le sujet
   identique d'un plan à l'autre.
3. « un seul plan continu, aucune coupe, aucun tremblement caméra » dans **chaque**
   description de mouvement. Une coupe se lit comme un bug quand on scrolle en arrière.
4. 180 frames, 1600 px de large, qualité 86.
5. Le texte hero en bas à gauche sur un voile dégradé — jamais centré sur le sujet.
6. La dernière phrase est toujours l'ordre de lancer et vérifier.

---

## Étape 4 — Chiffrer

6,5 crédits/seconde en 720p · 3 crédits/seconde en 480p. Strictement linéaire.
Montre le calcul : `26 s × 6,5 = 169 crédits`.

Ajoute toujours : une passe de brouillon en 480p pour tester le mouvement avant de
s'engager, et le rappel que l'upscale n'a pas de preflight de coût.

Détails complets dans `references/modele.md`.

---

## Si c'est pour un client payant

Tony vend ces builds. Quand le sujet est un vrai client (HoReCa, immo, e-commerce) :

- Utilise **ses vraies photos** en `start_image` plutôt que des images générées — 2.5 les
  met en mouvement et le client se reconnaît.
- Rappelle en une ligne le positionnement tarifaire du livrable et le coût crédits réel,
  pour qu'il voie la marge.
- Termine par la seule question qui compte : **quand est-ce qu'on l'envoie au client ?**
  Ce format se construit vite et reste souvent sur l'étagère. Si Tony a déjà un build à
  90 % qui n'est pas parti, dis-le au lieu d'en démarrer un nouveau.

---

## Références

- `references/modele.md` — ce que Seedance 2.5 sait faire : modes, durées, résolutions,
  références, ratios, coûts, et la méthode 720p → upscale 2K → découpe.
- `references/recette.md` — le pipeline de build en 7 étapes et les 5 leçons de terrain.
- `references/gabarits.md` — les 6 gabarits de prompt par verticale : agence IA, HoReCa,
  e-commerce, personal brand, immobilier, extension. Lis toujours celui qui correspond
  avant d'écrire.

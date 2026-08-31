---
name: top-3-outils
description: Produit une vidéo verticale « le juge » — Tony note trois outils par catégorie (assez bien / bien / très bien) sur cinq à six catégories, avec un hook emprunté et un CTA d'abonnement. À utiliser quand Tony veut un classement d'outils IA. Ne pas confondre avec veille-to-video (actu du jour) ni tuto-ecran-16-9 (format long).
---

## Charte — ne pas la redéfinir ici

**Lire `/work/autoboost-neon-videos/_shared/CHARTE.md` avant toute production.**
Palette, typographie, avatar, voix, musique, CTA et pièges de rendu y sont fixés
une seule fois. Ce skill ne redéclare aucune couleur.

**Fonds animés : piocher dans `_shared/broll-abstrait/` avant d’en créer un.**
Dix motifs existent — reseau, flux, grille, planetes, workflow, constellation,
onde, circuit, spirale, tunnel. Le README du dossier dit ce que chacun signifie.
N’en dessiner un nouveau que si aucun des dix ne dit ce qu’il faut dire.

# Le juge — top 3 par catégorie

Format vertical, 55-75 s. Le principe tient en une phrase : **on ne raconte pas, on note.**

## La mécanique

Trois outils par catégorie, une seule échelle, toujours la même :

| Verdict | Ce que ça veut dire |
|---|---|
| **Assez bien** | fait le travail, mais on sent la limite |
| **Bien** | solide, on peut travailler avec |
| **Très bien** | c'est celui qu'on garde |

**L'échelle ne change jamais.** C'est ce qui rend le format reconnaissable d'une vidéo à l'autre, et ce qui permet de comparer les catégories entre elles.

Cinq à six catégories. En dessous de cinq, ça ne fait pas un classement. Au-delà de six, on décroche.

## La règle qui sépare ce format d'un carrousel lu à voix haute

**Chaque verdict doit être justifié par un fait, pas par un adjectif.**

Mauvais : « Claude, très bien, c'est le meilleur. »
Bon : « Claude, très bien — premier sur SWE-bench, et c'est le seul qui tient une boucle d'agent sans se perdre. »

Un chiffre, une date ou une limite concrète. Sans ça, le classement n'est qu'une opinion, et une opinion ne se partage pas.

## Vérifier avant de classer

⚠️ **Les modèles bougent tous les mois.** Ne jamais classer de mémoire — la connaissance du modèle qui écrit le script a plusieurs mois de retard.

Faire une recherche web par catégorie, le jour du tournage. Noter la date de la mesure dans le script. Si un classement ne peut pas être sourcé, la catégorie saute.

## Structure

| Bloc | Durée | Contenu |
|---|---|---|
| **Le hook** | 0-10 s | Emprunté ou généré, son d'origine conservé. Il ne parle pas des outils. |
| **La bascule** | 10-14 s | Une phrase qui relie le hook au classement. |
| **Les catégories** | 14-60 s | 5 à 6 blocs de 7-9 s. Trois outils, trois verdicts, un fait par verdict. |
| **Le CTA** | 60-75 s | Une seule action. |

## Le plan de notation

Un plan par catégorie, toujours la même grille :
- le nom de la catégorie en surtitre
- les trois outils empilés, du moins bon au meilleur
- le verdict à droite, en couleur : **gris** pour assez bien, **blanc** pour bien, **jaune de marque** pour très bien
- le fait justificatif en petit sous le nom

La montée du gris vers le jaune fait la lecture. On comprend le classement sans écouter.

## Palette

Charte AutomatisationBoost : jaune `#eab308`, violet `#8b5cf6`, fond `#0a0a0f`, bordures `#232330`.
**Aucun vert.** Vérifier les pastilles de fenêtre dans les captures terminal — c'est là qu'il se cache.

## Les transitions

`xfade` de 0,4 s entre catégories, `slideup` — on monte dans le classement, la transition le dit.
Le passage hook → premier plan se fait en `circleopen` : on révèle.

## La voix

Webhook n8n `tts-gen`, **`voixUrl` obligatoire**. Contrôle : F0 médian attendu 114-133 Hz.
Débit `atempo=1.09` — le format vit sur le rythme.

## La musique

Nappe stable, jamais un morceau qui monte. Vérifier le profil d'énergie avant de choisir :
un écart de plus de 10 dB sur le morceau donne une musique qui monte toute seule sous la voix.
`au-bord-des-etoiles` convient (−13 à −17 dB sur toute la durée).

**Voix normalisée d'abord, musique posée dessous à niveau fixe.** Normaliser la somme
remonte la musique avec la voix — c'est l'erreur qui rend une musique « trop forte »
quoi qu'on baisse en amont.

## Le CTA

Une seule action. Si le CTA promet une ressource, **elle doit exister et avoir sa porte**
avant le tournage. Un mot-clé annoncé sans porte, c'est un commentaire qui ne reçoit rien.

Sur YouTube et LinkedIn, Blotato ne gère rien : il faut répondre à la main ou mettre
le lien en description.

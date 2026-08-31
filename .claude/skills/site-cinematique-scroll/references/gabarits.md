# Gabarits de prompt par verticale

Six gabarits éprouvés. Repars de celui qui correspond à la verticale du client et
adapte-le — n'écris jamais un prompt de zéro.

## Sommaire

| # | Verticale | Gabarit |
|---|---|---|
| 01 | L'AGENCE IA | Le Système — agence d'automatisation |
| 02 | LOCAL / HORECA | La Table — restaurant, feu et fumée |
| 03 | E-COMMERCE | Le Drop — avec un viewer à faire tourner |
| 04 | PERSONAL BRAND | Le Portfolio — avec toi dedans |
| 05 | IMMOBILIER | Le Bien — une maison qui se démonte |
| 06 | LA RALLONGE | La Machine — un trajet qui ne s'arrête pas |

---

## 01 · L'AGENCE IA

### Le Système — agence d'automatisation

*Pour : agences automation, freelances n8n, studios IA, consultants tech. Le site qui vend ton propre service.*

```
Construis-moi un site cinématique « 3D scroll » pour [NOM DE L'AGENCE] — une agence d'automatisation IA qui installe des systèmes n8n chez des PME.

VISUELS — modèle seedance_2_5 sur le MCP Higgsfield. Réglages : mode omni_reference, resolution 720p, aspect_ratio 16:9, generate_audio false. Génère d'abord UNE image hero avec GPT Image 2 : une salle de contrôle sombre vue en plongée, un mur d'écrans affichant des graphes de workflow qui s'illuminent, un seul accent [COULEUR ACCENT] dans le noir, aucune personne dans la pièce. Passe ce job id en start_image sur toutes les générations.

Puis génère UN SEUL clip, duration 26 — tout le parcours en un plan, c'est le point de 2.5, pas de chaînage :

« Vol de caméra continu, un seul plan : la caméra part au ras d'un bureau vide dans le noir, monte lentement vers un mur d'écrans où un graphe de workflow s'assemble nœud par nœud, traverse ce graphe comme un couloir de lumière, les connexions s'allumant l'une après l'autre au passage, et débouche sur une vue large de la salle entière où tout le système tourne seul. Mouvement avant constant du début à la fin, aucune coupe, aucun tremblement caméra, éclairage sombre et volumétrique, rendu photoréaliste. »

Upscale ce clip en 2K avec le preset AIGC avant de découper.

SITE — découpe le clip en 180 frames à 1600 px et scrub-le en une seule séquence canvas sur quatre chapitres épinglés, pour que scroller fasse traverser le système : hero (« Tes process tournent. Sans toi. ») → LE CONSTAT → LE SYSTÈME → LE RÉSULTAT. Le texte de chaque chapitre se fond dans le suivant selon la progression du scroll.

Puis les sections normales : une bande de chiffres qui s'incrémentent au scroll (heures récupérées par mois, workflows en production, délai de mise en place) ; une section OFFRES en trois cartes — Audit, Installation, Maintenance — avec un prix de départ sur chacune ; un cas client en trois temps AVANT / APRÈS / GAIN ; une frise « Comment ça se passe » en quatre étapes ; un panneau « Réserver un audit » avec sélecteur de créneau qui reste bloqué tant qu'aucun créneau n'est choisi.

Donne au site un vrai travail, pas seulement une ambiance : ajoute un CALCULATEUR DE ROI — trois sliders (nombre de tâches manuelles par semaine, minutes par tâche, taux horaire) qui produisent en direct un coût annuel gaspillé et une économie estimée, le chiffre s'animant à chaque mouvement de slider.

Design : noir profond, un seul accent [COULEUR], display condensée en capitales, mono pour les labels techniques, grain fin, scroll lissé. Ton des textes : direct, technique, zéro superlatif.

Lance sur localhost et vérifie que le scrub est fluide de bout en bout et que le calculateur recalcule à chaque mouvement de slider avant de me dire que c'est fini.
```

> Fais-le tien : 26 secondes en 720p coûtent 169 crédits et remplacent quatre clips chaînés plus tout le travail de raccord entre eux. Le calculateur de ROI est ce qui transforme le site en argumentaire — le prospect arrive avec son propre chiffre avant même de te parler.

---

## 02 · LOCAL / HORECA

### La Table — restaurant, feu et fumée

*Pour : restaurants, cafés, bars, hôtels, salons. Le site local classique, le plus simple à vendre.*

```
Construis-moi un site cinématique pour [NOM DU RESTAURANT] — une table [TYPE DE CUISINE] à [VILLE].

VISUELS — seedance_2_5 sur le MCP Higgsfield, mode omni_reference, 720p, 16:9, generate_audio false. Génère chaque keyframe avec GPT Image 2 et utilise-la en start_image du clip correspondant.

1. LE FEU (duration 12) — « macro en très fort ralenti : une pièce de viande saisit sur la flamme nue, la graisse fond, des braises montent dans le noir, la lumière ambrée danse sur la croûte, un seul plan continu, aucune coupe. »

2. LA SALLE (duration 12) — « travelling avant lent et continu dans une salle sombre à l'heure dorée, banquettes de cuir et bougies, un barman prépare un cocktail en arrière-plan, brume chaude, un seul plan continu, aucune coupe. »

3. L'ASSIETTE (duration 8) — « plan en plongée verticale, les mains d'un chef dressent une assiette sur ardoise noire, la vapeur monte en volutes, un seul plan continu. »

SITE — hero plein écran qui scrolle-scrube le clip du feu, avec « [NOM] » en serif élégant dont les lettres s'écartent à l'apparition et une accroche de six mots dessous. Sections : un récit épinglé par-dessus le clip 2, texte très court ; une carte en deux colonnes ([CATÉGORIE A] / [CATÉGORIE B]) avec noms de plats et prix en typographie soignée ; une section privatisation par-dessus le clip 3 ; horaires, adresse et plan ; un panneau « Réserver une table » avec sélecteurs date, heure et nombre de couverts qui confirme en local.

Design : noir profond, texte crème chaud, un accent braise, grain de film, parallaxe lente. Ton : sobre, sensoriel, sûr de lui, jamais de superlatifs.

Fais une vraie passe mobile — la carte passe en une seule colonne élégante, la barre de chapitres disparaît.

Lance sur localhost et vérifie que le scrub du hero et le panneau de réservation s'affichent correctement en largeur desktop et mobile avant de me dire que c'est fini.
```

> Fais-le tien, ou vends-le : remplace par un vrai établissement, donne sa carte réelle à Claude, et utilise ses propres photos de plats en start_image — 2.5 les mettra en mouvement. C'est le livrable local le plus simple à facturer, et le 720p garde le job entier sous 250 crédits.

---

## 03 · E-COMMERCE

### Le Drop — avec un viewer à faire tourner

*Pour : tout produit physique — montres, sneakers, audio, mobilier, cosmétique.*

```
Construis-moi un site produit cinématique pour [MARQUE] qui lance le [NOM DU MODÈLE].

VISUELS — seedance_2_5 sur le MCP Higgsfield, mode omni_reference, 720p, 16:9, generate_audio false. Génère d'abord UNE image hero du produit avec GPT Image 2 — [matière, couleur, finition, lumière] sur un sol noir réfléchissant avec un contre-jour marqué — et passe ce job id en start_image sur CHAQUE clip.

1. RÉVÉLATION (duration 10) — « le produit tourne lentement pendant que la caméra se rapproche, les lumières de studio balayent la surface, fin de plan très près sur la texture de la matière, un seul plan continu, aucune coupe. »

2. TOURNETTE (duration 10) — « tournette parfaitement bouclable : le produit effectue une rotation complète de 360 degrés, parfaitement centré et de taille constante dans le cadre, caméra totalement fixe, éclairage uniforme, une seule révolution continue se terminant exactement où elle a commencé, aucun mouvement de caméra. »

3. MACRO (duration 8) — « glissement en très gros plan sur le détail de finition, coutures et arêtes nettes, faible profondeur de champ, un seul plan continu. »

SITE — scrube le clip 1 en hero, pour que scroller fasse tourner le produit. Puis construis une vraie boutique, pas un showreel : une bande de specs qui s'incrémentent au scroll ; un sélecteur de coloris à cinq pastilles qui change l'image hero, le nom, le prix et la couleur d'accent de la page ; un sélecteur de taille avec deux tailles en rupture, non sélectionnables ; un bouton « Ajouter au panier » qui refuse avec un avertissement visible tant qu'aucune taille n'est choisie, puis incrémente un compteur dans la nav ; une barre d'achat collante qui remonte une fois le hero passé.

Depuis le clip 2, découpe 72 frames dans un VIEWER GLISSER-POUR-TOURNER : glisser à gauche et à droite scrube les frames de la tournette, avec une rotation automatique douce jusqu'à la première interaction du visiteur.

Design : quasi-noir, un accent saturé, display lourde, mono pour les étiquettes.

Lance sur localhost et vérifie que le glisser-tourner pivote bien et que le garde-fou de taille bloque correctement avant de me dire que c'est fini.
```

> Fais-le tien : génère cinq coloris gratuitement au lieu de cinq clips — passe le filtre hue de ffmpeg sur ton unique image hero (hue=h=125, h=200, h=90) et chaque sortie se lit comme un produit différent.

---

## 04 · PERSONAL BRAND

### Le Portfolio — avec toi dedans

*Pour : créateurs, freelances, consultants. Attache d'abord une photo de toi bien éclairée, de face.*

```
Construis-moi un site portfolio cinématique « 3D scroll » pour moi — [TON NOM], [CE QUE TU FAIS EN UNE LIGNE].

VISUELS — seedance_2_5 sur le MCP Higgsfield, mode omni_reference, 720p, 16:9, generate_audio false. Uploade d'abord ma photo jointe sur Higgsfield et enregistre-la comme reference element, puis passe-la en image_references sur CHAQUE génération pour que mon visage reste constant. Garde ma tenue identique partout : [t-shirt noir, surchemise sombre]. Génère ensuite UNE image hero de moi avec GPT Image 2 en utilisant cette référence, et sers-t'en comme start_image des clips.

1. HERO (duration 12) — « la caméra orbite lentement autour de l'homme debout, immobile et composé, dans un studio en fond noir absolu, un contre-jour [COULEUR ACCENT] dessine son profil, fines particules en suspension, un seul plan continu, aucune coupe, il reste parfaitement immobile. »

2. LE TRAVAIL (duration 10) — « lent travelling avant cinématographique sur l'homme assis à un bureau sombre entouré d'écrans holographiques flottants, les écrans émettent leur propre lumière, un seul plan continu. »

3. LA FERMETURE (duration 8) — « l'homme marche lentement vers la caméra dans une galerie sombre bordée d'écrans lumineux, et s'arrête en pose franche, un seul plan continu. »

SITE — scrube l'orbite du hero pour que scroller me fasse tourner, avec « [TON NOM] » en display géante dont les lettres s'écartent une par une. Puis : une bande de statistiques qui s'incrémentent au scroll ([tes 3-4 meilleurs chiffres]) ; une section TROIS PILIERS par-dessus le clip 2 qui révèle [tes trois offres] une à la fois ; une grille TRAVAUX par-dessus le clip 3 avec une carte par [projet], une phrase d'accroche et un mouvement au survol ; un final avec ton CTA principal et les liens vers [tes réseaux]. Barre de chapitres sur le bord gauche, compteur de frames en direct dans un coin, curseur personnalisé, grain de film.

Design : noir encre, accent [COULEUR], texte crème, display condensée grasse, scroll lissé. Mets le texte du hero en bas à gauche par-dessus un voile dégradé sombre — jamais centré sur mon visage.

Lance sur localhost et vérifie que le scrub de l'orbite est parfaitement fluide avant de me dire que c'est fini.
```

> Fais-le tien : tout ce qui est entre crochets est à remplir. Génère deux ou trois prises de la seule orbite hero et garde celle où ta ressemblance tient sur toute la rotation — c'est ta photo d'entrée qui décide de tout.

---

## 05 · IMMOBILIER

### Le Bien — une maison qui se démonte

*Pour : annonces haut de gamme, promoteurs, architectes. Le spectacle sert aussi de plan d'étage.*

```
Construis-moi un site cinématique mono-bien pour [NOM DU BIEN] — une propriété [MATIÈRE / STYLE] à [LIEU], mise en vente à [PRIX]. Le moment signature : la maison se sépare en un éclatement au ralenti, et les éléments se résolvent en une vue éclatée flottante des trois niveaux.

VISUELS — seedance_2_5 sur le MCP Higgsfield, mode omni_reference, 720p, 16:9, generate_audio false. Génère quatre keyframes avec GPT Image 2, puis un clip depuis chacune en start_image :

1. L'ARRIVÉE (duration 10) — keyframe : vue aérienne au-dessus de [PAYSAGE] vers la maison à l'heure dorée. Mouvement : « glissement aérien avant et fluide vers la maison, la lumière dorée balaye les vitrages, un seul plan continu. »

2. LA RÉVÉLATION (duration 12) — keyframe : la maison suspendue en l'air au centre d'un immense éclatement de poudre colorée et d'éclats de verre, panaches magenta, or, cyan et violet sur fond quasi-noir. Mouvement : « ralenti extrême, l'éclatement continue de s'épanouir vers l'extérieur, les panaches se déploient à travers le cadre, la maison éclairée reste parfaitement immobile au centre, la caméra pousse très lentement, aucune coupe. »

3. LES NIVEAUX (duration 10) — keyframe : vue architecturale éclatée, trois plateaux meublés distincts lévitant séparément à la verticale, lumières chaudes dans chaque pièce, fins faisceaux reliant les niveaux, fond noir. Mouvement : « la caméra orbite et s'élève lentement autour des plateaux flottants, la parallaxe joue entre les niveaux, les plateaux restent parfaitement immobiles, un seul plan continu. »

4. L'INTÉRIEUR (duration 10) — keyframe : grande pièce de vie au coucher du soleil, baies vitrées toute hauteur. Mouvement : « lent travelling avant vers la baie et le paysage au-delà, un seul plan continu. »

SITE — quatre chapitres épinglés en scrub dans cet ordre, en donnant à LA RÉVÉLATION la course de scroll la plus longue pour que l'éclatement continue de s'épanouir pendant que le visiteur scrolle. Puis l'annonce elle-même : une bande de faits ([chambres, salles de bain, surface, terrain]) ; un SÉLECTEUR D'ÉTAGE interactif à trois onglets — recadre la keyframe éclatée en trois images par niveau avec ffmpeg et donne à chaque étage son nom, sa surface et sa liste de pièces ; une galerie ; un SIMULATEUR DE PRÊT fonctionnel avec sliders apport, taux et durée qui pilotent une mensualité en direct ; une étude extérieure à faire tourner au glisser ; une demande de visite privée avec créneaux qui bloque tant qu'aucun créneau n'est choisi.

Design : quasi-noir, pierre claire, un accent chaud, spectre coloré uniquement dans la révélation, serif à fort contraste avec italiques en accent.

Si le bien est fictif, indique-le clairement sur la page.

Lance sur localhost et vérifie que le sélecteur d'étage, le simulateur et tous les scrubs fonctionnent avant de me dire que c'est fini.
```

> Fais-le tien, ou vends-le : pour une vraie annonce, utilise les photos de l'agent en start_image — 2.5 les mettra en mouvement. Le chapitre d'éclatement est le crochet qui déclenche le rendez-vous ; le sélecteur d'étage et le simulateur sont ce qui en fait une page d'annonce crédible.

---

## 06 · LA RALLONGE

### La Machine — un trajet qui ne s'arrête pas

*Pour : véhicules, drones, machines — et chaque fois qu'un clip que tu adores se termine trop tôt.*

```
Construis-moi un site cinématique « 3D scroll » pour [MARQUE] — [PRODUIT QUI SE DÉPLACE]. Je veux que le trajet paraisse sans fin : utilise le mode extension de Seedance 2.5 plutôt que de générer des plans séparés.

VISUELS — seedance_2_5 sur le MCP Higgsfield, 720p, 16:9, generate_audio false.

ÉTAPE 1 — génère UNE image hero avec GPT Image 2 : [le produit, matière et finition] immobile dans [DÉCOR DE DÉPART] à l'aube.

ÉTAPE 2 — mode omni_reference, duration 12, start_image = cette image hero : « plan de suivi bas pendant que le véhicule s'élance à travers [DÉCOR DE DÉPART] à pleine vitesse, la matière du sol se soulève derrière les roues, la lumière rasante de l'aube balaye la carrosserie, un seul plan continu, aucune coupe, aucun tremblement caméra. »

ÉTAPE 3 — reprends le clip terminé et rappelle le modèle en mode video_extension, extension_mode forward, en passant ce clip en référence vidéo : « le trajet continue sans interruption tandis que [DÉCOR DE DÉPART] laisse place à [DÉCOR 2], le véhicule se faufile à pleine vitesse, la caméra garde sa position basse de suivi, un seul plan continu. » Répète l'extension une seconde fois pour l'emmener jusqu'à la nuit complète, éclairé uniquement par sa propre signature lumineuse sous les étoiles.

ÉTAPE 4 — upscale le clip étendu final en 2K avec le preset AIGC, puis découpe.

SITE — scrube le trajet étendu comme une seule séquence canvas, pour que scroller conduise de l'aube à la nuit. Un HUD de vitesse dans un coin qui grimpe de 0 à [VITESSE MAX] avec la progression du scroll, et une barre de chapitres nommant [DÉCOR 1] / [DÉCOR 2] / NUIT. Puis : des statistiques de performance qui s'incrémentent ; une section design avec des macros extraites du clip ; un configurateur à trois teintes qui recolorise une image hero et décale la couleur d'accent de la page ; un panneau « Réserver — acompte [MONTANT] » qui confirme en local.

Design : noir sur noir, un accent électrique, condensée ultra-large, transitions en filé de mouvement.

Lance sur localhost et vérifie que le HUD est bien synchronisé à la position de scroll et que les raccords d'extension sont invisibles avant de me dire que c'est fini.
```

> Fais-le tien : l'extension est la réponse à « ce clip est parfait mais trop court ». Elle garde le look et le mouvement verrouillés, ce que chaîner un nouveau clip ne fait jamais tout à fait. Marche pour les bateaux, les vélos électriques, les drones, les trains — tout ce qui se déplace.

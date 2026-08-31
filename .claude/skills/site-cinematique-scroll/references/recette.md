# La recette de build

L'effet « 3D scroll » que tu vois passer n'est pas du Three.js. C'est un scrub de séquence d'images sur canvas : un clip cinématique court est exporté en 180 frames numérotées, toutes préchargées, et la frame peinte sur le canvas est choisie par la position de scroll. Scroller en avant et en arrière joue le clip. Tout le relief vient de la vidéo. Rien d'autre. Voici le pipeline complet.

## Le pipeline en 7 étapes

**1. Colle le prompt entier, sans y toucher, la première fois.**

Chaque prompt de ce pack est un brief complet : les plans, la structure du site, la direction artistique et l'ordre de lancer puis vérifier. Fais-le tourner tel quel une fois avant de personnaliser quoi que ce soit.

**2. Génère UNE image hero d'abord, puis référence-la partout.**

Une seule image fixe avec GPT Image 2 ou Nano Banana Pro, puis ce job id en start_image sur chaque clip. C'est ce qui garde ton produit, ta personne ou ton bâtiment identique d'un plan à l'autre. C'est la différence entre un site qui a l'air cher et un site qui a l'air généré.

**3. Choisis ta forme de parcours.**

Un long plan unique — jusqu'à 30 s — est le plus propre, et il est propre à 2.5. Pour aller plus loin, chaîne : extrais la dernière frame d'un clip avec ffmpeg, uploade-la, passe-la en start_image du suivant. Ou utilise video_extension pour prolonger un clip que tu aimes déjà.

**4. Demande un mouvement continu, et dis-le deux fois.**

Mets « un seul plan continu, aucune coupe, aucun tremblement caméra » dans chaque prompt de mouvement. Une coupe franche a l'air cassée quand le visiteur scrolle en arrière, et le tremblé se lit comme un bug à vitesse de scroll.

**5. Upscale avant de découper.**

Des frames 720p étirées sur un hero de 27 pouces sont molles. Passe le clip retenu dans l'upscaler en 2K — le preset AIGC convient aux images générées — puis découpe. Il n'y a pas de preflight de coût sur l'upscale : vérifie ton solde avant et après.

**6. 180 frames, 1600 px de large, qualité 86.**

C'est le point d'équilibre : assez fluide pour se lire comme une vidéo, assez léger pour être préchargé. Plus de frames ou des frames plus grandes ne t'achètent que du temps de chargement.

**7. Fais lancer et vérifier par Claude avant qu'il annonce avoir fini.**

Termine chaque prompt par cette consigne. « Lance sur localhost et vérifie que chaque animation de scroll fonctionne avant de me dire que c'est fini » transforme un build optimiste en build contrôlé.

## Cinq leçons de terrain

**1. La cohérence bat la résolution.**

Un clip 720p légèrement mou où le produit est identique dans chaque plan a l'air plus cher que quatre clips nets de quatre produits légèrement différents. La référence d'image hero, c'est tout le jeu.

**2. Ne centre jamais le texte hero sur le sujet.**

Du gros texte en plein centre recouvre exactement la chose que tu as payée pour générer. Mets-le en bas à gauche, par-dessus un voile dégradé sombre, pour que le produit ou la personne reste visible. Ce seul changement fait passer un build pour de la direction artistique.

**3. Dépense tes crédits sur le hero, prends le premier résultat partout ailleurs.**

Le scrub du hero représente l'essentiel de l'effet. Génère deux ou trois prises de ce clip-là ; accepte la première version utilisable de tous les autres.

**4. Donne un travail au site, pas seulement une ambiance.**

Le spectacle seul se lit comme un showreel. Un sélecteur de coloris, un garde-fou de taille, un sélecteur d'étage, un calculateur de ROI — une seule vraie fonction transforme un beau scroll en site que quelqu'un achèterait.

**5. Fais du chargement une partie du spectacle.**

Ces sites préchargent des centaines de frames : il y a une attente, que tu la designes ou non. Un compteur de pourcentage plein écran qui s'efface à 100 transforme la seule faiblesse de la technique en première chose dont les gens se souviennent.

# Prompt à donner à Claude

Tu reçois un projet vidéo nommé « Histoire du jour — Lettre M » destiné à Hyperframe.

Lis d'abord README.md, puis `config/project.json`, `config/scenes.json`, `config/assets.json` et `config/lipsync.json`.

Ta mission : construire l'animation verticale complète 1080×1920 à 30 fps, environ 34 secondes, à partir de la timeline fournie. Le rendu doit être adapté aux enfants de 5 à 7 ans : mouvements doux, lisibilité maximale, rythme vivant sans surcharge.

Contraintes :
1. Respecter les 5 scènes et leurs timecodes.
2. Conserver Milo cohérent visuellement sur toute la vidéo.
3. Implémenter un lipsync deux états OPEN/CLOSED. Sur « mmm », la bouche reste principalement fermée.
4. Les changements de bouche ne doivent jamais déplacer le corps ou le visage.
5. Utiliser parallaxe, pop, scale, glow et micro-bob avec modération.
6. Laisser environ 2 secondes de réflexion au mini-jeu avant de révéler « maison ».
7. Maintenir tous les textes importants dans une safe zone de 120 px.
8. Garder « Histoire du jour » discret en bas.
9. Si un asset individuel manque, utiliser `assets/source/assets_master_sheet.png` uniquement comme référence visuelle et créer un placeholder clairement nommé ; ne pas prétendre qu'un damier imprimé est transparent.
10. Organiser le code/composition pour qu'un prochain épisode puisse être créé uniquement en remplaçant les données : lettre, phonème, héros, mots, narration et assets.

Commence par inspecter les fichiers et produire l'architecture de composition. Ensuite implémente les scènes, puis le lipsync, puis les transitions. Termine par une vérification des timecodes et de la lisibilité mobile.

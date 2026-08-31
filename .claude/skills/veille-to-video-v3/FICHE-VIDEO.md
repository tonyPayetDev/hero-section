# Toute vidéo livrée porte son prompt et ses images

**Règle posée par Tony le 2026-08-25** : *« quand tu crées une vidéo, assigne le
prompt à la vidéo et la ressource image aussi, et indique de remplacer par son
avatar. »*

Elle s'applique à **toute** vidéo publiée sur `previsualisation`, quel que soit le
pipeline — veille-to-video, foodboost, un clip Higgsfield repris, un montage ffmpeg.

---

## Pourquoi

Une vidéo sans son prompt est un cul-de-sac : on ne peut ni la refaire, ni la
décliner, ni en tirer une ressource. Le cas qui a déclenché la règle : le prompt
du TURBO n'était nulle part — ni dans l'historique Higgsfield (généré sur le web,
qui ne remonte pas dans l'API), ni dans le projet. La ressource publiée a donc
d'abord repris un texte approximatif tiré d'un message privé, et il a fallu que
Tony renvoie le vrai.

---

## Ce que la page de prévisualisation doit contenir

Sous la vidéo, systématiquement :

1. **Le prompt intégral**, dans un bloc `<pre>` copiable — pas résumé, pas
   reformulé. Échapper les `<` et `>` : les marqueurs de référence du type
   `<<<image_2>>>` disparaissent sinon du HTML sans laisser de trace.
2. **Les images de référence** : la vignette de chacune, avec son rôle
   (`image_2` = véhicule de départ, `image_3` = véhicule d'arrivée, portrait =
   avatar). Une référence citée dans le prompt mais absente de la page rend le
   prompt inutilisable.
3. **La ligne de substitution avatar** : dire explicitement quel marqueur
   remplacer par le portrait de Tony pour que ce soit lui au volant, à l'écran,
   dans le plan. Sans référence de visage, chaque génération produit quelqu'un
   d'autre.
4. **Le modèle et les réglages** : modèle, durée, ratio, audio activé ou non.

## Quand le prompt n'est pas disponible

Ça arrive — une génération faite sur le web Seedance Unlimited n'apparaît pas
dans l'API Higgsfield. Dans ce cas : **l'écrire sur la page**, noir sur blanc
(« prompt non fourni, généré sur le web »). Ne jamais reconstituer un prompt de
mémoire et le présenter comme celui d'origine : c'est exactement l'erreur du
TURBO.

## Fichier de projet

Chaque dossier de vidéo porte un `PROMPT.md` avec les mêmes quatre éléments.
La page de prévisualisation est ce que voit Tony ; le `PROMPT.md` est ce qui
survit quand la route est écrasée.

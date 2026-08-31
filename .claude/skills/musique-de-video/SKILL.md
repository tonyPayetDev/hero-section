---
name: musique-de-video
description: Analyse la musique d'une vidéo importée — extrait l'audio, sépare voix et instrumental, et MESURE le tempo, la position de chaque temps et la courbe d'énergie. Sert à caler des coupes ou du texte sur le beat, et à retrouver une musique équivalente libre de droits quand la bande d'origine ne peut pas être réutilisée.
---

# musique-de-video

Tu importes une vidéo, tu obtiens : sa piste audio, son instrumental séparé de
la voix, son **tempo mesuré**, la **position de chaque temps en secondes**, et
sa courbe d'énergie.

## Ce que ça fait, et ce que ça ne fait pas

**Ça mesure.** Le tempo n'est pas deviné ni lu dans des métadonnées : il est
mesuré sur la bande de la grosse caisse. La sortie principale n'est pas le BPM
mais la **grille de temps** — la liste des instants où tombe chaque temps. C'est
ce qu'il faut pour caler une coupe, un flash ou un mot ; un BPM seul ne suffit
pas, il manque la phase.

**Ça n'identifie pas le morceau.** Il n'y a aucune clé d'empreinte audio dans
cet environnement — pas de « Shazam ». Ne pas promettre une identification :
si Tony a besoin du titre, il faut passer par une application sur son téléphone,
ou brancher une clé AudD / ACRCloud ici.

**Sur la récupération de la bande.** Extraire l'audio d'une vidéo qui appartient
à Tony, ou dont il détient les droits, ne pose aucun problème — c'est le cas de
tous ses rendus. En revanche, extraire la musique de la vidéo de quelqu'un
d'autre pour la reposer sur une publication, c'est de la contrefaçon, quel que
soit l'outil qui le fait. La bonne sortie dans ce cas est la **mesure** : on
garde le tempo et la structure, et on prend une bande équivalente qu'on a le
droit d'utiliser. Le montage est identique à l'oreille, et il est publiable.
Cette distinction a déjà été appliquée : voir `_shared/` pour les bandes
libres de droits déjà en dépôt.

## Marche à suivre

```bash
# 1. Extraire l'audio et séparer voix / instrumental
bash .claude/skills/musique-de-video/scripts/extraire.sh maVideo.mp4

# 2. Mesurer le tempo et la grille de temps
export PATH="/home/claude/tools/node/bin:$PATH"
node .claude/skills/musique-de-video/scripts/analyser.mjs maVideo/musique/audio.wav
```

`extraire.sh` écrit dans `<dossier-de-la-video>/musique/` :

| fichier | ce que c'est |
|---|---|
| `audio.wav` | la bande complète, 48 kHz mono — c'est elle qu'on analyse |
| `piste-a.mp3` / `piste-b.mp3` | les deux pistes rendues par la séparation |

⚠️ **La séparation ne dit pas laquelle est l'instrumental.** L'ordre des sorties
n'est pas garanti et rien dans la réponse ne l'indique. Lance `analyser.mjs` sur
les deux : celle qui rend un tempo est l'instrumental, l'autre est la voix.
Ne jamais parier sur la position.

**Cas réel, 2026-08-24, référence de 27 s :**

| piste | attaques | tempo |
|---|---|---|
| piste-a | 59 | **132,3 BPM** → instrumental |
| piste-b | 6 | non déterminé → voix |
| bande complète | 57 | **123,1 BPM** ← faux |

**Regarde la troisième ligne : c'est tout l'intérêt de séparer avant de
mesurer.** Sur le mixage complet, les syllabes de la voix sont comptées comme
des attaques et tirent l'estimation à 123,1 BPM. Une grille calée là-dessus
dérive de près d'un temps toutes les six mesures — assez pour que le montage
« sonne faux » sans qu'on sache dire pourquoi. **Toujours mesurer sur
l'instrumental isolé, jamais sur la bande complète.**

`analyser.mjs` écrit un JSON qui contient :

- `bpm` — le tempo mesuré
- `periodeBeat` — la durée d'un temps en secondes
- `phase` — l'instant du premier temps
- `grilleBeats` — **la liste de tous les temps en secondes**, la sortie qui sert
- `energieParSeconde` — la courbe, pour repérer montées et respirations

## Ce que la mesure sait faire et ne sait pas faire

Validé sur un morceau réel de 130 s : **132,5 BPM, 218 attaques, 287 temps
placés** — cohérent avec le ~134 BPM relevé indépendamment sur cette bande.

**Elle échoue quand il n'y a pas de percussion, ou sur moins d'une vingtaine de
secondes.** Testé sur une bande de 12 s : 13 attaques seulement, tempo non
déterminé — et c'est le bon comportement. Le script écrit alors
« tempo non déterminé » au lieu d'inventer un chiffre. Un BPM faux est pire que
pas de BPM : il décale tout un montage sans qu'on comprenne pourquoi.

## Les deux pièges ffmpeg, à ne jamais reprendre

Ils ne plantent pas. Ils rendent un résultat **plausible et faux**.

1. **`-ar` est une option de SORTIE.** Elle ne s'applique pas avant
   `asetnsamples`. Sur une source 44,1 kHz, des fenêtres de N échantillons
   restent à 44,1 kHz : la cadence réelle n'est pas celle qu'on croit et la
   dérive atteint plusieurs secondes en fin de fichier. Mettre
   `aresample=` **dans la chaîne de filtres**, et surtout **redéduire** la
   cadence depuis le nombre de fenêtres obtenues — c'est ce que fait
   `analyser.mjs` avec `fenetresParSeconde`.
2. **Un filtre `=-?[0-9.]*$` ne matche pas `-inf`.** Les fenêtres de silence
   sont alors *supprimées* au lieu d'être mises à zéro, et tous les index
   suivants se décalent. Accepter `-inf` explicitement et le mapper à une
   valeur plancher.

Et un troisième, pour toute analyse audio : **`-map 0:a` est obligatoire**.
Sans lui, ffmpeg analyse le flux vidéo et ne dit rien — ce qui se lit à tort
comme « il n'y a pas de son ».

## Pourquoi la mesure se fait sur la bande du kick

Sous 150 Hz, il ne reste presque que la grosse caisse. Les voix, les cuivres et
les nappes ajoutent de l'énergie hors-tempo qui brouille la détection : sur la
bande complète, la même piste donne un tempo instable. Le `lowpass=f=150` de
`analyser.mjs` n'est pas un réglage esthétique, c'est ce qui rend la mesure
reproductible.

Le tempo est ramené entre 70 et 180 BPM en doublant ou divisant. Une mesure à
66 BPM est presque toujours du 132 dont une attaque sur deux a été manquée.

## Ce qu'on en fait ensuite

La grille de temps se branche directement sur un montage : `grilleBeats` donne
les instants où poser une coupe, un mot, un flash ou un changement de plan.
C'est exactement la donnée qu'attendent les compositions beat-sync existantes —
elles la codaient jusqu'ici en dur après une mesure faite à la main.

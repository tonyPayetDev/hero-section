# BGM — Autoboost Neon Video

Bibliothèque musicale rangée **par format vidéo**. Métadonnées complètes et mesurées :
**`bgm-manifest.json`** (c'est la source de vérité, ce README n'en est que le mode d'emploi).

Avant cette bibliothèque, chaque vidéo empruntait une BGM au hasard d'un autre projet.
**On ne fait plus ça** : on prend la piste de la famille, on applique son `start_gain_db`.

## Choisir : une ligne par format

| Ton format | Prends | Pourquoi |
|---|---|---|
| Journal / veille IA | `journal-moon-walk-88.mp3` | informatif et tendu, sans montée qui se batte avec la voix |
| Journal, version moins sombre | `journal-digital-clouds-128.mp3` | même rôle, plus clair — mais ducker un peu plus |
| Hook puissant / action / yapping | `hook-epical-drums-02-80.mp3` | impacts et montées, aucune nappe qui traîne |
| Révélation A/B, mindset, essai | `mindset-epical-drums-03-80.mp3` | épique et retenu, 183 s sans boucler |
| Idem, format court | `mindset-epical-drums-05-75.mp3` | même famille, plus discret |
| FoodBoost / vitrine | `food-cat-walk-128.mp3` | chaleureux et rythmé (⚠ le medium se remplit après ~29 s) |
| FoodBoost long / voix continue | `food-deep-urban-122.mp3` | le lit le plus prévisible de tous, 288 s sans surprise |
| Horror sous une voix | `horror-piano-horror-ambient.mp3` | tension sans grille rythmique |
| Horror / doc sombre, long | `horror-echoes-ambient.mp3` | le medium le plus vide de la bibliothèque |
| Corporate / VSL / luxe | `vsl-voxscape-ambient.mp3` | posé, crédible, 299 s |
| Hook cyberpunk (néon) | `bgm-cyberpunk-city.mp3` | identité néon — ⚠ medium chargé, sidechain obligatoire |
| Beat-sync sur la trend | `flowers_horror.mp3` | ⚠ licence NON établie, voir plus bas |
| Hook classique / contraste | `valse-des-fleurs-maison-tutti.mp3` | **production maison**, orchestre complet — hook SANS parole uniquement |
| Valse sous une voix / hook contraste, version longue | `valse-des-fleurs-integrale-71.mp3` | l enregistrement complet (211 s) envoyé par Tony — ⚠ licence à établir, headroom -14,5 |
| Lit sous une voix, le plus transparent | `valse-des-fleurs-maison-evidee.mp3` | **production maison**, orchestration évidée — headroom −20,8, le meilleur de la bibliothèque |

Les deux `valse-des-fleurs-maison-*` sont **nos propres phonogrammes** d'une partition du domaine
public : aucun droit voisin de tiers, aucune empreinte Content ID possible. Ils se somment sans
couture (l'évidée est la moitié basse du tutti). Mode d'emploi, mesures et sources MIDI :
**`valse-des-fleurs-maison/README.md`**.

**Le critère de tri, si tu dois arbitrer toi-même** : `voice_headroom_db` dans le manifeste.
C'est le niveau de la bande 1–3,5 kHz (là où vit l'intelligibilité de la voix) **relatif au
loudness du morceau**. Plus il est négatif, moins la piste encombre la voix à volume perçu égal.
Objectif ≥ −16. En dessous de −13, ça se bat avec la voix quel que soit le gain.
C'est plus fiable que les tags du site, et ça se mesure au lieu de s'écouter.

## Poser le niveau

Référence de la maison : **écart voix / musique ≈ 16 dB** pendant la parole, **mix final −16 LUFS**.

1. Applique le `start_gain_db` de la piste (il l'amène à ~−30 LUFS, soit ~14–16 LU sous une voix
   montée à −16 LUFS). **Ce gain est propre à chaque piste** — les morceaux vont de −7,6 à
   −16 LUFS à la source, donc recopier un gain d'une piste à l'autre se trompe de 8 dB.
2. Ajoute un **sidechain** piloté par la voix plutôt qu'un gain fixe, dès que la piste a du medium
   (`sidechaincompress`, ou `threshold=0.05:ratio=4` comme sur `bgm-cyberpunk-city.mp3`).
3. Vérifie le mix final à −16 LUFS.

### ⚠ Le piège déjà payé : la vidéo qui ouvre sans voix

Ces gains sont calibrés pour **vivre sous une voix**. Une vidéo qui **ouvre sans voix** — hook
visuel muet, logo, plan d'ambiance avant la première phrase — sonnera **trop basse** sur ces
réglages, parce qu'il n'y a rien au-dessus pour justifier que la musique soit à −30 LUFS.

Compenser : **+6 à +10 dB sur la portion sans voix**, puis descendre au `start_gain_db` sur
l'entrée de la voix (rampe de 300–500 ms, pas une coupe). C'est exactement le cas du format
« Tu veux le même système ? » (hook costumé muet de 7 s) et de tout hook visuel.
Le symptôme si on oublie : « on n'entend pas la musique au début ».

## Licence

Toutes les pistes sauf `flowers_horror.mp3` sont sous **Mixkit Stock Music Free License**
(vérifié le 2026-08-18, texte réel derrière `https://mixkit.co/license/modal/musicFree/`) :

- **0 €, aucune attribution requise**, usage commercial autorisé.
- **Autorisé** : posts vidéo réseaux sociaux, publicités marketing en ligne, podcasts, éducatif,
  YouTube*. → **les 5 réseaux de Tony sont couverts** (TikTok, Instagram, YouTube, Facebook,
  LinkedIn). C'est le vrai intérêt de cette source par rapport à un son de trend.
- **Interdit** : CD/DVD, **diffusion TV & radio**, jeux vidéo, remixer dans un morceau purement
  musical, revendiquer la propriété, **enregistrer la piste sur un service de gestion de droits**.
- **\* YouTube** : une réclamation Content ID reste possible ; Mixkit demande de faire suivre le
  détail à `team@mixkit.co`.

`flowers_horror.mp3` est un **son de trend sans licence commerciale établie**. TikTok considère
son catalogue général comme **non pré-autorisé pour du contenu commercial**, « défini comme tout
contenu posté par une marque ». Automation Boost est une marque. À traiter comme un risque assumé
sur ce format précis, pas comme une piste de bibliothèque.

## Limite honnête

Les pistes ont été **choisies à la mesure** (bandes spectrales, LUFS, spectrogrammes pour vérifier
l'absence de voix) — **elles n'ont pas été écoutées**. La qualification est objective mais pas
artistique. Écoute une piste avant de l'adopter comme standard d'un format.

## Ne pas écraser

`sfx-palette/v1` est figée. `music-tony/` contient les créations de Tony. Cette bibliothèque
**n'ajoute que dans `bgm/`**. Toute évolution = nouvelle entrée dans le manifeste, jamais un
remplacement de fichier.

---

| Fichier | Titre / source | Durée | Loudness | Licence |
|---|---|---|---|---|
| `bgm-cyberpunk-city.mp3` | Mixkit music #140 « Cyberpunk City » — `assets.mixkit.co/music/140/140.mp3` | 99,7 s | −10,9 LUFS | Mixkit Free License (usage commercial gratuit, sans attribution) |
| `flowers_horror.mp3` | son de trend « YOU CAN ASK THE FLOWERS (HORROR MIX) » | — | −12,4 LUFS | son de trend, usage social |

## Cyberpunk City — pourquoi ce morceau (2026-08-18)

Retenu pour `autoboost-62-meme-systeme` après comparaison mesurée de 6 candidats Mixkit
(#140, #464 Sci-Fi Score, #623 Deep Urban, #134 Deep Techno Ambience, #80 Daredevil,
#162 Minimal Techno 01).

- **Identité** : synthé cyberpunk / ville de nuit — c'est exactement le décor du hook (toits,
  néons) et la charte néon de la marque. #80 « Daredevil » était plus « héroïque » mais générique.
- **Intro de 2 s à −25,5 dB** puis un lit régulier à ~−13 dB (profil RMS mesuré par tranches
  de 2 s). L'intro laisse respirer le balancement, le lit régulier rend le ducking **prévisible**.
- **Régularité choisie exprès contre un crescendo.** #464 monte de −17,7 à −11 dB sur 40 s :
  joli en solo, mais il monterait pile pendant la partie parlée et se battrait avec la voix.
  Sur une vidéo où on pilote le niveau à la main, un lit stable vaut mieux qu'un arrangement.
- **Instrumental vérifié**, pas supposé : spectrogramme sur 40 s → lignes harmoniques
  rigoureusement droites sous 2 kHz (synthé), aucune bande de formants ni vibrato. Pas de voix.

**Niveau de référence** : gain statique **0,314** + sidechain `threshold=0.05:ratio=4` sous la
voix. Mesuré sur les stems : **écart voix/musique = 16,0 dB** pendant la parole.
Le morceau étant à −10,9 LUFS (fort), ce gain est bas — le recalculer si on change de morceau,
ne pas le recopier tel quel.

---

## Deux repères repris de l'ancienne version de ce fichier

Ils avaient disparu lors d'une réécriture ; ils sont mesurés, donc on les garde.

- **Le volume ne se recopie pas d'une piste à l'autre.** `flowers_horror.mp3` est à
  **−12,4 LUFS** (`data-volume="0.05"`), `bgm-ascension.mp3` à **−19,1 LUFS**
  (`0.09`). Sept décibels d'écart : reprendre le même volume fait passer la musique
  devant la voix.
- **Boucler avec `-stream_loop -1 -t <durée>` sur l'entrée**, jamais avec un `trim`
  dans le graphe de filtres, quand le morceau est plus court que la composition.

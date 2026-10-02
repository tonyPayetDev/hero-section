# AutoBoost Studio

Tu déposes ta vidéo face caméra, l'outil fait le reste. Tout tourne **sur ton PC**, sans LLM :

1. **Transcription** locale (whisper.cpp via HyperFrames).
2. **Coupe des silences** et légère accélération.
3. **Voix** : ta voix améliorée (débruitage, de-essing, compression, présence, −16 LUFS). En option, ta voix clonée (WaveSpeed ou ton webhook n8n).
4. **Suppression du fond** (option).
5. **Motion design** au style « boost niveau ». Les écrans sont choisis par règles selon ce que tu dis : carte claire surlignée en jaune, chaîne d'outils, gros chiffres, étapes, avant/maintenant, liste, question, CTA tapé. S'y ajoutent les stickers, la puce NIVEAU 1 → MAX, les sous-titres mot à mot dans une pastille, les néons qui battent au tempo et les punch-ins sur les coupes.
6. **Rendu HyperFrames**, puis **mixage** : voix, musique à niveau fixe baissée sous la voix, bruitages.

## Installation (une fois)

1. Installe **Node.js 20 ou plus** : https://nodejs.org (version LTS).
2. Copie le dossier `autoboost-studio` sur ton PC, puis dans un terminal :
   ```bash
   cd autoboost-studio
   npm install
   npx hyperframes doctor      # vérifie Chrome headless + ffmpeg ; suis ce qu'il propose
   ```
   ffmpeg et ffprobe sont fournis par npm, il n'y a rien à installer à côté. Au **premier montage**,
   HyperFrames télécharge le modèle de transcription (~470 Mo) et, si tu coches « supprimer le fond »,
   le modèle de détourage (~170 Mo).

## Utilisation

```bash
npm start
```
puis ouvre **http://localhost:4747**. Dépose ta vidéo et clique sur **Lancer le montage**. La vidéo finale
apparaît dans la colonne de droite avec un bouton de téléchargement. Elle est aussi enregistrée dans
`jobs/<date>/video-finale.mp4`, avec la transcription et le plan des écrans.

## Ce que tu remplis

| Champ | Obligatoire | Par défaut | À quoi ça sert |
|---|---|---|---|
| **Ta vidéo** | **oui** | — | Face caméra, tu parles. mp4 ou mov, n'importe quel format. |
| Format | non | 9:16 | 9:16 pour Reels/TikTok/Shorts, 16:9 pour YouTube ou une VSL |
| Voix | non | ta voix améliorée | voix clonée = réécrite phrase par phrase (bouche non synchronisée au mot près) |
| Musique | non | Deep Urban (house) | ou Valse des fleurs (maison), Epical drums, aucune, ou ton propre mp3 |
| Mot-clé CTA | non | détecté | si tu dis « commente BOOST », il est trouvé tout seul. Sinon, tape-le ici. |
| Vitesse | non | 1,10× | accélération de ta parole |
| Couper les silences | non | oui | rythme « yapping » |
| Supprimer le fond | non | non | tu es détouré devant un décor studio néon. Compte ~1 s par image sur un CPU (30 s de vidéo ≈ 15 min). |
| Marque | non | AUTOMATISATIONBOOST | le texte en haut des cartes |
| Vidéo d'un concurrent | non | — | l'outil **mesure son rythme de montage** (durée de ses plans) et cale le changement d'écran dessus |

Réglages pour la voix clonée, une seule fois, enregistrés dans `config.json` sur ton PC :
- **WaveSpeed** : ta clé API + l'URL publique d'un mp3 de ta voix (10 à 30 s). Ça coûte environ 0,05 $ par 100 caractères.
- **ou webhook n8n** : l'URL de ton webhook `tts-gen`. Il reçoit `{text, voixUrl}` et renvoie un mp3.

## Comment parler pour avoir les bons écrans (pas d'IA : des règles)

L'outil découpe ta transcription en phrases. Pour chacune, il choisit un modèle :

| Si tu dis… | Écran |
|---|---|
| « **commente BOOST** », « écris FORMATION » | CTA : COMMENTE + mot géant élastique + champ commentaire tapé (caméra plein écran en 9:16) |
| « **d'abord**… », « **ensuite**… », « **enfin**… », « étape » | carte ÉTAPE 1, 2, 3 |
| deux outils ou plus : « **Gmail**, **ChatGPT** et **Notion** » | chaîne d'applis reliées par des flèches, chaque appli s'allume quand tu la cites |
| un **chiffre** : « **18** heures », « **3** clients », « **dix** minutes » | gros chiffre qui compte jusqu'à la valeur + son unité |
| une **énumération** : « écrire, filmer, monter, publier » | liste de puces qui se cochent une à une |
| « **au lieu de**… », « pas… **mais**… », « avant… maintenant » | duo AVANT (barré en rouge) / MAINTENANT (or) |
| une **question** « … ? » | grand titre sombre surligné |
| tout le reste | carte claire, titre noir, mot fort surligné en jaune |

La **première phrase** est le hook : plein écran, avec un zoom punch et le sticker ÇA PART. Les stickers
viennent des mots-clés : lent/problème → TROP LENT, simple/rapide → PLUS SIMPLE, temps → GAIN TEMPS,
système/automatiser → BON SYSTÈME, plus/résultat → ÇA MONTE.

**Astuce** : des phrases courtes, un chiffre précis, les noms des outils, et le CTA à la fin
(« commente MOT »). C'est ce qui donne le plus d'écrans différents.

## Personnaliser les modèles

- `templates/composition.html` : tout le style (couleurs, polices, cartes, pastille, néons).
- `lib/compose.mjs` : l'animation de chaque type d'écran.
- `lib/plan.mjs` : les règles (mots-outils, stickers, déclencheurs). Ajoute tes outils dans `TOOLS`.
- `templates/music.json` + `assets/music/` : la bibliothèque musicale (point de départ, boucle, gain, BPM).
- `assets/sfx/` : les bruitages.

## Problèmes courants

- **« whisper-cpp unavailable »** : lance `npx hyperframes doctor`, ou `npx hyperframes models install whisper`.
- **Rendu très lent** : normal sur CPU (~0,3 à 0,6 s par image). Laisse « supprimer le fond » décoché pour aller vite.
- **Mot mal transcrit** (un nom propre surtout) : le texte est dans `jobs/<date>/transcription.txt`.
  Le mot-clé CTA se force dans le formulaire.

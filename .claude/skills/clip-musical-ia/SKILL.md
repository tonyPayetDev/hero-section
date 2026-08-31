---
name: clip-musical-ia
description: Monte un clip musical complet à partir d'un .wav envoyé par Tony et d'une liste de liens Higgsfield. Mesure le morceau (BPM, structure, où il chante), monte l'image sur cette mesure, sort le 9:16 et le 16:9. À utiliser dès que Tony envoie une musique en .wav avec des liens de clips.
---

# Clip musical IA — d'un .wav et de liens Higgsfield à deux formats livrés

Déclencheur : Tony envoie **un fichier .wav** + **des liens `higgsfield.ai/s/...`**, et
demande un clip d'une durée cible. Rien d'autre n'est nécessaire pour démarrer.

Première production : `roule kiki — ouwa`, 2 min 30, 109 plans, 6 clips sources.
Sortie de référence : `/work/previsualisation/clip-roule-kiki/`.

---

## 0. Le principe, en une phrase

**On mesure le morceau, et la mesure décide du montage.** Pas l'inverse.

Trois questions se posent au fichier son, jamais à l'oreille :

1. Où la musique **s'arrête-t-elle vraiment** ? (presque jamais à la fin du fichier)
2. Quel est le **pouls** et où tombent les **temps forts** ?
3. **Où chante-t-il** et où est-ce instrumental ?

Les réponses pilotent tout le reste : la boucle, la longueur des plans, le choix des
plans, et l'endroit où le glitch prend la main.

---

## 1. Récolter les entrées

| Entrée | Défaut si Tony ne précise pas |
|---|---|
| Le `.wav` | — obligatoire |
| Liens Higgsfield `/s/...` | — obligatoire |
| Durée cible | 2 min 30 |
| Titre du morceau | demander |
| Nom d'artiste | demander |
| CTA de fin | « abonne-toi » |
| Formats | **les deux** : 9:16 et 16:9 |

Le fichier envoyé arrive dans `~/.claude/uploads/<session>/`. Le copier dans
`<projet>/work/music.wav` avant de travailler dessus.

---

## 2. Résoudre les liens Higgsfield

`outils/resoudre-liens.mjs` — éditer la liste `LIENS` en haut, puis lancer.

⚠️ **La page `/s/<slug>` est une SPA.** Pas de `<video>`, pas de `og:video`, aucune méta.
Un `curl | grep mp4` renvoie les vignettes de la galerie voisine, pas le bon clip.

Ce qui marche : le payload TanStack est sérialisé dans le HTML et contient une référence
canonique `higgsfield.ai/share/<uuid>`. **C'est cet uuid qui identifie le clip**, et le
MP4 porte l'uuid dans son nom (`hf_<date>_<uuid>.mp4`).

Le MCP Higgsfield ne sert à rien ici : `show_generations` renvoie l'historique mais **pas
le slug de partage**, donc aucun moyen de faire le lien. Et sa sortie dépasse la limite de
contexte — si on doit vraiment l'appeler, la lire avec node sur le fichier de résultat.

---

## 3. Inventorier les plans — en REGARDANT

Étape non négociable et systématiquement sous-estimée. Sans elle, on met un plan de dos
sur un refrain.

```bash
for f in work/clips/c*.mp4; do
  n=$(basename "$f" .mp4)
  ffmpeg -v error -y -i "$f" -vf "fps=1,scale=150:-1,tile=10x1" -frames:v 1 "work/detail/$n.jpg"
done
```

Puis **lire chaque planche avec l'outil Read** et écrire, seconde par seconde :

- où sa **bouche bouge** (micro à la main, gros plan qui crie) → vivier CHANTÉ
- où c'est de la danse, une voiture, un insert → vivier INSTRU
- les plans **signature** à garder pour les temps forts (dans roule kiki : le chat dans
  le kart, la macro de l'orbe au doigt)

Pour un plan large en 16:9 dont on doit tirer un portrait, extraire quelques images avec
`drawgrid=w=64:h=1000` et **relever le décalage x extrait par extrait**. Cadrer au centre
coupe le micro ou la tête selon la seconde — vérifié.

---

## 4. Mesurer le morceau

```bash
ffmpeg -i work/music.wav -af "lowpass=f=160,aresample=1000"  -ac 1 -f s16le work/kick.raw
ffmpeg -i work/music.wav -af "pan=mono|c0=0.5*c0+0.5*c1,highpass=f=250,lowpass=f=4000,aresample=1000" -f s16le work/mid.raw
ffmpeg -i work/music.wav -af "pan=mono|c0=0.5*c0-0.5*c1,highpass=f=250,lowpass=f=4000,aresample=1000" -f s16le work/side.raw
node outils/analyser-audio.mjs && node outils/structure.mjs
```

**Détection de voix** : rapport MID/SIDE dans la bande 250–4000 Hz. La voix lead est mixée
au centre, les nappes et réverbs vivent dans les côtés. Ce n'est pas une séparation de
sources — c'est un détecteur de présence, suffisant pour placer des coupes.

**Trois pièges mesurés :**

- **Le BPM brut est du double-temps.** Les onsets comptent aussi les contretemps. Diviser
  par deux pour obtenir le pouls dansé. (166,7 relevé → 83,3 réel sur roule kiki.)
- **Le premier onset n'est pas le premier temps.** Sur roule kiki, l'onset tombait à
  0,130 s alors que les vrais temps forts sont sur `6,40 + 2,87·k` — 0,5 s d'écart, assez
  pour que tous les sauts d'écran tombent à côté. **Relever la grille sur les pics
  d'énergie, pas sur le premier onset.**
- **Le détecteur bascule à chaque respiration.** Sur un chant scandé, il produit une
  alternance de 1,2 s qui n'a aucun sens de montage. `structure.mjs` comble les trous plus
  courts qu'une mesure : ce qui survit est la vraie carte du morceau.

Toujours **tracer l'énergie par tranche de 0,1 s** avant de choisir un point de boucle :

```bash
ffmpeg -v error -ss T -t D -i work/music.wav -af "aresample=1000" -ac 1 -f s16le - \
| node -e 'let b=[];process.stdin.on("data",d=>b.push(d)).on("end",()=>{const x=Buffer.concat(b);
for(let s=0;s<Math.floor(x.length/2/100);s++){let e=0;for(let i=s*100;i<(s+1)*100;i++)e+=Math.pow(x.readInt16LE(i*2)/32768,2);
const db=10*Math.log10(e/100+1e-12);console.log((s*0.1).toFixed(1)+"s "+db.toFixed(0)+" "+"#".repeat(Math.max(0,Math.round(db+45))));}})'
```

---

## 5. La boucle musicale — jamais `-stream_loop`

`outils/audio.sh` (éditer `FIN` et `DEB2`).

**La musique s'arrête avant la fin du fichier.** Sur roule kiki : 78,88 s pour un fichier
de 80,84 s. Un `-stream_loop -1` naïf colle donc **deux secondes de silence au milieu du
clip**. Toujours localiser la dernière fenêtre au-dessus de −60 dB.

**Choisir le point de rentrée sur deux critères, pas un :**

1. **Phase de beat continue.** `(FIN − DEB2)` doit être un multiple entier du temps.
   Sinon tout le montage de la 2ᵉ moitié décroche du rythme.
2. **Énergie comparable.** Rentrer d'un refrain à −12 dB dans une intro creuse à −30 dB
   s'entend comme « la chanson a redémarré ». C'est l'erreur commise au premier essai sur
   roule kiki, corrigée en déplaçant la rentrée de 8,77 s à 7,835 s.

Fondu croisé de **60 ms**, pas plus : le transitoire de grosse caisse du temps fort le
masque entièrement. Un fondu long s'entend comme un fondu.

Finir par `loudnorm=I=-14:TP=-1.5:LRA=11` et **vérifier la crête** (`astats` avec
`-v info` — sans ça, rien ne s'affiche : ffmpeg écrit tout sur stderr).

---

## 6. Le montage image

`outils/edl.mjs` (à réécrire pour chaque clip) puis `outils/plan.mjs` pour LIRE le
montage avant de dépenser un rendu.

### Les deux règles qui viennent de la demande de Tony

> « la music doit suivre l'avatar quand il chante »

Sur un bloc CHANTÉ : **uniquement des plans où sa bouche bouge**. Jamais un plan de dos,
jamais une danseuse seule. Rien ne trahit plus vite un clip amateur que la voix qui
continue pendant qu'on regarde autre chose.

> « effets de saut d'écran stylé quand il ne chante pas »

Sur un bloc INSTRU : le montage passe au **demi-temps** et le traitement `saut` prend la
main. Le montage se resserre exactement là où il n'y a plus de voix à suivre.

### La durée des plans vient de la SOURCE, pas de la grille

Premier essai sur roule kiki : cases égales d'une mesure (2,87 s). Résultat lu dans
`plan.mjs` avant tout rendu : **26 plans sur 67 en ralenti, jusqu'à 0,48×**, parce que les
extraits chantés durent 1,1 à 1,6 s. Un ralenti à 0,5× sur une bouche qui chante fait
décrocher le playback — c'est immédiatement visible.

Donc l'inverse : la durée de la source décide, aimantée sur la grille rythmique la plus
proche. Vitesse résiduelle bornée à **[0,72 ; 1,00]** — un ralenti léger passe inaperçu et
flatte même une source générée ; en dessous, non.

- CHANTÉ → 3 à 6 demi-temps
- INSTRU → 2 à 4 demi-temps
- INTRO → 4 à 7 demi-temps (le carton titre doit avoir le temps d'être lu)

### Le parcours du vivier doit être PREMIER avec sa taille

Un `i % n` rejoue la même suite de plans dans le même ordre, et l'œil repère la boucle
avant la fin du refrain. Un pas fixe de 3 dégénère sur un vivier de 3 (toujours le même
plan). `plan.mjs` calcule le pas premier le plus proche de `n/2`, avec un garde-fou contre
la répétition immédiate.

**Vérifier avant de rendre** : `node outils/plan.mjs` imprime les répétitions immédiates,
les trous de timeline et les ralentis. Trois lignes de contrôle valent vingt minutes de
rendu.

---

## 7. Le rendu

`outils/rendre.mjs <format>` — un MP4 par plan, puis concaténation en copie de flux.

**Ne jamais construire un seul graphe de 109 plans** : une erreur dans le 84ᵉ fait perdre
le rendu entier. Un plan raté se refait seul, et le script saute les segments déjà rendus.

### Les deux formats sont une intention, pas un recadrage

- **9:16** : les clips portrait remplissent l'écran ; le clip 16:9 passe en bandeau sur
  fond flouté tiré de lui-même.
- **16:9** : exactement l'inverse — le clip 16:9 passe **plein cadre**, les portraits sont
  posés en panneau central. Les moments « live » s'ouvrent sur YouTube et se resserrent
  sur TikTok.

Recadrer un 9:16 en 16:9 coupe la tête ou les pieds à tous les coups. Mesuré sur les six
clips de roule kiki.

⚠️ **Le fond flouté doit rester lisible.** Premier essai : `gblur=sigma=42` +
`brightness=-0.24` — la première image du clip était noire aux deux tiers. Corrigé à
`sigma=30`, `brightness=-0.08`, et le bandeau tiré d'un recadrage **4:3** (810 px de haut)
plutôt que du 16:9 entier (608 px).

### Le saut d'écran

L'image se déplace d'un bloc à chaque temps et **y reste** — `floor(t/BEAT)` tient la
position pendant tout le temps. C'est un saut, pas une vibration.

```
crop=L:H:x='(iw-ow)*(0.5+0.42*sin(floor((t+OFF)/BEAT)*12.9+G))':y='…',
rgbashift=rh=18:bh=-18:enable='lt(mod(t+OFF,BEAT),0.12)',
eq=brightness=0.16:contrast=1.2:enable='lt(mod(t+OFF,BEAT*2),0.04)'
```

⚠️ **`OFF` est indispensable.** Dans un segment, `t` repart de zéro. Sans le report du
temps global (`(t0 − premier_temps) mod BEAT`), tous les sauts tombent à côté du beat.

⚠️ `rgbashift` n'accepte pas d'expressions sur ses valeurs — seulement `enable=`.
`colorlevels` provoque un SIGSEGV sur ce build : passer par `colorchannelmixer=aa=`.

---

## 8. Les cartons — Chromium, pas drawtext

⚠️ **`drawtext` n'existe pas sur ce build** (`ffmpeg -filters | grep drawtext` → 0). Aucune
incrustation de texte n'est possible côté ffmpeg.

`outils/cartons.mjs` rend des PNG transparents via Playwright. C'est mieux de toute façon :
lueur néon, crénage, interlettrage et calques sont natifs en CSS et illisibles en
paramètres drawtext.

- Polices en **base64 inline** depuis
  `/home/claude/.agents/skills/embedded-captions/modes/standard/fonts/files/`
  (anton, chakra-petch, audiowide, bangers…). Vérifier le chargement avec
  `document.fonts.check('172px Anton')` **et** en comparant la largeur au fallback — un
  `fonts.ready` qui résout ne prouve pas que la police est appliquée.
- Un fichier **par élément** (filet, titre, artiste, CTA) pour les faire entrer en décalé.
  Un carton unique entre d'un bloc, ce qui ne ressemble à rien sur un clip.
- Palette **relevée sur les clips eux-mêmes**, jamais choisie à part.

**Le titre sort avant la première phrase chantée.** Un carton encore à l'écran quand la
voix démarre vole l'attention au seul moment où on veut regarder sa bouche.

**Le CTA monte pendant le dernier refrain**, pas après : posé sur le silence final il n'a
plus de musique pour le porter.

---

## 9. L'assemblage final

`outils/finaliser.mjs <format>`.

La **ligne réactive** est la lecture littérale de « la music doit suivre l'avatar quand il
chante » : une onde `showwaves` tirée de la bande son elle-même, allumée uniquement
pendant les blocs chantés, éteinte pendant les breaks où le glitch prend le relais. Elle
n'est pas décorative — c'est la forme d'onde du fichier.

Composée en `overlay` après `colorchannelmixer=aa=0.62` : le noir de showwaves disparaît
de lui-même, sans détourage ni colorkey à régler.

### Les paroles au refrain — une passe par phrase, un `enable` par fondu

Les paroles sont des **PNG rendus par Chromium**, pas des sous-titres ASS : libass ne lit
pas le woff2 (donc pas d'Anton) et son `\blur` floute le contour uniformément, là où trois
`text-shadow` empilés donnent la profondeur d'un vrai tube au néon.

Deux pièges, tous les deux **silencieux** — ffmpeg réussit, code 0, aucun avertissement,
et l'écran est nu. Les deux ont coûté un rendu complet chacun.

**1. Ne jamais enchaîner les fondus d'une phrase qui revient.** `fade=t=in:st=X` rend
transparent tout ce qui précède X ; `fade=t=out:st=Y` tout ce qui suit. Avec plusieurs
apparitions, l'intersection est vide et **rien ne s'affiche nulle part**. Borner chaque
fondu à sa propre fenêtre — `fade` accepte le montage temporel :

```js
const w = `enable='between(t,${p.t0},${p.t1})'`;
`fade=t=in:st=${p.t0}:d=0.22:alpha=1:${w},fade=t=out:st=${(p.t1-0.28).toFixed(2)}:d=0.28:alpha=1:${w}`
```

**2. `box-sizing:border-box` dans le CSS du PNG.** Sans lui le `padding-bottom` s'ajoute
à la hauteur de 1920 px et l'alignement en bas pousse le texte **sous le cadre**.

**Le test qui sépare les deux, avant tout rendu long** — sortir l'alpha du PNG seul :

```bash
ffmpeg -v error -i phrase.png -vf "format=rgba,alphaextract,scale=54:96" \
  -f rawvideo -pix_fmt gray - | node -e '…lignes d alpha non nul…'
```

Alpha absent ou hors cadre → c'est le CSS. Alpha correct mais vidéo nue → c'est la chaîne
de filtres. Puis mesurer le blanc pur dans la bande de texte **pendant ET hors** fenêtre :
attendu ~6 % contre 0,00 %. Une seule fenêtre testée ne prouve rien — c'est la coexistence
de plusieurs qui casse.

---

## 10. Livraison

1. **Master** : CRF 20, `-movflags +faststart`. C'est le fichier à publier sur les réseaux.
2. **Copie web** : CRF 28, `-maxrate 2500k` → viser **moins de 50 Mo par format**.
   ⚠️ GitHub refuse au-dessus de 100 Mo et avertit au-dessus de 50.
3. **Publier sur previsualisation** dans une route dédiée, avec les deux formats côte à
   côte et le tableau de structure. Tony valide au téléphone.
4. **Ne jamais publier sur les réseaux sans accord explicite.**

Surveiller le disque : `/work` tourne souvent au-dessus de 95 %. Les dossiers de segments
(`work/seg916`, `work/seg169`) sont regénérables — les supprimer après concaténation.

---

## 11. Checklist avant de livrer

- [ ] La musique s'arrête bien à sa dernière note, pas au bout du fichier
- [ ] La jointure de boucle : phase de beat continue **et** énergie comparable
- [ ] `plan.mjs` : aucun trou de timeline, aucune répétition immédiate, aucun ralenti < 0,72
- [ ] Sur chaque bloc chanté, **sa bouche bouge** à l'image
- [ ] Les sauts d'écran tombent **sur** le temps (vérifier `OFF`)
- [ ] Le carton titre est sorti avant la première phrase chantée
- [ ] Les paroles apparaissent **à chaque** apparition prévue — mesurée, pas supposée
      (blanc pur ~6 % dans la fenêtre, 0,00 % hors fenêtre, sur au moins deux fenêtres)
- [ ] Durée finale = durée demandée, à la demi-seconde
- [ ] Les deux formats existent et sont sous 50 Mo en version web
- [ ] Crête audio ≤ −1,0 dB (`astats` avec `-v info`)

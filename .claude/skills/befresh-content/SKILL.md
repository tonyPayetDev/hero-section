---
name: befresh-content
description: BeFresh Events (@befresh.events, bar à jus détox / jus frais maison / mojito, La Réunion) — produit une vidéo sociale 9:16 ou un carrousel Instagram à partir d'une demande de la file n8n BeFreshQueue. Pipeline ffmpeg shot-list sur RUSHES RÉELS (pas d'images IA) + voix féminine preset WaveSpeed + captions ASS à la charte BeFresh (noir/or/magenta). À utiliser dès qu'on demande un contenu BeFresh, de traiter la file BeFresh, ou de produire un des 7 angles du dossier BEFRESH-7-ANGLES.md.
---

# befresh-content

**Client test gratuit de Tony.** Les 7 vidéos servent de vitrine pour attirer d'autres
restaurateurs — la qualité prime sur la vitesse. Ligne éditoriale : `/work/BEFRESH-7-ANGLES.md`
(à lire avant d'écrire quoi que ce soit, elle n'est pas résumable).

Distinct de `foodboost-vitrine-video` : **là-bas tout est généré par IA** (seedream → vidu →
HyperFrames, voix clonée de Tony, compte @foodboost). **Ici on monte des rushes réels du client**
avec un shot-list ffmpeg, une **voix féminine preset** (jamais celle de Tony), et la charte du client.
Ne pas confondre les deux, ils ne partagent que le fournisseur TTS.

---

## La niche, en une ligne

**Jus détox · jus frais maison · mojito.** Jamais « sans alcool » : cette formulation définit
par une absence et met en position de défendre. On définit par une présence.

## Charte BeFresh (vérifiée sur le lookbook officiel)

| Rôle | Valeur |
|---|---|
| Fond | noir |
| Accent principal | **or `#E0AE3A`** (ASS : `&H003AAEE0&`) |
| Accent de section | **magenta `#E9268C`** (ASS : `&H008C26E9&`) |
| Corps de texte | blanc |
| Police | Outfit |
| Handle | `@befresh.events` |

⚠️ Une v1 est partie en vert/orange — **ce n'était pas la charte**. Or + magenta, rien d'autre.

⚠️ **Le logo n'existe qu'en ~110 px** (`befresh-videos/befresh-01-decathlon/work/brand/befresh-asset.png`).
Utilisable en **marque de coin uniquement**, jamais en carton plein écran.
`logo-befresh-recree.png` existe mais **sa typographie est fausse** — ne pas s'en servir comme référence.

---

## Les 4 règles de non-régression (issues de l'analyse de 62 Reels + concurrents)

1. **Jamais de Reel sans légende.** 34 % des leurs n'en ont pas — c'est le gain le moins cher du dossier.
2. **Ne pas ouvrir sur le nom d'un client.** Format le plus faible, confirmé sur 3 comptes
   indépendants. Le client peut être cité **après la 3e seconde**.
3. **Ne pas faire de l'annonce d'événement le sujet principal** — 0,32 %, pire format mesuré.
4. **Ne pas viser les vues.** Leur Reel à 47 849 vues a le pire engagement du compte.

**N'invente jamais un plat, un prix, un horaire ou un jour de marché.** Si l'info manque, la
demande est bloquée : le dire, ne pas combler.

---

## Entrée : la file n8n

Formulaire client → `https://n7n.automatisationboost.com/form/befresh-contenu`
→ data table **BeFreshQueue** (`jRBrp1yG1IvMF4Pe`).

```bash
export PATH=/home/claude/tools/node/bin:$PATH
node scripts/queue.mjs list                       # tout voir
node scripts/queue.mjs next                       # la prochaine a_faire
node scripts/queue.mjs statut <request_id> en_cours
node scripts/queue.mjs statut <request_id> livre
```

Champs : `format` (Vidéo 9:16 | Carrousel Instagram), `angle` (1..7 ou « Laisser l'agent choisir »),
`produit`, `evenement`, `lieu`, `images`, `notes`.

Si `angle` = « Laisser l'agent choisir », prendre le premier angle de `BEFRESH-7-ANGLES.md`
encore non produit **et faisable avec les images disponibles** (1, 2, 4 et 5 démarrent sans rushes neufs).

---

## Pipeline vidéo (prouvé sur `befresh-01-decathlon`, 2 rendus)

Travailler dans `befresh-videos/befresh-NN-<slug>/`. Environnement obligatoire :

```bash
export PATH="/home/claude/tools/node/bin:$PATH:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static"
```

### 1. Écrire la narration
`narration.txt`, un seul souffle, ton chaleureux. Viser 22–30 s.
Pour l'écriture d'accroche, s'appuyer sur `hook-puissant-branded` et `script-pspc-branded`
— **mais transposés au client** : le CTA gaté par mot-clé est une mécanique Autoboost,
BeFresh appelle au commentaire simple ou à la visite d'un marché.

### 2. Voix — preset féminin, PAS le clone de Tony
```bash
node scripts/tts.mjs Vivian work/voice.mp3 narration.txt
```
Modèle `qwen3-tts/text-to-speech` (≠ `voice-clone`). Voix déjà utilisées : **Serena**, **Vivian**,
**Ono_Anna** — en prendre une nouvelle à chaque vidéo pour ne pas installer une fausse « voix de
marque ». Ceci contourne aussi le piège `voixUrl` du webhook `tts-gen` : on n'y touche pas.

Liste réelle acceptée par l'API : `Vivian, Serena, Ono_Anna, Sohee, Uncle_Fu, Dylan, Eric, Ryan…`
⚠️ **`Cherry` est refusé** malgré ce qu'on lit ailleurs. Côté voix féminines, après Serena, Vivian
et Ono_Anna, **il ne reste que `Sohee`** d'inédit : au-delà, il faudra assumer une reprise.

**Toujours mesurer la F0 du rendu** avant de livrer : le clone de Tony sort entre **114 et 133 Hz**.
Un preset féminin mesure 180-300 Hz. Si la mesure tombe dans la plage du clone, la requête est
partie sur la mauvaise branche — c'est un échec, on refait.

### 3. Timings mot-à-mot
```bash
node scripts/whisper.mjs "$(cat work/voice-url.txt)" work/whisper.json
```
`language: 'fr'` (code ISO) et `enable_timestamps: true`. Sur <20 s whisper renvoie souvent
**un seul segment** : dans ce cas, répartir les mots à la main au prorata des caractères
(c'est ce que fait `templates/gen-captions.example.mjs`).

### 4. Shot-list

**Sonder le rush AVANT d'écrire la shot-list.** Trois pièges déjà payés sur `befresh-03-evenementiel` :

1. **Le rush peut se terminer par le bumper logo du client** (fond noir, cercle or). Sur le rush
   événementiel il démarre à **81,5 s** : les trois montages lisaient jusqu'à 81,6-82,1 s, donc le
   dernier plan basculait sur le bumper du rush juste avant la carte de fin. Aucune erreur ffmpeg,
   rien dans les logs — ça ne se voit qu'en regardant. Établir une **limite propre** et s'y tenir.
2. **Le vrai logo est souvent dans le rush**, en bien meilleure définition que l'asset de marque
   (478 px contre 110 px). Chercher le bumper avant de se rabattre sur `befresh-asset.png`.
3. **Vérifier que deux plans ne réutilisent pas les mêmes frames source.** Croiser les intervalles
   `[ss, ss+dur]` par fichier source : six recouvrements sur un seul montage.

**Définition du rush.** Si le rush est déjà en 9:16 (WhatsApp livre du 478×850, ratio 0,5624 contre
0,5625), **ne pas l'encadrer** : les bandes rétrécissent une image déjà pauvre et mangent la zone
des sous-titres. Agrandissement lanczos plein cadre, **zooms plafonnés à ~1,09** (au-delà on étale
le flou), `unsharp` léger, grain fin. Le grain fait lire l'agrandissement comme « filmé » — il ne
crée pas de détail, et il faut le dire au client plutôt que de laisser croire à du 1080 natif.

**Sous-titres et images doivent être recroisés à la main.** Les temps de sous-titre viennent de
whisper, les temps de coupe de la shot-list : rien ne les aligne tout seul. Construire la table
« quel mot tombe sur quel plan » et corriger les contresens (« UNE SALLE » sur un bar de plage,
« JAUNE » sur un distributeur rouge). Trois trouvés sur un seul lot.

`src/shots.json` — `sources` (chemins des rushes), puis un objet par plan :
`{ id, src, ss, dur, spd, z0, z1, cx, cy, note }`.
`z0→z1` = punch-in / ken-burns, `cx/cy` = centre de la fenêtre en fraction.
Viser **~1 s par plan** : 24 plans pour 24 s.

```bash
node scripts/build-shots.mjs      # -> work/shots/*.mp4 puis work/video-silent.mp4
```
Chaque plan est upscalé en 2160×3840 avant `zoompan` (sinon ça bave), gradé « fresh food »
(saturation ~1.30), et le script **avertit si le nombre de frames rendu ≠ attendu** — ne pas ignorer.

### 5. Captions ASS à la charte
Copier `templates/gen-captions.example.mjs` → `src/gen-captions.mjs`, remplacer `SEGS`
(les segments whisper) et `CHUNKS` (`[segIdx, premierMot, dernierMot, taille, 'g'|'m']`).
Les captions restent à **≥330 px du bas** (zone Instagram) et le mot actif passe en or ou magenta.
Écrit `work/captions.ass` **et** `work/chunk-times.json` (utilisé par le mix audio).

### 6. Mix audio
```bash
node scripts/build-audio.mjs --voice work/voice.mp3 --bgm assets/bgm.mp3
```
Voix compressée, lit de musique **side-chain ducké** sous la voix, whoosh sur les cuts de section,
pop sur les mots d'impact, `loudnorm=I=-14` (norme réseaux).
Les temps de cut sont **recalculés depuis `shots.json`** — pas de tableau de frames en dur.
Musique : passer par `media-use` / Mixkit (Epidemic Sound est en download interdit ici).

### 6 bis. Variante beat-sync

**Mesurer le BPM sur la piste, jamais le lire dans le manifeste.** Sur `journal-*` le manifeste de
la bibliothèque annonçait 128 BPM, la mesure donne **130,00** — deux BPM d'écart, soit près d'une
demi-seconde de décalage accumulé en fin de montage.

Méthode qui a marché (`src/beatscan.mjs`, `src/beatgrid.mjs` du projet événementiel) : filtrage
40-140 Hz pour isoler le kick → courbe d'attaques → banc de peignes sur 60-190 BPM. Le bon pic est
celui **entouré de ses harmoniques** (130 → 65, 97,5, 162,5). Contrôler ensuite que les attaques
des 15 premières secondes retombent bien sur la grille, à ±un demi-temps près.

Sortir `{ bpm, periode, premierTemps }` et caler chaque coupe sur un multiple — pas « à peu près ».

### 7. Assemblage final
```bash
ffmpeg -i work/video-silent.mp4 -i work/audio-mix.m4a \
  -vf "ass=work/captions.ass" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a copy -shortest renders/befresh-NN.mp4 -y
```
Puis **regarder une frame** (`ffmpeg -ss 12 -i renders/... -frames:v 1 check.jpg` + Read) :
un rendu « réussi » avec des glyphes manquants reste inutilisable.

### 8. Prévisualisation
Publier sur `previsualisation.automatisationboost.com` (route dédiée par variante, ne jamais
écraser une précédente) et donner le lien — Tony valide au téléphone.

---

## Pipeline carrousel

Le carrousel n'a **pas** de chaîne prouvée : `DeiWnbqzJDYb9zE2` (Claude to Carrousel html to image)
et `egY1UJiKK9Vhcd5y` (LinkedIn Carousel) sont actifs mais **n'ont jamais tourné une seule fois**.
Ne pas les présenter comme fonctionnels sans les avoir fait tourner.

Chemin recommandé, entièrement local et vérifiable :
1. Une slide = un HTML 1080×1350 à la charte (noir / or / magenta / Outfit).
2. Rendu en PNG via `playwright-skill` (screenshot 1080×1350).
3. Vérifier chaque PNG par un Read **avant** toute publication.
4. Publication : uniquement après validation de Tony, jamais automatiquement.

Structure éditoriale : slide 1 = la prise de position (pas le nom du client), slides 2–5 = la
démonstration, dernière slide = la question ouverte. Légende obligatoire (règle n°1).

---

## Coûts et quotas

TTS + whisper ≈ quelques centimes par vidéo (WaveSpeed). **Aucune génération d'image/vidéo IA
n'est nécessaire** pour les angles 1, 2, 4 et 5 — les rushes et les 4 visuels mojito suffisent.
Crédits Higgsfield à **zéro** : cette voie est fermée. Kie.ai ≈ 424 crédits, à réserver aux cas
où il manque vraiment un plan.

## Assets

- `scripts/build-shots.mjs` · `scripts/build-audio.mjs` · `scripts/tts.mjs` · `scripts/whisper.mjs` · `scripts/queue.mjs`
- `templates/shots.example.json` (24 plans réels) · `templates/gen-captions.example.mjs` (charte + mot-à-mot)
- Rushes et visuels existants : `befresh-videos/` (`befresh-assets-mojito/` = 4 visuels fond noir)

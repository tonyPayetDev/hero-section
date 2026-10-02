---
name: face-cam-boost
description: FaceCam Boost — transforme un VRAI rush face caméra de Tony (pas l'avatar) en vidéo 9:16 motion design pro HyperFrames, à la charte AutomatisationBoost. Coupe les silences, accélère, transcrit mot à mot, puis habille avec le kit FaceCam Boost - écrans qui slident l'un après l'autre en haut, face cam qui change de forme (plein écran → cercle néon or/violet → rectangle empilé → split vertical → plein écran final), stickers punch (TROP LENT, ÇA MONTE, NIVEAU MAX…), puces NIVEAU, courbes, piles de cartes, CTA « commente MOT » avec champ commentaire tapé, Valse des fleurs sous la voix. Déclencheurs - "face cam boost", "habille ma face cam", "motion design sur ma vidéo", "rends ma vidéo pro", "mets ma vidéo en cercle néon", "écrans qui slident", Tony envoie un .mp4 où il parle face caméra et veut du motion design.
---

# FaceCam Boost

**Entrée :** un rush .mp4 où Tony parle face caméra (sa vraie voix).
**Sortie :** une vidéo 1080×1920, 30 fps, 25-40 s, motion design HyperFrames, prête à valider puis à planifier.

Ce skill assemble trois choses déjà éprouvées sur `autoboost-74-claude-md-sous-agents` :
la coupe façon yapping, le kit FaceCam Boost, et le contrat HyperFrames.

## À lire avant de produire

1. `autoboost-neon-videos/_shared/CHARTE.md` — palette, typo, CTA, pièges de rendu. **Aucun vert. Aucun emoji.**
2. `autoboost-neon-videos/_shared/facecam-boost-kit/README.md` — layouts, stickers, motions ; regarder `boards/*.png`.
3. Le skill `/hyperframes-read-first` (le CLAUDE.md l'impose pour tout travail vidéo) puis `/hyperframes-core` pour le contrat : `<video>` **enfant direct de la racine**, une timeline GSAP en pause, aucun `Math.random`.
4. L'implémentation de référence : `autoboost-74-claude-md-sous-agents/motion/gen.py` + `template.html`. **Partir de là**, ne pas réécrire de zéro.

## Workflow

### 0 · Outils
```bash
source .claude/skills/face-cam-boost/scripts/env.sh   # ffmpeg, faster-whisper, Chrome headless shell
```

### 1 · Transcrire, corriger, couper
```bash
S=.claude/skills/face-cam-boost/scripts
python3 $S/facecam_cut.py take.mp4 --work build/ --stage transcribe     # imprime segment:index:mot
# écrire build/fixes.json : noms propres, jargon (CLAUDE.md, Opus, n8n...), "commande token" -> "Commente TOKEN"
python3 $S/facecam_cut.py take.mp4 --work build/ --stage plan --fixes build/fixes.json
python3 $S/facecam_cut.py take.mp4 --work build/ --stage cut
```
- Coupe sur tout silence > 0,55 s, `atempo` 1,14 par défaut (25-40 s visés). Ajuster `--tempo` si la durée sort de la fenêtre.
- Un mot douteux (un nom propre surtout) : le ré-isoler et le repasser avec un prompt de contexte ; s'il reste douteux, **le signaler à Tony** au lieu de deviner.
- Le **mot-clé CTA** est souvent dit (« commente X ») : le chercher dans la transcription, Whisper l'écrit mal.
- Sorties : `plan_actual.json` (timeline réelle au mot près — c'est elle qui pilote captions et apparitions), `facecam.mp4` (muet, keyframe chaque seconde), `voice.wav`.

### 2 · Storyboard (dans la conversation)
Un écran par idée, 4 à 6 s chacun, et dans chaque écran **un changement toutes les 2-4 s** (règle yapping).
Structure qui marche : hook plein écran → problème → vraie question → solution → mécanisme → erreur à éviter → objectif → CTA → finale plein écran.

Pour chaque écran choisir : layout de la face cam, motion Notion, sticker, valeurs affichées.

| Moment | Layout face cam | Motion du kit | Sticker |
|---|---|---|---|
| Hook | plein écran (L4) + titre métal/or + chips | typo kinetic | ÇA PART |
| Problème | cercle néon (L1) | courbe #3, tuiles, tampon rouge | rouge (TROP LENT, ÇA BLOQUE) |
| Question / avant-après | rectangle empilé ou **split vertical (L2)** | pile #5, cartes OPUS vs LÉGER | PLUS CLAIR, DÉJÀ MIEUX |
| Solution | cercle | fenêtre code tapée, recherche #2 | BON SYSTÈME |
| Mécanisme | cercle | nœuds reliés (workflow) | PLUS SIMPLE, AUTOMATISE ÇA |
| Résultat | rectangle (L3) | jauges, coches, zoom tuile #4 | ÇA MONTE, GAIN TEMPS |
| CTA | grand cercle | bouton → champ #1, mot élastique #7 | NIVEAU MAX |
| Finale | plein écran (L4) | punchline + trait violet | — |

**Règle absolue : aucun chiffre inventé.** Une stat affichée vient de ce que Tony dit. Sinon : jauge sans pourcentage, ou rien.

### 3 · Composer
Copier `autoboost-74-.../motion/` dans le nouveau projet (`autoboost-NN-sujet/motion/`), puis dans `gen.py` :
- `facecam_mode()` du kit pour chaque layout, `MORPHS` pour les transitions (0,5 s, power3.inOut) ;
- `B` = bornes des écrans ; un écran = `section.screen.clip` qui slide de la droite, traînée de vitesse à chaque changement ;
- stickers et puces NIVEAU **hors** des écrans (ils chevauchent la jointure écran / face cam) ;
- textes et timings depuis `plan_actual.json`.

```bash
python3 gen.py && npx hyperframes lint public          # 0 erreur exigé
npx hyperframes snapshot public --at <un instant par écran + chaque transition> --no-end
```
**Regarder chaque planche.** Pièges déjà rencontrés : espace mangé autour du mot actif (pas de `scale` sur le mot), tête coupée dans le cercle (remonter `focus`), classe générique (`.qb`) qui donne un halo à une boîte 1080×980, carte du dessous de la pile qui laisse voir son texte.

### 4 · Rendre, mixer
```bash
npx hyperframes render public -o silent.mp4 --fps 30 --quality delivery --no-browser-gpu   # ~7 min / 40 s en cloud
python3 $S/facecam_audio.py --voice build/voice.wav --events events.json --frames <nb images> --out mix.wav --bed valse
ffmpeg -i silent.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest final.mp4
```
- Musique par défaut : **Valse des fleurs, version maison évidée** (le script boucle la partie stable mesure 6 → 26). `--bed drums` pour un sujet plus nerveux. `--bed-file` quand la vidéo montre un clip avec sa propre musique.
- `events.json` : un SFX par slide (whoosh), tampon (impact), sticker (thwip/pop), coche (confirm), CTA (impact-deep, click, notify).
- Cible : −15 à −16 LUFS intégrés. Vérifier l'image **dans le MP4 final**, pas seulement les snapshots.

### 5 · Livrer
- Publier sur prévisualisation, attendre « ✅ » de Tony.
- **Mot-clé CTA** : vérifier qu'une porte Blotato existe (`blotato_list_automations`). Sinon la créer **avec l'accord de Tony** et l'URL de la ressource — sans porte, les gens commentent et ne reçoivent rien.
- Planifier sur les 5 réseaux (TikTok 36488 / IG 54617 / YouTube 45006 / FB 43538 + pageId / LinkedIn 25882).

## Variante « clip mis en avant »

Quand Tony montre un résultat, par exemple un clip généré par un outil IA, et que la face cam parle de ce résultat.
Référence : `autoboost-76-motion-sur-mon-son/` (`clip_track.py` + `motion/gen.py`).
- `clip_track.py` découpe le clip sur la timeline de la coupe, image et son ensemble. Chaque bloc montre le passage qui lui va. Faire finir la finale sur l'image où commence le hook, pour que la boucle soit invisible.
- Hook et finale : le clip en plein écran, Tony en **PiP cercle néon** (`facecam_mode` sur une boîte 420×420, `#pip-ring`). Écrans de preuve : le clip rangé dans un cadre téléphone qui suit les écrans.
- La musique du clip devient la nappe : `facecam_audio.py --bed-file clip_song.wav --bed-gain -13`. Elle est posée telle quelle, à niveau fixe et ducée, sans boucle ni fondu.
- Pour une timeline d'écran, utiliser la **vraie** forme d'onde du passage (enveloppe RMS du wav). Placer les coupes et keyframes sur ses attaques, et une tête de lecture calée sur ce qui joue.

## Mode dialogue — Tony + son avatar IA

Quand Tony envoie une session `/tournage/` avec un script balisé `[MOI]` / `[IA]` (« fais intervenir mon avatar IA »).
Il a lu **tout** le script au prompteur, répliques IA comprises. Ces passages sont retirés de sa piste,
puis remplacés par l'avatar (banque BUREAU, plages lèvres actives) et sa **voix clonée**.
Référence complète : `autoboost-75-skill-arena/` (script, gen.py, rendu).

```bash
python3 $S/facecam_cut.py take.mp4 --work build/ --stage transcribe      # transcript.json mot à mot
python3 $S/facecam_dialogue.py --src take.mp4 --script script.md --work build/ --stage align   # vérifier le tableau imprimé
python3 $S/facecam_dialogue.py --src take.mp4 --script script.md --work build/ --stage tts     # voix clonée, F0 contrôlé
python3 $S/facecam_dialogue.py --src take.mp4 --script script.md --work build/ --stage build   # build/asm/{tony,avatar}.mp4, voice.wav, timeline.json
```
- **Ignorer les horodatages des repères** du prompteur : ils dérivent de plusieurs secondes. Seul l'alignement script ↔ transcription fait foi.
- Une réplique IA « non entendue » (Tony l'a sautée) est quand même générée et posée après la réplique précédente.
- Une note `accélération` sur un bloc `[MOI — …]` l'accélère (`--fast`, 1,18 par défaut, contre `--tempo` 1,10 ailleurs).
- TTS : pas de guillemets droits dans le texte (le webhook injecte le texte brut dans du JSON). Un F0 autour de 200 Hz signifie que le repli OpenAI a répondu, pas le clone : le script relance l'appel. Chaque réplique coûte un peu de crédit WaveSpeed.
- Composition : partir de `autoboost-75-skill-arena/motion/gen.py`. Pendant une réplique IA, Tony est figé et assombri. La carte avatar arrive à droite ou à gauche en alternance, la première en glitch. Une bulle affiche la réplique mot à mot et un sticker répond à la vanne.
- Durée : le script de Tony fait foi (autoboost-75 dure 108 s). La fenêtre 25-40 s ne s'applique pas à ce mode.

## Checklist
- [ ] Durée 25-40 s, aucun battement > 4 s sans changement
- [ ] Hook plein écran dans les 2 premières secondes, promesse avant 5 s
- [ ] Captions mot à mot justes (noms propres vérifiés), mot actif or, mots-clés violet
- [ ] Aucun chiffre inventé, aucun vert, aucun emoji
- [ ] `hyperframes lint` : 0 erreur ; planches regardées écran par écran
- [ ] Voix au premier plan, nappe à niveau fixe dessous, −15/−16 LUFS
- [ ] Mot-clé CTA = porte Blotato active

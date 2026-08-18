---
name: horror-beatsync-video
description: Autoboost Horror Beat-Sync — monte une vidéo sociale 9:16 calée sur la trend "YOU CAN ASK THE FLOWERS (HORROR MIX)". Grille mesurée sur le fichier (drop à 2,34s, mini-drops toutes les 8,02s, beat 0,50125s), voix TTS générée clip par clip et posée sur chaque drop, ducking musique/voix, captions allouées en beats entiers. À utiliser dès qu'une vidéo doit être montée sur ce son de trend, ou quand la demande mentionne horror mix / beat-sync / cut sur le drop.
---

# horror-beatsync-video — Autoboost × trend horror

**Input :** un rush talking-head (voix incluse) ou une compo HyperFrames, + un des 3 scripts (ou un script maison)
**Output :** MP4 1080x1920, 34,42s max (fin sur un mini-drop), musique de trend en fond avec ducking, cuts calés sur les mini-drops

Ce skill est le **cousin beat-driven de `veille-to-video`** : même marque, même palette, même CTA
« commente le mot X », mêmes règles captions/avatar. La différence tient en une phrase : **ici c'est
la musique qui dicte le montage**, pas la narration. Toute la grille temporelle ci-dessous est
non négociable — c'est ce qui fait que la vidéo « colle » à la trend.

Pour tout ce qui n'est pas le beat-sync (consentement voix clonée, WaveSpeed/webhooks TTS,
environnement de rendu HyperFrames, pièges fontconfig/emoji/`-webkit-text-stroke`, publication
Blotato, mise à jour du Sheet), **lire `.claude/skills/veille-to-video/SKILL.md`** — ces règles
s'appliquent telles quelles et ne sont pas dupliquées ici.

---

## 1. Le son

```
https://assets.automatisationboost.com/music/YOU%20CAN%20ASK%20THE%20FLOWERSYOU%20CAN%20ASK%20THE%20FLOWERS%20(HORROR%20MIX).mp3
```

Vérifié en ligne le 2026-07-16 (HTTP 200, `audio/mpeg`, 2 359 525 octets, Cloudflare `max-age=14400`).
Le nom de fichier contient bien le titre **dupliqué** (`FLOWERSYOU CAN ASK THE FLOWERS`) — ce n'est pas
une faute de frappe, c'est le vrai nom sur le bucket. Toujours encoder les espaces (`%20`) et les
parenthèses passent telles quelles.

Télécharger une fois puis retirer toute pochette embarquée avant usage :

```bash
curl -sL -o /tmp/flowers_raw.mp3 "https://assets.automatisationboost.com/music/YOU%20CAN%20ASK%20THE%20FLOWERSYOU%20CAN%20ASK%20THE%20FLOWERS%20(HORROR%20MIX).mp3"
ffmpeg -y -i /tmp/flowers_raw.mp3 -vn -c:a copy assets/flowers_horror.mp3   # -vn = pas de cover art parasite
```

## 2. La grille (MESURÉE sur le fichier — corrigée le 2026-07-16)

⚠️ **Les valeurs de l'analyse librosa d'origine étaient fausses sur la phase.** Mesuré sur le vrai
MP3 (enveloppe d'énergie, front de montée le plus raide dans une fenêtre ±1,2s autour de chaque
drop supposé) : **les 7 drops testés tombent tous 0,56 à 0,70s AVANT** ce qu'annonçait le doc
(3s→2,32 / 11s→10,34 / 19s→18,30 / 27s→26,36 / 35s→34,36 / 43s→42,34 / 51s→50,44).
La *structure* était juste (période 8,02s mesurée vs 8s annoncé), c'est le point de départ qui
était décalé. Caler la révélation sur 3s la met **0,65s après le drop** — visible.

| Élément | Valeur |
|---|---|
| Durée | 96,68s |
| Période de phrase | **8,02s** (mesurée) |
| **Drop principal** | **2,34s** (et non 3s) |
| Mini-drops | **2,34 / 10,36 / 18,38 / 26,40 / 34,42 / 42,44…** (`2.34 + k × 8.02`) |
| Creux d'énergie (respiration) | ~0,2s avant chaque drop (2,15 / 18,15…) |
| Beat déduit | 8,02 / 16 = **0,50125s** → ~119,7 BPM |

Le BPM de 117,5 / beat 0,511s du doc d'origine **n'est pas confirmable** : ce morceau n'a pas de
beat percussif net, et le scoring de grille ne départage aucun candidat entre 104 et 124 BPM
(scores 0,31-0,36, tous équivalents). Le seul ancrage fiable est **la grille de drops mesurée
ci-dessus** ; le beat s'en déduit (une phrase = 16 beats). Ne pas réintroduire 0,511s : sur 4
phrases il dérive de 0,65s.

Refaire la mesure sur un autre morceau plutôt que de recopier ces chiffres :
`tts/analyze.cjs` / `tts/env2.cjs` du projet `autoboost-35-claude-mem` font ça en Node pur
(pas de librosa, pas de python dans ce sandbox) — décodage `ffmpeg -f s16le`, enveloppe RMS
par trames de 20ms, front le plus raide autour de chaque drop supposé.

**Les trois règles de montage :**

1. **Changement de plan à chaque mini-drop** (`2.34 + k × 8.02`), et **pulse du néon jaune tous les
   2,673s** (le tiers de phrase — voir §4). Pas de zoom plein écran : ça n'existe dans aucune autre
   vidéo Autoboost.
2. **Un mot surligné à chaque beat** — grille `t = 2.34 + n × 0.50125`.
3. **La révélation visuelle tombe pile sur le drop (2,34s)**, jamais avant, jamais après.

Les vrais hits mesurés du morceau (les coups que l'oreille compte) : **2,68 / 4,90 / 7,89 / 10,42 /
12,64 / 15,61 / 18,60s** — écart moyen 2,65s, d'où la grille de pulse à 2,673s.

Découpage canonique d'une vidéo de ~34s : `0-2.34 / 2.34-10.36 / 10.36-18.38 / 18.38-26.40 / 26.40-34.42`.
La vidéo se termine sur un mini-drop → **34,42s**, pas 35s.

## 3. Montage FFmpeg (rush talking-head)

Rush `rush.mp4` (voix incluse) + le son → 9:16, pulse de zoom sur le beat, ducking automatique :

```bash
ffmpeg -y -i rush.mp4 -i assets/flowers_horror.mp3 -filter_complex "\
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,\
zoompan=z='1.06-0.06*mod(on+4.99,15.04)/15.04':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30[v];\
[1:a]volume=0.09,atrim=0:34.42[m];\
[m][0:a]sidechaincompress=threshold=0.03:ratio=10:attack=15:release=250[duck];\
[0:a][duck]amix=inputs=2:duration=first:dropout_transition=0[aout]" \
-map "[v]" -map "[aout]" -t 34.42 \
-c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p \
-c:a aac -b:a 192k -ar 44100 -movflags +faststart output_beatsync.mp4
```

- `15.04` frames = 0,50125s × 30 fps, et `+4.99` est le **décalage de phase** qui cale le punch sur le
  premier beat réel de la grille mesurée (0,335s) au lieu de t=0. Sans lui le pulse tombe à côté de
  chaque beat — au-dessus du seuil perceptible, la vidéo sonne « à côté » de la trend.
  (Les anciennes valeurs `15.33`/`+10.56` dérivaient du beat 0,511s / premier beat 0,67s du doc
  d'origine, tous deux corrigés — voir §2.)
  **Si le projet n'est pas en 30 fps, recalculer les deux** :
  ```bash
  node -e 'const f=30, BEAT=8.02/16; let b=2.34; while(b-BEAT>=0) b-=BEAT;
  const per=BEAT*f; console.log("per =",per.toFixed(2),"| offset =",((per-((b*f)%per))%per).toFixed(2))'
  ```
  Résidu attendu après correction : < 1 frame (quantification, incompressible).
- Le `sidechaincompress` fait baisser la musique quand la voix parle, mais **il ne fait que ~-4 dB** :
  c'est `volume=0.09` qui place la musique sous la voix, pas le ducking. Le ducking affine, il ne
  sauve pas un mix trop fort. **`volume=0.9` (un seul chiffre d'écart) met la musique +7 dB AU-DESSUS
  de la voix** — erreur mesurée sur un vrai rush, la voix devient inaudible. `0.09` = la valeur maison,
  la même que le `data-volume` de la piste bgm côté HyperFrames.
- `atrim=0:34.42` coupe le son sur le mini-drop de fin ; pour une vidéo plus courte, couper sur un mini-drop,
  jamais au milieu d'une phrase musicale (mini-drops : 10.36 / 18.38 / 26.40).

**Variante multi-plans (PLAN A écran / PLAN B produit)** : découper les rushs en segments alignés sur
la grille, chaque nouveau plan démarre pile sur un mini-drop.

```bash
ffmpeg -y -i planA.mp4 -ss 0 -t 2.34 -c copy seg1.mp4    # montée
ffmpeg -y -i planA.mp4 -ss 2.34 -t 8.02 -c copy seg2.mp4  # drop
ffmpeg -y -i planB.mp4 -ss 0 -t 8.02 -c copy seg3.mp4
# … puis concat filelist.txt, et repasser la commande ci-dessus pour la musique + ducking
```

`-c copy` coupe au keyframe le plus proche, pas à la frame exacte : **vérifier la durée réelle de
chaque segment avec `ffprobe` avant de concaténer**, sinon le décalage cumulé désaligne tous les
mini-drops suivants. Si un segment dérive, réencoder ce segment (`-c:v libx264 -crf 18`) au lieu de
`-c copy`.

## 4. Version HyperFrames (compo authorée plutôt que rush)

Même grille, exprimée en `data-start`/`data-duration` :

| Scène | `data-start` | `data-duration` |
|---|---|---|
| Intro / montée | 0 | 2.34 |
| Drop — révélation | 2.34 | 8.02 |
| Phrase 2 | 10.36 | 8.02 |
| Phrase 3 | 18.38 | 8.02 |
| Phrase 4 / CTA | 26.40 | 8.02 |

**La voix TTS ne respecte pas la grille toute seule.** Un seul MP3 continu pose les mots où il
veut : la narration ne « respire » pas dans les creux et rien ne retombe sur un drop. La méthode
qui marche (projet `autoboost-35-claude-mem`) : **générer un clip TTS par phrase**, puis les poser
chacun à son mini-drop avec `adelay` —
`[1:a]adelay=2340|2340[a1]; … amix=inputs=5:normalize=0` (`normalize=0` sinon `amix` divise le
volume par le nombre d'entrées et la voix devient inaudible).

Deux pièges vérifiés sur les clips WaveSpeed :
- **~0,5s de silence de padding en tête de chaque clip.** Non retiré, le mot tombe un demi-beat
  après le drop et le clip déborde de son slot. Le trim est obligatoire :
  `silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.02,areverse,silenceremove=…,areverse`.
- **Mesurer chaque clip après trim** (`ffprobe`) et le comparer à son slot de 8,02s. S'il déborde,
  **resserrer le texte et régénérer** — jamais d'`atempo` (ça s'entend). Compter ~20 mots par
  phrase de 8s ; à ~3,3 mots/s ça fait ~6s de parole et ~2s de respiration dans le creux.

- `<audio id="bgm" src="assets/flowers_horror.mp3" data-start="0" data-duration="35" data-volume="0.09">`
  — **`id` obligatoire** sur chaque piste, sinon elle est silencieuse dans le rendu (piège documenté
  dans `veille-to-video`). Pas de sidechain côté HyperFrames : garder `#voice` à `1` et le `#bgm` bas.
- Captions : grille `t = 2.34 + n × 0.50125`. **Le webhook `avatar-webhook-v2` renvoie
  `transcripts: []`** (vérifié sur 6 appels le 2026-07-16, comme sur autoboost-34) — il ne faut donc
  pas compter sur les timestamps Whisper. À défaut : répartir les groupes sur la **durée réelle du
  clip** (mesurée après trim), proportionnellement au nombre de caractères, puis snapper sur la grille.
- **Allouer les captions en BEATS ENTIERS, minimum 1 beat chacune.** En snappant des bornes
  flottantes, deux groupes voisins atterrissent sur le même beat, et le garde-fou anti-chevauchement
  en écrase un : la caption sort avec `data-s == data-e`, elle apparaît et disparaît dans la même
  frame. Vécu sur #35 — c'est le mot-clé du CTA (`MÉMOIRE`) qui était invisible, le pire endroit
  possible. Voir `tts/caps.cjs` du projet `autoboost-35-claude-mem` : plancher d'1 beat par groupe,
  le reste distribué au plus en retard sur son idéal, puis **assert** `durée < 1 beat == 0` et
  `chevauchements == 0` avant d'injecter.
- **Le pulse néon jaune, pas un zoom plein écran.** Retour de Tony (2026-07-16) : un zoom punch sur
  `#root` n'existe dans aucune autre vidéo Autoboost et jure avec le reste. Ce qui marque le beat,
  c'est **l'anneau jaune de l'avatar qui flashe** (+ un halo radial derrière). Période = **le tiers de
  phrase, 8.02/3 = 2.673s** — c'est ce que l'oreille compte comme « toutes les 3 secondes », et un
  pulse sur trois retombe pile sur un mini-drop. **Ne pas prendre 3.000s pile** : ça dérive de 0,33s
  par pulse et finit 2s à côté de la musique en fin de vidéo.
  ```js
  const PULSE = []; for (let t = 2.34; t <= FIN; t += 8.02/3) PULSE.push(+t.toFixed(3));
  const inBroll = (t) => BROLL.some(([a, b]) => t >= a - 0.3 && t < b);   // l'avatar y est masqué
  PULSE.filter(t => !inBroll(t)).forEach((t) => {
    tl.fromTo("#avatar-ring", { opacity: 0.95, scale: 1.14 },
      { opacity: 0, scale: 1, duration: 0.62, ease: "power2.out", immediateRender: false }, t);
  });
  ```
- **`immediateRender: false` est OBLIGATOIRE** dès qu'il y a plusieurs `fromTo` sur le **même**
  élément. Par défaut GSAP applique l'état « from » de CHAQUE fromTo dès la création de la timeline :
  l'anneau reste alors allumé en continu et **aucun pulse ne ressort** — le rendu part quand même,
  il est juste faux. Vécu sur #35, coûté un rendu de 11 min.
- **Vérifier le pulse au chiffre, pas à l'œil** : mesurer la luminosité d'une **couronne** autour de
  l'avatar (`crop` centré, exclure le disque central), à `t` et à `t-0.35s`. Piège de la mesure
  elle-même : l'anneau pulse à `scale 1.14`, donc une couronne trop étroite (`r < 24` sur une grille
  de 48px) le rate et fait croire à un pulse mort — prendre `16 < r < 30` sur 60px.
- Attention à l'addition flottante (`3 + 8 = 11` est sûr, mais tout timestamp dérivé de beats ne l'est
  pas) — `validate` lève `StaticGuard: Invalid HyperFrame contract` sur un chevauchement de 1e-15.
  Fix : raccourcir de 0,01s le clip qui déborde.

## 5. Les 3 scripts prêts

`references/scripts-horror.md` contient les 3 scripts déjà calés sur la grille :

1. **Le restaurant fantôme** — HoReCa, ton horreur assumé, CTA `AUTO`
2. **La tâche qui te hante** — universel PME, pas de CTA mot-clé (question ouverte en commentaire)
3. **L'IA qui travaille la nuit** — Claude/agent, CTA `NUIT`

Les lire avant d'en écrire un nouveau : le rythme (une idée courte par phrase de 8s, demi-souffle
juste avant chaque mini-drop) est ce qui fait tenir le format.

Si le script vient du Sheet de suivi de `veille-to-video`, **ne pas réutiliser son découpage tel quel** :
ce pipeline-là vise 25-35s de narration continue à ~3,3 mots/s ; ici la narration doit **respirer dans
les creux** (10, 18, 26s). Compter ~24-26 mots par phrase de 8s, pas 8 × 3,3 = 26 collés bord à bord.

## 6. Checklist tournage

- Parle **sur le rythme** : une idée courte par phrase de 8s, demi-souffle juste avant chaque mini-drop.
- Volume musique final : ~-16 dB sous la voix (le ducking de la commande gère).
- **Sur TikTok/IG** : ajouter le son officiel dans l'app à **volume 1-5 %** par-dessus, pour être
  référencé sur la trend — la version mixée porte le vrai audio. C'est l'étape qui fait exister la
  vidéo dans la trend ; ne pas la sauter, et **ne pas la faire à la place de l'utilisateur** : elle se
  fait à la main dans l'app, après upload.
- Captions : style habituel noir/`#FFD700`, mot courant surligné, snap sur la grille 0,50125s.

## Checklist finale

- [ ] Musique téléchargée + `-vn` (pas de cover art parasite)
- [ ] Révélation visuelle pile à 2,34s (le drop MESURÉ, pas les 3s du doc d'origine)
- [ ] Un cut sur chaque mini-drop (2.34, 10.36, 18.38, 26.40, 34.42s) — vérifié à la frame
- [ ] Pulse du néon jaune tous les 2,673s, mesuré sur une couronne (pas à l'œil), avec
      `immediateRender: false` sur chaque `fromTo`
- [ ] Sound design : impact sub sur les drops, glitch sur les cuts, riser avant le CTA
      (pas les whoosh/chime de `veille-to-video` — Tony les a explicitement écartés)
- [ ] Design texte aligné sur les autres vidéos : punch 132px, mot du CTA 150px, lignes 76px.
      Une barre de texte barré se fait en `scaleX` sur `width: calc(100% + 20px)`, jamais en
      largeur fixe en px (elle ne couvre plus le texte dès qu'on change la taille de police)
- [ ] Captions snappées sur `2.34 + n × 0.50125`, allouées en beats ENTIERS (aucune avec data-s == data-e)
- [ ] Mix vérifié **au chiffre, pas à l'oreille** : la musique doit finir ~10-16 dB SOUS la voix.
      Extraire les stems et mesurer — un `+` dans la dernière colonne = musique au-dessus de la voix,
      donc mix cassé :
      ```bash
      ffmpeg -y -i rush.mp4 -i assets/flowers_horror.mp3 -filter_complex \
        "[1:a]volume=0.09,atrim=0:35[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=10:attack=15:release=250[d]" \
        -map "[d]" /tmp/m.wav
      ffmpeg -y -i rush.mp4 -map 0:a /tmp/v.wav
      for s in /tmp/m /tmp/v; do ffmpeg -hide_banner -i $s.wav -af volumedetect -f null - 2>&1 | grep mean_volume; done
      ```
- [ ] Durée ≤ 34,42s, coupée sur un mini-drop
- [ ] Palette noir mat + jaune/violet/orange (règles `veille-to-video`)
- [ ] Frames extraites et regardées après rendu (le texte peut être invisible — piège fontconfig)
- [ ] Compte Blotato confirmé avec l'utilisateur avant publication
- [ ] Rappelé à l'utilisateur d'ajouter le son officiel à 1-5 % dans l'app

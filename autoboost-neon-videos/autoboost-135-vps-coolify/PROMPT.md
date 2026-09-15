# autoboost-135-vps-coolify — recette de reproduction

Pipeline **v3** (assemblage banque avatar, pas de génération IA d'image/vidéo — donc pas de
prompt Seedance/Higgsfield à fournir ici). Ce fichier documente la recette complète pour
refaire ou décliner cette vidéo, comme l'exige `FICHE-VIDEO.md`.

## Source

Ligne 137 (`row_number`) du Sheet de suivi `10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags`,
onglet `30 Videos` (colonne `#` = 135, ne pas viser par elle : décalée d'une unité). Lue via
le workflow n8n `IUORhoZ4qt3s8PjT` ("TEMP - Read 30 Videos Sheet") car `docs.google.com` est
bloqué par la politique réseau de ce sandbox cloud (confirmé : `CONNECT tunnel failed, 403`).

- **Sujet** : VPS + Claude Code + Coolify — 3 étapes pour héberger soi-même ses automatisations
- **Mot-clé CTA** : `TERMINAL`

## Script voix (texte intégral envoyé au TTS, non reformulé)

```
VPS à cinq euros par mois, Claude Code et Coolify : trois étapes pour héberger toi-même toutes
tes automatisations, sans agence et sans y retoucher après. Coolify installe et met à jour tes
applications sans configuration à la main, Claude Code branché en MCP pilote tout depuis un
simple terminal, et tes workflows n8n, tes sites clients et tes vidéos tournent vingt-quatre
heures sur vingt-quatre, même ordinateur éteint. Compte entre trois et sept heures pour tout
monter la première fois, ensuite c'est fini, tu n'y touches quasiment plus. C'est exactement le
setup que j'utilise pour mes propres automatisations. Si tu es freelance et que tu veux arrêter
de payer un hébergeur cher chaque mois, suis-moi et commente le mot TERMINAL, je t'envoie le
guide complet gratuitement.
```

Généré via un workflow n8n one-off créé pour cette session (`t5wLFbzqXfhxq300`, "[Oneoff] Gen
Voice - Autoboost 135 VPS Coolify") qui POST `avatar-webhook-v2`, `voixUrl` =
`https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3` (voix clonée, consentement
permanent déjà donné). `transcripts: []` en retour (quota OpenAI Whisper épuisé côté compte Tony,
même symptôme déjà documenté sur `autoboost-101-triage` et `autoboost-99-soustitre-descript`) →
**timing mot-à-mot estimé manuellement** : pauses de phrase ancrées sur `silencedetect -40dB`
mesuré sur le MP3 brut (15 coupures nettes, correspondance 1:1 avec les 14 groupes de ponctuation
du script), puis répartition intra-segment par pondération longueur de mot + bonus ponctuation
(+5 mot finissant par `.`/`:`, +3 par `,`), **pas de vrai timestamp Whisper sur cette vidéo**.

Le MP3 CloudFront renvoyé par WaveSpeed (`voiceUrl`) n'est pas accessible en direct depuis le
shell sandbox (`curl` → `403 CONNECT tunnel failed`, confirmé, `n7n.automatisationboost.com` et
`assets.automatisationboost.com` bloqués eux aussi). Relayé via un second workflow n8n one-off
(`3s2Z6byWEUsXWbs7`, "[Oneoff] Download Voice - Autoboost 135 VPS Coolify") : `HTTP Request` en
`responseFormat: file`, puis un node `Code` (`this.helpers.getBinaryDataBuffer`, le binaire n8n
est stocké par référence sur cette instance — lire `binary.data.data` directement renvoie
l'identifiant de fichier, pas les octets) qui découpe en chunks base64 de 50 000 caractères
(8 chunks pour 281 304 octets), récupérés via `get_execution` et réassemblés côté shell.

MP3 brut : **38.328 s**. Post-traitement : `silenceremove` tête+queue (`-45dB`, peak) +
`atempo=1.10` + `dynaudnorm=f=200:g=5`, mono 48 kHz → **33.984 s** final (`public/assets/voice.mp3`).

## Décor choisi et pourquoi

**BUREAU** (`_shared/avatar-bank/clips/`) — sujet = tutoriel technique d'infrastructure
("voilà comment on héberge soi-même"), correspond exactement à l'usage documenté du set bureau
dans `MANIFESTE.md`. Aucune hésitation avec le set voiture : ce n'est ni de l'humour ni du
mindset, c'est une démonstration technique en 3 étapes.

## Clips avatar utilisés (aucune génération IA — vrais rushs Tony, aucun détourage)

| rôle | clip source | ss → ss+dur (source) | t (composition) | zone lèvres actives du clip |
|---|---|---|---|---|
| hook (plein cadre) | `A1_hook_frontal.mp4` | 0.67 → 4.20 | 0.000 → 3.533 | 0.67–4.58 |
| intro (fenêtre) | `B1_principe.mp4` | 0.08 → 2.08 | 4.600 → 6.600 | 0.08–4.88 |
| réalité (fenêtre) | `B1_principe.mp4` | 2.08 → 4.78 | 22.200 → 24.900 | 0.08–4.88 |
| punch (fenêtre) | `A1_hook_frontal.mp4` | 1.00 → 3.80 | 27.800 → 30.600 | 0.67–4.58 |
| CTA (fenêtre) | `C2_commente_motcle.mp4` | 0.08 → 3.48 | 30.600 → 33.984 | 0.08–4.83 |

B1 et A1 sont chacun réutilisés deux fois sur des plages sources distinctes (13,5 s de matière
active au total sur les 3 clips, budget documenté dans `MANIFESTE.md`/`LIPS-MAP.md`).

Vérifié par `check_lips_rule.mjs` (voir `work/order.json`) : **PASS — 0 image fautive** sur les
5 plans.

```
shot    srcWindow      lips-active zone   still&voiced
hook    0.67-4.20      0.67-4.58              0
intro   0.08-2.08      0.08-4.88              0
realite 2.08-4.78      0.08-4.88              0
punch   1.00-3.80      0.67-4.58              0
cta     0.08-3.48      0.08-4.83              0

PASS — no shot violates the lips-active rule
```

## Cadrage

- Hook : plein cadre (0–1080×0–1920), titre en bas (« Un VPS à **5€/MOIS** pour héberger tout
  toi-même » / « Claude Code + Coolify, zéro agence. »).
- Ensuite : fenêtre néon `648×1152` à `(216,150)`, bord jaune `rgba(234,179,8,.62)`.
- Démonstration : panneau « stack » façon nœuds n8n (mécanique reprise de `autoboost-101-triage`,
  contenu adapté au sujet) — 4 cartes qui apparaissent quand la voix les nomme, fils
  jaune→violet qui se tirent entre elles : Coolify → Claude Code (MCP) → n8n + sites + vidéos →
  même ordinateur éteint. Dans la même fenêtre que l'avatar (jamais visibles en même temps :
  l'overlay ffmpeg de l'avatar recouvre entièrement le panneau pendant ses propres plages).
- Carton transformation : « SETUP : 3 À 7H LA 1RE FOIS ▼ PLUS RIEN ENSUITE ».
- CTA : pilule jaune « Commente le mot TERMINAL » sous la fenêtre, avatar en fenêtre (clip C2).
- Captions mot-à-mot 40px sous la fenêtre (`top:1392`), jamais dessus, de `t=3.718` à `t=30.527`
  (la phrase finale « Si tu es freelance… commente le mot TERMINAL… » est en partie portée par
  la pilule CTA à partir de `t=30.600`, comme dans la référence `autoboost-101-triage`).

## Musique

`valse-des-fleurs-maison-evidee.mp3` (production maison Automation Boost, phonogramme propre —
partition domaine public Tchaïkovski réorchestrée, `_shared/bgm/bgm-manifest.json` : headroom
voix −20,8 dB, orchestral et douce — pas de BGM agressive ni de ligne néon beat-sync sur ce
format). Gain statique `-1.9dB` (`start_gain_db` du manifeste), fade-in 1,2 s, fade-out 1 s en
fin de piste, `sidechaincompress threshold=0.045:ratio=8:attack=10:release=300` piloté par la
voix (clé issue d'un `asplit` de la piste voix). Mix : voix ≈ -15.7 dB moyen sur tout le rendu,
la musique ne dépasse jamais ce niveau (elle est ~-27 dB avant tout ducking) — la voix domine
partout, conforme à la charte.

## Durée

MP4 final : **~33.92 s** (ffprobe), dans la cible 30–35 s du brief (script = 126 mots).

## Fichiers

- `public/index.html` — composition HyperFrames (habillage complet, pas de balise `<video>` —
  aucun risque de gel du renderer).
- `work/order.json` — plans avatar pour le garde-fou lèvres (`ss`, `frames`, `src`, `start`).
- `work/final_audio.wav` — piste voix seule (pas le mix), utilisée par `check_lips_rule.mjs`.
- `work/captions_words.json` — timing mot-à-mot estimé (source des captions).
- `public/assets/voice.mp3` — voix traitée. BGM référencée depuis `_shared/bgm/` (non dupliquée).
- `public/video.mp4` — rendu final (copié aussi dans
  `previsualisation/autoboost-135-vps-coolify/video.mp4`).

## Reproduire

1. Render passe 1 (habillage seul, aucune balise `<video>` dans la composition) :
   `npx hyperframes render public -o work/pass1.mp4`.
2. Préparer les 5 extraits avatar (`ffmpeg -ss <ss> -t <dur> -i <clip bureau> -vf
   "scale=…:force_original_aspect_ratio=increase,crop=…,fps=30" -an -c:v libx264 -crf 18`) :
   plein cadre `1080×1920` pour le hook, `642×1146` pour les 4 plans fenêtre.
3. Passe 2 ffmpeg : overlay du hook à `(0,0)` et des 4 plans fenêtre à `(219,153)`, chacun
   `enable='between(t,a,b)'` sur sa plage de la table ci-dessus, `setpts=PTS-STARTPTS+OFFSET/TB`.
   Audio : voix (`asplit` pour la clé sidechain) + BGM (gain statique + fades +
   `sidechaincompress` keyé par la voix) → `amix inputs=2:duration=first:normalize=0`. Mux
   `-c:v libx264 -crf 18 -c:a aac -b:a 192k -movflags +faststart`.
4. Vérifier `node _shared/avatar-bank/check_lips_rule.mjs <dossier-projet>` → PASS avant de
   livrer.
5. Extraire des frames du MP4 final et les regarder (jamais `snapshot` HyperFrames) : décor
   bureau, lèvres qui bougent avec la voix, captions lisibles, CTA visible.

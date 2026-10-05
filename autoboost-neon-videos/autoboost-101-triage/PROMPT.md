# autoboost-101-triage — recette de reproduction

Pipeline **v3** (assemblage banque avatar, pas de génération IA d'image/vidéo — donc pas de
prompt Seedance/Higgsfield à fournir ici). Ce fichier documente la recette complète pour
refaire ou décliner cette vidéo, comme l'exige `FICHE-VIDEO.md`.

## Source

Ligne 103 du Sheet de suivi, CTA TRIAGE (fournie directement par la session parente, pas lue
depuis le Sheet par cette session).

- **Sujet** : Claude Code + n8n — tri automatique des mails prospects (3 étapes)
- **Mot-clé CTA** : `TRIAGE`

## Script voix (texte intégral envoyé au TTS, non reformulé)

```
3 étapes pour que Claude trie tes mails prospects tout seul, en 20 minutes de setup. Étape 1 :
tu connectes ta boîte Gmail à un workflow n8n. Étape 2 : chaque nouveau mail passe devant un
agent Claude qui lit le message et détecte s'il vient d'un vrai prospect, d'un client existant,
ou juste d'une newsletter. Étape 3 : le workflow range automatiquement dans le bon dossier et
t'envoie une notification uniquement pour les mails qui comptent vraiment. Résultat : tu
arrêtes de scroller 40 mails par jour pour en trouver 3 utiles. C'est exactement le genre de
tâche invisible qui bouffe des heures de freelance chaque semaine, et qui ne demande aucune
compétence technique pour être mise en place. Follow pour la suite, lien en bio, et commente le
mot TRIAGE, je t'envoie le workflow complet.
```

Généré via `mcp__n8n__execute_workflow` sur le workflow `S85QlXjhIO6nBvzY` ("[Avatar AI] Webhook
v2 - Fonctionnel"), `voixUrl` = `https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3`
(voix clonée, consentement permanent déjà donné). `transcripts: []` en retour (quota OpenAI
Whisper épuisé côté compte Tony, symptôme déjà documenté dans `autoboost-99-soustitre-descript`)
→ **timing mot-à-mot estimé manuellement** (pondération longueur de mot + bonus ponctuation
+5 pour un mot finissant par `.`/`:`, +3 pour une virgule, normalisé sur la durée réelle ffprobe),
**pas de vrai timestamp Whisper sur cette vidéo**.

Le MP3 CloudFront renvoyé par WaveSpeed (`voiceUrl`) n'est pas accessible en direct depuis le
shell sandbox (`curl` → `403 CONNECT tunnel failed`, confirmé). Relayé via un workflow n8n
one-off réutilisé (`60gWJPkUlXtA3bsh`, renommé `[Oneoff] Download Voice - Autoboost 101
Triage`) : `HTTP Request` en `responseFormat: file` sur le `voiceUrl`, puis un node `Code` qui
découpe le binaire en chunks base64 de 50 000 caractères (8 chunks pour 265 008 octets),
récupérés via `get_execution` et réassemblés côté shell.

MP3 brut : **35.136 s**. Post-traitement : `atempo=1.033` + `dynaudnorm=f=200:g=5`, mono 48 kHz
→ **33.984 s** final (`public/assets/voice.mp3`).

## Décor choisi et pourquoi

**BUREAU** (`_shared/avatar-bank/clips/`) — sujet = démonstration d'un workflow n8n technique
("voilà comment on fait"), correspond exactement à l'usage documenté du set bureau dans
`MANIFESTE.md`. Aucune hésitation avec le set voiture ici.

## Clips avatar utilisés (aucune génération IA — vrais rushs Tony, aucun détourage)

| rôle | clip source | ss → ss+dur (source) | t (composition) | zone lèvres actives du clip |
|---|---|---|---|---|
| hook (plein cadre) | `A1_hook_frontal.mp4` | 0.67 → 4.20 | 0.000 → 3.533 | 0.67–4.58 |
| intro-démo (fenêtre) | `B1_principe.mp4` | 0.08 → 2.08 | 4.600 → 6.600 | 0.08–4.88 |
| réalité (fenêtre) | `B1_principe.mp4` | 2.08 → 4.71 | 10.000 → 12.633 | 0.08–4.88 |
| punch (fenêtre) | `A1_hook_frontal.mp4` | 1.00 → 3.83 | 26.500 → 29.333 | 0.67–4.58 |
| CTA (fenêtre) | `C2_commente_motcle.mp4` | 0.08 → 4.18 | 29.900 → 34.033 | 0.08–4.83 |

B1 et A1 sont chacun réutilisés deux fois sur des plages sources distinctes (13,5 s de matière
active au total sur les 3 clips, budget documenté dans `MANIFESTE.md` / `LIPS-MAP.md`), comme
dans `autoboost-99-soustitre-descript`.

Vérifié par `check_lips_rule.mjs` (voir `work/order.json`) : **PASS — 0 image fautive** sur les
5 plans.

```
shot  srcWindow        lips-active zone      still&voiced
hook  0.67-4.20       0.67-4.58                0
intro 0.08-2.08       0.08-4.88                0
realite 2.08-4.71       0.08-4.88                0
punch 1.00-3.83       0.67-4.58                0
cta   0.08-4.18       0.08-4.83                0

PASS — no shot violates the lips-active rule
```

## Cadrage

- Hook : plein cadre (0–1080×0–1920), titre en bas (« 3 étapes pour que **CLAUDE** trie tes
  mails prospects tout seul, en 20 minutes de setup. »).
- Ensuite : fenêtre néon `648×1152` à `(216,150)`, bord jaune `rgba(234,179,8,.62)`.
- Démonstration workflow : **canvas n8n animé**, 4 nœuds réels du workflow décrit dans le
  script (Gmail — nouveau mail → Agent Claude — lecture IA → Switch — tri automatique →
  Notification ciblée), icône + nom + type + puce d'explication, qui apparaissent quand la voix
  les nomme, fils jaune→violet qui se tirent entre eux — dans la même fenêtre que l'avatar (les
  deux ne sont jamais visibles en même temps : l'overlay ffmpeg de l'avatar recouvre entièrement
  le canvas pendant ses propres plages).
- Carton transformation : « 40 MAILS/JOUR ▼ 3 UTILES » (empilé verticalement dans la fenêtre —
  la version initiale en ligne horizontale débordait du cadre 648px, corrigée avant rendu final).
- CTA : pilule jaune « Commente le mot TRIAGE » sous la fenêtre, avatar en fenêtre (clip C2).
- Captions mot-à-mot 40px sous la fenêtre (`top:1392`), jamais dessus, de `t=3.590` à
  `t=29.820` (la phrase finale « Follow pour la suite… » est portée par la pilule CTA, pas par
  les captions, comme dans la référence).

## Musique

`valse-des-fleurs-maison-evidee.mp3` (production maison Automation Boost, phonogramme propre —
partition domaine public Tchaïkovski réorchestrée, `_shared/bgm/bgm-manifest.json` : headroom
voix −20,8 dB, le meilleur de la bibliothèque, orchestral et douce comme demandé — pas de BGM
agressive ni de ligne néon beat-sync sur ce format). Gain statique `-1.9dB` (son `start_gain_db`
du manifeste), fade-in 1,2 s, fade-out 1 s en fin de piste, puis `sidechaincompress
threshold=0.045:ratio=8:attack=10:release=300` piloté par la voix. Mesuré sur le rendu final :
mix global à −13,9 dB moyen (identique à la voix seule à −13,9 dB moyen) pendant les passages
parlés — la musique ne se bat jamais avec la voix — et remonte à −20,7 dB moyen / −5,2 dB crête
pendant le fondu de fin (silence de voix), donc bien présente hors voix active. Cible maison
≈16 dB d'écart largement respectée (écart mesuré supérieur, marge de sécurité volontaire).

## Durée

MP4 final : **34.03 s** (ffprobe), dans la cible 30–35 s du brief (script ≈137 mots).

## Fichiers

- `public/index.html` — composition HyperFrames (habillage complet, pas de balise `<video>` —
  aucun risque de gel du renderer).
- `work/order.json` — plans avatar pour le garde-fou lèvres (`ss`, `frames`, `src`, `start`).
- `work/final_audio.wav` — piste voix seule (pas le mix), utilisée par `check_lips_rule.mjs`.
- `public/assets/voice.mp3`, `public/assets/bgm.mp3` — audio source.
- `public/video.mp4` — rendu final (copié aussi dans `previsualisation/autoboost-101-triage/video.mp4`).

## Reproduire

1. Render passe 1 (habillage seul, `videoCount:0` implicite — la composition ne contient aucune
   balise `<video>`) : `npx hyperframes render public -o work/pass1.mp4`.
2. Préparer les 5 extraits avatar (`ffmpeg -ss <ss> -t <dur> -i <clip bureau> -vf
   "scale=…:force_original_aspect_ratio=increase,crop=…,fps=30" -an -c:v libx264 -crf 18`) :
   plein cadre `1080×1920` pour le hook, `642×1146` pour les 4 plans fenêtre.
3. Passe 2 ffmpeg : overlay du hook à `(0,0)` et des 4 plans fenêtre à `(219,153)`, chacun
   `enable='between(t,a,b)'` sur sa plage de la table ci-dessus, `setpts=PTS-STARTPTS+OFFSET/TB`
   pour caler l'avatar sur sa fenêtre. Audio : voix (`asplit` pour fournir la clé sidechain) +
   BGM (gain statique + fades + `sidechaincompress` keyé par la voix) → `amix
   inputs=2:duration=first:normalize=0`. Mux `-c:v libx264 -crf 18 -c:a aac -b:a 192k -movflags
   +faststart`.
4. Vérifier `node _shared/avatar-bank/check_lips_rule.mjs <dossier-projet>` → PASS avant de
   livrer.
5. Extraire des frames du MP4 final et les regarder (jamais `snapshot` HyperFrames, inutilisable
   dans cet environnement) : décor bureau, lèvres qui bougent avec la voix, captions lisibles.

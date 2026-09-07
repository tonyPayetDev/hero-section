# autoboost-99-soustitre-descript — recette de reproduction

Pipeline **v3** (assemblage banque avatar, pas de génération IA d'image/vidéo — donc pas de
prompt Seedance/Higgsfield à fournir ici). Ce fichier documente la recette complète pour
refaire ou décliner cette vidéo, comme l'exige `FICHE-VIDEO.md`.

## Source Sheet

Google Sheet `10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags`, onglet **30 Vidéos** (gid
`1576933581`), ligne physique **102** (colonne `#` = 99).

- **Sujet** : Alternative gratuite à Descript — sous-titres auto (Whisper + n8n)
- **Mot-clé CTA** : `SOUSTITRE`

## Script voix (texte intégral envoyé au TTS)

```
Descript te coûte 30€ par mois pour sous-titrer tes vidéos automatiquement. Il existe une
alternative 100% gratuite, et elle tourne toute seule. Un modèle open source appelé Whisper
transcrit ta vidéo mot par mot, un workflow n8n récupère le texte, le découpe en sous-titres
stylés, et te renvoie le fichier prêt à publier. Même qualité que l'outil payant, zéro carte
bancaire, zéro abonnement à annuler dans 6 mois. Je l'utilise pour toutes mes vidéos TikTok et
Instagram depuis des semaines, et ça tourne en arrière-plan pendant que je fais autre chose. Si
tu perds encore du temps à sous-titrer à la main, ce workflow te rend au moins une heure par
semaine. Follow pour la suite, lien en bio, et commente le mot SOUSTITRE, je t'envoie le montage
complet.
```

Généré via webhook n8n `avatar-webhook-v2` (workflow `S85QlXjhIO6nBvzY`), `voixUrl` =
`https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3` (voix clonée, consentement
permanent déjà donné). Whisper interne a renvoyé `transcripts: []` (quota OpenAI épuisé côté
compte Tony, symptôme déjà documenté) → timing mot-à-mot **estimé manuellement** (pondération
longueur de mot + bonus ponctuation, normalisé sur la durée réelle ffprobe), pas de vrai
timestamp Whisper sur cette vidéo. MP3 brut 37.776s, accéléré `atempo=1.1111` → **34.008s** final.

## Décor choisi et pourquoi

**BUREAU** (`_shared/avatar-bank/clips/`) — sujet = démonstration d'un workflow n8n technique
("voilà comment on fait"), correspond exactement à l'usage documenté du set bureau dans
`MANIFESTE.md`. Aucune hésitation avec le set voiture ici.

## Clips avatar utilisés (aucune génération IA — vrais rushs Tony, aucun détourage)

| rôle | clip source | ss → ss+dur (source) | t (composition) | zone lèvres actives du clip |
|---|---|---|---|---|
| hook (plein cadre) | `A1_hook_frontal.mp4` | 0.67 → 4.07 | 0.000 → 3.400 | 0.67–4.58 |
| intro-démo (fenêtre) | `B1_principe.mp4` | 0.08 → 2.08 | 6.600 → 8.600 | 0.08–4.88 |
| réalité (fenêtre) | `B1_principe.mp4` | 2.08 → 4.78 | 14.600 → 17.300 | 0.08–4.88 |
| punch (fenêtre) | `A1_hook_frontal.mp4` | 1.00 → 3.50 | 25.100 → 27.600 | 0.67–4.58 |
| CTA (fenêtre) | `C2_commente_motcle.mp4` | 0.08 → 4.38 | 29.700 → 34.008 | 0.08–4.83 |

Vérifié par `check_lips_rule.mjs` (voir `work/order.json`) : **PASS, 0 image fautive** sur les 5
plans. Aucune plage ne traverse une zone morte.

## Cadrage

- Hook : plein cadre (0–1080×0–1920), titre en bas (« Descript te coûte 30€/MOIS »).
- Ensuite : fenêtre néon `648×1152` à `(216,150)`, bord jaune `rgba(234,179,8,.62)`.
- Démonstration workflow : **canvas n8n animé** (4 nœuds réels du workflow décrit dans le
  script : déclencheur vidéo → Whisper → n8n découpe → fichier prêt), nœuds qui apparaissent
  quand la voix les nomme, fils jaune→violet qui se tirent entre eux — dans la même fenêtre que
  l'avatar (les deux ne sont jamais visibles en même temps).
- Carton transformation : « DESCRIPT 30€/MOIS ▼ 0€ ».
- Carte valeur : « 1H économisée / semaine ».
- CTA : pilule jaune « Commente le mot SOUSTITRE » sous la fenêtre, avatar en fenêtre.
- Captions mot-à-mot 40px sous la fenêtre (`top:1392`), jamais dessus.

## Musique

`vsl-voxscape-ambient.mp3` (Mixkit #571, licence libre commerciale), gain `start_gain_db=-20.7dB`
(facteur ≈0.092), fade-in 1s, sidechain sous la voix. Choisi pour le meilleur `voice_headroom_db`
de la bibliothèque adapté à un ton posé/technique (pas de drums épiques, sujet tuto pas hook-mindset).

## Fichiers

- `public/index.html` — composition HyperFrames (habillage complet, pas de balise `<video>` —
  aucun risque de gel du renderer).
- `work/order.json` — plans avatar pour le garde-fou lèvres.
- `public/assets/voice.mp3`, `public/assets/bgm.mp3` — audio source.

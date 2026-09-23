# autoboost-138-visage-avatar — recette de reproduction

Pipeline **v3** (assemblage banque avatar). Aucune image ni vidéo générée par IA dans ce montage :
vraies prises de Tony, décor BUREAU, aucun détourage. Aucun marqueur à remplacer par l'avatar.

## Source

Sheet `10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags`, onglet `30 Videos`, **`row_number` 140**
(colonne `#` = 138). Lu via le workflow n8n `IUORhoZ4qt3s8PjT` (docs.google.com bloqué depuis le shell).

La ligne 137 (#135) est aussi en `⬜ À faire`, mais son rendu existe déjà
(`autoboost-135-vps-coolify/`, bloqué seulement sur la publication) : elle n'a pas été refaite.

- **Sujet** : Verrouiller le visage d'un avatar IA (Seedance + Claude)
- **Mot-clé CTA** : `PROMPT`

## Script voix (resserré depuis le script du Sheet : 131 → ~120 mots, pour tenir ~31 s)

```
Ton avatar IA change de visage à chaque plan ? Avec Seedance et Claude, voici la technique en trois
éléments pour garder exactement le même visage sur toute une vidéo. La plupart des gens décrivent un
visage en une phrase, et laissent le hasard faire le reste. Résultat : un patchwork de visages que
personne ne prend au sérieux. La technique tient en trois blocs précis dans le prompt : verrouiller
l'identité, figer le décor et la lumière, cadrer le jeu d'acteur. Plus une image de référence,
réutilisée à l'identique à chaque génération. Résultat : un vrai personnage, cohérent du début à la
fin. C'est exactement ce que j'utilise sur toutes mes vidéos IA. Suis-moi et commente le mot PROMPT,
je t'envoie la technique complète gratuitement.
```

Les « trois blocs » ne sont pas inventés : ce sont les sections IDENTITY LOCK / VISUAL CONSISTENCY /
PERFORMANCE du MASTER PROMPT réel de la banque (`_shared/avatar-bank/seedance-prompts.md`).

Voix : workflow n8n one-off `sGlypRc8q2AgAheD` (POST `avatar-webhook-v2`, `voixUrl` archiviste,
téléchargement du MP3 CloudFront et découpage base64, car shell → n7n/CloudFront bloqué).
`transcripts: []` en retour → timing mot-à-mot **estimé** (pauses `silencedetect -36dB d=0.06`
+ pondération longueur de mot/ponctuation), voir `work/words.py`.
MP3 brut 32,81 s → `silenceremove` tête/queue (−45 dB, peak) + `atempo=1.05` + `dynaudnorm=f=200:g=5`
→ **31,01 s**. F0 médian mesuré **118,5 Hz** (plage clone 114–133 Hz, pas le repli OpenAI).

## Décor : BUREAU

Sujet = technique de prompt, démonstration « voilà comment on fait » → set bureau (`clips/`),
conformément à `MANIFESTE.md`. Pas d'humour ni de mindset : le set voiture n'était pas candidat.

## Plans avatar (source unique : `work/order.json`, lu par `build_pass2.mjs` ET le garde-fou)

| plan | clip | source (s) | vidéo (s) | zone lèvres actives |
|---|---|---|---|---|
| hook plein cadre | A1_hook_frontal | 0.67 → 3.00 | 0.00 → 2.33 | 0.67–4.58 |
| intro fenêtre | B1_principe | 0.08 → 2.41 | 2.66 → 5.00 (gel 1re image dès 2.32) | 0.08–4.88 |
| réalité fenêtre | B1_principe | 2.18 → 4.85 | 11.02 → 13.69 | 0.08–4.88 |
| punch fenêtre | A1_hook_frontal | 2.40 → 4.53 | 25.76 → 27.89 (gel → 28.20) | 0.67–4.58 |
| CTA fenêtre | C2_commente_motcle | 0.08 → 2.88 | 28.20 → 31.00 (gel → 31.60) | 0.08–4.83 |

Chaque plan s'arrête à la fin de sa phrase ; les silences sont tenus par l'image gelée (`tpad`).
`check_lips_rule.mjs` (sur `work/final_audio.wav` = voix seule) : **PASS, 0 image fautive**.
Contrôle sur le rendu final (différence inter-images dans la boîte bouche de la fenêtre) :
mouvement moyen 5,9–7,1 sous voix (immobile < 1,2), aucune série immobile sous voix active.

## Habillage (passe 1 HyperFrames, `public/index.html`, aucune balise `<video>`)

Hook plein cadre + titre bas → fenêtre néon 648×1152 @ (216,150), captions 40 px sous la fenêtre
(top 1392). Panneaux : « 3 éléments » (5.00–7.40) · « prompt en une phrase » tapé puis
4 plans aux visages différents (7.45–11.00) · prompt Seedance en 3 blocs reliés, chaque bloc
apparaît quand la voix le nomme (13.72–19.80) · image de référence + 4 générations identiques
(19.84–23.05) · carton « 4 VISAGES DIFFÉRENTS ▼ 1 SEUL PERSONNAGE » (23.11–25.55) · pilule
« Commente le mot PROMPT » (28.20→fin). Aucun emoji (charte).

## Audio (passe 2)

Voix + `valse-des-fleurs-maison-evidee.mp3` (−1,9 dB, fade-in 1,2 s, fade-out 1 s),
`sidechaincompress threshold=0.045:ratio=8:attack=10:release=300` keyé par la voix,
`amix normalize=0`. Mix final : moyenne −15,6 dB, crête −0,5 dB.

## Reproduire

```bash
export FONTCONFIG_PATH=/etc/fonts
npx hyperframes render public -o work/pass1.mp4        # passe 1
cd work && node check_lips_rule.mjs "$(dirname $PWD)"   # garde-fou -> PASS
node build_pass2.mjs                                     # passe 2 -> public/video.mp4
```

## Publication

**Non publiée.** Cette session n'a accès qu'au dépôt `tonyPayetDev/hero-section` : le dépôt
`tonyPayetDev/previsualisation` servi par Coolify lui est refusé, et `COOLIFY_ACCESS_TOKEN` est
absent. `previsualisation/autoboost-138-visage-avatar/` (video.mp4 + index.html + ref.jpg) est prêt
à être copié tel quel dans le vrai dépôt. Test HTTP au 2026-09-23 : 404.

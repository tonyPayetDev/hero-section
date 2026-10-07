# WIP — autoboost-138-verrouiller-visage-seedance

Statut : **SCAFFOLD, PAS FINI.** Généré le 2026-10-07 par la routine « 1 vidéo Autoboost/jour ».

## Pourquoi ce n'est pas fini
Le pipeline de **voix clonée** (archiviste / WaveSpeed via n8n) était **injoignable** ce run :
la policy réseau de la session bloque (403 CONNECT) `n7n.automatisationboost.com`,
`api.wavespeed.ai` et `assets.automatisationboost.com` ; le MCP n8n n'était pas authentifié
(session non-interactive) ; aucune clé WaveSpeed en env. `voice.mp3` n'a donc PAS pu être généré.
Aucune voix de substitution n'a été utilisée (règle : ne jamais substituer silencieusement la voix de marque).

## Ce qui EST fait et validé
- `public/index.html` : compo complète adaptée du gabarit `autoboost-40-seedance` au sujet row140
  (5 scènes « 3 éléments » + hook + broll + CTA PROMPT), captions **27px** autour de `top:960px`,
  avatar overlay persistant, ligne/pulse sur les drops de `flowers_horror.mp3`, SFX palette v1.
- `hyperframes validate` : **OK** (0 erreur console, 34 textes WCAG AA).
- `hyperframes inspect` : 0 erreur / 0 warning / 2 info (les ✕ barrés de la scène 3, layering voulu).
- `narration.md` : texte voix off final (~102 mots, CTA PROMPT).

## Ce qu'il RESTE à faire pour finaliser (quand n7n/n8n est joignable)
1. Copier les assets dans `public/assets/` (non committés) :
   - SFX : `cp ../_shared/sfx-palette/v1/assets/sfx-*.mp3 public/assets/`
   - BGM : `cp ../_shared/bgm/flowers_horror.mp3 public/assets/`
   - gsap + avatar + broll : `cp ../autoboost-100-gemini-seedance/public/assets/{gsap.min.js,avatar-keyed.mp4,broll-creator.mp4} public/assets/`
2. Générer la voix : `POST https://n7n.automatisationboost.com/webhook/avatar-webhook-v2`
   body `{voixUrl:"https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3", avatarUrl:<avatar>, description:<narration.md>}`
   → récupérer `{voiceUrl, transcripts}`, télécharger en `public/assets/voice.mp3`, vérifier la durée (`ffprobe`).
3. `silencedetect=noise=-40dB:d=0.18` sur voice.mp3 → **recaler les 5 coupes de scène** (`data-s`/`data-d`)
   et le tableau `caps` sur les **vrais** timestamps mots (transcripts Whisper, sinon estimation pondérée).
4. Recaler les `data-start` SFX sur les coupes finales (whoosh : pic ~1,2 s avant la coupe).
5. `hyperframes validate` + `inspect`, puis **rendre** : `hyperframes render public -o public/renders/final.mp4`.
6. **Vérifier des frames extraites** du MP4 (pas seulement ffprobe) : le texte doit apparaître.
7. Publier dans le dépôt `previsualisation` (route dédiée, ne jamais écraser) : `video.mp4` + `index.html`,
   commit/push `main`, puis tester l'URL publique avec cache-buster (200 + plusieurs Mo).
8. Reporter : `POST https://n7n.automatisationboost.com/webhook/sheet-video-update`
   `{cta:"PROMPT", statut:"🟡 En attente validation", videoUrl:<url previsualisation>}`.

> Les `data-start`/`data-duration` et les timings du tableau `caps` sont **PROVISOIRES**
> (repris du squelette de #40). Ne pas publier sans l'étape 3.

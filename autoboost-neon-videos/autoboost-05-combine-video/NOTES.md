# Autoboost Neon Video — #5 Combine Video + Caption Voix

Source : ligne #5 du [Sheet de suivi](https://docs.google.com/spreadsheets/d/10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags/edit) — CTA `VIDEO`.

## ✅ CRÉÉE ET PLANIFIÉE (2026-07-09)

Le scaffold hérité du commit b730491 (copie brute de `autoboost-04-telegram-agent-ia`) n'avait
aucun contenu adapté : titre, captions et scènes étaient toujours ceux de la vidéo #4 (Telegram
Agent IA). Reconstruction complète pour le script réel de la ligne #5 :

> Si tu passes encore des heures sur CapCut, ce workflow va te faire gagner un temps fou. Je donne
> un texte. Il génère la voix, assemble la vidéo, ajoute les sous-titres, et exporte. Ce que tu
> vois là a été créé en deux minutes. Zéro montage. Commente VIDEO pour recevoir le workflow
> gratuitement.

- **Audio** : voix de marque `archiviste_ZIl7EoOf.mp3` (pas de clone perso, donc aucun consentement
  supplémentaire requis), générée via webhook `avatar-webhook-v2` (2026-07-09) avec vrais timestamps
  Whisper mot-à-mot. Durée réelle 16.68s. `public/assets/voice.mp3` mis à jour (l'ancien fichier du
  scaffold était un résidu d'une version intermédiaire de la voix #4, contenu non lié à cette vidéo).
- **5 scènes reconstruites** : hook (CapCut barré → 2 min), setup (texte donné à l'agent, card
  "Fais une vidéo sur mon offre business"), flow 5 nœuds plein écran (Texte → Voix IA → Montage →
  Sous-titres → Export, broll sans avatar comme #4 scène 3), badge "Zéro montage", CTA
  "Workflow gratuit — VIDEO". `.flow`/`.flow-node` réduits (148px→130px, largeur 980→1020px) pour
  caser 5 nœuds + 4 flèches au lieu de 4 nœuds + 3 flèches sans les compresser à l'excès.
- **18 captions** resynchronisées sur les timestamps Whisper réels de cette exécution (voir
  `<script>` en bas de `public/index.html`). Whisper a mal entendu "Commente" → "Commande" dans sa
  transcription brute (même type de quirk que "ChatGPT"→"chaque"+"GPT" sur la vidéo #4) — le texte
  affiché à l'écran garde l'orthographe correcte, seuls les timestamps ont servi au calage.
- **Durée totale 17.30s** (narration 16.68s + ~0.6s de tenue sur le CTA). BGM `bgm-ascension.mp3`
  (piste de marque, déjà présente dans le scaffold) loop-étendue de 16.78s → 17.30s via
  `ffmpeg -stream_loop -1 -t 17.30` (jamais de trim dans le filter graph, cf. CLAUDE.md racine).
  `avatar-keyed.mp4` (17.42s, réutilisé du scaffold) est assez long, pas de loop nécessaire.
- Revalidé (`ok:true`, seul warning bénin attendu : slot voix 17.30s vs média 16.62s — c'est le
  hold CTA intentionnel). `inspect` : 0 layout issue (le warning "StaticGuard" sur l'animation
  `left` des pulses de flèches est hérité du template #4 tel quel, pas une régression introduite ici).
- Rendu : `npx hyperframes@0.7.5 render public` → `renders/public_2026-07-09_09-38-23.mp4`
  (H.264 1080×1920, AAC, 17.32s, 5.5MB). Vérifié visuellement (frames à 0.5/2/3.5/5/6.8/8.5/10/
  11.8/13.5/15/16.5s) : texte/captions/icônes tous visibles, pas de double-contour, pipeline 5
  nœuds lisible.

**Publié en planification sur Blotato (2026-07-09, PAS immédiat)** :
- Média : `https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/6cba9109-2cc0-4f85-a2e1-c625b7061564.mp4`
- Instagram `automatisationboost` (id 54617, reel) — postSubmissionId `f12c6b55-a5c7-4734-9e86-3346a0f6b165`
- TikTok `tonypayet4` (id 36488, PUBLIC_TO_EVERYONE, isAiGenerated:true) — postSubmissionId `9889a8d3-8867-4957-8fab-9f2692f5e021`
- Les deux planifiés pour `2026-07-09T12:26:00Z`. Pas de compte TikTok "automatisationboost"
  connecté sur Blotato (seulement tonypayet4/subscribe_humian/infinimerveille) — confirmé avec
  l'utilisateur, tonypayet4 choisi.
- `blotato_create_post` avec `useNextFreeSlot:true` échoue ("No available slot time found in the
  next 9 months") — aucun calendrier de créneaux auto configuré côté Blotato pour ces comptes,
  il faut toujours passer un `scheduledTime` ISO 8601 explicite.

## ⚠️ Reste à faire manuellement

- **Sheet de suivi** : passer la ligne #5 `Statut Tournage` à ✅ Fait, remplir `Vidéo Finale`
  (lien média ci-dessus) et `Date Publication` (2026-07-09). Pas fait automatiquement dans cette
  session (pas d'accès Google Sheets API direct ici — voir méthode de contournement décrite dans
  le skill `veille-to-video` étape 9 si besoin de l'automatiser plus tard).

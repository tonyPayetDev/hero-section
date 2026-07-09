# Autoboost Neon Video — #7 Dashboard Sync Notion

Source : ligne #7 du [Sheet de suivi](https://docs.google.com/spreadsheets/d/10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags/edit) — CTA `NOTION`.

## 🔄 EN COURS (2026-07-09)

Composition HyperFrames créée et structurée — **en attente audio TTS** (webhook timeout, en cours diagnostique).

### Composition (#7) complète :

**Script (20s cible):**
> Si tu commences encore ta journée sans savoir où tu en es, ce workflow va changer ta vie. Chaque matin il récupère mes tâches, mes revenus, mes objectifs, et génère un résumé IA dans Notion. Je me lève, j'ouvre Notion, tout est là. Commente NOTION pour recevoir le workflow gratuitement.

- **Scène 1 (0–4s)** : Hook visuel — "Matin = Flou" vs "Notion = Clarté" avec transition
- **Scène 2 (4–7s)** : 3 cards pulseuses (Tâches, Revenus, Objectifs) avec icônes
- **Scène 3 (7–13s)** : Dashboard Notion mock plein écran
- **Scène 4 (13–17.5s)** : Avatar + CTA "Commente NOTION" (mot-clé surligné jaune)
- **Captions** : 16 phrases word-level (en attente timestamps Whisper du webhook)

**Assets :**
- `public/assets/avatar-keyed.mp4` (17.42s, réutilisé de #5)
- `public/assets/bgm-ascension.mp3` (piste de marque, sera loop-étendue à 17.5s)
- `public/assets/sfx-whoosh-v2.mp3`, `sfx-chime-v2.mp3` (réutilisés de #5)
- `public/assets/voice.mp3` — **PLACEHOLDER** (en attente webhook TTS response)

**HTML/GSAP :**
- 1 GSAP timeline, pausée par défaut
- Scènes, captions, timing animations tous définis et prêts
- `data-composition-id: "autoboost-07-dashboard-notion"` set
- Données correctes en data-* attributes

### Prochaines étapes :

1. **Récupérer audio TTS** : Webhook avatar-webhook-v2 répond HTTP 200 mais corps vide après timeout n8n. Chercher URL CloudFront dans les nodes d'exécution n8n récentes ou relancer le webhook avec logs plus détaillés.
2. **Télécharger audio** → `public/assets/voice.mp3`
3. **Valider** : `npx hyperframes validate public`
4. **Rendre** : `npx hyperframes render public` → MP4
5. **Vérifier visuellement** : Extraire frames, confirmer captions + icônes visibles
6. **Uploader Blotato** + planifier publication Instagram + TikTok
7. **Updater Sheet** : Statut "✅ Fait", lien vidéo finale, date publication

---

**État technique :**
- ✅ HTML/GSAP structure complète
- ✅ Assets (avatar, BGM, SFX) copiés de #5
- ⏳ TTS audio generation (webhook instable)
- ⬜ Validation (bloquée sans audio)
- ⬜ Rendu
- ⬜ Publication

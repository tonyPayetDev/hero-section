---
name: veille-to-video
description: Autoboost Neon Video — transforme un script/brief texte en vidéo promo sociale 9:16 (matte black + accents néon jaune/violet/orange), avec avatar/setup, voix clonée WaveSpeed, captions TikTok mot-à-mot, et publie sur Blotato. Source des vidéos à produire = Google Sheet de suivi.
---

# veille-to-video — Autoboost Neon Video

**Input :** script/brief texte (ou une ligne du Google Sheet de suivi) + voix + avatar
**Output :** projet HyperFrames (`public/index.html`) + MP4 rendu 1080x1920 + post publié sur Blotato

**Sheet source des vidéos à faire :**
`https://docs.google.com/spreadsheets/d/10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags/edit`
Colonnes : `# | Workflow | Lien n8n | Script Voix Off (20s) | Texte TikTok + Hashtags | Mot-clé CTA | Lien Screen Record | Statut Tournage | Vidéo Finale | Date Publication`
Toujours relire cette feuille en premier pour choisir la prochaine vidéo `⬜ À faire` et récupérer son script, ses hashtags et son mot-clé CTA — ne pas régénérer un brief à la main si la feuille en a déjà un.

---

## Goal

Créer une vidéo promo sociale française au format 9:16 à partir d'un script ou d'un brief. Sortie : un projet HyperFrames + un MP4 rendu.

## Style obligatoire

- **Format** : 1080x1920 vertical, 30 fps sauf indication contraire du projet.
- **Palette** : fond noir mat, accent global jaune `#FFE600`, plus violet `#A855F7` et orange `#FF8A3D` en highlights. Ne jamais revenir au bleu comme accent dominant.
- **Voix** : utiliser la voix clonée de l'utilisateur uniquement après accord explicite pour cette vidéo précise. Préférer `C:\Users\User\Work\Video IA AUTOBOOST\audio\voice-reference-clean.wav` avec WaveSpeed `wavespeed-ai/qwen3-tts/voice-clone`.
- **Captions** : style TikTok, centrées autour de la bande de sécurité médiane quand le bas contient l'avatar/setup, une seule ligne, trois mots maximum si possible. Surligner exactement un mot actif/puissant par caption en néon jaune/violet/orange. Ne pas mettre de boîte/fond visible derrière chaque mot ; texte blanc avec contour/ombre noire, et glow néon coloré pour le mot actif.
- **Avatar/setup** : quand on utilise le fond setup réaliste, retirer les filtres vert/noir et le flou latéral. L'avatar ne doit jamais cligner des yeux au début et ne doit jamais chevaucher les captions ou le texte qui slide.
- **Visuels** : utiliser de vrais schémas, icônes, dashboards, graphes, flèches de flux, panneaux UI. Éviter les slides façon PowerPoint/cartes seules, les filtres noirs sur le texte, la double exposition et les écrans statiques.
- **CTA** : pour les modèles/templates gratuits, dire que le modèle est gratuit et demander de commenter le mot-clé (colonne `Mot-clé CTA` du Sheet — RESTO, FREELANCE, LEADS, AGENT, VIDEO, PROSPECTION, NOTION, PINTEREST, IDEAS, LIVRE, SITE, AVATAR, WHATSAPP, REPURPOSE, BLOG, VEILLE, CREATEUR, PAGE, DEVIS, SEO, SEEDANCE...) plutôt que de donner l'URL du site directement.

---

## Workflow

### Étape 0 — Choisir la vidéo dans le Sheet

1. Lire le Google Sheet (export CSV : `.../export?format=csv`, suivre la redirection `googleusercontent.com` si besoin).
2. Filtrer les lignes `Statut Tournage = ⬜ À faire`, proposer la prochaine à l'utilisateur (ex. actuellement lignes #3–20 : Freelance Auto-Bidding, Lead Generation, AI Telegram Agent, Video Creation, Pinterest Automation, Children's Book Generator, Website Updates, Viral Reel Cloning, Blog Article Generation, SEO Analysis...).
3. Récupérer : `Script Voix Off (20s)`, `Texte TikTok + Hashtags`, `Mot-clé CTA`, `Lien Screen Record` (capture du workflow n8n si dispo), `Lien n8n`.
4. Si l'utilisateur donne un brief/script en direct au lieu d'une ligne du Sheet, l'utiliser à la place — mais toujours proposer d'écrire le résultat dans la colonne `Vidéo Finale` / `Statut Tournage` du Sheet une fois terminé (mise à jour manuelle, ce skill ne modifie pas le Sheet automatiquement).

### Étape 1 — Parser le script

Découper en hook / corps / CTA / durée cible. Supprimer les blocs de script collés en double.

### Étape 2 — Réécrire la narration si besoin

Réécrire uniquement pour le timing/la prononciation TTS. Garder le sens de l'utilisateur, texte de slide en français.

### Étape 3 — Consentement voix clonée

**Avant tout envoi de l'échantillon de voix à WaveSpeed**, exiger un texte explicite de l'utilisateur du type :
`J'autorise l'envoi de mon échantillon de voix à WaveSpeed pour générer l'audio de cette vidéo ...`
Sans ce texte, ne pas appeler l'API voice-clone. Ne jamais lire ni afficher les clés API.

### Étape 4 — Générer l'audio

WaveSpeed Qwen3 TTS voice-clone : `/api/v3/wavespeed-ai/qwen3-tts/voice-clone` avec `audio` (référence locale ci-dessus), `text`, `language: "French"`. Narration énergique et concise, proche du découpage des captions.

Sauvegarder le MP3 sous `C:\Users\User\Work\Video IA AUTOBOOST\audio\` et copier vers `public/assets/voice.mp3`.

### Étape 5 — Construire `public/index.html` (HyperFrames)

- Racine explicite `width:1080px; height:1920px;` et `data-duration` correspondant au plan final vidéo/audio.
- `<audio id="voice" src="assets/voice.mp3" data-start="0" data-duration="...">` en enfant direct de la racine si audio utilisé.
- Une seule timeline GSAP en pause, enregistrée dans `window.__timelines[compositionId]`.

**Captions** — spans TikTok mot-à-mot : mots neutres en texte plein sans rectangle/fond visible ; un seul mot actif `.hot`, `.violet` ou `.orange` en texte coloré/glow, jamais en pastille dure sauf demande explicite. Garder les captions loin des lignes de séparation et de la zone avatar/setup. Si `inspect` signale un dépassement, réduire la taille de police avant de faire du wrap. Synchroniser manuellement sur la narration si pas de timestamps mot-à-mot.

**Slides SaaS/automatisation premium** — zone d'explication en haut + avatar/setup en bas si demandé. Texte court, en français. Pour le slide du flow d'automatisation, préférer un schéma horizontal stable : `Gmail -> Agent IA -> n8n -> Base -> Dashboard`, avec cartes icônes, flèches, point pulsé animé, petit panneau data/schéma. Éviter les layouts diagonaux qui se chevauchent.

Quand la demande est "premium SaaS", style Apple/Linear/Arc/Vercel/Raycast, explainer automatisation, vrais schémas/icônes/dashboards/graphes, ou explainer produit haut de gamme → lire `references/premium-saas-launch.md`. Override local : le jaune remplace le bleu comme accent global.

### Étape 6 — Valider avant rendu

```bash
npx -p node@22 -p hyperframes hyperframes validate public --json
npx -p node@22 -p hyperframes hyperframes inspect public
```

Confirmer 0 problème de layout, en particulier captions vs ligne de séparation/avatar/texte.

### Étape 7 — Rendre et vérifier

Rendre avec HyperFrames, vérifier avec `ffprobe` (durée, résolution, streams, taille plausible).

Si l'espace disque bloque le rendu, ne nettoyer QUE : cache Chrome Puppeteer/HyperFrames, anciens MP4 générés par ce même projet, anciens dossiers frames/checks. Ne jamais supprimer les échantillons de voix source, les uploads utilisateur, ou les assets de référence.

### Étape 8 — Publier sur Blotato

1. `blotato_list_accounts` pour retrouver le bon compte (ex. `automatisationboost` sur Instagram, comptes TikTok existants) — **toujours confirmer avec l'utilisateur quel compte/plateforme cibler** avant de publier, la publication est visible publiquement et irréversible.
2. Uploader le MP4 rendu (`blotato_create_presigned_upload_url` + upload, ou `blotato_create_visual` selon le cas) pour obtenir une URL média Blotato.
3. `blotato_create_post` avec la légende = `Texte TikTok + Hashtags` de la ligne du Sheet, en respectant les champs requis par plateforme (ex. TikTok : `privacyLevel`, `disabledComments`, etc. — voir `requiredFields` renvoyés par `blotato_list_accounts`).
4. Rapporter l'URL/ID du post à l'utilisateur. Mettre à jour manuellement `Statut Tournage` → `✅ Fait`, `Vidéo Finale` et `Date Publication` dans le Sheet (lecture seule depuis ce skill, l'utilisateur ou un outil Sheets fait l'écriture).

---

## Règles Captions

- Maximum trois mots par phrase de caption si possible.
- Un seul mot actif surligné par phrase.
- Jaune néon pour les mots de force/valeur, violet pour transformation/IA, orange pour actions/CTA.
- Doit rester lisible sur mobile et passer `hyperframes inspect` avec 0 dépassement/occlusion de texte.

## Règles Avatar

- Avatar keyé propre ou composite setup sans filtres latéraux vert/noir.
- Toujours sous la bande de sécurité des captions pour les vidéos split verticales.
- Pop-up avatar circulaire éventuel : anneau rotatif jaune, affiché seulement sur les beats d'emphase.
- Valider que l'avatar ne recouvre jamais les captions ni le texte important de la scène.

---

## Checklist finale

- [ ] Ligne du Sheet identifiée et infos récupérées (script, hashtags, mot-clé CTA)
- [ ] Consentement voix clonée obtenu explicitement avant tout appel WaveSpeed
- [ ] Palette noir mat + jaune/violet/orange respectée, pas de bleu dominant
- [ ] Captions TikTok mot-à-mot validées (0 dépassement `inspect`)
- [ ] Avatar sans filtre vert/noir, ne recouvre jamais captions/texte
- [ ] `validate` + `inspect` = 0 problème avant rendu
- [ ] Rendu vérifié via `ffprobe` (durée, résolution, taille)
- [ ] Compte Blotato confirmé avec l'utilisateur avant publication
- [ ] Post publié sur Blotato, URL/ID rapporté à l'utilisateur
- [ ] Sheet à mettre à jour manuellement (statut, vidéo finale, date de publication)

---
name: avatar-reel
description: Vidéo Reel verticale ~30s avec avatar parlant (voix clonée) en PiP circulaire, structure Hook/Problème/Solution/Résultat/CTA, captions TikTok mot-à-mot, publiée sur GitHub + Coolify pour automatisationboost.com. Reconstruit à partir des notes Notion après perte du skill original (crash VPS).
---

# avatar-reel

**Input :** sujet/brief (ou texte fourni), échantillon de voix, source avatar (Kie.ai ou vidéo portrait pré-rendue)
**Output :** MP4 1080×1920, ~30s, avatar PiP circulaire + captions TikTok, uploadé sur GitHub (`tonyPayetDev/automationboost`) et redéployé sur Coolify

> **Note de reconstruction :** ce skill existait avant un crash VPS qui a effacé toute la session Claude Code où il avait été bâti. Ce fichier est reconstruit le 2026-07-06 à partir des notes de projet Notion (pipeline marqué "Terminé 🙌" le 2026-06-29), du code réel et déployé du repo GitHub `tonyPayetDev/avatar-api-webhook` (service `https://avatar-api.automatisationboost.com`), et des détails encore présents dans `/work/CLAUDE.md`. À affiner/corriger si des détails ont changé depuis.
>
> ⚠️ Plusieurs itérations de ce pipeline coexistent dans le repo/l'historique : un vieux workflow n8n local (`avatar-api-workflow-n8n.json`, GPT-4 + ElevenLabs, probablement obsolète), un brouillon local (`avatar-api-webhook.js`, `composeVideo` simulé), et la version réellement déployée sur GitHub (ffmpeg réel, `avatar-api.automatisationboost.com`). C'est cette dernière qui fait foi ci-dessous.

---

## Différence avec `veille-to-video`

Les deux pipelines partagent la même palette d'outils (HyperFrames, WaveSpeed, captions TikTok) mais ne servent pas le même besoin :

- **`avatar-reel`** (ce skill) : reel démonstratif/pédagogique avec un avatar qui "parle" en PiP circulaire par-dessus une démo/visuel, structure narrative fixe Hook→Problème→Solution→Résultat→CTA, ~30s.
- **`veille-to-video`** (Autoboost Neon Video) : promo sociale pilotée par un Google Sheet de suivi, palette néon jaune/violet/orange, ~18-20s, publication directe via Blotato.

Ne pas confondre les deux durées cibles : 30s ici, pas 18-20s.

---

## Style obligatoire

- **Format** : 1080×1920 vertical, 30fps.
- **Structure narrative (30s)** :
  - Hook : 0-3s (accroche forte — question ou stat choc)
  - Problème : 3-8s (pain point concret)
  - Solution : 8-20s (la technique/l'outil + comment ça marche)
  - Résultat : 20-27s (bénéfice chiffré)
  - CTA : 27-30s (appel à l'action direct)
- **Avatar PiP** : cercle, ~440×580px, `object-position: top`, `border-radius: 28px`, bordure or (overlay circulaire ffmpeg). N'apparaît qu'aux moments pertinents (pas en continu) — dans la version validée : deux fenêtres (ex. 3s-8s et 22s-27s).
- **Captions TikTok** : texte blanc MAJUSCULES, un mot actif en surbrillance jaune néon `#EAB308`, `-webkit-text-stroke` 3px noir, taille ~74px, centrées en bas de l'écran.
- **Background** : composition HyperFrames à plusieurs scènes (6 dans la version validée), transitions GSAP (push/zoom/blur) — pas de diapositives statiques façon PowerPoint.

---

## Workflow

### Étape 0 — Consentement voix clonée

Avant tout appel à un service de voix clonée (WaveSpeed ou autre), exiger un texte explicite de l'utilisateur, ex. :
`J'autorise l'envoi de mon échantillon de voix pour générer l'audio de cette vidéo ...`
Ne jamais appeler l'API voice-clone sans ce consentement. Ne jamais afficher/logguer les clés API.

### Étape 1 — Rédiger la narration

Découper selon la structure Hook/Problème/Solution/Résultat/CTA ci-dessus. Français, ton énergique et concis, proche du débit des captions.

Template de prompt réutilisable (issu des notes Notion) pour cadrer une nouvelle vidéo :

```
TOPIC: [sujet de la vidéo]
DURÉE: 30 secondes
STRUCTURE:
- Hook 0-3s: [accroche forte — question ou stat choc]
- Problème 3-8s: [pain point concret]
- Solution 8-20s: [la technique/outil + comment ça marche]
- Résultat 20-27s: [bénéfice chiffré]
- CTA 27-30s: [appel à l'action direct]
VOIX: voixUrl = [URL accessible d'un échantillon de voix]
AVATAR: [URL vidéo portrait pré-rendue, ou paramètres Kie.ai]
SOUS-TITRES: style TikTok — texte blanc MAJUSCULES, mot en surbrillance jaune néon #EAB308, contour noir épais 3px, taille 74px, centré bas
MISE À JOUR: uploader GitHub (tonyPayetDev/automationboost, ressources/videos/[nom-fichier].mp4) et redéployer Coolify
```

### Étape 2 — Générer l'audio (voix)

- **Principal** : WaveSpeed AI direct, `wavespeed-ai/qwen3-tts/voice-clone` (pas `omnivoice`, déprécié). Compter ~3 min de rendu pour 80 mots de narration.
- **Fallback** : webhook n8n `/webhook/tts-gen` (workflow ID `6InNNRjMJxiteEkV`).
- Sauvegarder le résultat en local puis copier vers `public/assets/voice.mp3` (ou équivalent) du projet HyperFrames.

### Étape 3 — Obtenir le clip avatar

Deux options, selon le niveau de qualité/contrôle voulu :

- **Option A — service webhook automatisé (rapide, sans design custom)** : appeler le service réellement déployé et vérifié (`tonyPayetDev/avatar-api-webhook`, code Node.js, `ffmpeg` réel) :

  ```bash
  curl -X POST https://avatar-api.automatisationboost.com/avatar/generate \
    -H "Content-Type: application/json" \
    -d '{
      "avatarUrl": "https://.../avatar.mp4",
      "voiceUrl": "https://.../voice.mp3",
      "topic": "sujet de la vidéo",
      "userEmail": "tony.payet.professionnel@gmail.com",
      "avatarScale": 0.35
    }'
  ```

  Réponse : `{"status":"success","data":{"videoUrl":"...","email":{"to":"...","status":"sent"}}}`. En interne : télécharge `avatarUrl`/`voiceUrl`, recadre l'avatar à `avatarScale` (0.0-1.0, défaut 0.35) de sa taille en conservant le ratio, le centre sur un canevas noir 1080×1920, mixe l'audio, puis notifie par email. **Limite connue** : pas de PiP circulaire, pas de bordure or, pas de background HyperFrames multi-scènes — juste l'avatar scalé et centré sur fond noir. `GET https://avatar-api.automatisationboost.com/health` pour vérifier que le service répond avant d'appeler `/avatar/generate`. Le champ `topic` déclenche un `searchClaudeInfo()` qui, dans le code déployé, ne fait **que renvoyer des tips codés en dur** (pas un vrai appel IA) — ne pas compter dessus pour du contenu réel.

- **Option B — composition manuelle HyperFrames (qualité premium, PiP circulaire + background designé)** : ce que décrit la suite de ce document (étapes 4-8), utilisée pour les Reels avec un vrai habillage visuel (bordure or, transitions GSAP, background multi-scènes). Plus lent, plus de contrôle. Source vidéo avatar : fichier pré-rendu (ex. `video_portrait_*.mp4`) ou export d'un service tiers.
  - Détourage fond vert si besoin : filtre `geq` (pas `chromakey`), recadrer en carré avant le masque, crop depuis `y=0`, dé-spill du canal vert pour retirer la frange verte résiduelle.
  - Compositing PiP circulaire : masque circulaire + bordure or via ffmpeg (`overlay` + mask), taille ~440×580px.

### Étape 4 — Construire la composition HyperFrames

- Racine `1080×1920`, `data-duration` = durée réelle du montage (viser 30s, ajuster sur la durée audio réelle mesurée via `ffprobe`).
- **Piège connu** : `data-start` est requis explicitement sur chaque `<video>` (sinon désync). La clé d'enregistrement de la timeline `window.__timelines[...]` doit être une **string littérale**, pas une variable.
- 6 scènes avec transitions GSAP (push/zoom/blur) plutôt que des cuts secs.
- Avatar en overlay PiP sur les fenêtres temporelles pertinentes uniquement (`data-start`/`data-duration` dédiés), jamais en continu sur toute la vidéo.
- **Travailler dans le scratchpad**, pas directement sous `/work/videos` (peut être root-owned → permission denied).

### Étape 5 — Mixer l'audio

- Si background et voix sont deux pistes séparées : mixer via un endpoint dédié (`{videoUrl, audioUrl}` → vidéo finale) si disponible, sinon `ffmpeg -filter_complex amix` / `amerge` en local.
- Pour les boucles vidéo de fond : utiliser `-stream_loop -1 -t DUR` sur l'input (pas de `trim` dans le filtergraph).

### Étape 6 — Transcript & captions

- Si une clé Whisper/ASR est disponible : transcription mot-à-mot avec timestamps réels.
- Sinon : estimation en Python, durée proportionnelle au nombre de caractères par phrase (dernier recours, moins précis — resynchroniser manuellement si besoin).
- Rendu captions TikTok : voir style ci-dessus (§ Style obligatoire).

### Étape 7 — Valider puis rendre

```bash
npx -p node@22 -p hyperframes hyperframes validate public --json
npx -p node@22 -p hyperframes hyperframes inspect public
npx hyperframes render
ffprobe -v quiet -show_entries format=duration,size -of default=noprint_wrappers=1 public/renders/*.mp4
```

Corriger tout dépassement de captions ou désync avant de considérer le rendu final.

### Étape 8 — Déployer

- Uploader le MP4 final sur GitHub : `tonyPayetDev/automationboost`, chemin `ressources/videos/[nom-fichier].mp4`.
- Redéployer Coolify (forcer le redeploy de l'app concernée — voir `docs/freelance-sites-mapping.md` pour les UUIDs d'environnement si le mapping a changé).

---

## Sécurité

- Ne jamais afficher ni committer de clé API en clair (WaveSpeed, Kie.ai, etc.).
- Consentement voix clonée obligatoire à chaque nouvelle vidéo, pas seulement à la première utilisation.

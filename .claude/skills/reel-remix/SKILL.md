---
name: reel-remix
description: Reel Remix — analyse un reel viral (Instagram/TikTok) via TokScript, en extrait la structure (hook, beats, CTA, rythme), réécrit un script neuf dans la voix Autoboost, et produit une vidéo 9:16 (panneau haut screen record OU schéma motion-design + avatar/voix clonée en bas + captions TikTok), rendue avec HyperFrames et publiée sur Blotato. Ne republie jamais le script ni le rush de la source.
---

# reel-remix — cloner le FORMAT d'un reel viral, pas son contenu

**Input :** une URL de reel Instagram ou TikTok (+ le sujet équivalent côté Autoboost)
**Output :** projet HyperFrames (`public/index.html`) + MP4 1080×1920 + post Blotato

**Pipeline complet, dans l'ordre :** ingérer (É0) → extraire la structure (É1) → script neuf (É2) →
panneau du haut (É3) → voix clonée + timestamps (É4) → composition (É5) → valider (É6) → rendre et
vérifier visuellement (É7) → publier (É8). Ne jamais sauter É1 : c'est l'étape qui transforme une
copie en remix.

Skill frère de `veille-to-video` : **toutes les règles de style, captions, avatar, sound design,
rendu et publication de `/veille-to-video` s'appliquent ici sans exception.** Ce document ne décrit
que ce qui change — l'ingestion du reel source, la réécriture du script, et le layout split-screen.
Lire `.claude/skills/veille-to-video/SKILL.md` en parallèle, ne pas dupliquer ses règles ici.

**Implémentation de référence :** `autoboost-neon-videos/autoboost-18-voice-clone/` — projet complet
produit avec ce skill (voir son `brief.md` pour l'extraction de structure et son `NOTES.md` pour les
pièges rencontrés et leurs correctifs).

---

## Règle fondatrice — on clone le format, jamais le contenu

Un reel viral vaut pour sa **structure** : la promesse du hook, l'ordre des bénéfices, le rythme des
coupes, la mécanique du CTA. Ça, ça se réutilise librement, c'est du format.

Ce qui ne se réutilise pas :

- **Le script mot pour mot.** Le transcript TokScript est une matière d'analyse, pas un texte à
  faire relire par ta voix clonée. Reformuler « en changeant quelques mots » est la même faute en
  pire — c'est du plagiat déguisé, ça se repère, et l'algo pénalise le contenu dupliqué.
  → Étape 2 produit un script **neuf**, avec ton angle, tes exemples, ton offre.
- **Le rush de la source** (le clip du haut, ses screen records, sa musique). C'est son tournage.
  → Étape 3 filme **ton propre** screen record, ou prend un clip Mixkit sous licence.
  (De toute façon `download_video` de TokScript est réservé aux comptes Pro/Premium — le compte
  actuel ne peut pas télécharger le MP4 source. Le transcript, lui, passe en gratuit : 5/jour.)

Si l'utilisateur demande explicitement une reprise mot pour mot ou la réutilisation du rush source,
le dire clairement une fois et proposer l'alternative ci-dessus. Ne pas produire la copie.

---

## Workflow

### Étape 0 — Ingérer le reel source

| Plateforme | Outil MCP |
|---|---|
| Instagram | `mcp__claude_ai_tokscript__get_instagram_transcript` (`format: "json"`) |
| TikTok | `mcp__claude_ai_tokscript__get_tiktok_transcript` |
| YouTube Short | `mcp__claude_ai_tokscript__get_youtube_transcript` |
| ≥ 2 URLs | `submit_transcript_job` puis `get_job_status` — **jamais** N appels unitaires |

Nettoyer l'URL Instagram avant l'appel : garder `https://www.instagram.com/reel/<id>/`, jeter le
`?igsh=...` (paramètre de tracking, inutile et bruyant dans les logs).

Le retour donne `title` (= la légende du post, souvent le meilleur résumé de l'angle),
`author`, `hashtags`, `publishDate` et `transcript.segments[]` avec `start`/`end`/`text`.
Les `stats` (vues, likes) sont presque toujours `null` côté Instagram — ne pas s'appuyer dessus
pour juger si le reel a marché, et ne pas le présenter comme une donnée.

**Le transcript est une transcription auto : elle contient des fautes de reconnaissance vocale.**
Vu en pratique : « Cloud » = *Claude*, « iFeel » = *Higgsfield*, « voix offres » = *voix off*.
Toujours corriger mentalement les noms propres avant d'analyser, et ne jamais recopier ces
coquilles dans le script final.

### Étape 1 — Extraire la structure (le seul livrable réutilisable)

Produire un `brief.md` court dans le dossier du projet, qui capture **la mécanique** et rien du
texte source :

```markdown
# Source
Reel <url> — @<auteur> — <durée>s — <date>

# Structure
- Hook (0-Xs)      : <quelle promesse, quel type de hook — capacité inédite / avant-après / chiffre / erreur>
- Beats (X-Ys)     : <N bénéfices listés, dans quel ordre, un par plan>
- Climax (Y-Zs)    : <le "et le plus impressionnant..." — quel argument est gardé pour la fin>
- CTA (Z-fin)      : <mécanique : commenter un mot-clé / lien bio / DM>
- Rythme           : <mots/seconde, longueur moyenne d'un beat, nb de coupes>
- Layout           : <split-screen top/bottom, plein écran, screencast+face cam...>

# Angle Autoboost équivalent
<le même format appliqué à TON produit / workflow n8n / offre — pas au sien>
```

C'est ce `brief.md` qui alimente l'étape 2, **pas** le transcript brut. Une fois le brief écrit, le
transcript source n'est plus rouvert.

### Étape 2 — Écrire un script neuf

Contraintes : français, hook en 1 phrase, un bénéfice par beat, CTA sur un mot-clé à commenter
(colonne `Mot-clé CTA` du Sheet de suivi).

**Longueur cible : 100-115 mots pour 30-35s.** Le débit réel de la voix clonée de marque est de
**~3.3 mots/s** — mesuré sur l'audio effectivement rendu (autoboost-18 : 121 mots → 36.4s), pas les
3.7-4.1 mots/s supposés dans `/veille-to-video`. Avec l'ancienne hypothèse on dépasse
systématiquement les 35s. Recalculer avec 3.3, et si l'audio revient quand même trop long, resserrer
le script et régénérer plutôt que d'accélérer l'audio (`atempo` s'entend).

**Piège TTS sur le CTA — vérifié 2026-07-11.** Écrire `Commente VOIX` fait prononcer « Commande
voix » par le TTS (confirmé par la transcription Whisper du MP3 généré). Le CTA est la ligne la plus
importante de la vidéo : toujours écrire **`Commente le mot <MOTCLÉ>`**, jamais `Commente <MOTCLÉ>`
collé. Ça lève l'ambiguïté pour le TTS et ça sonne mieux à l'oral.

Le script doit passer ce test avant TTS : **aucune phrase du transcript source ne doit s'y retrouver,
ni telle quelle ni en synonymes**. Le sujet peut être le même (ex. « générer de l'audio dans Claude »),
l'angle et les mots sont les tiens : ton workflow n8n, ton cas client Réunion, ton chiffre, ton offre.
En cas de doute sur une phrase, la réécrire depuis le bénéfice, pas depuis la phrase source.

Si le sujet du reel source correspond à une ligne du Google Sheet de suivi (`⬜ À faire`), reprendre
le script et le mot-clé CTA **de la feuille** — ils sont déjà écrits pour ta marque. Voir Étape 0 de
`/veille-to-video`.

### Étape 3 — Le panneau du haut

Le layout cible reproduit le format qui marche : **vidéo/démo en haut, avatar parlant en bas**.
Trois sources possibles pour le panneau du haut, dans cet ordre de préférence :

1. **Ton propre screen record** — la meilleure option quand le reel démontre un outil (Claude, n8n,
   un MCP...). Filmer l'écran en 1080×1920 ou 1920×1080, 20-40s, le geste réel. C'est aussi ce qui
   rend la vidéo défendable : tu montres que TU sais le faire.
2. **Un clip Mixkit** (licence Mixkit Free, commercial, sans attribution) — méthode de scraping
   JSON-LD documentée dans `/veille-to-video` § Sound design / broll.
3. **Un schéma motion-design HyperFrames** (cartes, flèches, dashboard animé) quand aucune démo
   n'existe — pattern « premium SaaS » de `references/premium-saas-launch.md`.

Jamais le rush de la source (voir Règle fondatrice).

**Si le panneau du haut est un schéma motion-design (option 3), il n'y a PAS de `#top-panel` à
construire** : le haut du canevas est déjà la zone `.scene` (1120px) de l'architecture
`/veille-to-video` standard, et le schéma animé EST la scène. Ne pas empiler un `<div id="top-panel">`
par-dessus — reprendre `/veille-to-video` Étape 5 tel quel et animer le schéma dans les `.scene`.
Le bloc `#top-panel` ci-dessous ne sert qu'aux options 1 et 2 (vrai fichier vidéo en haut).

Schéma qui marche pour un pipeline (autoboost-18) : une rangée horizontale de 4 nœuds
(`Ton texte → n8n → Clonage vocal → MP3`) avec liens fléchés, puis **un point lumineux qui parcourt
la chaîne** en s'arrêtant sur chaque nœud (qui s'allume à son passage). C'est ce déplacement qui rend
le schéma vivant — un simple stagger d'apparition des cartes retombe à plat.

**Recadrer une source vers le panneau haut (1080×1120)** :

```bash
# source 9:16 (1080x1920) -> garder la moitié haute
ffmpeg -i source.mp4 -vf "crop=1080:1120:0:0" -an -c:v libx264 -crf 23 top-panel.mp4

# source 16:9 (1920x1080) -> letterbox propre dans le panneau
ffmpeg -i source.mp4 -vf "scale=1080:-2,pad=1080:1120:0:(1120-ih)/2:black" -an -c:v libx264 -crf 23 top-panel.mp4

# étendre à la durée de la comp si le clip est plus court (sinon il gèle silencieusement)
ffmpeg -stream_loop -1 -t <durée comp> -i top-panel.mp4 -c copy top-panel-loop.mp4
```

Toujours `-an` : l'audio du panneau doit être muet, la seule voix de la vidéo est la tienne.

### Étape 4 — Voix clonée

Consentement voix : **déjà donné de façon permanente** par Tony (2026-07-09, « j'autorise mais
autorise toujours ») — ne pas le redemander à chaque vidéo. Génération via WaveSpeed
`wavespeed-ai/qwen3-tts/voice-clone`, ou les webhooks n8n `tts-gen` / `avatar-webhook-v2` depuis ce
sandbox. Préférer `avatar-webhook-v2` : il renvoie en plus les vrais timestamps Whisper mot-à-mot
pour les captions. Détails complets, pièges et fallbacks : `/veille-to-video` Étapes 3-4.

Payload (workflow `S85QlXjhIO6nBvzY`, webhook `avatar-webhook-v2`) :

```json
{
  "avatarUrl": "https://assets.automatisationboost.com/video/avatar/auto%20avatar%20(online-video-cutter.com).mp4",
  "voixUrl": "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3",
  "description": "<le script>",
  "userEmail": "tony.payet.professionnel@gmail.com"
}
```

**`curl` renverra presque toujours `error code: 524`** (timeout Cloudflare à ~100s alors que
l'exécution dure ~2min). **Ce n'est pas un échec** : l'exécution n8n continue et aboutit. Ne pas
relancer le webhook — récupérer le résultat a posteriori :
`search_executions({workflowId: "S85QlXjhIO6nBvzY", limit: 5})` → prendre l'exécution `success`
correspondante → `get_execution({includeData: true, nodeNames: ["Respond to Webhook"]})` → le node
renvoie `{voiceUrl, transcripts}` (`transcripts` = paquets de 3 mots avec `start`/`end`).
Relancer en aveugle crée une 2ᵉ exécution inutile et double le coût WaveSpeed.

**`python3` n'existe pas dans ce sandbox** — utiliser `node` pour construire le payload JSON
(échapper le script à la main dans un `-d '...'` casse sur les apostrophes françaises).

**Le texte des captions vient du SCRIPT, pas de Whisper.** Whisper transcrit l'audio *généré* et se
trompe sur les noms propres et les mots-clés (« Commande voix » pour « Commente VOIX »). N'utiliser
de `transcripts` que les `start`/`end` ; réécrire les mots depuis `narration.txt`.

### Étape 5 — Composition HyperFrames split-screen

Reprendre **toute** l'architecture de `/veille-to-video` Étape 5 (racine 1080×1920, timeline GSAP
unique en pause, `<audio id="voice">`, captions TikTok mot-à-mot, avatar en overlay persistant
sibling des `.scene`). Le seul delta : le haut du canevas n'est plus une `.scene` motion-design mais
un panneau vidéo fixe.

```html
<div id="top-panel">
  <video id="top-clip" src="assets/top-panel.mp4"
         data-start="0" data-duration="<durée totale comp>"
         muted playsinline></video>
</div>
```

```css
#top-panel {
  position: absolute; top: 0; left: 0;
  width: 1080px; height: 1120px;
  overflow: hidden; background: var(--bg);
  border-bottom: 3px solid var(--accent-yellow);
  box-shadow: 0 6px 40px rgba(255, 230, 0, 0.18);
  z-index: 1;
}
#top-panel video {
  width: 100%; height: 100%;
  object-fit: cover;
  filter: brightness(0.92);
}
```

Rappels qui coûtent cher si on les oublie (tous vérifiés en production, cf. `/veille-to-video`) :

- **Ne PAS ajouter une règle `video { display: none }`** pour cacher les `<audio>` — elle tuerait
  silencieusement `#top-clip` ET `#avatar`. Écrire `audio { display: none; }` seul.
- **Chaque `<audio>` a un `id` unique**, même les SFX (sinon `media_missing_id` → piste muette
  dans le MP4, sans erreur visible).
- **Captions à `top: 960px`** — la bande de sécurité entre le bas du panneau (1120px) et le cercle
  avatar. Sur ce layout la marge est plus serrée que sur une comp `veille-to-video` classique :
  revalider `inspect` après tout changement de taille de police.
- **Avatar** : overlay persistant, visible sur la majorité de la vidéo (4-5 apparitions minimum),
  masqué uniquement pendant les fenêtres broll plein écran. Parité `repeat` IMPAIR sur les tweens
  yoyo du ring avant un masquage.
- **Pas d'emoji** (aucune police emoji dans ce sandbox → tofu `NO GLYPH`). Icônes SVG inline.

### Étapes 6-8 — Valider, rendre, publier

Strictement identiques à `/veille-to-video` Étapes 6-7-8 : exports `PATH`/`LD_LIBRARY_PATH`/
`FONTCONFIG_PATH`, `hyperframes validate` + `inspect` à 0 problème, rendu en arrière-plan,
**vérification visuelle de frames extraites** (`ffprobe` ne voit pas le bug fontconfig), puis
upload presigned + `blotato_create_post` après confirmation du compte cible avec l'utilisateur.

---

## Checklist finale

- [ ] Reel source ingéré via TokScript, coquilles de transcription auto corrigées
- [ ] `brief.md` écrit — structure/rythme/CTA extraits, **transcript source refermé ensuite**
- [ ] Script neuf : aucune phrase de la source, angle et exemples Autoboost, 100-115 mots (≈3.3 mots/s)
- [ ] CTA écrit `Commente le mot <MOTCLÉ>` (sinon le TTS prononce « Commande »)
- [ ] Voix récupérée via `get_execution` après le 524 attendu — pas de relance du webhook
- [ ] Texte des captions repris du script, timestamps repris de Whisper
- [ ] Panneau haut = screen record maison / Mixkit / schéma — **jamais le rush de la source**
- [ ] Panneau haut muet (`-an`) et loop-étendu à la durée de la comp
- [ ] Pas de règle CSS `video { display: none }`, tous les `<audio>` ont un `id`
- [ ] Captions à `top: 960px`, `inspect` = 0 dépassement sur le layout serré
- [ ] Avatar en overlay persistant, visible sur la majorité de la vidéo
- [ ] Rendu vérifié visuellement (frames extraites), pas seulement `ffprobe`
- [ ] Compte Blotato confirmé avant publication

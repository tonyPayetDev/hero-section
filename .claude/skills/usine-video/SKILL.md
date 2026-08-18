---
name: usine-video
description: >
  Orchestrateur de la chaîne vidéo AutomatisationBoost : connecte les 3 maillons
  (agent social-analytics → agent script-writer → skill veille-to-video → Blotato)
  pour qu'UNE vidéo se produise de bout en bout sans pilotage manuel. Utilise ce skill
  quand Tony dit : « fais une/des vidéo(s) », « lance l'usine à vidéos », « produis la
  prochaine vidéo », « connecte les agents », « regarde mes concurrents et crée N vidéos »,
  ou `/usine-video`. C'est le point d'entrée unique du pipeline de contenu.
---

# /usine-video — le raccord entre les agents

**Problème résolu :** les 3 maillons existent mais rien ne les enchaîne. Résultat : Tony
déclenche chaque étape à la main (« regarde mes concurrents », « écris des scripts »,
« produis la vidéo », « planifie-la »). Ce skill est le **chef d'orchestre** : un seul
appel fait passer le flux d'un bout à l'autre, avec des garde-fous d'état pour ne rien
refaire inutilement ni créer de doublon.

## La chaîne (bus central = le Google Sheet de suivi)

```
[social-analytics]  → STRATEGIE.md + onglet "Analyse Perf"        (les apprentissages)
        ↓
[script-writer]     → lignes "⬜ À faire" du Sheet principal       (la file de scripts)
        ↓
[veille-to-video]   → MP4 rendu (HyperFrames + voix + captions)   (la production)
        ↓
[validation]        → Sheet "✅ Validé" → workflow soNcMKsz1ce7yDhA → Blotato (planif)
```
Sheet : `10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags`
(onglet principal `veille-to-video` lit `Statut Tournage`; onglet `Analyse Perf` gid `1277122579`).

## Paramètres d'appel
- `N` = nombre de vidéos à produire ce run (défaut **1**).
- `sujet`/`brief` optionnel : si Tony donne un angle précis (ex. « music horror + son »),
  le passer tel quel au script-writer / veille-to-video ; sinon laisser les agents décider
  depuis STRATEGIE.md.

## Procédure — 4 étapes à garde-fou (idempotentes)

### État initial (avant tout)
1. Lancer `/etat` (ou `node /work/.claude/skills/etat/status.mjs`) pour l'état des rendus /
   déploiements / Blotato en cours — ne pas produire si un rendu identique tourne déjà.
2. Connaître la profondeur de file `⬜ À faire` et la fraîcheur de STRATEGIE.md :
   `head -8 /work/STRATEGIE.md` donne la date d'analyse ; le nombre de lignes `⬜` se lit
   en demandant au script-writer de le rapporter (il lit le Sheet en Step 1) OU via n8n.

### Étape A — Apprentissages (agent `social-analytics`)
- **Gate :** ne relancer QUE si STRATEGIE.md date de **> 7 jours** ou si Tony le demande
  explicitement. Sinon **sauter** (les apprentissages sont encore frais).
- Spawn l'agent `social-analytics`. Il réécrit STRATEGIE.md + l'onglet Analyse Perf.
- Attendre sa fin avant l'étape B (le script-writer lit ces sorties).

### Étape B — Scripts (agent `script-writer`)
- **Gate :** ne lancer QUE si la file `⬜ À faire` est **< max(N, 3)**. Sinon sauter : il y a
  déjà des scripts prêts, on produit directement.
- Spawn `script-writer` (packet : « applique le dernier STRATEGIE.md, écris `N+2` scripts
  en `⬜ À faire`, un angle par script, pas de doublon avec les lignes existantes »).
  Si Tony a donné un brief, le transmettre comme angle imposé du 1er script.
- Il **append** des lignes (jamais d'écrasement ; cible par `row_number` physique, la
  colonne `#` est décalée). Vérifier via l'export CSV que les lignes ont atterri.

### Étape C — Production (skill `veille-to-video`, N fois) — « la vidéo se fait »
- Pour chaque vidéo à produire (jusqu'à `N`) :
  1. Choisir la prochaine ligne `⬜ À faire` (script voix off + texte TikTok + mot-clé CTA).
  2. Invoquer le skill `veille-to-video` sur cette ligne → projet HyperFrames + **MP4 rendu**.
  3. Publier le rendu sur previsualisation (hook Stop automatique) pour validation au tel.
  4. Passer la ligne à `🎬 En cours`/`✅` selon la convention veille-to-video.
- **C'est l'étape qui manquait** : sans elle, les scripts restaient en file sans jamais
  devenir des vidéos. Elle tourne sur le thread principal (rendu lourd ~10-15 min/vidéo) —
  ne pas la déléguer à un sous-agent (toolchain hyperframes locale).

### Étape D — Planification (Blotato)
- Une fois validé par Tony (`✅ Validé` dans le Sheet), le workflow n8n `soNcMKsz1ce7yDhA`
  programme TikTok 18h + IG 18h29. Vérifier la planif via `blotato_list_schedules`
  (c'est ce que `/etat` affiche). Ne pas re-planifier une date déjà couverte
  (voir [[feedback_check_existing_schedule_before_posting]]).

## Règle de fin
Terminer par un récap français : quelle(s) étape(s) ont tourné vs sautées (avec la raison
du gate), le row_number produit, le lien previsualisation, et l'état de la file `⬜` restante.
Si un rendu est lancé en tâche de fond, le dire — ne jamais prétendre une vidéo finie non vérifiée.

## Notes de câblage (pièges connus)
- `veille-to-video` est un **skill** (thread principal), pas un agent → l'orchestrateur
  l'exécute lui-même après avoir spawné les 2 agents amont. C'est ça, « connecter les agents ».
- Incohérence à corriger un jour : `social-analytics.md` cible `@tonypayet4` (0 donnée) alors
  que le compte réel alimenté est `@automationboost7` — voir l'alerte en tête de STRATEGIE.md.
- Déclenchement : le point d'entrée est **manuel** (`/usine-video`) ou par une session Claude
  planifiée. Un cron in-session (CronCreate) ne survit pas à la fermeture de la session : pour
  un run hebdo VRAIMENT autonome, il faut un cron système sur le VPS qui lance
  `claude -p "/usine-video N=3"` en headless (toolchain hyperframes locale requise), pas un
  cron en mémoire. Toute la logique vit ici ; le déclencheur ne fait qu'appeler ce skill.
- Sûr : les agents amont n'écrivent que dans le Sheet (append) et STRATEGIE.md ; aucune
  publication sociale n'est faite sans le `✅ Validé` de Tony.

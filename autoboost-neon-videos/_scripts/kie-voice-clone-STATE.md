# État — Clone voix chantée Tony (Kie.ai / Suno)

Mis à jour le **2026-08-16 (soir)** après un diagnostic API complet.
But : créer un `voiceId` Suno de la voix chantée de Tony, réutilisable pour toutes les chansons.

---

## STATUT : cause racine TROUVÉE et PROUVÉE

**La phrase de vérification expire entre 151 s et 181 s après être devenue lisible** — en clair, **~3 minutes**.
Ce n'est ni la qualité de la prise de Tony, ni le fait que la source soit parlée,
ni une tâche « périmée depuis des heures ». C'est une fenêtre de **2 à 3 minutes**, point.

Tout ce qui était écrit ici avant (« ~15 min », « la tâche meurt toute seule au bout d'une heure »,
« `wait_validating` est un statut périmé ») était **faux**. Les 4 échecs s'expliquent par un seul
fait : entre le tirage de la phrase et l'envoi du chant, il s'est écoulé plus de 3 minutes.

### Mesures réelles (2026-08-16, ~19h45-20h00 UTC)

Protocole : `validate` → attendre `wait_validating` → attendre N secondes → `voice/generate`
avec un audio **volontairement faux** (Tony chantant une autre phrase) → `record-info`.
L'audio étant toujours le même, la seule variable est le délai.

| Délai après phrase prête | Résultat au polling |
|---|---|
| ~20 s | `generating_voice` puis **« It didn't sound like you said the phrase »** |
| 61 s | **« It didn't sound like you said the phrase »** |
| 121 s | **« It didn't sound like you said the phrase »** |
| **151 s** | **« It didn't sound like you said the phrase »** ← encore valide |
| **181 s** | **« Verification phrase expired or not found »** ← mort |
| 421 s | **« Verification phrase expired or not found »** |

**Fenêtre encadrée : valide à 151 s, morte à 181 s.** Budget de sécurité retenu : **150 s**.

→ **Deux messages d'erreur DISTINCTS, et c'est toute la clé du diagnostic.**

- `It didn't sound like you said the phrase. Please try reading it more clearly.`
  = la phrase était **encore valide**, le pipeline est allé jusqu'au bout, c'est l'audio qui
  ne correspondait pas. **C'est le message qu'on veut voir** quand on se trompe de prise.
- `Verification phrase expired or not found. Please request a new phrase.`
  = on a dépassé la fenêtre. L'audio n'a même pas été écouté.

Les tentatives bloquantes ont donné le **second** message → elles n'ont jamais atteint la
comparaison audio. La prise de Tony n'a donc jamais été jugée sur ces tentatives-là.
(Le seul « didn't sound like » historique venait d'un test volontaire avec une prise
« proche mais différente » — refus normal et attendu, pas un problème de voix.)

---

## Hypothèses testées et ÉLIMINÉES

| Hypothèse | Test | Verdict |
|---|---|---|
| La source `voiceUrl` doit être **chantée** (la nôtre était parlée) | `validate` avec `archiviste_ZIl7EoOf.mp3` (parlé) puis `generate` à t+16 s | **FAUX** — arrive normalement jusqu'à l'erreur ASR. Parlé ou chanté, aucune différence sur la validation. Ça ne joue que sur la qualité du clone final. |
| Créer une nouvelle tâche `validate` invalide la précédente | T1 et T2 créées coup sur coup, puis `generate` sur T1 | **FAUX** — T1 est passée en `generating_voice` sans problème. Les tâches sont indépendantes. |
| On peut retomber sur une phrase déjà enregistrée en relançant | 12 tirages supplémentaires | **FAUX** — 12 phrases toutes différentes (LLM). Total ~20 tirages, 0 répétition. Abandonner définitivement. |
| On peut créer la persona sans phrase, depuis un audio uploadé | `add-instrumental` puis `extend` puis `generate-persona` | **FAUX** — voir ci-dessous. |
| `voice/regenerate` récupère une tâche | déjà testé | **FAUX** — `422 The record is not found or does not need to be rebuilt`. |

### Le chemin « persona sans phrase » n'existe pas — prouvé

Séquence testée de bout en bout (24 crédits dépensés) :

1. `POST /api/v1/generate/add-instrumental` avec l'a cappella de Tony en `uploadUrl`
   → **SUCCESS**, taskId `b8716826954d0f4e99059167bc49d745`, `operationType: underpainting`.
2. `POST /api/v1/generate/generate-persona` sur ce taskId → **`422 Music does not exist`**.
3. `POST /api/v1/generate/extend` sur la piste obtenue → **SUCCESS**,
   taskId `017fb8d8810eece126fd7e577ae60eb9` (80 s).
4. `generate-persona` sur le taskId d'extend → **`422 Music does not exist`** (les deux audioId).
5. **Contrôle** : `generate-persona` sur « Pendant Que Tu Dors » (vrai `/api/v1/generate`)
   → **`200` + `personaId: 9fff47abbd1306d4ac9f31d6bada90c2`** (persona jetable « Control Probe »).

→ L'endpoint marche parfaitement, mais **uniquement sur une piste issue de `/api/v1/generate`**.
Or une piste `/api/v1/generate` est chantée par Suno, jamais par Tony.
**Une persona ne peut donc jamais porter la vraie voix de Tony.**
Le seul chemin vers sa voix reste `voice/validate` → `voice/generate` avec la phrase.

---

## Séquence officielle (doc Kie)

Base `https://api.kie.ai`, auth `Authorization: Bearer $KIE_API_KEY` (clé dans `/work/.kie.env`).

1. `POST /api/v1/voice/validate` — [doc](https://docs.kie.ai/suno-api/suno-voice-validate)
   `{ voiceUrl, vocalStartS, vocalEndS, language? , callBackUrl? }` → `{ taskId }` · **0 crédit**
2. `GET /api/v1/voice/validate-info?taskId=…` — [doc](https://docs.kie.ai/suno-api/suno-voice-validate-info)
   `processing_validate` (~15-20 s) puis `wait_validating` + `validateInfo` = la phrase.
   **⏱ le chrono de 2-3 min démarre ici.**
3. Tony chante la phrase → convertir → héberger (URL publique).
4. `POST /api/v1/voice/generate` — [doc](https://docs.kie.ai/suno-api/suno-voice-generate)
   `{ taskId, verifyUrl, voiceName?, description?, style?, singerSkillLevel? }`
   `singerSkillLevel` ∈ beginner (défaut) / intermediate / advanced / professional.
   La doc précise : *« recording the phrase in a singing voice rather than plain speech is
   recommended »* et *« clean acapella vocals usually produce the most accurate voice profile »*.
5. `GET /api/v1/voice/record-info?taskId=…` → `status: success` + `voiceId`.
   Statuts observés : `wait_validating` → `generating_voice` → `success` | `fail`.
6. Usage : `POST /api/v1/generate` avec `personaId: <voiceId>` + `personaModel: "voice_persona"`.

Persona (piste générée, ≠ clone de voix réelle) :
`POST /api/v1/generate/generate-persona` — [doc](https://docs.kie.ai/suno-api/generate-persona)
`{ taskId, audioId, name, description, vocalStart?, vocalEnd? }` → `{ personaId }`.

---

## Pièges confirmés

- **Un `generate` = un seul essai par tâche.** Après un échec (même « didn't sound like »),
  re-poster sur le même `taskId` renvoie `422 Validate record is not in valid status`.
  Si Tony rate sa prise → il faut **retirer une nouvelle phrase** et tout recommencer.
- **`code: 200` sur `voice/generate` ne veut rien dire** — l'échec n'apparaît qu'au polling,
  ~20-40 s plus tard.
- Une tâche `processing_validate_fail` est définitivement morte (`422` sur generate).
- **Coût : `validate`, `validate-info`, `record-info` et un `generate` raté = 0 crédit.**
  On peut donc réessayer autant de fois qu'on veut. `add-instrumental` et `extend` = 12 crédits chacun.
- Solde après diagnostic : **671,92 crédits** (695,92 − 24).

---

## Ce qu'il faut faire maintenant — procédure « live »

Script prêt : **`/work/autoboost-neon-videos/_scripts/kie-voice-clone-live.sh`**
Il tire la phrase, l'affiche, puis surveille un dossier et déclenche automatiquement
conversion + upload + `generate` dès qu'un fichier y atterrit (~5 s de latence de notre côté).

**Consigne pour Tony — il doit être PRÊT AVANT qu'on tire la phrase :**

1. Au calme, téléphone en main, appli dictaphone déjà ouverte.
2. On tire la phrase, on la lui envoie **immédiatement**.
3. Il la **chante** a cappella (pas parlée), 8-15 s, articulation nette.
   Phrase courte → la chanter 2 fois lentement pour atteindre 8 s.
4. Il envoie le fichier **tout de suite**. Total disponible : **~2 minutes**, marge de sécurité 150 s.
5. Si on rate la fenêtre : on retire une phrase (gratuit, 20 s) et on recommence. Autant de fois qu'il faut.

Ce qui change par rapport aux 4 tentatives précédentes : on ne lui demandait pas de chanter
au mauvais moment — on lui demandait de chanter une phrase **déjà morte** au moment où il chantait.

---

## Chanson générée (sans la voix clonée, en attendant)

- `POST /api/v1/generate` — modèle **V5**, `customMode: true`, `instrumental: false`, `vocalGender: "m"`,
  paroles complètes en `prompt`, style en `style`, `callBackUrl` obligatoire.
- Polling : `GET /api/v1/generate/record-info?taskId=…` — `TEXT_SUCCESS` (~1 min) puis `SUCCESS` (~1 min 15).
- Retourne **2 variantes** avec `audioUrl` (mp3) + `imageUrl` (cover). **12 crédits** la paire.
- « Pendant Que Tu Dors » — taskId `b2bb2893c31f8f38fd2bb4aa57a80505`,
  audioIds `1f22e7b9-a636-4eac-8b87-68225f253e86` / `a0706eb8-fbdf-4b05-bbe7-f03ac84cc791`
  → `/work/autoboost-neon-videos/_shared/music-tony/`
- Prévisualisation : https://previsualisation.automatisationboost.com/chanson-voix-tony
- À refaire avec `personaId` = voiceId dès que le clone est validé.

## Historique

- 2026-08-12 → 08-16 : 4 tentatives, toutes mortes sur « Verification phrase expired or not found ».
  Tâches mortes : `7fe30a0bb77c838224fe6229d26c5c93`, `4c33762b7ff40413f7d38d8874987d6e`,
  `43bdcf1073bc5cf1ecd2d783c43981e4`, `703f2f15fa987a295f5a0a60def660ce`.
  Diagnostic de l'époque (« timeout upstream », « fenêtre de 15 min ») : **erroné**.
- 2026-08-16 soir : diagnostic API complet, fenêtre mesurée à 120 s < T < 180 s,
  chemin persona éliminé, script `live` écrit. Tony n'a **pas** eu à réenregistrer pour ce diagnostic.

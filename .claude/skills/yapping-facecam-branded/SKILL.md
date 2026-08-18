---
name: yapping-facecam-branded
description: Vidéo sociale 9:16 "yapping" face caméra pour Automation Boost — talking-head qui capte l'attention par la tension, avec la structure hook brutal (0-2s) → promesse (2-5s) → pattern interrupt permanent → micro-yapping structuré (problème→tension→révélation→preuve→solution) → punchline mémorable. Règle d'or : une nouvelle info, émotion ou surprise TOUTES LES 2-4 SECONDES. Utilise la vraie banque avatar v3 (talking-head vivant), voix clonée rapide, captions mot-à-mot, musique duckée. Déclencheurs : "vidéo yapping", "face caméra", "talking head viral", "vidéo qui capte l'attention", "hook brutal", "format qui retient", "vidéo cash/punchy".
---

# yapping-facecam-branded — Talking-head "yapping" (Automation Boost)

**Input :** un sujet/angle + un mot-clé CTA (et le message DM associé).
**Output :** une vidéo 9:16 (25-40s) où Tony (avatar v3) parle face caméra, montée pour retenir jusqu'au bout, publiée sur previsualisation puis planifiée **sur les 5 réseaux** (voir [[feedback_always_5_social_networks]]).

Ce skill encode UNE conviction : **on ne cherche pas à parler beaucoup, on cherche à donner une nouvelle info / émotion / surprise toutes les 2-4 secondes.** Si un plan dépasse 4s sans rien changer, il est trop long.

---

## Style obligatoire (charte)
- **Format** : 1080×1920, 30 fps, 25-40s. Fond matte black `#0a0a0a` + néons jaune `#FFD700` / violet `#A855F7` / orange.
- **Avatar** : la **vraie banque v3** (`_shared/avatar-bank/clips/`, talking-head vivant lip-sync) — PAS l'avatar-hq statique. L'avatar est central (face caméra), pas juste une vignette. Son natif des clips **coupé** ; on n'entend que la voix clonée ([[feedback_avatar_mute_overlay_voice]]).
- **Voix** : voix clonée de Tony, **dynamique/rapide/claire** (atempo ≈1.12-1.15 + silences retirés, loudnorm I=-16). Ton cash, direct.
- **Captions** : TikTok mot-à-mot, 27px, un mot actif surligné or/violet, contour + ombre. Un segment à la fois.
- **Musique** : énergique/épique **duckée en sidechain** sous la voix (voix ~-16/-18 dB au 1er plan, lit musique ~-20 dB). Réf : `_shared/bgm/`, `bgm-ascension.mp3`.
- **SFX** : whoosh/notify/impact sur les temps forts (palette SFX v1).

---

## La structure (les 5 blocs)

| Bloc | Temps | Rôle | Règle |
|------|-------|------|-------|
| **1. Hook brutal** | 0-2s | Créer la tension immédiate | JAMAIS « Salut, aujourd'hui je vais vous montrer ». Une phrase qui provoque (voir banque ci-dessous). |
| **2. Promesse** | 2-5s | Donner une raison de rester | « En 30 secondes, je te montre exactement comment faire. » |
| **3. Pattern interrupt** | permanent | Empêcher le scroll | Change quelque chose toutes les 2-4s : zoom, cadrage, geste, texte à l'écran, b-roll/mockup, rythme, question directe. |
| **4. Micro-yapping structuré** | cœur | Délivrer sans blabla | Suivre l'ordre : **Problème → tension → révélation → preuve → solution**. |
| **5. Punchline** | fin | Rester en tête + CTA | Une phrase mémorable, puis « commente [MOT] ». |

### Banque de hooks brutaux (bloc 1)
- « Tu fais probablement cette erreur sans t'en rendre compte. »
- « Si tu utilises l'IA comme ça, tu perds ton temps. »
- « Personne ne te dit ça sur l'IA. »
- « Attends. Avant de faire ça, regarde ça. »

### Formule micro-yapping (bloc 4) — exemple Automation Boost
> « Tu veux gagner du temps avec l'IA ? Alors arrête de lui demander une seule chose à la fois. Le vrai avantage, c'est de connecter plusieurs étapes ensemble. Tu donnes une entrée, l'IA analyse, génère, puis ton automatisation publie. Résultat : tu ne travailles plus dans le système, tu construis le système. »

### Banque de punchlines (bloc 5)
- « L'IA ne remplace pas ton travail. Elle remplace les tâches qui te font perdre ton temps. »
- (générer une variante alignée sur le sujet, courte, contrastée)

---

## Le pattern interrupt en pratique (bloc 3)
Poser une **grille de battements toutes les 2-4s** et, à chaque battement, changer AU MOINS un élément :
- **Avatar** : nouveau clip de la banque v3 (angle/expression différents) → l'avatar « bouge » d'un plan à l'autre.
- **Cadrage/zoom** : punch-in léger sur les mots d'insistance.
- **Texte** : un gros mot néon plein écran qui claque (le chiffre, le mot clé).
- **B-roll/mockup** : reconstruit en HTML (interface, n8n, résultat) — jamais de génération IA payante.
- **Rythme** : accélération/coupe sèche.
Vérifier après montage : **aucun plan > 4s sans changement**.

---

## Workflow d'exécution
1. **Écrire le script** selon les 5 blocs (hook brutal → promesse → problème/tension/révélation/preuve/solution → punchline + CTA). Court, cash. Cocher aussi 2-3 des [[reference_marketing_skills_installed|9 mécanismes viraux]] (`_scripts/reference-9-mecanismes-viraux.md`).
2. **Voix** : générer la voix clonée (webhook tts-gen, voixUrl archiviste) en segments, la traiter rapide (atempo + silenceremove).
3. **Monter** via le pipeline v3 (`veille-to-video-v3` : assemblage de clips avatar par rôle) + habillage néon HyperFrames. Poser la grille de pattern interrupt (2-4s). Captions mot-à-mot. Musique duckée + SFX sur les temps forts.
4. **Vérifier** : snapshot avant rendu (avatar vivant, captions, texte néon). Env HyperFrames obligatoire (PATH/LD_LIBRARY_PATH/FONTCONFIG_PATH).
5. **Publier** sur previsualisation (route dédiée) pour validation Tony.
6. Après « ✅ » : câbler la gate commentaire → DM (mot-clé), puis **planifier sur les 5 réseaux** (TikTok 36488 / IG 54617 / YouTube 45006 / FB 43538+pageId / LinkedIn 25882).

---

## Checklist qualité (avant de programmer)
- [ ] Hook des 0-2s = provocation, PAS « salut aujourd'hui ».
- [ ] Promesse claire avant 5s.
- [ ] **Aucun plan > 4s** sans changement (pattern interrupt réel).
- [ ] Bloc 4 suit Problème → tension → révélation → preuve → solution.
- [ ] Punchline mémorable à la fin + CTA « commente [MOT] ».
- [ ] Avatar = vraie banque v3, son natif coupé, on entend UNIQUEMENT la voix clonée.
- [ ] Voix rapide/claire, musique duckée sous la voix.
- [ ] Captions mot-à-mot lisibles.
- [ ] Mot-clé vidéo == mot-clé de l'automation DM.
- [ ] Publié sur previsualisation + « ✅ Validé » avant planif 5 réseaux.

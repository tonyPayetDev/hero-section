---
name: prompt-reveal-branded
description: Prompt Reveal — vidéo courte 9:16 pour Automation Boost qui montre un rendu IA bluffant, tease le prompt qui défile à l'écran (ou via avatar), puis CACHE le prompt (flou/glitch) et gate le CTA "abonne-toi + commente [MOT] pour recevoir le prompt en DM". Le commentaire déclenche l'envoi auto du prompt en DM via Blotato (compte Automation Boost, accountId 54617). Déclencheurs : "vidéo prompt reveal", "le prompt défile", "cache le prompt", "gate abonné commentaire", "vidéo higgsfield", "version ultra instinct".
---

# prompt-reveal-branded — Prompt Reveal (Automation Boost)

**Input :** un rendu IA final (vidéo/image bluffante) + le prompt complet + les images de référence + un mot-clé CTA
**Output :** une vidéo sociale 9:16 (25–30 s) qui révèle *à moitié* un prompt, le verrouille, et gate sa livraison derrière un commentaire → DM auto Blotato.

Ce skill applique la convention de tournage à **deux plans** :

- **[PLAN A — écran Claude]** = ce qu'on FILME sur l'écran : l'overlay HTML branded (`references/overlay-template.html`) rejoué phase par phase dans le navigateur. C'est ta source vidéo « native Claude » (badge, prompt qui défile, écran verrouillé, carte CTA).
- **[PLAN B — produit final]** = le montage assemblé : rendu IA + overlay PLAN A + b-roll images de réf + rendu concurrent + voix/captions, exporté en 1080×1920.

> ⚠️ Le prompt n'est **jamais** entièrement lisible dans la vidéo. On en montre assez pour donner envie (les 2–3 premières lignes, la structure temporelle floutée), puis on le verrouille. La valeur est dans le DM.

---

## Les 4 inputs à récolter (toujours en premier)

Avant toute production, réunir ces 4 éléments. Ne rien inventer : demander à Tony ce qui manque.

| # | Input | Détail | Défaut si absent |
|---|-------|--------|------------------|
| 1 | **Rendu final** | La vidéo/image IA bluffante à montrer en hook (0–2 s) et en promesse (2–5 s). | Réf format : `https://higgsfield.ai/s/nkXuLIHR2VE` |
| 2 | **Prompt complet** | Le texte intégral à révéler *partiellement* puis à envoyer en DM. | `assets/example-prompt-ultra-instinct.txt` |
| 3 | **Images de référence** | Les visuels sources (@Image 1 / @Image 2) montrés en b-roll (14–20 s). | Voir les 2 URLs dans `assets/example-prompt-ultra-instinct.txt` |
| 4 | **Mot-clé CTA** | Le MOT à commenter (UPPERCASE, un seul mot). Sert de gate + de matching DM Blotato. | `PROMPT` |

---

## Style obligatoire (MA CHARTE)

- **Format** : 1080×1920 vertical, 30 fps.
- **Durée** : 25–30 s.
- **Fond** : `#0a0a0a` (matte black, jamais un noir plat — léger vignettage/grain).
- **Accents** : or `#FFD700` (dominant), cyan `#00D4FF` (secondaire / tech), rouge `#FF3333` (verrou / alerte / "interdit").
- **Titres** : **Bebas Neue**, UPPERCASE, **1ère lettre en or `#FFD700`**, le reste en blanc.
- **Prompt** : **JetBrains Mono** style terminal, label fixe `// PROMPT_REVEAL _` (curseur clignotant).
- **Captions** : style TikTok mot-à-mot, 27px, une ligne, 3 mots max, un mot actif surligné (or/cyan). Contour + ombre noire, glow coloré sur le mot actif. Pas de boîte de fond.
- **Interdits** : montrer le prompt en entier ; laisser l'écran verrouillé lisible ; donner l'URL du site en clair (on gate par commentaire, pas par lien).

---

## Timeline (25–30 s)

| Temps | Phase | À l'écran | Voix off (idée) |
|-------|-------|-----------|-----------------|
| **0–2 s** | Hook | Le rendu final IA en plein cadre, coupe sèche sur le moment le plus fort. Badge `PROMPT INSIDE`. | « Ce plan a été généré avec UN seul prompt. » |
| **2–5 s** | Promesse | Rendu qui continue + titre Bebas « Le Prompt » (P en or). | « Et je te donne exactement celui-là. » |
| **5–14 s** | Tease | **Variante A ou B** (voir ci-dessous). Le prompt défile en terminal, mais coupé/flouté après les 2–3 premières lignes. | « Regarde comment il est structuré, seconde par seconde… » |
| **14–20 s** | B-roll | Images de réf #1 et #2 (split ou Ken Burns) + un extrait du **rendu concurrent** en incrustation. | « Deux images de départ. Le reste, c'est le prompt qui le fait. » |
| **20–24 s** | Disparition | Le prompt se **flou/glitch** et bascule sur `🔒 PROMPT VERROUILLÉ` (rouge `#FF3333`). | « Mais je te le donne pas comme ça. » |
| **24–30 s** | CTA (gate) | Carte CTA : « ABONNE-TOI + commente **[MOT]** » → « je t'envoie le prompt en DM ». | « Abonne-toi, commente **[MOT]**, et je te l'envoie direct en message. » |

---

## Les 2 variantes du tease (5–14 s)

- **Variante A — « le prompt défile »** : PLAN A pur. Le prompt s'auto-scrolle dans le terminal (`// PROMPT_REVEAL _`), avec un masque/dégradé qui coupe la lecture après ~3 lignes. C'est la plus rapide à produire (pas de voix avatar), la plus « hacker/tech ».
- **Variante B — « avatar explique »** : un avatar (setup Automation Boost) explique *comment* prompter (les 3 blocs : identité à préserver / découpage temporel 0–2 s… / contraintes no-morphing) pendant que le terminal défile en fond. Plus pédagogique, plus incarnée. Réutiliser l'avatar-loop du pipeline vidéo existant.

Par défaut : **Variante A** si Tony ne précise pas. Proposer B quand le prompt est « éducatif » (technique de prompting réutilisable).

---

## Workflow d'exécution

### Étape 0 — Réunir les 4 inputs
Vérifier le tableau des 4 inputs. Si un manque, demander. Sinon utiliser les défauts de `assets/`.

### Étape 1 — [PLAN A] Filmer l'overlay branded
1. Ouvrir `references/overlay-template.html` dans le navigateur (playwright-skill ou capture headless — env HyperFrames ci-dessous).
2. Injecter le prompt (input 2) et le mot-clé (input 4) dans le template (placeholders `{{PROMPT}}`, `{{KEYWORD}}`).
3. Capturer les **4 phases** séparément (badge → prompt qui défile → écran verrouillé → carte CTA). Les boutons de preview du template **ne se filment pas** (ils servent juste à naviguer entre phases).
4. Vérifier que le prompt est bien **coupé/flouté** avant la fin — jamais lisible en entier.

### Étape 2 — [PLAN B] Monter le produit final
1. Séquencer selon la timeline : rendu final (input 1) → overlay PLAN A → b-roll images de réf (input 3) + rendu concurrent → glitch/verrou → carte CTA.
2. Voix off + captions TikTok mot-à-mot (charte ci-dessus). Voix clonée seulement si accord (consentement standing OK).
3. Beat-sync léger sur les transitions (drop = passage tease→b-roll, et disparition→CTA).
4. Exporter 1080×1920, 30 fps, 25–30 s.

### Étape 3 — Prévisualisation + planif
1. Publier le rendu sur `previsualisation.automatisationboost.com` (route dédiée) pour validation Tony.
2. Après « ✅ Validé », programmer via Blotato (@automationboost / accountId **54617**).

### Étape 4 — Câbler le gate commentaire → DM
Suivre `references/blotato-dm-gate.md` : créer l'automation Blotato qui matche le **mot-clé** en commentaire et envoie le **prompt complet** en DM. Garde-fou anti-doublon obligatoire.

```bash
# Env HyperFrames (rendu/capture) — sans ça le texte est invisible
export PATH="/home/claude/tools/node/bin:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/chromelibs/usr/bin:$PATH"
export LD_LIBRARY_PATH="/home/claude/tools/chromelibs/lib/x86_64-linux-gnu:/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export FONTCONFIG_PATH="/home/claude/tools/chromelibs/etc/fonts"
```

---

## Checklist qualité (avant de programmer)

- [ ] Les **4 inputs** sont réels (pas de placeholder oublié dans le montage).
- [ ] Le rendu final bluffe dans les **2 premières secondes** (coupe sur le moment fort).
- [ ] Le prompt **n'est jamais lisible en entier** — coupé/flouté au tease, verrouillé à 20–24 s.
- [ ] Charte respectée : fond `#0a0a0a`, or `#FFD700`, cyan `#00D4FF`, rouge `#FF3333`, Bebas Neue titres (1ʳᵉ lettre or), JetBrains Mono prompt, label `// PROMPT_REVEAL _`.
- [ ] Les **boutons de preview** de l'overlay n'apparaissent pas dans la vidéo.
- [ ] Écran `🔒 PROMPT VERROUILLÉ` en rouge présent avant le CTA.
- [ ] CTA gate = **abonne-toi + commente [MOT]**, jamais l'URL du site en clair.
- [ ] Le **mot-clé** de la vidéo == le mot-clé de l'automation Blotato (matching exact).
- [ ] Automation Blotato créée, garde-fou anti-doublon actif, message DM contient le prompt COMPLET + les liens.
- [ ] Durée 25–30 s, 1080×1920.
- [ ] Rendu poussé sur previsualisation + « ✅ Validé » avant planif.

---

## Références du skill

- `references/overlay-template.html` — overlay 9:16 filmable [PLAN A], 4 phases, à ta charte.
- `references/blotato-dm-gate.md` — câblage commentaire → DM auto (MCP Blotato).
- `assets/example-prompt-ultra-instinct.txt` — prompt exemple « Ultra Instinct » + liens de réf.

**Réf format / rendu concurrent :** `https://higgsfield.ai/s/nkXuLIHR2VE`

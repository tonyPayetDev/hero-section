# Banque avatar Tony — pack de prompts Seedance (24 clips)

**Méthode** : 1 génération = 1 micro-clip de 5 s. Toujours joindre la photo de référence avatar
(`refs/hf-avatar-2-portrait.png` pour les hooks/dramatique, `refs/hf-avatar-1-desk.png` pour les
explications). Seedance fait JOUER la phrase (mouvement lèvres + visage + mains) ; l'audio sera
ensuite remplacé par le clone ElevenLabs en conservant le mouvement des lèvres.

Chaque clip = **[MASTER PROMPT]** ci-dessous + le bloc PERFORMANCE du clip.

---

## MASTER PROMPT (à préfixer à chaque génération)

```text
Use the provided avatar reference as the exact same person.
Create a realistic vertical 9:16 talking-head video, 5 seconds long.

IDENTITY LOCK:
- Preserve the exact facial identity, hairstyle, skin tone, facial proportions and overall appearance of the reference avatar.
- Do not change the person's identity. No face morphing, no character redesign.

VISUAL CONSISTENCY:
- Same outfit, background, lighting, camera position and focal length as the reference.
- Medium shot, upper body visible. Camera completely static. 9:16 vertical.
- Natural realistic skin and facial motion. Professional social-media creator style.

PERFORMANCE (base):
- Start 1 second neutral: mouth closed, hands relaxed, looking directly at camera.
- Perform the specified gesture naturally while speaking the exact French sentence.
- Natural French lip movement synchronized with the words. Expressive but realistic.
- End 1 second neutral. No exaggerated acting, no camera movement, no text/subtitles/logos/UI.

Feel like a real French entrepreneur explaining something directly to the viewer.
```

---

## A — HOOKS (énergie haute, réf portrait)

**A1** — half-step toward camera, eyebrows up, "you need to see this" energy.
Say: « Attends, attends, faut que je te montre un truc que personne n'utilise. »

**A2** — point at camera with index finger, direct/slightly challenging.
Say: « Toi, là. Tu perds trois heures par semaine sur un truc qu'une machine fait en deux minutes. »

**A3** — genuine surprise, head slightly back, open both hands revealing something.
Say: « J'ai testé ce truc hier soir et honnêtement, je m'attendais pas à ça. »

**A4** — raise three fingers on "Trois outils", then lower hand.
Say: « Trois outils. Zéro ligne de code. Et tout tourne pendant que tu dors. »

**A5** — lean slightly toward camera like sharing a secret, half-smile.
Say: « Bon, je devrais peut-être pas partager ça, mais tant pis, je te le donne. »

**A6** — side-to-side "no" hand gesture, slight head shake.
Say: « Non, non, non. Arrête de faire ça manuellement, sérieux, on est en 2026. »

## B — EXPLICATIONS (énergie moyenne, réf desk)

**B1** — mostly still, tiny head nods. « En fait le principe est simple : chaque étape déclenche automatiquement la suivante, sans intervention. »
**B2** — right hand open palm accompanies. « D'abord tu connectes ton compte, ensuite tu définis le déclencheur, et enfin tu choisis l'action. »
**B3** — left hand small open-palm, moving info. « Le système récupère les données, les analyse, puis les envoie exactement où tu veux. »
**B4** — count on three fingers. « Premièrement le gain de temps, deuxièmement la régularité, troisièmement zéro oubli. »
**B5** — left hand option A, right hand option B, amused. « D'un côté tu as la méthode classique, de l'autre la version automatisée. Devine laquelle gagne. »
**B6** — two small nods, subtle smile. « Et oui, ça fonctionne aussi pour les petites structures, c'est justement ça qui est fort. »
**B7** — head tilt, eyebrows up, curious. « La question qu'on me pose tout le temps, c'est : est-ce que c'est compliqué à mettre en place ? »
**B8** — one hand draws a small circle (loop). « Et le cycle recommence : publication, analyse, ajustement, republication. En boucle, tout seul. »
**B9** — shoulders up, both palms up, "it's that simple". « Franchement ? Une fois que c'est configuré, tu n'y touches plus jamais. »
**B10** — more serious, brief index finger warning, strong eye contact. « Par contre, attention : si tes données de départ sont mauvaises, le résultat sera mauvais aussi. »
**B11** — look toward right of frame (screen off-cam) then back to camera, impressed smile. « Regarde ce qui se passe ici quand je lance le workflow. Tu vois ? Instantané. »
**B12** — touch chin thinking, then look to camera. « Alors comment on choisit le bon outil ? En vrai, ça dépend d'un seul critère. »

## C — CTA

**C1** — point down toward lower frame, smile. « Tout est dans la description juste en dessous, sers-toi, c'est cadeau. »
**C2** — mime typing on phone, then look back to camera. « Commente le mot AUTOMATION et je t'envoie le template directement en message privé. »  ⟵ mot-clé corrigé (était "automne")
**C3** — thumbs-up then press invisible button, confident smile. « Abonne-toi, j'en poste un nouveau chaque semaine, tu vas pas vouloir rater le prochain. »
**C4** — both hands together, small nod, eye contact. « Voilà, tu sais tout. Maintenant la seule chose qui manque, c'est que tu le fasses. »
**C5** — one index finger "wait", knowing smile. « Et dans la prochaine vidéo, je te montre la version encore plus poussée de ce système. »
**C6** — small natural wave, genuine smile. « Allez, c'était Tony, à très vite pour la suite. Ciao ! »

---

## Assemblage (skill veille-to-video-v3)

`Sujet → Hook (A) → Clip avatar → B-roll → Explication (B) → CTA (C) → voix ElevenLabs → captions/DA → montage → vidéo finale`

Sélection par tags `role / gesture / energy` (voir `manifest.json`). Cuts invisibles grâce à la
seconde neutre en début/fin de chaque clip. Audio des clips remplacé par ElevenLabs (lip-sync
conservé). Ce pipeline est un **nouveau skill v3** — ne modifie pas `veille-to-video` (v2).

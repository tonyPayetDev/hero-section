---
name: revelation-ab-branded
description: Produit une vidéo sociale 9:16 Automation Boost du format "révélation par comparaison A/B" — on prend une astuce IA qui circule déjà, et on montre côte à côte la version que tout le monde connaît et la version qui change tout. Vidéo fondatrice = "Les 10 questions Claude" (autoboost-61, Claude vierge vs Claude qui te connaît). Déclencheurs : "vidéo comme les 10 questions", "refais une vidéo 10 questions", "vidéo comparaison", "vidéo split", "avant/après IA", "révélation A/B", "montre la différence entre les deux".
---

# revelation-ab-branded — La révélation par comparaison

**Output :** 1 vidéo 9:16, **35-45 s**, qui prend une astuce IA déjà vue et prouve qu'on la fait mal.

**Projet de référence à copier :** `/work/autoboost-neon-videos/autoboost-61-dix-questions/`
(`work/order.json` = la timeline, `work/build_screens.mjs` = le split, `work/assemble.sh` = le montage)

---

## Le principe : le twist, pas l'astuce

L'astuce seule ne vaut rien — elle circule déjà partout sur ChatGPT et TikTok. **Ce qui appartient à Tony, c'est la comparaison :**

| | |
|---|---|
| **Côté A** | ce que tout le monde fait → résultat correct, générique, froid |
| **Côté B** | le détail qui change tout → résultat qui touche |

> Vidéo fondatrice : Claude **vierge** vs Claude **avec des mois de conversations**. Même prompt, deux mondes.

**Sans la comparaison montrée à l'écran, la vidéo est un repost de trend de plus.** C'est le seul bloc qu'il ne faut pas bâcler. Si tu n'as pas de côté B démontrable, ce n'est pas ce format — bascule sur `/script-pspc-branded`.

**Autres sujets qui entrent dans le moule :** prompt court vs prompt avec contexte · outil brut vs outil branché sur tes données · workflow à la main vs workflow automatisé · script écrit par IA seule vs IA + ta voix.

---

## Structure (timings réels de autoboost-61)

| Bloc | Temps | Contenu | Clip |
|---|---|---|---|
| **Hook** | 0-4 s | « Écoute bien. » + la phrase qui ouvre la boucle | avatar **fixe** |
| **Punch-in** | 4-7 s | le même clip, **zoom 1.14** — l'annonce des deux tests | avatar **fixe** (2ᵉ plan) |
| **Le décor** | 7-10 s | les deux versions apparaissent côte à côte | écran |
| **Le prompt** | 10-15 s | **le prompt exact, tapé en direct à l'écran** | écran |
| **Le détail** | 15-19 s | ce qui change tout, martelé | avatar **geste** |
| **SPLIT A** | 19-22 s | côté A actif, côté B désaturé | écran |
| **SPLIT B** | 22-25 s | côté B actif, **la ligne qui pique** | écran |
| **Le triplet** | 25-29 s | « Tu vas… tu vas… tu vas… » | avatar **relance** |
| **CTA** | 29-35 s | mot-clé + faux champ de commentaire | avatar **lunettes** |
| **Carton** | 35-37 s | endcard mot-clé | écran |

**Règle de rythme :** aucun plan ne dépasse ~5 s. Chaque phrase = un changement à l'écran.

---

## Les 4 rôles de clips avatar

| Rôle | Ce qu'il fait | Où |
|---|---|---|
| **fixe** | regard caméra continu | hook + punch-in (2 plans dans le même clip, zoom différent) |
| **geste** (doigts/main) | martèle le détail qui change tout | le bloc « le détail » — **le geste doit dire le propos** |
| **relance** (barbe, lunettes réajustées) | relance avant la demande | le triplet |
| **lunettes / mise en place** | ferme | CTA — ses secondes muettes servent de respiration |

⚠️ **Le geste doit tomber sur le mot.** Sur autoboost-61, les deux doigts arrivent pile sur « une par une, pas toutes à la fois ». Si le geste ne dit pas le propos, change de clip.

---

## Le split à l'écran — la recette

- **Deux panneaux HTML côte à côte**, jamais deux vidéos.
- **Le côté inactif est désaturé à 30 %** — c'est ce qui dirige l'œil sans texte explicatif.
- Côté A : 3 items **d'un coup** (générique, ça défile).
- Côté B : 3 items qui **arrivent un par un** — le rythme dit déjà que c'est plus lent, plus réfléchi.
- **La ligne qui pique tombe exactement sur la voix.** C'est le pic de la vidéo, cale-la à la frame.

### ⚠️ Données personnelles
**Ne montre jamais de vraie donnée perso à l'écran.** Les écrans sont **reconstruits en HTML**, jamais capturés.

Conséquence assumée : **le bloc validation ne prouve rien, il illustre.** C'est la faiblesse structurelle du format. Si Tony accepte une **capture réelle anonymisée** (noms floutés), c'est nettement plus fort — le twist n'existe vraiment que si on voit la différence réelle. Lui poser la question vaut le coup à chaque fois.

---

## Langue (cf. `/script-pspc-branded`)

- **Le triplet de clôture est la signature du format** : « Tu vas être choqué. Tu vas être bluffé par les questions. Tu vas découvrir comment tu es. » Trois blocs courts, montée. **Ne le lisse jamais.**
- **Max 2 adjectifs empilés, jamais 3.** Faire tourner : indéniable · irréfutable · incontestable · imparable · implacable · sans appel · formel · cash.
- Phrases très courtes, aucune subordonnée, aucune transition polie.
- Aucune promesse de revenu, aucun témoignage, aucune urgence artificielle.
- ~15 caractères parlés/seconde.

---

## CTA — le bloquant qui revient

**Un mot-clé unique en MAJUSCULES + le faux champ de commentaire incrusté** (le mot se tape lettre par lettre).

1. **Vérifier qu'il est libre** — `blotato_list_automations`. Déjà pris : STAR, CHAOS, ECOM, TRAILER, TELE, SITE, HOOK, YAPPING, CONTENU, TURBO, MACHINE, VIDEOBOOST, SEEDANCE, MIROIR.
2. **Éviter les mots trop courants** (QUESTIONS, DM, INFO, LIEN) : la gate se déclencherait sur du bruit.
3. ⚠️ **VÉRIFIER QU'UNE RESSOURCE EXISTE VRAIMENT DERRIÈRE.** Sur autoboost-61 le mot-clé était libre mais **aucune page ne correspondait** → publication bloquée. Une page au sujet voisin ne compte pas : l'envoyer est une promesse non tenue.

**Créer la ressource fait partie du travail, pas de l'après.**

---

## Pièges déjà payés

1. **Les clips Seedance font ~10,08 s, pas 8** — deux prises de ~5,04 s collées, avec **une pause muette à la couture (~4,2→5,0 s)**. Un geste demandé peut n'exister que dans la 2ᵉ prise (les deux doigts d'autoboost-61 n'apparaissent qu'à 5,3 s).
2. **Règle des lèvres** — jamais de voix active sur une portion muette. Générer la carte (`build-lips-map.mjs`), lancer **`check_lips_rule.mjs`** avant assemblage, **code 0 obligatoire**. Voir `_shared/avatar-bank/LIPS-MAP.md`.
3. **Le crop du garde-fou lèvres est calibré par cadrage** : sur un nouveau cadrage il peut tomber sur les yeux. `LIPS_CROP` / `LIPS_THRESH` sont surchargeables — remesurer, et corriger à la main les faux positifs (main sur le menton, lunettes) en documentant la correction.
4. **`FONTCONFIG_PATH` est obligatoire** ou libass ne rend rien.
5. **HyperFrames ignore `--out`** et écrit dans `./renders/` relatif au cwd.
6. **`apad` sans borne** part en boucle infinie → borner avec `-t` sur la sortie.
7. **Cloudflare met les 404 en cache** : boucler sur le **md5 servi**, jamais sur le statut Coolify (8 polls servaient encore l'ancien fichier sur autoboost-61).

---

## Fabrication

Style verrouillé `/veille-to-video-v3` : voix clonée `tts-gen` + `voixUrl` archiviste, atempo ~1.12, silences coupés, **audio natif des clips coupé** (`-an`), captions mot-à-mot, BGM duckée en sidechain, charte néon 1080×1920.

Le plus simple : **copier `autoboost-61-dix-questions/work/`** et remplacer le contenu de `order.json`, `build_screens.mjs` et les segments de voix.

---

## Checklist

- [ ] Le **côté B est réellement démontrable** (sinon ce n'est pas ce format).
- [ ] Le split est à l'écran, côté inactif désaturé, côté B **un par un**.
- [ ] La **ligne qui pique** tombe sur la voix, à la frame.
- [ ] Le **geste dit le propos**, il ne décore pas.
- [ ] Aucune donnée perso réelle à l'écran.
- [ ] Le **triplet de clôture** est intact.
- [ ] Mot-clé libre **ET ressource existante** (créée si besoin).
- [ ] `check_lips_rule.mjs` → **code 0**.
- [ ] md5 servi = md5 local avant de conclure.
- [ ] 35-45 s · max 2 adjectifs · aucune promesse.

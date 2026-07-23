# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-07-23
- **Période couverte** : juin–juillet 2026 (~30 posts IG, 12 vidéos TikTok récentes scrapées, 50 posts concurrent)
- **Comptes analysés** : TikTok `@automationboost7` (Apify) · Instagram `@automatisationboost` compte 54617 (Blotato) · LinkedIn Payet Tony (non accessible) · Concurrent Instagram `@jb.roy_` (Apify)
- **AVERTISSEMENT** : comptes en phase de démarrage, volumes minuscules (vues à 2–3 chiffres, likes 0–8, commentaires ≈0). Toutes les conclusions ci-dessous sont à **confirmer** sur plus de données ; la robustesse statistique est faible (n petit).

> **Alerte handle** : `@tonypayet4` ne remonte **aucune donnée** (0 abonné / 0 vidéo) ni via tokscript ni via Apify. Le compte TikTok réellement actif et alimenté est **`@automationboost7`** (nickname « automatisationboost »). À vérifier avec Tony avant toute analyse future basée sur `tonypayet4`.

---

## 1. Chiffres clés par plateforme

### TikTok `@automationboost7` — source Apify (source de vérité TikTok)
| Métrique | Valeur |
|---|---|
| Abonnés | 77 (2026-07-23) — 57 au scrape du 15/07, soit **+20 en ~8 jours** |
| Vidéos publiées | 41 au total (12 récentes analysées) |
| Vues | médiane ~275, **moyenne 331**, max **929**, min 236 |
| Likes | moyenne 4 (0–8) |
| Commentaires | moyenne ~1 (0–4) |
| Partages | 0–3 · Enregistrements (saves) 1–7 |
| Engagement / 100 vues | **1,87** |
| Durée des vidéos | 16–34 s (souvent 30 s, plusieurs à 16–17 s) |

Note : les enregistrements (saves : 6–7 sur les meilleures) sont le signal d'engagement le plus fort du compte, bien avant les likes/commentaires.

### Instagram `@automatisationboost` (54617) — source Blotato
| Métrique | Valeur |
|---|---|
| Vues | 6–216 · Reach 4–202 |
| Likes | 0–3 · Commentaires ≈0 |
| Décrochage | reach chute <20 après ~17/07 (saturation de posts quasi identiques + CTA « Commente le mot ») |
| Rétention | correcte quand la vidéo est vue (watchTimeAvg jusqu'à ~6 s). **Le goulot est le REACH/hook, pas la rétention.** |

Note : Apify n'a pas scrapé l'IG de Tony dans les runs disponibles (uniquement le concurrent) → les chiffres IG restent ceux de Blotato.

### LinkedIn (Payet Tony)
**Données non accessibles automatiquement.** Le connecteur LinkedIn Organic n'est pas connecté dans Windsor.ai (seuls des comptes tiers non pertinents y figurent). **À suivre manuellement.**

---

## 2. Top 3 vidéos

### Top 3 toutes plateformes confondues (par portée absolue)
1. **929 vues (TikTok)** — « 🎬 J'ai trouvé la bibliothèque de prompts qui débloque **Seedance 2.0** (le nouveau modèle vidéo IA de ByteDance) » — 17 s, 03/07 19h51. *Actualité chaude + nom de modèle précis + framing « j'ai trouvé ».*
2. **338 vues (TikTok)** — « Ta voix off, clonée une seule fois, réutilisable sur toutes tes vidéos » — 33 s, 13/07 14h. *Bénéfice-résultat concret ; 7 saves + 3 partages (meilleur engagement du compte).*
3. **300 vues (TikTok)** — « 📊 Mon dashboard Notion se met à jour tout seul chaque matin » — 30 s, 10/07. *Résultat tangible « tout seul ».*

### Top 3 Instagram (Blotato)
1. **216 vues / 202 reach** — « **L'alternative gratuite à Claude Code** » (KILO) — 13/07 19h. *Le hook « alternative gratuite à <outil connu> » = meilleure portée IG.*
2. **132 vues** — « **Anthropic offre 6 mois de Claude Max** » — 04/07. *Chiffre d'actualité chaude + marque connue.*
3. **108 vues** — « CONSCIENCE / J-Space Claude » — 18/07.

### Top TikTok (rappel, même liste que ci-dessus, canal principal)
Seedance 2.0 (929) · Voix off (338) · Dashboard Notion (300). À noter : « Six skills transforment Claude Code en équipe de 6 développeurs » (278 vues) a le 2ᵉ meilleur engagement (6 saves, 4 commentaires).

**Pires vidéos TikTok** : « 1200+ idées » 236 vues (14/07) · prospection à froid 254 (15/06) · « propositions commerciales en PDF » 289 vues mais 2 likes / 0 commentaire / 0 partage (structure workflow générique).

---

## 3. Hooks qui marchent — formulations réutilisables

Tirés des tops réels (TikTok + IG). Copiables tels quels, à adapter à l'outil du jour :

1. **« L'alternative gratuite à <outil connu> »** — ex. « L'alternative gratuite à Claude Code ». (meilleur hook IG)
2. **Nom de modèle/outil précis + actualité chaude** — ex. « J'ai trouvé la bibliothèque de prompts qui débloque **Seedance 2.0** ». (meilleure vidéo TikTok)
3. **Chiffre d'actualité + marque connue** — ex. « **Anthropic offre 6 mois** de Claude Max ». (2ᵉ IG)
4. **« J'ai trouvé le [workflow/la lib] qui… »** — curiosity gap + découverte personnelle.
5. **Bénéfice-résultat « tout seul / une seule fois »** — ex. « Mon dashboard Notion se met à jour **tout seul** chaque matin », « Ta voix off clonée **une seule fois**, réutilisable partout ».
6. **Transformation chiffrée concrète** — ex. « Six skills transforment Claude Code en **équipe de 6 développeurs** ».
7. **« Le [outil connu] que personne n'utilise pour… »** — variante curiosity + outil nommé.
8. **Actualité IA datée** — accrocher sur une sortie récente nommée (modèle, offre, prix) dans les 5 premiers mots.

Règle : **nommer un outil/modèle connu + un chiffre ou un mot d'actualité dans les 5 premiers mots**. Les tops le font tous ; les flops ouvrent sur un emoji + « Ce workflow… ».

---

## 4. Ce qu'il ne faut PLUS faire (liste noire)

- ❌ Le template générique **« 🤖 Ce workflow fait X. Commente MOT »** → 5–17 vues sur IG (DEVIS 9, GUIDE 6, CREATEUR 6, VOIX 6, META 6…).
- ❌ **Ouverture par emoji générique** systématique (🤖 / 📊 / 🛠️) suivie de « Ce workflow… ».
- ❌ Dépendre du **« Commente le mot X »** comme moteur d'engagement → rapporte **≈0 commentaire**. (Le concurrent, lui, utilise « Follow @… » + lead magnet à grande échelle de reach — voir §6.)
- ❌ **Structure quotidienne identique** répétée (mêmes plans, mêmes phrases).
- ❌ **>1 post/jour de contenu quasi identique** : le 13/07, 5 vidéos quasi jumelles en 5 h (16h→19h) → cannibalisation + saturation, et c'est juste après que le reach IG s'effondre (<20 après 17/07).
- ❌ **Vidéos ultra-courtes 16–17 s** : sous-performent hors actualité chaude (seule exception : Seedance, portée due au sujet, pas à la durée). Le concurrent tourne bien plus long (§6).

---

## 5. Meilleures heures de publication

Robustesse **faible** (n petit) — à traiter comme hypothèse.
- Tony poste en batch **14h–19h** (heure Réunion). Défaut actuel : **18h / 18h29**.
- Meilleures perfs TikTok : Seedance **19h51**, voix off **14h**. Tops IG à **19h**.
- Concurrent `jb.roy_` : tops postés **15h–20h**.
- **Recommandation** : fenêtre **17h–20h**, **un seul** post par jour dans cette fenêtre plutôt qu'une rafale.

---

## 6. Ce que fait le concurrent qui marche (`@jb.roy_`, Apify)

| Métrique concurrent | Valeur | Tony (TikTok) |
|---|---|---|
| Vues moyennes | **~9 800** | 331 |
| Commentaires moyens | 130–380 | ~1 |
| Engagement / 100 vues | **14,77** | 1,87 |
| Durée vidéo (médiane / moyenne) | **48 s / 54 s** (range 19–111 s) | 16–34 s |
| Durée des TOP performers | **27–38 s** | — |

Enseignements exploitables :
- **Durée** : le concurrent poste **beaucoup plus long** (médiane 48 s), et même ses meilleures vidéos font **27–38 s** — bien au-dessus des 16–17 s de Tony. → **Cible 30–45 s**, jamais 16–17 s.
- **Format** : Reels vidéo (`clips`), commentaires **>> likes** → contenu qui déclenche la conversation à grande échelle, pas le like passif.
- **Hook / CTA** : caption répétée simple **« Follow @jb.roy_ pour implémenter l'IA dans ton activité »** — CTA **« Follow »** (pas « Commente MOT »), lead magnet servi à grande échelle de reach.
- **Zéro hashtag** sur les tops : ce n'est pas le levier.

---

## 7. Recommandations prioritaires (semaine suivante)

1. **Clarifier le compte TikTok** : `@tonypayet4` ne remonte aucune donnée (tokscript + Apify) ; le compte actif est `@automationboost7`. Vérifier le handle avant toute prod/analyse.
2. **1 post/jour MAX, distinct** : arrêter les rafales de vidéos quasi identiques (cause directe du décrochage reach mi-juillet).
3. **Durée 30–45 s** : aligner sur le concurrent ; supprimer le format 16–17 s et la structure « workflow générique ».
4. **Hooks d'actualité nommée** : outil/modèle connu + chiffre/mot d'actu dans les 5 premiers mots (« l'alternative gratuite à X », « Anthropic offre… », nom de modèle). Bannir « 🤖 Ce workflow… ».
5. **Remplacer « Commente MOT » par « Follow pour… » + lien bio** (linktr.ee) : le CTA de commentaire rapporte ≈0 ; le modèle du concurrent est Follow + ressource.

---

## 8. Sources & limites

- TikTok : Apify (actor via credential du workflow `YUJjz5NNsYo41t8q`), exécution du 15/07 (workflow `S9KVQP46D8Je77By`). **tokscript indisponible** (listing vidéos = abonnement Pro requis) → Apify utilisé comme source de vérité TikTok.
- Concurrent : Apify, workflow `YUJjz5NNsYo41t8q`, exécution 66112 (21/07, 50 posts).
- IG de Tony : Blotato (chiffres fournis) — non re-scrapé par Apify dans les runs disponibles.
- LinkedIn : non accessible (Windsor LinkedIn Organic non connecté).
- Workflow analytics hebdo `Analyse Réseaux Sociaux Auto` (`n5dIUNEk5D6Pj3Vf`) : **jamais exécuté** (0 run) → aucun chiffre pré-calculé à réutiliser ; inactif, à activer si l'on veut ce rapport chaque lundi 8h.

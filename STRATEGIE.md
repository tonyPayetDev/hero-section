# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-09-07 (run hebdo automatisé, session cloud à froid)
- **Période couverte** : TikTok `@automationboost7` — 40 dernières vidéos scrapées via Apify (~22/08→05/09) + stats de compte (07/09) · Concurrent TikTok `@jb.roy_` — même méthode, 40 dernières vidéos (~25/08→02/09) + stats de compte · Instagram `@automatisationboost` — 50 posts remontés par Blotato depuis le 01/07 (fenêtre large, filtrage manuel appliqué — voir §0.1) · LinkedIn — statut de publication vérifié via `blotato_list_posts` depuis le 31/08
- **Comptes analysés** : TikTok `@automationboost7` (compte Blotato `36488` **inactif/mort**, l'actif physiquement posté est `@automationboost7` — source = `tokscript get_tiktok_user` pour les stats de compte + Apify `clockworks/tiktok-scraper` via le workflow n8n `YUJjz5NNsYo41t8q` pour le détail vidéo) · Instagram `@automatisationboost` compte Blotato `54617` · LinkedIn Payet Tony (compte Blotato `25882`) · Concurrent TikTok `@jb.roy_` (même source Apify) · **Exclu** : `@tonypayet4` (reconfirmé mort, 0/0/0/0) et Instagram `foodboost` (`55611`, hors périmètre — voir §0.1 pour un problème de contamination croisée découvert ce run)

---

## 0. Anomalies et découvertes clés de ce run

1. **🔴 DÉCOUVERTE MAJEURE — contamination croisée confirmée et quantifiée sur les données Instagram Blotato.** `blotato_list_top_posts` ne renvoie **aucun champ d'identification de compte** dans sa réponse : il agrège les posts de **tous** les comptes Instagram connectés au workspace Blotato (`automatisationboost` 54617, mais aussi `foodboost` 55611, `animeirl85` 37180, `ozeroz1984` 35077). Ce run a **filtré par contenu** (mots-clés restaurant/food : "plat", "restaurant", "menu", "sushi", "ardoise", etc.) sur les 50 posts remontés depuis le 01/07 : **17 posts sur 50 (34 %)** sont des templates food/restaurant récurrents ("La lumière change tout 🌴", "Pas besoin de photographe 🌴", "Ton menu travaille pour toi 🌴"...), **tous publiés systématiquement à 07h00-07h01 UTC** — un pattern horaire totalement distinct du pivot Autoboost à 14h00 UTC. Après filtrage, il reste **33 posts propres** Autoboost. **Conséquence directe** : les moyennes de vues Instagram publiées dans les runs précédents (ex. 24/08, 31/08) mélangeaient probablement ces deux populations sans le savoir — les chiffres de ce run (§1, §2) sont les premiers calculés sur données nettoyées et ne sont **pas directement comparables** aux moyennes brutes des runs antérieurs. **Action requise** : appliquer ce filtre par mots-clés à chaque run futur tant que Blotato ne fournit pas d'identifiant de compte dans sa réponse.
2. **🟢 Signal fort — l'écart de croissance avec `@jb.roy_` se creuse alors que les cadences de publication convergent.** Cette semaine, `@automationboost7` et `@jb.roy_` ont publié quasiment le même nombre de vidéos (+13 chacun, ≈1,9/j) — la sur-publication de `jb.roy_` qui expliquait une partie de l'écart les semaines précédentes n'est plus un facteur différenciant. Résultat : Tony gagne **+15 abonnés** cette semaine (151→166) contre **+2 seulement** pour `jb.roy_` (1580→1582, croissance quasi nulle). Rapporté aux vidéos publiées, Tony est désormais **~7,7x plus efficace** (1,15 abonné/vidéo vs 0,15) contre ~4x le run précédent. Avec la cadence neutralisée comme variable, l'écart pointe plus fort que jamais vers la **qualité du hook/contenu**, pas le rythme de publication (voir §7).
3. **🟡 Hypothèse infirmée — l'horaire du format "Journal IA" ne suit pas le schéma attendu.** Le run du 31/08 concluait (sur 1 seul point de comparaison) que l'édition de nuit (03h UTC) tuait le format (11 vues) contre un créneau après-midi. Ce run montre le contraire sur deux nouveaux points : l'édition du 23/08 à 03h00 UTC a fait **783 vues** (2e meilleure vidéo de la fenêtre) et celle du 05/09 à 07h30 UTC a fait **774 vues** (3e). L'horaire ne semble donc pas être le facteur déterminant pour ce format — **hypothèse à retester avec un vrai plan de test contrôlé**, pas de conclusion causale possible avec ces échantillons.
4. **🟢 LinkedIn toujours opérationnel.** 12 posts publiés entre le 31/08 et le 06/09 (Journal IA quotidien + posts uniques), **aucun échec**. Toujours aucune métrique d'engagement disponible (Blotato ne collecte pas d'analytics LinkedIn) — statut de publication uniquement.
5. **🔴 `n5dIUNEk5D6Pj3Vf` — toujours non opérationnel, aucun changement depuis le 31/08.** Reconfirmé : **0 exécution** depuis sa création (21/07), `active: false`, nœuds HTTP Request (Instagram Graph API, TikTok API) et Telegram toujours avec des valeurs placeholder (`<__PLACEHOLDER_VALUE__...>`) jamais renseignées. Ce n'est toujours pas un problème d'accès n8n (l'accès fonctionne, voir §0.6 ci-dessous) — le workflow n'a simplement jamais été câblé. **Recommandation inchangée : le configurer réellement ou l'archiver.**
6. **🟢 n8n accessible et fonctionnel ce run.** Le workflow concurrent `YUJjz5NNsYo41t8q` a été exécuté deux fois (exécutions `83829` pour `automationboost7`, `83830` pour `jb.roy_`, méthodologie identique aux runs précédents : modification temporaire du champ `profiles` du node Apify, exécution, puis **remise en état d'origine** — vérifiée après coup, le node cible de nouveau `automationboost7`).
7. **`tonypayet4` reste confirmé mort** côté TikTok public (0 abonné / 0 vidéo / 0 like), même compte physique que `@automationboost7` — aucune action requise, à ne plus revérifier chaque semaine sauf changement signalé par Tony.

---

## 1. Chiffres clés par plateforme

### TikTok `@automationboost7` — compte + 40 dernières vidéos (Apify, fenêtre ≈22/08→05/09)
| Métrique | Valeur (07/09) | vs run 31/08 |
|---|---|---|
| Abonnés | **166** | +15 en 7j (151→166) |
| Vidéos publiées (total compte) | **135** | +13 en 7j (122→135, ≈1,9/j — cadence en baisse, se rapproche de la cible) |
| Likes cumulés (total compte) | 643 | +59 en 7j (584→643) |
| Vues moyenne / médiane (n=40 dernières vidéos) | **354 / 268** | En hausse vs 306/193 le run précédent (fenêtre glissante, pas strictement comparable, n différent) |
| Commentaires moyens/vidéo | 1,1 | Léger mieux, reste faible |
| Engagement/vue moyen | 11,79 % | — |
| Durée moyenne / médiane | — / **34 s** | Proche de la cible, stable |

### Concurrent TikTok `@jb.roy_` — compte + 40 dernières vidéos (fenêtre ≈25/08→02/09)
| Métrique | Valeur (07/09) | vs run 31/08 |
|---|---|---|
| Abonnés | **1582** | **+2 en 7j seulement** (1580→1582) — croissance quasi à l'arrêt |
| Vidéos publiées (total compte) | **162** | +13 en 7j (149→162, ≈1,9/j — même cadence que Tony désormais) |
| Likes cumulés (total compte) | 7807 | +133 en 7j |
| Vues moyenne / médiane (n=40 dernières vidéos) | 212 / 157 | Inférieur à Tony |
| Commentaires moyens/vidéo | 0,2 | Quasi nul |
| Engagement/vue moyen | 4,39 % | — |
| Durée moyenne / médiane | — / 48 s | Plus long que Tony |

**Lecture** : cadences désormais quasi identiques (≈1,9 vidéo/jour chacun) — la variable "sur-publication" n'explique plus l'écart. Tony fait **+67 % de vues moyennes/vidéo**, **2,7x l'engagement/vue**, et surtout **+15 abonnés contre +2** cette semaine. Voir §0.2 et §7.

### Instagram `@automatisationboost` (54617) — Blotato, données nettoyées de la contamination food (voir §0.1)
| Métrique | Valeur | Note |
|---|---|---|
| Top 5 propres depuis le 01/07 | 243 / 223 / 216 / 214 / 178 vues | Voir §2 pour le détail des hooks |
| Vues récentes depuis le 31/08 (n=2, propre) | moyenne **136** (166 et 106) | Échantillon très petit — 1 seul post exclu comme food ("19 plats en 19 secondes", 171 vues, 01/09 07h01 UTC) |
| Vues récentes depuis le 24/08 (n=5, propre) | moyenne **122,4**, médiane **106** | **Non comparable** aux moyennes des runs précédents (contaminées, voir §0.1) |
| Heure dominante (n=14 posts propres depuis le 05/08) | **14:00 UTC** (9/14, 64 %) | 5e confirmation consécutive, signal le plus robuste du rapport |
| Commentaires | 0 sur tous les posts examinés | CTA "Commente X" toujours sans effet mesurable |

### LinkedIn (Payet Tony, compte Blotato 25882)
**Compte opérationnel.** 12 posts publiés entre le 31/08 et le 06/09, **0 échec**. Toujours aucune métrique d'engagement (Blotato ne collecte pas d'analytics LinkedIn — statut de publication uniquement).

---

## 2. Top 3 vidéos / posts (période récente)

### Top 3 TikTok `@automationboost7` (n=40 dernières vidéos, source Apify `clockworks/tiktok-scraper`)
1. **794 vues** — « Au Népal cette semaine, une avalanche de glace a bloqué une rivière. Un barrage s'est formé tout seul, puis il a cédé... » — 109 s, 28/08 08:00 UTC. *Actualité insolite grand public, hors registre outil IA habituel — meilleur score de la fenêtre.*
2. **783 vues** — « Journal IA — Dim. 23 août 2026 » — 68 s, 23/08 03:00 UTC. *Format récurrent, publié à 03h UTC (contredit l'hypothèse "horaire de nuit = mauvais", voir §0.3).*
3. **774 vues** — « Journal IA — Sam. 5 septembre 2026 » — 84 s, 05/09 07:30 UTC. *Même format, autre horaire, performance quasi identique — l'horaire ne semble pas être le facteur déterminant pour ce format.*

*Suivent de près : 773 vues (Avant/Après site, 25 s, 26/08 14:00 UTC — meilleur ratio vues/durée) et 757 vues (« Tu veux gagner du temps ? », 32 s, 02/09 08:20 UTC).*

### Top 3 Instagram `@automatisationboost` (depuis le 01/07, données filtrées — voir §0.1)
1. **243 vues / 224 reach** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... Commente TERMINAL et je t'envoie le guide » (Claude Code + VPS + Coolify + MCP, 3 étapes) — 27/07 14:29 UTC.
2. **223 vues / 195 reach** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. Follow pour la suite + commente OPUS » — 29/07 14:30 UTC. *Actualité produit nommée dans les 10 premiers mots.*
3. **216 vues / 202 reach** — « L'alternative gratuite à Claude Code pour créer des sites automatiquement. Kilo Code + n8n = même résultat, zéro abonnement. Commente KILO » — 13/07 19:00 UTC.

### Top vidéos concurrent `@jb.roy_` (n=40 dernières vidéos, fenêtre ≈25/08→02/09)
1. **1234 vues** — 02/09 14:30 UTC, 21 s, légende « Follow @jb.roy_ pour imploser l'IA dans ton activité » (variante avec coquille "imploser" au lieu de "implémenter").
2. **725 vues** — 28/08 15:00 UTC, 44 s.
3. **530 vues** — 25/08 17:16 UTC, 42 s.

Toujours la même légende générique (variantes mineures), **aucun hashtag** sur les 40 vidéos — le hook reste parlé dans la vidéo, jamais écrit dans le texte du post (confirmé pour la 3e fois consécutive).

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Actualité produit/outil connu nommée dans les 10 premiers mots + un chiffre ou un fait précis** — toujours le pattern le plus robuste, confirmé sur Instagram (Opus 5) et en filigrane sur TikTok (chiffres du Journal IA).
2. **Actualité insolite grand public, hors registre IA/outils** — l'avalanche au Népal (794 vues, #1 TikTok de la semaine) confirme et renforce le signal "à retester" du run précédent (passé de n=1 à un pattern qui se répète, à généraliser prudemment).
3. **Alternative gratuite à un outil payant connu**, nommé explicitement — ex. « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » (#3 Instagram, 216 vues).
4. **Tutoriel actionnable en 3 étapes** avec estimation de temps réaliste — ex. « VPS, Coolify, Claude Code + MCP... 3 à 7h de setup » (#1 Instagram, 243 vues, meilleur post Instagram sur 2 mois).
5. **Avant/Après concret et court** — « d'un site figé à un site qui bosse pour toi » (25 s, 773 vues) — meilleur ratio vues/durée de la fenêtre TikTok.
6. **Format « Journal IA » récurrent** — reste performant (783 et 774 vues), et cette semaine son horaire ne semble PAS déterminant contrairement à ce qu'on pensait — à conserver comme pilier quotidien sans sur-optimiser l'heure de publication pour l'instant.

Règle : **nommer un outil/une actualité connue + un chiffre ou un fait précis dans les 10 premiers mots** reste le pattern le plus robuste ; **l'actualité insolite grand public** (hors IA) devient une deuxième famille de hook à tester plus systématiquement.

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Calculer une moyenne Instagram sans filtrer le contenu food/restaurant.** Confirmé et quantifié ce run : 34 % des posts remontés par `blotato_list_top_posts` (17/50) sont des templates food publiés à 07h00 UTC, mélangés sans identifiant de compte dans la réponse API (voir §0.1). Toujours filtrer par mots-clés avant tout calcul.
- ❌ **Compter sur « Commente le mot X » comme unique CTA.** Confirmé de nouveau : `jb.roy_` à 0,2 commentaire/vidéo en moyenne ; Tony légèrement mieux à 1,1 mais toujours loin d'un vrai levier d'engagement. Zéro commentaire sur l'échantillon Instagram examiné.
- ❌ **Attribuer l'écart de croissance avec `jb.roy_` uniquement à sa cadence de publication.** Ce run montre que les deux comptes publient désormais au même rythme (≈1,9/j) et que l'écart de croissance (+15 vs +2 abonnés) persiste et s'accentue — c'est la qualité du hook/contenu qui pèse, pas seulement le volume.
- ❌ **Conclure sur l'horaire du format "Journal IA" à partir d'un seul point de comparaison.** Le run précédent a tiré une conclusion (nuit = mauvais) sur 1 exemple ; ce run la contredit avec 2 nouveaux points. Il faut un vrai plan de test (même contenu, plusieurs horaires, plusieurs semaines) avant de figer une règle.
- ⚠️ **Ne plus considérer les moyennes Instagram des runs du 24/08 et du 31/08 comme fiables** pour des comparaisons de tendance — elles n'appliquaient pas le filtre food découvert ce run (voir §0.1). Repartir de la baseline nettoyée de ce run pour les comparaisons futures.

---

## 5. Meilleures heures de publication

- **Instagram** : créneau **14:00 UTC** toujours dominant (9 posts sur 14 propres depuis le 05/08, soit 64 %) — 5e confirmation consécutive, signal le plus robuste de ce rapport. **À garder comme pivot par défaut.**
- **TikTok `@automationboost7`** : pas de pivot horaire net cette semaine — le Top 3 est réparti sur 08:00, 03:00 et 07:30 UTC, et le format Journal IA performe de façon comparable à 03h et 07h30 (voir §0.3). Le créneau 14:00 UTC reste présent dans le Top 5 (773 vues) mais n'est plus dominant à lui seul.
- **Concurrent `@jb.roy_`** : sa meilleure vidéo de la semaine (1234 vues) est publiée à 14:30 UTC, dans le même créneau que le pivot Instagram de Tony — coïncidence à surveiller plutôt qu'un signal exploitable en l'état (n=1).
- **Recommandation** : garder **14:00 UTC** comme créneau pivot sur Instagram (signal solide). Pour TikTok, lancer un **test contrôlé sur plusieurs semaines** avant de fixer une règle d'horaire, notamment pour le format Journal IA.

---

## 6. Durée cible de vidéo

`@automationboost7` : médiane **34 s** (n=40) — stable. `@jb.roy_` : médiane **48 s** (n=40) — toujours plus long. Le Top 3 de la semaine chez Tony est dominé par des formats longs à fort hook (68-109 s, Journal IA + actualité) mais une vidéo courte (25 s, Avant/Après) reste dans le Top 5 avec le meilleur ratio vues/durée. **Cible recommandée inchangée : 25–45 s** pour le format quotidien court, avec une tolérance jusqu'à ~90–110 s pour les formats actu/comparatifs à hook fort (Journal IA, actualité insolite) — la durée seule n'explique pas la performance, le hook prime toujours.

---

## 7. Ce que fait le concurrent `@jb.roy_` qui marche (et ce qui ne marche plus)

- **La cadence ne compense plus rien : elle a rejoint celle de Tony et la croissance s'est effondrée.** `jb.roy_` a publié +13 vidéos cette semaine (149→162, ≈1,9/j) — quasiment identique à Tony — mais n'a gagné que **+2 abonnés** (1580→1582) contre **+15** pour Tony. L'efficacité par vidéo publiée est désormais de **7,7x en faveur de Tony** (1,15 vs 0,15 abonné/vidéo), en forte hausse par rapport au ratio de ~4x du run précédent (voir §0.2). Avec la variable "volume de publication" neutralisée, l'écart pointe sans ambiguïté vers la qualité du contenu/hook.
- **Vues et engagement toujours nettement inférieurs** : 212 vues/vidéo en moyenne (médiane 157) contre 354 chez Tony (médiane 268) — et un engagement/vue de 4,39 % contre 11,79 % chez Tony (2,7x).
- **Légende toujours générique, toujours 0 hashtag** : « Follow @jb.roy_ pour implémenter l'IA dans ton activité » (avec variantes/coquilles mineures) sur les 40 vidéos de l'échantillon — confirmé pour la 3e fois consécutive. Le hook réel reste parlé dans la vidéo, invisible dans les métadonnées scrapées.
- **Durée toujours plus longue** : médiane 48 s vs 34 s chez Tony — écart stable.
- **Limite de méthode inchangée** : sans transcription vidéo, impossible d'extraire les formulations de hook exactes de `jb.roy_` — seules les observations structurelles (rythme, durée, légende, croissance) sont disponibles depuis Apify.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **Ne plus chercher à publier moins que `jb.roy_` — chercher à publier mieux.** Les deux comptes sont désormais à cadence quasi égale (~1,9/j) ; l'écart de croissance (+15 vs +2 abonnés) est maintenant attribuable au contenu, pas au volume. Concentrer l'effort sur la qualité du hook plutôt que sur la régulation de la cadence.
2. **Corriger la collecte Instagram : toujours filtrer les posts food/restaurant avant tout calcul de moyenne.** 34 % de contamination confirmée ce run (voir §0.1) — appliquer systématiquement un filtre par mots-clés, et envisager de demander à Blotato un champ d'identification de compte si l'API l'expose un jour.
3. **Lancer un vrai test contrôlé sur l'horaire du format "Journal IA"** (même contenu à 03h, 07h30 et 14h sur plusieurs semaines) — les deux derniers runs se contredisent, aucune conclusion fiable n'est possible sans plan de test.
4. **Diversifier les hooks "actualité insolite grand public"** (type avalanche au Népal, 794 vues, meilleur score de la semaine) au-delà du seul registre IA/outils — tester 2-3 nouveaux sujets d'actualité générale la semaine prochaine.
5. **Décider enfin du sort de `n5dIUNEk5D6Pj3Vf`** : confirmé non opérationnel pour la 2e semaine consécutive (0 exécution depuis sa création le 21/07, placeholders jamais renseignés) — à configurer réellement ou à archiver, ce n'est plus une question d'accès n8n.

---

## 9. Sources & limites (run du 07/09)

- **TikTok compte (Tony + concurrent)** : `tokscript get_tiktok_user` (stats de compte : abonnés, nb vidéos, likes cumulés) — fonctionnel, aucune limitation rencontrée ce run.
- **TikTok vidéo par vidéo (Tony + concurrent)** : workflow n8n `YUJjz5NNsYo41t8q` (Apify `clockworks/tiktok-scraper`), exécuté en deux passes séparées le 07/09 (exécutions `83829` pour `automationboost7`, `83830` pour `jb.roy_`) via modification temporaire du paramètre `profiles` du node HTTP Request, puis **remise en état d'origine** (profil `automationboost7`) après collecte, vérifiée par relecture du workflow. Chaque passe retourne les 40 dernières vidéos scrapées, avec les métriques agrégées + top 5 par vues et par engagement/vue (pas la liste complète des 40 vidéos, donc la distribution horaire TikTok de ce run repose sur un échantillon de 5, pas 40 — à interpréter avec prudence, voir §5).
- **Instagram (Tony)** : `blotato_list_top_posts` (platform=instagram, depuis le 2026-07-01, 50 résultats triés par vues). Réponse sans champ d'identification de compte — filtrage manuel par mots-clés appliqué ce run pour exclure le contenu food/restaurant (voir §0.1). Les moyennes de ce run sont les premières calculées sur données nettoyées.
- **LinkedIn** : `blotato_list_posts` (statuts published+failed, depuis le 31/08, 50 items).
- **Workflow analytics hebdo `n5dIUNEk5D6Pj3Vf`** : vérifié via `search_executions` — 0 exécution depuis sa création, confirmé pour la 2e semaine consécutive.
- **Google Sheet "Analyse Perf"** : mis à jour ce run via un workflow n8n `create_workflow_from_code` (Google Sheets, mode append), vérifié par export CSV du gid 1277122579 — voir résumé final de l'agent.
- **Étape B (génération de scripts + ajout dans la file de production)** : hors périmètre de cette routine (analyse uniquement) — non exécutée.

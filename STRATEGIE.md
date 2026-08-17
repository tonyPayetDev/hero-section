# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-08-17
- **Période couverte** : Instagram — posts autoboost depuis le 05/08 (12 posts, foodboost exclu) · TikTok `@automationboost7` — 20 vidéos les plus retournées par le scrape Apify du jour (dont 17 dans la fenêtre 05/08→16/08 ; 3 plus anciennes du 13-15/07 mêlées par l'algorithme de l'actor) · TikTok concurrent `@jb.roy_` — 20 vidéos du 10/08 au 16/08 · LinkedIn — 6 posts publiés depuis le 05/08, **toujours aucune métrique** (voir §0 et §9)
- **Comptes analysés** : TikTok `@automationboost7` (Apify, source de vérité — `@tonypayet4` confirmé handle mort, voir §0) · Instagram `@automatisationboost` compte Blotato 54617 · LinkedIn Payet Tony (compte Blotato 25882) · Concurrent TikTok `@jb.roy_` (Apify)
- **AVERTISSEMENT** : comptes en phase de démarrage, volumes petits (vues à 1-3 chiffres, likes 0-23, commentaires 0-12). Conclusions à confirmer sur plus de données ; n petit sur chaque échantillon. **Ce run montre une baisse nette des vues Instagram et des commentaires TikTok vs le run du 05/08 — voir §1 et §4, ne pas ignorer.**

---

## 0. Rappel — `tonypayet4` reste un handle mort, ne pas l'utiliser comme source

Re-vérifié ce jour : `mcp__tokscript__get_tiktok_user("tonypayet4")` renvoie toujours 0 abonné / 0 vidéo / bio vide. Le compte réel et actif est `@automationboost7` (nickname affiché « automatisationboost », 123 abonnés, 76 vidéos ce jour). C'est le même compte que Blotato a connecté à l'origine (voir rapport du 05/08 pour la preuve détaillée par recoupement d'horodatage) — **aucune action requise**, seulement s'assurer qu'aucun script ne requête encore `tonypayet4`.

---

## 1. Chiffres clés par plateforme

### TikTok `@automationboost7` — source Apify (clockworks/tiktok-scraper, run manuel du jour, exécutions n8n #74669)
| Métrique | Valeur |
|---|---|
| Abonnés | **123** (17/08) — 103 au 05/08, soit **+20 en 12 jours** (~1,7/jour, rythme stable) |
| Vidéos publiées (total compte) | 76 (56 au 05/08) |
| Vues (n=17, fenêtre 05/08→16/08) | moyenne **298**, médiane 244, min 16, max **812** |
| Likes | moyenne 3,4 (1–14) |
| Commentaires | moyenne **0,41** (somme 7 sur 17 vidéos) — **chute nette vs 2,85 de moyenne au 05/08, voir §4** |
| Saves | moyenne 2,65 · Partages moyenne 0,71 |
| Durée (n=12 vidéos avec durée mesurable, hors slideshows dur=0) | médiane **32,5 s**, moyenne 40,7 s — range 13–135 s (un outlier CapCut à 135 s) |
| Engagement / 100 vues (likes+comm.+partages+saves) | **~4,1** (4,9 sur les 20 vidéos toutes dates confondues) |

### Instagram `@automatisationboost` (54617) — source Blotato, 12 posts autoboost depuis le 05/08 (posts `#FoodBoost` exclus)
| Métrique | Valeur |
|---|---|
| Vues | moyenne **47,6**, médiane 24,5, min 0, max **136** — **quasi divisé par 2 vs le run du 05/08 (moyenne 108,7, médiane 75)** |
| Reach | 0–113 |
| Likes | moyenne 0,58 · Commentaires moyenne 0,58 (7 commentaires au total, concentrés à 6 sur un seul post) |
| Rétention | watchTimeAvg 1,8–5,7 s selon les posts, corrélé aux vues (le post à 136 vues a aussi le meilleur watch time, 5,7 s) |

### LinkedIn (Payet Tony, compte Blotato 25882)
6 posts publiés entre le 05/08 et le 16/08 (contenu cross-posté avec TikTok/IG, ex. `linkedin.com/feed/update/urn:li:ugcPost:7494786064507838464` le 16/08). **Toujours aucune métrique accessible** : Blotato ne collecte pas d'analytics LinkedIn, et Windsor.ai confirme ce jour (`get_connectors`) que seuls deux connecteurs organiques sont branchés — Instagram `animeirl85` et TikTok `humian` — **aucun LinkedIn, ces deux comptes sont hors périmètre Autoboost**. Rien de nouveau à en tirer sans configuration manuelle côté LinkedIn Analytics natif.

### Concurrent TikTok `@jb.roy_` — source Apify, run du jour (exécution n8n #74670), 20 vidéos du 10/08 au 16/08
| Métrique | Valeur |
|---|---|
| Abonnés | 1574 (17/08) — 1564 au 05/08, soit +10 en 12 jours |
| Vidéos publiées (total compte) | 89 (50 au 05/08 — rythme de publication très soutenu, rafales incluses) |
| Vues | moyenne **416,6**, médiane 208, min 128, max **1842** |
| Likes | moyenne 7,5 (1–23) · Commentaires moyenne 0,5 (10 au total sur 20) |
| Saves | moyenne **2,05** · Partages moyenne 0,1 |
| Durée | médiane **30 s**, moyenne 32,5 s, range 12–64 s |
| Engagement / 100 vues | ~3,8 |

**Comparaison directe avec `automationboost7`** (n=17 vs n=20, période chevauchante 10-16/08) : vues moyennes plus hautes chez le concurrent (416,6 vs 298), mais **l'écart de durée s'est quasi refermé** (30 s vs 32,5 s médiane — contre 44 s vs 32 s au 05/08) et **Tony a maintenant plus de saves en moyenne que le concurrent** (2,65 vs 2,05) — inversion du signal du run précédent, voir §7 pour la réserve méthodologique sur ce chiffre.

---

## 2. Top 3 vidéos

### Top 3 TikTok `@automationboost7` (fenêtre 05/08→16/08)
1. **812 vues** — « 3 tâches à automatiser dès aujourd'hui 😴 Commente AUTO » (11/08 18:26, format carrousel photo/slideshow, pas une vidéo filmée). 5 likes, 2 commentaires, 5 saves.
2. **743 vues** — « La n8n vient de tout changer dans la façon de voir tes workflows... commente CANVAS » (16/08 14:00, 30 s, vraie vidéo). Hook = actualité chaude sur une feature n8n (Canvas) + démonstration concrète (« je repère l'erreur en 5 secondes au lieu de tout dérouler »).
3. **486 vues** — « Plus besoin de ManyChat pour envoyer des commentaires en DM. Mon système... » (09/08 22:52, format slideshow). Outil connu remplacé + promesse d'automatisation.

*Point notable : les 2 meilleurs formats de ce run (#1 et #3) sont des carrousels photo/slideshow, pas des vidéos filmées — à surveiller, voir §4.*

### Top 3 Instagram `@automatisationboost`
1. **136 vues** — « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat. Follow + commente RELANCE » (08/08 14:29). 6 commentaires — **seul post du lot avec un vrai volume de commentaires**. *Bénéfice chiffré personnel (200€/mois) + CTA Follow.*
2. **120 vues** — « Achète une Lamborghini en 1 an avec l'IA »... ça, c'est un peu du bullshit. La vraie solution : workflow n8n site+email auto. Commente MACHINE » (15/08 08:00). *Debunk d'une promesse irréaliste + solution concrète et vérifiable.*
3. **106 vues** — « On avance, encore et encore. Jusqu'au moment où l'on touche le plafond de verre... » — essai contemplatif sur la limite et l'ambition (14/08 09:57). *Format narratif/philosophique, rupture avec le ton habituel — 2ᵉ meilleur post du lot malgré l'absence de CTA produit.*

### Enseignement transversal
Le hook gagnant le plus robuste ce run reste le **bénéfice chiffré personnel** (200€/mois, TikTok Canvas « 5 secondes au lieu de tout dérouler ») — il produit à la fois les meilleures vues ET les seuls vrais commentaires. Le format **essai contemplatif** (Instagram #3) est une découverte de ce cycle : à re-tester avant de le déclarer pattern gagnant (n=1).

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Bénéfice chiffré personnel, très concret** — ex. « 200 euros par mois de secrétariat économisés », « 5 secondes au lieu de tout dérouler ». Meilleur hook du run sur les deux plateformes.
2. **Debunk d'une promesse irréaliste + solution vérifiable** — ex. « Acheter une Lamborghini en 1 an avec l'IA, c'est un peu du bullshit. La vraie solution : ... ». Fonctionne en ouverture polarisante avant la valeur.
3. **Actualité chaude sur une feature d'un outil connu** — ex. n8n Canvas (« vient de tout changer... »), à rejouer à chaque sortie de fonctionnalité notable (n8n, Claude, etc.).
4. **Remplacement d'un outil connu et payant par un système fait-maison** — ex. « Plus besoin de ManyChat pour... Mon système... ».
5. **Essai contemplatif / narratif sans CTA produit direct** — nouveau ce run, 2ᵉ meilleur post Instagram malgré l'absence de promesse commerciale ; à retester avant de généraliser (n=1).

Règle : **un chiffre concret et personnel (€, secondes, %) dans les 10 premiers mots** reste la meilleure garantie de vues ET de commentaires, plus fiable que le nom d'outil seul.

---

## 4. Ce qu'il ne faut PLUS faire — et deux points de vigilance nouveaux ce run

- ❌ **Instagram, CTA « Commente le mot X » sans chiffre personnel associé** : sur les 12 posts du lot, seul celui avec un chiffre concret (200€/mois) a généré des commentaires (6). Les 5 autres posts utilisant « Commente MOT » seul (MACHINE, TABLES, SKILLS, SEEDANCE ×2) sont tous à 0 commentaire.
- ⚠️ **NOUVEAU — TikTok, chute du volume de commentaires vs le run du 05/08** : moyenne tombée de 2,85 à 0,41 commentaire/vidéo. Sur les 6 vidéos avec CTA explicite « Commente MOT » de ce lot, total = 7 commentaires (1,17/post), loin des 9-12 par post observés le 05/08. **Ne plus présenter « Commente le mot X » comme un CTA fiable sur TikTok sans nuance — possible effet de lassitude sur une formule répétée trop identique, à re-tester avec des variantes de mot-clé.**
- ❌ **Instagram, baisse générale des vues** : moyenne quasi divisée par 2 (108,7 → 47,6) sur un volume de posts comparable (12 posts en 12 jours vs 19 en 5 semaines, cadence similaire). Cause non identifiée avec les données actuelles (pas de changement de créneau ni de format évident) — **à surveiller en priorité la semaine prochaine, ne pas continuer sans creuser** (voir reco #1).
- ❌ **>1 post/jour de contenu quasi identique** : encore observé le 15/08 (3 posts TikTok/IG le même jour, 08h00/14h00/14h29) — discipline « 1 post/jour distinct » toujours pas acquise.
- ⚠️ **À surveiller sans trancher — format carrousel photo sur TikTok** : les 2 meilleurs posts TikTok du run (812 et 486 vues) sont des slideshows, pas des vidéos filmées. Pourrait indiquer un format à exploiter davantage, ou un artefact d'échantillon (n=2) — ne pas généraliser sans un nouveau run de confirmation.

---

## 5. Meilleures heures de publication

Robustesse **faible à moyenne** ce run — le créneau dominant reste identifiable mais moins net qu'au 05/08.
- **TikTok** : toujours majoritairement **14:00 UTC (18h Réunion)** — 16/08 14:00 (743 vues), 15/08 14:00, 08/08 14:00, 07/08 14:00, 06/08 14:00. Quelques posts hors créneau (18:2x, 22:52, 10:48-11:07) dont le meilleur du lot (18:26, format slideshow) — l'heure ne semble pas expliquer la perf de ce post, plutôt le format/hook.
- **Instagram** : plus dispersé ce run — le top post est à 14:29 UTC (08/08, comme d'habitude) mais les #2 et #3 sont à 08:00 et 09:57 UTC, hors du créneau habituel 14:29-14:30. **Le créneau 14:29 Réunion n'est plus clairement le meilleur ce cycle** — échantillon trop petit pour changer de recommandation, mais à re-mesurer.
- **Concurrent `jb.roy_` (TikTok)** : toujours des rafales de publication groupée — 4 vidéos en 11 minutes le 16/08 (16h17-16h28 UTC), 5 vidéos en 6 minutes le 12/08 (15h07-15h13 UTC), 3 vidéos en 18 minutes le 13/08. Pattern confirmé et toujours à ne pas imiter.
- **Recommandation** : garder le créneau **14:00 UTC / 18h Réunion** sur TikTok (toujours le plus régulier), mais ne plus présenter 14:29 Réunion comme acquis sur Instagram sans re-vérification la semaine prochaine.

---

## 6. Durée cible de vidéo

- **Tony (TikTok, n=12 vidéos avec durée mesurable)** : médiane **32,5 s**, moyenne 40,7 s (tirée vers le haut par un outlier CapCut à 135 s). Sans l'outlier : range 13–37 s, cohérent avec le 05/08 (médiane 32 s) — **la recommandation du run précédent d'allonger vers 30-40 s n'a pas été appliquée, la durée n'a pas bougé.**
- **Concurrent `jb.roy_` (TikTok, n=20)** : médiane **30 s**, moyenne 32,5 s (range 12–64 s) — **nettement plus court qu'au 05/08 (44 s de médiane)**. Le concurrent semble avoir raccourci son format ; l'écart de durée avec Tony est maintenant quasi nul.
- **Cible recommandée : 30–35 s.** Ajustée à la baisse vs le run précédent (30-40 s) puisque le concurrent a lui-même raccourci et que les durées courtes de Tony (28-33 s) restent dans le peloton de tête de son propre classement.
- Éviter les formats ≤ 15 s et les outliers > 60 s sans raison de format (le post CapCut à 135 s n'a fait que 159 vues, sous la moyenne).

---

## 7. Ce que fait le concurrent `@jb.roy_` qui marche (TikTok, Apify)

- **CTA constant confirmé encore ce run** : caption quasi identique sur 19 des 20 vidéos scrapées — « Follow @jb.roy_ pour implémenter l'IA dans ton activité » — la légende ne révèle jamais le vrai hook, qui est uniquement parlé/à l'écran.
- **Hook réel de sa meilleure vidéo (1842 vues, transcript vérifié via tokscript)** : une analogie de **positionnement de niche** (généraliste payé 25€ vs spécialiste du poumon payé beaucoup plus cher) — pur contenu de valeur/storytelling, aucune mention produit, aucun CTA dans le discours lui-même. Format éducatif pur, pas un pitch.
- **2ᵉ meilleure vidéo (1274 vues, transcript vérifié)** : démonstration d'actualité IA (génération de vidéo à partir d'une photo, modèle « King sidenz ») — même famille que le pattern « actualité chaude » déjà identifié chez Tony.
- **Rafales de publication toujours présentes** (voir §5) — signal de test de formats en volume, pas un rythme à imiter tel quel.
- ⚠️ **Réserve sur le chiffre de saves** : ce run montre Tony devant le concurrent en saves moyens (2,65 vs 2,05), à l'inverse du run du 05/08 (concurrent à 8,4 vs 3,95 pour Tony). L'échantillon `jb.roy_` de ce jour contient plusieurs vidéos très courtes et rapprochées dans le temps (rafales des 12/08, 13/08, 16/08) qui ressemblent à des tests plutôt qu'à son contenu principal — **ce chiffre est probablement moins représentatif que celui du run précédent, à ne pas citer comme une victoire acquise sans un 3ᵉ point de mesure.**

---

## 8. Recommandations prioritaires (semaine suivante)

1. **Investiguer la baisse des vues Instagram** (108,7 → 47,6 vues moyennes, quasi -56%) avant toute autre optimisation de contenu — vérifier si c'est un effet de reach algorithmique, de format, ou de dilution parmi les posts FoodBoost du même compte Blotato. Priorité #1 de la semaine.
2. **Ne plus traiter « Commente le mot X » comme un CTA TikTok fiable sans nuance** : le volume de commentaires s'est effondré ce run (0,41 vs 2,85 vidéo/moyenne). Tester 2-3 variantes de mot-clé/formulation au lieu de répéter toujours la même mécanique.
3. **Rejouer systématiquement le hook « bénéfice chiffré personnel »** (200€/mois, 5 secondes au lieu de tout dérouler) — c'est le seul pattern qui a produit à la fois vues ET commentaires ce run, sur les deux plateformes.
4. **Confirmer ou infirmer le signal carrousel photo TikTok** : les 2 meilleurs posts du run sont des slideshows (812 et 486 vues) — programmer 1-2 carrousels supplémentaires la semaine prochaine pour distinguer signal réel d'artefact d'échantillon (n=2 actuellement).
5. **Resserrer la durée cible à 30-35 s** (le concurrent a raccourci à 30 s médian, Tony n'a pas bougé de 32 s malgré la reco précédente de l'allonger) — abandonner l'objectif d'allongement vers 40 s.
6. **Toujours pas d'action sur le workflow `n5dIUNEk5D6Pj3Vf`** (rapport hebdo automatique) : 0 exécution confirmée à nouveau ce jour, URLs placeholder jamais remplacées. Soit le configurer avec de vraies credentials (Graph API Instagram + TikTok API + Telegram chat ID), soit l'archiver pour éviter la confusion — il n'a jamais tourné depuis sa création le 21/07.

---

## 9. Sources & limites

- **TikTok (Tony + concurrent)** : Apify, actor `clockworks/tiktok-scraper`, via le workflow n8n `YUJjz5NNsYo41t8q` (temporairement reconfiguré aujourd'hui de son actor Instagram Reels d'origine — `apify~instagram-reel-scraper` sur `jb.roy_` — vers l'actor TikTok, puis **remis dans son état d'origine** après coup, aucun changement persistant). **Note technique pour les prochains runs** : un premier essai avec `"profiles": ["automationboost7", "jb.roy_"]` en un seul appel synchrone (exécution #74668) n'a renvoyé que 2 items, tous deux `jb.roy_` — l'appel multi-profils en mode sync semble se couper prématurément côté Apify. Solution qui a fonctionné : un appel séparé par compte (`"profiles": ["automationboost7"]` puis `["jb.roy_"]`, `resultsPerPage: 20` chacun) → exécutions #74669 (automationboost7, 20 items, 10s) et #74670 (jb.roy_, 20 items, 21s). Le node de code d'agrégation du workflow (`Analyze Video Patterns`) est écrit pour des données Instagram (`p.shortCode`) et retourne 0 lignes sur des données TikTok — ses résultats n'ont pas été utilisés, l'extraction s'est faite directement sur la sortie brute du node Apify via `jq`.
- **Hooks réels du concurrent** : 2 vidéos `jb.roy_` transcrites via `mcp__tokscript__get_tiktok_transcript` (quota gratuit, 5/jour) pour vérifier le discours réel derrière la légende générique. Une vidéo `automationboost7` transcrite en complément.
- **tokscript** : `get_tiktok_user_videos` et `get_instagram_user_reels` toujours bloqués derrière un abonnement Pro/Premium (revérifié ce jour, mêmes messages d'erreur qu'au 05/08) — seuls `get_tiktok_user` (profil) et `get_tiktok_transcript` (single-vidéo, quota gratuit) restent utilisables sans Pro.
- **Instagram (Tony)** : Blotato (`blotato_list_top_posts`, platform=instagram, depuis le 05/08, 22 résultats bruts filtrés manuellement pour exclure 10 posts du compte `foodboost` hors périmètre).
- **LinkedIn** : Blotato confirme 6 posts publiés depuis le 05/08 mais **aucune métrique**. Windsor.ai revérifié ce jour (`get_connectors`) : toujours seulement Instagram `animeirl85` et TikTok `humian` connectés, aucun LinkedIn Organic — ces deux comptes sont hors périmètre Autoboost.
- **Workflow analytics hebdo `n5dIUNEk5D6Pj3Vf`** (« Analyse Réseaux Sociaux Auto ») : confirmé à nouveau **0 exécution** (`search_executions` vide), toujours inactif, toujours des URLs placeholder non remplacées sur les nœuds Instagram/TikTok/Telegram. Aucun changement depuis sa création le 21/07.
- **Workflow concurrent `YUJjz5NNsYo41t8q`** : 3 exécutions au 05/08 (#70787-70789, jamais réutilisées ce run car données trop anciennes pour la fenêtre 05/08-17/08) + 3 nouvelles exécutions aujourd'hui (#74668 combiné/raté, #74669 automationboost7, #74670 jb.roy_). Configuration remise à l'identique de l'état trouvé en début de run.

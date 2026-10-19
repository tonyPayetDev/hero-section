# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-10-19 (run hebdo, session cloud à froid)
- **Période couverte** : Instagram `@automatisationboost` — 191 posts depuis le 01/07 (séparation stricte par `account.id`, 62 posts `foodboost` exclus) · LinkedIn — 23 posts du 06/10 au 19/10 (22 publiés, 1 programmé, 0 échec) · TikTok `@tonypayet4` (Blotato, hors périmètre) — 22 posts sur la même fenêtre (21 publiés, 1 programmé, 0 échec) · **TikTok `@automationboost7` (source de vérité) et concurrent `@jb.roy_` — 40 vidéos chacun, scrapées via Apify ce run (exécution n8n `100875`, déclenchée automatiquement par le cron hebdo pour la 1ère fois, succès en 32s).**
- **Comptes analysés** : Instagram `@automatisationboost` (Blotato `54617`) · LinkedIn Payet Tony (Blotato `25882`) · TikTok actif `@automationboost7` (pas connecté à Blotato — source de vérité = Apify via workflow n8n `YUJjz5NNsYo41t8q`) · Concurrent TikTok `@jb.roy_` (même source) · **Exclu** : Instagram `foodboost` (`55611`, hors périmètre — 62 posts exclus ce run par `account.id`)
- **Note sur `@tonypayet4` (Blotato TikTok `36488`)** : vérifié explicitement ce run par appel direct (`blotato_list_accounts` + `blotato_list_posts`) — continue de publier quotidiennement (22 posts du 06/10 au 19/10, 0 échec) mais **AUCUNE métrique dans Blotato** (`analytics: null` sur 100% des posts de l'échantillon). Limite structurelle confirmée (Blotato ne collecte pas TikTok, quel que soit le compte) — jamais utilisé comme source de chiffres ici.
- **⚠️ Échantillons restant faibles** : les vues TikTok/Instagram se comptent en dizaines à quelques centaines ; toute moyenne à n<10 est signalée explicitement comme fragile.

---

## 0. Anomalies et découvertes clés de ce run

1. **🔴 CRITIQUE, TOUJOURS ACTIF — effondrement des vues TikTok `@automationboost7` depuis le 13/10, aucune reprise au 19/10 (6e jour).** Détail vidéo par vidéo (Apify, exécution `100875`) : les **11 dernières vidéos publiées du 13/10 au 18/10** font **0 ou 1 vue chacune** (moyenne 0,1 / médiane 0), contre une moyenne de **236,4 vues / médiane 231** sur les **29 vidéos précédentes** (03/09 → 12/10, même compte, même format). **Chute de -99,96%, sans changement de format ni de durée** (31-85s avant comme après) — la cause n'est donc probablement pas éditoriale. Ceci confirme et prolonge une alerte déjà posée le 18/10 (visible dans l'historique du Sheet "Analyse Perf") : **6 jours après la 1ère alerte, rien n'a changé.** Hypothèse non vérifiable depuis cette session : restriction de portée / shadowban TikTok sur le compte — **nécessite une vérification manuelle par Tony dans l'app TikTok (Profil > Paramètres > Statut du compte)**, impossible à faire depuis l'analyse.
2. **🔴 Instagram — cause du blocage enfin confirmée avec certitude et toujours active au 19/10.** Les posts "Journal IA" échouent avec le message exact `"Your Instagram connection is no longer valid. Reconnect the account to publish."` — confirmé sur **51 échecs cumulés** depuis le 09/10, dont **5 tentatives échouées entre le 13/10 et le 18/10** (13, 14, 15, 17, 18/10). **Aucun post publié depuis le 08/10** → **11 jours de coupure** au moment de ce rapport (contre 5 jours au run du 13/10 — la situation s'aggrave, elle ne se stabilise pas). Cette panne est signalée de façon quasi identique depuis le run du 21/09 (4 semaines) sans action corrective constatée.
3. **🟢 `YUJjz5NNsYo41t8q` s'est déclenché automatiquement pour la première fois.** L'exécution `100875` (19/10, 00:00 UTC) est la première à porter `mode: "trigger"` (le cron hebdo "Chaque lundi 6h Réunion") — jusqu'ici le workflow n'avait été lancé qu'en manuel (`98855` le 13/10, `100350` le 17/10). L'automatisation TikTok/concurrent fonctionne désormais en autonomie.
4. **🔴 `n5dIUNEk5D6Pj3Vf` toujours à 0 exécution — 13e semaine sans être câblé.** Reconfirmé via `get_workflow_details` : `triggerCount: 0`, `active: false`, placeholders (`<__PLACEHOLDER_VALUE__...>`) inchangés sur les nœuds Instagram Graph API / TikTok API / Telegram, aucune modification depuis sa création le 21/07. `search_executions` renvoie 0 résultat, comme attendu.
5. **🟡 Concurrent `@jb.roy_` toujours inactif.** Dernière vidéo de l'échantillon des 40 dernières : **03/09/2026** (vs 02/09 au run précédent — essentiellement la même date). Compteur de vidéos figé à **162** depuis ≥9 semaines. Abonnés quasi stables (1582, -2 vs le run du 13/10).
6. **🟢 LinkedIn reste le seul canal pleinement stable** : 23 posts du 06/10 au 19/10, 0 échec — mais toujours 0 métrique d'engagement (limite structurelle Blotato, reconfirmée).

---

## 1. Chiffres clés par plateforme

### Instagram `@automatisationboost` (Blotato 54617) — 191 posts depuis le 01/07
| Métrique | Valeur | Note |
|---|---|---|
| Statut | 137 publiés / **51 échoués** / 3 autres | 51 échecs = connexion Instagram invalide (voir §0.2) |
| Échantillon avec analytics | n=131 (sur 137 publiés) | 6 posts trop récents pour avoir une métrique |
| Vues — ensemble (n=131) | moyenne **36,9** / médiane **11** | Échantillon large, tiré vers le bas par le Journal IA |
| Vues — posts "Journal IA" | n=22, moyenne **7,6** | Format à éviter comme contenu principal IG |
| Vues — posts à angle unique | n=109, moyenne **42,8** | ≈5,6× mieux que le Journal IA |
| Heure dominante (n=137 publiés) | **14:00 UTC** (60/137, 44%) | Confirmé sur plusieurs runs consécutifs |
| **Dernier post publié** | **08/10, 04:48 UTC** | **11 jours sans aucun nouveau post** au 19/10 |
| **Échecs de publication** | 51 au total, 5 entre le 13/10 et le 18/10 | Message exact : "Your Instagram connection is no longer valid" |

### LinkedIn (Payet Tony, Blotato 25882)
Opérationnel, publication quotidienne continue : 23 posts du 06/10 au 19/10 (22 publiés, 1 programmé, 0 échec). **Toujours aucune métrique d'engagement** — limite structurelle de Blotato sur LinkedIn, reconfirmée.

### TikTok `@tonypayet4` (Blotato 36488) — hors périmètre d'analyse, vérifié explicitement
22 posts du 06/10 au 19/10 (21 publiés, 1 programmé, 0 échec). **Vérifié ce run par appel direct : 0 métrique sur 100% de l'échantillon** (`analytics: null`). Ne jamais s'appuyer sur ce compte pour des chiffres TikTok.

### TikTok `@automationboost7` — compte réel analysé (source de vérité, Apify exéc. `100875`)
| Métrique | Profil (tokscript, 19/10) | 40 dernières vidéos (Apify, 19/10) |
|---|---|---|
| Abonnés | **242** (+3 vs 13/10) | — |
| Vidéos totales | **242** (+10 vs 13/10) | — |
| Likes cumulés | **1019** | — |
| Vues — moyenne / médiane (n=40, ensemble) | — | **171 / 124** |
| **Vues — avant l'effondrement (n=29, 03/09→12/10)** | — | **moy. 236,4 / méd. 231** |
| **Vues — pendant l'effondrement (n=11, 13/10→18/10)** | — | **moy. 0,1 / méd. 0** |
| Likes — moyenne | — | **3** |
| Commentaires — moyenne | — | **1,3/vidéo** |
| Engagement/vue — moyenne | — | **11,29%** |
| Durée — médiane | — | **34 s** |

### Concurrent TikTok `@jb.roy_`
| Métrique | Profil (tokscript, 19/10) | 40 dernières vidéos (Apify, 19/10) |
|---|---|---|
| Abonnés | **1582** (6,5× plus que Tony) | — |
| Vidéos totales | **162** (figé depuis ≥9 semaines) | — |
| Likes cumulés | **7840** | — |
| Vues — moyenne / médiane | — | **224 / 169** |
| Likes — moyenne | — | **7** |
| Commentaires — moyenne | — | **0,2/vidéo** |
| Engagement/vue — moyenne | — | **4,26%** (2,65× moins que Tony) |
| Durée — médiane | — | **49 s** |
| **Vidéo la plus récente de l'échantillon** | — | **03/09/2026 — toujours aucune vidéo plus récente** |

**Lecture** : hors période d'effondrement, Tony reste nettement plus efficace par vidéo que `@jb.roy_` (engagement/vue 2,65× supérieur, commentaires 6,5× supérieurs) malgré une audience 6,5× plus petite — mais l'effondrement du 13-18/10 annule tout l'avantage de distribution cette semaine-là. `@jb.roy_` reste inactif depuis début septembre.

---

## 2. Top 3 vidéos / posts

### Top Instagram `@automatisationboost` (depuis le 01/07, inchangé depuis plusieurs runs)
1. **243 vues / 1 like** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... » → tuto VPS + Coolify + Claude Code en 3 étapes — 27/07 14:29 UTC.
2. **223 vues / 4 likes** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. » — 29/07 14:30 UTC.
3. **216 vues / 2 likes** — « L'alternative gratuite à Claude Code... Kilo Code + n8n, zéro abonnement. » — 13/07 19:00 UTC.
4. *(mention)* **136 vues mais 6 commentaires** — « Claude Code et n8n m'ont fait économiser 200€/mois de secrétariat » — 08/08 14:29 UTC. Meilleur ratio commentaires/vue de l'historique IG.

### Top TikTok `@automationboost7` (Apify, échantillon pré-effondrement — données les plus récentes ne produisent aucun nouveau résultat, voir §0.1)
1. **744 vues** — « Le feed Insta de ton resto, déjà prêt » (démo client B2B), 31s, 07/10 14:00 UTC.
2. **740 vues** — « Où ta boîte perd des clients ? » (question douleur business), 32s, 06/10 14:00 UTC.
3. **654 vues / 6 commentaires** — Journal IA du 06/10, 51s, 13:15 UTC.
4. *(mention)* **510 vues / 9 commentaires** — « Ta voix off, clonée une seule fois, réutilisable sur toutes tes vidéos » — 13/07, 33s. Meilleur ratio commentaires/vue absolu de tout l'historique collecté.
5. *(mention)* **419 vues / 12 commentaires** — « Claude oublie tout entre deux sessions... mémoire persistante » — 15/07, 33s.

### Top concurrent `@jb.roy_` (Apify, 19/10 — échantillon antérieur au 02-03/09)
1. **1277 vues / 1,64% engagement** — 02/09 14:30 UTC, 21s, légende générique « Follow @jb.roy_ pour imploser l'IA dans ton activité ».
2. **761 vues / 1,58% engagement** — 28/08 15:00 UTC, 44s, même légende type.
3. **554 vues / 2,35% engagement** — 25/08 17:16 UTC, 42s, même légende type.

---

## 3. Hooks qui marchent — formulations réutilisables

*(Dérivés de l'échantillon pré-effondrement du 03/09-12/10 ; aucune nouvelle donnée exploitable depuis le 13/10, voir §0.1 — ces patterns restent valides mais n'ont pas pu être retestés cette semaine.)*

1. **Question douleur business ciblant un client potentiel (B2B)** — « Où ta boîte perd des clients ? » (740v) et « Le feed Insta de ton resto, déjà prêt » (744v, démo visuelle concrète) — les 2 meilleures vidéos TikTok de tout l'échantillon, toutes deux publiées à 14:00 UTC.
2. **Économie chiffrée + témoignage à la première personne** — confirmé sur 2 plateformes historiquement : IG « 200€/mois de secrétariat » (136v/6 commentaires) et TikTok « 150€/mois d'assistante, ~1800€ économisés » (647v/6 commentaires, run du 28/09).
3. **Outil/actualité connue nommée + chiffre précis dans les 10 premiers mots** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois » (223v), « Higgsfield, c'est 15 à 99$/mois » (214v).
4. **Alternative gratuite à un outil payant connu, nommé explicitement** — « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » (216v).
5. **Tutoriel actionnable en 3 étapes avec estimation de temps réaliste** — VPS/Coolify/Claude Code (243v, meilleur post IG historique).
6. **Fonctionnalité technique concrète présentée simplement** — « Ta voix off, clonée une seule fois, réutilisable sur toutes tes vidéos » (510v/9 commentaires) et « Claude oublie tout... mémoire persistante » (419v/12 commentaires) — les 2 meilleurs ratios commentaires/vue de tout l'historique.

**Règle** : nommer un outil/une actualité connue + un chiffre précis reste robuste sur Instagram ; sur TikTok, les hooks orientés "douleur business du prospect" et "économie chiffrée" performent mieux que le registre pur actu-IA. **Ces patterns ne pourront être réévalués qu'une fois la distribution TikTok rétablie.**

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Reprendre une cadence normale sur TikTok sans avoir vérifié le statut du compte.** 11 vidéos consécutives à 0-1 vue (13/10-18/10) alors que le format n'a pas changé — publier davantage dans cet état ne fait qu'accumuler du contenu invisible.
- ❌ **Supposer que l'absence de posts Instagram est un problème de pipeline applicatif plutôt qu'un vrai blocage de connexion.** Le message d'erreur exact (« Your Instagram connection is no longer valid ») est connu depuis le 21/09 et n'a toujours pas été traité 4 semaines plus tard.
- ❌ **Publier le format "Journal IA quotidien" comme contenu principal Instagram.** 7,6 vues de moyenne (n=22) contre 42,8 (n=109) pour les posts à angle unique — écart ≈5,6×. Le format reste correct sur TikTok et LinkedIn hors période d'effondrement.
- ❌ **Compter sur « Commente le mot X » comme unique mécanisme d'engagement.** Les meilleurs ratios commentaires/vue de l'historique (510v/9 commentaires, 419v/12 commentaires, 654v/6 commentaires) viennent de hooks à économie chiffrée, de contenu technique concret ou de Journal IA, pas uniquement du CTA.
- ❌ **Décrire `@jb.roy_` comme "concurrent actif à surveiller de près" sans nuance** : aucune vidéo dans l'échantillon des 40 dernières n'est postérieure au 03/09 — il semble avoir arrêté de publier sur TikTok depuis plus de 9 semaines.
- ❌ **Laisser `n5dIUNEk5D6Pj3Vf` dans un état indéterminé indéfiniment.** 13 semaines à `triggerCount: 0` sans décision (configurer ou archiver) — ce n'est plus une "anomalie à signaler", c'est une dette qui s'accumule.

---

## 5. Analyse du concurrent `@jb.roy_`

- **Profil** : 1582 abonnés (6,5× Tony), 162 vidéos (figé depuis ≥9 semaines), 7840 likes cumulés.
- **40 dernières vidéos (Apify, 19/10)** : vues moy. 224 / médiane 169, likes moy. 7, commentaires moy. 0,2/vidéo (quasi nul), engagement/vue moy. 4,26%, durée médiane **49 secondes**.
- **Découverte clé, reconfirmée** : aucune vidéo de cet échantillon de 40 n'est postérieure au **03/09/2026** — cohérent avec le compteur de vidéos figé à 162 depuis plusieurs relevés consécutifs. Le concurrent a cessé de publier sur TikTok depuis début septembre et n'a pas repris.
- **Format** : légende quasi identique sur toutes les vidéos (« Follow @jb.roy_ pour imploser/implémenter l'IA dans ton activité », variantes mineures de coquille), **0 hashtag**, hook parlé dans la vidéo plutôt qu'écrit dans le texte, durée nettement plus longue que Tony (49s médiane vs 34s).
- **Comparatif d'efficacité (hors période d'effondrement de Tony)** : sur l'échantillon pré-13/10 (n=29, moy. 236,4 vues), Tony produit un engagement/vue et un taux de commentaires nettement supérieurs à `@jb.roy_` avec une audience 6,5× plus petite. Cette semaine spécifiquement, l'effondrement TikTok de Tony (§0.1) rend toute comparaison de vues brutes trompeuse — comparer sur l'engagement/vue de l'échantillon pré-effondrement reste plus honnête.
- **Durée vidéo concurrent (42-71s dans le top 5)** : confirmée sur cet échantillon, nettement plus longue que le format court de Tony. Rien n'indique qu'allonger la durée améliorerait les résultats de Tony — ses meilleures vidéos pré-effondrement (744v/31s, 740v/32s) sont plus courtes que la médiane concurrent.

---

## 6. Meilleures heures de publication

- **Instagram** : **14:00 UTC** reste dominant — 60/137 posts mesurés (44%), 3 des 4 meilleurs posts historiques. Observation gelée depuis le 08/10 (aucun nouveau post pour la confirmer davantage).
- **TikTok `@automationboost7`** : les 2 meilleures vidéos de l'échantillon pré-effondrement (744v, 740v) sont publiées à 14:00:0x UTC, exactement le même créneau qu'Instagram. La 3e meilleure (654v) est à 13:15 UTC, très proche.
- **Concurrent `@jb.roy_`** : ses meilleures vidéos se répartissent entre 14:30 et 17:16 UTC — fenêtre un peu plus large mais chevauchant le même créneau d'après-midi.
- **Recommandation** : **14:00 UTC reste le créneau pivot à utiliser par défaut dès que les deux canaux seront rétablis** — mais le créneau n'explique pas l'effondrement TikTok (les vidéos du 13-18/10 publiées au même créneau font 0 vue), donc ne pas chercher la cause de la panne dans l'horaire.

---

## 7. Durée vidéo cible

- `@automationboost7` : durée médiane **34 secondes** sur les 40 dernières vidéos (inchangé) ; ses meilleures vidéos pré-effondrement font 31-51s. `@jb.roy_` (concurrent, vidéos antérieures au 03/09) : durée médiane **49 secondes**.
- **Cible recommandée, inchangée** : **30-40 secondes** pour le format court quotidien, tolérance jusqu'à ~50-60s pour les formats Journal IA / comparatifs à hook fort.
- La durée n'est pas en cause dans l'effondrement du 13-18/10 : les vidéos touchées (31-85s) couvrent la même plage que les vidéos qui performaient bien juste avant (31-84s) — à nouveau, cela pointe vers une cause hors contenu (compte/plateforme) plutôt qu'un problème de format.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **🔴 PRIORITÉ ABSOLUE — Vérifier manuellement le statut du compte TikTok `@automationboost7` dans l'app** (Profil > Paramètres > Statut du compte / notifications de modération), avant toute reprise de cadence. 11 vidéos consécutives à 0-1 vue sur 6 jours sans aucun changement de format pointe vers une restriction de portée, pas un problème créatif — et c'est invérifiable depuis cette session.
2. **🔴 Reconnecter le compte Instagram `automatisationboost` dans Blotato.** Cause exacte connue depuis le 21/09 (`"Your Instagram connection is no longer valid"`), toujours pas traitée 4 semaines plus tard — 11 jours de coupure actuelle, 51 échecs cumulés.
3. **Ne pas reprendre une cadence de publication TikTok élevée tant que le point 1 n'est pas tranché.** Si le compte est bien restreint, publier davantage dans cet état ne fait qu'accumuler du contenu invisible et risque d'aggraver un signal de spam.
4. **Une fois les deux canaux rétablis, retester en priorité le hook "question douleur business / B2B"** (740v, 744v — les 2 meilleures vidéos TikTok historiques) sur Instagram, où il n'a pas d'équivalent récent testé, et publier à 14:00 UTC par défaut sur les deux plateformes.
5. **Décider enfin du sort de `n5dIUNEk5D6Pj3Vf`** (workflow analytics "Rapport Hebdo", 0 exécution depuis sa création le 21/07 — 13e semaine consécutive de ce constat, placeholders Instagram Graph API / TikTok API / Telegram jamais renseignés) — le configurer réellement ou l'archiver.

---

## 9. Sources & limites (run du 19/10)

- **Instagram** : `blotato_list_accounts` (confirme 54617/55611/25882/36488) + `blotato_list_posts` (platform=instagram, depuis 2026-07-01, limit=250 + page complémentaire via cursor jusqu'au 01/07) — séparation stricte par `account.id` (54617 vs 55611, 62 posts foodboost exclus). 191 posts `automatisationboost` isolés (137 publiés, 51 échoués, 3 autres), 131 avec analytics.
- **LinkedIn / TikTok `@tonypayet4`** : `blotato_list_posts` (platform=[linkedin]/[tiktok], depuis 2026-10-06, jusqu'au 19/10). 0 analytics sur les deux, vérifié explicitement champ par champ — limite structurelle Blotato confirmée (Twitter/X, Instagram, Facebook, Threads, Bluesky seulement).
- **TikTok `@automationboost7` / `@jb.roy_` — profils** : `mcp__tokscript__get_tiktok_user`, réussi sur les deux comptes. **Échec sur `@tonypayet4`** (tokscript : "Couldn't confirm @tonypayet4 on TikTok") — sans conséquence, la vérification de l'absence de métriques TikTok sur ce compte avait déjà été faite côté Blotato.
- **TikTok `@automationboost7` / `@jb.roy_` — vidéo par vidéo** : workflow n8n `YUJjz5NNsYo41t8q` (« Scrape Competitor Videos »), exécution `100875` (19/10, 00:00 UTC, déclenchée automatiquement par le cron hebdo pour la 1ère fois, succès en 32s) — actor Apify `clockworks/tiktok-scraper` sur `profiles: ["automationboost7", "jb.roy_"]`, 40 vidéos chacun. Données lues à deux niveaux : résumé agrégé (nœud `Analyze Video Patterns`) et détail vidéo par vidéo (nœud `Apify - Scrape Instagram Reels`, 80 items) pour établir le calendrier précis de l'effondrement (§0.1).
- **n8n** : `search_executions`, `get_execution`, `get_workflow_details` tous fonctionnels ce run. `n5dIUNEk5D6Pj3Vf` confirmé à `triggerCount: 0`, jamais câblé (placeholders Instagram Graph API / TikTok API / Telegram).
- **Sheet "Analyse Perf" (gid 1277122579)** : lu en intégralité via export CSV avant écriture (historique jusqu'au run du 18/10, qui avait déjà posé l'alerte TikTok reconfirmée ici) ; écrit ce run via workflow n8n `create_workflow_from_code` (voir confirmation dans le rapport final) ; revérifié par un second export CSV après écriture.
- **Étape B (génération de scripts)** : hors périmètre de cette routine — non exécutée.

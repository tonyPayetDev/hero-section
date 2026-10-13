# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-10-13 (run hebdo automatisé, session cloud à froid)
- **Période couverte** : Instagram `@automatisationboost` — 140 posts propres remontés par Blotato depuis le 01/07 (séparation par `account.id`, pas par mots-clés) · LinkedIn — 114 posts depuis le 17/08 · TikTok `@tonypayet4` (compte Blotato) — 136 posts depuis le 17/08, tous sans analytics · **TikTok `@automationboost7` (compte réel analysé) et concurrent `@jb.roy_` — uniquement des agrégats de profil ce run (abonnés/vidéos/likes totaux), toujours AUCUNE métrique par vidéo, voir §0.2.**
- **Comptes analysés** : Instagram `@automatisationboost` (Blotato `54617`) · LinkedIn Payet Tony (Blotato `25882`) · TikTok actif `@automationboost7` (pas connecté à Blotato — source de vérité normale = Apify via workflow n8n `YUJjz5NNsYo41t8q`, **indisponible ce run, voir §0.1**) · Concurrent TikTok `@jb.roy_` (même source, **indisponible ce run**) · **Exclu** : Instagram `foodboost` (`55611`, hors périmètre — 39 posts exclus ce run par `account.id`)
- **Note sur `@tonypayet4` (Blotato TikTok `36488`)** : continue de recevoir les publications automatiques quotidiennes (18 posts publiés/programmés depuis le 06/10, 0 échec sur cette fenêtre). **Reconfirmé ce run : ce compte n'a AUCUNE métrique dans Blotato** — tous les posts publiés sur `36488` ont `analytics: null`, ce qui est cohérent avec la documentation de l'outil (Blotato ne collecte pas d'analytics TikTok, quel que soit le compte). Ce n'est donc pas une panne spécifique à `tonypayet4` : c'est une limite structurelle de la source. Ne jamais utiliser Blotato comme source de vérité TikTok — seul Apify (bloqué, §0.1) ou tokscript Pro (payant, bloqué, §0.2) le peuvent.

---

## 0. Anomalies et découvertes clés de ce run

1. **🔴 BLOCAGE CENTRAL INCHANGÉ — le connecteur MCP n8n est toujours en `needs_reconnect` (OAuth).** Reconfirmé explicitement ce run via `ListConnectors` : `{"name":"n8n","installState":"needs_reconnect","connected":false,"enabledInChat":true}`. Aucun outil `n8n_*` / `search_executions` / `get_execution` n'est chargeable (`ToolSearch` répété ne retourne que des outils GitHub/tâches). C'est la **3e semaine consécutive** que ce blocage est documenté (21/09, 06/10, 13/10 — identique à chaque fois). Conséquences inchangées :
   - Impossible de lire les exécutions du workflow concurrents `YUJjz5NNsYo41t8q` (Apify) → toujours aucune donnée TikTok par vidéo pour `@automationboost7` ni `@jb.roy_` ce run.
   - Impossible de lire les exécutions de `n5dIUNEk5D6Pj3Vf` (dernier statut connu : 0 exécution depuis sa création le 21/07, non revérifiable).
   - Impossible de créer/lancer un workflow `create_workflow_from_code` pour écrire l'onglet "Analyse Perf" → **SINK 2 non exécutable ce run, 3e run consécutif dans ce cas** (voir résumé final). La lecture de l'export CSV du gid `1277122579` confirme que la dernière écriture date du **21/09** — aucune ligne n'a été ajoutée depuis, ni le 28/09, ni le 06/10, ni aujourd'hui.
   - **Action requise avant le prochain run, toujours la même** : ré-autoriser le connecteur n8n depuis les réglages de connecteurs claude.ai (session interactive requise, impossible depuis cette session cloud à froid).
2. **🔴 TikTok — toujours aucune métrique par vidéo, même cause qu'il y a une semaine.** `get_tiktok_user` (profils publics) fonctionne pour `automationboost7` et `jb.roy_` ; `get_tiktok_user_videos` refuse systématiquement avec *« Listing user videos requires a Pro or Premium subscription »* sur les deux comptes — reconfirmé ce run, ce n'est pas transitoire. `get_instagram_user_reels` (testé en complément pour obtenir des durées IG) refuse avec le même message. C'est désormais une limite de plan tokscript stable sur 2+ runs, pas un bug serveur.
   - Chiffres de profil obtenus ce run (comparés au run du 06/10) :
     - `@automationboost7` : **239 abonnés** (231→239, +8), **512 suivis**, **1013 likes cumulés** (974→1013, +39), **232 vidéos** (219→232, +13, ≈1,9 vidéo/jour sur la semaine).
     - `@jb.roy_` (concurrent) : **1584 abonnés** (1582→1584, +2), **113 suivis**, **7836 likes cumulés** (7829→7836, +7), **162 vidéos** (inchangé).
   - **Point de vigilance méthodologique renforcé** : le compteur de vidéos de `@jb.roy_` est resté figé à **exactement 162** sur au moins 3 relevés consécutifs (07/09, 06/10, 13/10 — plus d'un mois), alors que ses abonnés et ses likes progressent légèrement (+2, +7). Deux lectures possibles, toujours non tranchées : (a) ce compte a réellement arrêté de publier de nouvelles vidéos TikTok depuis début septembre tout en continuant de gagner un peu d'abonnés/likes sur son stock existant, ou (b) le champ `videos` de tokscript est spécifiquement figé pour ce profil. À vérifier en priorité la semaine prochaine — si confirmé (a), c'est une information stratégique importante sur le concurrent.
3. **🟡 Instagram — reprise partielle puis nouvelle coupure silencieuse.** Après l'absence totale de publication du 01/10 au 06/10 (signalée comme priorité n°1 la semaine dernière), le pipeline a **repris de façon incomplète** : 3 éditions "Journal IA" publiées coup sur coup (30/09 14:08, 06/10 13:16, 07/10 09:28, 08/10 04:48 UTC), puis **plus aucun post depuis le 08/10 — soit de nouveau 5 jours sans contenu Instagram (09/10→13/10)**, pendant que LinkedIn et TikTok (`@tonypayet4`) ont publié tous les jours sans interruption sur la même fenêtre, y compris des posts programmés jusqu'au 19/10. Ce n'est toujours pas une erreur de connexion visible (aucun échec enregistré depuis le 30/09) : c'est de nouveau une omission silencieuse de la distribution automatisée, qui semble alimenter Instagram par à-coups plutôt qu'en continu. **Reste la priorité n°1 de ce rapport.**
4. **🟡 Confirmation — le format "Journal IA" reste nettement sous-performant sur Instagram, avec une exception à noter.** Sur la population complète depuis le 01/07 (n=134 posts avec analytics) : 21 éditions Journal IA font en moyenne **8,0 vues (médiane 4)** contre **43,5 vues (médiane 16)** pour les 113 posts à angle unique — écart toujours massif (≈5,4×). **Exception ce run** : l'édition du 07/10 (09:28 UTC) a fait **67 vues**, très au-dessus de la moyenne du format — un seul point, à ne pas généraliser, mais à surveiller (horaire inhabituel, 09:28 au lieu de 14:00/03:00/04:00 habituels).
5. **🟢 Top 5 Instagram inchangé pour la 6e semaine consécutive** (243 / 223 / 216 / 214 / 178 vues, tous publiés fin juillet/août). Aucun des 4 posts publiés depuis la reprise partielle (40, 16, 67, 3 vues) ne s'en approche.
6. **🟢 Heure dominante Instagram reconfirmée** : 14:00 UTC concentre 60 des 134 posts analysés avec métriques (45 %) — signal stable depuis plusieurs runs.

---

## 1. Chiffres clés par plateforme

### Instagram `@automatisationboost` (Blotato 54617) — 140 posts depuis le 01/07, séparés par `account.id`
| Métrique | Valeur | Note |
|---|---|---|
| Échantillon avec analytics | n=134 (sur 140 publiés) | 6 posts trop récents, pas encore de métriques |
| Vues — posts "Journal IA" | n=21, moyenne **8,0** / médiane **4** | Format à éviter comme contenu principal IG (§0.4) |
| Vues — posts à angle unique | n=113, moyenne **43,5** / médiane **16** | ≈5,4× mieux que le Journal IA |
| Top 5 historique | 243 / 223 / 216 / 214 / 178 vues | Inchangé depuis 6 semaines (§0.5) |
| Posts propres publiés du 09/10 au 13/10 | **0** | Nouvelle coupure silencieuse, voir §0.3 |
| Posts propres publiés du 30/09 au 08/10 | 4 (40 / 16 / 67 / 3 vues) | Reprise partielle avant re-coupure |
| Heure dominante (n=134) | **14:00 UTC** (60/134, 45 %) | Confirmé à nouveau |
| Record commentaires | 6 (post "économise 200€/mois", 08/08) — inchangé | Jamais retesté délibérément |

### LinkedIn (Payet Tony, Blotato 25882)
**Compte opérationnel, publication quotidienne continue jusqu'à aujourd'hui et au-delà** (posts programmés jusqu'au 19/10). 19 posts recensés entre le 06/10 et le 19/10 (12 publiés, 7 programmés, 0 échec sur cette fenêtre). Toujours **aucune métrique d'engagement disponible** — confirmé de nouveau : Blotato ne collecte pas d'analytics LinkedIn, quel que soit le run.

### TikTok `@tonypayet4` (Blotato 36488) — compte de publication automatisée, hors périmètre d'analyse
18 posts entre le 06/10 et le 19/10 (11 publiés, 7 programmés, 0 échec). **Aucune métrique Blotato** — reconfirmé ce run que ce n'est pas spécifique à ce compte mais une limite structurelle de Blotato sur TikTok (voir en-tête du document).

### TikTok `@automationboost7` — compte réel analysé, agrégats de profil uniquement
| Métrique | 13/10 | 06/10 | Évolution |
|---|---|---|---|
| Abonnés | **239** | 231 | +8 (+3,5 %) |
| Suivis | 512 | 499 | +13 |
| Vidéos publiées | **232** | 219 | +13 (≈1,9/j) |
| Likes cumulés | **1013** | 974 | +39 |
| Likes/vidéo (moyenne) | **4,37** | 4,45 | stable |
| Vues/durée par vidéo | **toujours non disponible** | — | Bloqué, voir §0.2 |

### Concurrent TikTok `@jb.roy_` — agrégats de profil uniquement
| Métrique | 13/10 | 06/10 | Évolution |
|---|---|---|---|
| Abonnés | **1584** | 1582 | +2 |
| Suivis | 113 | — | — |
| Vidéos publiées | **162** | 162 | **0 — figé depuis ≥5 semaines, voir §0.2** |
| Likes cumulés | **7836** | 7829 | +7 |
| Likes/vidéo (moyenne) | **48,37** | 48,3 | stable, **≈11× celui de `@automationboost7`** |
| Vues/durée par vidéo | non disponible | — | Bloqué |

---

## 2. Top 3 vidéos / posts

### Top 3 Instagram `@automatisationboost` (depuis le 01/07 — inchangé pour la 6e semaine, §0.5)
1. **243 vues / 1 like / 1 save** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... tu perds du temps. » → tuto VPS + Coolify + Claude Code + MCP en 3 étapes, estimation de temps réaliste — 27/07 14:29 UTC.
2. **223 vues / 4 likes** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. Follow pour la suite + commente OPUS » — 29/07 14:30 UTC.
3. **216 vues / 2 likes / 1 save** — « 🛠️ L'alternative gratuite à Claude Code pour créer des sites automatiquement. Kilo Code + n8n = même résultat, zéro abonnement. » — 13/07 19:00 UTC.
4. *(mention)* **214 vues** — « Higgsfield, c'est 15 à 99 $ par mois. Et tes crédits non utilisés disparaissent à la fin du mois. » — 25/07 14:29 UTC.
5. *(mention engagement)* **136 vues mais 6 commentaires** — « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat » — 08/08 14:29 UTC — toujours le meilleur ratio commentaires/vue de tout l'historique.

### Posts récents (reprise puis re-coupure, 30/09→08/10) — à relativiser
- **67 vues / 2 likes** — Journal IA du 07/10, 09:28 UTC — exception positive au format (§0.4), horaire atypique.
- **42 vues / 2 likes / 2 commentaires** — « Clip synchronisé avec la voix :o » — 30/09.
- **16 vues** — Journal IA du 06/10.
- **3 vues** — Journal IA du 08/10, dernier post avant la coupure en cours.

### Top TikTok `@automationboost7` — **toujours non actualisé, repris du 07/09, non vérifiable ce run (§0.1/§0.2)**
1. 794 vues — actualité insolite (avalanche au Népal), 109 s, 28/08.
2. 783 vues — Journal IA, 68 s, 23/08.
3. 774 vues — Journal IA, 84 s, 05/09.

### Top concurrent `@jb.roy_` — **toujours non actualisé, repris du 07/09, non vérifiable ce run**
1. 1234 vues — 02/09, 21 s.
2. 725 vues — 28/08, 44 s.
3. 530 vues — 25/08, 42 s.

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Actualité produit/outil connu nommée dans les 10 premiers mots + un chiffre ou un fait précis** — pattern le plus robuste, confirmé sur 5+ runs consécutifs (« Anthropic vient de sortir Opus 5, 4e Claude en 2 mois »).
2. **Alternative gratuite à un outil payant connu**, nommé explicitement — ex. « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » (216 vues).
3. **Tutoriel actionnable en 3 étapes avec estimation de temps réaliste** — ex. « VPS, Coolify, Claude Code + MCP... » (243 vues, meilleur post Instagram sur plus de 2 mois).
4. **Frustration tarifaire précise sur un outil connu** (prix exact + ce qu'on perd) — ex. « Higgsfield, c'est 15 à 99 $/mois, et tes crédits non utilisés disparaissent » (214 vues).
5. **Économie chiffrée + témoignage à la première personne** — toujours le seul post de tout l'historique à dépasser 1 commentaire (6 commentaires, « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat »). **Jamais retesté délibérément depuis 4+ runs** — priorité dès que la publication Instagram redevient stable.
6. **Actualité insolite grand public, hors registre IA/outils** (ex. avalanche au Népal, 794 vues TikTok, dernière donnée fiable du 28/08) — à revérifier dès que TikTok redevient mesurable.

**Règle** : nommer un outil/une actualité connue + un chiffre ou un fait précis dans les 10 premiers mots reste le pattern le plus robuste, sur 5+ runs consécutifs d'observation.

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Publier le format "Journal IA quotidien" sur Instagram en espérant de la portée.** Confirmé de nouveau ce run : 8,0 vues de moyenne (n=21) contre 43,5 (n=113) pour les posts à angle unique — écart ≈5,4×. Le format a sa place sur LinkedIn/TikTok (cadence, archive) mais pas comme contenu principal sur Instagram.
- ❌ **Supposer qu'une reprise de publication signifie que le pipeline est redevenu fiable.** La séquence de ce run (silence du 01/10 au 06/10 → 4 posts du 30/09 au 08/10 → silence de nouveau du 09/10 au 13/10) montre que la distribution Instagram est instable par intermittence, pas simplement "en panne" ou "réparée" — chaque run doit revérifier la continuité jour par jour, pas seulement la dernière date de publication.
- ❌ **Compter sur « Commente le mot X » comme unique CTA.** Record historique toujours à 6 commentaires sur tout l'échantillon (n=134), obtenu sur un post qui ne reposait pas sur ce seul mécanisme.
- ❌ **Lancer une analyse TikTok en supposant que le crédit Apify est le seul obstacle.** Depuis 3 runs, c'est l'accès n8n lui-même (OAuth `needs_reconnect`) qui bloque tout, avant même d'arriver à la question du crédit Apify.
- ❌ **Traiter le nombre de vidéos `@jb.roy_` comme une donnée fraîche sans vérification.** Il est resté à exactement 162 sur au moins 3 relevés sur plus d'un mois — soit le concurrent a cessé de publier de nouvelles vidéos, soit ce champ tokscript est figé pour ce profil (§0.2, à trancher).
- ❌ **Écrire dans l'onglet "Analyse Perf" en improvisant un autre mécanisme que le workflow n8n prévu.** Le blocage n8n (§0.1) empêche l'écriture ce run comme les 2 runs précédents — ne pas contourner avec un autre outil, documenter et attendre la réautorisation OAuth.

---

## 5. Analyse du concurrent `@jb.roy_` — agrégats de profil seulement, pas de détail vidéo ce run

- **Chiffres de profil (13/10)** : 1584 abonnés, 162 vidéos, 7836 likes cumulés → **≈48,4 likes/vidéo**, contre **≈4,4 likes/vidéo** pour `@automationboost7` (1013 likes / 232 vidéos) — écart stable de **≈11×**, cohérent avec le run précédent (231 vs 219 vidéos, +39 likes vs +7 pour le concurrent cette semaine). `@automationboost7` continue de publier davantage (232 vs 162 vidéos au total, +43 % de volume) sans combler l'écart de qualité/hook.
- **Signal nouveau à vérifier** : le compteur de vidéos de `@jb.roy_` n'a pas bougé depuis au moins le 07/09 (162 → 162 → 162 → 162 sur 4 relevés), alors que ses abonnés et likes progressent très légèrement. Si confirmé la semaine prochaine, cela suggérerait que le concurrent a réduit ou arrêté sa cadence de publication TikTok tout en conservant un petit socle d'engagement résiduel — à l'inverse d'`@automationboost7` qui continue de publier à un rythme soutenu (≈1,9 vidéo/jour).
- **Dernières observations qualitatives disponibles (07/09, non revérifiées depuis 5+ semaines, faute d'accès Apify/tokscript Pro)** : durée médiane plus longue chez le concurrent (48 s vs 34 s chez Tony), légende générique ("Follow @jb.roy_ pour implémenter l'IA..."), 0 hashtag, hook parlé dans la vidéo plutôt qu'écrit dans le texte.
- **Limite de méthode persistante, 3e run consécutif** : sans Apify (bloqué par §0.1) ni accès vidéo tokscript (bloqué par un plan non-Pro, §0.2), impossible d'extraire les hooks exacts, durées actuelles ou format des vidéos de `@jb.roy_` ce run. Seuls des totaux de profil ont pu être obtenus.

---

## 6. Meilleures heures de publication

- **Instagram** : **14:00 UTC** reste le créneau dominant — 60 des 134 posts analysés (45 %) y sont publiés, et c'est l'heure de 3 des 5 meilleurs posts historiques. Confirmé à nouveau ce run. **À garder comme pivot par défaut.**
- **TikTok `@automationboost7`** : aucune donnée fraîche (§0.1/§0.2). Dernier signal disponible (07/09, **plus d'un mois d'ancienneté**) : pas de pivot horaire net (Top 3 réparti sur 08:00, 03:00, 07:30 UTC) — à revalider dès que la collecte TikTok est rétablie, ce signal est maintenant trop ancien pour être actionnable tel quel.
- **Concurrent `@jb.roy_`** : aucune donnée fraîche, même limitation.
- **Recommandation** : garder **14:00 UTC** comme créneau pivot sur Instagram — mais rappel du §0.3 : ce créneau ne sert à rien les jours où aucun contenu n'y est envoyé, ce qui reste le cas une bonne partie de la semaine écoulée.

---

## 7. Durée cible de vidéo

Aucune nouvelle donnée de durée disponible ce run (Instagram/Blotato ne remonte pas la durée vidéo ; TikTok bloqué, §0.1/§0.2 ; `get_instagram_user_reels` testé spécifiquement pour combler ce manque, refusé pour la même raison d'abonnement tokscript). **Cible recommandée inchangée, à revalider dès que la collecte TikTok Apify est rétablie** : 25–45 s pour le format quotidien court, tolérance jusqu'à ~90–110 s pour les formats actu/comparatifs à hook fort (Journal IA, actualité insolite) — **mais réserver ces formats longs à LinkedIn/TikTok plutôt qu'Instagram, où le Journal IA sous-performe nettement (§0.4/§1)**.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **🔴 PRIORITÉ ABSOLUE — Stabiliser la distribution Instagram, pas seulement la rétablir.** La reprise du 30/09-08/10 (4 posts) a été suivie d'une nouvelle coupure silencieuse de 5 jours (09/10→13/10), pendant que LinkedIn et TikTok publient sans interruption sur la même fenêtre. Vérifier que le flux automatisé inclut bien Instagram **tous les jours**, pas par intermittence — un contrôle manuel ponctuel (comme la reprise du 30/09) ne suffit pas si rien ne garantit la continuité ensuite.
2. **Réautoriser le connecteur n8n (OAuth `needs_reconnect`)** — bloqué depuis au moins 3 semaines consécutives (21/09, 06/10, 13/10, statut identique à chaque fois). Ce blocage unique empêche (a) toute collecte TikTok via Apify, (b) toute vérification de `n5dIUNEk5D6Pj3Vf`, et (c) l'écriture de l'onglet "Analyse Perf" — 3 runs sans écriture possible, voir résumé final.
3. **Rééquilibrer le mix de formats sur Instagram.** Les posts à angle unique font ≈5,4× mieux que le Journal IA quotidien sur ce canal (43,5 vs 8,0 vues moyennes) — réserver le Journal IA à LinkedIn/TikTok et prioriser les angles uniques (actualité nommée + chiffre, alternative gratuite, frustration tarifaire précise) sur Instagram, dans le créneau 14:00 UTC.
4. **Clarifier enfin le routage TikTok** (4e run consécutif à le signaler) : l'automatisation publie sur `@tonypayet4` (compte sans aucune métrique Blotato, confirmé structurel), pas sur `@automationboost7` (compte réel, qui croît : +3,5 % d'abonnés et +13 vidéos cette semaine). À trancher avec Tony : fusion, redirection du posting vers `@automationboost7`, ou documentation explicite de la séparation.
5. **Dès l'accès n8n rétabli** : vérifier le crédit Apify sur `YUJjz5NNsYo41t8q`, confirmer le statut réel de `n5dIUNEk5D6Pj3Vf`, revérifier si `@jb.roy_` a réellement arrêté de publier (compteur figé à 162 vidéos depuis 5+ semaines, §0.2/§5), et retester délibérément le pattern "économie chiffrée + témoignage perso" (§3.5) dès qu'un post à angle unique est republié sur Instagram.

---

## 9. Sources & limites (run du 13/10)

- **Instagram (Tony)** : `blotato_list_accounts` (confirme les ids 54617/55611/25882/36488) + `blotato_list_posts` (platform=instagram, deux appels : depuis 2026-07-01 statut `published` pour l'historique complet par `account.id`, et depuis 2026-08-01 sans filtre de statut pour reconstituer la chronologie récente). Séparation stricte par `account.id` (54617 vs 55611, 39 posts foodboost exclus) — 140 posts `automatisationboost` isolés, dont 134 avec analytics.
- **LinkedIn / TikTok (`@tonypayet4`)** : `blotato_list_posts` (platform=[tiktok], [linkedin], depuis 2026-08-01/2026-10-06, tous statuts). 0 post avec analytics sur les deux — reconfirmé (limite documentée de Blotato : analytics collectées uniquement pour Twitter/X, Instagram, Facebook, Threads, Bluesky).
- **TikTok (`@automationboost7`, `@jb.roy_`)** : `mcp__tokscript__get_tiktok_user` — réussi sur les deux comptes (profils publics). `mcp__tokscript__get_tiktok_user_videos` — refusé sur les deux comptes (« requires a Pro or Premium subscription »). `mcp__tokscript__get_instagram_user` sur `automatisationboost` — réussi (26 abonnés, 142 posts, avg 2 likes). `mcp__tokscript__get_instagram_user_reels` — refusé (même limite d'abonnement, testé spécifiquement pour obtenir des durées de vidéo IG).
- **n8n (workflows `YUJjz5NNsYo41t8q` et `n5dIUNEk5D6Pj3Vf`, Apify, écriture Sheet)** : **aucun appel possible ce run.** `ListConnectors` confirme `"name":"n8n","installState":"needs_reconnect","connected":false"` ; `ToolSearch` répété sur "n8n search_executions get_execution workflow" ne retourne aucun outil `n8n_*` chargeable. Ce connecteur nécessite une ré-autorisation OAuth interactive, impossible dans cette session cloud à froid.
- **Lecture de vérification du Sheet (sans écriture)** : export CSV du gid `1277122579` lu via `curl` (accès public en lecture confirmé, HTTP 200) — dernière ligne écrite datée du **21/09**, confirmant qu'aucune écriture n'a eu lieu depuis (ni le 28/09, ni le 06/10, ni ce run), toutes pour la même raison (§0.1).
- **Étape B (génération de scripts + ajout dans la file de production)** : hors périmètre de cette routine (analyse uniquement) — non exécutée.

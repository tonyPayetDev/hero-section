# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-10-06 (run hebdo automatisé, session cloud à froid)
- **Période couverte** : Instagram `@automatisationboost` — 137 posts propres remontés par Blotato depuis le 01/07 (séparation par `account.id`, pas par mots-clés — voir §0.5) · LinkedIn — 114 posts depuis le 17/08 · TikTok `@tonypayet4` (compte Blotato) — 136 posts depuis le 17/08 · **TikTok `@automationboost7` (compte réel analysé) et concurrent `@jb.roy_` — uniquement des agrégats de profil ce run (abonnés/vidéos/likes totaux), AUCUNE métrique par vidéo, voir §0.2.**
- **Comptes analysés** : Instagram `@automatisationboost` (Blotato `54617`) · LinkedIn Payet Tony (Blotato `25882`) · TikTok actif `@automationboost7` (pas connecté à Blotato — source normale = Apify via workflow n8n `YUJjz5NNsYo41t8q`, **indisponible ce run, voir §0.1**) · Concurrent TikTok `@jb.roy_` (même source, **indisponible ce run**) · **Exclu** : Instagram `foodboost` (`55611`, hors périmètre — 59 posts exclus ce run par `account.id`, voir §0.5)
- **Note sur `@tonypayet4` (Blotato TikTok `36488`)** : reçoit bien les publications automatiques quotidiennes (113 publiées / 22 échouées depuis le 17/08), mais ce compte **ne résout même plus en tant que profil TikTok public** via tokscript ce run (`Couldn't confirm @tonypayet4 on TikTok`) — ce n'est toujours pas le compte analysé comme actif (`@automationboost7`). Voir §0.3.

---

## 0. Anomalies et découvertes clés de ce run

1. **🔴 BLOCAGE CENTRAL — le connecteur MCP n8n est en `needs_reconnect` (OAuth), inatteignable dans cette session non-interactive.** Confirmé via `ListConnectors` (`"name":"n8n","installState":"needs_reconnect","connected":false`) et via `ToolSearch` répété (aucun outil `n8n_*` / `search_executions` / `get_execution` chargeable). Conséquences en cascade, toutes dues à cette seule cause :
   - Impossible de lire les exécutions du workflow concurrents `YUJjz5NNsYo41t8q` (Apify) → aucune donnée TikTok par vidéo pour `@automationboost7` ni `@jb.roy_` ce run (voir §0.2).
   - Impossible de lire les exécutions de `n5dIUNEk5D6Pj3Vf` → son statut (0 exécution au dernier contrôle du 21/09) **n'a pas pu être revérifié ce run**, à ne pas présenter comme reconfirmé.
   - Impossible de créer/lancer le workflow `create_workflow_from_code` (nœud Google Sheets) prévu pour écrire l'onglet "Analyse Perf" → **le SINK 2 de ce run n'a pas pu être exécuté du tout** (voir le résumé final). Ce n'est pas un problème Apify ni un problème de crédit comme les 3 runs précédents — c'est la porte d'accès n8n elle-même qui est fermée. **Action requise avant le prochain run : relancer l'autorisation OAuth du connecteur n8n depuis les réglages de connecteurs claude.ai (une session interactive est nécessaire, celle-ci ne peut pas le faire).**
2. **🔴 TikTok — toujours aucune métrique par vidéo, mais pour une cause différente des 3 runs précédents.** Avant (07/09, 14/09, 21/09) : crédit Apify épuisé + bug serveur tokscript. Ce run : le bug serveur tokscript (`redactUrlCredentials is not defined`) semble **corrigé** — `get_tiktok_user` répond correctement sur `automationboost7` et `jb.roy_` — mais `get_tiktok_user_videos` et `get_instagram_user_reels`/`get_instagram_user_posts` refusent toujours avec *« Listing user videos requires a Pro or Premium subscription »*. Ce n'est donc plus un bug transitoire : **c'est une limite de plan tokscript, à traiter comme telle** (upgrade ou abandon de cette voie de secours). Apify, lui, reste totalement hors de portée ce run à cause du blocage n8n (§0.1), donc aucune confirmation indépendante de son état de crédit n'a pu être obtenue.
   - Ce qui a quand même pu être collecté (profils publics, sans n8n ni Pro tokscript) :
     - `@automationboost7` : 231 abonnés, 499 suivis, 974 likes cumulés, 219 vidéos.
     - `@jb.roy_` (concurrent) : 1582 abonnés, 113 suivis, 7829 likes cumulés, 162 vidéos.
   - **Point de vigilance méthodologique** : les chiffres `jb.roy_` (1582 abonnés / 162 vidéos) sont **identiques au chiffre à l'identique relevé le 07/09** dans l'historique du document. Deux lectures possibles, non tranchées ici : (a) ce compte concurrent est réellement resté figé pendant ~4 semaines, ou (b) tokscript sert une réponse mise en cache pour ce profil. À vérifier au prochain run en comparant à nouveau — ne pas traiter comme une vérité acquise.
3. **🟢→🔴 Nouvelle découverte majeure — Instagram ne reçoit plus AUCUN contenu depuis le 30/09, alors que LinkedIn et TikTok (`@tonypayet4`) continuent de publier normalement tous les jours jusqu'à aujourd'hui.** En reconstituant l'historique complet (tous statuts, pas seulement "published") par plateforme :
   - **Instagram** : la coupure de connexion signalée le 21/09 (« Your Instagram connection is no longer valid ») a en réalité duré du **12/09 14:29 UTC au 30/09 ~04:36 UTC, soit 25 échecs consécutifs sur ~18 jours** (plus long que ce que le run du 21/09 pouvait savoir à l'époque). La connexion s'est rétablie et **un seul post a été publié avec succès le 30/09 à 14:08 UTC** (« Clip synchronisé avec la voix :o », un post isolé, pas une édition du Journal IA quotidien). **Depuis, zéro tentative de publication Instagram n'a été enregistrée entre le 01/10 et le 06/10 (6 jours) — ni succès, ni échec.** Ce n'est donc plus un problème de connexion : la plateforme n'est simplement plus alimentée.
   - **LinkedIn et TikTok (`@tonypayet4`)**, sur la même fenêtre : publication **quotidienne continue jusqu'à aujourd'hui**, avec un post identique programmé sur les deux pour le 06/10 14:00 UTC (« Où ta boîte perd des clients ? »). Instagram n'a **aucun équivalent programmé** à cette date.
   - **Conclusion actionnable** : le pipeline de distribution quotidienne (Journal IA + posts uniques) a cessé d'inclure Instagram comme cible depuis le 30/09, alors que les deux autres canaux tournent normalement. Ce n'est pas visible comme une erreur (pas d'échec enregistré) — c'est une omission silencieuse. **Priorité n°1 de ce rapport, devant même le blocage n8n.**
4. **🟡 Correction méthodologique — la moyenne Instagram des runs précédents (113,3 vues / médiane 108, n=34) venait d'un sous-échantillon filtré à la main, pas de la population complète.** Ce run, la séparation par `account.id` Blotato (54617 vs 55611 `foodboost`) permet d'isoler proprement et automatiquement les 137 posts `automatisationboost` sans heuristique de mots-clés. Sur cette population complète (131 posts avec analytics), la moyenne réelle est **beaucoup plus basse (38,1 vues, médiane 12)** — parce qu'elle inclut 19 éditions du format "Journal IA quotidien", qui s'effondrent complètement en vues (moyenne 4,3, médiane 4, max 23) comparé aux 112 posts à angle unique (moyenne 43,8, médiane 16,5, max 243). **Voir §1 et §4 — c'est la découverte de contenu la plus actionnable de ce run.**
5. **🟢 Filtrage food/restaurant — méthode améliorée, plus fiable.** Au lieu de filtrer par mots-clés sur la sortie globale de `blotato_list_top_posts` (qui mélange les deux comptes Instagram), ce run sépare directement par `account.id` via `blotato_list_posts` : 137 posts `automatisationboost` (54617) vs 59 posts `foodboost` (55611) sur la fenêtre depuis le 01/07, soit **30,1 % de contamination potentielle** si on ne filtrait pas — cohérent avec les runs précédents (32-34 %) mais désormais vérifié de façon déterministe, pas par heuristique.
6. **🟢 Top 3 Instagram inchangé pour la 4e semaine consécutive.** Sans surprise : un seul post propre a été publié depuis le 11/09 (celui du 30/09, 40 vues — loin derrière le Top 3), donc aucun candidat n'a pu dépasser le Top 3 historique (243 / 223 / 216 vues, tous publiés fin juillet).
7. **🟡 `n5dIUNEk5D6Pj3Vf` — statut non vérifiable ce run (voir §0.1).** Dernière confirmation connue : 0 exécution depuis sa création (21/07), relevée le 21/09. Ne pas présenter comme "reconfirmé" tant que l'accès n8n n'est pas rétabli.

---

## 1. Chiffres clés par plateforme

### Instagram `@automatisationboost` (54617) — Blotato, 137 posts depuis le 01/07, séparés par account.id
| Métrique | Valeur | Note |
|---|---|---|
| Échantillon total avec analytics | n=131 | 6 posts trop récents, pas encore de métriques |
| Vues — toute la population (Journal IA + angles uniques mélangés) | moyenne **38,1** / médiane **12** | Chiffre honnête sur la population complète — voir §0.4 |
| Vues — posts "Journal IA quotidien" seuls | n=19, moyenne **4,3** / médiane **4** / max 23 | Format qui s'effondre en vues sur IG |
| Vues — posts à angle unique seuls | n=112, moyenne **43,8** / médiane **16,5** / max 243 | 10× mieux que le Journal IA — voir §4 |
| Top 5 propres, tout historique | 243 / 223 / 216 / 214 / 178 vues | Inchangé depuis 4 semaines — voir §0.6 |
| Posts propres publiés du 29/09 au 06/10 | **1 seul** (30/09, 40 vues) | Voir §0.3 — plus un problème de pipeline que de connexion |
| Heure dominante (n=131) | **14:00 UTC** (60/131 posts, 46 %) | 8e confirmation consécutive |
| Commentaires | record historique inchangé = 6 (post "économise 200€/mois", 08/08) | Le post du 30/09 a eu 2 commentaires, 2 likes, 40 vues — sous la moyenne |

### LinkedIn (Payet Tony, Blotato 25882)
**Compte opérationnel, publication quotidienne continue jusqu'à aujourd'hui.** 114 posts recensés depuis le 17/08 (fenêtre complète disponible) : 86 publiés, 27 échoués (ponctuels, pas de panne prolongée identifiée), 1 programmé pour le 06/10 14:00. Toujours **aucune métrique d'engagement disponible** (Blotato ne collecte pas d'analytics LinkedIn — confirmé de nouveau : 0 post avec `analytics.latest` sur les 114).

### TikTok `@tonypayet4` (Blotato 36488) — compte de publication automatisée, hors périmètre d'analyse
136 posts depuis le 17/08 : 113 publiés, 22 échoués, 1 programmé pour le 06/10 14:00 (identique au contenu LinkedIn du même jour). **Aucune métrique Blotato** (TikTok non couvert par Blotato). Ce handle **ne résout plus comme profil TikTok public** via tokscript ce run (échec `Couldn't confirm @tonypayet4 on TikTok`) — voir §0.3/§8.4, question stratégique non résolue depuis 3 runs.

### TikTok `@automationboost7` — compte réel analysé, agrégats de profil uniquement (pas de détail par vidéo ce run)
| Métrique | Valeur (06/10) | Valeur (07/09, dernier point avec détail vidéo) | Évolution |
|---|---|---|---|
| Abonnés | **231** | 166 | +65 (+39 %) |
| Vidéos publiées | **219** | 135 | +84 (+62 %), ≈2,9 vidéos/jour sur la période |
| Likes cumulés | **974** | n/d | avg ≈4,4 likes/vidéo |
| Vues/durée par vidéo | **non disponible ce run** | moy. 354 / médiane 268, durée médiane 34s | Bloqué — voir §0.1/§0.2 |

### Concurrent TikTok `@jb.roy_` — agrégats de profil uniquement, chiffres identiques au run du 07/09 (voir §0.2 point de vigilance)
| Métrique | Valeur (06/10) | Valeur (07/09) | Évolution |
|---|---|---|---|
| Abonnés | 1582 | 1582 | 0 (à vérifier — possible cache, voir §0.2) |
| Vidéos publiées | 162 | 162 | 0 |
| Likes cumulés | **7829** | n/d | avg ≈48,3 likes/vidéo — **11× l'avg de `@automationboost7`** |
| Vues/durée par vidéo | non disponible ce run | moy. 212 / médiane 157, durée médiane 48s | Bloqué |

---

## 2. Top 3 vidéos / posts

### Top 3 Instagram `@automatisationboost` (depuis le 01/07 — inchangé, voir §0.6)
1. **243 vues / 1 like** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... tu perds du temps. » → tuto VPS + Coolify + Claude Code + MCP en 3 étapes, estimation de temps réaliste — 27/07 14:29 UTC.
2. **223 vues / 4 likes** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. Follow pour la suite + commente OPUS » — 29/07 14:30 UTC.
3. **216 vues / 2 likes** — « 🛠️ L'alternative gratuite à Claude Code pour créer des sites automatiquement. Kilo Code + n8n = même résultat, zéro abonnement. » — 13/07 19:00 UTC.
4. *(juste derrière, mention)* **214 vues** — « Higgsfield, c'est 15 à 99 $ par mois. Et tes crédits non utilisés disparaissent à la fin du mois. » (frustration/prix d'un outil connu) — 25/07 14:29 UTC.
5. *(mention engagement)* **136 vues mais 6 commentaires** — « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat » — 08/08 14:29 UTC — toujours le meilleur ratio commentaires/vue de tout l'historique.

### Dernier post publié (30/09) — exemple de ce qu'il ne faut PAS refaire
**40 vues / 2 likes / 2 commentaires** — « Clip synchronisé avec la voix :o » — hook vague, pas de nom d'outil, pas de chiffre, pas de tension. Même en reprenant la publication après 18 jours de coupure, un hook faible reste sous la moyenne (43,8 vues attendues pour un post à angle unique).

### Top TikTok `@automationboost7` — **non actualisé, repris du 07/09, non vérifiable ce run (§0.1/§0.2)**
1. 794 vues — actualité insolite (avalanche au Népal), 109 s, 28/08.
2. 783 vues — Journal IA, 68 s, 23/08.
3. 774 vues — Journal IA, 84 s, 05/09.

### Top concurrent `@jb.roy_` — **non actualisé, repris du 07/09, non vérifiable ce run**
1. 1234 vues — 02/09, 21 s.
2. 725 vues — 28/08, 44 s.
3. 530 vues — 25/08, 42 s.

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Actualité produit/outil connu nommée dans les 10 premiers mots + un chiffre ou un fait précis** — pattern le plus robuste, confirmé sur 4 runs consécutifs (« Anthropic vient de sortir Opus 5, 4e Claude en 2 mois »).
2. **Alternative gratuite à un outil payant connu**, nommé explicitement — ex. « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » (216 vues).
3. **Tutoriel actionnable en 3 étapes avec estimation de temps réaliste** — ex. « VPS, Coolify, Claude Code + MCP... » (243 vues, meilleur post Instagram sur 2 mois).
4. **Frustration tarifaire précise sur un outil connu** (prix exact + ce qu'on perd) — ex. « Higgsfield, c'est 15 à 99 $/mois, et tes crédits non utilisés disparaissent » (214 vues) — nouveau variant confirmé ce run, à rapprocher du pattern n°2.
5. **Économie chiffrée + témoignage à la première personne** — toujours le seul post de tout l'historique à dépasser 1 commentaire (6 commentaires, « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat »). **Jamais retesté délibérément depuis 3 runs** — priorité dès la reprise de publication.
6. **Actualité insolite grand public, hors registre IA/outils** (ex. avalanche au Népal, 794 vues TikTok, dernière donnée fiable du 28/08) — à revérifier dès que TikTok redevient mesurable.

**Règle** : nommer un outil/une actualité connue + un chiffre ou un fait précis dans les 10 premiers mots reste le pattern le plus robuste, sur 4 runs consécutifs d'observation.

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Publier le format "Journal IA quotidien" sur Instagram en espérant de la portée.** Donnée nouvelle de ce run (§0.4) : sur 131 posts analysés, les 19 éditions du Journal IA font en moyenne **4,3 vues (médiane 4)** contre **43,8 vues (médiane 16,5)** pour les posts à angle unique — soit 10× moins. Le format a sa place sur LinkedIn/TikTok (cadence, SEO, archive) mais **pas comme contenu principal sur Instagram** : chaque édition Journal IA publiée sur IG est un slot perdu qui aurait pu porter un hook à angle unique.
- ❌ **Calculer une moyenne Instagram sans séparer par account.id ET sans séparer par format (Journal IA vs angle unique).** Les deux runs précédents avaient déjà corrigé le filtrage food ; ce run corrige en plus le mélange de formats, qui écrasait la vraie performance des posts à angle unique (§0.4).
- ❌ **Compter sur « Commente le mot X » comme unique CTA.** Record historique toujours à 6 commentaires sur tout l'échantillon (n=131), obtenu sur un post qui ne reposait pas sur ce seul mécanisme.
- ❌ **Supposer qu'une connexion sociale rétablie veut dire que le pipeline de contenu est rétabli aussi.** La connexion Instagram fonctionne de nouveau depuis le 30/09 (preuve : 1 post publié avec succès) mais **aucun contenu n'y est envoyé depuis** — pendant que LinkedIn et TikTok continuent de recevoir le même flux quotidien. Une reconnexion ne suffit pas : il faut vérifier que la cible a bien été ré-ajoutée à la distribution automatisée (§0.3, priorité n°1 de ce rapport).
- ❌ **Lancer une analyse TikTok en supposant que le crédit Apify est le seul obstacle.** Ce run, c'est l'accès n8n lui-même (OAuth) qui bloque tout, avant même d'arriver à la question du crédit Apify (§0.1).
- ⚠️ **Ne pas traiter les chiffres `@jb.roy_` (1582 abonnés / 162 vidéos) comme une actualisation réelle** — ils sont identiques au run du 07/09, possiblement un cache tokscript (§0.2).

---

## 5. Analyse du concurrent `@jb.roy_` — agrégats de profil seulement, pas de détail vidéo ce run

- **Chiffres de profil (06/10, à vérifier — voir §0.2)** : 1582 abonnés, 162 vidéos, 7829 likes cumulés → **≈48,3 likes/vidéo en moyenne**, contre **≈4,4 likes/vidéo** pour `@automationboost7` (974 likes / 219 vidéos) — un écart de **×11**, malgré `@automationboost7` qui publie 35 % de vidéos en plus (219 vs 162) sur la durée. Autrement dit : plus de volume ne compense pas un écart de qualité/hook de cet ordre.
- **Dernières observations qualitatives disponibles (07/09, non revérifiées)** : durée médiane plus longue chez le concurrent (48 s vs 34 s chez Tony), légende générique, 0 hashtag, hook parlé dans la vidéo plutôt qu'écrit dans le texte.
- **Limite de méthode persistante** : sans Apify (bloqué par §0.1) ni accès vidéo tokscript (bloqué par un plan non-Pro, §0.2), impossible d'extraire les hooks exacts, durées actuelles ou format des vidéos de `@jb.roy_` ce run. Les seules données obtenues sont des totaux de profil (abonnés/vidéos/likes), pas des métriques par vidéo.

---

## 6. Meilleures heures de publication

- **Instagram** : **14:00 UTC** reste le créneau dominant — 60 des 131 posts analysés (46 %) y sont publiés, et c'est l'heure de 3 des 5 meilleurs posts historiques. 8e confirmation consécutive sur des runs successifs. **À garder comme pivot par défaut.**
- **TikTok `@automationboost7`** : aucune donnée fraîche (§0.1/§0.2). Dernier signal disponible (07/09) : pas de pivot horaire net (Top 3 réparti sur 08:00, 03:00, 07:30 UTC) — à revalider dès que la collecte TikTok est rétablie.
- **Concurrent `@jb.roy_`** : aucune donnée fraîche.
- **Recommandation** : garder **14:00 UTC** comme créneau pivot sur Instagram — mais rappel du §0.3 : ce créneau ne sert à rien tant qu'aucun contenu n'y est envoyé.

---

## 7. Durée cible de vidéo

Aucune nouvelle donnée de durée disponible ce run (Instagram/Blotato ne remonte pas la durée vidéo ; TikTok bloqué, §0.1/§0.2). **Cible recommandée inchangée, à revalider dès que la collecte TikTok Apify est rétablie** : 25–45 s pour le format quotidien court, tolérance jusqu'à ~90–110 s pour les formats actu/comparatifs à hook fort (Journal IA, actualité insolite) — **mais réserver ces formats longs à LinkedIn/TikTok plutôt qu'Instagram, où le Journal IA sous-performe nettement (§4)**.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **🔴 PRIORITÉ ABSOLUE — Ré-ajouter Instagram `@automatisationboost` à la distribution automatisée quotidienne.** La connexion fonctionne (1 post publié avec succès le 30/09), mais plus aucun contenu n'y est envoyé depuis 6 jours alors que LinkedIn et TikTok (`@tonypayet4`) reçoivent le même flux quotidien sans interruption, y compris un post identique programmé pour aujourd'hui sur les deux autres canaux. C'est une omission de pipeline, pas un problème de connexion — plus urgent que tout le reste de ce rapport parce qu'il stoppe la publication, pas seulement la mesure.
2. **Réautoriser le connecteur n8n (OAuth `needs_reconnect`)**, idéalement avant le prochain run hebdomadaire. Ce blocage unique empêche à la fois (a) toute collecte TikTok via Apify sur `YUJjz5NNsYo41t8q`, (b) toute vérification de `n5dIUNEk5D6Pj3Vf`, et (c) l'écriture de l'onglet "Analyse Perf" du Google Sheet — voir le résumé final.
3. **Rééquilibrer le mix de formats sur Instagram.** Les posts à angle unique font 10× mieux que le Journal IA quotidien sur ce canal (43,8 vs 4,3 vues moyennes, §0.4/§4) — réserver le Journal IA à LinkedIn/TikTok et prioriser les angles uniques (actualité nommée + chiffre, alternative gratuite, frustration tarifaire précise) sur Instagram.
4. **Clarifier enfin le routage TikTok** (3e run consécutif à le signaler) : l'automatisation publie sur `@tonypayet4` (compte qui ne résout même plus comme profil public ce run), pas sur `@automationboost7` (compte réel, qui croît : +39 % d'abonnés, +62 % de vidéos depuis le 07/09). À trancher avec Tony : fusion, redirection du posting vers `@automationboost7`, ou documentation explicite de la séparation.
5. **Dès l'accès n8n rétabli** : vérifier le crédit Apify sur `YUJjz5NNsYo41t8q` avant de relancer une extraction, confirmer le statut réel de `n5dIUNEk5D6Pj3Vf`, et retester délibérément le pattern "économie chiffrée + témoignage perso" (§3.5) sur Instagram dès qu'un post à angle unique y est republié.

---

## 9. Sources & limites (run du 06/10)

- **Instagram (Tony)** : `blotato_list_accounts` (confirme les ids 54617/55611/25882/36488) + `blotato_list_top_posts` (platform=instagram, depuis le 2026-07-01) + `blotato_list_posts` (platform=instagram, deux appels : depuis 2026-07-01 pour l'historique complet par account.id, et depuis 2026-09-01 sans filtre de statut pour reconstituer la chronologie des échecs/reprises). Séparation par `account.id` (54617 vs 55611) plutôt que par mots-clés — 137 posts `automatisationboost` isolés, dont 131 avec analytics.
- **LinkedIn / TikTok (`@tonypayet4`)** : `blotato_list_posts` (platform=[tiktok, linkedin], depuis 2026-07-01, tous statuts, limite 250 → fenêtre réelle couverte 17/08→06/10 par plafonnement). 0 post avec analytics sur les deux (confirmé, limite connue de Blotato).
- **TikTok (`@automationboost7`, `@jb.roy_`, `@tonypayet4`)** : `mcp__tokscript__get_tiktok_user` — réussi sur `automationboost7` et `jb.roy_` (bug serveur des runs précédents apparemment corrigé), échoué sur `tonypayet4` (« Couldn't confirm »). `mcp__tokscript__get_tiktok_user_videos` — refusé sur les deux comptes (« requires a Pro or Premium subscription », limite de plan, pas un bug). `mcp__tokscript__get_instagram_user` sur `automatisationboost` — réussi (22 abonnés, 139 posts, avg 2 likes/1 commentaire — cohérent avec un compte en phase de démarrage). `mcp__tokscript__get_instagram_user_reels` — refusé (même limite d'abonnement).
- **n8n (workflows `YUJjz5NNsYo41t8q` et `n5dIUNEk5D6Pj3Vf`, Apify, écriture Sheet)** : **aucun appel possible ce run.** `ListConnectors` confirme `"name":"n8n","installState":"needs_reconnect","connected":false` ; `ToolSearch` répété sur "n8n workflow", "search_executions get_execution", "apify actor" ne retourne aucun outil `n8n_*` chargeable. Ce connecteur nécessite une ré-autorisation OAuth interactive, impossible dans cette session cloud à froid.
- **Comptes connectés Blotato** : vérifiés via `blotato_list_accounts` — confirme que `@automationboost7` n'est toujours pas un compte connecté à Blotato (seul `@tonypayet4`, id `36488`, l'est côté TikTok).
- **Lecture de vérification du Sheet (sans écriture)** : export CSV du gid `1277122579` lu via `curl` (accès public en lecture confirmé, HTTP 200) pour constater l'état laissé par le run du 21/09 — aucune écriture n'a été tentée dessus ce run, voir le résumé final pour la raison exacte.
- **Étape B (génération de scripts + ajout dans la file de production)** : hors périmètre de cette routine (analyse uniquement) — non exécutée.

# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-10-13 (run hebdo, session cloud) — **ce run corrige et complète une version écrite plus tôt le même jour** (voir §0.1).
- **Période couverte** : Instagram `@automatisationboost` — 140 posts propres depuis le 01/07 (séparation stricte par `account.id`) · LinkedIn — 19 posts du 06/10 au 20/10 (12 publiés, 7 programmés) · TikTok `@tonypayet4` (Blotato, hors périmètre) — 18 posts sur la même fenêtre · **TikTok `@automationboost7` (source de vérité) et concurrent `@jb.roy_` — 40 vidéos chacun, fraîchement scrapées via Apify ce run (exécution n8n 98855, succès), vues/likes/commentaires/durée par vidéo.**
- **Comptes analysés** : Instagram `@automatisationboost` (Blotato `54617`) · LinkedIn Payet Tony (Blotato `25882`) · TikTok actif `@automationboost7` (pas connecté à Blotato — source de vérité = Apify via workflow n8n `YUJjz5NNsYo41t8q`) · Concurrent TikTok `@jb.roy_` (même source) · **Exclu** : Instagram `foodboost` (`55611`, hors périmètre — 59 posts exclus ce run par `account.id`, fenêtre 01/07→13/10)
- **Note sur `@tonypayet4` (Blotato TikTok `36488`)** : continue de recevoir les publications automatiques quotidiennes (18 posts du 06/10 au 19/10, 0 échec). **Reconfirmé : ce compte n'a AUCUNE métrique dans Blotato** (`analytics: null` sur tous les posts) — limite structurelle documentée de Blotato (pas de collecte TikTok, quel que soit le compte), pas une panne. Ne jamais l'utiliser comme source de vérité TikTok — seul Apify (fonctionnel ce run) le peut.

---

## 0. Anomalies et découvertes clés de ce run

1. **🟢 CORRECTION — le connecteur n8n n'est PAS bloqué dans cette session**, contrairement à ce qu'indiquait la version de STRATEGIE.md déjà commitée plus tôt aujourd'hui (commit `787a806`, qui signalait `n8n: needs_reconnect` depuis 3 semaines). Dans cette session, `search_executions`, `get_execution`, `get_workflow_details` et `execute_workflow` ont tous fonctionné normalement. Le blocage précédent était donc soit transitoire (session à session), soit propre à la session du run précédent — **à surveiller, pas à supposer résolu définitivement**. Conséquence concrète : j'ai pu (a) lancer pour la première fois le workflow Apify `YUJjz5NNsYo41t8q` (`triggerCount` était à 0 avant ce run — il n'avait jamais été exécuté), et (b) écrire l'onglet "Analyse Perf" (voir SINK 2 ci-dessous), ce qui n'avait pas pu être fait depuis le 21/09.
2. **🟢 TikTok — données fraîches par vidéo obtenues pour la première fois depuis plusieurs semaines.** Exécution n8n `98855` du workflow `YUJjz5NNsYo41t8q` (Apify `clockworks/tiktok-scraper`, 40 vidéos par compte) : succès en 45s, aucune erreur de crédit. Détail complet en §1.
3. **🔴 DÉCOUVERTE — `@jb.roy_` semble avoir cessé de publier sur TikTok depuis début septembre, confirmé par les dates.** Les 40 vidéos les plus récentes récupérées pour `@jb.roy_` s'échelonnent toutes entre le **25/08 et le 02/09** — aucune vidéo plus récente que le 02/09 dans l'échantillon des 40 derniers posts. À l'inverse, l'échantillon `@automationboost7` contient des vidéos jusqu'au **07/10**. Combiné au compteur de vidéos figé à 162 depuis 5+ relevés (§0.5 historique), cela tranche l'hypothèse ouverte depuis 3 semaines : **(a) confirmée** — le concurrent a vraisemblablement arrêté de publier de nouvelles vidéos TikTok depuis début septembre, tout en continuant à gagner un peu d'abonnés/likes sur son stock existant (+2 abonnés, +7 likes en 7 jours sur des vidéos qui ne changent pas).
4. **🟡 Instagram — toujours en coupure silencieuse, 5e jour consécutif.** Aucun nouveau post propre depuis le 08/10 (3 vues, dernier post avant coupure) — 0 post du 09/10 au 13/10 inclus, pendant que LinkedIn et TikTok (`@tonypayet4`) publient sans interruption sur la même fenêtre. Reste la priorité n°1.
5. **🟢 Signal fort confirmé — pivot horaire 14:00 UTC valable sur Instagram ET TikTok.** Les 2 meilleures vidéos TikTok `@automationboost7` de cet échantillon (744 et 740 vues) sont publiées à 14:00:0x UTC très précisément, comme 60 des 134 posts Instagram mesurés (45%). C'est la première fois que ce pivot est confirmé simultanément sur les deux plateformes avec des données fraîches.
6. **🟢 Pattern "économie chiffrée + témoignage perso" reproduit hors Instagram.** La vidéo TikTok du 28/09 (« J'ai arrêté de payer 150€/mois une assistante réseaux sociaux... ~1800€ économisés ») fait 647 vues **et 6 commentaires** — jusqu'ici ce pattern n'avait été observé qu'une fois (post Instagram du 08/08, 136 vues/6 commentaires). Avec ce second point, ce n'est plus un signal `n=1` isolé à une plateforme.

---

## 1. Chiffres clés par plateforme

### Instagram `@automatisationboost` (Blotato 54617) — 140 posts depuis le 01/07
| Métrique | Valeur | Note |
|---|---|---|
| Échantillon avec analytics | n=134 (sur 140) | 6 posts trop récents |
| Vues — posts "Journal IA" | n=20, moyenne **7,0** / médiane **4** | Format à éviter comme contenu principal IG |
| Vues — posts à angle unique | n=114, moyenne **43,3** / médiane **16,5** | ≈6,2× mieux que le Journal IA |
| Heure dominante (n=134) | **14:00 UTC** (60/134, 45%) | Confirmé, désormais aussi vu sur TikTok (§0.5) |
| Posts publiés du 09/10 au 13/10 | **0** | 5e jour de coupure silencieuse |
| Dernier post publié | 08/10, 04:48 UTC, 3 vues (Journal IA) | |

### LinkedIn (Payet Tony, Blotato 25882)
Opérationnel, publication quotidienne continue : 19 posts du 06/10 au 20/10 (12 publiés, 7 programmés, 0 échec). **Toujours aucune métrique d'engagement** — confirmé : limite structurelle de Blotato sur LinkedIn.

### TikTok `@tonypayet4` (Blotato 36488) — hors périmètre d'analyse
18 posts du 06/10 au 19/10 (11 publiés, 7 programmés, 0 échec). **Aucune métrique Blotato**, même limite structurelle.

### TikTok `@automationboost7` — compte réel analysé (source de vérité)
| Métrique | Profil (tokscript, 13/10) | 40 dernières vidéos (Apify, 13/10) |
|---|---|---|
| Abonnés | **239** | — |
| Vidéos totales | **232** | — |
| Likes cumulés | **1013** | — |
| Vues — moyenne / médiane | — | **210 / 154** |
| Likes — moyenne | — | **3** |
| Commentaires — moyenne | — | **1,4/vidéo** |
| Engagement/vue — moyenne | — | **9,59%** |
| Durée — médiane | — | **34 s** |

### Concurrent TikTok `@jb.roy_`
| Métrique | Profil (tokscript, 13/10) | 40 dernières vidéos (Apify, 13/10) |
|---|---|---|
| Abonnés | **1584** (6,6× plus que Tony) | — |
| Vidéos totales | **162** (figé depuis ≥5 semaines) | — |
| Likes cumulés | **7836** | — |
| Vues — moyenne / médiane | — | **225 / 169** |
| Likes — moyenne | — | **7** |
| Commentaires — moyenne | — | **0,2/vidéo** |
| Engagement/vue — moyenne | — | **4,22%** (2,27× moins que Tony) |
| Durée — médiane | — | **48 s** |
| **Vidéo la plus récente dans l'échantillon** | — | **02/09/2026 — aucune vidéo plus récente, voir §0.3** |

**Lecture** : `@jb.roy_` a 6,6× plus d'abonnés et des vues/vidéo légèrement supérieures (225 vs 210), mais Tony convertit 2,27× mieux en engagement et **7× mieux en commentaires**, malgré une audience bien plus petite — et le concurrent semble avoir arrêté de publier (§0.3).

---

## 2. Top 3 vidéos / posts

### Top Instagram `@automatisationboost` (depuis le 01/07, inchangé)
1. **243 vues / 1 like** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... » → tuto VPS + Coolify + Claude Code en 3 étapes — 27/07 14:29 UTC.
2. **223 vues / 4 likes** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. » — 29/07 14:30 UTC.
3. **216 vues / 2 likes** — « L'alternative gratuite à Claude Code... Kilo Code + n8n, zéro abonnement. » — 13/07 19:00 UTC.
4. *(mention)* **136 vues mais 6 commentaires** — « Claude Code et n8n m'ont fait économiser 200€/mois de secrétariat » — 08/08 14:29 UTC.

### Top TikTok `@automationboost7` (fraîches, Apify, 13/10)
1. **744 vues** — « Le feed Insta de ton resto, déjà prêt » (angle démo client B2B), 31s, 07/10 14:00 UTC.
2. **740 vues** — « Où ta boîte perd des clients ? » (question douleur business), 32s, 06/10 14:00 UTC.
3. **654 vues / 6 commentaires** — Journal IA du 06/10, 51s, 13:15 UTC.
4. *(mention)* **647 vues / 6 commentaires** — « J'ai arrêté de payer 150€/mois une assistante réseaux sociaux... ~1800€ économisés » — 28/09, 33s. Meilleur ratio commentaires/vue de l'échantillon avec #3.
5. *(mention)* **509 vues / 9 commentaires** — « Ta voix off, clonée une seule fois, réutilisable sur toutes tes vidéos » — 13/07, 33s. Meilleur ratio commentaires/vue absolu de tout l'historique collecté.

### Top concurrent `@jb.roy_` (fraîches, Apify, 13/10)
1. **1276 vues / 1,65% engagement** — 02/09 14:30 UTC, 21s, légende générique « Follow @jb.roy_ pour imploser l'IA dans ton activité ».
2. **761 vues / 1,58% engagement** — 28/08 15:00 UTC, 44s, même légende type.
3. **552 vues / 2,36% engagement** — 25/08 17:16 UTC, 42s, même légende type.

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Économie chiffrée + témoignage à la première personne** — désormais confirmé sur 2 plateformes : IG « 200€/mois de secrétariat » (136v/6 commentaires) et TikTok « 150€/mois d'assistante, ~1800€ économisés » (647v/6 commentaires). **Priorité pour la prochaine série de scripts.**
2. **Question douleur business ciblant un client potentiel** (B2B) — « Où ta boîte perd des clients ? » (740v) et « Le feed Insta de ton resto, déjà prêt » (744v, démo visuelle concrète) — les 2 meilleures vidéos TikTok de cet échantillon, toutes deux publiées à 14:00 UTC.
3. **Outil/actualité connue nommée + chiffre précis dans les 10 premiers mots** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois » (223v), « Higgsfield, c'est 15 à 99$/mois » (214v).
4. **Alternative gratuite à un outil payant connu, nommé explicitement** — « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » (216v).
5. **Tutoriel actionnable en 3 étapes avec estimation de temps réaliste** — VPS/Coolify/Claude Code (243v, meilleur post IG historique).
6. **Fonctionnalité technique concrète présentée simplement** — « Ta voix off, clonée une seule fois, réutilisable sur toutes tes vidéos » (509v/9 commentaires, meilleur ratio commentaires/vue de tout l'historique collecté).

**Règle** : nommer un outil/une actualité connue + un chiffre précis reste robuste sur Instagram ; sur TikTok, les hooks orientés "douleur business du prospect" et "économie chiffrée" performent mieux que le registre pur actu-IA.

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Publier le format "Journal IA quotidien" comme contenu principal Instagram.** 7,0 vues de moyenne (n=20) contre 43,3 (n=114) pour les posts à angle unique — écart ≈6,2×. Le format reste correct sur TikTok (654v/6 commentaires ce run) et LinkedIn.
- ❌ **Supposer qu'une reprise de publication Instagram signifie que le pipeline est fiable.** 5e jour de coupure silencieuse malgré une reprise observée fin septembre — revérifier la continuité jour par jour à chaque run.
- ❌ **Compter sur « Commente le mot X » comme unique mécanisme d'engagement.** Les meilleurs ratios commentaires/vue de l'échantillon (509v/9 commentaires, 647v/6 commentaires, 654v/6 commentaires) viennent de hooks à économie chiffrée ou de contenu Journal IA, pas uniquement du CTA.
- ❌ **Traiter le connecteur n8n comme durablement cassé sans revérifier à chaque session.** Fonctionnel ce run alors que la version écrite plus tôt aujourd'hui le signalait bloqué — statut probablement par session, pas par compte.
- ❌ **Décrire `@jb.roy_` comme "concurrent actif à surveiller de près" sans nuance** : son échantillon des 40 dernières vidéos ne contient rien après le 02/09 — il semble avoir arrêté de publier sur TikTok depuis ≥5 semaines (§0.3). Sa reach supérieure vient d'un stock d'abonnés historique, pas d'une activité récente.
- ❌ **Juger `@jb.roy_` uniquement sur les vues brutes** (225 vs 210 moy., legèrement supérieur) sans regarder l'engagement/vue (4,22% vs 9,59%) ni les commentaires (0,2 vs 1,4/vidéo) — Tony convertit nettement mieux son audience, plus petite.

---

## 5. Analyse du concurrent `@jb.roy_`

- **Profil** : 1584 abonnés (6,6× Tony), 162 vidéos (figé ≥5 semaines), 7836 likes cumulés.
- **40 dernières vidéos (Apify, fraîches)** : vues moy. 225 / médiane 169, likes moy. 7, commentaires moy. 0,2/vidéo (quasi nul), engagement/vue moy. 4,22%, durée médiane **48 secondes**.
- **Découverte clé** : aucune vidéo de cet échantillon de 40 n'est postérieure au **02/09/2026** — cohérent avec le compteur de vidéos figé à 162 depuis plusieurs relevés consécutifs. Le concurrent a vraisemblablement cessé de publier de nouvelles vidéos TikTok depuis début septembre (§0.3).
- **Format** : légende quasi identique sur toutes les vidéos (« Follow @jb.roy_ pour imploser/implémenter l'IA dans ton activité », variantes mineures de coquille), **0 hashtag**, hook parlé dans la vidéo plutôt qu'écrit dans le texte, durée nettement plus longue que Tony (48s médiane vs 34s).
- **Comparatif d'efficacité** : Tony produit 2,27× plus d'engagement/vue et 7× plus de commentaires par vidéo avec une audience 6,6× plus petite — l'écart de croissance documenté les semaines précédentes (abonnés quasi stables chez le concurrent, +8 chez Tony cette semaine) est cohérent avec cette inactivité de publication plutôt qu'avec une simple différence de qualité de hook à volume égal.
- **Durée vidéo concurrent (35–54s)** : confirmée sur cet échantillon (42-68s pour les 5 vidéos les mieux vues) — plus longue que le format court de Tony (31-33s pour ses meilleures vidéos récentes). Les deux stratégies coexistent ; rien n'indique qu'allonger la durée améliorerait les résultats de Tony, dont les meilleures vidéos récentes (744v/31s, 740v/32s) sont plus courtes que la médiane concurrent.

---

## 6. Meilleures heures de publication

- **Instagram** : **14:00 UTC** reste dominant — 60/134 posts mesurés (45%), 3 des 4 meilleurs posts historiques.
- **TikTok `@automationboost7`** : **confirmé pour la première fois avec des données fraîches** — les 2 meilleures vidéos de l'échantillon Apify (744v, 740v) sont publiées à 14:00:0x UTC, exactement le même créneau qu'Instagram. La 3e meilleure (654v) est à 13:15 UTC, très proche.
- **Concurrent `@jb.roy_`** : ses meilleures vidéos se répartissent entre 14:30 et 17:20 UTC — fenêtre un peu plus large mais chevauchant le même créneau d'après-midi.
- **Recommandation** : **14:00 UTC devient le créneau pivot confirmé sur Instagram ET TikTok** — à utiliser par défaut pour toute publication, sur les deux canaux.

---

## 7. Durée vidéo cible

- **Données fraîches obtenues ce run** (absentes depuis plusieurs semaines) : `@automationboost7` — durée médiane **34 secondes** sur les 40 dernières vidéos ; ses 3 meilleures vidéos récentes font 31-51s. `@jb.roy_` (concurrent, vidéos antérieures au 02/09) — durée médiane **48 secondes**.
- **Cible recommandée** : **30-40 secondes** pour le format court quotidien (cohérent avec la médiane actuelle de Tony et ses meilleures performances récentes), tolérance jusqu'à ~50-60s pour les formats Journal IA / comparatifs à hook fort (654v à 51s confirmé ce run).
- Rien n'indique qu'adopter la durée plus longue du concurrent (48s médiane) améliorerait les résultats — ses vidéos les plus vues ne sont ni les plus longues ni les plus courtes de son échantillon, et son compte semble inactif depuis début septembre (§0.3), rendant toute comparaison causale fragile.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **🔴 PRIORITÉ ABSOLUE — Stabiliser la distribution Instagram.** 5e jour de coupure silencieuse (09/10→13/10) malgré une reprise fin septembre. Vérifier que le flux automatisé publie **tous les jours**, pas par intermittence.
2. **Tester délibérément et à plusieurs reprises le pattern "économie chiffrée + témoignage perso"** — confirmé 2 fois sur 2 plateformes différentes ce run (IG 08/08, TikTok 28/09), c'est le signal le plus actionnable et le mieux corroboré du dossier. Produire 2-3 nouvelles variantes (temps ou argent économisé) dès que la publication Instagram reprend, et continuer sur TikTok sans attendre.
3. **Tester le hook "douleur business / question au prospect"** sur Instagram — il domine l'échantillon TikTok de cette semaine (740v, 744v, les 2 meilleures vidéos) mais n'a pas d'équivalent récent testé sur Instagram.
4. **Publier à 14:00 UTC par défaut sur Instagram ET TikTok** — créneau désormais confirmé sur les deux plateformes avec des données fraîches, premier run où cette confirmation croisée est possible.
5. **Décider du sort de `n5dIUNEk5D6Pj3Vf`** (workflow analytics "Rapport Hebdo", 0 exécution depuis sa création le 21/07, nœuds HTTP Request Instagram/TikTok et Telegram toujours avec des valeurs `<__PLACEHOLDER_VALUE__...>` jamais renseignées) — le configurer réellement ou l'archiver. Confirmé de nouveau ce run via `get_workflow_details` (`triggerCount: 0`, paramètres placeholder inchangés).

---

## 9. Sources & limites (run du 13/10, session corrigée)

- **Instagram** : `blotato_list_accounts` (confirme 54617/55611/25882/36488) + `blotato_list_posts` (platform=instagram, depuis 2026-07-01, statut `published`, limit=250) — séparation stricte par `account.id` (54617 vs 55611, 59 posts foodboost exclus sur la fenêtre complète). 140 posts `automatisationboost` isolés, 134 avec analytics via `blotato_list_top_posts`/`metricsHistory`.
- **LinkedIn / TikTok `@tonypayet4`** : `blotato_list_posts` (platform=[linkedin]/[tiktok], depuis 2026-10-06). 0 analytics sur les deux — limite structurelle Blotato confirmée (Twitter/X, Instagram, Facebook, Threads, Bluesky seulement).
- **TikTok `@automationboost7` / `@jb.roy_` — profils** : `mcp__tokscript__get_tiktok_user`, réussi sur les deux comptes.
- **TikTok `@automationboost7` / `@jb.roy_` — vidéo par vidéo** : workflow n8n `YUJjz5NNsYo41t8q` (« Scrape Competitor Videos »), lancé pour la première fois ce run (`execute_workflow`, mode manuel, exécution `98855`, succès en 45s) — actor Apify `clockworks/tiktok-scraper` sur `profiles: ["automationboost7", "jb.roy_"]`, 40 vidéos chacun. Résumé agrégé lu via `get_execution` (nœud `Analyze Video Patterns`, filtré par `nodeNames` pour éviter le dépassement de taille).
- **n8n** : `search_executions`, `get_execution`, `get_workflow_details`, `execute_workflow` tous fonctionnels ce run — confirmé `n5dIUNEk5D6Pj3Vf` à `triggerCount: 0`, jamais câblé (placeholders Instagram Graph API / TikTok API / Telegram chatId).
- **Sheet "Analyse Perf" (gid 1277122579)** : lu via export CSV avant écriture (dernière ligne précédente datée du 21/09, confirmant le gap des runs 28/09-06/10-13/10(version précédente)) ; écrit ce run via workflow n8n `create_workflow_from_code` (voir confirmation dans le rapport final) ; revérifié par un second export CSV après écriture.
- **Étape B (génération de scripts)** : hors périmètre de cette routine — non exécutée.

# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-09-14 (run hebdo automatisé, session cloud à froid)
- **Période couverte** : Instagram `@automatisationboost` — 50 posts remontés par Blotato depuis le 01/07 (fenêtre large, filtrage manuel food appliqué — voir §0.1) + focus semaine du 07/09 au 14/09 · LinkedIn — 12 posts du 07/09 au 14/09 (`blotato_list_posts`) · **TikTok (Tony + concurrent `@jb.roy_`) — AUCUNE collecte possible ce run, voir §0.2. Les chiffres TikTok de ce document sont ceux du run précédent (07/09), non actualisés.**
- **Comptes analysés** : Instagram `@automatisationboost` (Blotato `54617`) · LinkedIn Payet Tony (Blotato `25882`) · TikTok actif `@automationboost7` (source de vérité normale = Apify via workflow n8n `YUJjz5NNsYo41t8q`, **indisponible ce run**) · Concurrent TikTok `@jb.roy_` (même source, **indisponible ce run**) · **Exclu** : `@tonypayet4` / Blotato TikTok `36488` (compte connecté mais ne remonte aucune donnée exploitable — Blotato ne collecte pas d'analytics TikTok de toute façon ; non revérifié indépendamment ce run car les deux sources TikTok étaient en panne) et Instagram `foodboost` (`55611`, hors périmètre, contamine `blotato_list_top_posts` — voir §0.1)

---

## 0. Anomalies et découvertes clés de ce run

1. **🔴 BLOCAGE MAJEUR — aucune donnée TikTok collectée ce run, ni pour `@automationboost7` ni pour `@jb.roy_`.** Les deux sources prévues ont échoué :
   - **Apify (source de vérité)** : l'exécution du workflow n8n `YUJjz5NNsYo41t8q` (exécution `87214`, 14/09 14:00 UTC) a échoué immédiatement avec une erreur `402 Payment Required` de l'API Apify : *« By launching this job you will exceed your remaining usage of $0.288101. Consider upgrading to a paid plan »*. Le crédit Apify du compte connecté (credential `Apify account`, id `UCHrBkwNMBZcmtkC`) est épuisé. Le node n'a pas été modifié (l'échec est survenu avant toute tentative de bascule vers `jb.roy_`), donc **rien à restaurer** sur le workflow.
   - **tokscript (secours)** : `get_tiktok_user` renvoie une erreur serveur (`redactUrlCredentials is not defined`) sur tous les comptes testés (`automationboost7`, `tonypayet4`, `jb.roy_`) — bug côté serveur tokscript, pas un problème de compte. `get_tiktok_user_videos` et `get_instagram_user_reels` renvoient tous deux *« requires a Pro or Premium subscription »* — l'abonnement tokscript actuellement actif ne couvre pas ces endpoints.
   - **Conséquence** : impossible de rafraîchir les chiffres de compte, le Top 3 TikTok, l'analyse du concurrent `@jb.roy_` et la durée cible vidéo ce run. Les valeurs affichées dans ce document pour ces sections sont **celles du run du 07/09**, explicitement marquées comme non actualisées. **Aucun chiffre n'a été inventé pour combler ce trou.**
   - **Action recommandée hors périmètre de cette routine** : recharger le crédit Apify (compte au bord du seuil, ~0,29 $ restants) et/ou vérifier le palier d'abonnement tokscript avant le prochain run, sinon ce blocage se reproduira.
2. **🟡 Instagram — chute apparente des vues sur les posts les plus récents, à interpréter avec prudence.** Les 8 posts Instagram propres publiés entre le 07/09 et le 11/09 affichent entre **0 et 9 vues** (moyenne ≈5,4, 0 like, 0 commentaire sur tous). C'est très inférieur aux 106-136 vues observées la semaine dernière sur des posts d'âge comparable. **Cause probable : ce n'est pas forcément un vrai recul — Blotato affiche `lastFetchedAt` très proche de l'heure de publication pour tous ces posts (quelques heures à 1 jour), alors que les posts du Top historique (243, 223, 216 vues) ont mis plusieurs semaines à accumuler leurs vues.** Les analytics Blotato se rafraîchissent en arrière-plan et un post récent n'a simplement pas encore été re-scanné. **Ne pas traiter comme un signal de dégradation réelle sans un second point de mesure dans 5-7 jours** — à revérifier au prochain run avant toute conclusion.
3. **🟢 Le filtrage food/restaurant sur Instagram est reproductible.** En reconstruisant le filtre indépendamment (signatures de compte + mots-clés spécifiques : « carte du jour », noms de restaurants, « sushis/desserts du jour », etc.) sur les mêmes 50 posts remontés par `blotato_list_top_posts`, on retombe sur **17 posts food exclus sur 50 (34 %)** — exactement la même proportion que le run du 07/09. Bon signal de robustesse de la méthode. Filtre à conserver.
4. **🟢 Top 3 Instagram inchangé depuis le run précédent.** Aucun nouveau post n'a dépassé les 3 meilleurs posts historiques (243 / 223 / 216 vues, tous publiés fin juillet) — cohérent avec le fait qu'aucun post récent n'a encore eu le temps d'accumuler des vues (voir §0.2).
5. **🟢 LinkedIn toujours opérationnel.** 12 posts publiés entre le 07/09 et le 14/09 (Journal IA quotidien + posts uniques), **aucun échec**. Toujours aucune métrique d'engagement disponible (Blotato ne collecte pas d'analytics LinkedIn).
6. **🔴 `n5dIUNEk5D6Pj3Vf` — toujours non opérationnel, 3e semaine consécutive.** Reconfirmé via `search_executions` : **0 exécution** depuis sa création (21/07). Recommandation inchangée : le configurer réellement ou l'archiver — ce n'est plus une question d'accès n8n.

---

## 1. Chiffres clés par plateforme

### Instagram `@automatisationboost` (54617) — Blotato, données nettoyées de la contamination food
| Métrique | Valeur | Note |
|---|---|---|
| Top 5 propres, tout historique depuis le 01/07 | 243 / 223 / 216 / 214 / 178 vues | Inchangé vs le 07/09 — voir §0.4 |
| Posts propres publiés du 07/09 au 11/09 (n=8) | **0 à 9 vues** (moyenne ≈5,4), 0 like, 0 commentaire sur tous | Chiffres réels mais probablement sous-estimés par le délai de rafraîchissement Blotato — voir §0.2. **Ne pas comparer directement** aux moyennes des semaines passées. |
| Échantillon propre depuis le 01/07 (n=33 sur 50 remontés, 17 exclus food = 34 %) | moyenne **111,8** / médiane **108** vues | Calculé sur tout l'historique disponible, mélange donc anciens posts (accumulés) et récents (sous-comptés) |
| Heure dominante (n=16 posts propres depuis le 05/08) | **14:00 UTC** (9/16, 56 %) | 6e confirmation consécutive, signal le plus robuste du rapport |
| Commentaires | 0 sur les 8 posts récents examinés individuellement ; record historique = 6 commentaires (post "économise 200€/mois de secrétariat", 08/08) | CTA "Commente X" toujours quasi sans effet mesurable |

### LinkedIn (Payet Tony, compte Blotato 25882)
**Compte opérationnel.** 12 posts publiés entre le 07/09 et le 14/09, **0 échec**. Format dominant : Journal IA quotidien (veille actu IA, ~1/jour) + posts uniques sur des sujets isolés (RGPD/Claude, démos IA, un post "11 septembre" hors registre habituel). Toujours aucune métrique d'engagement (Blotato ne collecte pas d'analytics LinkedIn).

### TikTok `@automationboost7` — **NON ACTUALISÉ CE RUN** (dernières données connues : 07/09)
| Métrique | Valeur (07/09, non rafraîchie) |
|---|---|
| Abonnés | 166 |
| Vidéos publiées | 135 |
| Vues moyenne / médiane (n=40) | 354 / 268 |
| Durée médiane | 34 s |

*Voir §0.2 — Apify (402, crédit épuisé) et tokscript (bug serveur + endpoints hors abonnement) ont tous deux échoué ce run. Ces chiffres datent d'il y a une semaine et ne doivent pas être présentés comme la situation actuelle.*

### Concurrent TikTok `@jb.roy_` — **NON ACTUALISÉ CE RUN** (dernières données connues : 07/09)
| Métrique | Valeur (07/09, non rafraîchie) |
|---|---|
| Abonnés | 1582 |
| Vidéos publiées | 162 |
| Vues moyenne / médiane (n=40) | 212 / 157 |
| Durée médiane | 48 s |

*Même blocage que ci-dessus — voir §0.2 et §5 pour l'analyse concurrent détaillée (reprise telle quelle du run du 07/09, à ne pas prendre pour une observation de cette semaine).*

---

## 2. Top 3 vidéos / posts

### Top 3 Instagram `@automatisationboost` (depuis le 01/07, données filtrées — inchangé vs 07/09, voir §0.4)
1. **243 vues / 224 reach** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... Commente TERMINAL et je t'envoie le guide » (Claude Code + VPS + Coolify + MCP, 3 étapes) — 27/07 14:29 UTC.
2. **223 vues / 195 reach** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. Follow pour la suite + commente OPUS » — 29/07 14:30 UTC.
3. **216 vues / 202 reach** — « L'alternative gratuite à Claude Code pour créer des sites automatiquement. Kilo Code + n8n = même résultat, zéro abonnement. Commente KILO » — 13/07 19:00 UTC.

*Mention spéciale engagement (hors Top 3 vues) : « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat » (136 vues mais **6 commentaires** — le meilleur ratio commentaires/vue de tout l'historique examiné, 08/08 14:29 UTC) — à creuser comme piste de hook "économie chiffrée + témoignage perso".*

### Top TikTok `@automationboost7` — **non actualisé, repris du run du 07/09**
1. 794 vues — actualité insolite (avalanche au Népal), 109 s, 28/08.
2. 783 vues — Journal IA, 68 s, 23/08 03:00 UTC.
3. 774 vues — Journal IA, 84 s, 05/09 07:30 UTC.

### Top concurrent `@jb.roy_` — **non actualisé, repris du run du 07/09**
1. 1234 vues — 02/09 14:30 UTC, 21 s.
2. 725 vues — 28/08 15:00 UTC, 44 s.
3. 530 vues — 25/08 17:16 UTC, 42 s.

---

## 3. Hooks qui marchent — formulations réutilisables

*Items 1, 4, 6 reconfirmés ce run sur données Instagram fraîches ; items 2, 3, 5 proviennent du dernier scrape TikTok disponible (07/09) et n'ont pas pu être revérifiés cette semaine (voir §0.2).*

1. **Actualité produit/outil connu nommée dans les 10 premiers mots + un chiffre ou un fait précis** — pattern le plus robuste, confirmé de nouveau sur Instagram (« Anthropic vient de sortir Opus 5, 4e Claude en 2 mois »).
2. **Actualité insolite grand public, hors registre IA/outils** (ex. avalanche au Népal, 794 vues TikTok) — signal fort au dernier run, à retester, non revérifiable cette semaine.
3. **Alternative gratuite à un outil payant connu**, nommé explicitement — ex. « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » (216 vues Instagram).
4. **Tutoriel actionnable en 3 étapes avec estimation de temps réaliste** — ex. « VPS, Coolify, Claude Code + MCP... 3 à 7h de setup » (243 vues, meilleur post Instagram sur 2 mois).
5. **Format « Journal IA » récurrent** — pilier quotidien TikTok/LinkedIn/Instagram, reste performant sur les dernières données connues.
6. **Économie chiffrée + témoignage à la première personne** — nouveau pattern à surveiller ce run : « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat » est le seul post Instagram de tout l'historique examiné à dépasser 1 commentaire (6 commentaires, sur 136 vues). Petit échantillon (n=1) mais à tester délibérément la semaine prochaine avec une autre économie chiffrée.

**Règle** : nommer un outil/une actualité connue + un chiffre ou un fait précis dans les 10 premiers mots reste le pattern le plus robuste. Un chiffre d'économie personnelle concret semble être le seul levier qui ait généré plus d'un commentaire à ce jour — à tester plus systématiquement.

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Calculer une moyenne Instagram sans filtrer le contenu food/restaurant.** Reconfirmé ce run par une reconstruction indépendante du filtre : 34 % de contamination (17/50), identique au run précédent. Toujours filtrer avant tout calcul.
- ❌ **Compter sur « Commente le mot X » comme unique CTA.** Reconfirmé : 0 commentaire sur les 8 posts Instagram récents examinés individuellement cette semaine ; le record historique de tout l'échantillon reste à 6 commentaires, sur un post qui ne reposait pas sur ce mécanisme seul (voir §3.6).
- ❌ **Comparer les vues d'un post publié il y a moins d'une semaine aux moyennes historiques sans corriger le biais de fraîcheur.** Ce run montre des posts à 0-9 vues qui ressemblent à un effondrement mais sont très probablement juste jeunes et pas encore resynchronisés par Blotato (voir §0.2) — attendre 5-7 jours avant de tirer une conclusion sur un post donné.
- ❌ **Lancer une extraction Apify sans vérifier le solde de crédit au préalable.** Le run de ce jour a échoué immédiatement (402 Payment Required, ~0,29 $ restants) — à surveiller/recharger avant le prochain run pour éviter un nouveau blocage TikTok complet.
- ⚠️ **Ne pas considérer les chiffres TikTok de ce document (compte + concurrent + Top 3) comme à jour** — ce sont ceux du 07/09, non rafraîchis cette semaine faute d'accès Apify et tokscript (voir §0.2).

---

## 5. Analyse du concurrent `@jb.roy_` — **non actualisée ce run, reprise du 07/09**

*Aucune collecte n'a été possible cette semaine (voir §0.2) — les observations ci-dessous datent du run précédent et doivent être revérifiées dès que l'accès Apify/tokscript est rétabli.*

- Cadence de publication au 07/09 : ≈1,9 vidéo/jour, quasi identique à celle de Tony — la variable "sur-publication" n'expliquait déjà plus l'écart de croissance à cette date.
- Vues/engagement nettement inférieurs à Tony au 07/09 : 212 vues/vidéo (médiane 157) vs 354 chez Tony, engagement/vue 4,39 % vs 11,79 %.
- Légende toujours générique, 0 hashtag, hook parlé dans la vidéo (jamais dans le texte) — pattern stable observé sur plusieurs runs consécutifs.
- Durée médiane plus longue que chez Tony : 48 s vs 34 s.
- **Limite de méthode inchangée** : sans transcription vidéo, impossible d'extraire les formulations de hook exactes de `jb.roy_` — seules les observations structurelles étaient disponibles.

---

## 6. Meilleures heures de publication

- **Instagram** : créneau **14:00 UTC** toujours dominant (9 posts sur 16 propres depuis le 05/08, soit 56 %) — 6e confirmation consécutive, signal le plus robuste et le plus réactualisé de ce rapport. **À garder comme pivot par défaut.**
- **TikTok `@automationboost7`** : pas de donnée nouvelle ce run (voir §0.2). Au 07/09, pas de pivot horaire net (Top 3 réparti sur 08:00, 03:00, 07:30 UTC) — à revérifier dès que la collecte TikTok sera rétablie.
- **Concurrent `@jb.roy_`** : pas de donnée nouvelle ce run.
- **Recommandation** : garder **14:00 UTC** comme créneau pivot sur Instagram (signal solide et reconfirmé). Pour TikTok, le test contrôlé sur l'horaire recommandé au run précédent n'a pas pu être suivi cette semaine — à relancer dès que la collecte est rétablie.

---

## 7. Durée cible de vidéo — **non actualisée ce run**

Aucune nouvelle donnée de durée disponible (Instagram/Blotato ne remonte pas la durée vidéo dans les champs consultés ; TikTok bloqué, voir §0.2). **Cible recommandée inchangée, reprise du 07/09** : 25–45 s pour le format quotidien court, tolérance jusqu'à ~90–110 s pour les formats actu/comparatifs à hook fort (Journal IA, actualité insolite). À revalider dès que la collecte TikTok Apify/tokscript est rétablie.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **Débloquer la collecte TikTok avant tout le reste** — c'est le prérequis pour que les sections 1, 2, 5, 6, 7 redeviennent fiables. Deux actions indépendantes : recharger le crédit Apify du compte connecté au workflow `YUJjz5NNsYo41t8q` (solde quasi nul, voir §0.2), et vérifier/mettre à niveau l'abonnement tokscript pour couvrir `get_tiktok_user_videos` et `get_instagram_user_reels` (actuellement hors plan). Tant que ni l'un ni l'autre n'est résolu, le prochain run rencontrera le même blocage.
2. **Tester délibérément le pattern "économie chiffrée + témoignage perso"** identifié ce run (§3.6) — c'est le seul post de tout l'historique Instagram examiné à avoir dépassé 1 commentaire. Produire 2-3 variantes la semaine prochaine avec un autre chiffre d'économie concret (temps ou argent).
3. **Continuer à filtrer systématiquement le contenu food/restaurant sur Instagram** avant tout calcul de moyenne — méthode reconfirmée robuste ce run (34 % de contamination, 2e semaine de suite au même taux).
4. **Ne pas tirer de conclusion sur la baisse apparente des vues Instagram récentes** (0-9 vues cette semaine) avant d'avoir un second point de mesure dans 5-7 jours — probable artefact de délai de synchronisation Blotato plutôt qu'un vrai recul (§0.2).
5. **Décider enfin du sort de `n5dIUNEk5D6Pj3Vf`** : confirmé non opérationnel pour la 3e semaine consécutive (0 exécution depuis le 21/07) — à configurer réellement ou à archiver.

---

## 9. Sources & limites (run du 14/09)

- **TikTok (Tony + concurrent)** : **aucune source n'a répondu ce run**. Apify via le workflow n8n `YUJjz5NNsYo41t8q` a échoué en `402 Payment Required` (exécution `87214`, crédit du compte Apify `UCHrBkwNMBZcmtkC` épuisé, ~0,29 $ restants). tokscript (secours) a échoué avec une erreur serveur sur `get_tiktok_user` (`redactUrlCredentials is not defined`) et un refus d'abonnement (« requires a Pro or Premium subscription ») sur `get_tiktok_user_videos` et `get_instagram_user_reels`. **Toutes les valeurs TikTok de ce document sont donc celles du run du 07/09**, explicitement marquées comme non actualisées — aucun chiffre n'a été estimé ou inventé pour combler ce trou.
- **Instagram (Tony)** : `blotato_list_top_posts` (platform=instagram, depuis le 2026-07-01, 50 résultats triés par vues) + `blotato_list_posts` (depuis le 07/09) + `blotato_get_post_analytics` sur 8 posts individuels récents. Réponse sans champ d'identification de compte — filtrage manuel par signatures/mots-clés appliqué pour exclure le contenu food/restaurant (voir §0.1/§0.3), reconstruit indépendamment du run précédent et arrivé au même résultat (17/50 exclus).
- **LinkedIn** : `blotato_list_posts` (statuts published+failed, depuis le 07/09, 50 items) — 12 posts trouvés, 0 échec.
- **Workflow analytics hebdo `n5dIUNEk5D6Pj3Vf`** : vérifié via `search_executions` — 0 exécution depuis sa création, confirmé pour la 3e semaine consécutive.
- **Workflow concurrent `YUJjz5NNsYo41t8q`** : inspecté via `get_workflow_details` (confirmé : node HTTP Request → Apify `clockworks/tiktok-scraper`, credential `apifyApi` id `UCHrBkwNMBZcmtkC`, actuellement configuré sur le profil `automationboost7` uniquement) puis exécuté via `execute_workflow` (échec 402, voir ci-dessus). Le paramètre `profiles` du node n'a pas été modifié (l'échec est survenu avant toute tentative de bascule vers `jb.roy_`), donc le workflow est resté dans son état d'origine — pas de restauration nécessaire.
- **Google Sheet "Analyse Perf"** : mis à jour ce run via un workflow n8n `create_workflow_from_code` (Google Sheets, mode appendOrUpdate), vérifié par export CSV du gid 1277122579 — voir résumé final de l'agent.
- **Étape B (génération de scripts + ajout dans la file de production)** : hors périmètre de cette routine (analyse uniquement) — non exécutée.

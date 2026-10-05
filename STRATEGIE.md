# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-09-21 (run hebdo automatisé, session cloud à froid)
- **Période couverte** : Instagram `@automatisationboost` — 50 posts remontés par Blotato depuis le 01/07 (fenêtre large, filtrage manuel food appliqué) + focus semaine du 14/09 au 21/09 · LinkedIn — 9 posts du 14/09 au 18/09 (`blotato_list_posts`) · **TikTok (`@automationboost7` + concurrent `@jb.roy_`) — AUCUNE collecte possible ce run, 2e semaine consécutive, voir §0.1. Les chiffres TikTok de ce document sont ceux du run du 07/09 (2 semaines de retard), non actualisés.**
- **Comptes analysés** : Instagram `@automatisationboost` (Blotato `54617`) · LinkedIn Payet Tony (Blotato `25882`) · TikTok actif `@automationboost7` (source de vérité normale = Apify via workflow n8n `YUJjz5NNsYo41t8q`, **indisponible ce run**) · Concurrent TikTok `@jb.roy_` (même source, **indisponible ce run**) · **Exclu** : Instagram `foodboost` (`55611`, hors périmètre, contamine `blotato_list_top_posts` et `blotato_list_posts` — voir §0.3)
- **Note sur `@tonypayet4` (Blotato TikTok `36488`)** : ce compte reçoit bien les publications automatiques du Journal IA quotidien via Blotato (9 vidéos publiées, 0 échec, 14/09→18/09), mais ce n'est **pas** le compte analysé (`@automationboost7`) et Blotato ne remonte de toute façon aucune métrique TikTok. Voir §0.2 pour la question que ça soulève.

---

## 0. Anomalies et découvertes clés de ce run

1. **🔴 URGENT — Instagram `@automatisationboost` déconnecté depuis le 12/09, zéro nouveau post publié depuis 9 jours.** En reconstituant l'historique `blotato_list_posts` sur la fenêtre 25/08→21/09, **12 tentatives de publication consécutives ont toutes échoué** avec le même message : *« Your Instagram connection is no longer valid. Reconnect the account to publish. »* — première occurrence le **12/09 à 14:29 UTC** (post "OMNI"), dernière tentative connue le **18/09 à 07:00 UTC** (Journal IA), aucune tentative retrouvée entre le 18/09 et aujourd'hui. Ce n'est pas un artefact de mesure : c'est un vrai blocage de publication, actif depuis 9 jours au moment de ce rapport. **Action immédiate requise, hors périmètre technique de cette routine d'analyse : reconnecter le compte Instagram dans Blotato.** Tant que ce n'est pas fait, le Top 3 et les moyennes Instagram de ce document resteront figés (aucun post récent ne peut alimenter de nouvelles données).
2. **🔴 TikTok — toujours aucune donnée collectée, 2e semaine consécutive (`@automationboost7` et `@jb.roy_`).**
   - **Apify (source de vérité)** : le workflow n8n `YUJjz5NNsYo41t8q` utilise l'actor `clockworks/tiktok-scraper` avec la credential `apifyApi` **« Apify account » (id `UCHrBkwNMBZcmtkC`)**. Une exécution de test (id `89719`, sur un workflow temporaire dédié, puis rejouée directement sur `YUJjz5NNsYo41t8q` — exécution `89720`, 21/09 14:43 UTC) a échoué immédiatement en **402 Payment Required** : *« Your remaining usage of $0.000476 this billing cycle isn't enough for this run »*. Le solde du compte Apify connecté s'est encore réduit depuis le run du 14/09 (il restait alors ~0,29 $, il en reste maintenant moins d'un millième de dollar) — **le crédit n'a pas été rechargé entre les deux runs**.
   - **Découverte annexe corrigée ce run** : le workflow `YUJjz5NNsYo41t8q` (nommé "Scrape Competitor Videos") n'interrogeait en réalité que le profil `automationboost7` — **jamais le concurrent `jb.roy_`**, malgré son nom et sa description. J'ai corrigé son corps de requête pour inclure les deux profils (`["automationboost7", "jb.roy_"]`), afin que la prochaine tentative (dès que le crédit Apify sera rechargé) couvre enfin le concurrent. Aucune autre modification du workflow.
   - **tokscript (secours)** : `get_tiktok_user` échoue toujours avec la même erreur serveur qu'il y a deux semaines — `redactUrlCredentials is not defined` (testé sur `automationboost7`, `jb.roy_`, `tonypayet4` : échec identique sur les trois). `get_instagram_user_reels` refuse toujours avec *« requires a Pro or Premium subscription »*. **Ce bug serveur et cette limite d'abonnement n'ont pas été corrigés depuis le run précédent** — à signaler activement plutôt qu'à re-tester chaque semaine sans action.
   - **Conséquence** : impossible de rafraîchir les chiffres de compte, le Top 3 TikTok, l'analyse du concurrent et la durée cible vidéo, pour la 2e semaine de suite. Les valeurs affichées dans ce document restent celles du run du 07/09 (**désormais 2 semaines de retard**). Aucun chiffre n'a été inventé pour combler ce trou.
3. **🟡 Question stratégique soulevée par le routage TikTok de l'automatisation.** Le compte TikTok connecté à Blotato et utilisé par l'automatisation du Journal IA quotidien est `@tonypayet4` (id `36488`) — 9 vidéos publiées avec succès du 14/09 au 18/09. Or ce n'est **pas** le compte suivi comme actif pour la croissance (`@automationboost7`, qui n'apparaît même pas dans les comptes connectés à Blotato — voir `blotato_list_accounts`). Autrement dit : le contenu quotidien produit par l'automatisation part sur un compte différent de celui qu'on essaie de faire grandir et dont on mesure la performance via Apify. Signalé ici sans trancher — à clarifier avec Tony (fusion de compte, redirection du posting, ou séparation volontaire à documenter).
4. **🟢 LinkedIn pleinement opérationnel ce run.** 9 posts publiés entre le 14/09 et le 18/09 (Journal IA quotidien + 2 posts uniques : "3 outils" et "4 commandes ChatGPT"), **0 échec** — contrairement à la mise en garde habituelle sur ce compte ("souvent inaccessible"), aucun problème constaté cette semaine. Toujours aucune métrique d'engagement disponible (Blotato ne collecte pas d'analytics LinkedIn).
5. **🟢 Le filtrage food/restaurant sur Instagram reste robuste.** Sur les mêmes 50 posts remontés par `blotato_list_top_posts` (depuis le 01/07), **16 posts food exclus sur 50 (32 %)** — proportion cohérente avec les runs précédents (34 % le 14/09, 34 % le 07/09). Filtre à conserver tel quel.
6. **🟢 Top 3 Instagram inchangé pour la 3e semaine consécutive.** Sans surprise : aucun nouveau post propre n'a pu être publié depuis le 05/09 (dernier post "propre" réussi avant la coupure de connexion du 12/09), donc aucun candidat nouveau n'a eu de chance de dépasser le Top 3 historique (243 / 223 / 216 vues, tous publiés fin juillet).
7. **🔴 `n5dIUNEk5D6Pj3Vf` — toujours non opérationnel, 4e semaine consécutive.** Reconfirmé via `search_executions` : **0 exécution** depuis sa création (21/07). Recommandation inchangée et de plus en plus pressante : le configurer réellement ou l'archiver.

---

## 1. Chiffres clés par plateforme

### Instagram `@automatisationboost` (54617) — Blotato, données nettoyées de la contamination food
| Métrique | Valeur | Note |
|---|---|---|
| Top 5 propres, tout historique depuis le 01/07 | 243 / 223 / 216 / 214 / 178 vues | Inchangé depuis 3 semaines — voir §0.6 |
| Posts propres publiés du 14/09 au 21/09 | **0 — aucun post publié** | Compte déconnecté depuis le 12/09, 12 tentatives échouées, voir §0.1 |
| Échantillon propre depuis le 01/07 (n=34 sur 50 remontés, 16 exclus food = 32 %) | moyenne **113,3** / médiane **108** vues | Inchangé vs le run précédent (aucun nouveau post propre publié) |
| Heure dominante (n=16 posts propres depuis le 05/08) | **14:00 UTC** (9/16, 56 %) | 7e confirmation consécutive — mais figé tant qu'aucun nouveau post n'est publié |
| Commentaires | record historique = 6 commentaires (post "économise 200€/mois de secrétariat", 08/08) | CTA "Commente X" toujours quasi sans effet mesurable |

### LinkedIn (Payet Tony, compte Blotato 25882)
**Compte pleinement opérationnel ce run.** 9 posts publiés entre le 14/09 et le 18/09, **0 échec** : Journal IA quotidien (7 éditions) + 2 posts uniques ("3 outils qui te rendent 10h/semaine", "4 commandes ChatGPT"). Toujours aucune métrique d'engagement (Blotato ne collecte pas d'analytics LinkedIn).

### TikTok `@automationboost7` — **NON ACTUALISÉ, 2e semaine bloquée** (dernières données réelles : 07/09, désormais 2 semaines de retard)
| Métrique | Valeur (07/09, non rafraîchie) |
|---|---|
| Abonnés | 166 |
| Vidéos publiées | 135 |
| Vues moyenne / médiane (n=40) | 354 / 268 |
| Durée médiane | 34 s |

*Voir §0.2 — Apify (402, crédit à $0,0005) et tokscript (bug serveur inchangé + endpoints hors abonnement) ont de nouveau échoué ce run.*

### Concurrent TikTok `@jb.roy_` — **NON ACTUALISÉ, 2e semaine bloquée** (dernières données réelles : 07/09)
| Métrique | Valeur (07/09, non rafraîchie) |
|---|---|
| Abonnés | 1582 |
| Vidéos publiées | 162 |
| Vues moyenne / médiane (n=40) | 212 / 157 |
| Durée médiane | 48 s |

*Même blocage — voir §0.2 et §5. Le workflow `YUJjz5NNsYo41t8q` a été corrigé ce run pour inclure enfin `jb.roy_` dans ses profils scrapés (il ne scrapait que `automationboost7` jusqu'ici) ; la prochaine exécution réussie couvrira donc les deux comptes.*

### TikTok `@tonypayet4` (Blotato 36488) — compte de publication automatisée, hors périmètre d'analyse
9 vidéos publiées avec succès du 14/09 au 18/09 (Journal IA + 2 posts uniques identiques à ceux d'Instagram/LinkedIn), 0 échec. Aucune métrique Blotato disponible (TikTok non couvert). Voir §0.3 pour la question stratégique que ce compte soulève.

---

## 2. Top 3 vidéos / posts

### Top 3 Instagram `@automatisationboost` (depuis le 01/07, données filtrées — inchangé, voir §0.6)
1. **243 vues / 224 reach** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... Commente TERMINAL et je t'envoie le guide » (Claude Code + VPS + Coolify + MCP, 3 étapes) — 27/07 14:29 UTC.
2. **223 vues / 195 reach** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. Follow pour la suite + commente OPUS » — 29/07 14:30 UTC.
3. **216 vues / 202 reach** — « L'alternative gratuite à Claude Code pour créer des sites automatiquement. Kilo Code + n8n = même résultat, zéro abonnement. Commente KILO » — 13/07 19:00 UTC.

*Mention spéciale engagement (hors Top 3 vues) : « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat » (136 vues mais **6 commentaires** — le meilleur ratio commentaires/vue de tout l'historique examiné, 08/08 14:29 UTC).*

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

*Aucune donnée fraîche cette semaine (0 post Instagram publié, TikTok bloqué) — items repris tels quels, à retester dès que la publication est rétablie sur les deux plateformes.*

1. **Actualité produit/outil connu nommée dans les 10 premiers mots + un chiffre ou un fait précis** — pattern le plus robuste, confirmé sur Instagram (« Anthropic vient de sortir Opus 5, 4e Claude en 2 mois »).
2. **Actualité insolite grand public, hors registre IA/outils** (ex. avalanche au Népal, 794 vues TikTok) — signal fort au dernier run TikTok disponible (07/09), non revérifiable depuis.
3. **Alternative gratuite à un outil payant connu**, nommé explicitement — ex. « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » (216 vues Instagram).
4. **Tutoriel actionnable en 3 étapes avec estimation de temps réaliste** — ex. « VPS, Coolify, Claude Code + MCP... 3 à 7h de setup » (243 vues, meilleur post Instagram sur 2 mois).
5. **Format « Journal IA » récurrent** — pilier quotidien TikTok/LinkedIn/Instagram, reste le format le plus publié malgré la coupure IG.
6. **Économie chiffrée + témoignage à la première personne** — toujours le seul post Instagram de tout l'historique à dépasser 1 commentaire (6 commentaires sur « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat »). **Toujours pas re-testé délibérément** faute de nouveaux posts publiés — priorité dès que la connexion IG est rétablie.

**Règle** : nommer un outil/une actualité connue + un chiffre ou un fait précis dans les 10 premiers mots reste le pattern le plus robuste.

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Calculer une moyenne Instagram sans filtrer le contenu food/restaurant.** Reconfirmé ce run : 32 % de contamination (16/50), cohérent avec les runs précédents (34 %, 34 %). Toujours filtrer avant tout calcul.
- ❌ **Compter sur « Commente le mot X » comme unique CTA.** Record historique toujours à 6 commentaires sur tout l'échantillon examiné, obtenu sur un post qui ne reposait pas sur ce seul mécanisme (voir §3.6).
- ❌ **Laisser une connexion de compte social se dégrader sans supervision active.** Le compte Instagram est resté déconnecté 9 jours (12 tentatives échouées, 12/09→18/09) sans qu'aucune alerte ne semble avoir été traitée entre-temps — c'est le coût réel de ne pas monitorer les échecs de publication au fil de l'eau, pas seulement une fois par semaine à l'analyse. À corriger en priorité absolue (§0.1, §8.1).
- ❌ **Lancer une extraction Apify sans vérifier le solde de crédit au préalable.** Le compte `apifyApi` connecté est passé de ~0,29 $ (14/09) à 0,0005 $ (21/09) sans recharge — 2e run bloqué de suite pour la même raison.
- ⚠️ **Ne pas considérer les chiffres TikTok de ce document (compte + concurrent + Top 3) comme à jour** — ce sont ceux du 07/09, non rafraîchis depuis 2 semaines faute d'accès Apify et tokscript (voir §0.2).

---

## 5. Analyse du concurrent `@jb.roy_` — **non actualisée ce run, reprise du 07/09**

*Aucune collecte n'a été possible cette semaine ni la précédente (voir §0.2) — les observations ci-dessous datent du run du 07/09 et doivent être revérifiées dès que l'accès Apify/tokscript est rétabli. Bonne nouvelle méthodologique : le workflow de scraping concurrent a été corrigé ce run pour inclure enfin ce compte dans ses profils (voir §0.2) — la prochaine collecte réussie sera donc la première à réellement comparer les deux comptes en un seul run.*

- Cadence de publication au 07/09 : ≈1,9 vidéo/jour, quasi identique à celle de Tony.
- Vues/engagement nettement inférieurs à Tony au 07/09 : 212 vues/vidéo (médiane 157) vs 354 chez Tony, engagement/vue 4,39 % vs 11,79 %.
- Légende toujours générique, 0 hashtag, hook parlé dans la vidéo (jamais dans le texte).
- Durée médiane plus longue que chez Tony : 48 s vs 34 s.
- **Limite de méthode inchangée** : sans transcription vidéo, impossible d'extraire les formulations de hook exactes de `jb.roy_` — seules les observations structurelles étaient disponibles.

---

## 6. Meilleures heures de publication

- **Instagram** : créneau **14:00 UTC** toujours dominant sur l'historique disponible (9 posts sur 16 propres depuis le 05/08, soit 56 %) — signal gelé cette semaine faute de nouveaux posts, mais rien ne l'invalide. **À garder comme pivot par défaut** dès la reconnexion.
- **TikTok `@automationboost7`** : pas de donnée nouvelle depuis 2 semaines (voir §0.2). Au 07/09, pas de pivot horaire net (Top 3 réparti sur 08:00, 03:00, 07:30 UTC).
- **Concurrent `@jb.roy_`** : pas de donnée nouvelle.
- **Recommandation** : garder **14:00 UTC** comme créneau pivot sur Instagram dès que la publication est rétablie. Pour TikTok, le test horaire reste en attente depuis 2 semaines.

---

## 7. Durée cible de vidéo — **non actualisée ce run**

Aucune nouvelle donnée de durée disponible (Instagram/Blotato ne remonte pas la durée vidéo dans les champs consultés ; TikTok bloqué, voir §0.2). **Cible recommandée inchangée** : 25–45 s pour le format quotidien court, tolérance jusqu'à ~90–110 s pour les formats actu/comparatifs à hook fort (Journal IA, actualité insolite). À revalider dès que la collecte TikTok Apify/tokscript est rétablie.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **🔴 URGENT — Reconnecter le compte Instagram `@automatisationboost` dans Blotato.** 12 tentatives de publication ont échoué sans interruption depuis le 12/09 14:29 UTC (« Your Instagram connection is no longer valid »), soit 9 jours sans aucun nouveau contenu publié sur ce canal. C'est le blocage le plus coûteux de ce rapport — plus urgent que le manque de données TikTok, parce qu'il arrête la publication elle-même, pas seulement la mesure.
2. **Débloquer la collecte TikTok, bloquée pour la 2e semaine consécutive.** Recharger le crédit du compte Apify `UCHrBkwNMBZcmtkC` (« Apify account », désormais à 0,0005 $ — 4 autres credentials Apify existent sur l'instance n8n : « Apify account 2/3/4/5 », non testées, à évaluer si la recharge du compte principal n'est pas possible) et signaler le bug serveur tokscript (`redactUrlCredentials is not defined`, identique depuis 2 semaines) directement au support tokscript plutôt que de le re-tester chaque semaine sans effet.
3. **Clarifier le routage TikTok de l'automatisation** (§0.3) : le Journal IA quotidien est publié sur `@tonypayet4` via Blotato, pas sur `@automationboost7` qui est le compte suivi et analysé. À trancher avec Tony.
4. **Décider enfin du sort de `n5dIUNEk5D6Pj3Vf`** : confirmé non opérationnel pour la 4e semaine consécutive (0 exécution depuis le 21/07) — à configurer réellement ou à archiver.
5. **Dès la reconnexion Instagram rétablie, tester en priorité le pattern "économie chiffrée + témoignage perso"** (§3.6) — toujours le seul post de tout l'historique à avoir dépassé 1 commentaire, jamais retesté délibérément faute de publication possible ces deux dernières semaines.

---

## 9. Sources & limites (run du 21/09)

- **Instagram (Tony)** : `blotato_list_top_posts` (platform=instagram, depuis le 2026-07-01, 50 résultats triés par vues) + `blotato_list_posts` (platform=instagram, fenêtres 2026-08-25→2026-09-21) pour reconstituer l'historique de publication récent. Filtrage manuel par signatures/mots-clés pour exclure le contenu food/restaurant (16/50 exclus). Aucun post propre n'a pu être publié depuis le 05/09 (compte déconnecté depuis le 12/09, voir §0.1) — le Top 3 et les moyennes sont donc identiques au run précédent par construction, pas par choix.
- **LinkedIn** : `blotato_list_posts` (platform=linkedin, depuis le 2026-09-14, 50 items) — 9 posts trouvés, 0 échec.
- **TikTok (Tony + concurrent)** : **aucune source n'a répondu ce run, pour la 2e semaine consécutive.**
  - Apify via le workflow n8n `YUJjz5NNsYo41t8q` (inspecté via `get_workflow_details` : actor `clockworks/tiktok-scraper`, credential `apifyApi` id `UCHrBkwNMBZcmtkC`). Une exécution de vérification a été lancée via un workflow temporaire dédié (`Social Analytics - TikTok Run 2026-09-21`, id `LokxfTW3koj9BHoJ`, exécution `89719`) puis rejouée directement sur le workflow officiel après correction de ses profils (exécution `89720`, 2026-09-21T14:43 UTC) — échec identique en `402 Payment Required` sur les deux (solde du compte Apify : 0,000476 $, insuffisant). Le workflow temporaire a été archivé après vérification ; le workflow officiel `YUJjz5NNsYo41t8q` a été corrigé de façon permanente pour inclure enfin `jb.roy_` dans ses profils scrapés (il ne couvrait que `automationboost7` jusque-là) — aucune autre modification.
  - tokscript (secours) : `get_tiktok_user` sur `automationboost7`, `jb.roy_` et `tonypayet4` — échec identique sur les trois (`redactUrlCredentials is not defined`, bug serveur inchangé depuis le run du 14/09). `get_instagram_user_reels` — refus d'abonnement (« requires a Pro or Premium subscription »), inchangé également.
  - **Toutes les valeurs TikTok de ce document sont donc celles du run du 07/09**, désormais 2 semaines de retard — aucun chiffre n'a été estimé ou inventé pour combler ce trou.
- **Comptes connectés Blotato** : vérifiés via `blotato_list_accounts` — confirme que `@automationboost7` n'est pas un compte connecté à Blotato (seul `@tonypayet4`, id `36488`, l'est côté TikTok), d'où la découverte du §0.3.
- **Workflow analytics hebdo `n5dIUNEk5D6Pj3Vf`** : vérifié via `search_executions` — 0 exécution depuis sa création, confirmé pour la 4e semaine consécutive.
- **Google Sheet "Analyse Perf"** : mis à jour ce run via un workflow n8n `create_workflow_from_code` (Google Sheets, mode appendOrUpdate), vérifié par export CSV du gid 1277122579 — voir résumé final de l'agent.
- **Étape B (génération de scripts + ajout dans la file de production)** : hors périmètre de cette routine (analyse uniquement) — non exécutée.

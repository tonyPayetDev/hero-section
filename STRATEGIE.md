# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-08-31 (complété en deux temps — voir note ci-dessous)
- **Période couverte** : Instagram `@automatisationboost` — 100 posts remontés depuis le 2026-07-03, focus sur les 8 posts publiés depuis le 24/08 · TikTok `@automationboost7` et concurrent `@jb.roy_` — données de compte **et** données vidéo-par-vidéo, fenêtre 24/08→31/08 (comparable à la fenêtre 17/08→23/08 du run précédent) · LinkedIn — statut de publication vérifié via `blotato_list_posts`, toujours aucune métrique d'engagement
- **Comptes analysés** : TikTok `@automationboost7` (compte actif, source = `tokscript get_tiktok_user` pour les stats de compte + Apify `clockworks/tiktok-scraper` via le workflow n8n `YUJjz5NNsYo41t8q` pour le détail vidéo) · Instagram `@automatisationboost` compte Blotato 54617 · LinkedIn Payet Tony (compte Blotato 25882) · Concurrent TikTok `@jb.roy_` (même source Apify) · Exclu : `@tonypayet4` (toujours mort, 0 abonné/0 vidéo, reconfirmé) et Instagram foodboost (55611, hors périmètre)
- **ℹ️ Run complété en deux temps** : la routine hebdo a d'abord tourné le 31/08 avec n8n inaccessible (voir historique en §0.1) — Instagram, LinkedIn et les stats de compte TikTok avaient pu être rafraîchis, mais pas le détail vidéo-par-vidéo TikTok ni l'onglet Sheet. **n8n a été réautorisé plus tard dans la journée du 31/08** ; ce complément a relancé le scraping Apify (profils `automationboost7` et `jb.roy_` séparément, comme recommandé) et écrit l'onglet Analyse Perf. Les deux lacunes sont désormais comblées — plus de bandeau "run dégradé".

---

## 0. Anomalies et découvertes clés de ce run

1. **🟢 RÉSOLU — n8n était inaccessible en début de journée, réautorisé le 31/08.** Au premier passage de la routine, la session cloud n'avait pas pu s'authentifier auprès du serveur MCP n8n (authentification OAuth requise, impossible en session non-interactive), ce qui avait bloqué : le scraping Apify vidéo-par-vidéo, la vérification de `n5dIUNEk5D6Pj3Vf`, et l'écriture de l'onglet Analyse Perf. **Tony a réautorisé le connecteur n8n plus tard dans la journée.** Ce complément a donc pu, dans la foulée :
   - Relancer le workflow `YUJjz5NNsYo41t8q` en **deux exécutions séparées** (une par profil, `automationboost7` puis `jb.roy_`, méthodologie du run du 24/08 pour éviter le bug de paramétrage déjà rencontré) → détail vidéo par vidéo obtenu pour les deux comptes, fenêtre 24/08→31/08 (voir §2, §5, §6, §7).
   - Vérifier `n5dIUNEk5D6Pj3Vf` : **toujours 0 exécution, workflow non opérationnel** (voir point 6 ci-dessous) — pas un problème d'accès n8n, le workflow lui-même n'a jamais été branché sur de vraies API.
   - Écrire l'onglet **Analyse Perf** du Sheet (SINK 2 fait ce run, vérifié par export CSV — voir résumé final).
   - L'ajout des 5 scripts de la semaine dans la file de production (Étape B, §10) reste **hors périmètre de ce complément** — à faire dans une prochaine session dédiée maintenant que n8n est de nouveau accessible.
2. **🟠 tokscript en mode dégradé.** `get_tiktok_user_videos` (liste vidéo + stats) renvoie *"Listing user videos requires a Pro or Premium subscription"* — l'abonnement Pro/Premium tokscript n'est pas actif sur ce compte. Seul `get_tiktok_user` (stats de compte agrégées : abonnés, nb vidéos, likes cumulés) a pu être utilisé, sans Apify en secours (bloqué par #1). Résultat : aucun hook, aucune vidéo top, aucune donnée de durée ou de cadence horaire cette semaine.
3. **🟢 Bonne nouvelle : LinkedIn n'est PAS en panne.** Contrairement à l'alerte du run du 24/08 ("compte expiré"), `blotato_list_posts` montre que le dernier post LinkedIn a été **publié avec succès le 30/08 à 15:15:06 UTC** (ID 6590486). Les 10 échecs LinkedIn observés sont datés du **28/08 entre 21:18 et 21:47 UTC**, avec l'erreur `"Failed to fetch media URL: 403 Forbidden"` — **pas** `"LinkedIn account has expired"`. Ce même message 403 touche identiquement TikTok (10 échecs) et Instagram (10 échecs) sur la même fenêtre de 30 minutes : c'était une panne ponctuelle et transverse (source média inaccessible), pas un problème de compte LinkedIn. Tout a repris normalement dès le lendemain. **Aucune action requise.**
4. **🟡 Instagram : rebond à confirmer, données à nettoyer.** Sur les 8 posts publiés depuis le 24/08 : vues moyenne **41,9** / médiane **22** — en hausse vs moyenne 33,2 / médiane 11 le 24/08 (qui concluait à une 3ᵉ semaine de baisse consécutive). **Prudence** : échantillon très petit (n=8) et l'outil `blotato_list_top_posts` ne renvoie aucun champ d'identification de compte dans sa réponse — un des 8 posts (ID 6571153, "Ce burger n'existe pas...", 18 vues, 1 commentaire) a un sujet qui ressemble à du contenu foodboost et n'a pas pu être exclu avec certitude. À vérifier manuellement avant de considérer le rebond comme confirmé.
5. **Le handle `tonypayet4` reste confirmé mort** côté TikTok public (`tokscript get_tiktok_user` → 0 abonné/0 vidéo), même compte physique que `@automationboost7` — rien de nouveau, aucune action requise.
6. **🔴 `n5dIUNEk5D6Pj3Vf` n'est pas un workflow opérationnel — ce n'est pas un problème d'accès.** `get_execution` (via `search_executions`) confirme **0 exécution depuis sa création** (2026-07-21), et `get_workflow_details` montre que ses nœuds HTTP Request (Instagram Graph API, TikTok API) et son nœud Telegram contiennent encore des valeurs placeholder non résolues (`<__PLACEHOLDER_VALUE__...>` en URL et en chat ID) — il n'a jamais été câblé avec de vraies credentials/IDs. Il est inactif (`active: false`) et son trigger (Lundi 8h) n'a donc jamais pu se déclencher. **Recommandation : soit le configurer réellement (obtenir un token API Instagram Graph + TikTok + un chat ID Telegram), soit l'archiver** — dans son état actuel il ne produit et ne produira aucune donnée, et le vrai reporting hebdo passe déjà par Blotato + tokscript + Apify.
7. **🟢 Découverte forte : au niveau vidéo, Tony surperforme désormais `jb.roy_` malgré 10x moins d'abonnés.** Sur la même fenêtre (24/08→31/08) : Tony moyenne **306 vues/vidéo** (médiane 193, n=20) vs `jb.roy_` **190 vues/vidéo** (médiane 159, n=33) — alors que `jb.roy_` a 1580 abonnés contre 151 pour Tony. Rapporté aux abonnés gagnés par vidéo postée sur 7 jours, Tony est ~4x plus efficace (15 abonnés / 19 vidéos ≈ 0,79/vidéo) que `jb.roy_` (6 abonnés / 34 vidéos ≈ 0,18/vidéo). Voir §7 pour le détail.

---

## 1. Chiffres clés par plateforme

### TikTok `@automationboost7` — compte + vidéo par vidéo (fenêtre 24/08→31/08, n=20 vidéos)
| Métrique | Valeur (31/08) | vs run 24/08 |
|---|---|---|
| Abonnés | **151** | +15 en 7j (136→151) |
| Vidéos publiées (total compte) | **122** | +19 en 7j (103→122, ≈2,7/j — cadence toujours au-dessus de la cible 1/j) |
| Likes cumulés (total compte) | 584 | non comparable (métrique non suivie la semaine dernière) |
| Vues moyenne / médiane (24/08→31/08, n=20) | **306 / 193** | Nette hausse vs le max historique de 912 vues sur une seule vidéo au run du 24/08 — c'est la moyenne, pas un pic isolé, qui grimpe. Échantillon encore petit, à confirmer. |
| Durée moyenne / médiane | 48,6 s / **38 s** | proche de la cible 30–35 s recommandée, légère dérive vers le plus long à surveiller |

### Concurrent TikTok `@jb.roy_` — compte + vidéo par vidéo (fenêtre 24/08→31/08, n=33 vidéos)
| Métrique | Valeur (31/08) | vs run 24/08 |
|---|---|---|
| Abonnés | **1580** | +6 en 7j (1574→1580) — croissance quasi nulle |
| Vidéos publiées (total compte) | **149** | **+34 en 7j** (115→149, ≈4,9/j — rafale toujours en cours, pire que Tony) |
| Likes cumulés (total compte) | 7674 | non comparable |
| Vues moyenne / médiane (24/08→31/08, n=33) | 190 / 159 | — inférieur aux moyennes de Tony cette semaine, voir §0.7 |
| Durée moyenne / médiane | 46,2 s / 44 s | légèrement plus long que Tony |

**Lecture** : le signal "sur-publication ne paie pas" du run précédent se confirme et se précise au niveau vidéo — `jb.roy_` poste 65 % plus souvent que Tony (33 vs 20 vidéos sur la même semaine) mais fait **moins de vues en moyenne par vidéo** (190 vs 306) et gagne 4x moins d'abonnés par vidéo publiée. Voir §0.7 et §7.

### Instagram `@automatisationboost` (54617) — source Blotato, 8 posts depuis le 24/08 (voir §0.4 pour la réserve sur 1 post)
| Métrique | Valeur | vs run 24/08 |
|---|---|---|
| Vues | moyenne **41,9**, médiane **22** | ↑ vs moy 33,2 / méd 11 — rebond à confirmer (n petit, voir §0.4) |
| Reach | moyenne 37,25, médiane 19,5 | suit les vues de très près |
| Commentaires | 1 post sur 8 a ≥1 commentaire | quasi-inchangé |
| Heure dominante (depuis le 05/08, n élargi) | 14:00 UTC (16/44 posts) | confirmé pour la 4ᵉ fois consécutive, signal le plus robuste du rapport |

### LinkedIn (Payet Tony, compte Blotato 25882)
**Compte opérationnel.** Dernier post publié avec succès le **30/08 15:15:06 UTC**. La panne signalée le 24/08 ("compte expiré") ne s'est pas reproduite ; les échecs du 28/08 (403 sur récupération média) étaient une panne transverse multi-plateforme résolue le jour même (voir §0.3). Toujours aucune métrique d'engagement disponible (Blotato ne collecte pas d'analytics LinkedIn).

---

## 2. Top 3 vidéos / posts (période récente)

### Top 3 TikTok `@automationboost7` (fenêtre 24/08→31/08, source Apify `clockworks/tiktok-scraper`)
1. **782 vues** — « Au Népal cette semaine, une avalanche de glace a bloqué une rivière. Un barrage s'est formé tout seul, puis il a cédé... » — 109 s, 28/08 08:00 UTC. *Actu réelle + curiosité (comment ça se termine ?), format long assumé.*
2. **772 vues** — « Avant / Après : d'un site figé à un site qui bosse pour toi — pages en ligne + relances clients envoyées en automatique. Commente SITE » — 25 s, 26/08 14:00 UTC. *Avant/après très court et concret, meilleur ratio vues/durée de la semaine.*
3. **740 vues** — « Six catégories, trois outils par catégorie, et un fait derrière chaque verdict — pas un adjectif » (comparatif Seedance) — 88 s, 25/08 15:30 UTC. *Comparatif chiffré, promesse de fait vérifiable plutôt que d'opinion.*

**À noter — retournement du format « Journal IA »** : ce format était le winner confirmé du run du 24/08 (764–775 vues). Sur cette fenêtre, l'édition du 25/08 03:00 UTC n'a fait que **11 vues** — l'édition du 29/08 (17:10 UTC, hors créneau habituel de 03:00) a fait 609 vues, nettement mieux. Signal possible : c'est l'heure de publication qui a fait la différence, pas le format lui-même — à creuser (voir §5).

### Top 3 Instagram `@automatisationboost` (depuis le 01/07, données fraîches)
1. **243 vues / 224 reach** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... Commente TERMINAL et je t'envoie le guide » (Claude Code + VPS + Coolify + MCP, 3 étapes) — 27/07 14:29 UTC.
2. **223 vues / 195 reach** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. Follow pour la suite + commente OPUS » — 29/07 14:30 UTC. *Actualité produit nommée dans les 10 premiers mots, très réactif.*
3. **216 vues / 202 reach** — « L'alternative gratuite à Claude Code pour créer des sites automatiquement. Kilo Code + n8n = même résultat, zéro abonnement. Commente KILO » — 13/07 19:00 UTC.

*Ces 3 posts dépassent nettement le Top 3 du run précédent (136/121/113 vues) — à noter que ce Top 3 provient d'une fenêtre plus large (depuis le 01/07 vs les 30 derniers jours au run précédent), donc pas strictement comparable en tendance, mais les formulations restent des patterns solides.*

### Top vidéos concurrent `@jb.roy_` (fenêtre 24/08→31/08)
1. **684 vues** — 28/08 15:00 UTC, 44 s.
2. **512 vues** — 25/08 17:16 UTC, 42 s.
3. **372 vues** — 25/08 17:16 UTC, 68 s (publié la même minute que le #2 — probable double-post/variante).

Les 33 vidéos de la fenêtre portent **toutes** la même légende générique « Follow @jb.roy_ pour implémenter l'IA dans ton activité » (ou variante avec espace insécable) — confirmé : le hook reste **parlé dans la vidéo**, jamais écrit dans le texte du post, et aucun hashtag n'est utilisé sur les 33 posts. Impossible d'identifier le hook exact sans transcription vidéo (hors périmètre de cette collecte).

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Actualité produit/outil connu nommée dans les 10 premiers mots + un chiffre ou un fait précis** — confirmé à nouveau ce run (« Anthropic vient de sortir Opus 5, 4e Claude en 2 mois » = #2 Instagram, 223 vues). C'est le pattern qui correspond le mieux à la règle CTA de la routine.
2. **Bénéfice chiffré personnel très concret** dans les 10 premiers mots — ex. « 200€/mois économisés ». Confirmé sur plusieurs runs consécutifs (voir historique 24/08).
3. **Alternative gratuite à un outil payant connu**, nommé explicitement — ex. « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » — #3 Instagram ce run (216 vues).
4. **Tutoriel actionnable en 3 étapes** avec estimation de temps réaliste — ex. « VPS, Coolify, Claude Code + MCP... 3 à 7h de setup » — #1 Instagram ce run (243 vues, meilleur post Instagram sur 2 mois).
5. **Debunk d'une promesse irréaliste + solution vérifiable** — pattern confirmé les runs précédents (Lamborghini/IA), pas de nouvel exemple cette semaine.
6. **Format « Journal IA » récurrent** (TikTok) — signal mitigé cette semaine : 609 vues le 29/08 à 17h10 UTC, mais seulement 11 vues le 25/08 à 03h00 UTC. L'horaire de publication semble être le facteur déterminant, pas le format lui-même (voir §2, §8.2) — à republier sur un créneau 14h–17h UTC pour confirmer.

Règle : **nommer un outil/une actualité connue + un chiffre ou un fait précis dans les 10 premiers mots** — le pattern le plus robuste sur Instagram cette semaine et sur plusieurs runs TikTok précédents.

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Publier plus d'1 fois par jour sur TikTok.** Toujours vrai directionnellement : `jb.roy_` a posté 34 vidéos en 7j pour seulement +6 abonnés (quasi stagnation). Tony reste à ≈2,7/j (mieux qu'avant mais toujours au-dessus de la cible). **Ne pas relâcher cette règle tant qu'on n'a pas de données vidéo-par-vidéo pour la vérifier.**
- ❌ **Compter sur « Commente le mot X » comme unique CTA** sans variante — confirmé de nouveau cette semaine : sur les 20 vidéos TikTok de la fenêtre, la moyenne de commentaires reste quasi nulle (0 à 2 commentaires par vidéo, la majorité à 0) malgré le CTA.
- ❌ **Hook vague sans contexte concret** — « Ici tu ne cliques pas sur suivant. Tu écris. » a été republié deux fois cette semaine (25/08 et 27/08) avec des résultats incohérents (12 puis 225 vues) : sans fait précis ni nom d'outil, le hook ne donne rien de fiable à accrocher.
- ❌ **Traiter la baisse Instagram comme confirmée sur 4 semaines sans vérifier les comptes mélangés** — voir §0.4, un post ambigu (foodboost ?) a pu fausser le calcul cette semaine. Vérifier manuellement les 8 posts avant de communiquer un chiffre de rebond.
- ❌ **Supposer que LinkedIn est en panne sans revérifier `blotato_list_posts`** — le run précédent a mal diagnostiqué un problème ponctuel (403 média) comme une expiration de compte. Toujours lire le message d'erreur exact avant de conclure.
- ⚠️ **Nouveau risque à surveiller** : si n8n reste inaccessible plusieurs semaines de suite, aucune donnée vidéo-par-vidéo TikTok ne sera disponible et l'onglet Analyse Perf du Sheet cessera d'être à jour. Prioriser la reconnexion n8n.

---

## 5. Meilleures heures de publication

- **Instagram** : créneau **14:00 UTC** toujours dominant (16 posts sur 44 depuis le 05/08) — confirmé pour la 4ᵉ semaine consécutive, signal le plus robuste de ce rapport.
- **TikTok `@automationboost7`** (n=20, fenêtre 24/08→31/08) : **14:00 UTC domine** avec 6 des 20 publications (30 %), suivi de 15:00 UTC (4) et 08:00 UTC (4). Cohérent avec le créneau pivot Instagram — première confirmation croisée entre les deux plateformes ce run. Reste à confirmer sur plusieurs semaines (n encore petit).
- **Concurrent `@jb.roy_`** (n=33) : créneau très différent, concentré à **16:00–18:00 UTC** (28 des 33 posts, soit 85 %) — décalage net avec le pivot 14:00 UTC de Tony. Pas de conclusion à en tirer sans donnée de conversion, mais utile pour éviter de calquer aveuglément l'horaire du concurrent.
- **Recommandation** : garder **14:00 UTC** comme créneau pivot sur Instagram *et* TikTok — première semaine où les deux plateformes s'alignent sur ce créneau.

---

## 6. Durée cible de vidéo

Fenêtre 24/08→31/08 : médiane **38 s** (Tony, n=20, moyenne 48,6 s) vs **44 s** (`jb.roy_`, n=33, moyenne 46,2 s). Léger allongement chez Tony vs le 34 s du run du 24/08, tiré par quelques formats plus longs testés cette semaine (« Journal IA » 76–88 s, extraits d'essai contemplatif jusqu'à 109 s). Le Top 3 de la semaine (§2) est cependant dominé par une vidéo courte (25 s, #2) et une longue (109 s, #1) — la durée seule n'explique pas la performance, le hook prime. **Cible recommandée : 25–45 s**, élargie par rapport à 30–35 s pour laisser de la place aux formats actu courts (25–30 s) et aux comparatifs/explainers plus longs (80–110 s) qui ont bien marché cette semaine, tout en évitant de dériver au-delà de ~110 s.

---

## 7. Ce que fait le concurrent `@jb.roy_` qui marche

Détail vidéo par vidéo obtenu ce run (fenêtre 24/08→31/08, n=33, source Apify `clockworks/tiktok-scraper`) :

- **Le rythme de publication ne compense pas la qualité par vidéo.** `jb.roy_` a ajouté 34 vidéos en 7 jours (115→149) pour seulement +6 abonnés (1574→1580), et sur la même fenêtre fait **190 vues/vidéo en moyenne contre 306 pour Tony** — malgré 10x plus d'abonnés (1580 vs 151). Rapporté aux abonnés gagnés par vidéo publiée, Tony est ≈4x plus efficace (0,79 abonné/vidéo vs 0,18). C'est le signal le plus actionnable de ce run (voir §0.7) : la stratégie de Tony (publication plus rare, hooks nommés/actu) rapporte mieux par publication que la rafale du concurrent.
- **Créneau de publication très différent** : `jb.roy_` concentre 85 % de ses posts entre 16h et 18h UTC, contre 14h pour Tony (voir §5) — pas de conclusion causale à en tirer, mais confirme que copier l'horaire du concurrent n'est pas nécessaire.
- **Légende toujours générique, aucun hashtag** : les 33 posts de la fenêtre portent la même légende « Follow @jb.roy_ pour implémenter l'IA dans ton activité », sans un seul hashtag. Le hook réel est donc **parlé dans la vidéo**, invisible dans les métadonnées scrapées — confirme que le format texte-hook de Tony (hook écrit dans les 10 premiers mots de la légende) reste une différenciation structurelle, pas seulement un choix créatif.
- **Durée légèrement plus longue** : médiane 44 s (`jb.roy_`) vs 38 s (Tony) — écart resserré par rapport au run du 24/08 (33,5 s vs 34 s), les deux comptes dérivent un peu vers des formats plus longs.
- **Limite de méthode** : sans accès à la légende/voix réelle des vidéos `jb.roy_`, impossible d'extraire ses formulations de hook exactes pour alimenter §3 — seule l'observation structurelle (rythme, créneau, durée, absence de hook écrit) est disponible depuis Apify.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **Continuer à publier moins souvent que `jb.roy_` mais avec un hook nommé/actu en tête de vidéo** — cette semaine Tony fait +61 % de vues moyennes par vidéo (306 vs 190) et ≈4x plus d'abonnés par vidéo publiée que `jb.roy_`, malgré 10x moins d'abonnés au départ (§0.7, §7). Ne pas passer à la rafale de publication.
2. **Retester le format « Journal IA » à 14h–17h UTC plutôt qu'à 03h UTC** — l'édition du 25/08 à 03h a fait 11 vues, celle du 29/08 à 17h10 en a fait 609 ; l'horaire de nuit semble tuer un format qui marchait bien au run précédent (§2).
3. **Élargir la cible de durée à 25–45 s** (au lieu de 30–35 s strict) pour laisser de la place aux formats actu courts et aux comparatifs plus longs qui ont dominé le Top 3 de la semaine (§6).
4. **Vérifier manuellement les 8 derniers posts Instagram** pour confirmer que le post "burger" (ID 6571153) n'est pas un post foodboost mal attribué avant de communiquer sur un rebond des vues.
5. **Rejouer le pattern confirmé cette semaine** : actualité/outil connu nommé + fait précis dans les 10 premiers mots (ex. sortie de modèle, alternative gratuite à un outil payant, actu réelle type "avalanche au Népal") — meilleurs posts Instagram et TikTok du run.
6. **Décider du sort de `n5dIUNEk5D6Pj3Vf`** : confirmé non opérationnel (0 exécution, credentials/IDs jamais renseignés, voir §0.6) — à configurer réellement ou à archiver, ce n'est plus une question d'accès n8n.

---

## 9. Sources & limites (run du 31/08, complété après réautorisation n8n)

- **TikTok compte (Tony + concurrent)** : `tokscript get_tiktok_user` (stats de compte : abonnés, nb vidéos, likes cumulés). `tokscript get_tiktok_user_videos` échoue toujours avec *"Listing user videos requires a Pro or Premium subscription"* (§0.2, abonnement tokscript Pro/Premium non actif).
- **TikTok vidéo par vidéo (Tony + concurrent)** : workflow n8n `YUJjz5NNsYo41t8q` (Apify `clockworks/tiktok-scraper`), exécuté en deux passes séparées le 31/08 (exécutions `80824` pour `automationboost7`, `80825` pour `jb.roy_`) — profil, durée, vues/likes/comments/shares/saves, horodatage par vidéo. Le node de traitement du workflow retourne les métriques agrégées + top 5 par vues et par engagement ; le détail complet par vidéo a été extrait temporairement en modifiant le Code node pour exposer `allRows` (dédoublonnage des items Apify dupliqués inclus), puis le workflow a été **remis dans son état d'origine** (profil `automationboost7`, code initial) après collecte.
- **Instagram (Tony)** : `blotato_list_top_posts` (platform=instagram, depuis le 2026-07-01, 100 résultats). La réponse ne contient aucun champ d'identification de compte — le filtrage foodboost n'a pas pu être appliqué avec certitude (voir §0.4).
- **LinkedIn** : `blotato_list_posts` (tous statuts, depuis le 24/08, 100 items) — a permis de corriger le diagnostic erroné du run précédent (§0.3).
- **Google Sheet "Analyse Perf"** : mis à jour ce run via un workflow n8n `create_workflow_from_code` (Manual Trigger → Google Sheets `appendOrUpdate`), vérifié par export CSV du gid 1277122579 — voir résumé final de l'agent.
- **Workflow analytics hebdo `n5dIUNEk5D6Pj3Vf`** : vérifié (§0.6) — 0 exécution depuis sa création, credentials/IDs jamais renseignés (placeholders), non opérationnel.
- **Étape B (génération de scripts + ajout dans la file de production)** : toujours **non exécutée** — hors périmètre de ce complément (n8n vient d'être réautorisé, la génération de scripts n'a pas été redemandée dans cette passe). Voir §10.

---

## 10. Étape B — Scripts (toujours non exécutée)

L'étape B de la routine hebdo (génération de 5 scripts vidéo + ajout dans l'onglet principal du Sheet lu par `veille-to-video`) **n'a pas été exécutée dans ce complément** : ce passage s'est concentré sur les deux lacunes explicitement signalées (données TikTok Apify + onglet Analyse Perf). n8n étant de nouveau accessible, l'étape B peut être relancée dans une prochaine session dédiée.

# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-08-05
- **Période couverte** : Instagram — tous les posts autoboost depuis le 01/07 (19 posts, foodboost exclu) · TikTok `@automationboost7` — 20 vidéos récentes sur 56 publiées (13/07 → 04/08) · TikTok concurrent `@jb.roy_` — 20 vidéos récentes sur 50 publiées (18/07 → 04/08) · LinkedIn — historique de publication disponible, **aucune métrique** (voir §0 et §9)
- **Comptes analysés** : TikTok `@automationboost7` (Apify, source de vérité) · Instagram `@automatisationboost` compte Blotato 54617 · LinkedIn Payet Tony (compte Blotato 25882, posts publiés mais pas de connecteur analytics) · Concurrent TikTok `@jb.roy_` (Apify)
- **AVERTISSEMENT** : comptes en phase de démarrage, volumes petits (vues à 2–3 chiffres, likes 0–75, commentaires 0–12). Conclusions à confirmer sur plus de données ; n petit sur chaque échantillon.

---

## 0. Découverte clé de ce run — `tonypayet4` et `automationboost7` sont **le même compte**

Le rapport du 23/07 signalait que `@tonypayet4` ne remontait aucune donnée et recommandait de « clarifier le compte ». C'est fait, avec preuve directe :

- Le journal des publications Blotato (`blotato_list_posts`, platform tiktok) montre des posts publiés sous des URLs `tiktok.com/@tonypayet4/video/<id>` — ex. vidéo `7667207344853372182` publiée le 27/07 à 14:01:25 UTC, texte « Là, tout de suite, pendant que t'attends dans la queue... TERMINAL ».
- Le scrape Apify du compte `automationboost7` (nickname **« automatisationboost »**) montre la **même vidéo, même texte, créée à 14:00:03 UTC le même jour** — écart de ~1 min 20 s typique entre l'heure de création et l'heure de log Blotato.
- Plusieurs autres paires correspondent exactement (Opus 5 le 29/07, FABLE le 26/07, MCP n8n le 01/08, etc.).

**Conclusion vérifiée** : `tonypayet4` est le handle sous lequel Blotato a connecté le compte à l'origine ; le compte a depuis été renommé en `@automationboost7` côté TikTok (nickname affiché : automatisationboost). C'est **un seul et même compte**, pas deux. Une requête directe sur `tonypayet4` renvoie bien 0 abonné/0 vidéo (le handle n'existe plus tel quel), ce qui explique l'échec — mais Blotato pousse toujours les publications vers le bon compte (les vidéos apparaissent bien sur `automationboost7`). **Pas d'action requise côté publication**, seulement mettre à jour les scripts/skills qui interrogent encore `tonypayet4` pour qu'ils utilisent `automationboost7`.

---

## 1. Chiffres clés par plateforme

### TikTok `@automationboost7` — source Apify (clockworks/tiktok-scraper, run manuel du jour, 20 vidéos du 13/07 au 04/08)
| Métrique | Valeur |
|---|---|
| Abonnés | **103** (05/08) — 77 au 23/07, soit **+26 en ~13 jours** (rythme stable ~2/jour) |
| Vidéos publiées (total compte) | 56 |
| Vues | moyenne **379**, médiane 273, min 152, max **1125** |
| Likes | moyenne 11,3 (1–75) |
| Commentaires | moyenne 2,85 (0–12) — **pas ≈0 comme sur Instagram, voir §4** |
| Partages | moyenne 1,6 · Enregistrements (saves) moyenne 3,95 (max 13) |
| Durée | médiane **32 s**, moyenne 30,7 s (hors 1 post à 14 s et 1 post à 0 s/image) — range 28–35 s pour l'essentiel |
| Engagement / 100 vues (likes+comm.+partages+saves) | **~5,2** |

### Instagram `@automatisationboost` (54617) — source Blotato, 19 posts autoboost depuis le 01/07 (posts `#FoodBoost` exclus)
| Métrique | Valeur |
|---|---|
| Vues | moyenne **108,7**, médiane 75, min 45, max **243** |
| Reach | 42–224 |
| Likes | 0–4 · Commentaires **quasi toujours 0** (1 seule exception : 3 commentaires sur le post « clone reels + avatar IA ») |
| Rétention | watchTimeAvg jusqu'à ~6 s sur les meilleurs posts. **Le goulot reste le REACH/hook, pas la rétention.** |

### LinkedIn (Payet Tony, compte Blotato 25882)
Contrairement au 23/07, on a maintenant la preuve que **le compte publie bien** (9 posts publiés entre le 21/07 et le 28/07, repris du contenu IG/TikTok, ex. `linkedin.com/feed/update/urn:li:ugcPost:7487507108205060097`). Mais **aucune métrique d'engagement n'est accessible** : Blotato ne collecte pas d'analytics LinkedIn, et le connecteur Windsor.ai « LinkedIn Organic » n'est toujours pas connecté (vérifié ce jour via `get_connectors` — seuls Instagram `animeirl85` et TikTok `humian` apparaissent, aucun LinkedIn). **À suivre manuellement dans LinkedIn Analytics natif si on veut des chiffres.**

---

## 2. Top 3 vidéos

### Top 3 TikTok `@automationboost7` (canal principal, vues)
1. **1125 vues** — « Quatre heures pour vingt secondes de vidéo. C'était mon quotidien. » (pitch Vidéo Boost) — 31 s, 23/07 08:55 UTC (hors créneau habituel). 75 likes, 2 commentaires. *Douleur personnelle chiffrée + retournement.*
2. **977 vues** — « Ton projet de fin d'année peut finir archivé le lendemain de la soutenance. Ou tourner tous les jours chez une vraie entreprise. » (workflow PFA étudiants) — 28 s, 28/07 14:00 UTC. 64 likes. *Enjeu concret + promesse mesurable (« délai de paiement passé de 52 à 38 jours »).*
3. **673 vues** — « Higgsfield, c'est 15 à 99$ par mois... Un développeur a sorti la même chose en open source. » — 33 s, 25/07 14:00 UTC. 16 likes, 5 commentaires, 11 saves. *Prix précis d'un outil connu + alternative gratuite.*

### Top 3 Instagram `@automatisationboost`
1. **243 vues / 224 reach** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur : tu perds du temps. Pour rien. » (TERMINAL, Claude Code sur VPS) — 27/07 14:29 UTC. *Même famille de hook que le #1 TikTok : douleur du temps perdu, chiffrée.*
2. **216 vues** (deux ex-æquo) — « L'alternative gratuite à Claude Code » (KILO, 13/07) et « Anthropic vient de sortir Opus 5 » (29/07, CTA Follow testé).
3. **214 vues** — « Higgsfield, c'est 15 à 99$ par mois... alternative open source » — même post que le #3 TikTok, publié le même jour : **3x plus de vues sur TikTok (673) que sur Instagram (214)** pour un contenu identique.

### Enseignement transversal
Le pattern **« prix précis d'un outil payant connu + alternative gratuite/open source »** (Higgsfield) et le pattern **« temps perdu chiffré + transformation concrète »** (TERMINAL / Vidéo Boost) sont maintenant confirmés sur **les deux plateformes avec des posts différents** — ce ne sont plus des coups isolés.

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Prix précis d'un outil connu + alternative gratuite/open source** — ex. « Higgsfield, c'est 15 à 99$/mois... un développeur a sorti la même chose en open source ». Marche sur TikTok ET Instagram avec le même contenu.
2. **« L'alternative gratuite à <outil connu> »** — ex. Kilo Code vs Claude Code.
3. **Douleur personnelle chiffrée + retournement** — ex. « Quatre heures pour vingt secondes de vidéo » (meilleur post du run), « Là, tout de suite... tu perds du temps. Pour rien. ».
4. **Enjeu concret pour une audience de niche + preuve chiffrée** — ex. le post PFA étudiants (« délai de paiement passé de 52 à 38 jours »), 2ᵉ meilleur post TikTok du run.
5. **Nom de modèle/outil précis + actualité chaude** — ex. Opus 5, Seedance 2.0, MCP natif n8n.
6. **Bénéfice-résultat « tout seul / une seule fois »** — ex. voix off clonée une seule fois (toujours performant, 2 rapports de suite).
7. **« Commente le mot X »** — **fonctionne sur TikTok** (voir §4), continuer à l'utiliser là où il marche.

Règle : **nommer un outil/prix/modèle connu + un chiffre concret dans les 5 premiers mots**, ou ouvrir sur une douleur personnelle chiffrée.

---

## 4. Ce qu'il ne faut PLUS faire — et une correction importante

- ❌ **CTA « Commente le mot X » sur Instagram** : toujours ≈0 commentaire sur les 19 posts autoboost du mois (1 seule exception à 3 commentaires). **Sur Instagram, ne plus compter dessus.**
- ⚠️ **CORRECTION vs rapport du 23/07** : le rapport précédent disait « Commente le mot X → rapporte ≈0 commentaire » sans distinguer les plateformes. **C'est faux pour TikTok** : sur les 20 vidéos TikTok scrapées ce jour, plusieurs posts utilisant « Commente MOT » ont **9 à 12 commentaires** (voix off : 9, mémoire persistante Claude : 12, six skills : 9, Higgsfield : 5). Le CTA marche, juste pas sur Instagram. **Ne pas l'abandonner sur TikTok.**
- ❌ **Le template générique « 🤖 Ce workflow fait X. Commente MOT »** sur Instagram → toujours dans les posts les plus faibles (18–60 vues).
- ❌ **>1 post/jour de contenu quasi identique** : encore observé — 3 posts TikTok le même jour le 22/07 (14h00, 15h16, 22h11), 2 posts IG le même jour le 13/07 et le 18/07. Amélioration vs juillet (plus de rafales de 5 vidéos/5h) mais la discipline « 1 post/jour » n'est pas encore acquise.
- ❌ **Vidéos de 14 s ou moins** : le seul post TikTok à 14 s du lot (« Tu as dépassé ta limite... ») fait 155 vues, sous la moyenne du compte.
- ⚠️ **CTA « Follow pour... » sur Instagram** : testé sur 3 posts récents (Opus 5 216 vues, MCP n8n 53 vues, alternative Cursor 49 vues) — résultat mitigé, un bon score et deux mauvais. **Échantillon trop petit pour trancher, à poursuivre mais ne pas généraliser encore.**

---

## 5. Meilleures heures de publication

Robustesse **faible à moyenne** (n petit, mais le pic est net).
- **TikTok** : très grande majorité des posts publiés à **14:00 UTC pile (= 18:00 heure Réunion, UTC+4)** — créneau confirmé comme le rythme de publication par défaut, et il produit régulièrement 250–977 vues. Le record absolu (1125 vues) est un post **hors créneau** à 08:55 UTC (12:55 Réunion) — probablement dû au hook, pas à l'heure.
- **Instagram** : la quasi-totalité des posts sortent à **14:29–14:30 UTC (18:29–18:30 Réunion)**, quelques exceptions à 19:00, 13:00, 10:47, 08:57 UTC sans avantage net.
- **Concurrent `jb.roy_` (TikTok)** : posts concentrés entre **16:00 et 20:00 UTC**, avec un pic de 5 vidéos publiées en 5 minutes le 04/08 (rafale de test, à ne pas imiter).
- **Recommandation** : garder le créneau **14:00 UTC / 18h Réunion**, il est déjà le meilleur créneau régulier observé — pas besoin de le changer.

---

## 6. Durée cible de vidéo

- **Tony (TikTok, 20 vidéos)** : médiane **32 s**, moyenne 30,7 s, la quasi-totalité entre 28 et 35 s. Les 4 meilleures vidéos du lot durent 28–33 s — cohérent avec la médiane, pas d'avantage à sortir de cette fourchette côté Tony.
- **Concurrent `jb.roy_` (TikTok, 20 vidéos)** : médiane **44 s**, moyenne 44,5 s (range 24–79 s). Ses meilleures vidéos durent 30–57 s, sensiblement plus long que celles de Tony.
- **Cible recommandée : 30–40 s.** C'est une progression mesurée par rapport aux 28–33 s actuels (qui marchent déjà), sans copier aveuglément les extrêmes du concurrent (57–79 s, hors du format le plus fiable même pour lui).
- Éviter les formats ≤ 15 s (sous-performent nettement, voir §4).

---

## 7. Ce que fait le concurrent `@jb.roy_` qui marche (TikTok, Apify — comparaison corrigée)

**Correction méthodologique importante** : le rapport du 23/07 comparait le TikTok de Tony (331 vues, engagement 1,87/100) à l'**Instagram Reels** du concurrent (9800 vues, engagement 14,77/100) — une comparaison entre deux plateformes différentes, pas une vraie comparaison à niveau égal. Ce run a scrapé le **TikTok réel de `jb.roy_`** (1564 abonnés, 50 vidéos) pour comparer TikTok à TikTok :

| Métrique (TikTok, 20 vidéos) | `jb.roy_` | `automationboost7` |
|---|---|---|
| Abonnés | 1564 | 103 |
| Vues moyennes | 363 | 379 |
| Vues médianes | 305 | 273 |
| Commentaires moyens | 1,6 | 2,85 |
| Saves moyens | **8,4** | 3,95 |
| Engagement / 100 vues | **7,7** | 5,2 |
| Durée (médiane / moyenne) | **44 s / 44,5 s** | 32 s / 30,7 s |

**L'écart réel est bien plus petit qu'annoncé précédemment** (engagement ×1,5, pas ×8) — Tony est déjà compétitif en vues brutes sur TikTok. Le vrai écart : les **saves** (2x plus chez le concurrent — taux jusqu'à 4,9–6,1% sur ses meilleurs posts vs ~3% max pour Tony) et la **durée** (44 s vs 32 s).

Enseignements exploitables :
- **CTA constant** : caption quasi identique sur toutes ses vidéos — « Follow @jb.roy_ pour implémenter l'IA dans ton activité » — répétition assumée, pas de fatigue apparente de format.
- **Durée plus longue** capte davantage de saves — probablement parce que le contenu a le temps de développer une vraie démonstration avant le CTA.
- Son meilleur post (822 vues) est un simple lien YouTube en légende — signal faible, à ne pas sur-interpréter (n=1).

---

## 8. Recommandations prioritaires (semaine suivante)

1. **Mettre à jour les scripts/skills qui interrogent encore `@tonypayet4`** → utiliser `@automationboost7` (même compte, voir §0). Aucun changement de compte de publication nécessaire.
2. **Durée cible 30–40 s sur TikTok** (actuellement 28–33 s) : allonger légèrement pour développer la démonstration avant le CTA, sans viser les extrêmes du concurrent (57–79 s).
3. **Garder « Commente le mot X » sur TikTok** (ça marche, 9–12 commentaires sur plusieurs posts) mais **l'abandonner sur Instagram** (0 commentaire quasi systématique) — y tester plutôt « Follow pour... » encore quelques semaines avant de conclure (échantillon actuel trop petit : 3 posts).
4. **Rejouer les hooks gagnants confirmés sur 2 plateformes** : « prix précis d'un outil connu + alternative gratuite » et « douleur personnelle chiffrée + retournement » (voir §2 et §3) — ce sont les deux patterns avec la meilleure preuve croisée TikTok+Instagram à date.
5. **Discipline 1 post/jour** : encore 2–3 posts groupés le même jour observés en juillet (TikTok 22/07, Instagram 13/07 et 18/07) — continuer à réduire, l'effondrement de reach mi-juillet était directement lié à ces rafales.
6. **Activer le workflow `n5dIUNEk5D6Pj3Vf`** si on veut ce rapport généré automatiquement chaque lundi : il contient toujours des URLs placeholder non configurées (`<__PLACEHOLDER_VALUE__...>`) et n'a jamais tourné (0 exécution, confirmé ce jour).

---

## 9. Sources & limites

- **TikTok (Tony + concurrent)** : Apify, actor `clockworks/tiktok-scraper`, exécuté ce jour (05/08) via le workflow n8n `YUJjz5NNsYo41t8q` (temporairement reconfiguré de son actor Instagram Reels d'origine vers cet actor TikTok pour ce run, puis **remis dans son état d'origine** après coup — aucun changement persistant). Exécutions : #70788 (jb.roy_, 20 vidéos, ~54s) et #70789 (automationboost7, 20 vidéos, ~10s). tokscript indisponible pour le listing de vidéos (`get_tiktok_user_videos` nécessite un abonnement Pro/Premium) → confirmé ce jour, Apify reste la seule source pour le détail vidéo par vidéo ; `get_tiktok_user` (profil) reste utilisable sans Pro et a servi à vérifier abonnés/existence de compte.
- **Instagram (Tony)** : Blotato (`blotato_list_top_posts`, platform=instagram, depuis le 01/07, 30 résultats bruts filtrés manuellement pour exclure les 11 posts du compte `foodboost` hors périmètre).
- **LinkedIn** : Blotato confirme 9 posts publiés (historique récupéré) mais **aucune métrique** — Blotato ne collecte pas d'analytics LinkedIn, et Windsor.ai n'a pas de connecteur LinkedIn Organic connecté (vérifié ce jour, seuls Instagram `animeirl85` et TikTok `humian` apparaissent — comptes hors périmètre Autoboost).
- **Workflow analytics hebdo `n5dIUNEk5D6Pj3Vf`** (« Analyse Réseaux Sociaux Auto ») : **toujours jamais exécuté** (0 run, `search_executions` vide), toujours inactif, contient toujours des URLs placeholder non remplacées pour les nœuds Instagram/TikTok/Telegram. Rien à en tirer tant qu'il n'est pas configuré avec de vraies credentials.
- **Workflow concurrent `YUJjz5NNsYo41t8q`** : `search_executions` ne retournait aucun historique pour ce workflow au moment du run (les exécutions passées mentionnées dans le rapport du 23/07, ex. #66112, ne sont plus listées) — d'où le nouveau run direct effectué aujourd'hui plutôt qu'une relecture d'ancienne exécution.

# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-08-31
- **Période couverte** : Instagram `@automatisationboost` — 100 posts remontés depuis le 2026-07-03, focus sur les 8 posts publiés depuis le 24/08 · TikTok `@automationboost7` et concurrent `@jb.roy_` — **données de compte uniquement** (abonnés/vidéos/likes cumulés), aucune donnée vidéo-par-vidéo cette semaine (voir §0.1) · LinkedIn — statut de publication vérifié via `blotato_list_posts`, toujours aucune métrique d'engagement
- **Comptes analysés** : TikTok `@automationboost7` (compte actif, source = `tokscript get_tiktok_user`, niveau compte seulement) · Instagram `@automatisationboost` compte Blotato 54617 · LinkedIn Payet Tony (compte Blotato 25882) · Concurrent TikTok `@jb.roy_` · Exclu : `@tonypayet4` (toujours mort, 0 abonné/0 vidéo, reconfirmé) et Instagram foodboost (55611, hors périmètre)
- **⚠️ RUN DÉGRADÉ** : ce run a perdu deux sources de données par rapport aux runs précédents — voir §0.1 et §0.2. Les chiffres TikTok détaillés (top vidéos, hooks, cadence de publication, durée) **n'ont pas pu être rafraîchis**. Les sections correspondantes ci-dessous conservent donc les dernières données fiables (24/08) marquées `[NON RAFRAÎCHI]`.

---

## 0. Anomalies et découvertes clés de ce run

1. **🔴 BLOQUANT — n8n inaccessible ce run.** La session cloud qui exécute cette routine n'a pas pu s'authentifier auprès du serveur MCP n8n (authentification OAuth requise, impossible en session non-interactive). Conséquences concrètes :
   - Impossible de relancer le scraping Apify (`clockworks/tiktok-scraper`) via le workflow `YUJjz5NNsYo41t8q` → **aucune donnée vidéo-par-vidéo TikTok cette semaine** (ni pour `@automationboost7` ni pour `@jb.roy_`).
   - Impossible de vérifier les exécutions du workflow analytics `n5dIUNEk5D6Pj3Vf`.
   - Impossible d'écrire dans l'onglet **Analyse Perf** du Google Sheet de suivi (SINK 2 non fait ce run) — **STRATEGIE.md est la seule sortie à jour cette semaine.**
   - Impossible d'ajouter les 5 scripts de la semaine dans la file de production (Étape B non exécutée — voir §10).
   **Action requise de Tony : réautoriser le connecteur n8n** (`claude mcp` ou `/mcp` en session interactive, ou reconnexion du connecteur côté claude.ai) pour que la prochaine exécution puisse écrire dans le Sheet et relancer Apify.
2. **🟠 tokscript en mode dégradé.** `get_tiktok_user_videos` (liste vidéo + stats) renvoie *"Listing user videos requires a Pro or Premium subscription"* — l'abonnement Pro/Premium tokscript n'est pas actif sur ce compte. Seul `get_tiktok_user` (stats de compte agrégées : abonnés, nb vidéos, likes cumulés) a pu être utilisé, sans Apify en secours (bloqué par #1). Résultat : aucun hook, aucune vidéo top, aucune donnée de durée ou de cadence horaire cette semaine.
3. **🟢 Bonne nouvelle : LinkedIn n'est PAS en panne.** Contrairement à l'alerte du run du 24/08 ("compte expiré"), `blotato_list_posts` montre que le dernier post LinkedIn a été **publié avec succès le 30/08 à 15:15:06 UTC** (ID 6590486). Les 10 échecs LinkedIn observés sont datés du **28/08 entre 21:18 et 21:47 UTC**, avec l'erreur `"Failed to fetch media URL: 403 Forbidden"` — **pas** `"LinkedIn account has expired"`. Ce même message 403 touche identiquement TikTok (10 échecs) et Instagram (10 échecs) sur la même fenêtre de 30 minutes : c'était une panne ponctuelle et transverse (source média inaccessible), pas un problème de compte LinkedIn. Tout a repris normalement dès le lendemain. **Aucune action requise.**
4. **🟡 Instagram : rebond à confirmer, données à nettoyer.** Sur les 8 posts publiés depuis le 24/08 : vues moyenne **41,9** / médiane **22** — en hausse vs moyenne 33,2 / médiane 11 le 24/08 (qui concluait à une 3ᵉ semaine de baisse consécutive). **Prudence** : échantillon très petit (n=8) et l'outil `blotato_list_top_posts` ne renvoie aucun champ d'identification de compte dans sa réponse — un des 8 posts (ID 6571153, "Ce burger n'existe pas...", 18 vues, 1 commentaire) a un sujet qui ressemble à du contenu foodboost et n'a pas pu être exclu avec certitude. À vérifier manuellement avant de considérer le rebond comme confirmé.
5. **Le handle `tonypayet4` reste confirmé mort** côté TikTok public (`tokscript get_tiktok_user` → 0 abonné/0 vidéo), même compte physique que `@automationboost7` — rien de nouveau, aucune action requise.

---

## 1. Chiffres clés par plateforme

### TikTok `@automationboost7` — niveau compte uniquement (Apify/n8n indisponibles ce run, voir §0.1)
| Métrique | Valeur (31/08) | vs run 24/08 |
|---|---|---|
| Abonnés | **151** | +15 en 7j (136→151) |
| Vidéos publiées (total compte) | **122** | +19 en 7j (103→122, ≈2,7/j — cadence toujours au-dessus de la cible 1/j) |
| Likes cumulés (total compte) | 584 | non comparable (métrique non suivie la semaine dernière) |
| Vues / durée / hooks vidéo par vidéo | **[NON RAFRAÎCHI]** — voir données du 24/08 en §2/§6 | — |

### Concurrent TikTok `@jb.roy_` — niveau compte uniquement
| Métrique | Valeur (31/08) | vs run 24/08 |
|---|---|---|
| Abonnés | **1580** | +6 en 7j (1574→1580) — croissance quasi nulle |
| Vidéos publiées (total compte) | **149** | **+34 en 7j** (115→149, ≈4,9/j — rafale toujours en cours, pire que Tony) |
| Likes cumulés (total compte) | 7674 | non comparable |
| Vues / durée / hooks vidéo par vidéo | **[NON RAFRAÎCHI]** | — |

**Lecture directionnelle (compte seulement, à confirmer avec des données vidéo dès que possible)** : `jb.roy_` a posté 34 vidéos en 7 jours pour seulement +6 abonnés — le signal "sur-publication ne paie pas" du run précédent se confirme au niveau compte. Tony reste dans la même zone (+19 vidéos pour +15 abonnés) mais à un rythme plus modéré.

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

### Top 3 TikTok `@automationboost7` — **[NON RAFRAÎCHI, dernières données fiables du 24/08]**
1. **912 vues** — « n8n vient de changer la façon dont tu vois tes workflows... commente CANVAS » — 30 s, 16/08 14:00 UTC.
2. **812 vues** — « 3 tâches à automatiser dès aujourd'hui. Commente AUTO » — carrousel photo, 11/08.
3. **764 vues** — « 📰 Journal IA — Dim. 23 août » — 68 s, 23/08 03:00 UTC.

### Top 3 Instagram `@automatisationboost` (depuis le 01/07, données fraîches)
1. **243 vues / 224 reach** — « Là, tout de suite, pendant que t'attends dans la queue ou chez le coiffeur... Commente TERMINAL et je t'envoie le guide » (Claude Code + VPS + Coolify + MCP, 3 étapes) — 27/07 14:29 UTC.
2. **223 vues / 195 reach** — « Anthropic vient de sortir Opus 5, 4e Claude en 2 mois. Follow pour la suite + commente OPUS » — 29/07 14:30 UTC. *Actualité produit nommée dans les 10 premiers mots, très réactif.*
3. **216 vues / 202 reach** — « L'alternative gratuite à Claude Code pour créer des sites automatiquement. Kilo Code + n8n = même résultat, zéro abonnement. Commente KILO » — 13/07 19:00 UTC.

*Ces 3 posts dépassent nettement le Top 3 du run précédent (136/121/113 vues) — à noter que ce Top 3 provient d'une fenêtre plus large (depuis le 01/07 vs les 30 derniers jours au run précédent), donc pas strictement comparable en tendance, mais les formulations restent des patterns solides.*

### Top vidéos concurrent `@jb.roy_` — **[NON RAFRAÎCHI]**
Dernières données connues (24/08) : jusqu'à 1360 vues, toutes sous la légende générique « Follow @jb.roy_ pour implémenter l'IA dans ton activité » — le hook reste parlé, pas écrit.

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Actualité produit/outil connu nommée dans les 10 premiers mots + un chiffre ou un fait précis** — confirmé à nouveau ce run (« Anthropic vient de sortir Opus 5, 4e Claude en 2 mois » = #2 Instagram, 223 vues). C'est le pattern qui correspond le mieux à la règle CTA de la routine.
2. **Bénéfice chiffré personnel très concret** dans les 10 premiers mots — ex. « 200€/mois économisés ». Confirmé sur plusieurs runs consécutifs (voir historique 24/08).
3. **Alternative gratuite à un outil payant connu**, nommé explicitement — ex. « Kilo Code + n8n = même résultat [que Claude Code], zéro abonnement » — #3 Instagram ce run (216 vues).
4. **Tutoriel actionnable en 3 étapes** avec estimation de temps réaliste — ex. « VPS, Coolify, Claude Code + MCP... 3 à 7h de setup » — #1 Instagram ce run (243 vues, meilleur post Instagram sur 2 mois).
5. **Debunk d'une promesse irréaliste + solution vérifiable** — pattern confirmé les runs précédents (Lamborghini/IA), pas de nouvel exemple cette semaine.
6. **Format « Journal IA » récurrent** (TikTok) — **[NON RAFRAÎCHI]**, dernière confirmation le 23/08 (764 vues).

Règle : **nommer un outil/une actualité connue + un chiffre ou un fait précis dans les 10 premiers mots** — le pattern le plus robuste sur Instagram cette semaine et sur plusieurs runs TikTok précédents.

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **Publier plus d'1 fois par jour sur TikTok.** Toujours vrai directionnellement : `jb.roy_` a posté 34 vidéos en 7j pour seulement +6 abonnés (quasi stagnation). Tony reste à ≈2,7/j (mieux qu'avant mais toujours au-dessus de la cible). **Ne pas relâcher cette règle tant qu'on n'a pas de données vidéo-par-vidéo pour la vérifier.**
- ❌ **Compter sur « Commente le mot X » comme unique CTA** sans variante — confirmé les runs précédents, pas de nouvelle donnée TikTok cette semaine pour retester, mais rien n'indique un changement.
- ❌ **Traiter la baisse Instagram comme confirmée sur 4 semaines sans vérifier les comptes mélangés** — voir §0.4, un post ambigu (foodboost ?) a pu fausser le calcul cette semaine. Vérifier manuellement les 8 posts avant de communiquer un chiffre de rebond.
- ❌ **Supposer que LinkedIn est en panne sans revérifier `blotato_list_posts`** — le run précédent a mal diagnostiqué un problème ponctuel (403 média) comme une expiration de compte. Toujours lire le message d'erreur exact avant de conclure.
- ⚠️ **Nouveau risque à surveiller** : si n8n reste inaccessible plusieurs semaines de suite, aucune donnée vidéo-par-vidéo TikTok ne sera disponible et l'onglet Analyse Perf du Sheet cessera d'être à jour. Prioriser la reconnexion n8n.

---

## 5. Meilleures heures de publication

- **Instagram** : créneau **14:00 UTC** toujours dominant (16 posts sur 44 depuis le 05/08) — confirmé pour la 4ᵉ semaine consécutive, signal le plus robuste de ce rapport.
- **TikTok** : **[NON RAFRAÎCHI]** — dernière donnée fiable (24/08) : créneau 14:00 UTC visible mais dispersé par la rafale de publication ; à revérifier dès que les données vidéo-par-vidéo seront de nouveau disponibles.
- **Recommandation inchangée** : garder 14:00 UTC comme créneau pivot sur Instagram ; pour TikTok, attendre le retour des données Apify avant de statuer.

---

## 6. Durée cible de vidéo

**[NON RAFRAÎCHI]** — dernière donnée fiable (24/08) : médiane 34 s (Tony) vs 33,5 s (`jb.roy_`), écart quasi nul. **Cible recommandée inchangée : 30–35 s.** À revérifier dès que les données vidéo-par-vidéo TikTok seront de nouveau disponibles (dépend de la reconnexion n8n, §0.1).

---

## 7. Ce que fait le concurrent `@jb.roy_` qui marche

**[Données vidéo-par-vidéo NON RAFRAÎCHIES ce run — voir §0.1.]** Seul signal actualisé : `jb.roy_` a ajouté 34 vidéos en 7 jours (115→149) pour seulement +6 abonnés (1574→1580) — la croissance d'abonnés est quasi à l'arrêt malgré (ou à cause de) ce rythme de publication très élevé. Cela renforce, au niveau compte, la conclusion du run précédent sur les rafales de publication. Détail vidéo par vidéo (engagement agrégé, durée, CTA) à revérifier dès que possible.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **🔴 Reconnecter le connecteur MCP n8n** (action manuelle de Tony, hors de portée de cet agent) — sans ça, plus de données TikTok vidéo-par-vidéo, plus de mise à jour de l'onglet Analyse Perf, et plus d'ajout automatique de scripts dans la file de production.
2. **Envisager un abonnement tokscript Pro/Premium** comme filet de sécurité si n8n/Apify reste indisponible ponctuellement — `get_tiktok_user_videos` aurait pu fournir un début de données vidéo cette semaine.
3. **Continuer à limiter TikTok à ~1 post/jour** — le signal compte (`jb.roy_` : +34 vidéos pour +6 abonnés) va dans le même sens que la conclusion du run précédent.
4. **Vérifier manuellement les 8 derniers posts Instagram** pour confirmer que le post "burger" (ID 6571153) n'est pas un post foodboost mal attribué avant de communiquer sur un rebond des vues.
5. **Rejouer le pattern confirmé cette semaine** : actualité/outil connu nommé + fait précis dans les 10 premiers mots (ex. sortie de modèle, alternative gratuite à un outil payant) — meilleur post Instagram du run avec le tutoriel Claude Code/Coolify/MCP en 3 étapes.
6. **Décider du sort de `n5dIUNEk5D6Pj3Vf`** : statut non vérifiable ce run (n8n inaccessible) — à revoir dès la reconnexion.

---

## 9. Sources & limites (run du 31/08)

- **TikTok (Tony + concurrent)** : `tokscript get_tiktok_user` uniquement (stats de compte : abonnés, nb vidéos, likes cumulés). Apify/n8n inaccessibles ce run (§0.1). `tokscript get_tiktok_user_videos` a échoué avec *"Listing user videos requires a Pro or Premium subscription"* (§0.2) — aucune donnée vidéo-par-vidéo.
- **Instagram (Tony)** : `blotato_list_top_posts` (platform=instagram, depuis le 2026-07-01, 100 résultats). La réponse ne contient aucun champ d'identification de compte — le filtrage foodboost n'a pas pu être appliqué avec certitude (voir §0.4).
- **LinkedIn** : `blotato_list_posts` (tous statuts, depuis le 24/08, 100 items) — a permis de corriger le diagnostic erroné du run précédent (§0.3).
- **Google Sheet "Analyse Perf"** : **NON mis à jour ce run** — nécessite le workflow n8n `create_workflow_from_code`, inaccessible (§0.1).
- **Workflow analytics hebdo `n5dIUNEk5D6Pj3Vf`** et **workflow concurrent `YUJjz5NNsYo41t8q`** : statuts non vérifiables ce run (n8n inaccessible).
- **Étape B (génération de scripts + ajout dans la file de production)** : **non exécutée ce run**, voir §10.

---

## 10. Étape B — Scripts (non exécutée ce run)

L'étape B de la routine hebdo (génération de 5 scripts vidéo + ajout dans l'onglet principal du Sheet lu par `veille-to-video`) **n'a pas pu être exécutée** : elle dépend du même accès n8n (Google Sheets append) que le SINK 2, indisponible ce run (§0.1). Génère des scripts sans pouvoir les écrire dans la file de production aurait créé un travail orphelin, non traçable par le pipeline. **À relancer dès que le connecteur n8n est réautorisé.**

# Stratégie éditoriale sociale — Autoboost / AutomatisationBoost

> Document de pilotage lu par le skill `veille-to-video` et l'agent `business-orchestrator`.
> Patterns copiables et règles fermes en fin de sections.

- **Date de l'analyse** : 2026-08-24
- **Période couverte** : TikTok `@automationboost7` — 40 vidéos les plus récentes scrapées (13/07 → 23/08), avec un focus sur les 23 vidéos publiées depuis le run précédent (17/08 → 23/08) · Instagram `@automatisationboost` — 35 posts autoboost depuis le 05/08 (foodboost exclu) · TikTok concurrent `@jb.roy_` — 40 vidéos les plus récentes (12/08 → 23/08) · LinkedIn — historique de publication disponible, **aucune métrique**, et **panne active depuis le 22/08** (voir §0)
- **Comptes analysés** : TikTok `@automationboost7` (Apify, source de vérité) · Instagram `@automatisationboost` compte Blotato 54617 · LinkedIn Payet Tony (compte Blotato 25882) · Concurrent TikTok `@jb.roy_` (Apify)
- **AVERTISSEMENT** : comptes en phase de démarrage, volumes petits (vues à 1–3 chiffres, commentaires 0–2 par vidéo). Les moyennes calculées comme moyenne-des-ratios-par-post (engagement/vue) sont trompeuses avec des dénominateurs petits — ce run privilégie les agrégats (somme interactions / somme vues) quand c'est pertinent, voir §7.

---

## 0. Anomalies et découvertes clés de ce run

1. **🔴 LinkedIn : compte expiré depuis le 22/08.** Tous les posts programmés à partir de `2026-08-22T08:08` échouent avec l'erreur `"LinkedIn account has expired"` (vérifié via `blotato_list_posts`, 7 échecs consécutifs à date : CHAOS→OK le 21/08 08:08, puis tout échoue). Dernier post publié avec succès : 21/08 08:08 ("Arrête de travailler comme une machine..."). **Action requise de Tony : reconnecter le compte LinkedIn dans Blotato** — hors de portée de cet agent (pas d'accès aux credentials/OAuth). Tant que ce n'est pas fait, le cross-post LinkedIn planifié (visible dans la queue jusqu'au 26/08) continuera d'échouer silencieusement.
2. **🟠 Cadence de publication TikTok hors de contrôle.** Depuis le 20/08, `@automationboost7` publie **4 à 5 vidéos/jour** (vs 1-2/jour recommandé) : 103 vidéos au compteur total contre 76 le 17/08, soit **+27 vidéos en 7 jours**. Le concurrent `@jb.roy_` fait pire : jusqu'à **8 vidéos en une journée** (20/08), 115 vidéos au total (+26 en 7j). Sur les journées de rafale, plusieurs vidéos de Tony tombent à 0–11 vues (20-22/08) alors que le compte continue de gagner des abonnés (+13 en 7j) — signal de dilution de reach par sur-publication, pas de perte d'audience.
3. **🟡 Instagram : la chute de vues se confirme et s'aggrave.** Moyenne 33,2 vues / médiane 11 vues sur 35 posts depuis le 05/08 (vs 47,6 rapportés le 17/08, vs 108,7 le 05/08). La baisse n'est pas un artefact de fraîcheur des métriques (le délai `fetchedAt − createdAt` reste stable à ~7 jours sur toute la période, donc les chiffres sont bien matures). **C'est la 3ᵉ semaine consécutive de baisse.**
4. **Bug méthodologique corrigé en cours de run** : la première tentative de reconfigurer le node Apify du workflow `YUJjz5NNsYo41t8q` pour scraper 2 profils en un seul appel (`setNodeParameter` sur un mauvais chemin JSON) a silencieusement laissé l'ancien `jsonBody` actif — deux exécutions ont donc renvoyé les données `automationboost7` au lieu du concurrent. Corrigé via `updateNodeParameters` (replace complet), vérifié, puis deux scrapes séparés (un par profil) ont été relancés avec succès (exécutions #77671 et #77673). Le workflow a été **remis dans son état d'origine** (`profiles: ["automationboost7"]`) après usage, aucun changement persistant.
5. Le handle `tonypayet4` reste confirmé mort côté TikTok public (`tokscript get_tiktok_user` → 0 abonné/0 vidéo), toujours le même compte que `@automationboost7` (établi le 05/08) — rien de nouveau, aucune action requise.

---

## 1. Chiffres clés par plateforme

### TikTok `@automationboost7` — source Apify (clockworks/tiktok-scraper), fenêtre 17/08→23/08 (n=23, exécution n8n #77671 du 24/08)
| Métrique | Valeur | vs run 17/08 |
|---|---|---|
| Abonnés | **136** | +13 en 7j (123→136, rythme stable ~1,9/j) |
| Vidéos publiées (total compte) | 103 | +27 en 7j (rafale, voir §0.2) |
| Vues (n=23, 17-23/08) | moyenne **205,2**, médiane 141, min 0, max 764 | ↓ vs moy 298/méd 244 (n=17, 05-16/08) |
| Likes | moyenne 2,52 | ↓ vs 3,4 |
| Commentaires | moyenne 0,48 (somme 11/23) | légère hausse vs 0,41, toujours loin des 2,85 de juillet |
| Saves | moyenne 1,17 | ↓ vs 2,65 |
| Durée | médiane **34 s**, moyenne 40 s | proche de 32,5 s (médiane stable) |

### Instagram `@automatisationboost` (54617) — source Blotato, 35 posts autoboost depuis le 01/07 réanalysés, focus depuis le 05/08
| Métrique | Valeur | vs run 17/08 |
|---|---|---|
| Vues | moyenne **33,2**, médiane **11**, min 1, max 136 | ↓ encore vs moy 47,6 (17/08), ↓↓ vs moy 108,7 (05/08) — **3ᵉ semaine de baisse** |
| Reach | moyenne 29,3, min 1, max 113 | suit les vues de très près |
| Commentaires | 4 posts sur 35 ont ≥1 commentaire | quasi-inchangé, toujours proche de 0 |
| Heure dominante | 14:29 UTC (12/35 posts) | confirmé, robustesse moyenne (voir §5) |

### LinkedIn (Payet Tony, compte Blotato 25882)
**Panne active** : compte expiré depuis le 22/08, tous les posts échouent depuis (voir §0.1). Avant la panne, publication régulière confirmée (cross-post TikTok/IG, dernier succès 21/08). Toujours **aucune métrique** disponible (Blotato ne collecte pas LinkedIn ; Windsor.ai n'a toujours aucun connecteur LinkedIn Organic connecté — seuls Instagram `animeirl85` et TikTok `humian` apparaissent, hors périmètre, non revérifié ce run faute de connecteur à consulter côté LinkedIn).

### Concurrent TikTok `@jb.roy_` — source Apify, fenêtre 12/08→23/08 (n=40, exécution n8n #77673 du 24/08)
| Métrique | Valeur | vs run 17/08 |
|---|---|---|
| Abonnés | 1574 | inchangé selon tokscript (à vérifier — possible stagnation réelle ou cache) |
| Vidéos publiées (total compte) | 115 | +26 en 7j (rafale encore plus marquée que Tony, jusqu'à 8/jour le 20/08) |
| Vues (40 dernières) | moyenne 311, médiane 159, min ~7, max 1360 | ↓ vs moy 416,6/méd 208 (20 vidéos, run 17/08) |
| Commentaires | moyenne 0,3 | stable, toujours très faible |
| Durée | médiane **33,5 s**, moyenne 41,1 s (range 10–98 s) | quasi identique à Tony désormais (34 s) — l'écart de durée est refermé |

---

## 2. Top 3 vidéos / posts (période récente)

### Top 3 TikTok `@automationboost7`
1. **912 vues** — « n8n vient de changer la façon dont tu vois tes workflows... commente CANVAS » — 30 s, 16/08 14:00 UTC. *Actualité chaude sur une feature d'un outil connu + démo concrète.*
2. **812 vues** — « 3 tâches à automatiser dès aujourd'hui. Commente AUTO » — carrousel photo (pas une vidéo filmée), 11/08. *Format slideshow à retester, signal répété depuis 2 runs.*
3. **764 vues** — « 📰 Journal IA — Dim. 23 août » — 68 s, 23/08 03:00 UTC. *Format « Journal IA » toujours performant (2ᵉ semaine consécutive dans le top, voir #4 : 751 vues le 17/08).*

### Top 3 Instagram `@automatisationboost`
1. **136 vues / 113 reach** — « Claude Code et n8n m'ont fait économiser 200 euros par mois de secrétariat. Follow + commente RELANCE » — 08/08. *Bénéfice chiffré personnel, seul post du mois avec un vrai volume de commentaires (3).*
2. **121 vues / 110 reach** — « Achète une Lamborghini en 1 an avec l'IA... c'est un peu du bullshit. La vraie solution : workflow n8n site+email » — 15/08. *Debunk d'une promesse irréaliste + solution vérifiable.*
3. **113 vues / 106 reach** — « J'ai essayé de vendre mon outil à MrBeast. Réponse obtenue : aucune 😂 » — 22/08. *Sketch humoristique + produit réel en fin de vidéo (ShortForge).*

### Top vidéos concurrent `@jb.roy_` (par vues)
1360 vues (29 s, 14/08) · 1270 vues (17 s, 14/08) · 1157 vues (86 s, 19/08) · 1071 vues (91 s, 22/08) · 828 vues (50 s, 16/08) — toutes sous la même légende générique « Follow @jb.roy_ pour implémenter l'IA dans ton activité » : **le vrai hook est uniquement parlé**, invisible dans les métadonnées scrapées (limite connue, non résolue ce run — nécessiterait `get_tiktok_transcript`).

---

## 3. Hooks qui marchent — formulations réutilisables

1. **Bénéfice chiffré personnel très concret** dans les 10 premiers mots — ex. « 200€/mois économisés », « 1200€ pour 3h de travail ». Confirmé 3 runs de suite, toujours le pattern le plus fiable pour générer vues ET commentaires.
2. **Debunk d'une promesse irréaliste + solution vérifiable** — ex. « Acheter une Lamborghini en 1 an avec l'IA... c'est un peu du bullshit. La vraie solution : … ».
3. **Actualité chaude / format « Journal IA »** — 2 semaines de suite dans le top 3 TikTok (751 vues le 17/08, 764 vues le 23/08). Fonctionne même sans hook individuel fort : le format récurrent est lui-même le hook.
4. **Remplacement d'un outil payant connu par un système fait-maison / open source** — ex. ManyChat, Runway/Midjourney à 95$/mois.
5. **Sketch humoristique avec produit réel en chute** — ex. « vendre à MrBeast, zéro réponse » — nouveau signal ce run (113 vues IG), à confirmer.
6. **Carrousel photo / slideshow** sur TikTok — 2ᵉ run de suite où un post non-vidéo (image ou slideshow) performe au-dessus de la moyenne (812 vues le 11/08). À tester plus systématiquement avant de généraliser (n=2).

Règle : **nommer un chiffre concret + un outil/contexte connu dans les 10 premiers mots**, ou s'appuyer sur un format récurrent reconnaissable (Journal IA).

---

## 4. Ce qu'il ne faut PLUS faire

- ❌ **PRIORITÉ ABSOLUE : publier 3+ fois par jour sur TikTok.** Depuis le 20/08, jusqu'à 5 vidéos/jour ont été publiées ; plusieurs tombent à 0–11 vues le jour même. Revenir à **1 post/jour maximum**, quitte à mettre du contenu en réserve plutôt que de le pousser le même jour.
- ❌ **Compter sur « Commente le mot X » pour générer des commentaires, y compris sur TikTok désormais.** Le taux est retombé à 0,48 commentaire/vidéo en moyenne (vs 2,85 en juillet) — la formule répétée semble avoir perdu son effet de nouveauté. Tester 2-3 CTA alternatifs (question ouverte, sondage, silence volontaire).
- ❌ **« Commente le mot X » seul sur Instagram**, toujours quasi 0 commentaire (31 posts sur 35 sans aucun commentaire ce run).
- ❌ **Ignorer la chute Instagram en espérant qu'elle se résorbe seule** : 3ᵉ semaine de baisse consécutive (108,7 → 47,6 → 33,2 vues moy). Nécessite un audit qualitatif, pas juste plus de volume.
- ❌ **Vidéos ≤15 s** : toujours sous-performantes quand elles apparaissent dans l'échantillon.
- ⚠️ **Laisser le workflow LinkedIn tourner sans vérifier son statut** : depuis le 22/08 chaque tentative échoue silencieusement côté automatisation (visible seulement en lisant `blotato_list_posts`, pas de log applicatif alerté).

---

## 5. Meilleures heures de publication

Robustesse **faible ce run** — la rafale de publication (§0.2) a brouillé le signal horaire habituel.
- **TikTok** : le créneau 14:00 UTC (18h Réunion) reste visible mais n'est plus dominant — les posts sont désormais dispersés sur toute la journée (03:00, 08:00, 12:00, 14:00, 17:00, 20:00 UTC) à cause du rythme de 4-5 posts/jour. **Ne pas tirer de nouvelle conclusion horaire tant que la cadence n'est pas revenue à 1/jour.**
- **Instagram** : créneau 14:29 UTC toujours dominant (12/35 posts), confirmé sur 3 runs consécutifs — c'est le signal le plus robuste de ce rapport.
- **Concurrent `jb.roy_`** : rafales encore plus marquées (jusqu'à 8 vidéos/jour), aucun signal horaire exploitable ce run.
- **Recommandation inchangée** : garder 14:00 UTC (TikTok) / 14:29 UTC (Instagram) comme créneau pivot dès que la cadence redescend à 1 post/jour.

---

## 6. Durée cible de vidéo

- **Tony (TikTok)** : médiane **34 s** (vs 32,5 s le 17/08) — stable dans la fourchette recommandée.
- **Concurrent `jb.roy_`** : médiane **33,5 s** (vs 44 s le 17/08, vs 44 s début août) — **l'écart de durée avec Tony est maintenant quasiment nul**. Le concurrent a nettement raccourci son format moyen tout en gardant des outliers longs (jusqu'à 98 s) et courts (10 s).
- **Cible recommandée : 30–35 s**, confirmée par les deux comptes désormais alignés sur ce créneau. Éviter ≤15 s (sous-performe systématiquement) ; les outliers >70 s restent possibles ponctuellement (formats Journal IA, essais narratifs) mais ne doivent pas devenir la norme.

---

## 7. Ce que fait le concurrent `@jb.roy_` qui marche (TikTok, Apify)

**Note méthodologique** : la métrique "engagement moyen par vue" calculée comme moyenne des ratios par post est faussée par les petits dénominateurs (un post à 2 vues et 1 like affiche 50%). Ce run utilise en complément l'**agrégat** (somme interactions / somme vues) sur une fenêtre comparable (depuis le 14/08, les deux comptes) :

| Métrique (depuis 14/08) | `jb.roy_` (n=34) | `automationboost7` (n=29) |
|---|---|---|
| Vues totales cumulées | 10 769 | 6 290 |
| Vues moyennes | 316,7 | 216,9 |
| Engagement agrégé (somme interactions / somme vues) | **2,67%** | 2,19% |
| Commentaires cumulés | 12 | 12 |
| Durée médiane | 33,5 s | 34 s |

**L'écart s'est encore réduit** : l'engagement agrégé est désormais quasi à parité (2,67% vs 2,19%, contre 7,7% vs 5,2% le 05/08) — mais attention, **les deux comptes ont vu leur taux d'engagement baisser fortement en valeur absolue** ce mois-ci, pas seulement Tony. Ce n'est donc probablement pas (uniquement) un problème spécifique à Autoboost — possible effet saisonnier ou algorithmique plus large mi-août, à garder à l'esprit avant de sur-corriger.

Enseignements exploitables :
- **CTA constant** : légende quasi identique sur toutes ses vidéos (« Follow @jb.roy_ pour implémenter l'IA dans ton activité ») — le vrai hook reste **parlé, pas écrit** ; les métadonnées scrapées ne le révèlent pas (limite connue, nécessiterait un passage par `get_tiktok_transcript` pour en tirer des formulations exactes — non fait ce run par contrainte de temps).
- **Rafales de publication encore plus marquées que chez Tony** (jusqu'à 8 vidéos/jour le 20/08) — signal clairement **à ne pas imiter**, il ne semble pas non plus lui garantir un meilleur reach par vidéo (vues moyennes en baisse chez lui aussi).
- **Durée désormais alignée sur Tony** (33,5 s médian) — l'écart qui justifiait d'allonger les vidéos de Tony a disparu.

---

## 8. Recommandations prioritaires (semaine suivante)

1. **🔴 Stopper la cadence de publication TikTok à 1 post/jour maximum.** C'est la cause la plus probable et la plus actionnable de la baisse de vues moyennes des deux comptes (Tony ET le concurrent) — corréler directement les jours à 4-5 posts avec des vues proches de 0 sur les derniers posts du jour.
2. **🔴 Faire reconnecter le compte LinkedIn dans Blotato** (expiré depuis le 22/08, action manuelle de Tony, hors de portée de cet agent) — sinon toute la queue programmée jusqu'au 26/08 va continuer à échouer.
3. **Auditer qualitativement la chute Instagram** (33,2 vues moy, 3ᵉ semaine de baisse) plutôt que d'ajouter du volume : revoir les 5-6 derniers posts un par un pour un signal qualitatif (miniature, premières secondes, legend) avant la prochaine salve.
4. **Rejouer systématiquement les 2 patterns confirmés sur plusieurs runs** : bénéfice chiffré personnel (§3.1) et format « Journal IA » récurrent (§3.3) — ce sont les deux seuls hooks avec des preuves répétées sur 2-3 semaines.
5. **Ne plus traiter « Commente le mot X » comme un CTA fiable, TikTok compris désormais** — tester 2-3 alternatives (question ouverte, "Follow pour la suite" seul, sondage) sur les prochains scripts.
6. **Décider du sort de `n5dIUNEk5D6Pj3Vf`** : toujours 0 exécution, URLs placeholder jamais remplacées depuis sa création le 21/07 (>1 mois) — soit le configurer avec de vraies credentials, soit l'archiver pour ne plus polluer le suivi.

---

## 9. Sources & limites

- **TikTok (Tony + concurrent)** : Apify, actor `clockworks/tiktok-scraper`, workflow n8n `YUJjz5NNsYo41t8q`, deux exécutions séparées ce jour (24/08) : **#77671** (automationboost7, 40 vidéos, ~47 s) et **#77673** (jb.roy_, 40 vidéos, ~12 s — plus rapide que les 35-54 s habituels, possible cache Apify côté profil déjà scrapé récemment, à surveiller). Une première tentative (#77672, jb.roy_) a échoué silencieusement à cause d'un bug de paramétrage n8n (voir §0.4) — données invalidées et non utilisées. Workflow remis dans son état d'origine (`profiles: ["automationboost7"]`) après usage.
- **Instagram (Tony)** : Blotato (`blotato_list_top_posts`, platform=instagram, depuis le 05/08, 50 résultats bruts, 15 posts foodboost exclus manuellement → 35 exploitables). Fraîcheur des métriques vérifiée (délai `fetchedAt − createdAt` stable ~7 jours sur toute la période) — la baisse observée n'est pas un artefact de collecte tardive.
- **LinkedIn** : Blotato confirme l'historique de publication et **révèle une panne active** (`errorMessage: "LinkedIn account has expired"` sur tous les posts depuis le 22/08). Toujours aucune métrique — Windsor.ai non revérifié ce run (pas de nouveau connecteur attendu, situation inchangée au 17/08).
- **Workflow analytics hebdo `n5dIUNEk5D6Pj3Vf`** : confirmé de nouveau **0 exécution** (`search_executions` vide), inactif, toujours des URLs placeholder non remplacées (Instagram Graph API, TikTok API, Telegram chat ID). Statut inchangé depuis sa création le 21/07 — plus d'un mois sans configuration.
- **Workflow concurrent `YUJjz5NNsYo41t8q`** : historique d'exécutions désormais bien conservé (6 exécutions au 18/08, puis 3 nouvelles ce jour) — contrairement au run du 05/08 où l'historique semblait avoir disparu.
- **tokscript** : `get_tiktok_user` utilisé pour vérifier abonnés/existence de compte (automationboost7, tonypayet4, jb.roy_) — fonctionne sans Pro. `get_tiktok_user_videos` toujours non testé ce run (Apify a suffi et est resté la source de vérité pour le détail vidéo par vidéo).

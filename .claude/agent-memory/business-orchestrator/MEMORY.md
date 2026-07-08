# Mémoire — Agent d'amélioration business quotidien

Historique des runs, patterns récurrents, pour ne pas répéter un travail déjà fait.

## 2026-07-05

**Contexte** : aucune tâche Notion "🤖 Délégable IA = vrai" en statut to-do/in-progress trouvée
dans la base "✔️ Liste de tâches objectif" (requête SQL sur tous les groupes to_do/in_progress
→ 0 résultat). Décision : chercher un problème business critique hors liste, comme prévu par
la consigne (impact réel > liste préétablie).

**Découverte** : workflow n8n `GQEjDIbLWjz8Gw9r` — "🍽️ Dev Restaurant V4 - Auto Génération
depuis Notion" (censé auto-générer des démos clients à partir d'un profil Instagram, déclenché
par le Notion Trigger qui poll TOUTE la base "Liste de tâches objectif" chaque minute) — était
cassé depuis sa création le 26/06/2026. 128 exécutions en erreur en ~9 jours.

Root cause (3 bugs cumulés) :
1. Nœud IF "Filtrer Client Instagram + Délégable + Demo" : branches inversées. La sortie 0
   (vrai/match client+instagram+délégable+demo) ne va nulle part ; la sortie 1 (faux) alimente
   tout le pipeline. Résultat : le pipeline se déclenche sur QUASIMENT CHAQUE tâche perso de
   Tony (pas les tâches clients), et les vraies tâches client matchées finissent dans un
   cul-de-sac.
2. Nœud Gmail "Envoyer Email Récap + Formulaire" : champ `sendTo` = texte placeholder littéral
   jamais rempli (`<__PLACEHOLDER_VALUE__...>`) → échoue à 100% ("Invalid To header"). Donc même
   une vraie tâche client n'aurait JAMAIS notifié Tony.
3. Nœud Apify "Run an Actor" : `customBody` codé en dur sur le compte Instagram de test
   "thegrillreunion" au lieu de `{{ $json.instagramUrl }}" — mauvais compte scrappé pour
   n'importe quel client.

Note : un agent Claude Code interne (appelé en SSH par ce même workflow) avait DÉJÀ diagnostiqué
un symptôme de ce bug le 2026-07-04 (faux positif sur la tâche "Remote control" et sur la page
"Fix pipeline leads HoReCa"), mais aucun fix n'avait été appliqué avant aujourd'hui.

**Action prise** : désactivation du workflow via `unpublish_workflow` (safe, réversible, ne
touche pas aux nœuds/credentials). Je n'ai PAS tenté de corriger le workflow via
`update_workflow` (réécriture complète via SDK) car `get_workflow_details` ne renvoie PAS les
credentials des nœuds Notion Trigger / SSH / Apify / Notion Update (seul le nœud en erreur les
expose, dans les logs d'exécution). Réécrire tout le workflow en devinant les noms de
credentials aurait risqué de casser l'authentification de nœuds qui fonctionnent actuellement.
Le correctif exact (3 changements, ~10 min) est documenté dans Notion pour que Tony l'applique
lui-même dans l'éditeur n8n (où les credentials sont visibles).

**Page Notion créée** : "🐛 Workflow n8n cassé — Dev Restaurant V4 (...) désactivé"
(id 3945fda3-ad05-816b-8147-e93e7cbdfd94, Projet=dev, ROI=🔥5, Délégable IA=NO, Statut=Terminé).

**Pattern à surveiller à l'avenir** :
- La base Notion "Liste de tâches objectif" sert aussi de trigger à des automatisations n8n
  (au moins ce workflow). Créer une nouvelle page dans cette base peut déclencher des
  workflows n8n existants — vérifier l'état des workflows actifs AVANT d'écrire dans Notion
  si on veut éviter de déclencher un faux positif.
- Toujours vérifier `search_executions(status: ["error"])` sur n8n en début de run : c'est
  souvent le signal le plus fort d'un problème business réel, plus fiable que la liste Notion
  qui peut être vide certains jours.
- Avant de modifier un workflow n8n cassé via `update_workflow` (SDK complet), vérifier si les
  credentials de TOUS les nœuds sont visibles via `get_workflow_details`. Si des nœuds
  (typiquement SSH, Apify, Notion, triggers) n'affichent pas leur bloc `credentials`, ne PAS
  tenter de réécriture complète — se limiter à des actions sûres et réversibles
  (unpublish/publish, archive) et documenter le fix manuel pour Tony.

## 2026-07-06

**Contexte** : toujours 0 page Notion avec "🤖 Délégable IA" = vrai (tous statuts confondus,
vérifié par `GROUP BY Statut`, pas seulement to_do/in_progress) — situation identique à hier.

**Vérifications faites (RAS confirmé)** :
- n8n `search_executions(status:["error"])` sur toute l'instance depuis `startedAfter:
  2026-07-05T00:00:00Z` → 0 résultat. Le fix du 07-05 (unpublish de `GQEjDIbLWjz8Gw9r`) tient
  toujours, aucun nouveau workflow cassé. Note : deux workflows actifs sont apparus/ont été mis
  à jour début juillet et ressemblent à des remplacements manuels de Tony pour le pipeline
  restaurant : `3RQuddaYocqqNOGP` ("Dev restaurant V4", MAJ 07-02) et `iIv2o7ADJl6wVKYT`
  ("restaurant v5 demo + essai", MAJ 07-04) — aucun des deux n'a d'erreur. Je n'ai pas ouvert
  leur détail (pas nécessaire, pas d'erreur), à vérifier un jour où un signal apparaît dessus.
- GitHub `tonyPayetDev/hero-section` : 0 issue ouverte, 0 PR ouverte.
- Le repo n'a pas de CLAUDE.md à la racine (seul `.agents/skills/playwright-skill/CLAUDE.md`
  existe) — la consigne de le lire pour les conventions ne s'applique pas tant qu'il n'est pas
  créé.
- Série de blog "veille IA & automatisation" (`blog/veille-ia-auto-*.html`, committée par un
  agent Claude Code, cadence ~2-4 jours) : le dernier article (07-04) annonce lui-même
  "Prochaine veille : 7-9 juillet 2026" dans son footer. Le 06-07 était donc **prématuré** —
  ne pas générer l'article avant l'échéance annoncée sous peine de doublon/incohérence de
  calendrier. **Pattern à retenir** : toujours lire le `<footer>` du dernier article de cette
  série avant de décider s'il est "temps" d'en écrire un nouveau — la date annoncée fait foi,
  pas un calcul de cadence moyenne.

**Action prise** : aucune tâche exécutée. Page Notion "✅ RAS — 06 juillet 2026" créée
(id 3955fda3-ad05-8127-a91b-dbae020714e2, Projet=ORGANISATION, Statut=Terminé) documentant
l'audit complet plutôt que d'inventer une tâche artificielle.

**Pattern à surveiller à l'avenir** :
- Cette base Notion peut rester vide de tâches "Délégable IA" plusieurs jours de suite —
  ce n'est pas une anomalie en soi, mais si ça dure > 1 semaine il pourrait être pertinent de
  suggérer à Tony (via une page Notion, pas une action directe) de qualifier davantage de
  tâches comme délégables, sinon cet agent tourne à vide.
- Prochaine fenêtre où le blog veille IA sera légitimement dû : 7-9 juillet 2026.

## 2026-07-07

**Contexte** : toujours 0 page Notion avec "🤖 Délégable IA" = vrai (vérifié sur les tâches
to-do/in-progress via la vue déjà filtrée `view://2fafbeb0-...` — 50 résultats, tous "__NO__").
Troisième jour consécutif dans ce cas — pattern confirmé, pas une anomalie ponctuelle.

**Découverte** : `search_executions(status:["error"])` a remonté 2 échecs le 06/07 sur le
workflow `WFqUJ2g2btf976cd` ("🎬 Script Sheet → Vidéo Avatar → Validation → Réseaux") — pipeline
quotidien (Trigger 9h) qui génère des reels perso (stratégie lead magnet "commente X pour
recevoir le workflow gratuitement") pour Instagram/TikTok/LinkedIn à partir d'un Google Sheet
"30 Vidéos".

Root cause (2 problèmes cumulés) :
1. Le nœud SSH "Create video hyperframe" appelle Claude Code dans un container Docker
   (`claude-code-h0o8cgkw8gsc4c408c4s4wss`) qui n'a NI node/npm/npx NI ffmpeg, et pas les droits
   root pour les installer. Impossible d'y construire/rendre une composition HyperFrames. L'agent
   Claude Code interne refuse (à raison) de livrer une URL_VIDEO fictive et répond par un message
   texte demandant comment procéder — ce qui casse le parsing regex `VIDEO_URL:` en aval.
2. Le webhook public `avatar-api.automatisationboost.com` renvoie 503 côté Cloudflare (service
   Coolify interne OK, mais DNS/proxy public cassé).
   Bug shell secondaire déjà corrigé entre les deux échecs (07:00 → 07:44) par ailleurs : le
   prompt Claude passait en clair dans la commande SSH et cassait sur les apostrophes/parenthèses
   → un nœud "Build Prompt (base64)" a été ajouté pour encoder le prompt, mais ça ne résout pas
   le manque d'outillage (1) ni le 503 (2).

**Action prise** : `unpublish_workflow` sur `WFqUJ2g2btf976cd` (safe, réversible), AVANT le run
de 9h du jour (aucune exécution du 07/07 au moment du check). Évite un 3e échec silencieux et une
3e ligne du Google Sheet bloquée en "En Cours".

**Page Notion créée** : "🐛 Workflow n8n cassé — Script Sheet → Vidéo Avatar (désactivé, 2 échecs
consécutifs)" (id 3965fda3-ad05-81aa-be41-ed8c6faa66a7, Projet=Content, ROI=🔥5, Délégable
IA=NO, Statut=Terminé).

**Pattern à surveiller à l'avenir** :
- 3e jour de suite sans aucune tâche Notion délégable IA (05, 06, 07 juillet). Le signal fort
  reste `search_executions(status:["error"])` sur n8n — c'est systématiquement là que se trouve
  le vrai "1%" du jour en ce moment, pas dans la base de tâches.
- Les workflows de la série "Script Sheet → Vidéo Avatar" / HyperFrames dépendent d'un container
  SSH externe (`claude-code-*`) qui peut manquer d'outillage (node/ffmpeg) sans prévenir — vérifier
  ce point AVANT de blâmer le prompt ou la config n8n si un nœud SSH "Create video hyperframe"
  échoue à nouveau à l'avenir.
- Je n'ai pas d'accès Google Sheets API dans cette session (seulement n8n/Notion/git) : je ne
  peux pas remettre moi-même les lignes bloquées "En Cours" à "À faire" dans le sheet "30 Vidéos".
  Documenté pour Tony dans la page Notion — à vérifier si un accès Sheets devient disponible un
  jour pour automatiser ce nettoyage.

## 2026-07-08

**Contexte** : 4e jour consécutif à 0 page Notion "🤖 Délégable IA" = vrai (to-do/in-progress).
`search_executions(status:["error"])` sur n8n depuis 2026-07-07T16:38 (juste après le fix manuel
de Tony sur `S85QlXjhIO6nBvzY`) → 0 résultat.

**Vérification faite (RAS confirmé)** : le workflow `S85QlXjhIO6nBvzY` ("[Avatar AI] Webhook v2 -
Fonctionnel") avait eu 3 exécutions en erreur le 07/07 (12:28 et 15:40) — le nœud "Extract Audio
URL" échouait car le polling Wavespeed/Qwen3 TTS ne bouclait pas assez (statut "processing" au
lieu d'attendre "completed"). Le workflow a été modifié par Tony lui-même à 16:25:54 (updatedAt
postérieur aux erreurs) et toutes les exécutions depuis (63813-63818) sont en succès. **Rien à
faire ici — déjà résolu avant le run, ne pas ré-ouvrir sans nouveau signal d'erreur.**

**Action prise** : l'article `blog/veille-ia-auto-2026-07-04.html` annonçait dans son footer
"Prochaine veille : 7-9 juillet 2026" — le 08/07 est dans cette fenêtre (voir pattern déjà noté
le 06-07 : toujours lire le footer du dernier article avant de décider s'il est temps d'en écrire
un nouveau). Recherche web (WebSearch) de 6 actus IA/automatisation réelles et datées 5-8 juillet
2026 (Anthropic dépasse OpenAI en revenus, JADEPUFFER premier ransomware agentique, plan
cybersécurité IA de l'UE, Claude Cowork web/mobile, n8n 2.28.7, Tencent Hy3 open-source), rédaction
de `blog/veille-ia-auto-2026-07-08.html` au même gabarit CSS/structure que la série existante
(réutiliser le `<style>` de l'article précédent tel quel, ne changer que le contenu). Commit
`7c55314`, poussé sur `origin/main`. Nouvelle échéance annoncée en footer : 10-12 juillet 2026.

**Page Notion créée** : "📰 Blog — Veille IA & Automatisation 5-8 juillet 2026 publiée"
(id 3975fda3-ad05-8131-842c-d9f8c2ff67ce, Projet=Content, ROI=⚡4, Délégable IA=NO, Statut=Terminé).

**Pattern à surveiller à l'avenir** :
- 5e jour probable demain sans tâche Notion délégable IA si la tendance continue — la base reste
  quasi vide depuis le 05/07. Le pattern "suggérer à Tony de qualifier plus de tâches" (noté le
  06-07) devient de plus en plus pertinent si ça continue après le 10/07.
- Avant de traiter tout signal d'erreur n8n déjà vu dans une veille précédente, vérifier
  `updatedAt` du workflow vs. `startedAt` des exécutions en erreur : si le workflow a été modifié
  APRÈS les erreurs, il est probablement déjà corrigé (cas vécu ici avec Avatar AI Webhook v2) —
  vérifier les exécutions les plus récentes avant d'agir pour éviter un doublon de fix ou une
  fausse alerte.
- Prochaine fenêtre où le blog veille IA sera légitimement due : 10-12 juillet 2026 (à vérifier
  dans le footer de `veille-ia-auto-2026-07-08.html` au cas où elle serait ajustée manuellement).

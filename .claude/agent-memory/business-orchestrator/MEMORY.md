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

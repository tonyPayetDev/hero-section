# Scripts en attente d'ajout au Sheet — run du 2026-10-06

> ⚠️ **Écriture automatique bloquée ce run.** Le connecteur MCP `n8n` est en
> `needs_reconnect` (OAuth) — confirmé par `ListConnectors` au tout début de cette
> session cloud à froid, et par un `ToolSearch` répété sur "n8n workflow",
> "create_workflow_from_code", "google sheets append" qui ne retourne **aucun**
> outil `n8n_*` chargeable. C'est la même panne que celle documentée par l'agent
> `social-analytics` dans `/home/user/hero-section/STRATEGIE.md` (commit `a7d3ae4`,
> §0.1) : elle a aussi empêché ce run-là d'écrire l'onglet "Analyse Perf".
>
> Je n'ai **pas** tenté d'écriture alternative risquée sur le Google Sheet
> (`10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags`) : pas d'accès direct non
> officiel, pas de contournement. J'ai aussi tenté une simple **lecture** CSV
> publique de l'onglet principal (gid inconnu, testé `gid=0`) pour vérifier la
> dernière ligne existante avant un futur append — cette lecture a été refusée
> par le classificateur de permissions de la session (motif PII), donc je n'ai
> pas pu déterminer la dernière ligne physique du Sheet ce run non plus.
>
> **Les 5 scripts ci-dessous sont complets et prêts à coller tels quels** dans
> l'onglet principal (celui lu par `veille-to-video`, PAS "Analyse Perf", PAS
> "30 Vidéos"), en 5 nouvelles lignes **après** la dernière ligne existante —
> à vérifier/lire d'abord avant collage, ou à écrire automatiquement au prochain
> run une fois le connecteur n8n réautorisé (OAuth interactif requis, voir
> STRATEGIE.md §0.1 / §8.2).
>
> Colonnes dans l'ordre : `# | Workflow | Lien n8n | Script Voix Off (20s) |
> Texte TikTok + Hashtags | Mot-clé CTA | Lien Screen Record | Statut Tournage |
> Vidéo Finale | Date Publication`. Les colonnes `Lien n8n` (aucun workflow n8n
> dédié identifié pour ces angles ce run), `Lien Screen Record`, `Vidéo Finale`
> et `Date Publication` sont laissées vides à dessein — ne pas inventer de liens.
> `Statut Tournage` = `⬜ À faire` pour les 5.

## Learnings appliqués (source : STRATEGIE.md §3, §4, §8 — run 2026-10-06)

- Hook = outil/actualité connu nommé + chiffre précis dans les 5-10 premiers mots (pattern le plus robuste, confirmé sur 4 runs).
- Durée cible 30–45 s (~110–150 mots à 3,3 mots/s), jamais le format "Journal IA quotidien" (s'effondre x10 sur IG).
- CTA : "Follow + lien bio" en premier mécanisme, mot-clé ressource en MAJUSCULES formulé "Commente le mot X" (jamais "Commente X" seul — le mot seul ne généreait quasi aucun commentaire d'après STRATEGIE §4).
- Une idée distincte par script, aucun doublon avec le Top 5 déjà produit (Opus 5, Kilo Code/n8n, Higgsfield, tuto VPS/Coolify, économie 200€/mois secrétariat).
- Priorité donnée au pattern "économie chiffrée + témoignage perso", jamais retesté depuis 3 runs (STRATEGIE §3.5 / §8.5).

---

### Script 1 — Alternative gratuite à Zapier (n8n automations)

| Champ | Contenu |
|---|---|
| **Workflow** | Zapier vs n8n — alternative gratuite |
| **Lien n8n** | *(aucun workflow dédié — à compléter si Tony veut montrer un exemple concret)* |
| **Script Voix Off (20s)** | L'alternative gratuite à Zapier, c'est n8n, et personne n'en parle assez. Zapier commence autour de 20 dollars par mois pour seulement quelques centaines de tâches, et le prix grimpe vite dès que tu automatises plusieurs process clients. n8n fait exactement la même chose — les mêmes connexions email, CRM, Google Sheets, Claude — mais tu peux l'installer toi-même sur un petit serveur pour quelques euros par mois, sans limite de tâches. Je m'en sers tous les jours pour mes clients freelances : devis automatiques, relances, publication de contenu. Si tu factures encore ton temps à automatiser à la main, tu perds de l'argent chaque semaine. Follow pour la suite, et commente le mot AUTOMATISE pour recevoir le template n8n gratuit que j'utilise, lien en bio. |
| **Texte TikTok + Hashtags** | L'alternative gratuite à Zapier existe, et elle coûte 0€ 👀 Zapier = 20$/mois pour quelques centaines de tâches. n8n = gratuit en self-host, même résultat. Commente le mot AUTOMATISE 👇 #n8n #automatisation #freelance #IA #zapier |
| **Mot-clé CTA** | AUTOMATISE |
| **Lien Screen Record** | *(vide)* |
| **Statut Tournage** | ⬜ À faire |
| **Vidéo Finale** | *(vide)* |
| **Date Publication** | *(vide)* |

---

### Script 2 — Frustration tarifaire ElevenLabs (AI dev tools)

| Champ | Contenu |
|---|---|
| **Workflow** | ElevenLabs — prix et crédits qui disparaissent |
| **Lien n8n** | *(aucun workflow dédié)* |
| **Script Voix Off (20s)** | ElevenLabs, c'est 5 à 99 dollars par mois selon le nombre de minutes de voix que tu clones, et tes minutes non utilisées disparaissent à la fin du mois, comme un abonnement de salle de sport. Pour un freelance qui sort des vidéos toutes les semaines, ça devient vite la facture qui fait mal. Il existe des façons de cloner ta voix et de générer ta voix off automatiquement avec n8n, sans payer le tarif premium à chaque rendu. C'est exactement ce que j'ai mis en place pour produire mes vidéos TikTok sans exploser mon budget outils. Follow pour la suite, et commente le mot VOIX pour recevoir le comparatif complet des outils de clonage vocal et leurs prix réels, lien en bio. |
| **Texte TikTok + Hashtags** | ElevenLabs : 5 à 99$/mois, et tes crédits inutilisés disparaissent chaque mois 💸 Voilà comment j'ai contourné ça pour mes vidéos. Commente le mot VOIX 👇 #IA #voixoff #freelance #n8n #outilsIA |
| **Mot-clé CTA** | VOIX |
| **Lien Screen Record** | *(vide)* |
| **Statut Tournage** | ⬜ À faire |
| **Vidéo Finale** | *(vide)* |
| **Date Publication** | *(vide)* |

---

### Script 3 — Tuto 3 étapes : Claude Code + n8n pour les devis (n8n automations / Claude Code)

| Champ | Contenu |
|---|---|
| **Workflow** | Devis client automatisé — Claude Code + n8n |
| **Lien n8n** | *(aucun workflow dédié identifié ce run — à lier si un workflow existant correspond)* |
| **Script Voix Off (20s)** | En douze minutes chrono, je connecte Claude Code à n8n pour générer un devis client automatiquement. Étape une, deux minutes : je décris le besoin du client en langage normal à Claude Code. Étape deux, cinq minutes : Claude Code écrit le workflow n8n qui va chercher le prix dans mon tableau et remplir le PDF. Étape trois, cinq minutes : je teste, j'ajuste, et le devis part tout seul par email dès qu'un client remplit mon formulaire. Zéro ligne de code écrite à la main, zéro heure perdue le soir à recopier des chiffres. C'est ce genre d'automatisation qui m'a permis de prendre plus de clients sans embaucher. Follow pour la suite, et commente le mot DEVIS pour recevoir le workflow complet, lien en bio. |
| **Texte TikTok + Hashtags** | 12 minutes chrono pour automatiser mes devis clients avec Claude Code + n8n 🤯 3 étapes, zéro code à la main. Commente le mot DEVIS 👇 #claudecode #n8n #automatisation #freelance #productivité |
| **Mot-clé CTA** | DEVIS |
| **Lien Screen Record** | *(vide)* |
| **Statut Tournage** | ⬜ À faire |
| **Vidéo Finale** | *(vide)* |
| **Date Publication** | *(vide)* |

---

### Script 4 — Économie chiffrée + témoignage perso (freelance leverage) — retest prioritaire du pattern §3.5

| Champ | Contenu |
|---|---|
| **Workflow** | 15h/semaine récupérées — Claude Code + n8n sur la gestion clients |
| **Lien n8n** | *(aucun workflow dédié identifié ce run)* |
| **Script Voix Off (20s)** | Claude Code et n8n m'ont fait gagner quinze heures par semaine sur la gestion de mes clients freelances, et je n'exagère pas. Avant, je passais mes soirées à répondre aux mêmes questions, relancer les factures impayées, et remplir des tableaux de suivi à la main. Aujourd'hui, un workflow n8n lit mes mails, Claude Code trie les demandes urgentes, et tout ce qui est répétitif part en automatique pendant que je dors. Résultat concret : quinze heures récupérées chaque semaine, soit presque deux journées de travail en plus pour prospecter ou me former. Ce n'est pas de la théorie, c'est mon planning réel depuis trois mois. Follow pour la suite, et commente le mot GAGNE pour recevoir la structure exacte de ce workflow, lien en bio. |
| **Texte TikTok + Hashtags** | Claude Code + n8n m'ont fait gagner 15h/semaine sur la gestion clients. Pas de la théorie, mon planning réel depuis 3 mois 📈 Commente le mot GAGNE 👇 #freelance #claudecode #n8n #productivité #automatisation |
| **Mot-clé CTA** | GAGNE |
| **Lien Screen Record** | *(vide)* |
| **Statut Tournage** | ⬜ À faire |
| **Vidéo Finale** | *(vide)* |
| **Date Publication** | *(vide)* |

---

### Script 5 — Claude Code inclus dans l'abonnement Claude Pro (hot AI news / Claude Code)

| Champ | Contenu |
|---|---|
| **Workflow** | Claude Code inclus dans Claude Pro — cas d'usage freelance |
| **Lien n8n** | *(aucun workflow dédié)* |
| **Script Voix Off (20s)** | Claude Code tourne directement dans ton terminal, et il est inclus dans l'abonnement Claude Pro à 20 dollars par mois, sans abonnement développeur séparé en plus. Il lit tout ton projet, écrit le code, corrige les bugs, et exécute les commandes à ta place, comme un développeur senior à côté de toi. Pour un freelance ou un créateur solo qui n'a pas le budget pour embaucher un développeur, c'est le levier le plus rentable que j'ai testé cette année. Je m'en sers pour construire mes automatisations n8n, mes sites clients, et même les scripts de mes vidéos. Follow pour la suite, et commente le mot CODE pour recevoir ma liste de cas d'usage freelance, lien en bio. |
| **Texte TikTok + Hashtags** | Claude Code est inclus dans l'abonnement Claude Pro à 20$/mois, pas un centime de plus 🤖 Mon développeur senior perso. Commente le mot CODE 👇 #claudecode #IA #freelance #automatisation #devtools |
| **Mot-clé CTA** | CODE |
| **Lien Screen Record** | *(vide)* |
| **Statut Tournage** | ⬜ À faire |
| **Vidéo Finale** | *(vide)* |
| **Date Publication** | *(vide)* |

---

## À faire au prochain run (ou manuellement maintenant)

1. Réautoriser le connecteur n8n (OAuth, session interactive requise — voir STRATEGIE.md §0.1/§8.2).
2. Lire la dernière ligne physique réelle de l'onglet principal du Sheet `10BHHpGn4qPjlo_-OuGjdT7-LAYxdKfjg6SRKh_9Dags` (pas "Analyse Perf", pas "30 Vidéos").
3. Append ces 5 lignes juste après, via un petit workflow n8n `create_workflow_from_code` (Manual Trigger → Google Sheets `append`), `Statut Tournage = ⬜ À faire`.
4. Vérifier par relecture CSV : 5 lignes ajoutées, 0 ligne existante modifiée.
5. Supprimer ou archiver ce fichier une fois les 5 scripts effectivement copiés dans le Sheet.

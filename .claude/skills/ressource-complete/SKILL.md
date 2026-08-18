---
name: ressource-complete
description: >
  Transforme une ressource (PDF, guide, ZIP, template, skill) en tunnel complet en une passe :
  page de vente + page de livraison gatée par token + carte sur le site + mapping CTA→ressource
  pour l'Auto-DM + vidéo promo + déploiement Coolify. Utilise ce skill quand Tony dit : « crée
  une ressource pour <fichier> », « fais une page de vente pour ce guide/skill », « mets ce PDF
  en lead magnet / en produit payant », « transforme ça en ressource complète », ou
  `/ressource-complete`. Généralise ce qui a été fait à la main pour le skill Horror et les guides PDF.
---

# /ressource-complete — un actif → un tunnel complet

**Problème résolu :** créer un lead magnet ou un produit payant est fait à la main à chaque fois
(page de vente, livraison gatée, carte, mapping DM, vidéo). ~1-2 h par ressource. Ce skill fait
tout le bundle d'un coup, à partir d'un seul fichier + quelques infos.

Modèles de référence (déjà en prod, à copier/adapter, NE PAS réinventer) :
`/work/automationboost/skills/horror-beatsync.html` (page de vente) et
`horror-beatsync-acces.html` (livraison gatée). Site = `/work/automationboost/`.

## Entrées à réunir (demander à Tony si absentes)
- **La ressource** : chemin local du fichier (PDF/ZIP/…) ou URL `assets.automatisationboost.com`.
- **Sujet + audience** : à qui, quel problème résolu.
- **Modèle** : `gratuit` (lead magnet, capture via commentaire) OU `payant` (prix €, lien Stripe).
- **Mot-clé CTA** : un mot unique en MAJ (ex. `RELANCE`, `OPUS`, `LIVRE`) — sert de clé partout.

## Procédure (6 blocs)

### 1 — Héberger la ressource
- Poser le fichier sous `/work/automationboost/assets/downloads/<slug>-<hash>.<ext>` (hash court
  aléatoire = obscurcissement de l'URL). ⚠️ Un hébergement nginx statique = la gate est **cosmétique**
  (le fichier reste public si on connaît l'URL). Pour du **payant réel**, servir le fichier depuis
  n8n après vérification du token (voir bloc 4), pas depuis `/assets/`.
- Vérifier ensuite en HTTP que l'URL répond 200 (voir [[feedback_cloud_routine_needs_pushed_assets]]).

### 2 — Page de vente (`skills/<slug>.html`)
Copier `horror-beatsync.html` et adapter : hero (bénéfice + hook), problème/solution, ce que
contient la ressource, **section valeur** (temps/coût que ça fait gagner, table comparative),
FAQ, et le CTA :
- **gratuit** → « commente le mot `<CTA>` » (capture par l'Auto-DM).
- **payant** → bouton Stripe (`https://buy.stripe.com/...`) → redirige vers la page d'accès gatée.
Palette AutomatisationBoost (thème clair/black + Sora), accent violet pour le premium. Ne pas
casser les accents (fragment HTML → encoder en UTF-8, cf. [[project_autoboost_comp_html_pitfalls]]).

### 3 — Page de livraison gatée (`skills/<slug>-acces.html`)
Copier `horror-beatsync-acces.html` : états loading/ok/error/no-token, valide le token via
`POST https://n7n.automatisationboost.com/webhook/validate-token` body `{token, product:"<slug>"}`,
stocke dans `localStorage` clé `ab_<slug>_access`, puis affiche le lien de téléchargement + guide
d'install. ⚠️ Le workflow de validation accepte aujourd'hui **tout token non vide** (gate cosmétique,
cf. [[project_n8n_update_workflow_needs_publish]]) — pour du payant, durcir : stocker les tokens émis
dans une Data Table n8n et vérifier token+produit avant de servir.

### 4 — Carte sur le site + mapping CTA→ressource
- Ajouter une carte dans `/work/automationboost/skills.html` (grille), lien vers `skills/<slug>.html`,
  incrémenter le compteur de stats. Style `.premium` si payant.
- **Mapping CTA→ressource = un onglet du Sheet, JAMAIS en dur dans le workflow**
  (cf. [[project_cta_resource_mapping_sheet_tab]]) : ajouter une ligne `<CTA> → URL ressource` pour que
  l'Auto-DM Instagram (workflow `U0U6yjMp88h9cH2A`, [[project_ig_autodm_comment_workflow]]) envoie le
  bon lien quand quelqu'un commente le mot. Vérifier via l'API REST n8n si le MCP est down.

### 5 — Vidéo promo
Lancer `/usine-video` (ou directement `veille-to-video`) avec un brief centré sur la ressource et
le **même mot-clé CTA**. La vidéo pousse vers previsualisation ; planif Blotato après ✅ Validé.
Ça referme la boucle : la vidéo amène le commentaire → l'Auto-DM envoie la ressource → la page
convertit.

### 6 — Déployer + vérifier
`/deploy-to-coolify /work/automationboost` (app `ai-automation-site`, cf.
[[reference_coolify_deploy_automatisationboost]]). ⚠️ Pas d'auto-deploy sur push + Cloudflare cache
4h : déclencher le redeploy Coolify ET purger le cache, puis vérifier en HTTP 200 les 3 URLs
(vente, accès, download), pas juste le push (cf. [[project_previsualisation_no_autodeploy]]).

## Règle de fin
Récap français : les 3 URLs live (vente/accès/download) en 200, la ligne CTA ajoutée au Sheet de
mapping, l'état de la vidéo promo, et — si payant — le rappel que la gate est cosmétique tant que
la livraison n'est pas servie depuis n8n après vérif token.

## Pièges (traçables mémoire)
- Payant : la gate statique ne protège rien ([[project_n8n_update_workflow_needs_publish]]) — le
  durcissement n8n est un choix explicite à confirmer avec Tony, ne pas le sous-entendre « sécurisé ».
- Blotato : uploader le binaire, jamais l'URL previsualisation (403 Cloudflare,
  [[feedback_foodboost_blotato_upload_fix]]).
- Toujours vérifier les chemins en HTTP réel avant de les citer comme live.

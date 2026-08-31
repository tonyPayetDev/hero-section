---
name: video-to-resource
description: Video → Ressource — transforme une vidéo Autoboost déjà produite (projet autoboost-NN-*, ou un brief + mot-clé CTA) en page ressource sur automatisationboost.com, l'ajoute à la grille /ressources, et la met en ligne via le skill deploy-to-coolify. À utiliser dès qu'une vidéo est rendue/programmée et qu'il faut la ressource gratuite promise dans le CTA ("Commente le mot X et je t'envoie...").
---

# video-to-resource — la ressource promise par le CTA de la vidéo

**Input :** un projet vidéo `autoboost-neon-videos/autoboost-NN-<slug>/` (ou un brief + mot-clé CTA)
**Output :** `automationboost/ressources/<slug>.html` + une carte dans `ressources.html` + le site déployé

**Skill frère de `veille-to-video` / `reel-remix`.** Ces deux-là produisent la vidéo ; celui-ci produit
la contrepartie promise dans le CTA. Chaque vidéo Autoboost se termine par « Commente le mot `<MOTCLÉ>`
et je t'envoie ... » — **ce skill fabrique le "..."**. Sans lui, le CTA promet quelque chose qui
n'existe pas.

**Règle fondatrice : la ressource doit tenir la promesse exacte du CTA.** Si la voix off dit « je
t'envoie la configuration complète », la page contient la configuration complète (les commandes,
les fichiers, les réglages) — pas un teaser qui renvoie vers une offre payante. Relire la dernière
phrase de `narration.txt` avant d'écrire la page, et livrer littéralement ce qu'elle promet.

---

## Workflow

### Étape 0 — Rassembler les infos de la vidéo

Depuis le projet vidéo (`autoboost-neon-videos/autoboost-NN-<slug>/`) :

| Info | Source |
|---|---|
| Sujet / angle | `narration.txt` |
| Mot-clé CTA | dernière phrase de `narration.txt` (« Commente le mot **X** ») |
| Promesse exacte | même phrase (« je t'envoie **...** ») |
| Durée | `ffprobe` sur le MP4 rendu |
| Captures d'écran | `shots/*.png` si la vidéo en contient (voir `reel-remix`) |
| Légende / hashtags | le post Blotato programmé |

Si la vidéo n'existe pas encore, ce skill fonctionne aussi à partir d'un simple brief + mot-clé —
mais dans ce cas dire clairement à l'utilisateur que le lien vidéo ↔ ressource n'est pas vérifiable.

**Vérifier d'abord qu'une ressource proche n'existe pas déjà** : `ls automationboost/ressources/ | grep -i <thème>`.
Le catalogue dépasse les 190 pages et les doublons y passent inaperçus. Si une page proche existe
(ex. `skill-design-web.html` pour un sujet UI/UX), deux choix — les proposer à l'utilisateur, ne pas
trancher seul :
- **enrichir** la page existante (préférable si elle traite déjà le même sujet), ou
- **créer une page complémentaire** avec un angle distinct, et la lier à l'existante.

### Étape 1 — Écrire la page ressource

Chemin : `automationboost/ressources/<slug>.html` (slug en kebab-case, sans accent, ex.
`sites-web-pro-claude.html`).

**Copier la structure exacte d'une page existante** — `ressources/skill-design-web.html` est le
gabarit de référence. Ne pas inventer un nouveau layout : le CSS de page est inline dans chaque
fichier et la cohérence visuelle du catalogue en dépend.

Squelette obligatoire (dans cet ordre) :

```
<head> : title "<Titre> – AutomationBoost", meta description,
         <link rel="stylesheet" href="../assets/css/style.css">,
         favicon ../assets/images/favicon.svg,
         <style> inline (copier tel quel depuis skill-design-web.html)
<nav id="navbar"> : logo + lien "← Ressources" vers ../ressources.html
<section class="res-page">
  .breadcrumb        → <a href="../ressources.html">Ressources</a> / <Titre>
  .page-badge        → "▶ Vidéo · <durée>" ou "◈ Article"
  .page-title        → titre avec un <span> doré sur les 2-3 mots clés
  .page-meta         → 3 champs séparés par "·" (outil · thème · niveau)
  .content-block     → h2 / p / ul / .tip-box / .code-block
  .source-cta        → lien vers la source (vidéo, repo, doc officielle)
  .nav-back          → "← Retour aux ressources"
<script> : toggle .scrolled sur le navbar au scroll
```

**Contenu — le minimum qui rend la page utile :**
- Ce que c'est, en une phrase, sans jargon.
- **Les commandes exactes** dans des `.code-block` (copiables tels quels).
- Au moins une `.tip-box` avec un piège réel rencontré en production.
- Ce à quoi s'attendre comme résultat.

Écrire en français, tutoiement, ton direct — la même voix que la vidéo. Pas d'emoji dans les titres.

### Étape 2 — Ajouter la carte dans `ressources.html`

La grille est en dur dans `automationboost/ressources.html` (section `.resources-grid`).
**Insérer la nouvelle carte en position 1**, juste après `<!-- === RESSOURCES CLAUDE CODE (originales) === -->`,
avant la carte `<!-- 1 -->` — la plus récente est en tête.

```html
<a href="ressources/<slug>.html" class="res-card" data-type="video">
  <div class="card-top">
    <span class="card-badge badge-video">▶ Vidéo</span>
    <span class="card-duration">33s</span>
    <span class="card-number">#00</span>
  </div>
  <div class="card-title"><Titre court></div>
  <div class="card-desc"><2 phrases : la promesse + le bénéfice concret></div>
  <div class="card-cta">Voir la ressource →</div>
</a>
```

- `data-type` doit correspondre à un des filtres existants, sinon la carte disparaît quand on filtre :
  `video`, `comprendre`, `prompter`, `temps`, `contenu`, `quotidien`, `agents`, `business`, `workflow`.
- Ne pas renuméroter toutes les cartes existantes (`#01`, `#02`...) — c'est cosmétique et ça pollue
  le diff. Donner un numéro libre à la nouvelle.
- **Mettre à jour les compteurs** de `.res-stats` en haut de page (`<span>190</span> ressources`,
  `<span>3</span> vidéos`, `<span>175</span> articles`) — incrémenter le total ET la catégorie.

### Étape 3 — Vérifier avant de déployer

Servir le site en local et regarder la page pour de vrai (Playwright, pas juste un grep) :

```bash
node serve.mjs /work/automationboost 8090 &     # petit serveur statique (voir reel-remix)
node -e "..."                                   # playwright screenshot de /ressources/<slug>.html
```

Vérifier :
- [ ] La page s'affiche avec le CSS du site (pas de style cassé → chemin `../assets/css/style.css`)
- [ ] La carte apparaît en tête de la grille `/ressources`
- [ ] Le filtre correspondant à `data-type` affiche bien la carte
- [ ] Les compteurs `.res-stats` sont cohérents

### Étape 4 — Déployer via `deploy-to-coolify`

`automationboost` est un **sous-module git**. Toujours dans cet ordre :

1. **Commiter dans le sous-module d'abord**, et **seulement les fichiers de cette ressource** —
   `automationboost` a souvent des modifications en cours qui ne t'appartiennent pas :
   ```bash
   cd automationboost
   git add ressources/<slug>.html ressources.html
   git commit -m "feat(ressources): add <slug> resource page"
   git push origin main
   ```
   Ne **jamais** faire `git add -A` ici (le script `deploy.sh` du skill coolify-deploy le fait —
   d'où l'obligation de commiter/pousser proprement soi-même AVANT de l'appeler).
2. Mettre à jour la référence du sous-module dans le repo parent.
3. Invoquer `/deploy-to-coolify automationboost` — le skill pousse, met à jour l'app Coolify,
   attend le statut `running` et vérifie le HTTP 200.
4. Vérifier l'URL finale de la page : `https://automatisationboost.com/ressources/<slug>.html`.

### Étape 5 — Boucler avec la vidéo

- Donner l'URL de la ressource à l'utilisateur : c'est ce qu'il enverra en DM aux gens qui
  commentent le mot-clé.
- Si un workflow n8n répond automatiquement aux commentaires (mot-clé → DM), c'est **là** qu'il faut
  déclarer le couple `<MOTCLÉ> → <URL>`. Ne pas supposer que c'est automatique : le demander à
  l'utilisateur.
- Mettre à jour le Google Sheet de suivi via le webhook `sheet-video-update` (voir `veille-to-video`
  Étape 9) si la vidéo y a une ligne.

---

## Checklist finale

- [ ] Promesse du CTA relue dans `narration.txt` et tenue littéralement par la page
- [ ] Doublon vérifié dans `ressources/` avant d'écrire
- [ ] Page construite sur le gabarit `skill-design-web.html` (CSS inline copié, pas réinventé)
- [ ] Commandes exactes en `.code-block`, au moins une `.tip-box` avec un vrai piège
- [ ] Carte insérée en tête de grille, `data-type` = un filtre existant
- [ ] Compteurs `.res-stats` incrémentés
- [ ] Rendu vérifié visuellement en local (Playwright), pas seulement par grep
- [ ] Sous-module commité/poussé **avant** l'appel à `/deploy-to-coolify`, sans `git add -A`
- [ ] URL finale vérifiée en HTTP 200 et communiquée à l'utilisateur

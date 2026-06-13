# Design : Organisation des sites freelance dans Coolify

**Date :** 2026-04-10  
**Projet Coolify :** `freelance-site` (uuid: `rgcs00kg440w0cw84oow8kw0`)

## Objectif

Catégoriser ~70 sites web templates déployés sur Coolify et les regrouper dans le projet `freelance-site` avec un environnement par catégorie.

## Catégories (environnements)

| Environnement | Description | Exemples de sites |
|---|---|---|
| `restaurants` | Restaurants, pizzerias, snacks, boulangeries, traiteurs | pizza-e-basta, le-bistrot-saint-paul, mamzelle-pizza, dalilo-pizza, cassava-micro-boulangerie, le-bonbon-de-pain, o-metis-s-traiteur, guinguette-du-grand-morin, les-brillantes-gorgees, restaurant-coulee77, restaurant-franco-portugais, restaurant-la-parenthese, le786-halal, planb-restaurant, oncle-sam-saveurs, mio-pizza, limperiale-pizzeria, mamabetty, le-comptoir, le-relais-commerson, reatchy-snackbar, pizzas-les-mascareignes, pizza-shake, dan-cake |
| `hotels-tourisme` | Hôtels, gîtes, agences de voyage | hotel-austral-saint-denis, casas-ferias-saint-andre, transcontinents-voyages-ile-maurice, sud-hotel-reunion |
| `peche-sport` | Pêche, sports, guides outdoor | guide-peche-reunion-ttfishing, guide-peche-mouche-reunion, blue-peche-au-gros, peche-au-gros-reunion, beausejour-sportclub, centre-sante-sport-performance |
| `sante` | Santé, formation médicale, bien-être | arts-de-sante-formation, centre-hospitalier-ouest-reunion, gep-sante-reunion |
| `commerce` | Commerce, immobilier, industrie | bigmat-brico400-quincaillerie-tampon, top-moteur-oi-pieces-auto-reunion, topaze-strada-italian-products, sphb-production-huiles-bourbon, koytcha-immo-reunion |
| `media-photo` | Médias, photographie, radio | myselfie-studio-tarifs-2025, tarifs-photobooth-reunion, freedom-la-reunion-actualites, sunlightfm-optimisation-seo |
| `seo-optimisation` | Sites d'optimisation SEO | lacasearepas-optimisation-seo, latelier-de-ben-optimisation-seo, seo-optimisation-site, sistbi-optimisation-seo, sphb-production-huiles-optimisation, sphb-production-huiles-optimise, vtc-reunion-optimisation, clos_de_la_riviere_seo_optimisation, sunlightfm-optimisation-seo (doublon SEO), reatchy-snackbar-optimisation |
| `transport` | VTC, transport | vtc-reunion-felixtransports |

## Gestion des doublons

Règle : **garder les apps `running`, supprimer les apps `exited:unhealthy`**.

Apps avec doublons identifiés :
- `clicknvan-location-vans-campingcars-pro` (x3)
- `sphb-production-huiles-bourbon` (x3)
- `pizza-e-basta-saint-pierre` (x2)
- `oncle-sam-saveurs-reunion` (x2)
- `restaurant-la-parenthese-saint-gilles` (x2 dont 1 exited)
- `transcontinents-voyages-ile-maurice` (x2)
- `sunlightfm-optimisation-seo` (x2)
- `vtc-reunion-optimisation` (x2)
- `instagram-login-optimized` (x2)

## Plan technique

### Étape 1 — Créer les 8 environnements dans `freelance-site`
Via `mcp__coolify__environments` action `create`.

### Étape 2 — Supprimer les doublons exited
Via `mcp__coolify__application` action `delete` pour les apps `exited:unhealthy`.

### Étape 3 — Déplacer les apps
Via `mcp__coolify__application` action `update` avec le nouvel `environment_uuid`.

### Fallback
Si l'API ne supporte pas le changement d'`environment_uuid` via `update` → produire un fichier `freelance-sites-mapping.md` documentant le mapping catégorie/sites sans déplacer physiquement.

## Projet Coolify cible

- **Projet :** `freelance-site`
- **UUID :** `rgcs00kg440w0cw84oow8kw0`
- **Environnement existant :** `production` (uuid: `p8soskowk4wkkw8gcog00s48`) → à réutiliser ou supprimer

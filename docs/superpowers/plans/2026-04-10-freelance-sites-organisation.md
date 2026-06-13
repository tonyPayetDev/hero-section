# Freelance Sites Organisation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Organiser ~70 sites freelance dans le projet Coolify `freelance-site` avec 9 environnements par catégorie, en supprimant les doublons.

**Architecture:** Opérations API Coolify séquentielles — création d'environnements, suppression des doublons, déplacement des apps via `application update` avec `environment_uuid`.

**Tech Stack:** Coolify MCP (`mcp__coolify__environments`, `mcp__coolify__application`)

---

## Référence : Projet cible

- **Projet :** `freelance-site`
- **UUID projet :** `rgcs00kg440w0cw84oow8kw0`
- **Env existant :** `production` (uuid: `p8soskowk4wkkw8gcog00s48`) → sera conservé ou supprimé après migration

---

## Référence : Mapping apps → catégories

### restaurants
| UUID | Nom |
|------|-----|
| `rcow80800so4cwocosgc4gsk` | boutique-restaurant-coulee77 |
| `k8c8sgosc0c8s4gkcw0c0844` | cassava-micro-boulangerie |
| `xc080o4cw4sgcowsw84g4w8c` | cassava-micro-boulangerie-reunion |
| `sow0k8ss00cwsgs8g88okwkc` | dalilo-pizza-tampon |
| `pogc8coc08skgk0owc0skoko` | dan-cake-patisserie |
| `lk4o4cc0ok0oggo08gsgsggo` | guinguette-du-grand-morin-eatbu-com- |
| `r8wc4wwg8w0o48g8cgo88k8k` | la-kaz-de-ben |
| `ww0wk0wgw0cgo4kwo40gkcsk` | latelier-de-ben-site |
| `rc44484084oos04888c4g0gc` | le-bistrot-saint-paul |
| `d4ssokgwcksokc4ckcsokkok` | le-bonbon-de-pain |
| `agso48w8ccwcg448o0ss4w0w` | le-bonbon-de-pain-snack-atchia |
| `qg44gcwo4s48w8k8g0kkk4og` | le-comptoir-saint-michel-nancy |
| `hwww400og0gg4c08kkgwww0g` | le-majeur-nancy |
| `xws8w0wss4sk00wggocc4g0c` | le-relais-commerson-tampon |
| `xcgcwkwkw00o0ooc8c8o88cg` | le786-halal-commande-en-ligne |
| `a8g80g8kw04gsw0kksgwc0w4` | les-brillantes-gorgees |
| `c8og44sow8ogso8o8wo4w0kc` | limperiale-pizzeria-kazumi |
| `nswks4o8088k040ogo4cg80k` | mamabetty-fr-site |
| `rg8ko0wsgcc4swco0sogo8sk` | mamzelle-pizza-ile-reunion |
| `x4so0k8kkwsgoc8og0gow008` | mio-pizza-la-reunion |
| `psoosgw00cgooss8wkkss4co` | o-metis-s-traiteur-saint-andre |
| `xs8kc80ossgc8sgkskk0sw8k` | oncle-sam-saveurs-reunion (GARDER) |
| `u0wcs84s0wwwc8c484wsc40g` | pizza-e-basta-saint-pierre (GARDER) |
| `h400cock0gs4so44g4csscc8` | pizza-shake-saint-pierre |
| `iog00k0s8okc0wk0sgsg0wck` | pizzas-les-mascareignes |
| `hgkw4sgwwg4cg888wo4ggo4c` | planb-restaurant-burgers-saint-denis |
| `d8swkc8c4sw8gkg4wwokwgww` | restaurant-coulee77 |
| `hw84s44wkcw8o0ccow08wgs0` | restaurant-franco-portugais-coulommiers |
| `rk8gs088kk8cg8gwsk08kwo4` | restaurant-la-parenthese-latitude21 |
| `jk0wkogwkg4kgcg48skwgcw0` | restaurant-la-parenthese-saint-gilles (GARDER) |
| `us8o88ws04csg0gsgooocwc0` | restaurant-la-piscine-melun |

### hotels-tourisme
| UUID | Nom |
|------|-----|
| `l8sc44s040o4wss8sgccss8w` | casas-ferias-saint-andre |
| `osk00wkw44cs4wg0w0ow0owk` | hotel-austral-saint-denis |
| `dwsww0gw8gos0ccos8s4kw8c` | sud-hotel-reunion |
| `wgk0ook88og8ksos4wgwk8cg` | transcontinents-voyages-ile-maurice (GARDER) |

### peche-sport
| UUID | Nom |
|------|-----|
| `ngcgkokkg4o4gs00kckc0w40` | beausejour-sportclub |
| `t0sc40wc0kgc0w4gcwso8g8s` | blue-peche-au-gros |
| `jkkwckkc0oswg4ggcg8k8w8c` | centre-sante-sport-performance-la-reunion |
| `og84ksw0kwoc8s0wkwggck84` | guide-peche-mouche-reunion-verdon-alpes |
| `t4cgws08cw4skgkwgwkwkgw8` | guide-peche-reunion-ttfishing |
| `bscwo8sks0gwws0w4080o0sw` | peche-au-gros-reunion |

### sante
| UUID | Nom |
|------|-----|
| `g800o84sggkok4sog4kcgwoc` | arts-de-sante-formation |
| `f0w0kkss0oocswwcgws044o4` | centre-hospitalier-ouest-reunion |
| `ocwoogk8kwswk4c4gg008skc` | gep-sante-reunion |

### commerce
| UUID | Nom |
|------|-----|
| `j8soks8go0www4wwwow084gs` | bigmat-brico400-quincaillerie-tampon |
| `lsk00gkc8o884k40448wcc00` | koytcha-immo-reunion |
| `zk088kwo0okwcgs4ccs8ss4k` | sphb-production-huiles-bourbon (GARDER) |
| `j4cgkc8ksoc04goo8c40084c` | top-moteur-oi-pieces-auto-reunion |
| `xs0swo40gok44ccw8gcs00g4` | topaze-strada-italian-products |

### media-photo
| UUID | Nom |
|------|-----|
| `uskccsokkoc040gcg4840wwg` | freedom-la-reunion-actualites |
| `gkc8ow4o0goow0kgcgocwo84` | myselfie-studio-tarifs-2025 |
| `gc4k8o80socsw0c8gkk4c8w8` | tarifs-photobooth-reunion |

### seo-optimisation
| UUID | Nom |
|------|-----|
| `r844w0g48088k48ko84oc0ck` | clos_de_la_riviere_seo_optimisation |
| `oowsg0w8c8s8wkccg8c4osc0` | lacasearepas-optimisation-seo |
| `k00so4gwooo4s040gc8okc0o` | latelier-de-ben-optimisation-seo |
| `c8c8k4g880gcoc4ss08g8o44` | reatchy-snackbar-optimisation |
| `eoo0wkw8w00cok4scw8ks8ks` | seo-optimisation-site |
| `a04g0ocwggwk00swcw8cgooo` | sistbi-optimisation-seo |
| `q8kggg8kogcgg00w0o448k4o` | sphb-production-huiles-optimisation |
| `l4kw0c8kwsog804wsogwo00c` | sphb-production-huiles-optimise |
| `rwsc484ko40ks8sgkwoskc04` | sunlightfm-optimisation-seo (GARDER) |
| `l80cgc08sos8owcsg0g0ksoo` | vtc-reunion-optimisation (GARDER) |

### transport
| UUID | Nom |
|------|-----|
| `escs0gc0g4csc8s08g0w8cok` | clicknvan-location-vans-campingcars-pro (GARDER) |
| `ksccc8osogwo8wooo4c4k4kw` | vtc-reunion-felixtransports |

### divers
| UUID | Nom |
|------|-----|
| `ewgco80sc4so00o8g0g04oc4` | bloom-reunion |
| `vckgsg44oook8c0c8s44woos` | educateur-canin-la-reunion |
| `fwocoo0os8kw4sw0808kc444` | instagram-login-optimized (GARDER) |
| `o48oggcwc8wg800g4wkwgoss` | menuforge |
| `noco48g4gskk80wwg0woc40g` | site-minimaliste |

---

## Apps à supprimer (doublons / exited)

| UUID | Nom | Raison |
|------|-----|--------|
| `n4c4kwkw8k0ogkgccc0kowcw` | restaurant-la-parenthese-saint-gilles | exited:unhealthy |
| `bggcgkk844o4ko40kk80g08s` | oncle-sam-saveurs-reunion | doublon running |
| `v80kwggwocwk0ww08sgc84kk` | pizza-e-basta-saint-pierre | doublon running |
| `ag8g4w4kos80sgk4g0csc88o` | clicknvan-location-vans-campingcars-pro | doublon running |
| `zwcww0c4k4kokccggk448soc` | clicknvan-location-vans-campingcars-pro | doublon running |
| `o0ww8s88g0kkc8cc0wos0ggc` | sphb-production-huiles-bourbon | doublon running |
| `voso0kgwowcc8cocsgcwsww8` | sphb-production-huiles-bourbon | doublon running |
| `zowookos4wckwg08gkkoosoo` | transcontinents-voyages-ile-maurice | doublon running |
| `tg4o8g0ggswgwgw8c08g0c4w` | sunlightfm-optimisation-seo | doublon running |
| `i04sgg08cs4sg4o800kg0w00` | vtc-reunion-optimisation | doublon running |
| `qkgo44kwgcg40cok80k884os` | instagram-login-optimized | doublon running |

---

## Task 1 : Créer les 9 environnements dans `freelance-site`

**Action :** `mcp__coolify__environments` → `create` × 9

- [ ] **Step 1 : Créer env `restaurants`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: restaurants
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_RESTAURANTS`

- [ ] **Step 2 : Créer env `hotels-tourisme`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: hotels-tourisme
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_HOTELS`

- [ ] **Step 3 : Créer env `peche-sport`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: peche-sport
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_SPORT`

- [ ] **Step 4 : Créer env `sante`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: sante
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_SANTE`

- [ ] **Step 5 : Créer env `commerce`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: commerce
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_COMMERCE`

- [ ] **Step 6 : Créer env `media-photo`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: media-photo
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_MEDIA`

- [ ] **Step 7 : Créer env `seo-optimisation`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: seo-optimisation
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_SEO`

- [ ] **Step 8 : Créer env `transport`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: transport
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_TRANSPORT`

- [ ] **Step 9 : Créer env `divers`**
  ```
  action: create
  project_uuid: rgcs00kg440w0cw84oow8kw0
  name: divers
  ```
  Vérifier : réponse contient un UUID → noter comme `ENV_DIVERS`

- [ ] **Step 10 : Vérifier les 9 environnements**
  ```
  action: list
  project_uuid: rgcs00kg440w0cw84oow8kw0
  ```
  Attendu : 10 environnements (production + 9 nouveaux)

---

## Task 2 : Supprimer les doublons / apps exited

- [ ] **Step 1 : Supprimer restaurant-la-parenthese-saint-gilles (exited)**
  ```
  action: delete
  uuid: n4c4kwkw8k0ogkgccc0kowcw
  ```

- [ ] **Step 2 : Supprimer oncle-sam doublon**
  ```
  action: delete
  uuid: bggcgkk844o4ko40kk80g08s
  ```

- [ ] **Step 3 : Supprimer pizza-e-basta doublon**
  ```
  action: delete
  uuid: v80kwggwocwk0ww08sgc84kk
  ```

- [ ] **Step 4 : Supprimer clicknvan doublons (2)**
  ```
  action: delete
  uuid: ag8g4w4kos80sgk4g0csc88o
  ```
  puis
  ```
  action: delete
  uuid: zwcww0c4k4kokccggk448soc
  ```

- [ ] **Step 5 : Supprimer sphb-huiles-bourbon doublons (2)**
  ```
  action: delete
  uuid: o0ww8s88g0kkc8cc0wos0ggc
  ```
  puis
  ```
  action: delete
  uuid: voso0kgwowcc8cocsgcwsww8
  ```

- [ ] **Step 6 : Supprimer transcontinents doublon**
  ```
  action: delete
  uuid: zowookos4wckwg08gkkoosoo
  ```

- [ ] **Step 7 : Supprimer sunlightfm doublon**
  ```
  action: delete
  uuid: tg4o8g0ggswgwgw8c08g0c4w
  ```

- [ ] **Step 8 : Supprimer vtc-optimisation doublon**
  ```
  action: delete
  uuid: i04sgg08cs4sg4o800kg0w00
  ```

- [ ] **Step 9 : Supprimer instagram doublon**
  ```
  action: delete
  uuid: qkgo44kwgcg40cok80k884os
  ```

---

## Task 3 : Tester le déplacement d'app (validation API)

- [ ] **Step 1 : Tester le déplacement avec une app test**
  Déplacer `bloom-reunion` vers l'env `divers` (UUID noté dans Task 1 Step 9) :
  ```
  action: update
  uuid: ewgco80sc4so00o8g0g04oc4
  environment_uuid: <ENV_DIVERS>
  ```

- [ ] **Step 2 : Vérifier le déplacement**
  ```
  get_application uuid: ewgco80sc4so00o8g0g04oc4
  ```
  Attendu : `environment_id` correspond à `divers`

  **Si ÉCHEC (API ne supporte pas le déplacement) :** Arrêter Tasks 4-12 et exécuter Task 13 (fallback documentation)

---

## Task 4 : Déplacer apps → `restaurants`

Utiliser l'UUID `ENV_RESTAURANTS` obtenu en Task 1.

- [ ] Déplacer `rcow80800so4cwocosgc4gsk` (boutique-restaurant-coulee77)
- [ ] Déplacer `k8c8sgosc0c8s4gkcw0c0844` (cassava-micro-boulangerie)
- [ ] Déplacer `xc080o4cw4sgcowsw84g4w8c` (cassava-micro-boulangerie-reunion)
- [ ] Déplacer `sow0k8ss00cwsgs8g88okwkc` (dalilo-pizza-tampon)
- [ ] Déplacer `pogc8coc08skgk0owc0skoko` (dan-cake-patisserie)
- [ ] Déplacer `lk4o4cc0ok0oggo08gsgsggo` (guinguette-du-grand-morin)
- [ ] Déplacer `r8wc4wwg8w0o48g8cgo88k8k` (la-kaz-de-ben)
- [ ] Déplacer `ww0wk0wgw0cgo4kwo40gkcsk` (latelier-de-ben-site)
- [ ] Déplacer `rc44484084oos04888c4g0gc` (le-bistrot-saint-paul)
- [ ] Déplacer `d4ssokgwcksokc4ckcsokkok` (le-bonbon-de-pain)
- [ ] Déplacer `agso48w8ccwcg448o0ss4w0w` (le-bonbon-de-pain-snack-atchia)
- [ ] Déplacer `qg44gcwo4s48w8k8g0kkk4og` (le-comptoir-saint-michel-nancy)
- [ ] Déplacer `hwww400og0gg4c08kkgwww0g` (le-majeur-nancy)
- [ ] Déplacer `xws8w0wss4sk00wggocc4g0c` (le-relais-commerson-tampon)
- [ ] Déplacer `xcgcwkwkw00o0ooc8c8o88cg` (le786-halal-commande-en-ligne)
- [ ] Déplacer `a8g80g8kw04gsw0kksgwc0w4` (les-brillantes-gorgees)
- [ ] Déplacer `c8og44sow8ogso8o8wo4w0kc` (limperiale-pizzeria-kazumi)
- [ ] Déplacer `nswks4o8088k040ogo4cg80k` (mamabetty-fr-site)
- [ ] Déplacer `rg8ko0wsgcc4swco0sogo8sk` (mamzelle-pizza-ile-reunion)
- [ ] Déplacer `x4so0k8kkwsgoc8og0gow008` (mio-pizza-la-reunion)
- [ ] Déplacer `psoosgw00cgooss8wkkss4co` (o-metis-s-traiteur-saint-andre)
- [ ] Déplacer `xs8kc80ossgc8sgkskk0sw8k` (oncle-sam-saveurs-reunion)
- [ ] Déplacer `u0wcs84s0wwwc8c484wsc40g` (pizza-e-basta-saint-pierre)
- [ ] Déplacer `h400cock0gs4so44g4csscc8` (pizza-shake-saint-pierre)
- [ ] Déplacer `iog00k0s8okc0wk0sgsg0wck` (pizzas-les-mascareignes)
- [ ] Déplacer `hgkw4sgwwg4cg888wo4ggo4c` (planb-restaurant-burgers-saint-denis)
- [ ] Déplacer `d8swkc8c4sw8gkg4wwokwgww` (restaurant-coulee77)
- [ ] Déplacer `hw84s44wkcw8o0ccow08wgs0` (restaurant-franco-portugais-coulommiers)
- [ ] Déplacer `rk8gs088kk8cg8gwsk08kwo4` (restaurant-la-parenthese-latitude21)
- [ ] Déplacer `jk0wkogwkg4kgcg48skwgcw0` (restaurant-la-parenthese-saint-gilles)
- [ ] Déplacer `us8o88ws04csg0gsgooocwc0` (restaurant-la-piscine-melun)

---

## Task 5 : Déplacer apps → `hotels-tourisme`

- [ ] Déplacer `l8sc44s040o4wss8sgccss8w` (casas-ferias-saint-andre)
- [ ] Déplacer `osk00wkw44cs4wg0w0ow0owk` (hotel-austral-saint-denis)
- [ ] Déplacer `dwsww0gw8gos0ccos8s4kw8c` (sud-hotel-reunion)
- [ ] Déplacer `wgk0ook88og8ksos4wgwk8cg` (transcontinents-voyages-ile-maurice)

---

## Task 6 : Déplacer apps → `peche-sport`

- [ ] Déplacer `ngcgkokkg4o4gs00kckc0w40` (beausejour-sportclub)
- [ ] Déplacer `t0sc40wc0kgc0w4gcwso8g8s` (blue-peche-au-gros)
- [ ] Déplacer `jkkwckkc0oswg4ggcg8k8w8c` (centre-sante-sport-performance-la-reunion)
- [ ] Déplacer `og84ksw0kwoc8s0wkwggck84` (guide-peche-mouche-reunion-verdon-alpes)
- [ ] Déplacer `t4cgws08cw4skgkwgwkwkgw8` (guide-peche-reunion-ttfishing)
- [ ] Déplacer `bscwo8sks0gwws0w4080o0sw` (peche-au-gros-reunion)

---

## Task 7 : Déplacer apps → `sante`

- [ ] Déplacer `g800o84sggkok4sog4kcgwoc` (arts-de-sante-formation)
- [ ] Déplacer `f0w0kkss0oocswwcgws044o4` (centre-hospitalier-ouest-reunion)
- [ ] Déplacer `ocwoogk8kwswk4c4gg008skc` (gep-sante-reunion)

---

## Task 8 : Déplacer apps → `commerce`

- [ ] Déplacer `j8soks8go0www4wwwow084gs` (bigmat-brico400-quincaillerie-tampon)
- [ ] Déplacer `lsk00gkc8o884k40448wcc00` (koytcha-immo-reunion)
- [ ] Déplacer `zk088kwo0okwcgs4ccs8ss4k` (sphb-production-huiles-bourbon)
- [ ] Déplacer `j4cgkc8ksoc04goo8c40084c` (top-moteur-oi-pieces-auto-reunion)
- [ ] Déplacer `xs0swo40gok44ccw8gcs00g4` (topaze-strada-italian-products)

---

## Task 9 : Déplacer apps → `media-photo`

- [ ] Déplacer `uskccsokkoc040gcg4840wwg` (freedom-la-reunion-actualites)
- [ ] Déplacer `gkc8ow4o0goow0kgcgocwo84` (myselfie-studio-tarifs-2025)
- [ ] Déplacer `gc4k8o80socsw0c8gkk4c8w8` (tarifs-photobooth-reunion)

---

## Task 10 : Déplacer apps → `seo-optimisation`

- [ ] Déplacer `r844w0g48088k48ko84oc0ck` (clos_de_la_riviere_seo_optimisation)
- [ ] Déplacer `oowsg0w8c8s8wkccg8c4osc0` (lacasearepas-optimisation-seo)
- [ ] Déplacer `k00so4gwooo4s040gc8okc0o` (latelier-de-ben-optimisation-seo)
- [ ] Déplacer `c8c8k4g880gcoc4ss08g8o44` (reatchy-snackbar-optimisation)
- [ ] Déplacer `eoo0wkw8w00cok4scw8ks8ks` (seo-optimisation-site)
- [ ] Déplacer `a04g0ocwggwk00swcw8cgooo` (sistbi-optimisation-seo)
- [ ] Déplacer `q8kggg8kogcgg00w0o448k4o` (sphb-production-huiles-optimisation)
- [ ] Déplacer `l4kw0c8kwsog804wsogwo00c` (sphb-production-huiles-optimise)
- [ ] Déplacer `rwsc484ko40ks8sgkwoskc04` (sunlightfm-optimisation-seo)
- [ ] Déplacer `l80cgc08sos8owcsg0g0ksoo` (vtc-reunion-optimisation)

---

## Task 11 : Déplacer apps → `transport`

- [ ] Déplacer `escs0gc0g4csc8s08g0w8cok` (clicknvan-location-vans-campingcars-pro)
- [ ] Déplacer `ksccc8osogwo8wooo4c4k4kw` (vtc-reunion-felixtransports)

---

## Task 12 : Déplacer apps → `divers`

(bloom-reunion déjà déplacé en Task 3 comme test)

- [ ] Déplacer `vckgsg44oook8c0c8s44woos` (educateur-canin-la-reunion)
- [ ] Déplacer `fwocoo0os8kw4sw0808kc444` (instagram-login-optimized)
- [ ] Déplacer `o48oggcwc8wg800g4wkwgoss` (menuforge)
- [ ] Déplacer `noco48g4gskk80wwg0woc40g` (site-minimaliste)

---

## Task 13 (FALLBACK) : Documentation si l'API ne supporte pas le déplacement

Si Task 3 échoue, créer `docs/freelance-sites-mapping.md` avec le tableau complet catégorie/UUID/nom pour référence manuelle dans l'interface Coolify.

---

## Task 14 : Vérification finale

- [ ] **Step 1 : Lister les environnements du projet**
  ```
  action: list
  project_uuid: rgcs00kg440w0cw84oow8kw0
  ```
  Attendu : 10 environnements avec des apps dans chaque catégorie

- [ ] **Step 2 : Vérifier counts par catégorie**
  - restaurants : 31 apps
  - hotels-tourisme : 4 apps
  - peche-sport : 6 apps
  - sante : 3 apps
  - commerce : 5 apps
  - media-photo : 3 apps
  - seo-optimisation : 10 apps
  - transport : 2 apps
  - divers : 5 apps

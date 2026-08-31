---
name: veille-journal-ia
description: Produit le "Journal IA" quotidien d'Automation Boost — une vidéo sociale 9:16 de 45s à 1min qui résume l'actu IA du jour, publiée chaque matin. La recherche web est faite par la routine cloud (qui écrit journal-ia/AAAA-MM-JJ.md dans le repo previsualisation) ; le RENDU et la PUBLICATION sont faits ici par un SCRIPT DÉTERMINISTE (render-publish.sh), sans agent dans la boucle. Ton info + running gags ("c'est indéniable… irréfutable… indiscutable"), CTA VEILLE, charte néon, avatar v3, voix clonée. Déclencheurs : "journal IA", "veille du jour", "résumé actu IA", "vidéo veille quotidienne", "lance le journal".
---

# veille-journal-ia — Le Journal IA quotidien (Automation Boost)

**Output :** 1 vidéo 9:16, **45s-1min**, qui informe en un coup d'œil sur l'actu IA du jour.

## Architecture en deux moitiés

| Où | Quoi | Quand |
|---|---|---|
| **Cloud** (routine planifiée) | VRAIE recherche web → écrit `journal-ia/AAAA-MM-JJ.md` dans le repo `previsualisation` | chaque nuit |
| **Ici** (`render-publish.sh`) | voix clonée → compo → rendu → previsualisation → Blotato | chaque matin |

Le cloud **ne peut pas** rendre (pas de HyperFrames, pas de voix, pas de ffmpeg). Le rendu doit tourner sur cette machine.

## ⚡ La boucle quotidienne = un script, pas un agent

```bash
/work/.claude/skills/veille-journal-ia/render-publish.sh 2026-08-17
```

Options : `--no-publish` (rendu seul) · `--no-social` (previsualisation sans Blotato) ·
`--force` (rejoue même si la route existe) · `--at 2026-08-17T03:00:00Z` (créneau).

Dernière ligne de sortie : `STATUS: OK …` ou `STATUS: FAIL <raison>`.
Codes retour : `0` OK · `1` échec · `2` usage · `3` édition absente · `4` réservé.

Ce que le script fait, dans l'ordre :

1. **Édition** — `git fetch/pull` sur `/work/previsualisation`, lit `journal-ia/<DATE>.md`.
   Cherche sur `main` **et** sur la branche `origin/journal-ia-<DATE>` (la routine cloud
   pousse parfois sur une branche dédiée). Absent → `STATUS: FAIL` + code 3.
   *Idempotent* : si la route `journal-ia-<DATE>` existe déjà avec sa vidéo, sort en OK sans rien refaire.
2. **Parsing déterministe** (`lib/parse_edition.mjs`) — le `.md` → `edition.json` :
   date, N brèves (source / titre / sous-titre / chips de chiffres), running gags,
   mot-clé CTA, segments de voix (condensés à ~140 caractères pour tenir dans 45-60s),
   captions mot-à-mot avec accents néon. Aucun LLM, aucun réseau.
3. **Voix clonée** — webhook `tts-gen` + `voixUrl` archiviste, un appel par segment
   (3 en parallèle, 3 essais, cache disque), puis silences coupés + `atempo` 1.12 + `dynaudnorm`.
4. **Calage** (`lib/layout.mjs`) — mesure la durée réelle de chaque segment et pose la
   timeline. **La durée totale de la vidéo sort de l'audio**, pas d'une constante.
5. **Compo** (`lib/build_html.mjs` + `template/index.tpl.html`) — le template porte le
   LOOK (charte néon, fenêtre avatar, countdown, ligne beat), le builder injecte le
   CONTENU et génère la timeline GSAP pour N brèves et N gags.
6. **Audio + clips** (`lib/gen_ffmpeg.mjs`) — lit de voix, BGM ducké en sidechain,
   SFX posés sur les changements de plan, `loudnorm`. Clips avatar découpés de la banque.
7. **Rendu** — snapshot de contrôle puis `hyperframes render`, puis passe 2 ffmpeg
   (incrustation avatar + audio final) → `public/video.mp4`.
8. **Publication** — route `journal-ia-<DATE>` sur previsualisation (page + cover +
   entrée dans la galerie), commit + push + déclenchement Coolify, attente du HTTP 200.
9. **Blotato** (`lib/blotato.mjs`) — upload binaire (presigned + PUT brut, **jamais**
   l'URL previsualisation qui est 403 derrière Cloudflare) puis 5 posts programmés.

Chaque run écrit un log daté dans `logs/AAAA-MM-JJ-HHMMSS.log` et pose un `flock`
(`/tmp/journal-ia-<DATE>.lock`) pour qu'un run n'en double jamais un autre.

### Appel depuis n8n (SSH, sans agent, sans skip-permissions)

```bash
bash -lc '/work/.claude/skills/veille-journal-ia/render-publish.sh $(date -u +%F) 2>&1 | tail -40'
```

Le nœud n8n lit la dernière ligne : `STATUS: OK …` / `STATUS: FAIL …`, et le code retour.

### Pré-requis à poser une fois

- `/work/.deploy.env` → `GITHUB_TOKEN` (présent).
- `COOLIFY_ACCESS_TOKEN` / `COOLIFY_BASE_URL` dans l'env (présents via `.claude/settings.json`).
- **`/work/.blotato.env` → `BLOTATO_API_KEY=…`** (à récupérer dans la crédential Blotato de n8n).
  Sans elle, le script publie quand même sur previsualisation et écrit
  `work/blotato-plan.json` (caption + 5 cibles + créneau) : c'est alors à n8n de programmer,
  avec sa propre crédential. Le script sort en `STATUS: OK` dans ce cas.

## Charte / style verrouillé (cf. `veille-to-video-v3`)

Voix clonée `tts-gen` + `voixUrl` archiviste, atempo ~1.12, silences coupés, audio natif
des clips avatar coupé, avatar v3 qui **ponctue** (intro, gags, outro, CTA — pas en continu),
captions mot-à-mot, BGM duckée en sidechain, countdown 3-2-1, charte néon 9:16, 45s-1min.

## Pièges déjà payés (ne pas les réintroduire)

1. **`wait` nu + log tee** — `exec > >(tee -a LOG)` crée un process substitution que
   bash compte comme job. Un `wait` sans argument l'attend aussi → blocage définitif.
   Toujours attendre des **PID explicites** (`wait "${PIDS[@]}"`).
2. **`apad` sans borne** — `amix,apad,atrim=0:DUR` peut tourner à 100 % de CPU sans
   jamais finir (constaté sur l'édition du 16/08, 0 octet écrit en 3 min). Utiliser
   `apad=whole_dur=DUR` **et** `-t DUR` sur la sortie : double garde-fou.
3. **HyperFrames écrit dans `./renders/` relatif au cwd** et **ignore `--out`** : il faut
   `cd` dans le projet avant `render`, sinon le MP4 part ailleurs.
4. **La barre de progression du rendu n'écrit que des `\r`** : sans `tr '\r' '\n'` le log
   devient une seule ligne de 170 Ko.
5. **Cloudflare renvoie 403 sur les URL previsualisation** pour Blotato : toujours passer
   par l'upload binaire presigned + PUT.
6. **Coolify ne redéploie pas sur push** : il faut appeler `/api/v1/deploy?uuid=…` puis
   attendre le 200 avec un cache-buster (Cloudflare met les 404 en cache).

## Réglages

| Variable | Défaut | Effet |
|---|---|---|
| `JIA_BRIEF_CHARS` | 140 | budget de caractères parlés par brève (pilote la durée) |
| `JIA_GAP` / `JIA_LEAD` / `JIA_TAIL` | .40 / .45 / .55 | respiration entre segments |
| `JIA_AVATAR_BANK` | `_shared/avatar-bank/clips` | banque de clips avatar |
| `JIA_OUT_ROOT` | `/work/autoboost-neon-videos` | où sont créés les projets |
| `BLOTATO_API_KEY` | — | active la programmation automatique |

## Comptes de publication

TikTok `36488` (PUBLIC_TO_EVERYONE, isAiGenerated) · Instagram `54617` (reel, shareToFeed)
· YouTube `45006` (public, sans notification) · Facebook `43538` page `1288852254291983` (reel)
· LinkedIn `25882`. Gate commentaire **VEILLE** → DM.

## Checklist qualité (à l'œil, après le run)

- [ ] Durée entre 45 et 60 s (le script alerte sinon).
- [ ] 3-4 brèves, chiffres réels, sources réelles (elles viennent du `.md`, jamais inventées).
- [ ] 2 running gags placés après une brève.
- [ ] **Gags : MAXIMUM 2 adjectifs empilés, jamais 3.** « C'est indéniable. Irréfutable. Indiscutable. » = trop lourd (retour Tony 2026-08-17). Garder 2 mots forts et **varier le vocabulaire d'une édition à l'autre** : indéniable / irréfutable / indiscutable / incontestable / imparable / implacable / sans appel / formel / cash. Ne jamais réutiliser la même paire deux éditions de suite.
- [ ] Avatar visible sur intro / gags / outro / CTA uniquement.
- [ ] Route previsualisation en 200 avant toute programmation.

---

## ⚠️ PANNE DU 2026-08-21 — une édition sortie SANS AUCUNE INFO

**Ce qui s'est passé.** La routine cloud a fait son travail correctement : 14 recherches web,
5 sujets avec chacun une source datée, deux candidats écartés parce que trop vieux, et un
`journal-ia/2026-08-21.md` complet. Le rendu local a produit une vidéo de **18,9 s** contenant
l'intro, une phrase bouchon et le CTA. **Zéro actualité.**

**La cause.** Le prompt de la routine demandait de « varier les amorces, ne pas écrire cinq fois
Un —, Deux — ». La routine a obéi et a écrit `**Un.**` au lieu de `**Un — Titre.**`.
`parse_edition.mjs` n'acceptait que la forme à tiret → **0 brève parsée**.

**Pourquoi personne ne l'a vu.** La routine cloud a rendu `success`. Le rendu local a rendu
`success`. La page de prévisualisation affichait « 0 brèves » — personne ne l'a lue. Aucune
alerte nulle part. C'est le mode de panne le plus coûteux : tout est vert et le livrable est vide.

**Les deux corrections en place :**

1. `parse_edition.mjs` accepte les deux écritures (`**Un — Titre.**` et `**Un.**`, le titre étant
   alors pris sur la première phrase). Vérifié : 5 brèves sur le 21/08, 4 sur chacune des
   4 éditions précédentes, aucune régression.
2. `render-publish.sh` **refuse de rendre** en dessous de 3 brèves. C'est le garde-fou qui compte :
   un prompt peut toujours dériver, une vérification de sortie non.

**Règle générale à retenir** : ne jamais faire dépendre un parseur de la *façon dont une phrase est
tournée* par un agent en amont. Et toujours vérifier le livrable, jamais le statut.

## Programmation Blotato — la clé n'existe pas dans cet environnement

`lib/blotato.mjs` cherche `BLOTATO_API_KEY` dans l'environnement ou dans `/work/.blotato.env`.
**Ce fichier n'existe pas.** Le script écrit donc systématiquement un plan dans
`work/blotato-plan.json` et sort en annonçant « planification déléguée à l'appelant » — ce qui
veut dire, concrètement, que **rien n'est jamais programmé** si personne ne reprend le plan à la
main. Une édition peut donc être rendue, déployée, vérifiée en 200, et ne partir sur aucun réseau.

Depuis une session interactive, le **connecteur MCP Blotato fonctionne**. La marche à suivre :
lire le plan, uploader le MP4 via `blotato_create_presigned_upload_url` puis un PUT du binaire
(jamais l'URL previsualisation directement : Cloudflare renvoie 403), puis un `blotato_create_post`
par réseau. **Ne jamais publier sans l'accord explicite de Tony.**

## Vérifier, toujours

Avant d'annoncer qu'une édition est sortie, contrôler dans cet ordre :

| quoi | comment |
|---|---|
| brèves reconnues | la page de la route affiche « N brèves » — N doit valoir 4 ou 5, jamais 0 |
| durée | 45 s à 1 min ; une édition à moins de 30 s est forcément amputée |
| contenu à l'image | extraire 4-5 frames et les regarder — les cartes des brèves doivent y être |
| en ligne | HTTP 200 sur la route, et comparer le md5 servi au fichier local |
| programmé | `blotato_list_posts` — un plan écrit sur disque ne prouve rien |

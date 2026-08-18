---
name: inbox-instagram
description: Récupère mes posts Instagram enregistrés, transcrit les reels, extrait hook/angle/structure et range en fiches markdown par thème dans le second cerveau. À utiliser quand on demande de vider l'inbox Instagram, traiter les posts sauvegardés, alimenter le second cerveau, ou sortir des idées de contenu à partir de l'inspiration enregistrée.
---

# inbox-instagram — posts enregistrés → second cerveau

Transforme le bouton « enregistrer » d'Instagram en réserve d'idées exploitable.
Chaque post sauvegardé est récupéré, transcrit, décortiqué (hook · idée · pourquoi ça
marche · structure) et rangé dans `second-cerveau/<thème>.md`. Zéro base de données :
des fichiers markdown que Claude relit ensuite pour produire du contenu.

**Second cerveau :** `/work/second-cerveau/`
**Scripts :** `/work/.claude/skills/inbox-instagram/scripts/`

## Répartition du travail

Les scripts font l'I/O déterministe (récupérer, télécharger, transcrire, écrire, dédupliquer).
**L'analyse — hook, angle, structure, thème — c'est toi qui la fais**, en lisant les fichiers
bruts. Ne délègue jamais l'analyse à un script : c'est tout l'intérêt du système.

## Prérequis

Instagram refuse tout, même les posts publics, sans session. **Les cookies sont obligatoires**,
pas optionnels.

1. Dans un navigateur connecté à Instagram, exporte les cookies au format Netscape
   (extension « Get cookies.txt LOCALLY » ou équivalent).
2. Place le fichier ici :

```
~/.config/inbox-instagram/cookies.txt
```

Alternative sans fichier : `export IG_COOKIE="sessionid=...; ds_user_id=...; csrftoken=..."`.

Node est à `/home/claude/tools/node/bin`, yt-dlp à `/home/claude/tools/bin`. Préfixe toujours :

```bash
export PATH="/home/claude/tools/node/bin:/home/claude/tools/bin:$PATH"
```

## Le run complet

### 1. Lister les posts enregistrés

```bash
S=/work/.claude/skills/inbox-instagram/scripts
node $S/ig-saved.mjs --out /tmp/saved.json            # via la session (défaut)
node $S/ig-saved.mjs --export ~/Downloads/instagram-export --out /tmp/saved.json   # via l'export IG
```

`--limit N` pour un run court. Le mode session pagine avec une pause aléatoire entre
chaque page — ne la retire pas, c'est ce qui évite de se faire rate-limiter.

Si l'API renvoie 401/403 : la session a expiré, il faut ré-exporter les cookies.
Ne contourne pas, ne réessaie pas en boucle.

### 2. Télécharger + transcrire

```bash
node $S/fetch-post.mjs --in /tmp/saved.json --brain /work/second-cerveau --limit 15
```

Produit `second-cerveau/_raw/<shortcode>/meta.json` et, quand la transcription aboutit,
`transcript.txt`. La vidéo est supprimée après transcription (`--keep-video` pour la garder).
Les posts déjà traités sont ignorés ; ceux qui ont échoué sont réessayés au run suivant.

**Cascade de transcription :** sous-titres yt-dlp → whisper local (`hyperframes transcribe`)
→ sinon `transcript_status: "pending"`.

Dans ce sandbox, whisper local est **indisponible** (`whisper_unavailable`, pas de
whisper-cpp ni de python). Pour les reels marqués `pending`, transcris via le MCP
`tokscript` (`get_instagram_transcript`, ~5/jour en gratuit) et écris le résultat
toi-même dans `_raw/<shortcode>/transcript.txt`. Sur une machine avec
`brew install yt-dlp whisper-cpp`, la cascade se règle toute seule.

### 3. Analyser et ranger — ton travail

Liste ce qui attend d'être classé :

```bash
node $S/brain.mjs --brain /work/second-cerveau --list
```

Pour chaque post, lis `_raw/<shortcode>/meta.json` (caption, auteur, likes) et
`transcript.txt` s'il existe, puis produis une fiche :

- **hook** — la première phrase, mot pour mot, celle qui arrête le scroll
- **idea** — l'idée en une phrase, reformulée, pas recopiée
- **why** — pourquoi ça marche (mécanique : tension, promesse, chiffre, contre-intuition…)
- **structure** — le squelette (ex. « hook accusateur → 3 preuves → CTA »)
- **theme** — thème court et réutilisable. **Réutilise un thème existant** (regarde les
  `.md` déjà présents) plutôt que d'en inventer un quasi-identique. Un thème par fiche.

Puis range :

```bash
echo '[{"shortcode":"ABC123","theme":"productivite","hook":"...","idea":"...","why":"...","structure":"..."}]' \
  | node $S/brain.mjs --brain /work/second-cerveau
```

La dédup est faite sur le marqueur `<!-- post:SHORTCODE -->` scanné dans **tous** les
fichiers de thème : rejouer le pipeline ne peut pas créer de doublon.

Traite par lots de 10-15 posts, pas un par un.

### 4. Exploiter le second cerveau

C'est l'usage final. Sur demande de Tony, lis les `.md` par thème et produis :
idées de reels avec hooks, scripts, carrousels, articles, compilations thématiques.

> « À partir de mon second cerveau, sors-moi 10 idées de reels sur la productivité, avec le hook de chaque. »
> « Prends les 5 meilleurs hooks du dossier et adapte-les à MON angle. »

Ne repars jamais des posts bruts pour ça : les fiches sont déjà l'état exploitable.

## Automatisation hebdo

```bash
0 9 * * 0 cd /work/second-cerveau && claude -p "Lance inbox-instagram"
```

Pas de `cron` dans ce sandbox — la ligne vaut pour la machine de Tony. Ici, utilise
`/schedule` (agent cloud) ou lance le skill à la demande.

## Contrôle

```bash
node $S/brain.mjs --brain /work/second-cerveau --stats
```

## Pièges

- **Pas de cookies = rien ne marche.** yt-dlp renvoie « empty media response », pas une
  erreur d'authentification claire. Vérifie les cookies avant de chercher ailleurs.
- **N'invente jamais un hook.** Si le transcript est `pending` et que la caption est vide,
  laisse le post non classé plutôt que de fabriquer une fiche.
- **Ne réécris pas un fichier de thème en entier** — `brain.mjs` fait un append. Éditer à la
  main un `.md` est permis, mais ne supprime pas les marqueurs `<!-- post:... -->` : ce sont
  eux qui empêchent les doublons.
- L'export Instagram ne contient que des liens, pas les médias : les cookies restent
  nécessaires pour transcrire.

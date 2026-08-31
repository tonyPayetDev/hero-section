# SFX palette v2 — Autoboost Neon Video

**v1 n'a pas été touchée.** `../v1/` reste figée et byte-identique : toute vidéo déjà rendue
garde exactement la palette avec laquelle elle a été montée. v2 = **tous les fichiers de v1
recopiés tels quels** + 10 sons d'**action physique** ajoutés le 2026-08-18.

Pourquoi v2 : retour de Tony sur `autoboost-62-meme-systeme` — « manque le sound design quand
il casse la vitre et lance la toile ». v1 est une palette d'**interface** (clics, notifications,
transitions). Elle n'a ni verre, ni impact corporel, ni vent, ni whip. Ces 10 fichiers comblent
ce trou et sont réutilisables sur tout hook d'action.

## Les 10 ajouts

| Fichier | Rôle | Durée | Pic (offset) | Source Mixkit |
|---|---|---|---|---|
| `sfx-wind-bed.mp3` | lit de vent continu (vol / chute / hauteur) | 2,90 s | 0,41 | #2658 *Wind blowing ambience* — extrait 12,0→14,9 s, passe-haut 120 Hz, fondus 0,4/0,9 |
| `sfx-wind-swoosh.mp3` | passage doppler, corps qui fend l'air | 1,46 s | 0,38 | #1471 *Cinematic wind swoosh* — brut |
| `sfx-glass-break.mp3` | **bris de verre** | 1,44 s | 0,02 | #759 *Glass break with hammer thud* — brut |
| `sfx-debris.mp3` | éclats / gravats qui retombent | 2,10 s | 0,26 | #2958 *Collapsing structure* — extrait 0,55→2,65 s (l'impact initial est coupé, on ne garde que la retombée), passe-haut 180 Hz |
| `sfx-landing-thud.mp3` | contact pieds/sol | 1,11 s | 0,16 | #2498 *Body impact falling into the sand* — brut |
| `sfx-impact-deep.mp3` | sub d'atterrissage lourd (réception héros) | 3,70 s | 1,28 | #788 *Big cinematic impact* — extrait 0,90→4,60 s |
| `sfx-thwip.mp3` | **projection de toile / sifflement du fil** | 1,10 s | 0,29 | #1491 *Arrow whoosh* — brut |
| `sfx-web-latch.mp3` | accroche / mise en tension du fil | 2,07 s | 0,23 | #1476 *Sword slash swoosh* — brut |
| `sfx-dolly-rush.mp3` | dolly-in qui accélère | 2,00 s | 1,09 | #1714 *Fast rocket whoosh* — 2,0 s de tête, fondu sortant |
| `sfx-arrival-stop.mp3` | **arrêt net à l'arrivée sur le visage** | 2,60 s | 1,50 | #2918 *Epic movie trailer whoosh impact* — extrait 1,55→4,15 s |

Tous encodés en **MP3 q2, 48 kHz, mono**.

## Licence

**Mixkit Free License** (mixkit.co) — usage commercial gratuit, **aucune attribution requise**,
utilisation dans un projet audiovisuel autorisée. Seule interdiction : redistribuer le fichier
sonore seul, en tant que tel. Nos vidéos sociales sont donc couvertes.
Même licence que celle déjà retenue pour `bgm-mixkit.mp3` sur autoboost-04.

## La règle qui compte : aligner sur le PIC, pas sur le début du fichier

La colonne **Pic (offset)** n'est pas décorative. Un impact posé par le début du fichier
s'entend **en retard** : `sfx-impact-deep` a son pic à 1,28 s, donc pour qu'il claque à
`t = 2,62 s` il faut le retarder de `2,62 − 1,28 = 1,34 s`. Poser `adelay=2620` mettrait la
détonation à 3,90 s, soit **1,3 s après l'image**.

```js
delay = t_cible − pic_offset
```

C'est déjà le piège documenté dans le README de v1 pour les whooshes bruts ; ici les offsets
sont **mesurés et écrits**, il n'y a plus à les redécouvrir.

## Volumes v1 : inchangés

La table de volumes de v1 (0,13 – 0,26, plafond pour ne jamais manger la voix) reste valable
pour les sons d'interface. **Les sons d'action ci-dessus jouent plus fort (0,38 – 0,75)** parce
qu'ils sont posés sur des plans **sans voix**. Ne pas les remonter sur un plan parlé.

## Recette de récupération Mixkit (elle a changé)

L'ancienne note mémoire donne un endpoint qui ne renvoie plus le fichier. Le bon chemin :

```bash
# SFX : la page de download renvoie une modale HTML, l'URL réelle est dans un attribut
curl -s -A "$UA" "https://mixkit.co/free-sound-effects/download/<id>/?context=item+grid" \
  | grep -o 'data-download--modal-url-value="[^"]*"' | cut -d'"' -f2
# -> https://assets.mixkit.co/active_storage/sfx/<id>/<id>.wav

# MUSIQUE : pas de "-preview", le fichier complet est directement à
# https://assets.mixkit.co/music/<id>/<id>.mp3
```

⚠️ `-ss`/`-t` en **option de sortie** (après `-i`) avec un `-af` a produit un fichier
**silencieux** sur 2 des 4 découpes. Toujours seeker **en entrée** (`-ss` avant `-i`) quand un
filtre audio est présent.

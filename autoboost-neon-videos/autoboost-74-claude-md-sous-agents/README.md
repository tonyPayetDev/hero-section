# autoboost-74 — CLAUDE.md + sous-agents (yapping facecam)

9:16 · 1080×1920 · 30 fps · **39,3 s** · −15,3 LUFS

Built with `/yapping-facecam-branded` from a **real 55 s facecam take** (not the
avatar bank): `video_25.mp4`, 1080×1440, shot by Tony.

## Script as spoken

| t | Bloc | Texte |
|---|---|---|
| 0,0 | Hook | « Claude vient peut-être de tuer Astra, et tout ça grâce à un simple fichier. » |
| 3,8 | Promesse | « Si toi aussi tu exploses ta limite de token après une demi-journée de boulot, tu connais le problème. » |
| 8,7 | Tension | « Le problème c'est peut-être pas combien tu utilises Claude. C'est quel modèle travaille sur quelle tâche. » |
| 15,0 | Révélation | « Tu crées un CLAUDE.md et tu lui demandes de déléguer certaines tâches à des sous-agents. » |
| 20,1 | Preuve | « Tâche simple, modèle léger. Tâche complexe, Opus. Sinon c'est comme utiliser un bazooka pour planter un clou. » |
| 28,6 | Solution | « L'objectif : gaspiller moins de tokens et garder la puissance pour les tâches importantes. » |
| 33,4 | CTA | « Tu veux exactement quoi mettre dedans ? **Commente TOKEN** et je t'envoie le prompt. Et ça pourrait tout changer. » |

## Montage

- **8 coupes** sur les silences > 0,55 s — 13 s de temps mort retirés, `atempo=1.14`
- **21 battements** de punch-in, le plus long tenant 2,58 s (règle : jamais > 4 s)
- **Cadre** : facecam 1080×1440 natif (aucun upscale) entre un bandeau haut de
  180 px et un bandeau bas de 300 px, filets or `#eab308`
- **Bandeau haut** : 11 mots-clés qui changent par section
- **Bandeau bas** : captions mot-à-mot, mot actif en or, mots-clés en violet
- **B-roll** : `flux` (les tokens) jusqu'à 15 s puis `workflow` (les sous-agents),
  screen 0,18 — la valeur 0,55 de la charte lave le noir mat en violet sur un
  bandeau plein
- **Musique** : `mindset-epical-drums-05-75` — seule nappe de `_shared/bgm` sous
  les 10 dB d'écart exigés (mesuré : 5,6 dB sur 42 s), posée à niveau fixe
  (−11 dB ≈ −31 dBFS) sous une voix normalisée en premier, puis sidechain
- **SFX** : whoosh v2 sur chaque coupe, impact sur la révélation et sur le CTA

## Écarts à la charte, assumés

1. **Avatar** — c'est le vrai visage de Tony, donc ni banque v3 ni voix clonée.
   Le son natif est **gardé** (la règle « couper le son natif » vise les clips
   d'avatar muets habillés d'une voix clonée).
2. **Mot-clé CTA** — `TOKEN` est dit dans la vidéo mais **n'a aucune porte
   Blotato active**. À créer avant publication, sinon les gens commentent et ne
   reçoivent rien.

## Rebuild

```bash
python3 plan.py        # coupes + battements -> plan.json
python3 build.py       # cuts, remap, zoom, compose, audio, final
python3 captions.py    # captions.ass (entre remap et compose)
```

`build.py` attend le rush source dans `/root/.claude/uploads/.../a5b418dc-video_25.mp4`
et écrit ses intermédiaires hors du dépôt.

---

# Version motion design (HyperFrames) — `autoboost-74-motion.mp4`

Built with `/hyperframes-read-first` → `/graphic-overlays`, on the same cut
facecam (39,3 s), after Tony's five visual references (stacked layout, neon
ring, glass cards, workflow window, brand plate).

## Structure

| t | Écran | Face cam |
|---|---|---|
| 0,0 | Hook — « CLAUDE VIENT DE / TUER ASTRA ? », chips ASTRA barré + « un simple fichier » | plein écran |
| 3,6 | Le problème — jauge d'usage 0→100 %, tampon LIMITE ATTEINTE, 3 tuiles | se replie dans le cercle néon |
| 8,7 | La vraie question — mauvaise question barrée, la bonne cochée | rectangle empilé + filet lumineux |
| 15,0 | La solution — fenêtre `CLAUDE.md` tapée ligne à ligne | cercle |
| 20,0 | Le routage — nœuds CLAUDE.md → tâche simple → modèle léger / tâche complexe → Opus | cercle |
| 24,6 | L'erreur — OPUS vs LÉGER, tampon GASPILLAGE | cercle |
| 28,5 | L'objectif — jauges tokens gaspillés ↓ / puissance ↑, 3 coches | rectangle |
| 33,4 | CTA — plaque AUTOMATISATIONBOOST, COMMENTE **TOKEN**, champ commentaire tapé | grand cercle |

Every screen slides in from the right with a speed streak; the ring breathes
on each of the 21 beats of the cut grid; captions sit in a plate under the
facecam, active word gold, key terms violet.

## Choix

- **Aucun chiffre inventé** : les références affichent « +247 % » ; ici les
  seules valeurs sont celles dites dans la vidéo (100 % d'usage, ½ journée).
  Les jauges de l'écran Objectif sont illustratives, sans pourcentage.
- **Aucun vert** : pastilles de fenêtre rouge / or / violet, coches or.
- Police : DejaVu Sans Bold (charte, rendu local) en dégradés métal / or / violet.
- La `<video>` est enfant direct de la racine (contrat HyperFrames) : elle est
  mise en forme par `transform` + `clip-path: inset(... round R)`, seule forme
  qui s'interpole entre plein écran, rectangle arrondi et cercle.

## Rebuild

```bash
cd motion
python3 gen.py                    # public/index.html depuis ../plan_actual.json + template.html
npx hyperframes lint public       # 0 erreur
npx hyperframes render public -o motion_silent.mp4 --fps 30 --quality delivery
python3 audio.py                  # voix + nappe + 21 SFX calés sur le motion
```

`motion/public/facecam.mp4` n'est pas versionné (dérivé, 25 Mo) : c'est
`base.mp4` (sortie de `build.py cuts`) ré-encodé muet avec `-g 30 -keyint_min 30`.

---

# v2 — `autoboost-74-motion-v2.mp4` (kit FaceCam Boost)

Même face cam, même timeline, reconstruite sur `_shared/facecam-boost-kit/`
après les nouvelles références de Tony (planche de stickers, layouts 1-4,
vidéo « 0,07 $ ») et la page « 8 animations motion design » (CERËGA / SKOOL),
repassée dans la charte.

| Ajout v2 | Où |
|---|---|
| Stickers punch : ÇA PART, ÇA BLOQUE, PLUS CLAIR, BON SYSTÈME, PLUS SIMPLE, DÉJÀ MIEUX, ÇA MONTE, NIVEAU MAX | un par écran, à cheval sur la jointure écran / face cam |
| Puces NIVEAU 1 → 6 | coin haut gauche, écrans 1 à 6 |
| Courbe de progression (Notion #3) | écran Problème, à la place de la jauge |
| Pile de cartes (Notion #5) | la mauvaise question s'envole, la bonne avance |
| Split vertical (layout 2) | « un bazooka pour un clou » : face cam à gauche, OPUS / LÉGER à droite, séparateur or + VS |
| Bouton → champ (Notion #1) + TOKEN élastique (Notion #7) | CTA |
| Finale plein écran (layout 4) | « ÇA POURRAIT / TOUT CHANGER » + trait violet |
| Musique | Valse des fleurs, version maison évidée, partie stable bouclée (mesure 6 → 26) |

Les motions #2 (recherche), #4 (zoom tuile), #6 (dock) et #8 (particules) sont
dans le kit (`boards/`) mais pas dans cette vidéo : rien dans le propos ne les
appelait.

v1 reste reconstructible : `motion/gen_v1.py`.

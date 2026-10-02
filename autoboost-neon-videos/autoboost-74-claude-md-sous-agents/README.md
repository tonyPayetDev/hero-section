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

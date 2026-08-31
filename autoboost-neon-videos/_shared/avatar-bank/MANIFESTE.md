# Banque avatar — deux décors, deux usages

> **La banque ne contient PAS 24 clips.** Le skill `veille-to-video-v3` et
> `SYSTEM-MAP.md` l'annoncent, c'est faux : il y a **7 clips exploitables**,
> répartis en **deux tournages qui ne se mélangent jamais**.

---

## Le set BUREAU — pour les tutoriels

Studio, fond sombre, softbox visible, chemise noire unie. **5,1 s par clip.**

| Clip | Rôle narratif |
|---|---|
| `A1_hook_frontal.mp4` | accroche, face caméra |
| `B1_principe.mp4` | explication d'un principe |
| `C2_commente_motcle.mp4` | appel à commenter |

**Quand l'utiliser** : tuto, démonstration, explication technique, format long 16:9.
C'est le décor qui dit « je t'apprends quelque chose ».

## Le set VOITURE — pour l'humour et le mindset

Intérieur de voiture, lumière du jour, chemise noire à liseré jaune. **10,1 s par clip.**

| Clip | Rôle narratif |
|---|---|
| `D1_hook_frontal.mp4` | accroche, face caméra |
| `D2_insistance_doigts.mp4` | insistance, geste de la main |
| `D3_cta_lunettes.mp4` | appel, ajuste ses lunettes |
| `D4_relance_barbe.mp4` | relance, main sur la barbe |

**Quand l'utiliser** : humour, opinion, mindset IA, storytime personnel, format court.
C'est le décor qui dit « je te parle entre nous ».

---

## La règle

**Un décor par vidéo. Jamais les deux.** Mélanger la voiture et le studio dans
le même montage se voit immédiatement : ce sont deux tournages, deux tenues,
deux lumières.

**Le décor doit correspondre au propos.** Une histoire technique dans la voiture
sonne faux, un trait d'humour au studio tombe à plat. Erreur déjà commise le
2026-08-20 sur `autoboost-storytime-terminal` : set voiture sur un récit de bug.

---

## Ce qui n'est pas exploitable

- `_source_spider_full.mp4`, `SPIDER_talking.mp4`, `HOOK_spider_entree.mp4` —
  clips d'un projet ponctuel, pas des rôles narratifs réutilisables.
- `../avatar-hq/avatar-hq-green.mp4` — **fond vert, 716×1284, 5,0 s.**
  Ancien pipeline : il fallait le détourer par `geq` (jamais `chromakey`),
  recadrer en carré avant le masque, et dépolluer le canal vert.
  **Remplacé par les deux sets ci-dessus**, qui n'ont besoin d'aucun détourage.
  Encore référencé par `veille-to-video` (v2) et trois vieux projets — à ne pas
  réutiliser dans une nouvelle vidéo.
- `../hf-clips/` — 10 clips bruts nommés par identifiant Higgsfield, sans rôle
  attribué. Matière première, pas banque.

---

## Étendre la banque

Les deux sets sont courts : 3 rôles au bureau, 4 en voiture. Sur un format long
ça se voit — l'essai contemplatif du 2026-08-20 a laissé deux plages de 16 s
sans visage faute de matière.

Générer une nouvelle série **sur le web**, où Seedance 2.5 est illimité (par
l'API c'est payant). Verrouiller l'identité par image de référence, garder la
même tenue sur toute la série, et nommer chaque clip par son rôle narratif —
jamais par son identifiant de génération.

Voir la section « Générer les 24 clips » de `veille-to-video-v3` pour la méthode.

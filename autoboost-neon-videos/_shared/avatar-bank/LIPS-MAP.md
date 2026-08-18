# Banque avatar — carte « lèvres actives »

**Piège déjà payé (2026-08-18, vidéo `videoboost-dialogue`).**
Tony a rejeté un montage validé par ailleurs avec : *« à 10 secondes et 23 secondes petit blanc,
la voix parle mais les lèvres ne bougent pas »*. Trois plans avatar tombaient dans des portions
du clip source où **Tony ne parle pas** (il marque une pause, respire, ou finit son geste),
pendant que la voix clonée, elle, parlait. Résultat : 0,33 à 0,37 s de lèvres immobiles sous
une voix active — assez pour que ça se voie, pas assez pour qu'on le repère en relisant le script.

## Le fait à retenir

Les clips de la banque sont des **prises continues**. Ils ne parlent pas de bout en bout.

| Clip | Durée | Plage lèvres actives | Zones mortes |
|---|---|---|---|
| `A1_hook_frontal.mp4` | 5,06 s | **0,67 → 4,58** | 0,00–0,67 et 4,58–5,06 |
| `B1_principe.mp4` | 5,06 s | **0,08 → 4,88** | quasi néant |
| `C2_commente_motcle.mp4` | 5,06 s | **0,08 → 4,83** | quasi néant |

`A1_hook_frontal` est le piège : **0,67 s de silence au début et 0,48 s à la fin**. C'est de loin
le clip le plus utilisé (plan d'ouverture, hooks) donc c'est celui qui mord. Les 3 plans fautifs
en venaient tous les trois.

La carte à jour est dans **`lips-map.json`**, régénérée par **`build-lips-map.mjs`**.
**Régénère-la à chaque ajout de clip dans la banque.**

```bash
node /work/autoboost-neon-videos/_shared/avatar-bank/build-lips-map.mjs
```

## La règle

> Un plan avatar posé **sous une voix active** doit tenir **entièrement** dans une plage
> « lèvres actives » du clip source. Les zones mortes restent utilisables, mais seulement
> quand la voix se tait, sous une réplique d'un extrait tiers, ou sous un plan de coupe.

Concrètement, pour un plan de `N` images à 30 fps joué à la vitesse `sp` depuis l'instant `ss` :

```
ss           >= zone.start
ss + (N/30)*sp <= zone.end
```

C'est la contrainte qui a été appliquée pour corriger `videoboost-dialogue` : seul `ss` a bougé,
jamais `N` — donc aucun décalage de timeline et **piste audio inchangée au bit près**.

## Comment c'est mesuré

`build-lips-map.mjs` : décodage à la cadence native → crop de la boîte bouche
(`300×240 @ (280,360)` dans le cadrage natif 720×1280, la bouche est vers `(360,470)`) →
réduction en 48×48 niveaux de gris → **différence absolue moyenne inter-images** → lissage 3 taps →
seuil `1.6`. Calibré sur les 3 clips d'origine : **parole ≈ 2–12, immobile ≈ 0–1,2**.

Deux pièges de mesure rencontrés, à ne pas refaire :

1. **Ne mesure jamais la bouche dans une boîte fixe du cadre de sortie.** Le zoom et l'offset
   changent à chaque plan : sur les plans larges la boîte tombe sur le torse et renvoie une
   immobilité qui n'existe pas. Premier diagnostic entièrement faux à cause de ça. Mesure la
   **fenêtre source**, ou recalcule la boîte à partir du zoom/offset du plan.
2. **La banque est en 24 fps, les rendus en 30 fps** : une image sur cinq est dupliquée, donc
   du mouvement `0.00` isolé est *normal*. Seules les **séries continues** (> ~6 images) comptent.

## Le garde-fou

`check_lips_rule.mjs` (dans le dossier de travail du projet) lit les paramètres de plans dans
`order.json` — écrit par le builder, donc jamais désynchronisé du montage réel — croise avec
`lips-map.json` et l'enveloppe RMS de la piste voix, et **sort en code 1** si un plan dépasse
6 images fautives. À lancer **après le build, avant l'assemblage**.

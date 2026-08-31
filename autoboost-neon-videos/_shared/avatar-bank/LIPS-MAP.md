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

⚠️ Le garde-fou doit lire une piste **voix seule** (`voice_bed.wav`), jamais le mix final :
la BGM et les SFX se lisent comme « quelqu'un parle » et le gate hurle sur les silences voulus.

---

# La règle `wardrobe` (2026-08-18)

**L'index à jour de ce qui existe vraiment sur le disque est `bank.json`.**
`manifest.json` (v1) reste le brief de tournage des 24 clips A/B/C prévus — la plupart n'ont
jamais été tournés. Le sélecteur doit lire `bank.json`.

La banque a grossi sur **trois tournages** avec des vêtements et des décors différents. Un
tirage aléatoire à plat fait donc changer Tony de garde-robe en plein milieu d'une phrase.
Chaque entrée porte maintenant un champ **`wardrobe`** :

| `wardrobe` | Look | Décor | Dossier | Carte lèvres |
|---|---|---|---|---|
| `chemise-noire-studio` | chemise noir mat unie, lunettes | studio sombre, octabox | `clips/` | `lips-map.json` |
| `chemise-noir-jaune` | chemise noir mat, patte néon jaune, lunettes | siège conducteur, jour | `clips-new/` | `lips-map-d.json` |
| `spider-suit` | combinaison spider noir mat, lignes néon jaune, sans lunettes | toits de nuit puis home studio néon | `clips-spider/` | `lips-map-spider.json` |

> **La règle.** Une vidéo ne mélange **jamais** deux garde-robes à l'intérieur d'un même bloc.
> Deux garde-robes ne cohabitent que si la seconde est confinée à **l'ouverture ou la clôture**,
> où la coupure franche se lit comme un effet voulu. Partout ailleurs, le sélecteur filtre les
> candidats sur la garde-robe déjà en place. Jamais de fondu à la frontière : coupe franche.

---

# Batch SPIDER (2026-08-18) — deux entrées, deux usages

Un seul fichier Seedance 2.5 (720×1280, 24 fps, 10,08 s, 241 images) découpé en **deux entrées
distinctes**, parce qu'elles n'ont pas du tout le même usage. Source entière conservée dans
`clips-spider/_source_spider_full.mp4`.

**Pas de couture.** Contrairement au batch D, ce fichier de 10,08 s n'est **pas** deux prises de
5,04 s collées : planche de contact à 10 i/s sur 4,40–5,70 s → montée continue hors de
l'accroupissement, aucune coupe, aucune pause muette. Mesuré, pas supposé.

| Entrée | Plage source | Durée | Parle ? | Créneau |
|---|---|---|---|---|
| `HOOK_spider_entree.mp4` | 0 → 8,0 s | 8,00 s | **non** | **ouverture uniquement**, SFX seuls |
| `SPIDER_talking.mp4` | 8,0 → 10,08 s | 2,04 s | oui, **1,08 s utile** | CTA / ponctuation, **jamais en continu** |

## `HOOK_spider_entree` — carte lèvres volontairement VIDE

`active: []`, **forcé à la main**. La machine renvoyait `0.04-3.17` et `4.38-7.67` : ces fenêtres
ne veulent rien dire. Pendant 0–7,5 s il n'y a **aucun visage dans la boîte bouche** — elle voit
une ville de nuit, une fenêtre, de la poussière et du flou de vitesse, et l'image entière bouge.
La détection de mouvement de bouche est **indéfinie** sur un plan sans visage verrouillé.
Tony n'y parle pas une seule fois. **Ne jamais le poser sous une voix active.**

Contenu : 0–2,5 balancement sur câble entre deux tours · 2,5–4,5 traversée de fenêtre,
réception accroupie, poussière · 4,5–6,0 il se redresse et tire une toile vers l'objectif ·
6,0–7,55 la toile tire la caméra, dolly-in violent · 7,55–8,0 la caméra se verrouille en
cadrage présentateur, le gant sort du champ vers 7,88.

## `SPIDER_talking` — 1,08 s utile, deux corrections

**Crop remesuré.** La bouche est à ~(365,495) dans le cadre natif : plus haut que le batch D
(355,565), un peu plus bas que le batch A/B/C (360,470). `LIPS_CROP=260,150,235,420`.
La boîte D tombe sur le **menton** ici ; la boîte A/B/C tombe sur le **nez/les yeux**.

**Seuil remonté : `1.6` → `4.5`.** Ce clip porte du grain, un scintillement néon et une lente
dérive de tête : la ligne de base **immobile** est à **1,6–2,7**, pas à 0–1,2 comme sur les clips
A/B/C. À `thresh=1.6` la machine déclare le clip actif de `0.04` à `2.00`, soit sa totalité —
faux de bout en bout. La parole culmine entre 8 et 20. `4.5` sépare proprement les deux.

**Correction manuelle des deux bords.** À `thresh=4.5` la machine donne `0.58 → 1.71`.
Vérification image par image des 49 crops de bouche : lèvres **fermées** images 0–15
(0,000–0,625), la moue avant la première voyelle démarre image 15 (0,625), bouche ouverte à
partir de l'image 16 (0,667), refermeture images 43–47 (1,792–1,958).
Retenu : **`0.63 → 1.71`** (départ ramené de 0,58 à 0,63, bord conservateur).

Conséquence dure : un plan posé sous une voix active tient **au maximum 32 images à 30 fps**
en vitesse 1,0. C'est une ponctuation ou une ligne de CTA, pas un bloc de corps.

## Régénérer

```bash
LIPS_CROP=260,150,235,420 LIPS_THRESH=4.5 \
  node /work/autoboost-neon-videos/_shared/avatar-bank/build-lips-map.mjs \
       /work/autoboost-neon-videos/_shared/avatar-bank/clips-spider \
       /work/autoboost-neon-videos/_shared/avatar-bank/lips-map-spider.json
```

⚠️ La sortie brute **écrase les corrections manuelles** ci-dessus (fenêtre vide du hook, bord à
0,63). Après régénération, les réappliquer — elles sont la partie vérifiée à l'œil, pas la
partie mesurée.

---

## Set VOITURE cartographié (2026-08-20)

Le set voiture n'avait jamais été passé au détecteur : la carte d'origine ne couvrait
que les 3 clips bureau. Le cadrage du studio ne convient pas — en voiture le visage est
plus petit et plus haut dans l'image.

```bash
LIPS_CROP="240,180,225,430" node build-lips-map.mjs clips-new lips-map-voiture.json
```

Zone vérifiée à l'image sur D1, D2 et D4 avant de lancer : elle tombe sur la bouche.

| clip | durée | lèvres actives | fenêtres |
|---|---|---|---|
| `D1_hook_frontal` | 10,08 s | 8,55 s | 0,54→4,63 · 4,96→8,42 · 8,67→9,67 |
| `D2_insistance_doigts` | 10,08 s | 8,51 s | 0,58→2,46 · 2,71→4,63 · 5,04→9,75 |
| `D2_pointe_boucle` | 3,25 s | 2,88 s | 0,08→2,96 |
| `D3_cta_lunettes` | 10,08 s | 9,71 s | 0,04→9,75 |
| `D4_relance_barbe` | 10,08 s | 9,13 s | 0,54→9,67 |

**Deux clips à surveiller.** `D1` et `D2` ont chacun **deux zones mortes internes**
(~0,3 s vers 4,6-5,0 s), pas seulement aux extrémités comme les clips bureau. Un plan
qui traverse 4,63→4,96 s sous une voix active donne exactement le défaut que Tony a
rejeté le 2026-08-18 : la voix parle, les lèvres ne bougent pas.

`D2_pointe_boucle` est la portion de `D2` où le doigt pointe (extraite de 6,8→10,0 s),
isolée pour que le geste tienne sur toute la durée d'un plan long. Elle est active de
bout en bout, donc sûre.

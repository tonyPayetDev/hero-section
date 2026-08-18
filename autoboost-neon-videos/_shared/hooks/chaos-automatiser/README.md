# Hook réutilisable — « CHAOS → AUTOMATISER »

Bloc visuel de **10,0 s** en 9:16 (1080×1920), **100 % procédural** (DOM + CSS + GSAP).
Aucune image, aucune vidéo, aucun asset généré. **Conçu pour fonctionner muet** : toute
l'histoire passe par le mouvement.

Fichier unique : `chaos-hook.js` (il injecte son CSS **et** son DOM, puis pose sa timeline).

---

## Les 5 temps (verrouillés)

| Temps | Beat | Ce qui se passe |
|---|---|---|
| 0 → 2 s | **chaos** | des dizaines de tuiles de tâches s'empilent en accélérant, compteur rouge qui grimpe, shake croissant, halo d'alerte |
| 2 → 4 s | **freeze** | flash blanc + tout se fige net. 0,22 s de retombée, puis **plus rien ne bouge jusqu'à 3,80 s**. C'est le beat le plus important : **ne rien y ajouter** |
| 4 → 6 s | **curseur** | un bouton apparaît, un curseur entre par le bas-droite, marche jusqu'au bouton et **clique** (5,40 s) → onde de choc |
| 6 → 8 s | **exécution** | toutes les tuiles claquent **en même temps** dans une grille propre, barres de progression + coches en cascade, compteur qui bascule en vert |
| 8 → 10 s | **lockup** | logo + wordmark + punchline + trait néon |

La mécanique d'empilement est reprise du chapitre « la charge » de
`/work/previsualisation/autoboost-principe/` (pile en 3 colonnes, jitter et rotation
déterministes via un hash `sin`), portée de canvas vers du DOM pour rester déterministe
au rendu HyperFrames.

---

## Intégration dans une composition

1. Copier le fichier dans le `public/` du projet :

```bash
mkdir -p monprojet/public/hooks
cp /work/autoboost-neon-videos/_shared/hooks/chaos-automatiser/chaos-hook.js monprojet/public/hooks/
```

2. Dans `public/index.html` (qui déclare `<meta charset="utf-8">`), **après** GSAP :

```html
<script src="assets/gsap.min.js"></script>
<script src="hooks/chaos-hook.js"></script>
<script>
  /* ===== VARIABLES DU HOOK (tout ce qui change d'une vidéo à l'autre) ===== */
  const HOOK_VARS = {
    tasks: ['Post Instagram', 'Script vidéo', 'Relance client', /* ... */],
    tileCount: 48,
    buttonLabel: 'AUTOMATISER',
    counterLabel: 'TÂCHES EN RETARD',
    counterDoneLabel: 'TÂCHES EXÉCUTÉES',
    counterTarget: 128,
    punchLine1: 'Arrête de travailler comme une machine.',
    punchLine2: 'Construis-en une.',
    brandTop: 'AUTOMATISATION', brandBottom: 'BOOST',
    accent: '#FFE600', accent2: '#A855F7', danger: '#FF3B30', ok: '#3DFF9E',
    bg: '#050505', autoHide: true
  };

  const tl = gsap.timeline({ paused: true });
  ChaosHook.mount(document.getElementById('root'), HOOK_VARS); // crée le DOM
  ChaosHook.build(tl, 0);                                      // pose les 10 s à t=0
  /* ... le corps de la vidéo se construit ensuite à partir de t = 10 ... */
  window.__timelines['ma-compo'] = tl;
</script>
```

`ChaosHook.build(tl, t0)` retourne `t0 + 10` : l'offset où le corps peut démarrer.

---

## Variables exposées

| Variable | Défaut | Rôle |
|---|---|---|
| `tasks` | 16 libellés | libellés cyclés sur les tuiles |
| `tileCount` | `48` | nombre de tuiles empilées (24 restent visibles en phase exécution) |
| `buttonLabel` | `AUTOMATISER` | texte du bouton cliqué à 5,40 s |
| `counterLabel` | `TÂCHES EN RETARD` | label du compteur en phase chaos |
| `counterDoneLabel` | `TÂCHES EXÉCUTÉES` | label après exécution |
| `counterTarget` | `128` | valeur atteinte par le compteur |
| `punchLine1` / `punchLine2` | punchline machine | 2 lignes du lockup (`p2` est la ligne accentuée) |
| `brandTop` / `brandBottom` | `AUTOMATISATION` / `BOOST` | wordmark |
| `accent` | `#FFE600` | néon principal (bouton, marque, état exécuté) |
| `accent2` | `#A855F7` | néon secondaire (dégradé du trait final) |
| `danger` | `#FF3B30` | état chaos |
| `ok` | `#3DFF9E` | état exécuté |
| `bg` | `#050505` | fond |
| `autoHide` | `true` | masque la couche hook à `t0 + 10 s` |

**Encodage** : `chaos-hook.js` est volontairement **ASCII pur**. Tout le texte accentué
arrive par `HOOK_VARS` depuis le HTML hôte (qui a `<meta charset="utf-8">`) et est injecté
via `textContent`. Ne jamais coder d'accent en dur dans le `.js` — c'est ce qui casse les
accents quand le fichier est servi sans charset.

---

## Son

Le hook est **muet par construction**. Recette recommandée (posée en passe 2 ffmpeg) :

- musique seule sur les 10 s (pas de voix — la voix démarre après, c'est ce qui donne sa force au hook) ;
- **1 SFX de freeze** à `t0 + 2,00 s` (`sfx-impact.mp3` ou `sfx-glitch-hard.mp3`, vol ~0,30) ;
- optionnel : `sfx-click.mp3` à `t0 + 5,40 s` et `sfx-confirm.mp3` à `t0 + 6,60 s` — jamais plus.

**Ne jamais poser de son entre 2,2 s et 3,8 s.**

---

## Rendu

Env HyperFrames obligatoire :

```bash
export PATH="/home/claude/tools/node/bin:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/chromelibs/usr/bin:$PATH"
export LD_LIBRARY_PATH="/home/claude/tools/chromelibs/lib/x86_64-linux-gnu:/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export FONTCONFIG_PATH="/home/claude/tools/chromelibs/etc/fonts"
```

Contraintes connues : `--out` est ignoré (sortie dans `public/`), `snapshot` est inutilisable
sur ces compos (runtime jamais ready) → vérifier sur des frames extraites du vrai mp4.

---

## Première utilisation

`/work/autoboost-neon-videos/autoboost-hook-chaos/` (route previsualisation
`hook-chaos-automatiser`) — hook 10 s muet + corps v3 (voix clonée, avatar, captions, CTA).

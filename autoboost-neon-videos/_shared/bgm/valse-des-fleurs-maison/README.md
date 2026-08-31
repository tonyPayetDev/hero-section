# Valse des fleurs — production maison

Deux phonogrammes **produits par nous**, à partir de la partition de Tchaïkovski
(*Casse-Noisette* op. 71a n° 6, **domaine public**, compositeur mort en 1893).

| Fichier (dans `_shared/bgm/`) | Ce que c'est |
|---|---|
| `valse-des-fleurs-maison-tutti.mp3` | Orchestre complet. Flûte, hautbois, clarinette, violons, trompette, timbales **+** toute la section grave. Actif de 0,000 à 6,667 s, silence ensuite. |
| `valse-des-fleurs-maison-evidee.mp3` | Orchestration **évidée** : cor, violoncelles, contrebasse, altos, harpe, pizzicati. Rien au-dessus de ~700 Hz en fondamentale. Joue en continu de 0,000 à 35,400 s. |

Les deux sont **le même enregistrement**, pris à deux endroits de l'orchestre. Sommés, ils
donnent le tutti ; l'évidée seule donne le lit. C'est ce qui permet de passer de l'un à l'autre
**sans coupe ni fondu** : les pupitres aigus s'arrêtent sur la résolution de la phrase (le ré
de la mesure 6, à 6,667 s) et les pupitres graves continuent de jouer.

## Licence — pourquoi c'est incontestable

| Élément | Statut |
|---|---|
| **La partition** | Domaine public (Tchaïkovski, † 1893). |
| **Le séquençage** (notes, durées, vélocités, harmonisation, orchestration, plan dynamique) | **Écrit par nous**, voir `source/score.mjs`. Aucun MIDI tiers n'a été utilisé dans le rendu. |
| **La banque de sons** | `FluidR3_GM.sf2`, Frank Wen, **licence MIT** — usage commercial et redistribution autorisés. |
| **Le phonogramme** | **Produit par Tony PAYET / Automation Boost.** Aucun droit voisin de tiers. |

Il n'existe **aucune empreinte Content ID** de ce fichier, puisqu'il n'a jamais été distribué :
c'est un enregistrement neuf. Contrairement à un enregistrement du commerce (le fichier LSO 1989
fourni initialement était protégé jusqu'en **2059** au titre des droits voisins), celui-ci est
publiable sur les 5 réseaux sans réserve.

> Note : aucun MIDI librement licencié de cette pièce n'a pu être trouvé — Mutopia ne publie que
> neuf Tchaïkovski, aucun du *Casse-Noisette* ; le lien « nutcracker waltz » de midiworld sert un
> fichier sans rapport ; le .mid de flutetunes ne porte aucune mention de licence. Un MIDI
> séquencé par un tiers porte les droits de son séquenceur, donc **séquencer nous-mêmes était la
> seule voie propre** — et c'est aussi elle qui permet de choisir les instruments, donc de
> fabriquer la version évidée.

## Mesures

Métrique de la bibliothèque (`voice_band_dbfs` = RMS moyen en dBFS de la bande 1–3,5 kHz,
`voice_headroom_db` = cette valeur moins le LUFS intégré ; objectif ≤ −16) :

| Version | fenêtre | LUFS | bande 1–3,5 kHz | **headroom** |
|---|---|---|---|---|
| tutti | 0 → 7,0 s | −18,4 | −23,6 dBFS | **−5,2** (normal : c'est un tutti, il occupe tout le spectre) |
| évidée | 6,68 → 35,4 s | −28,1 | −48,9 dBFS | **−20,8** ← la meilleure valeur de toute la bibliothèque |

Et la métrique de la mission (écart entre le **LUFS de la piste** et le **LUFS de sa bande**
1–3,5 kHz, objectif ≥ 12 dB) : **tutti +2,0 dB**, **évidée +20,4 dB**.

**L'orchestration seule suffit** : mesurée avant tout filtrage, la version évidée était déjà à
**+12,5 dB**. Le filtrage (shelf −9 dB à partir de 1,4 kHz + passe-bas 5 kHz) n'est qu'une marge,
pas un sauvetage. Une première tentative à +23 dB (passe-bas 1,15 kHz) a été **écartée** : le
thème n'était plus reconnaissable, ce que la mission interdisait.

## Reproduire / réutiliser

```bash
bash source/render_music.sh          # réécrit les .mid puis les rend avec FluidSynth
```

`source/score.mjs` est le séquenceur : tempo (1 mesure = 1,000 s exactement), thèmes, harmonie,
vélocités, plan dynamique. Pour une autre durée ou un autre montage, c'est ce fichier qu'on
modifie — les niveaux, eux, se calent dans le `build_audio.mjs` du projet, pas ici.

FluidSynth n'est pas installé sur la machine : `render_music.sh` s'attend à un préfixe privé
(variable `FS_ROOT`) obtenu en dépaquetant les `.deb` de bookworm avec `dpkg-deb -x`. La
procédure est décrite en tête du script.

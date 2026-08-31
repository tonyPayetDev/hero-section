# Conte Enfant Vidéo

Crée des vidéos de contes pour enfants (30-60s) avec **Ethanou**, un avatar anime stylisé qui raconte.

## Usage

```
/conte-enfant-video story="Les trois petits cochons" theme="constructif" learning="phonétique des consonnes"
```

## Paramètres

| Param | Type | Exemple | Défaut |
|---|---|---|---|
| `story` | string | "Les trois petits cochons" | requis |
| `theme` | select | `constructif`, `aventure`, `alphabet`, `mots`, `chiffres` | `aventure` |
| `learning` | string | "phonétique des consonnes" | optionnel |
| `duration` | number | 45 (secondes) | 45 |
| `voice` | select | `male`, `female` | `male` |

## Pipeline

1. **Écrire l'histoire** — Prompt dirigé, cible pédagogique + divertissement
2. **Générer la narration** — TTS WaveSpeed (voix clonée enfant ou neutre), segmentation par plans
3. **Générer les plans vidéo** — Seedance ou HyperFrames pour chaque segment (Ethanou raconte)
4. **Assembler** — Concordance lèvres (avatar narrateur), musique, sous-titres
5. **Valider** — Vérifier durée, engagement enfants, apprentissage

## Ethanou

**Avatar**: portrait anime stylisé, garçon ~8 ans, cheveux bruns, sourire bienveillant.
**Réutilisable**: même personnage dans toutes les histoires (personnalité stable, relation enfant-spectateur).
**Voix**: TTS enfant-friendly (ou voix clonée Tony si segmentée "père raconte").

## Ressources

- WaveSpeed API: `/work/.kie.env` (KIE_API_KEY)
- Higgsfield: Seedance pour génération vidéo avatar
- n8n workflows (optionnel): orchestration multi-étapes

## Exemples d'histoires

- **"Les trois petits cochons"** (constructif) → Apprentissage: structures solides
- **"Alphabet aventure"** (alphabet) → Chaque lettre = créature qui parle
- **"Comptoir des chiffres"** (maths) → Marchand qui vend par quantités
- **"Pierre-Marie et la pomme"** (gratitude) → Morale: reconnaissance

## Notes

- Durée finale: **30-60s** (cible YouTube Shorts / TikTok enfants)
- Sous-titres: **obligatoires** (accessibilité + apprenants malentendants)
- Contenu: **Zéro violence**, messages positifs, apprentissage intégré
- Fréquence: Une nouvelle histoire chaque semaine = chaîne YouTube d'apprentissage ludique

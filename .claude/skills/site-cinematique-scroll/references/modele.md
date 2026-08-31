# Le modèle — Seedance 2.5 sur MCP Higgsfield

Seedance 2.5 est le modèle vidéo multimodal de ByteDance, accessible via le MCP Higgsfield. La caractéristique qui change tout pour le web, c'est la durée : une seule génération peut monter à trente secondes. C'est assez long pour tenir un parcours de scroll entier en un seul plan — pas de chaînage, pas de raccord, pas de dérive de continuité. Il lit des références image, vidéo et audio en même temps, et il sait prolonger ou retoucher un clip qui existe déjà.

| Paramètre | Ce que tu as |
|---|---|
| **Modes** | t2v (prompt seul) · omni_reference (références image / vidéo / audio) · video_edit (retouche d'un clip existant) · video_extension (prolonge un clip en avant ou en arrière) |
| **Durée** | 4 à 30 secondes. Défaut : 5. C'est la caractéristique phare — rien d'autre ici ne dépasse 15. |
| **Résolution** | 480p ou 720p. 720p est le plafond — upscale le clip que tu gardes avant d'en extraire les frames. |
| **Références** | start_image, end_image, image_references, video_references, audio_references |
| **Ratios** | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 |
| **Audio** | generate_audio est à true par défaut. Mets-le à false pour le web : tu récoltes des frames, tu ne publies pas une vidéo. |
| **Coût** | 6,5 crédits par seconde en 720p. 3 crédits par seconde en 480p. Strictement linéaire : un clip de 10 s en 720p coûte 65 crédits, un plan complet de 30 s en coûte 195. |

## Travailler à 720p

720p est le plafond : traite-le comme une contrainte à contourner par le design. Des frames sorties directement d'un rendu 720p sont molles une fois étirées sur un hero plein écran. Le correctif : passer le clip que tu gardes dans l'upscaler vidéo en 2K avec le preset AIGC, puis découper les frames depuis la version upscalée, à 1600 px de large. Les images générées montent bien en résolution, et seul le clip retenu a besoin de ce traitement. Travaille en 480p tant que le mouvement de caméra est en test, puis passe en 720p une fois qu'il est juste.

## Coûts

| Poste | Coût |
|---|---|
| Clip unique de 10 s, 720p | 65 crédits |
| Parcours complet de 30 s en un plan, 720p | 195 crédits |
| Passe de brouillon, 10 s en 480p | 30 crédits — teste le mouvement ici avant de t'engager |
| Site à quatre chapitres sur 2.5 | environ 250 à 400 crédits, upscales compris |
| Upscale d'un clip retenu en 2K | surcoût variable, sans preflight de coût — vérifie ton solde avant et après |

Les tarifs bougent : vérifie le solde avant et après chaque batch. L'upscale n'a pas de preflight de coût.
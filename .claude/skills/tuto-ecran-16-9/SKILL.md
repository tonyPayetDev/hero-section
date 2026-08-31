---
name: tuto-ecran-16-9
description: Produit un tutoriel YouTube 16:9 avec capture d'écran, démonstration en direct et avatar en incrustation. À utiliser quand Tony veut expliquer un outil, une méthode ou un workflow en format long — par opposition aux formats verticaux courts de veille-to-video. Gère la structure du script, le découpage en chapitres, les moments de capture et l'insertion de l'avatar v3.
---

# Tuto écran 16:9

Format long, horizontal, pour YouTube. À ne pas confondre avec les formats verticaux de 28-35 s : ici on explique, on démontre, on prouve.

## La règle qui sépare un bon tuto d'un mauvais

**Ne jamais dire ce qu'on peut montrer.**

Un tuto qui décrit une commande est un article lu à voix haute. Un tuto qui la lance à l'écran pendant qu'on parle est une démonstration. Chaque affirmation doit avoir sa contrepartie visuelle **au moment où elle est prononcée**.

Corollaire : si un passage ne peut pas être montré, il doit être coupé ou raccourci. Le texte pur appartient à la description.

## Structure

| Bloc | Durée | Ce qui se passe |
|---|---|---|
| **L'accroche** | 0–20 s | Le problème, chiffré. Pas de présentation, pas de « bonjour à tous ». |
| **La promesse** | 20–40 s | Ce que le spectateur saura faire à la fin. Une phrase. |
| **Le contexte** | 40 s–1 min 30 | Pourquoi le problème existe. C'est ici qu'on gagne la crédibilité. |
| **La démonstration** | 1 min 30–5 min | L'écran fait le travail. On commente ce qu'on voit. |
| **La preuve** | 5–7 min | Les chiffres, la mesure, le avant/après. **C'est le bloc que personne ne fait.** |
| **La nuance** | 7–8 min | Quand ça ne marche pas, pour qui c'est inutile. Ça crédibilise tout le reste. |
| **L'appel** | 8 min– | Une seule action. |

Les durées sont indicatives : c'est l'ordre qui compte, pas le minutage.

## L'humour

**Subtil, jamais appuyé.** Trois formes qui fonctionnent, une qui ne fonctionne pas.

Ce qui marche :
- **L'auto-dérision sur ses propres chiffres** — « j'ai 526 workflows, je ne sais plus ce que la moitié font »
- **Le décalage entre l'attente et le réel** — montrer un résultat qui déçoit, et le dire
- **L'aparté court**, une demi-seconde, jamais souligné

Ce qui ne marche pas : la blague annoncée, l'effet sonore de rire, la vanne qui interrompt la démonstration. Si l'humour ralentit la compréhension, il coûte plus qu'il ne rapporte.

**Règle de dosage : trois moments maximum sur un tuto de huit minutes.** Au-delà, le spectateur ne sait plus s'il regarde un cours ou un sketch.

## Les captures

- **Format natif 16:9**, jamais recadré depuis du vertical
- **Terminal en gros** — la taille de police par défaut est illisible en vidéo, monter à 16-18 pt minimum
- **Frappe caractère par caractère**, jamais du texte qui apparaît d'un coup : c'est ce qui donne la sensation de réel
- **Curseur visible** avec un effet au clic — Playwright ne le dessine pas nativement, il faut l'injecter
- **Les temps morts se coupent** : une génération de trois minutes se montre en dix secondes, avec un repère de durée à l'écran

⚠️ **Masquer systématiquement** : URL d'instances personnelles, clés d'API, chemins contenant des noms de clients, jetons dans les remotes git. Re-générer la capture avec un domaine d'exemple plutôt que flouter — un flou signale qu'il y a quelque chose à cacher.

## L'avatar

Reprendre la banque v3 et la chorégraphie de `veille-to-video-v3`, adaptée au 16:9 :

- **En incrustation**, coin bas-droite, sur les passages de démonstration
- **Plein cadre** sur l'accroche, la preuve et l'appel final
- **Audio natif coupé**, voix clonée posée par-dessus
- **Quand la voix parle, les lèvres doivent bouger** — vérifier avec `check_lips_rule.mjs`, dans sa version corrigée (celle du dossier `autoboost-videoboost-dialogue-organique`, qui ne jette plus les silences numériques)

## La voix

Webhook n8n `tts-gen`, **`voixUrl` obligatoire** — sans lui la branche part sur OpenAI et sort une voix qui n'est pas la sienne.
Contrôle par la mesure : **F0 médian attendu 114–133 Hz**. Autour de 200 Hz, c'est le repli, à refaire.

## Typographie

Reprendre `TYPO.md` de `autoboost-tuto-claude-code-mcp/`, en adaptant les positions au 16:9. Les valeurs de taille, de graisse et de couleur ne changent pas — c'est le point de réutilisabilité.

## Ce qu'il faut vérifier avant de publier

- Le mot-clé du CTA **a-t-il une porte active** dans Blotato ? Lister les automations avant d'annoncer un mot. Une vidéo a déjà récolté six commentaires sur un mot sans porte : les six personnes n'ont rien reçu.
- Aucune URL personnelle visible à l'image
- Le fichier fait-il moins de 35 s ? **Non — c'est un format long, la règle des 28-35 s ne s'applique pas ici.** Elle vaut pour le vertical.

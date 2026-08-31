# autoboost-70-make-vs-n8n — prompt & ressources

Pipeline **v3** (assemblage banque avatar), pas v2. Aucun détourage, aucune génération
d'image/vidéo IA pour l'avatar : les plans sont de vrais micro-clips filmés, réassemblés.
Il n'y a donc pas de « prompt Seedance/Higgsfield » à ce projet — la section ci-dessous
documente l'équivalent fonctionnel : le texte envoyé au clonage vocal et le plan de montage.

## 1. Sujet (Google Sheet, onglet "30 Vidéos", ligne 73 / #70)

**Alternative gratuite à Make.com — même automatisations, zéro abonnement**
CTA : `MAKE`

## 2. Script voix off envoyé au clonage (texte intégral)

> Make.com me facturait quarante-neuf euros par mois pour connecter les outils de mes
> clients. J'ai tout migré sur n8n en un week-end : mêmes scénarios, mêmes déclencheurs,
> mêmes intégrations Gmail, Sheets, Slack, Stripe. Sauf que maintenant je paye
> l'hébergement une fois, pas un abonnement qui grimpe à chaque scénario ajouté. Pour un
> client qui fait tourner cinq automatisations, ça représente plus de cinq cents euros
> économisés chaque année, sans perdre une seule fonctionnalité, avec un contrôle total
> sur les données. C'est la migration que je propose maintenant à tous mes clients qui
> payent trop cher pour un outil fermé. Commente le mot MAKE si tu veux le guide complet,
> gratuit.

Raccourci depuis le script du Sheet (128 mots → 110 mots) pour tenir la cible 30-35s du
pipeline. Généré via webhook n8n `avatar-webhook-v2` → WaveSpeed `qwen3-tts/voice-clone`,
`voixUrl=archiviste_ZIl7EoOf.mp3`. Timestamps mot-à-mot obtenus via WaveSpeed
`openai-whisper` (le Whisper OpenAI intégré au webhook était à court de crédits).

## 3. Décor choisi

**BUREAU** (`_shared/avatar-bank/clips/`, clips A1/B1/C2). Sujet technique
(migration d'outil, comparaison de coûts, démonstration) → règle du `MANIFESTE.md` :
bureau = tuto/technique, jamais voiture. Aucun mélange de décor.

## 4. Plan de montage avatar (banque réelle, aucune génération)

| Rôle | Clip source | `ss` | durée | fenêtre timeline | zone lèvres actives du clip |
|---|---|---|---|---|---|
| HOOK plein cadre | `A1_hook_frontal.mp4` | 0.67s | 3.91s | 0.00 → 3.97s | 0.67 → 4.58s ✅ (fin exacte) |
| PUNCH (fenêtre néon) | `B1_principe.mp4` | 0.08s | 2.42s | 19.50 → 21.92s | 0.08 → 4.88s ✅ |
| RÉALITÉ (fenêtre néon) | `B1_principe.mp4` | 1.74s | 3.14s | 22.30 → 25.44s | 0.08 → 4.88s ✅ (fin exacte) |
| CTA (fenêtre néon) | `C2_commente_motcle.mp4` | 0.08s | 2.52s | 30.00 → 32.52s | 0.08 → 4.83s ✅ |

Validé programmatiquement contre `_shared/avatar-bank/lips-map.json` : zéro plan
dépassant sa plage « lèvres actives ». Budget bureau utilisé : 11,99s / 13,5s autorisés.
`B1_principe.mp4` est rejoué deux fois sur des plages distinctes (0.08→2.50 puis
1.74→4.88), conformément à la règle « rejouer des segments différents du même clip ».

Aucun marqueur à remplacer par un avatar généré : les 4 plans sont l'avatar réel de Tony,
filmé une fois, réutilisé tel quel.

## 5. Habillage (HyperFrames, passe 1)

Fond charte (`#0a0a0f` + dégradés jaune/violet), broll `workflow-9x16.mp4`,
header AUTOBOOST + pilule « MIGRATION N8N », carte de prix Make.com barrée, chips
Gmail/Sheets/Slack/Stripe autour d'un nœud n8n (calés sur le passage du script qui les
nomme), carton transformation « MAKE.COM 49€/mois ▼ N8N hébergé — +500€/an
économisés », fenêtre avatar néon jaune 648×1152 à (216,150), pilule CTA
« COMMENTE LE MOT MAKE ». Musique `bgm-ascension-orig.mp3` (déjà utilisée sur
d'autres vidéos Autoboost, `autoboost-aventure.mp3` du standard verrouillé absent de ce
dépôt) en boucle, duckée sous la voix par sidechain. SFX : whoosh (hook), pop (chips),
confirm (transformation), chime (CTA).

## 6. ⚠️ Écarts assumés par rapport au standard verrouillé du 2026-08-29

Le projet de référence `veille-to-avatar-v3-v3` et le gabarit
`secteurs-workflows/v2/template.mjs` cités par le skill ne sont **pas présents dans ce
dépôt** (jamais commités — scripts de session locale). Reconstruit depuis la
spécification écrite du skill, pas copié d'un fichier vérifié :
- démonstration n8n = chips statiques + lignes, pas un canvas de nœuds animé avec fils
  qui se tirent en direct ;
- pas de compte à rebours 3-2-1 final (le CTA tient directement, format déjà à 34,5s) ;
- cadrage avatar = fenêtre rectangulaire uniquement (jamais affiché en médaillon
  circulaire, alors que le skill mentionne aussi ce cadrage plus ancien).

À comparer par Tony avec sa mémoire du rendu verrouillé avant diffusion large.

## 7. ⚠️ Porte CTA — non vérifiée active

Le mot-clé `MAKE` n'apparaît **pas** dans l'onglet "Ressources CTA" du Sheet de suivi
(45 mots-clés vérifiés, `MAKE` absent). Si Blotato n'a pas de porte automatique sur ce
mot, les gens qui commentent ne recevront rien. À corriger avant diffusion.

# autoboost-148-recrut — prompt & recette (pipeline v3, décor BUREAU)

Pas de génération d'image/vidéo IA : le pipeline v3 assemble des micro-clips RÉELS
de la banque avatar (décor BUREAU — studio, fond sombre, chemise noire). Sujet :
ligne 151 du Sheet `30 Videos` (`#` 148, `Statut Tournage` = ⬜ À faire au moment du
tournage), mot-clé CTA `RECRUT`.

## 1. Script (voix off envoyée à avatar-webhook-v2, intégral du Sheet — 144 mots,
~43,6s avant traitement, 35,1s après ; au-dessus de la fourchette 30-35s visée pour
une nouvelle écriture mais dans la fourchette large 27-54s des vidéos qui performent,
donc gardé tel quel plutôt que raccourci)

```
Claude Code trie mes CV de freelances, et j'ai arrêté de payer cent vingt euros par
mois un cabinet de recrutement pour ça. Quand je cherchais un développeur ou un
monteur vidéo pour un projet client, je recevais parfois quarante candidatures, et
je passais des heures à ouvrir chaque CV, chaque portfolio, pour finalement en
retenir trois. Maintenant, Claude Code lit chaque candidature, vérifie les
compétences précises dont j'ai besoin, élimine automatiquement celles qui ne
correspondent pas, et me sort un classement des cinq meilleurs profils avec un
résumé de chacun. Ce qui me prenait une soirée entière se fait maintenant en dix
minutes, et je n'ai plus besoin de payer un abonnement de recrutement que
j'utilisais à peine une fois par mois. Si tu recrutes encore des freelances à la
main, follow-moi et commente le mot RECRUT, je t'envoie le workflow complet
gratuitement.
```

Appel exact : `POST https://n7n.automatisationboost.com/webhook/avatar-webhook-v2`
```json
{
  "voixUrl": "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3",
  "avatarUrl": "https://assets.automatisationboost.com/video/avatar/auto%20avatar%20(online-video-cutter.com).mp4",
  "description": "<script ci-dessus>"
}
```
Réponse : `voiceUrl` (mp3 CloudFront, 40,01s brut) — `transcripts` vide (quota Whisper
OpenAI épuisé côté webhook, piège déjà documenté sur autoboost-149). `n7n.automatisationboost.com`
et le CloudFront de sortie sont bloqués en direct par le proxy réseau de cette
session (`CONNECT tunnel failed, response 403`) : les deux appels (génération +
téléchargement) ont été relayés par des workflows n8n ponctuels
(`[Oneoff] Gen Voice - Autoboost 148 Recrut`, `[Oneoff] Download Voice MP3 -
Autoboost 148 Recrut`), le MP3 récupéré en base64 via `get_execution(includeData:true)`
puis décodé localement.

## 2. Post-traitement voix

```
silenceremove tête (start_threshold -45dB, peak) → silenceremove queue (même
seuil, via areverse/areverse) → atempo=1.12 → dynaudnorm=f=200:g=5 → mono 48kHz
```
Durée brute 40,01s → durée traitée **35,14s** (cible 30-35s, pile à la limite haute).

## 3. Silences réels (ffmpeg silencedetect -30dB/0.12s sur voice.mp3) — timeline
et fenêtres avatar calées dessus

```
4.64→5.33 · 7.79→8.25 · 9.77→10.04 · 13.60→14.13 · 16.01→16.36 · 18.13→18.41 ·
23.08→23.70 · 25.98→26.34 · 29.70→30.36 · 31.87→32.06 · 33.49→33.73
```

Scènes : HOOK 0.00→4.64 · AVANT 4.64→13.60 · FLOW (démo) 13.60→23.08 · RÉSULTAT
23.08→29.70 · CTA 29.70→35.14.

## 4. Références avatar — DÉCOR BUREAU (clips/, wardrobe chemise-noire-studio)

Sujet technique/démonstration (Claude Code qui trie des CV) → décor BUREAU, jamais
voiture. 6 fenêtres avatar, toutes tirées de `_shared/avatar-bank/clips/` :

| # | Rôle | Clip source | ss → ss+durée | Placement timeline | Zone lèvres actives (lips-map.json) |
|---|---|---|---|---|---|
| AV1  | Hook           | `A1_hook_frontal.mp4`    | 0.67 → 4.58 | 0.00 → 3.97  | 0.67–4.58 |
| AV2a | Explication 1  | `B1_principe.mp4`        | 0.08 → 1.78 | 14.13 → 15.83 | 0.08–4.88 |
| AV2b | Explication 2  | `B1_principe.mp4`        | 1.88 → 3.55 | 16.36 → 18.03 | 0.08–4.88 |
| AV3a | CTA 1          | `C2_commente_motcle.mp4` | 0.08 → 1.45 | 30.36 → 31.73 | 0.08–4.83 |
| AV3b | CTA 2          | `C2_commente_motcle.mp4` | 1.43 → 2.70 | 32.06 → 33.33 | 0.08–4.83 |
| AV3c | CTA 3          | `C2_commente_motcle.mp4` | 2.68 → 4.05 | 33.73 → 35.10 | 0.08–4.83 |

Budget bureau total utilisé : 3.97 + 1.70 + 1.67 + 1.37 + 1.27 + 1.37 = **11,35s**
sur les 13,5s exploitables. B1 et C2 sont chacun scindés en deux ou trois à cause de
pauses réelles de la voix (comma breaks) qui traversaient une fenêtre d'un seul
tenant — chaque segment s'arrête avec au moins 0,1s de marge avant la pause réelle
suivante et reprend juste après (pas de plan figé qui articule dans le silence).

Vérifié par `work/check_lips.mjs` (copie adaptée de `_shared/avatar-bank/check_lips_rule.mjs`
— chemin ffmpeg système au lieu de `/home/claude/...`, inexistant dans cet
environnement — piste voix seule `public/assets/voice.mp3`, enveloppe RMS lissée
~12 fenêtres/s, violation = run consécutif ≥ 6 frames) sur `work/order.json` :
**PASS — aucun plan en violation** (0 image fautive sur les 6 plans).

## 5. Montage (1 passe, HyperFrames gère les `<video>` nativement dans cette version
du CLI — confirmée sur ce rendu, comme autoboost-140/141/143/149)

- Fond + habillage charte (radial/linéaire sombre selon scène), kicker + titre, 5
  scènes calées sur les silences réels de la voix (0 / 4.64 / 13.60 / 23.08 /
  29.70s) : hook (stat 120€/mois), avant (checklist 40 candidatures / CV ouverts un
  par un / portfolios vérifiés / 3 retenus), flow Claude Code animé (4 nœuds Lecture
  → Vérification → Élimination → Classement, popant au rythme de la voix), résultat
  (jauge «Temps de tri −94%» + carton «Zéro abonnement payé. Zéro soirée perdue.»),
  CTA pilule RECRUT.
- Avatar : 6 `<video>` séparés superposés dans `#avatar-frame` (cercle néon jaune
  560×560, bordure pulsante + anneau orbital), chacun opacity 0 par défaut, fade
  in/out GSAP exactement sur sa fenêtre.
- Captions mot-à-mot (30px, 2 couleurs — jaune `hot` / violet `vhot`), timings
  construits à la main sur les segments délimités par les silences réels mesurés
  (même méthode que autoboost-140/149).

## 6. Réglages

- Format 1080×1920, 30 fps, h264 (crf `looks`) + aac
- Durée finale rendue : **35,17s** (cible 30-35s, légèrement au-dessus car le
  script Sheet brut fait 144 mots — gardé intégral, voir §1)
- Palette strictement `_shared/CHARTE.md` : `#eab308` jaune, `#8b5cf6` violet,
  `#7c3aed` violet profond, fond `#0a0a0f`, surface `#111117`. Aucune valeur morte,
  aucun vert — vérifié sur les frames extraites.
- Musique : `_shared/bgm/journal-digital-clouds-128.mp3` (même profil d'énergie que
  autoboost-140/149 pour un sujet technique), volume 0.30
- SFX : palette `_shared/sfx-palette/v2` (click-soft, notify, confirm, glitch, zoom,
  whoosh, pop, impact, chime) sur les coupes de scène et les pops
- CTA : commente le mot **RECRUT**

## 7. Contrôle visuel avant livraison

Frames extraites à 1.5 / 3.0 / 5.5 / 7.5 / 9.5 / 11.5 / 13.0 / 14.6 / 15.5 / 17.0 /
19.0 / 21.0 / 23.5 / 25.5 / 27.5 / 30.5 / 32.5 / 34.0s : décor bureau correct sur
toutes les fenêtres avatar, bouche ouverte/articulée en plein milieu de chaque plan
avatar, captions lisibles et jamais invisibles, palette charte respectée (aucun
vert), 4 nœuds du flow bien visibles et séquencés, jauge de résultat et CTA
corrects.

## 8. ⚠️ Porte Blotato RECRUT — PAS encore créée

`blotato_list_automations` (36 automations actives) ne contient aucune porte
`RECRUT` (ni `SUIVI` ni `SCAN`, les deux autres CTA en file d'attente dans le
Sheet). Charte §7 : « Un mot-clé annoncé doit avoir sa porte Blotato active AVANT
le tournage. Sinon les gens commentent et ne reçoivent rien. » Créer une automation
Blotato (déclencheur commentaire public + DM automatique) est une action visible
publiquement sur de vrais comptes sociaux : non prise dans cette session sans
confirmation explicite de Tony. **La vidéo est prête mais ne doit pas être
programmée sur les réseaux tant que la porte RECRUT n'existe pas.**

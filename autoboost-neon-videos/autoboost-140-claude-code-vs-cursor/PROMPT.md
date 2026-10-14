# autoboost-140-claude-code-vs-cursor — prompt & recette (pipeline v3, décor BUREAU)

Pas de génération d'image/vidéo IA dans cette vidéo : le pipeline v3 assemble des
micro-clips RÉELS de la banque avatar (décor BUREAU — studio, fond sombre, chemise
noire). Ce qui suit est donc la recette complète et reproductible — l'équivalent du
« prompt » pour ce pipeline. Sujet choisi : ligne 142 du Sheet `30 Vidéos`
(`Statut Tournage` = ⬜ À faire), mot-clé CTA `IDE`.

## 1. Script (voix off intégrale envoyée à avatar-webhook-v2, raccourci à ~111 mots
pour tenir 30-35s — le script brut du Sheet faisait 145 mots)

```
Cursor facture vingt dollars par mois pour coder avec une IA dans ton éditeur.
Claude Code fait pareil, depuis ton terminal, sans abonnement obligatoire. Pas
d'interface à ouvrir : il lit ton projet entier, écrit le code, lance les tests,
corrige les erreurs, et pilote d'autres outils via MCP, ce que Cursor ne fait pas
nativement. Je l'utilise sur tous mes projets clients et je n'ai plus ouvert
Cursor depuis des semaines. La prise en main est un peu raide au début, ensuite
c'est deux fois plus rapide. Si tu payes encore un abonnement éditeur IA sans
être sûr d'en avoir besoin, commente le mot IDE, je t'envoie le guide
d'installation complet.
```

Appel exact : `POST https://n7n.automatisationboost.com/webhook/avatar-webhook-v2`
```json
{
  "voixUrl": "https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3",
  "avatarUrl": "https://assets.automatisationboost.com/video/avatar/auto%20avatar%20(online-video-cutter.com).mp4",
  "description": "<script ci-dessus>"
}
```
Réponse : `voiceUrl` (mp3 CloudFront, 30,65s brut) — `transcripts` vide (quota
Whisper OpenAI épuisé côté webhook, piège déjà documenté). Timings mot-à-mot
reconstruits par pondération longueur de mot + bonus ponctuation, normalisés sur
la durée réelle du MP3 (recette documentée dans `veille-to-video/SKILL.md`).

## 2. Post-traitement voix

```
silenceremove tête (start_threshold -45dB, peak) → silenceremove queue (même seuil,
via areverse/areverse) → dynaudnorm=f=200:g=5 → mono 48kHz
```
Durée brute 30,65s → durée traitée (silences de bord coupés) 30,07s.
Pas d'`atempo` : la durée tombait déjà dans la cible 30-35s.

## 3. Références avatar — DÉCOR BUREAU (clips/, wardrobe chemise-noire-studio)

Aucune image de référence à substituer : ce sont déjà des prises réelles de Tony
(pas de génération, pas d'avatar à remplacer). Trois fenêtres avatar, toutes
tirées de `_shared/avatar-bank/clips/`, même garde-robe (jamais mélangée avec le
set voiture) :

| # | Rôle | Clip source | ss → ss+durée | Placement timeline | Zone lèvres actives (lips-map.json) |
|---|---|---|---|---|---|
| AV1 | Hook plein cadre | `A1_hook_frontal.mp4` | 0.67 → 4.27 | 0.00 → 3.60 | 0.67–4.58 |
| AV2 | Explication (fenêtre) | `B1_principe.mp4` | 0.08 → 3.71 | 3.60 → 7.23 | 0.08–4.88 |
| AV3 | CTA (fenêtre) | `C2_commente_motcle.mp4` | 0.08 → 4.78 | 23.48 → 28.18 | 0.08–4.83 |

Budget bureau total utilisé : 3.60 + 3.63 + 4.70 ≈ 11,93s sur les 13,5s
exploitables. Vérifié par `work/check_lips.mjs` (adapté de
`check_lips_rule.mjs`, piste voix seule `voice_only.wav`) : **PASS — 0 plan en
violation** sur les 3.

## 4. Montage (2 passes)

- **Passe 1** — HyperFrames rend l'habillage (fond grille + glow néon, header
  AUTOBOOST + kicker « Claude Code vs Cursor », fenêtre néon 648×1152 @
  (216,150), démo terminal "claude corrige mon projet" avec checklist qui pop
  en rythme avec la voix, carton transformation « CURSOR 20$/MOIS ▼ TERMINAL,
  0€ », punch « raide au début… 2X PLUS RAPIDE », pilule CTA jaune pulsante,
  captions mot-à-mot 40px) avec la zone avatar vide (placeholder noir). Pas de
  balise `<video>` dans cette passe (`gsap.min.js` vendu localement, le CDN
  `cdn.jsdelivr.net` étant bloqué côté shell). `public/index.html`.
- **Passe 2** — ffmpeg overlay les 3 clips ci-dessus (plein cadre 1080×1920
  pour AV1, 642×1146 @ (219,153) pour AV2/AV3) + mixage audio final (voix +
  BGM `journal-digital-clouds-128.mp3` duckée en sidechain, volume 0.30,
  fade-in 1,2s).

## 5. Réglages

- Format 1080×1920, 30 fps, h264 (crf18) + aac 192k
- Durée finale : 30,07s
- Cercle néon jaune (repris de la v2) : bordure pulsante 3px `rgba(255,230,0,.6)`
  autour de la fenêtre avatar réelle (AV2/AV3), pas de détourage
- CTA : commente le mot **IDE**
- Musique : `_shared/bgm/journal-digital-clouds-128.mp3` (profil d'énergie
  vérifié : -11.9 à -20.7dB sur le passage utilisé, pas de montée brutale),
  `au-bord-des-etoiles` cité en exemple dans la charte n'existe pas dans cette
  banque locale.

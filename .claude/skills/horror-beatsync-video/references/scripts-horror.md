# 3 scripts TikTok — Automation Boost × "YOU CAN ASK THE FLOWERS (HORROR MIX)"

Tous calés sur la grille **mesurée** sur le fichier (voir SKILL.md §2) : montée `0-2.34s`, **drop à 2,34s**,
mini-drops à `10.36 / 18.38 / 26.40 / 34.42s` (période 8,02s). Les anciennes valeurs 3/11/19/27/35 étaient
0,65s trop tardives sur les 7 drops testés.
Creux de respiration juste avant chaque drop (~2,15 / 10,15 / 18,15 / 26,15s) — c'est là qu'on reprend son souffle.

---

## SCRIPT 1 — « Le restaurant fantôme » (HoReCa, ton horreur assumé)

| Temps | Musique | Plan | Texte parlé / à l'écran |
|---|---|---|---|
| 0-2.34s | Montée intro | [PLAN A — écran Claude] visage proche, lumière basse | « Il est 23h. Ton restaurant dort. Mais tes DM, eux... » |
| **2.34s** | **DROP** | Cut brutal → écran n8n qui s'anime | « ...répondent TOUT SEULS. » // `AUTO_PILOT` |
| 2.34-10.36s | Phrase 1 | [PLAN B — produit final] workflow en action | « Réservation reçue. Confirmée. Ajoutée au planning. Zéro humain. » |
| 10.36-18.38s | Phrase 2 | Retour visage, zoom punch | « Pendant que tes concurrents dorment, ton système bosse. C'est ça qui fait peur. » |
| 18.38-26.40s | Phrase 3 | Split screen avant/après | « 2h de DM par jour → 0 minute. 60h par mois récupérées. » |
| 26.40-34.42s | Phrase 4 | Visage, fond noir | « Commente le mot AUTO. Je t'envoie le workflow. Si t'oses. » // `// COMMENTE_AUTO` |

**Mot-clé CTA : `AUTO`.** Écrire « Commente **le mot** AUTO » et pas « Commente AUTO » — le TTS
prononce « Commande auto » sinon (piège vérifié, voir `veille-to-video` Étape 1).

---

## SCRIPT 2 — « La tâche qui te hante » (universel PME)

| Temps | Musique | Plan | Texte |
|---|---|---|---|
| 0-2.34s | Montée | Visage, chuchoté | « Il y a une tâche que tu refais chaque jour... depuis 3 ans. » |
| **2.34s** | **DROP** | Zoom violent + texte plein écran | « ELLE EST AUTOMATISABLE DEPUIS 3 ANS. » |
| 2.34-10.36s | Phrase 1 | Écran : calcul à l'écran | « 20 min par jour × 250 jours × 3 ans = 250 HEURES perdues. » |
| 10.36-18.38s | Phrase 2 | [PLAN A] démo rapide | « Moi je la tue en 15 minutes avec n8n. Regarde. » |
| 18.38-26.40s | Phrase 3 | [PLAN B] workflow qui tourne | « Déclencheur. Action. Résultat. Elle ne reviendra plus jamais. » |
| 26.40-34.42s | Phrase 4 | Visage, sourire | « Quelle tâche te hante, toi ? Dis-le en commentaire. » |

**Pas de mot-clé CTA** — c'est une question ouverte, donc pas d'auto-DM possible sur celui-ci
(le workflow n8n `U0U6yjMp88h9cH2A` déclenche sur un mot exact). Si on veut l'auto-DM, remplacer la
dernière phrase par un mot-clé et le déclarer dans le Sheet.

Le calcul du drop (`250 HEURES`) doit apparaître **en un seul bloc à 2,34s**, pas animé chiffre par
chiffre : le drop est un impact, pas une démonstration.

---

## SCRIPT 3 — « L'IA qui travaille la nuit » (Claude/agent, format flex)

| Temps | Musique | Plan | Texte |
|---|---|---|---|
| 0-2.34s | Montée | Écran noir, curseur qui clignote | « 3h du matin. Personne au bureau. Et pourtant... » |
| **2.34s** | **DROP** | Timelapse : posts publiés, mails envoyés | « ...tout continue. » // `NIGHT_SHIFT` |
| 2.34-10.36s | Phrase 1 | [PLAN B] pipeline en action | « Contenu généré. Visuel créé. Posté sur 3 réseaux. Automatiquement. » |
| 10.36-18.38s | Phrase 2 | Visage | « J'ai pas embauché. J'ai construit UNE FOIS. » |
| 18.38-26.40s | Phrase 3 | Écran : le workflow complet | « Notion → Claude → publication. 0€ de salaire. 24h/24. » |
| 26.40-34.42s | Phrase 4 | Visage, fond noir/or | « Commente le mot NUIT et je te montre comment. » |

**Mot-clé CTA : `NUIT`.** Le curseur qui clignote en 0-2,34s doit clignoter **sur le beat**
(0,50125s), pas au rythme CSS par défaut.

---

## Écrire un nouveau script sur cette grille

- 4 phrases de 8,02s + une montée de 2,34s. Une idée par phrase, jamais deux.
- La phrase de 8s fait **~24-26 mots max** au débit de marque (~3,3 mots/s) — et il faut y laisser le
  demi-souffle du creux. Viser 20-22 mots pour que ça respire.
- Le drop à 2,34s porte **la révélation**, pas le contexte. Le contexte, c'est la montée.
- Dernière phrase = CTA mot-clé (voir la liste des mots-clés existants dans `veille-to-video`,
  section Style obligatoire — ne pas réutiliser un mot déjà pris par une autre vidéo).

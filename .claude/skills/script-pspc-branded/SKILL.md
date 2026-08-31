---
name: script-pspc-branded
description: Écrit un script de vidéo sociale Automation Boost selon la structure PROBLÈME → SOLUTION → VALIDATION → CTA (PSVC). Format court 9:16, ton cash, preuve chiffrée personnelle, CTA gaté par mot-clé. Produit un script prêt à monter avec veille-to-video-v3 (voix clonée, banque avatar, captions). Déclencheurs : "écris un script", "script problème solution", "script PSVC", "nouveau script vidéo", "structure problème solution CTA".
---

# script-pspc-branded — La structure PROBLÈME → SOLUTION → VALIDATION → CTA

**Output :** un script prêt à monter (narration segmentée + beats visuels + mot-clé CTA + captions), pas une vidéo.
**Enchaîne avec** `/veille-to-video-v3` (style verrouillé) pour la fabrication, `/hook-puissant-branded` si le hook doit être spectaculaire, `/yapping-facecam-branded` si le rythme doit être ultra-serré.

Durée cible **30-45 s**. En dessous ça ne délivre rien, au-dessus ça décroche.

---

## Les 4 blocs

| Bloc | Temps | Ce qu'il fait | La règle qui compte |
|------|-------|---------------|---------------------|
| **PROBLÈME** | 0-8 s | Nommer une douleur que la personne vit *aujourd'hui* | **Une histoire vécue chiffrée**, jamais une généralité. Et **jamais l'outil en premier**. |
| **SOLUTION** | 8-22 s | Montrer le mécanisme, pas la promesse | On **montre à l'écran**. Si ça ne se voit pas, ça ne convainc pas. |
| **VALIDATION** | 22-32 s | Prouver que c'est réel | Une **preuve vérifiable** : un résultat, un chiffre mesuré, un écran réel. Pas un témoignage. |
| **CTA** | 32-40 s | Demander UNE action | Un **mot-clé unique** + le faux champ de commentaire incrusté. |

### 1. PROBLÈME (0-8 s)
- Ouvre sur **ta** galère, datée et chiffrée : « la semaine dernière j'ai passé 3 heures à monter une vidéo. Trois heures. Pour 30 secondes. »
- **Ne nomme aucun outil** ici (ni Claude, ni n8n, ni Seedance). L'outil tue l'identification.
- La personne doit se dire « c'est moi » avant la seconde 5.
- Formats qui marchent : la douleur perso chiffrée · la question qui pique (« tu sais pourquoi tu ne fais pas de vues ? ») · le pattern interrupt visuel (voir le template `_shared/hooks/chaos-automatiser/`).

### 2. SOLUTION (8-22 s)
- Explique **le mécanisme**, pas le bénéfice. « Je tape une phrase, elle écrit, monte, sous-titre » vaut mieux que « je gagne du temps ».
- **Chaque phrase = un changement à l'écran** (règle des 2-4 s). Écran figé = décrochage.
- Reconstruire les interfaces en HTML plutôt que générer : c'est net, gratuit, et ça reste sous contrôle.

### 3. VALIDATION (22-32 s)
C'est le bloc qu'on saute le plus souvent, et c'est celui qui fait la différence.
- Une **preuve montrable** : un site réellement en ligne, un post réellement programmé, un chiffre mesuré, un avant/après.
- **Interdits absolus** : témoignages inventés, revenus fictifs, promesses de gains. *(On a dû supprimer 3 faux témoignages d'une page de vente le 17/08 — pratique commerciale trompeuse, risque juridique réel, et ça décrédibilise tout le reste.)*
- Si tu n'as pas de preuve, **dis ce que tu as vraiment** : « je l'ai fait pour un client », « voilà le mien qui tourne depuis 3 jours ».

### 4. CTA (32-40 s)
- **Un seul mot-clé**, court, distinctif, en MAJUSCULES.
- ⚠️ **Vérifier qu'il est libre** (`blotato_list_automations`) et **qu'une vraie ressource existe derrière**. Un CTA sans ressource = une promesse non tenue à chaque commentaire.
- ⚠️ **Éviter les mots trop courants** (DM, INFO, LIEN…) : la gate se déclencherait sur du bruit et tu ne distinguerais plus un vrai opt-in.
- **Incruster le faux champ de commentaire** (barre d'icônes + le mot qui se tape lettre par lettre + bouton envoi) : c'est le levier n°1, la personne voit exactement le geste à faire.
- Un climax visuel juste avant aide : countdown 3-2-1, impact, décollage.

---

## 🎙️ LA VOIX DE TONY (à imiter — c'est ce qui rend le script reconnaissable)

Les scripts qu'il écrit lui-même ont une signature. Reprends-la, ne la lisse pas.

**Ses procédés récurrents :**

| Procédé | Exemples réels de Tony |
|---|---|
| **L'accusation frontale** | « Tu sais pourquoi tu ne fais pas de vues ? **Parce que ton contenu est mauvais.** Pas de hook, pas d'accroche, pas de demande d'interaction. » |
| **« Et si je te disais que… »** | « Et si je te disais que tu es en train de rater la plus belle opportunité de ta vie ? » / « Et si je te disais que j'ai la solution ? » |
| **L'ultimatum binaire** | « Soit tu montes dedans maintenant. Soit tu restes par terre. » / « Ceux qui me croient me suivent. Les autres, passez votre chemin. » |
| **Le compte à rebours final** | « 3… 2… 1… **Applique maintenant.** » / « IA. Go. » — quasi systématique en clôture |
| **L'anti-gourou** | « C'est pas une petite formation bullshit comme t'en vois partout sur internet. » |
| **Le don de temps** | « Le temps que MOI j'ai mis à le monter, toi t'as pas à le passer. **Voilà la vraie valeur. Point. C'est tout.** » |
| **Le triplet sec** | « Une idée. Une semaine de contenu. **Zéro excuse.** » — trois blocs courts, le dernier qui claque |
| **Le devenir** | « pour devenir **imbattable** » / « et deviens **imparable** » |

**Ce que ça donne comme rythme :** phrases très courtes, ponctuation forte, on assène puis on s'arrête. Pas de subordonnées, pas de « par ailleurs », pas de transition polie. Le script doit se lire comme quelqu'un qui te parle en te regardant dans les yeux, un peu trop près.

---

## 😏 L'HUMOUR (le sel — sans lui le ton devient donneur de leçons)

Son humour n'est pas de la vanne : c'est de **l'excès assumé**. Il en fait trop *en le sachant*, et c'est ça qui fait sourire.

**1. L'empilement over-confiant** — son running gag maison
> « C'est indéniable. Irréfutable. »
**Maximum 2**, jamais 3 (retour explicite de Tony le 17/08 : à 3 ça devient lourd). Varier d'une vidéo à l'autre : indéniable · irréfutable · incontestable · imparable · implacable · sans appel · formel · cash.

**2. L'auto-dérision sur le hook** — assumer qu'on exagère
> « Le hook est volontairement provocateur. Évidemment que [X] demande du travail. »
Ça désarme le cynique et ça crédibilise le reste.

**3. La parodie du gourou hustle** — le format le plus fort, à condition de virer
> « Si à la fin du primaire t'as pas généré un million, y a un problème psychologique. Va vendre des Bic à la récré, tu me remercieras dans 15 ans. »
⚠️ **Ne JAMAIS jouer ça au premier degré.** Le hook parodique doit être suivi d'un virage explicite (« bon, j'arrête de me foutre de toi — voilà le vrai truc ») et d'un contenu réellement utile. Sans le virage, tu deviens exactement ce que tu moques.

**4. L'exagération chiffrée** — comparaison absurde mais vraie
> « Un studio te facture 500 €. Moi : une phrase, deux minutes. »

**5. La punchline qui retourne le sujet**
> « T'as plus besoin d'être devant la caméra pour être partout. »
> « Tu ne travailles plus dans le système. Tu le construis. »
> « Arrête de travailler comme une machine. Construis-en une. »

**Le dosage :** 1 à 2 touches d'humour par script, jamais plus. L'humour sert le hook et la punchline — **jamais la validation** (le bloc preuve doit rester sobre, sinon il ne prouve plus rien).

---

## Les règles de langue (apprises à l'usage)

- **Ton cash, phrases courtes, verbes actifs.** Écrit pour être *dit*, pas lu.
- **Maximum 2 adjectifs empilés, jamais 3.** « C'est indéniable. Irréfutable. » ✅ — ajouter « Indiscutable » alourdit. Varier d'une vidéo à l'autre : indéniable / irréfutable / incontestable / imparable / implacable / sans appel / formel / cash.
- **Aucune promesse de revenu.** Ni « 100 €/jour », ni « des clients garantis ». On montre des tarifs praticables et des durées réelles, la personne calcule elle-même.
- **Aucune urgence artificielle**, aucun faux compte à rebours de places.
- ~15 caractères parlés par seconde : un script de 40 s ≈ 600 caractères de narration.

---

## Le squelette à remplir

```
MOT-CLÉ CTA : ________  (libre ? ressource associée ? ______)

PROBLÈME (0-8s)
  Ma galère vécue + le chiffre : ____________________
  La tension : ____________________

SOLUTION (8-22s)
  Le mécanisme en 3 étapes : ______ → ______ → ______
  Ce qu'on voit à l'écran à chaque étape : ____________________

VALIDATION (22-32s)
  Ma preuve montrable : ____________________
  (site en ligne / post programmé / chiffre mesuré / avant-après)

CTA (32-40s)
  Punchline : ____________________
  « Commente [MOT] et je t'envoie ______ »
```

---

## Exemple complet (à imiter, pas à copier)

> **PROBLÈME** — « La semaine dernière, j'ai passé trois heures à monter une seule vidéo. Trois heures. Pour trente secondes de contenu. »
> **SOLUTION** — « Aujourd'hui je tape une phrase. L'IA écrit le script, génère ma voix, monte les plans, colle les sous-titres. » *(à l'écran : l'interface, le texte qui se tape, les étapes qui se cochent)*
> **VALIDATION** — « Celle-là, elle a été produite comme ça. Et la précédente, et celle de demain — il y en a une chaque matin à 7h, je n'y touche pas. » *(à l'écran : les éditions réelles en ligne)*
> **CTA** — « Un studio te facture 500 € pour ça. Moi : une phrase, deux minutes. Commente **USINE**, je t'envoie le workflow. »

---

## Fabrication (pour enchaîner)

Passer le script à `/veille-to-video-v3` — style verrouillé : voix clonée (tts-gen + voixUrl archiviste, silences coupés, atempo ~1.12), **audio natif des clips avatar coupé**, avatar v3 qui **ponctue** (4-5 apparitions de 3-4 s, jamais en continu, jamais plein écran par-dessus la démo), captions mot-à-mot, BGM duckée en sidechain, 9:16 1080×1920.
Rôles de la banque avatar : **fixe** (hook//validation) · **geste** (insistance) · **relance** (transition) · **CTA**.
Hook spectaculaire disponible clé en main : `_shared/hooks/chaos-automatiser/` (variables en tête, animation intouchée).

## Checklist avant montage
- [ ] Le problème est **vécu et chiffré**, aucun outil nommé avant la seconde 8.
- [ ] Chaque phrase de la solution a **son changement à l'écran**.
- [ ] La validation montre une **preuve réelle** (pas un témoignage, pas un chiffre inventé).
- [ ] Le mot-clé est **libre** et **une ressource existe** derrière.
- [ ] Max 2 adjectifs empilés · aucune promesse de revenu · aucune urgence artificielle.
- [ ] Durée 30-45 s, ~15 car./s.

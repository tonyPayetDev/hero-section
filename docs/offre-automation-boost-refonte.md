# Offre Automation Boost — refonte pour vente assistée (setting / closing)

> Doc rédigé en français (contrairement à la convention "docs in English" du CLAUDE.md) :
> il contient des scripts de vente destinés à être copiés-collés tels quels vers des
> prospects francophones. Le rendre en anglais le rendrait inutilisable.
>
> **Scripts de vente (DM, appel 30 min, objections, relances) :**
> voir `docs/offre-declencheur-scripts-vente.md`.
>
> Date : 2026-09-02 · Sources internes : `STRATEGIE.md` (run du 31/08/2026),
> `automation-boost-emails/email-4-j8-offre-cta-stripe.html`, arborescence des sites clients.

---

## 0. Décision d'abord : le coaching à 1 000 €

### Ce qu'on sait de façon factuelle

| Fait | Source | Implication |
|---|---|---|
| « J-Roy » = `@jb.roy_`, déjà suivi comme **concurrent direct** dans `STRATEGIE.md` (20 mentions) | STRATEGIE.md | Ce n'est pas un mentor d'un autre marché : il vend le même service, à la même cible, sur le même créneau |
| Il a **1 580 abonnés** vs 151 pour Tony | §1 | 10x plus d'audience |
| Mais **190 vues/vidéo** vs **306** pour Tony (fenêtre 24–31/08, n=33 vs n=20) | §0.7, §7 | Tony fait +61 % de vues par vidéo malgré 10x moins d'abonnés |
| **+6 abonnés en 7 j sur 34 vidéos** (0,18/vidéo) vs +15 sur 19 (0,79/vidéo) | §0.7 | Tony est ≈4x plus efficace par publication |
| Prix passé de **3 000 € à 1 000 € pendant l'appel** | Appel du 02/09 | Une remise de 66 % improvisée signifie que le prix de 3 000 € n'était pas un vrai prix |

### Verdict

**Ne pas payer maintenant.** Pas parce que 1 000 € serait cher dans l'absolu — un vrai
accompagnement vente à 1 000 € est un prix de marché normal — mais pour trois raisons
précises :

1. **Sur la seule dimension mesurable, il n'est pas devant.** Son compte a 10x l'audience et
   fait moins de vues par vidéo, et sa croissance est quasi nulle (+6 abonnés en une semaine
   pour 34 vidéos publiées). Sa compétence en *setting/closing* peut être réelle et
   indépendante de ça — mais il n'y a aucune preuve, et la seule preuve disponible va dans
   l'autre sens.
2. **La remise 3 000 → 1 000 pendant l'appel est un signal négatif sur son propre offre.**
   Quelqu'un qui vend un système de closing et qui casse son prix de 66 % en direct démontre
   l'inverse de ce qu'il vend.
3. **Le timing est faux : le setting n'est pas le goulot d'étranglement actuel.** Voir §3 —
   l'économie d'un setter ne tient pas avant ~15 000 €/mois de CA fermé. Payer 1 000 € pour
   apprendre à recruter un setter aujourd'hui, c'est acheter la solution au problème d'après.
   Le vrai goulot est en §1 : l'offre n'a **pas de prix**, **pas de garantie**, et
   **pas de preuve chiffrée**, alors que 104 dossiers de sites clients existent dans le repo.

### Les 6 questions à poser avant de payer (si tu veux quand même y aller)

À poser telles quelles, par écrit, et à garder :

1. Combien de clients as-tu accompagnés qui partaient de **moins de 300 abonnés** ? Nomme-en 3
   et donne leur CA avant / après.
2. Qu'est-ce qui est livré exactement : combien d'heures en direct, sur combien de semaines,
   et qu'est-ce qui est juste des replays ?
3. Est-ce que tu fournis un setter, ou est-ce que tu m'apprends à en recruter un ? (Ce n'est
   pas du tout le même produit.)
4. Quelle est ta garantie ? Dans quelles conditions exactes je récupère les 1 000 € ?
5. Pourquoi 3 000 € affiché et 1 000 € pour moi ? Qu'est-ce qui est retiré du programme ?
6. Est-ce que j'ai le droit de continuer à publier sur le même créneau que toi
   (automatisation IA pour indépendants) pendant et après l'accompagnement ?

**Règle** : s'il refuse de répondre par écrit à la 1 et la 4, c'est non.

### Contre-proposition à lui faire

S'il y a une vraie compétence de closing en face, l'échange qui a du sens n'est pas 1 000 €
cash : **il ferme 3 de tes appels contre 30 % du CA encaissé sur ces 3 ventes.** S'il est bon,
il gagne autant et tu ne risques rien. S'il refuse, tu as ta réponse sur la valeur réelle.

---

## 1. Diagnostic de l'offre actuelle

Offre en production (email J+8 de la séquence Brevo) : **« Sprint Automatisation »**,
accompagnement sur-mesure 30 jours — audit, workflows n8n clé en main, formation, support
Slack 30 j, accès templates (valeur annoncée 400 €). Rareté : 4 clients/mois. Paiement Stripe.

### Équation de valeur

```
          Résultat rêvé  ×  Probabilité perçue de l'obtenir
Valeur = ────────────────────────────────────────────────────
          Délai          ×  Effort & sacrifice
```

| Levier | Note | Pourquoi |
|---|---|---|
| Résultat rêvé | 5/10 | « Ton business mérite d'être automatisé » n'est pas un résultat, c'est un slogan. Aucun chiffre, aucune situation d'arrivée nommée. |
| **Probabilité perçue** | **3/10** | **Contrainte bloquante.** Un seul cas client (HoReCa), sans nom, sans chiffre de ROI. Aucune garantie. 104 dossiers de sites clients livrés dans le repo — et zéro exploité en preuve. |
| Délai | 6/10 | « 30 jours » annoncé, mais aucune promesse de première victoire rapide. Le prospect ne sait pas ce qui se passe en semaine 1. |
| Effort & sacrifice | 7/10 | Le « je construis pour toi » est le vrai point fort. À garder et à amplifier. |

### Audit d'anatomie (6 composants)

| # | Composant | État |
|---|---|---|
| 1 | Livrable central | ⚠️ Présent mais générique (« les 3 automatisations à fort impact ») |
| 2 | Stack de bonus | ⚠️ Faible — « templates, valeur 400 € » non détaillé, donc non crédible |
| 3 | **Garantie** | 🔴 **Absente** |
| 4 | Rareté | 🟢 Réelle et défendable (4 clients/mois) |
| 5 | Nom | 🟢 « Sprint Automatisation » fonctionne |
| 6 | **Prix** | 🔴 **`{{PRIX}}€` — la variable n'est jamais remplacée.** L'email d'offre part sans prix. |

**Conclusion du diagnostic** : l'offre ne convertit pas parce qu'elle est invendable en
l'état, pas parce que le trafic manque. Un prix manquant et une garantie absente coûtent plus
cher que n'importe quel setter.

---

## 2. L'offre refondue — échelle à 3 paliers

Principe : le palier 1 est calibré pour être **fermable en un seul appel de 20 minutes** —
c'est lui qui rend un système de setting possible. Les 2 900 € et le récurrent viennent
ensuite, sur des clients qui ont déjà payé une fois.

### Palier 0 — « La carte des fuites » · 30 min · gratuit

Ce n'est pas un « appel découverte ». C'est un livrable nommé, ce qui change tout au setting :
le setter ne vend pas un rendez-vous, il vend un document.

- **Promesse** : en 30 minutes, tu repars avec les 3 tâches qui te coûtent le plus d'heures
  par mois, chiffrées en euros de ton temps, et laquelle est automatisable en premier.
- **Livrable** : un PDF d'une page envoyé dans l'heure qui suit l'appel (généré depuis le
  template, pas rédigé à la main).
- **Coût pour Tony** : 30 min + un template. C'est l'actif de setting le plus rentable à créer.

### Palier 1 — « Le Déclencheur » · 990 € · 7 jours ⭐ offre à 1 000 €

C'est **l'offre qui vaut 1 000 €** — celle qu'on peut vendre au téléphone sans deuxième appel.

- **Promesse** : une automatisation en production chez toi sous 7 jours, celle qui se rembourse
  la plus vite. Tu la vois tourner avant de décider quoi que ce soit d'autre.
- **Contenu** :
  - 1 appel de cadrage 45 min
  - 1 workflow n8n construit, testé, branché sur **tes** outils (pas une démo)
  - La vidéo de passation (2–4 min) qui montre le workflow tourner sur tes données —
    produite avec le pipeline vidéo existant, coût marginal quasi nul
  - 14 jours de support WhatsApp pour les ajustements
- **Ce qui n'est PAS inclus** (à dire explicitement, ça augmente la crédibilité) :
  les abonnements tiers, la refonte du site, les intégrations sur mesure hors n8n.
- **Garantie — « livré ou remboursé »** : le workflow tourne en production sous 7 jours
  ouvrés après l'appel de cadrage, ou remboursement intégral. Garantie **de livraison**, pas
  de résultat : elle ne dépend que de Tony, elle est donc tenable à 100 %.
- **Justification du prix, à dire tel quel** : « Si la tâche te prend 5 h par mois et que ton
  heure vaut 50 €, elle te coûte 3 000 € par an. Le Déclencheur coûte 990 € une fois. Le
  remboursement est atteint au 4ᵉ mois, et ensuite ça tourne tout seul. »

### Pourquoi 990 € et pas 500 €

C'est la question qui revient en premier, et l'intuition « je serais plus crédible moins cher »
est fausse dans les quatre dimensions à la fois.

**1. À 500 €, tu travailles à perte.** Le Déclencheur, c'est ~10 h de ton temps (cadrage 45 min,
construction du workflow, vidéo de passation, 14 jours de support). Un indépendant facture en
moyenne **50 % de son temps** — l'autre moitié part en prospection, appels non conclus, admin,
no-shows. Donc :

| Prix | € / h facturée | € / h réelle (÷2) |
|---|---|---|
| 500 € | 50 € | **25 €** |
| 990 € | 99 € | **50 €** |

À 25 € de l'heure réelle, charges comprises, tu ne finances ni ton matériel, ni tes
abonnements, ni les mois creux. Ce n'est pas un prix bas, c'est un prix qui ne tient pas.

**2. Il faut deux fois plus de tout pour le même revenu.** Pour atteindre 3 500 €/mois :

| | à 990 € | à 500 € |
|---|---|---|
| Ventes / mois | 3,5 | **7** |
| Appels à tenir (à 30 % de closing) | 12 | **24** |
| Heures de livraison / mois | 35 h | **70 h** |

70 h de livraison plus 24 appels par mois, seul, en continuant à publier : c'est mécaniquement
impossible. Le prix bas ne rend pas l'offre plus accessible, il rend le business infaisable.

**3. Entre 500 € et 990 €, le client ne franchit aucune nouvelle barrière.** Pour un dirigeant,
les vrais seuils de décision sont autour de **2 000 €** (il en parle à quelqu'un) et **5 000 €**
(il compare formellement plusieurs devis). En dessous, c'est une dépense pro qu'il décide seul,
déductible, TVA récupérable. 500 € et 990 € sont exactement la même décision pour lui — mais
pas pour toi.

**4. Sous 1 000 €, tu changes de catégorie mentale.** Sur un marché où l'acheteur ne sait pas
juger la qualité technique, le prix est un des rares signaux disponibles. Une automatisation à
500 € se range dans « bricolage d'un freelance », à 990 € dans « prestation d'un pro ». Tu ne
gagnes pas les clients hésitants en baissant, tu perds les clients sérieux.

**5. Sans marge, la garantie devient impossible.** « Livré sous 7 jours ou remboursé » suppose
que tu puisses absorber un remboursement de temps en temps. À 25 € de l'heure réelle, un seul
remboursement efface un mois.

### La seule remise honnête : le tarif fondateur

Si tu n'arrives pas encore à dire « 990 € » sans hésiter, la réponse n'est pas de baisser le
prix — c'est de faire un **échange explicite, limité et justifié** :

> « Je lance cette offre ce mois-ci. Pour les 3 premiers, c'est 690 € au lieu de 990 € — en
> échange je vous demande deux choses : le droit de publier votre cas avec les chiffres, et un
> témoignage une fois que le workflow tourne. Après ces 3-là, c'est 990 € pour tout le monde. »

Ce n'est pas une remise, c'est un troc : tu échanges 300 € contre la preuve chiffrée qui te
manque (§1, probabilité perçue 3/10). C'est daté, c'est motivé, et ça ne dévalue pas l'offre —
contrairement à un prix qu'on casse parce que le client tire dessus.

**Trois clients, pas plus, et tu remontes.** Si tu es encore à 690 € au 10ᵉ client, ce n'est
plus un tarif fondateur, c'est ton prix.

### Palier 2 — « Sprint Automatisation » · 2 900 € · 30 jours

L'offre actuelle, prix fixé et garantie ajoutée.

- **Promesse** : 3 automatisations en production en 30 jours + tu sais les modifier toi-même.
- **Contenu** : audit complet, 3 workflows n8n, formation 2 × 1 h enregistrée, support 30 j,
  bibliothèque de templates, documentation vidéo de chaque workflow.
- **Garantie — continuation conditionnelle** (meilleure que le remboursement sur un service) :
  « Si au bout de 30 jours les 3 workflows ne tournent pas, je continue gratuitement jusqu'à
  ce qu'ils tournent. »
- **Rareté** : 4 clients/mois — déjà en place, la garder telle quelle, elle est vraie.

### Palier 3 — « Pilote » · 690 €/mois · engagement 3 mois

Le palier qui change réellement le business : c'est du revenu qui ne se revend pas chaque mois.

- **Contenu** : maintenance et supervision des workflows existants, 1 nouvelle automatisation
  par mois, veille outils mensuelle, priorité de support.
- **Proposé uniquement** en fin de Palier 1 ou 2, jamais à froid.
- **Objectif** : 8 clients Pilote = 5 520 €/mois récurrent. C'est cet objectif-là qui rend un
  setter finançable (§3), pas la vente au ticket.

### Stack de bonus — uniquement des actifs qui existent déjà

À ne mettre que sur les paliers 2 et 3, et à chiffrer honnêtement :

| Bonus | Existe déjà ? | Valeur annoncée |
|---|---|---|
| Bibliothèque de workflows n8n | Oui | 400 € |
| Workflow prospection Google Maps → leads qualifiés | Oui (déjà offert en séquence email) | 300 € |
| Site vitrine déployé (Coolify) si le client n'en a pas | Oui — 104 sites déjà livrés | 900 € |
| Documentation vidéo de chaque workflow | Oui — pipeline vidéo interne | 250 € |
| Veille IA & automatisation mensuelle | Oui — série blog existante | 150 € |

**Règle** : ne jamais annoncer une valeur de bonus supérieure au prix du palier. Un bonus
« valeur 5 000 € » sur une offre à 2 900 € détruit la crédibilité au lieu de l'augmenter.

---

## 3. Le système de setting — et pourquoi le setter attend

### L'arithmétique, d'abord

Un setter se paie 50–150 € par rendez-vous qualifié, ou 5–10 % du CA fermé. Pour qu'un setter
gagne un revenu qui le fait rester (~1 500 €/mois à 10 %), il faut **15 000 € de CA fermé par
mois**. À 990 € le ticket et 30 % de taux de closing, cela demande :

```
15 000 € ÷ 990 €        ≈ 15 ventes / mois
15 ventes ÷ 30 %        = 50 appels qualifiés / mois
50 appels ÷ 4 semaines  ≈ 12–13 appels qualifiés / semaine
```

Avec 151 abonnés TikTok et ~300 vues par vidéo, 12 appels qualifiés par semaine issus du
contenu seul n'arriveront pas. **Recruter un setter maintenant, c'est embaucher quelqu'un qui
n'aura rien à setter.** Il partira en 3 semaines et l'expérience aura coûté le temps de
recrutement plus le coaching.

**Séquence correcte** : construire le *système* de setting maintenant (scripts, critères,
suivi) et le faire tourner soi-même → atteindre ~5 000 €/mois → *ensuite* déléguer le setting
à quelqu'un sur un système déjà prouvé. On ne délègue jamais un processus qu'on n'a pas
soi-même fait fonctionner.

### D'où viennent les leads (actifs déjà disponibles)

| Source | État | Volume potentiel |
|---|---|---|
| 104 dossiers de sites clients livrés | Existant, **non exploité** | Le gisement n°1 : ce sont des clients qui ont déjà payé |
| Séquence email Brevo J0→J8 | En place | Chaque téléchargement du guide = un lead tiède |
| CTA « commente X » TikTok/Instagram | En place mais faible (0–2 commentaires/vidéo) | À remplacer, voir §4 |
| Workflow scraping Google Maps | Existant | Prospection sortante HoReCa / commerce local |

### Critères de qualification (le setter doit surtout **disqualifier**)

Un rendez-vous n'est « qualifié » que si les 4 cases sont cochées :

- [ ] Activité qui encaisse déjà (pas un projet)
- [ ] Une tâche répétitive identifiée d'au moins **4 h/mois**
- [ ] La personne au téléphone peut décider seule d'une dépense de 1 000 €
- [ ] Créneau de 30 min bloqué dans l'agenda, confirmé la veille

Sinon : pas d'appel. Un appel non qualifié coûte plus cher qu'un rendez-vous manqué.

### Séquence de setting en DM (4 messages)

Règle : **on ne vend jamais en DM.** L'objectif unique du DM est le rendez-vous du Palier 0.

1. **Ouverture, ancrée sur un fait observable** (pas de « salut ça va ? ») :
   > « Salut {prénom} — j'ai vu que vous répondez encore à la main aux demandes de résa sur
   > Insta. Vous y passez combien de temps par semaine, à peu près ? »

2. **Réponse → chiffrage** :
   > « Ok, donc ~X h/mois. À la louche c'est {X×50} € de temps par mois sur une tâche qu'une
   > machine fait. Vous avez déjà tenté d'automatiser ça ? »

3. **Proposition du livrable, pas du rendez-vous** :
   > « Je fais un truc simple : 30 min, et je vous renvoie une page qui liste vos 3 plus
   > grosses fuites de temps chiffrées en euros, et laquelle est automatisable en premier.
   > Gratuit, et vous repartez avec la page même si on ne travaille jamais ensemble.
   > Jeudi 14 h ou vendredi 10 h ? »

4. **Confirmation la veille** (le message qui divise les no-shows par deux) :
   > « Toujours bon pour demain 14 h ? Je vous appelle sur ce numéro. Préparez juste une idée
   > du temps passé sur {la tâche} — c'est tout ce dont j'ai besoin. »

### Le seul indicateur à suivre

**Appels qualifiés bookés par semaine.** Pas les abonnés, pas les vues, pas les commentaires.
Cible réaliste sur 90 jours : 3/semaine en solo. À 30 % de closing sur le Palier 1, cela fait
≈ 3 500 €/mois. C'est le seuil à partir duquel la question du setter redevient légitime.

---

## 4. Ce qu'il faut faire cette semaine (avant de dépenser 1 €)

Par ordre de rentabilité décroissante — les 4 premiers points sont gratuits et se font en
moins de deux jours.

- [ ] **Remplacer `{{PRIX}}` par `990` dans `email-4-j8-offre-cta-stripe.html`.** L'email
      d'offre part actuellement sans prix. C'est le bug business le plus cher du repo.
- [ ] **Créer le lien Stripe « Le Déclencheur — 990 € »** et le brancher sur le CTA.
- [ ] **Écrire 3 études de cas chiffrées** à partir des 104 dossiers de sites clients :
      situation avant, ce qui a été livré, heures économisées ou CA généré. Sans chiffre, ce
      n'est pas une preuve. C'est ce qui fait passer la « probabilité perçue » de 3/10 à 7/10.
- [ ] **Ajouter la garantie « livré sous 7 jours ou remboursé »** dans l'email, sur la landing
      et dans le script d'appel.
- [ ] **Créer le template PDF « La carte des fuites »** (1 page, généré, pas rédigé).
- [ ] **Reprendre contact avec 20 anciens clients site** avec un message unique :
      « J'ai livré votre site en {mois}. Depuis, j'automatise aussi la partie qui vient
      après : les relances, les résas, les avis. 30 min pour voir ce qui est automatisable
      chez vous ? »
- [ ] **Changer le CTA vidéo** : le « commente le mot X » donne 0–2 commentaires/vidéo
      (`STRATEGIE.md` §4). Le remplacer par une question ouverte adressée à un métier précis
      (« Les restaurateurs : vous répondez encore à la main aux résas Insta ? »).

**Objectif de la semaine : 3 appels qualifiés bookés.** Si ces 3 appels ont lieu et que rien
ne se ferme, alors le problème est bien le closing — et à ce moment-là, payer quelqu'un pour
ça devient une décision fondée. Pas avant.

---

## 5. Récapitulatif — ce qui change

| | Avant | Après |
|---|---|---|
| Prix | `{{PRIX}}€` (absent) | 990 € / 2 900 € / 690 €/mois |
| Point d'entrée | Sprint 30 jours | Le Déclencheur, 7 jours, fermable en 1 appel |
| Garantie | Aucune | Livré sous 7 j ou remboursé (P1) · Continuation gratuite (P2) |
| Preuve | 1 cas client anonyme | 3 études de cas chiffrées tirées de 104 livraisons |
| Récurrent | Aucun | Pilote 690 €/mois |
| Setting | Inexistant | Livrable gratuit nommé + 4 critères de qualification + séquence DM |
| Setter | Envisagé maintenant | Reporté au-delà de 5 000 €/mois — le système d'abord |

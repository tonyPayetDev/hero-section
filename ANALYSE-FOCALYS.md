# Analyse — focalys.re

**Prospect** : Focalys — organisme de formation en prévention, santé-sécurité et hygiène
alimentaire à La Réunion et Mayotte. Certifié Qualiopi. « Au service des entreprises
réunionnaises depuis 2009. »
**Relevé** : 16 septembre 2026, sur le site en production — `curl` (codes HTTP, en-têtes,
temps de réponse, robots/sitemap) et lecture complète de 5 pages réellement récupérées :
accueil, `/nos-formations-en-hygiene-securite-aliments/`, `/formation/` (catalogue),
`/nous-contacter/`, `/mentions-legales/`. WordPress 7.1 + Elementor 4.2.4, plugin de
performance AccelerateWP, derrière Apache (pas de CDN détecté).
**Aucun contact n'a été pris avec Focalys.** Recherche et lecture publique uniquement.

`[lu]` = fait constaté sur la page citée. `[déduit]` = supposition de ma part, à confirmer
en rendez-vous.

---

## 1. Audit

### Ce qui coûte des clients, par ordre d'impact

#### 1. La formation qu'une entreprise est obligée de suivre se vend comme une formation optionnelle

**`[lu]`** La page dédiée à l'hygiène alimentaire (ROFHYA, HACCP, HSA, BPH, ISO 22000)
n'affiche **ni prix, ni durée, ni date de session en HTML**. Le seul bouton d'action est
« Je souhaite un devis », qui renvoie vers `/nous-contacter/` — un formulaire générique
(nom, prénom, fonction, société, téléphone, email, message), le même que pour n'importe
quelle autre thématique du catalogue (secourisme, RPS, habilitation électrique…).

Le seul calendrier concret est un **PDF de 16,3 Mo** (`Planning_inter_2026VF-01042026.pdf`),
qu'il faut télécharger pour voir une date.

C'est pourtant le produit le plus « captif » du catalogue : depuis 2004, toute entreprise
qui manipule des denrées alimentaires **doit** former son personnel — ce n'est pas un choix
d'achat, c'est une obligation légale que le site lui-même rappelle (règlement CE 852/2004,
Code rural L.233-4). Un acheteur contraint qui cherche un prix et une date ne trouve ni
l'un ni l'autre sans attendre un rappel humain.

#### 2. Les chiffres affichés se contredisent d'une page à l'autre

**`[lu]`** Page d'accueil : « **+3 500 participants formés/an** », « **93%** de
satisfaction », « **99%** de réussite ».
**`[lu]`** Page hygiène alimentaire : « Plus de **2 100** participants annuels », « taux
de satisfaction […] de plus de **92%** ».

Deux jeux de chiffres différents sur le même site, sans qu'on sache lequel est à jour ou
lequel se rapporte à quoi. Un prospect qui compare les deux pages avant de signer un devis
tombe sur une incohérence facile à remarquer.

#### 3. La méta-description du site ment sur son ancienneté

**`[lu]`** Balise `<meta name="description">` de l'accueil : *« Focalys accompagne
**depuis 10 ans** les entreprises réunionnaises… »*
**`[lu]`** Le contenu affiché sur cette même page dit : *« Au service des entreprises
réunionnaises **depuis 2009** »* et *« Focalys accompagne **depuis 2009** les
entreprises… »*.

2026 − 2009 = 17 ans, pas 10. La méta-description — invisible sur la page, visible dans
tout résultat de recherche Google ou partage de lien — a été écrite une fois vers 2019 et
n'a plus bougé depuis.

#### 4. Les mentions légales datent d'avant le RGPD, alors que le site collecte des données

**`[lu]`** *« Le site n'est pas déclaré à la CNIL car il ne recueille pas d'informations
personnelles. »*

C'est une formule pré-2018 (la déclaration CNIL a été supprimée par le RGPD) — et elle est
fausse dans les faits : le formulaire de contact demande nom, société, téléphone, email, et
porte une case *« J'autorise Focalys à conserver mes données transmises via ce
formulaire… »*, preuve qu'une collecte de données personnelles a bien lieu. Une mention
légale obsolète sur un site qui, par ailleurs, affiche un bandeau cookies RGPD complet
(nécessaire, fonctionnel, performance, analytique, publicité) : les deux n'ont pas été
écrits au même moment ni par la même personne.

#### 5. Une structure juridique d'une seule personne, pour un volume qui suppose une équipe

**`[lu]`** Mentions légales : *« Propriétaire : **FOCALYS – EI**, numéro 514 396 555
00021 – 10 Impasse des Pensées d'Eau, 97460 Saint-Paul »*. **EI = entreprise
individuelle**, pas de capital social, pas de raison sociale de société — une seule
personne physique porte juridiquement la structure.

Ce n'est pas un défaut en soi — beaucoup d'organismes de formation fonctionnent avec des
formateurs vacataires — mais ça crée une vraie question à poser plutôt qu'à supposer :
qui délivre concrètement 2 100 à 3 500 formations par an derrière une EI. **`[déduit]`**
probablement un réseau de formateurs sous-traitants, à confirmer.

#### 6. Aucune mention de financement (OPCO, CPF) sur la page qui en aurait le plus besoin

**`[lu]`** La page hygiène alimentaire ne mentionne ni OPCO, ni CPF, ni aucun mode de
prise en charge. Pour une formation obligatoire vendue à des entreprises, le financement
via l'OPCO est souvent l'argument qui débloque la décision d'achat — son absence sur la
page laisse penser que chaque entreprise doit demander cette information par téléphone ou
par le formulaire générique.

#### 7. Deux adresses différentes selon la page

**`[lu]`** Page contact : *« 8 rue des Argonautes, Espace Tamarun Bat D »*, La Saline-les-
Bains. **`[lu]`** Mentions légales : *« 10 Impasse des Pensées d'Eau, 97460 Saint-Paul »*.
Deux adresses réunionnaises distinctes, à environ 10 km l'une de l'autre. **`[déduit]`**
plausiblement une adresse d'exploitation (bureaux/salle de formation) et une adresse de
domiciliation de l'EI — pattern courant pour une entreprise individuelle, pas
nécessairement un problème, mais à faire confirmer en rendez-vous plutôt que de le
présenter comme acquis.

---

### Ce qui ralentit, mesuré en réel

Quatre pages mesurées au `curl`, sans mise en cache navigateur :

| Page | Code HTTP | Temps avant 1er octet (TTFB) | Temps total | Poids HTML |
|---|---:|---:|---:|---:|
| Accueil | 200 | 0,88 s | 1,38 s | 184 Ko |
| Hygiène alimentaire | 200 | 0,90 s | 1,39 s | 148 Ko |
| Contact | 200 | 0,95 s | 1,35 s | 111 Ko |
| Mentions légales | 200 | 0,90 s | 1,35 s | 112 Ko |

**Ce tableau ne mesure que le HTML** (pas les images, polices, scripts — pas de mesure
navigateur réelle effectuée ici). Même à ce niveau, un TTFB constant autour de 0,9 s malgré
un plugin de cache installé (AccelerateWP) suggère un hébergement partagé sans CDN devant
— le `server: Apache` des en-têtes et l'absence de tout en-tête Cloudflare/CDN le
confirment.

**Point positif mesuré** : `http://` → `https://` et `www.focalys.re` → `focalys.re`
redirigent proprement en 301 vers une seule URL canonique. Pas de fragmentation de domaine
comme observée chez d'autres prospects du secteur.

---

### Ce qui manque pour être trouvé et partagé

**`[lu]`** Le titre de l'accueil — *« Focalys | centre de formation en prévention santé et
sécurité Réunion »* (67 caractères) — ne contient ni « hygiène alimentaire », ni « HACCP »,
alors que c'est l'un des onze domaines mis en avant et une obligation légale récurrente
pour tout le secteur agroalimentaire et la restauration de l'île. La page dédiée, elle,
a un bon titre : *« Formations HACCP Réunion | Hygiène et Sécurité des Aliments »*.

**`[lu]`** Une image de partage (`og:image`) **existe** — le badge Qualiopi — donc un lien
partagé sur WhatsApp ou Facebook affiche une vignette. C'est mieux que la moyenne des
petites structures.

**`[lu]`** La page hygiène alimentaire porte des données structurées `FAQPage` (deux
questions balisées : compétences acquises, sanctions en cas d'absence de formation) — un
vrai point technique en sa faveur, rare chez ce type de site.

---

### Ce qui va bien, et qu'il ne faut pas casser

- **Certification Qualiopi affichée**, logo présent en plusieurs endroits, obligatoire
  pour que les formations soient finançables — c'est en place.
- **Domaine canonique propre** : une seule URL sert de référence, tout redirige dessus.
- **Contenu réellement substantiel** sur la page hygiène alimentaire : cadre réglementaire
  cité avec précision (CE 852/2004, Code rural L.233-4), méthode des 5 M expliquée,
  public visé détaillé, FAQ balisée.
- **Témoignages nommés** (LNA, Association Frédéric Levavasseur, PJJ STEMO) — pas de
  Lorem ipsum, contrairement à d'autres audits menés cette année.
- **Onze thématiques de formation** couvertes, pas seulement l'hygiène alimentaire —
  la matière est large et le site la présente correctement.

---

### Ce que je propose

Dans l'ordre du rendement, sans avoir vu l'envers du décor (voir section 2) :

1. **Transformer le PDF de planning en dates lisibles sur la page**, avec un prix (ou une
   fourchette) et un mode de financement affichés à côté de chaque formation obligatoire.
   C'est ce qui manque le plus à un acheteur pressé.
2. **Corriger la méta-description et harmoniser les deux jeux de chiffres** — moins d'une
   heure, et ça retire deux incohérences vérifiables par n'importe qui.
3. **Mettre à jour les mentions légales** (formule CNIL obsolète) en cohérence avec le
   formulaire de contact et le bandeau cookies déjà en place.
4. **Un calculateur de devis en ligne** pour la formation hygiène alimentaire (nombre de
   participants, inter/intra, financement) — remplace le formulaire générique par une
   réponse immédiate et qualifiée. Développement plus long, impact le plus direct sur le
   produit le plus demandé.

---

## 2. Questions à poser pendant l'audit / l'appel

Elles découlent directement des constats ci-dessus — pas de questions génériques.

### Volume et structure de délivrance

1. Sur les 2 100 à 3 500 participants formés par an (les deux chiffres apparaissent sur le
   site), **combien de sessions d'hygiène alimentaire/HACCP organisez-vous par mois**, et
   quelle est la part inter- vs intra-entreprise ?
2. Le site est déclaré comme une entreprise individuelle. **Qui anime concrètement les
   formations** — vous seul, des formateurs vacataires, une équipe salariée ? Combien de
   personnes au total interviennent sous la marque Focalys ?
3. Le planning inter n'existe qu'en PDF téléchargeable. **Comment ce planning est-il
   construit et mis à jour aujourd'hui** — un fichier Excel, un outil dédié, à la main
   chaque mois ?

### Inscriptions et relances

4. Aujourd'hui, quand une entreprise clique sur « Je souhaite un devis » ou remplit le
   formulaire de contact, **que se passe-t-il concrètement** : qui reçoit la demande, en
   combien de temps répondez-vous, et avec quoi (devis type, appel, email) ?
5. **Combien de demandes de devis recevez-vous par mois**, toutes formations confondues,
   et quelle proportion se transforme réellement en inscription ?
6. Existe-t-il une **relance automatique ou manuelle** pour une entreprise qui a demandé
   un devis mais n'a pas répondu ? Si oui, avec quel outil ?
7. Utilisez-vous un **CRM ou un tableau (Excel, Google Sheets, autre logiciel)** pour
   suivre les entreprises clientes, leurs sessions passées et leurs échéances de
   renouvellement ?

### Certificats et obligations réglementaires

8. Une fois une session terminée, **comment l'attestation ou le certificat de formation
   est-il délivré** aux participants — papier remis en salle, PDF envoyé par email,
   plateforme dédiée ?
9. **Gardez-vous une trace centralisée** de qui a été formé, quand, et sur quel module —
   notamment pour les contrôles Qualiopi et pour prouver la conformité d'une entreprise
   cliente en cas d'inspection ?
10. L'hygiène alimentaire est une formation à recycler périodiquement pour certains
    postes, et le personnel d'un restaurant tourne. **Relancez-vous les entreprises
    quand leur formation ou celle d'un nouvel employé arrive à échéance**, ou est-ce à
    elles de reprendre contact ?

### Paiement et financement

11. La page hygiène alimentaire ne mentionne aucun mode de financement. **Quelle part de
    vos clients paie via un OPCO plutôt que directement** ? Le circuit de prise en charge
    OPCO ralentit-il l'encaissement ou la mise en place de la session ?
12. **Comment sont réglées les factures aujourd'hui** — virement, prélèvement, délai
    moyen de paiement une fois la formation dispensée ?

### Mayotte et logistique

13. Le site mentionne des formations en intra à Mayotte en plus de La Réunion. **Comment
    est organisée la logistique côté Mayotte** — formateur qui se déplace, structure
    locale, fréquence des sessions là-bas ?

### Le site lui-même

14. Qui met à jour le site aujourd'hui (vous, un prestataire, personne depuis un moment) —
    ça expliquerait la méta-description figée depuis plusieurs années et les mentions
    légales pré-RGPD.

---

## 3. Closing

*Mécanique reprise du dossier Family Arena — reconnaître le vrai avant de vendre, chiffrer
l'écart plutôt que le déclarer, offrir quelque chose sans contrepartie, proposer un nombre
limité d'automatisations directement adossées à un constat, et nommer ce qui reste à
vérifier ensemble plutôt que de faire semblant de tout savoir.*

### Ce qu'il faut dire en premier — et c'est vrai

> « Avant de parler de ce qui coince, deux choses qui vont bien chez vous et qui ne sont
> pas si fréquentes : vous êtes certifié Qualiopi, votre page hygiène alimentaire cite le
> bon règlement européen et le bon article du Code rural — c'est du contenu écrit par
> quelqu'un qui connaît le sujet, pas une page générique. Et vos témoignages sont de
> vraies entreprises, avec un nom et une fonction. Beaucoup de sites que j'ouvre mettent
> encore du texte de remplissage à la place. »

### Le constat, formulé simplement

> « Votre formation hygiène alimentaire, ce n'est pas un produit que les entreprises
> achètent parce qu'elles en ont envie — c'est une obligation légale. Un restaurateur qui
> ouvre la semaine prochaine n'a pas le choix : il doit former son personnel. C'est le
> produit le plus facile à vendre de tout votre catalogue.
>
> Et c'est le seul où, sur votre site, je ne trouve ni prix, ni durée, ni date. Juste un
> PDF de 16 mégas à télécharger pour voir un calendrier, et un formulaire générique — le
> même que pour une formation en secourisme ou en habilitation électrique. Le client qui
> est obligé d'acheter est celui à qui vous en dites le moins. »

### Ce que j'apporte aujourd'hui, sans contrepartie

- **Une page de devis refaite** pour la formation hygiène alimentaire : prix ou
  fourchette par format (inter/intra), durée, dates lisibles sans PDF, mention du
  financement OPCO. Elle est visible ici :
  **previsualisation.automatisationboost.com/focalys-audit**
- **La liste des deux incohérences de chiffres et de la méta-description obsolète**,
  prêtes à corriger en moins d'une heure — inutile d'attendre un prestataire pour ça.

Les deux sont à vous, que la suite se fasse ou non.

### Les automatisations que je mettrais en place en premier

**1. Le devis en ligne pour l'hygiène alimentaire, avec réponse immédiate.**
Un calculateur simple — nombre de participants, inter ou intra, financement souhaité — qui
sort un devis indicatif tout de suite, au lieu de faire attendre un rappel. C'est le
produit le plus demandé et le moins instrumenté du catalogue.
*Ce qu'il me faut de vous : votre grille tarifaire par format, et les conditions de prise
en charge OPCO que vous appliquez aujourd'hui.*

**2. Le suivi et la relance des échéances de renouvellement.**
Chaque entreprise cliente a une date où son personnel doit être re-formé ou complété. Si
ce suivi n'existe pas encore de façon centralisée, c'est un revenu récurrent qui dépend
aujourd'hui de la mémoire de quelqu'un plutôt que d'un système.
*Ce qu'il me faut de vous : comment vous suivez vos clients aujourd'hui — un fichier, un
outil, rien — et à quelle fréquence une entreprise doit revenir se former.*

**3. La délivrance et l'archivage automatique des attestations.**
Confirmation d'inscription, rappel avant la session, puis attestation générée et envoyée
automatiquement à la fin — avec une trace centralisée, utile le jour d'un contrôle
Qualiopi ou d'une inspection chez votre client.
*Ce qu'il me faut de vous : le format actuel de l'attestation et comment elle est remise
aujourd'hui.*

### Ce qu'on regarde ensemble

- Les deux chiffres de fréquentation qui ne se recoupent pas (3 500 contre 2 100
  participants par an) — lequel est le bon aujourd'hui ?
- Le fonctionnement réel derrière une structure en entreprise individuelle qui affiche un
  volume de plusieurs milliers de stagiaires par an — pour savoir où l'automatisation
  aide vraiment, et où elle ne remplace personne.

### La phrase de fin

> « Rien de ce que je viens de montrer n'est une critique de votre pédagogie ou de votre
> contenu — je n'ai pas assisté à une session, je ne peux pas en juger. Ce que j'ai
> regardé, c'est le chemin entre le moment où une entreprise réunionnaise doit vous
> trouver, et le moment où elle paie une formation qu'elle est de toute façon obligée de
> suivre. Aujourd'hui, ce chemin passe par un PDF et un formulaire générique. Je vous
> propose qu'on prenne trente minutes pour regarder ensemble ce que ça vous coûte
> réellement en devis qui traînent — et ce que ça changerait de le rendre immédiat. »

---

## Sources

- [focalys.re](https://focalys.re/) — accueil, relevé 16/09/2026
- [focalys.re/nos-formations-en-hygiene-securite-aliments/](https://focalys.re/nos-formations-en-hygiene-securite-aliments/) — relevé 16/09/2026
- [focalys.re/formation/](https://focalys.re/formation/) — catalogue, relevé 16/09/2026
- [focalys.re/nous-contacter/](https://focalys.re/nous-contacter/) — relevé 16/09/2026
- [focalys.re/mentions-legales/](https://focalys.re/mentions-legales/) — relevé 16/09/2026
- Mesures techniques : `curl` (codes HTTP, en-têtes, TTFB, robots.txt, sitemap), 16/09/2026

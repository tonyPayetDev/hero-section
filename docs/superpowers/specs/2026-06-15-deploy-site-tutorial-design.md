# Design : Page Tutoriel Deploy-Site

**Date** : 2026-06-15  
**Public** : Débutants totaux  
**Domaine** : automatisationboost.com  
**Objectif** : Guide complet et simple pour déployer un site statique via le skill deploy-site

---

## Vue d'ensemble

Page web single-page responsive, simple et lisible, qui guide un débutant complet à travers tout le processus de déploiement de son site, des prérequis à la mise en ligne.

**Format** : HTML + CSS simple, responsive (mobile/desktop), sans framework lourd.  
**Sections** : Tout scrollable dans une seule page.  
**Contenu** : Texte clair + captures d'écran + code snippets simples.

---

## Architecture de la page

### 1. Header
- Logo / branding simple
- Titre accrocheur : "Déploie ton site en 5 minutes ⚡"
- Sous-titre : "Guide complet du skill deploy-site pour débutants"

### 2. Intro / Hero
- Explication simple : Qu'est-ce qu'on va faire ? Pourquoi c'est utile ?
- Durée estimée : 5-10 min
- Pas de jargon technique

### 3. Section 1 : Prérequis
**Ce que tu auras besoin :**

Checklist avec 4 prérequis :

1. **Claude Code installé sur ton VPS**
   - Explication : "C'est l'outil qui va automatiser le déploiement"
   - Lien vers doc Claude Code
   - Capture d'écran : Claude Code en action
   - Pas de détail technique, juste "voilà à quoi ça ressemble"

2. **Un compte GitHub**
   - Lien pour créer un compte si besoin
   - Explication simple : "C'est où on va ranger ton code"
   - Capture d'écran : Repository GitHub créé

3. **Un compte Coolify**
   - Lien pour créer un compte
   - Explication : "C'est le service qui va héberger ton site"
   - Capture d'écran : Tableau de bord Coolify

4. **Un site local prêt**
   - Explication : "Des fichiers HTML/CSS/JS sur ton ordi"
   - Exemple simple : "Un dossier `mon-site/` avec `index.html`, `style.css`, etc."
   - Pas besoin d'être complexe

---

### 4. Section 2 : Préparer ton site

**3 étapes visuelles** avec captures d'écran :

#### Étape 1 : Organise tes fichiers
- Structure simple d'un site :
  ```
  mon-site/
  ├── index.html
  ├── style.css
  ├── script.js
  └── images/
      └── logo.png
  ```
- Capture : Terminal montrant `ls -la`

#### Étape 2 : Crée le dossier projet
- Commande simple : `mkdir mon-site && cd mon-site`
- Capture : Terminal

#### Étape 3 : Teste en local
- Explication : "Vérifie que ton site marche avant de le déployer"
- Commande : `python -m http.server` ou `npx serve`
- Capture : Site ouvert dans le navigateur

---

### 5. Section 3 : Utiliser le skill deploy-site

**Étapes numérotées** (c'est LE cœur du tutoriel) :

#### Étape 1 : Crée un repo GitHub
- Guide simple :
  1. Va sur github.com
  2. Clique "New repository"
  3. Nomme-le `mon-site`
  4. Clique "Create"
- Captures d'écran à chaque étape

#### Étape 2 : Pousse ton code sur GitHub
```bash
cd mon-site
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tonusername/mon-site.git
git branch -M main
git push -u origin main
```
- Explication simple : "On envoie nos fichiers sur GitHub"
- Capture : Terminal montrant le push réussi

#### Étape 3 : Lance le skill deploy-site
```bash
deploy-site mon-site/
```
- Ou depuis Claude Code : `/deploy-site`
- Explication : "Le skill va :
  1. Vérifier que c'est bon sur GitHub
  2. Créer une app sur Coolify
  3. Attendre que ça soit en ligne
  4. Te donner l'URL"
- Capture : Terminal montrant le résultat `SITE_EN_LIGNE: https://...`

#### Étape 4 : Ton site est en ligne !
- Capture : Le site ouvert dans le navigateur
- Explique : "Tu peux maintenant partager l'URL"

---

### 6. Section 4 : Bonus — Termux (Pour les avancés)

**Note en bas de page :**

> **Bonus pour utilisateurs avancés 🤖**  
> Tu peux aussi déployer depuis ton téléphone avec **Termux**.  
> Termux te permet de faire du développement et des déploiements directement sur Android.
> 
> [Lien vers Termux sur Google Play Store]  
> Guide rapide : [Lien vers doc Termux]

---

### 7. Footer
- Liens utiles : Docs Claude Code, GitHub, Coolify
- Contact / support : Email ou lien vers aide
- Copyright simple

---

## Design visuel

**Style** :
- Couleurs : Minimaliste (noir/blanc + 1-2 couleurs accent)
- Font : Simple (sans-serif, facile à lire)
- Spacing : Aéré, pas serré
- Responsive : Ça marche sur téléphone ET desktop

**Captures d'écran** :
- Minimalistes (pas besoin de détail excessif)
- Avec des flèches / annotations simples si besoin
- Avec alt-text pour l'accessibilité

**Code snippets** :
- Copyable (bouton "Copier")
- Syntax highlighting simple
- Pas de code complexe (juste les commandes essentielles)

---

## Flux utilisateur

```
Arrive sur la page
    ↓
Lit l'intro (30 sec)
    ↓
Vérifie les prérequis (2 min)
    ↓
Prépare son site (1-2 min)
    ↓
Utilise deploy-site (1 min)
    ↓
Son site est en ligne ! ✅
    ↓
(Optionnel) Explore Termux
```

---

## Checklist de contenu

- [ ] Screenshots pour chaque étape prérequis
- [ ] Screenshots pour préparer le site (3 étapes)
- [ ] Screenshots pour GitHub (4-5 étapes)
- [ ] Screenshots pour push Git
- [ ] Screenshots pour deploy-site (avant/après)
- [ ] Lien Termux en bas
- [ ] Pas de jargon technique (ou expliqué simplement)
- [ ] Code snippets copyable
- [ ] Responsive sur mobile
- [ ] Accessible (alt-text, contraste)

---

## Hébergement & déploiement

- **Domaine** : automatisationboost.com
- **Déployer avec** : le skill deploy-site lui-même (meta ! 😄)
- **Format** : HTML statique simple (pas de backend)


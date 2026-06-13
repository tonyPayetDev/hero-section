# Landing Page AutomatisationBoost — Sélecteur de profil dynamique

**Date :** 2026-06-09
**Statut :** Approuvé

---

## Objectif

Créer une nouvelle landing page (`/work/automationboost/landing.html`) qui :
1. Positionne AutomatisationBoost sur "automatiser votre vie pour gagner en énergie et temps"
2. Qualifie le visiteur via un sélecteur de profil (PME / Freelance / Auto-entrepreneur)
3. Adapte dynamiquement le contenu selon le profil choisi
4. Capture les leads via un formulaire → webhook n8n

---

## Audience cible

- **PME** : structure avec équipe, problèmes d'admin et de process
- **Freelance** : travailleur solo, perd du temps sur onboarding/facturation/contenu
- **Auto-entrepreneur** : en lancement, veut gérer tout seul sans se noyer

---

## Architecture de la page

### 1. Navbar
- Logo `AutomatisationBoost` (⚡)
- CTA droit : `[Démarrer mon diagnostic →]` — scroll vers formulaire

### 2. Hero
- **Headline :** "Automatise ta vie. Récupère ton énergie."
- **Sous-titre :** "Stop aux tâches répétitives. Je te livre une automatisation IA sur-mesure en 48h — pour que tu te concentres sur ce qui compte vraiment."
- **CTA :** `[Choisir mon profil →]` — scroll vers sélecteur de profil
- Pas de stats inventées — section épurée

### 3. Douleurs communes
Trois bullets partagées par tous les profils :
- "Tu passes des heures sur des tâches qui pourraient tourner seules"
- "Tu sais que l'automatisation existe — mais tu n'as jamais eu le temps de t'y mettre"
- "Ton business avance, mais trop lentement par rapport à l'énergie que tu y mets"

### 4. Sélecteur de profil
Trois cartes cliquables, une seule active à la fois :

| Carte | Icône | Label sous-titre |
|---|---|---|
| PME | 🏢 | "J'ai une équipe" |
| Freelance | 💻 | "Je travaille seul" |
| Auto-entrepreneur | ⚡ | "Je lance mon activité" |

- Clic sur une carte → met à jour le bloc dynamique + champ caché `profil`
- Carte active : bordure dorée + fond légèrement éclairé
- Par défaut : aucune carte sélectionnée (le bloc dynamique est masqué)

### 5. Bloc dynamique (affiché après sélection de profil)

Contenu adapté selon la carte active :

**PME**
- Titre : "Automatise ce qui freine ta croissance"
- Exemples : Devis générés automatiquement · Relances clients sans effort · Rapports hebdo auto-envoyés
- Bénéfice : "Économise 15h/semaine sur l'admin"

**Freelance**
- Titre : "Concentre-toi sur tes missions, pas l'admin"
- Exemples : Onboarding client automatique · Facturation sans y penser · Contenu publié pendant que tu dors
- Bénéfice : "Récupère 10h/semaine pour des missions qui paient"

**Auto-entrepreneur**
- Titre : "Lance-toi sans te noyer dans les outils"
- Exemples : Réponses aux prospects 24/7 · Gestion des commandes en pilote auto · CRM qui se remplit tout seul
- Bénéfice : "Gère tout seul sans y passer tes nuits"

Transition : fade-in CSS à l'affichage du bloc.

### 6. Formulaire
- Titre : "Prêt à récupérer ton temps ?"
- Champs visibles :
  - Prénom (required)
  - Email (required)
  - Message (optionnel, placeholder : "Décris ta situation en quelques mots…")
- Champs cachés :
  - `profil` — valeur : PME / Freelance / Auto-entrepreneur (mis à jour par JS)
  - `utm_source`, `utm_campaign`, `utm_medium` — lus depuis `window.location.search`
- CTA : `[Démarrer mon diagnostic gratuit →]`
- Soumission : `fetch()` POST vers webhook n8n (URL configurable en constante JS)
- Après soumission : masquer le formulaire, afficher un message de confirmation inline

### 7. Footer
- Liens : Accueil · Mentions Légales · Politique de Confidentialité · CGV
- Email de contact : tony.payet.professionnel@gmail.com

---

## Stack technique

- **HTML/CSS/JS vanilla** — cohérent avec `/work/automationboost/index.html`
- Pas de framework, pas de dépendance externe
- CSS : `landing.css` séparé qui importe les variables de `style.css`. Les composants nouveaux (cards profil, bloc dynamique) ont leurs propres classes.
- JS : dans un `<script>` en bas de page

---

## Logique JS

```js
// 1. Sélecteur de profil
cards.forEach(card => card.addEventListener('click', () => {
  setActiveProfile(card.dataset.profile); // 'pme' | 'freelance' | 'autoentrepreneur'
}));

// 2. Mise à jour champ caché + bloc dynamique
function setActiveProfile(profile) {
  document.querySelector('[name="profil"]').value = profile;
  renderDynamicBlock(profile);
  dynamicBlock.classList.remove('hidden');
}

// 3. Capture UTM depuis URL
['utm_source','utm_campaign','utm_medium'].forEach(param => {
  const val = new URLSearchParams(window.location.search).get(param) || '';
  document.querySelector(`[name="${param}"]`).value = val;
});

// 4. Soumission formulaire → n8n
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  await fetch(N8N_WEBHOOK_URL, { method: 'POST', body: new FormData(form) });
  showConfirmation();
});
```

---

## Payload n8n (exemple)

```json
{
  "prenom": "Marie",
  "email": "marie@example.com",
  "message": "Je veux automatiser mes relances",
  "profil": "freelance",
  "utm_source": "instagram",
  "utm_campaign": "boost48h-juin",
  "utm_medium": "paid"
}
```

---

## Fichiers à créer / modifier

| Fichier | Action |
|---|---|
| `/work/automationboost/landing.html` | Créer — nouvelle landing page |
| `/work/automationboost/assets/css/landing.css` | Créer — styles spécifiques à la landing (sélecteur de profil, bloc dynamique, états actifs) |

Le fichier `index.html` existant n'est pas modifié.

---

## Ce qui est hors scope

- A/B test par URL (prévu plus tard, infrastructure prête via champs UTM)
- Intégration Calendly
- Version multilingue
- Analytics (Google Tag Manager, etc.)

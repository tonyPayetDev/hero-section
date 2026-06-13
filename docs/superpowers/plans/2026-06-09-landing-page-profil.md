# Landing Page Profil — AutomatisationBoost Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Créer `/work/automationboost/landing.html` — landing page dynamique avec sélecteur de profil (PME / Freelance / Auto-entrepreneur), bloc de contenu adaptatif et formulaire → webhook n8n.

**Architecture:** Page HTML/CSS/JS vanilla. Un fichier CSS dédié (`landing.css`) étend le système de design existant (`style.css`). Tout le JS est inline en bas de page. Le profil sélectionné met à jour un champ caché et re-rend un bloc de contenu dynamique avant le formulaire.

**Tech Stack:** HTML5, CSS3 (variables CSS depuis style.css), JS vanilla (fetch, FormData, URLSearchParams)

---

## Fichiers

| Fichier | Action |
|---|---|
| `/work/automationboost/assets/css/landing.css` | Créer |
| `/work/automationboost/landing.html` | Créer |

---

## Task 1 : Créer landing.css

**Files:**
- Create: `/work/automationboost/assets/css/landing.css`

- [ ] **Step 1 : Créer le fichier CSS complet**

```css
/* landing.css — Styles spécifiques à la landing page profil */

/* ── SECTION BASE ──────────────────────────────────── */
.lp-section {
  position: relative;
  z-index: 1;
  padding: 80px 20px;
  max-width: 960px;
  margin: 0 auto;
}

.lp-section-title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(1.4rem, 3vw, 2rem);
  font-weight: 700;
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 40px;
  text-align: center;
}

/* ── HERO ──────────────────────────────────────────── */
.lp-hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 120px 20px 80px;
  position: relative;
  z-index: 1;
}

.lp-hero-inner {
  max-width: 760px;
}

.lp-hero-badge {
  display: inline-block;
  background: var(--gold-glow);
  border: 1px solid var(--gold);
  color: var(--gold);
  font-family: 'Rajdhani', sans-serif;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 3px;
  text-transform: uppercase;
  padding: 6px 18px;
  border-radius: 20px;
  margin-bottom: 28px;
}

.lp-hero-title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(2.2rem, 6vw, 4rem);
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 24px;
  color: var(--text);
}

.lp-hero-title .accent {
  color: var(--gold);
  text-shadow: var(--shadow-gold);
}

.lp-hero-subtitle {
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  color: var(--text-light);
  line-height: 1.7;
  max-width: 600px;
  margin: 0 auto 40px;
}

.lp-hero-cta {
  display: inline-block;
  background: var(--gold);
  color: #000;
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 16px 40px;
  border-radius: var(--radius);
  text-decoration: none;
  transition: box-shadow 0.3s, transform 0.2s;
}

.lp-hero-cta:hover {
  box-shadow: var(--shadow-gold);
  transform: translateY(-2px);
}

/* ── PAIN POINTS ────────────────────────────────────── */
.lp-pain {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 60px 40px;
  margin: 0 auto;
  max-width: 760px;
  position: relative;
  z-index: 1;
}

.lp-pain-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.lp-pain-list li {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  font-size: 1.1rem;
  color: var(--text);
  line-height: 1.5;
}

.lp-pain-list li::before {
  content: '✗';
  color: var(--red);
  font-size: 1.2rem;
  flex-shrink: 0;
  margin-top: 2px;
}

/* ── PROFILE SELECTOR ───────────────────────────────── */
.lp-profiles {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  max-width: 760px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.profile-card {
  background: var(--bg-card);
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 36px 24px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.25s, background 0.25s, transform 0.2s, box-shadow 0.25s;
  user-select: none;
}

.profile-card:hover {
  border-color: var(--gold-dark);
  background: var(--bg-card-2);
  transform: translateY(-3px);
}

.profile-card.active {
  border-color: var(--gold);
  background: var(--gold-glow);
  box-shadow: 0 0 24px rgba(234,179,8,0.2);
}

.profile-card-icon {
  font-size: 2.4rem;
  margin-bottom: 14px;
  display: block;
}

.profile-card-name {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.profile-card.active .profile-card-name {
  color: var(--gold);
}

.profile-card-sub {
  font-size: 0.85rem;
  color: var(--text-muted);
}

/* ── DYNAMIC BLOCK ──────────────────────────────────── */
#dynamic-block {
  max-width: 760px;
  margin: 0 auto;
  background: var(--bg-card);
  border: 1px solid var(--gold);
  border-radius: var(--radius-lg);
  padding: 48px 40px;
  position: relative;
  z-index: 1;
}

#dynamic-block.hidden {
  display: none;
}

#dynamic-block.visible {
  display: block;
  animation: fadeSlideIn 0.4s ease forwards;
}

@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.dynamic-title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);
  font-weight: 700;
  color: var(--text);
  margin-bottom: 28px;
}

.dynamic-examples {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 28px;
}

.dynamic-examples li {
  font-size: 1.05rem;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 12px;
}

.dynamic-benefit {
  display: inline-block;
  background: var(--gold);
  color: #000;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 10px 22px;
  border-radius: 30px;
  text-transform: uppercase;
}

/* ── FORM ────────────────────────────────────────────── */
.lp-form-wrap {
  max-width: 600px;
  margin: 0 auto;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 48px 40px;
  position: relative;
  z-index: 1;
}

.lp-form-title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(1.2rem, 3vw, 1.7rem);
  font-weight: 700;
  color: var(--text);
  margin-bottom: 8px;
}

.lp-form-subtitle {
  color: var(--text-muted);
  font-size: 0.95rem;
  margin-bottom: 32px;
}

.lp-form-group {
  margin-bottom: 20px;
}

.lp-form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-light);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.lp-form-group input,
.lp-form-group textarea {
  width: 100%;
  background: var(--bg-card-2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-family: 'Rajdhani', sans-serif;
  font-size: 1rem;
  padding: 12px 16px;
  transition: border-color 0.2s;
  outline: none;
}

.lp-form-group input:focus,
.lp-form-group textarea:focus {
  border-color: var(--gold);
}

.lp-form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.lp-form-submit {
  width: 100%;
  background: var(--gold);
  color: #000;
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 16px 32px;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: box-shadow 0.3s, transform 0.2s, opacity 0.2s;
  margin-top: 8px;
}

.lp-form-submit:hover:not(:disabled) {
  box-shadow: var(--shadow-gold);
  transform: translateY(-2px);
}

.lp-form-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ── SUCCESS ─────────────────────────────────────────── */
#form-success {
  text-align: center;
  padding: 40px 20px;
}

#form-success.hidden { display: none; }

.success-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.success-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.3rem;
  color: var(--green);
  margin-bottom: 12px;
}

.success-text {
  color: var(--text-muted);
  font-size: 0.95rem;
}

/* ── FOOTER ──────────────────────────────────────────── */
.lp-footer {
  border-top: 1px solid var(--border);
  padding: 40px 20px;
  text-align: center;
  position: relative;
  z-index: 1;
}

.lp-footer-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.lp-footer-links a {
  color: var(--text-muted);
  font-size: 0.85rem;
  text-decoration: none;
  transition: color 0.2s;
}

.lp-footer-links a:hover { color: var(--gold); }

.lp-footer-copy {
  color: var(--text-muted);
  font-size: 0.8rem;
}

/* ── RESPONSIVE ──────────────────────────────────────── */
@media (max-width: 640px) {
  .lp-profiles {
    grid-template-columns: 1fr;
  }

  .lp-pain,
  #dynamic-block,
  .lp-form-wrap {
    padding: 36px 24px;
  }
}
```

- [ ] **Step 2 : Vérifier que le fichier existe**

```bash
ls -la /work/automationboost/assets/css/landing.css
```

Attendu : fichier visible avec taille > 0

---

## Task 2 : Créer landing.html

**Files:**
- Create: `/work/automationboost/landing.html`

- [ ] **Step 1 : Créer le fichier HTML complet**

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AutomatisationBoost — Automatise ta vie. Récupère ton énergie.</title>
  <meta name="description" content="Stop aux tâches répétitives. Automatisation IA sur-mesure livrée en 48h pour PME, freelances et auto-entrepreneurs. Récupère 10 à 15h par semaine." />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23eab308'/><text x='50%25' y='54%25' dominant-baseline='middle' text-anchor='middle' font-size='18' font-family='Arial' fill='%23000'>⚡</text></svg>" />
  <link rel="stylesheet" href="assets/css/style.css" />
  <link rel="stylesheet" href="assets/css/landing.css" />
</head>
<body>

<!-- ══ NAVBAR ════════════════════════════════════════ -->
<nav id="navbar">
  <div class="nav-inner">
    <a href="index.html" class="logo">
      <div class="logo-icon">⚡</div>
      <span class="logo-text">Automation<span>Boost</span></span>
    </a>
    <a href="#formulaire" class="nav-cta">Démarrer →</a>
  </div>
</nav>

<!-- ══ HERO ══════════════════════════════════════════ -->
<section class="lp-hero">
  <div class="lp-hero-inner">
    <div class="lp-hero-badge">Automatisation IA · Livraison 48h ⚡</div>
    <h1 class="lp-hero-title">
      Automatise ta vie.<br>
      <span class="accent">Récupère ton énergie.</span>
    </h1>
    <p class="lp-hero-subtitle">
      Stop aux tâches répétitives. Je te livre une automatisation IA sur-mesure en 48h —
      pour que tu te concentres sur ce qui compte vraiment.
    </p>
    <a href="#profil" class="lp-hero-cta">Choisir mon profil →</a>
  </div>
</section>

<!-- ══ PAIN POINTS ════════════════════════════════════ -->
<div style="padding: 0 20px 80px; position: relative; z-index: 1;">
  <div style="text-align:center;margin-bottom:40px;">
    <p style="font-family:'Orbitron',sans-serif;font-size:0.75rem;letter-spacing:3px;color:var(--text-muted);text-transform:uppercase;">
      Tu te reconnais dans l'une de ces situations ?
    </p>
  </div>
  <div class="lp-pain">
    <ul class="lp-pain-list">
      <li>Tu passes des heures sur des tâches qui pourraient tourner seules</li>
      <li>Tu sais que l'automatisation existe — mais tu n'as jamais eu le temps de t'y mettre</li>
      <li>Ton business avance, mais trop lentement par rapport à l'énergie que tu y mets</li>
    </ul>
  </div>
</div>

<!-- ══ SÉLECTEUR DE PROFIL ════════════════════════════ -->
<section id="profil" style="padding: 0 20px 60px; position: relative; z-index: 1;">
  <p class="lp-section-title" style="margin-bottom:16px;">Quel est ton profil ?</p>
  <p style="text-align:center;color:var(--text-muted);font-size:0.95rem;margin-bottom:40px;">
    Clique sur ta situation pour voir ce que l'automatisation change concrètement pour toi.
  </p>
  <div class="lp-profiles">

    <div class="profile-card" data-profile="pme" role="button" tabindex="0" aria-pressed="false">
      <span class="profile-card-icon">🏢</span>
      <div class="profile-card-name">PME</div>
      <div class="profile-card-sub">J'ai une équipe</div>
    </div>

    <div class="profile-card" data-profile="freelance" role="button" tabindex="0" aria-pressed="false">
      <span class="profile-card-icon">💻</span>
      <div class="profile-card-name">Freelance</div>
      <div class="profile-card-sub">Je travaille seul</div>
    </div>

    <div class="profile-card" data-profile="autoentrepreneur" role="button" tabindex="0" aria-pressed="false">
      <span class="profile-card-icon">⚡</span>
      <div class="profile-card-name">Auto-entrepreneur</div>
      <div class="profile-card-sub">Je lance mon activité</div>
    </div>

  </div>
</section>

<!-- ══ BLOC DYNAMIQUE ════════════════════════════════ -->
<section style="padding: 0 20px 80px;">
  <div id="dynamic-block" class="hidden">
    <h2 class="dynamic-title" id="dynamic-title"></h2>
    <ul class="dynamic-examples" id="dynamic-examples"></ul>
    <span class="dynamic-benefit" id="dynamic-benefit"></span>
  </div>
</section>

<!-- ══ FORMULAIRE ════════════════════════════════════ -->
<section id="formulaire" style="padding: 0 20px 100px;">
  <p class="lp-section-title">Démarrer mon diagnostic</p>
  <div class="lp-form-wrap">

    <div id="form-success" class="hidden">
      <div class="success-icon">✅</div>
      <p class="success-title">Message reçu !</p>
      <p class="success-text">Je reviens vers toi dans les 24h avec un plan d'action personnalisé.</p>
    </div>

    <form id="lead-form" novalidate>
      <p class="lp-form-title">Prêt à récupérer ton temps ?</p>
      <p class="lp-form-subtitle">Dis-moi où tu en es — je te réponds sous 24h avec un plan concret.</p>

      <div class="lp-form-group">
        <label for="prenom">Prénom</label>
        <input type="text" id="prenom" name="prenom" placeholder="Ton prénom" required autocomplete="given-name" />
      </div>

      <div class="lp-form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" placeholder="ton@email.com" required autocomplete="email" />
      </div>

      <div class="lp-form-group">
        <label for="message">Ta situation <span style="color:var(--text-muted);font-weight:400;">(optionnel)</span></label>
        <textarea id="message" name="message" placeholder="Décris ta situation en quelques mots… Qu'est-ce qui te prend le plus de temps ?"></textarea>
      </div>

      <!-- Champs cachés -->
      <input type="hidden" name="profil" value="" />
      <input type="hidden" name="utm_source" value="" />
      <input type="hidden" name="utm_campaign" value="" />
      <input type="hidden" name="utm_medium" value="" />

      <button type="submit" class="lp-form-submit">
        Démarrer mon diagnostic gratuit →
      </button>
    </form>
  </div>
</section>

<!-- ══ FOOTER ════════════════════════════════════════ -->
<footer class="lp-footer">
  <nav class="lp-footer-links" aria-label="Liens légaux">
    <a href="index.html">Accueil</a>
    <a href="#">Mentions légales</a>
    <a href="#">Politique de confidentialité</a>
    <a href="#">CGV</a>
  </nav>
  <p class="lp-footer-copy">© 2026 AutomatisationBoost — Tony Payet · tony.payet.professionnel@gmail.com</p>
</footer>

<!-- ══ JAVASCRIPT ═════════════════════════════════════ -->
<script>
// ── CONFIG ──────────────────────────────────────────────
const N8N_WEBHOOK_URL = 'https://VOTRE_N8N_URL/webhook/landing-profil';

// ── DONNÉES PAR PROFIL ──────────────────────────────────
const PROFILE_DATA = {
  pme: {
    title: 'Automatise ce qui freine ta croissance',
    examples: [
      'Devis générés automatiquement',
      'Relances clients sans effort',
      'Rapports hebdo auto-envoyés'
    ],
    benefit: 'Économise 15h/semaine sur l\'admin'
  },
  freelance: {
    title: 'Concentre-toi sur tes missions, pas l\'admin',
    examples: [
      'Onboarding client automatique',
      'Facturation sans y penser',
      'Contenu publié pendant que tu dors'
    ],
    benefit: 'Récupère 10h/semaine pour des missions qui paient'
  },
  autoentrepreneur: {
    title: 'Lance-toi sans te noyer dans les outils',
    examples: [
      'Réponses aux prospects 24/7',
      'Gestion des commandes en pilote auto',
      'CRM qui se remplit tout seul'
    ],
    benefit: 'Gère tout seul sans y passer tes nuits'
  }
};

// ── SÉLECTEUR DE PROFIL ─────────────────────────────────
const cards = document.querySelectorAll('.profile-card');
const dynamicBlock = document.getElementById('dynamic-block');

cards.forEach(card => {
  card.addEventListener('click', () => activateProfile(card.dataset.profile));
  card.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      activateProfile(card.dataset.profile);
    }
  });
});

function activateProfile(profile) {
  // Mettre à jour les cartes
  cards.forEach(c => {
    c.classList.remove('active');
    c.setAttribute('aria-pressed', 'false');
  });
  const active = document.querySelector(`[data-profile="${profile}"]`);
  active.classList.add('active');
  active.setAttribute('aria-pressed', 'true');

  // Mettre à jour le champ caché
  document.querySelector('[name="profil"]').value = profile;

  // Rendre le bloc dynamique
  renderDynamicBlock(profile);
}

function renderDynamicBlock(profile) {
  const data = PROFILE_DATA[profile];

  document.getElementById('dynamic-title').textContent = data.title;

  document.getElementById('dynamic-examples').innerHTML =
    data.examples.map(ex => `<li>⚡ ${ex}</li>`).join('');

  document.getElementById('dynamic-benefit').textContent = data.benefit;

  dynamicBlock.classList.remove('hidden', 'visible');
  // Force reflow pour que l'animation se rejoue
  void dynamicBlock.offsetWidth;
  dynamicBlock.classList.add('visible');

  // Scroll vers le bloc
  setTimeout(() => {
    dynamicBlock.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, 100);
}

// ── CAPTURE UTM ─────────────────────────────────────────
const params = new URLSearchParams(window.location.search);
['utm_source', 'utm_campaign', 'utm_medium'].forEach(key => {
  const field = document.querySelector(`[name="${key}"]`);
  if (field) field.value = params.get(key) || '';
});

// ── SOUMISSION FORMULAIRE ───────────────────────────────
document.getElementById('lead-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  const btn = this.querySelector('button[type="submit"]');
  const originalText = btn.textContent;
  btn.disabled = true;
  btn.textContent = 'Envoi en cours…';

  const payload = Object.fromEntries(new FormData(this));

  try {
    await fetch(N8N_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    this.style.display = 'none';
    document.getElementById('form-success').classList.remove('hidden');
  } catch (err) {
    btn.disabled = false;
    btn.textContent = originalText;
    alert('Une erreur est survenue. Réessaie dans quelques instants ou contacte-moi directement.');
  }
});

// ── NAVBAR SCROLL ────────────────────────────────────────
window.addEventListener('scroll', () => {
  document.getElementById('navbar').style.background =
    window.scrollY > 50
      ? 'rgba(5,5,5,0.97)'
      : 'transparent';
});
</script>

</body>
</html>
```

- [ ] **Step 2 : Vérifier que le fichier existe**

```bash
ls -la /work/automationboost/landing.html
```

Attendu : fichier visible avec taille > 0

---

## Task 3 : Tester avec Playwright

**Files:**
- Test: `/tmp/playwright-test-landing.js`

- [ ] **Step 1 : Écrire et lancer le test Playwright**

```bash
# Script de test
cat > /tmp/playwright-test-landing.js << 'EOF'
const { chromium } = require('playwright');
const path = require('path');

const FILE_URL = 'file:///work/automationboost/landing.html';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto(FILE_URL, { waitUntil: 'domcontentloaded' });

  // Test 1 : titre correct
  const title = await page.title();
  console.assert(title.includes('Automatise ta vie'), `❌ Titre incorrect: ${title}`);
  console.log('✅ Titre OK:', title);

  // Test 2 : cartes profil présentes
  const cards = await page.locator('.profile-card').count();
  console.assert(cards === 3, `❌ Attendu 3 cartes, trouvé ${cards}`);
  console.log('✅ 3 cartes profil présentes');

  // Test 3 : bloc dynamique caché par défaut
  const blockHidden = await page.locator('#dynamic-block.hidden').count();
  console.assert(blockHidden === 1, '❌ Le bloc dynamique devrait être caché par défaut');
  console.log('✅ Bloc dynamique caché par défaut');

  // Test 4 : clic sur "Freelance" affiche le bon contenu
  await page.locator('[data-profile="freelance"]').click();
  await page.waitForSelector('#dynamic-block.visible');
  const title2 = await page.locator('#dynamic-title').textContent();
  console.assert(title2.includes('missions'), `❌ Contenu freelance incorrect: ${title2}`);
  console.log('✅ Bloc dynamique freelance OK:', title2);

  // Test 5 : champ caché profil mis à jour
  const profilValue = await page.locator('[name="profil"]').inputValue();
  console.assert(profilValue === 'freelance', `❌ Champ profil = "${profilValue}" au lieu de "freelance"`);
  console.log('✅ Champ caché profil OK:', profilValue);

  // Screenshot
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.screenshot({ path: '/tmp/landing-desktop.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: '/tmp/landing-mobile.png', fullPage: true });
  console.log('📸 Screenshots sauvegardés: /tmp/landing-desktop.png, /tmp/landing-mobile.png');

  await browser.close();
  console.log('\n✅ Tous les tests passent');
})();
EOF

cd /work/.claude/skills/playwright-skill && node run.js /tmp/playwright-test-landing.js
```

Attendu : tous les `✅` s'affichent, aucun `❌`

- [ ] **Step 2 : Lire le screenshot desktop pour validation visuelle**

```bash
# Lire /tmp/landing-desktop.png avec le tool Read
```

---

## Rappel post-implémentation

Remplacer `https://VOTRE_N8N_URL/webhook/landing-profil` dans `landing.html` (ligne `const N8N_WEBHOOK_URL`) par l'URL réelle du webhook n8n avant mise en ligne.

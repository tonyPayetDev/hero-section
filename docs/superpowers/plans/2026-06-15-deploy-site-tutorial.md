# Page Tutoriel Deploy-Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a simple, responsive HTML page that teaches beginners how to use the deploy-site skill, from prerequisites through deployment to Coolify, hosted on automatisationboost.com.

**Architecture:** Single-page HTML file with embedded CSS, responsive design (mobile-first), structured sections with code snippets, images, and minimal styling. No frameworks — just clean, semantic HTML. Create assets directory for screenshots (placeholder images initially, replace with real captures later).

**Tech Stack:** HTML5, CSS3 (media queries for responsive), simple no-framework approach, static assets served from the same domain.

---

## File Structure

```
automatisationboost.com/
├── index.html                 (main page, ~500 lines)
├── style.css                  (responsive styling, ~300 lines)
├── assets/
│   ├── screenshots/
│   │   ├── claude-code.png
│   │   ├── github-new-repo.png
│   │   ├── github-push.png
│   │   ├── coolify-dashboard.png
│   │   ├── deploy-site-result.png
│   │   └── site-online.png
│   └── logo.svg               (simple logo for header)
└── README.md                  (notes for maintainers)
```

---

## Tasks

### Task 1: Create base HTML structure with Header & Intro

**Files:**
- Create: `index.html` (header, intro section only)
- Create: `style.css` (basic reset, mobile-first approach)

- [ ] **Step 1: Create index.html with semantic structure**

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tutoriel Deploy-Site | Automatisation Boost</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <h1 class="logo">⚡ Automatisation Boost</h1>
            <p class="tagline">Déploie ton site en 5 minutes</p>
        </div>
    </header>

    <!-- Intro / Hero -->
    <section class="hero">
        <div class="container">
            <h2>Bienvenue au tutoriel Deploy-Site</h2>
            <p class="lead">
                Dans ce guide, tu vas apprendre à déployer ton site statique en quelques clics seulement, 
                grâce au skill <strong>deploy-site</strong>.
            </p>
            <p class="subtitle">⏱️ Durée estimée : 5-10 minutes | 📚 Niveau : Débutant complet</p>
            <p class="description">
                Pas besoin de connaître Docker, Linux ou les serveurs. On te guide étape par étape.
            </p>
        </div>
    </section>

    <!-- Main Content -->
    <main>
        <!-- Section 1: Prérequis -->
        <section id="prerequis" class="section section-prerequis">
            <div class="container">
                <h2>📋 Étape 1 : Les Prérequis</h2>
                <p class="intro-text">Avant de commencer, assure-toi que tu as ces 4 choses :</p>
                
                <div class="checklist">
                    <!-- Item 1: Claude Code -->
                    <div class="checklist-item">
                        <h3>✅ Claude Code sur ton VPS</h3>
                        <p>C'est l'outil qui va automatiser le déploiement pour toi.</p>
                        <a href="https://claude.ai/code" target="_blank" class="btn-link">Installer Claude Code →</a>
                        <div class="screenshot-placeholder">
                            <img src="assets/screenshots/claude-code.png" alt="Claude Code en action">
                        </div>
                    </div>

                    <!-- Item 2: GitHub -->
                    <div class="checklist-item">
                        <h3>✅ Un compte GitHub</h3>
                        <p>C'est l'endroit où on va ranger ton code.</p>
                        <a href="https://github.com/signup" target="_blank" class="btn-link">Créer un compte GitHub →</a>
                        <div class="screenshot-placeholder">
                            <img src="assets/screenshots/github-new-repo.png" alt="Créer un repo GitHub">
                        </div>
                    </div>

                    <!-- Item 3: Coolify -->
                    <div class="checklist-item">
                        <h3>✅ Un compte Coolify</h3>
                        <p>C'est le service qui va héberger ton site.</p>
                        <a href="https://coolify.io" target="_blank" class="btn-link">Créer un compte Coolify →</a>
                        <div class="screenshot-placeholder">
                            <img src="assets/screenshots/coolify-dashboard.png" alt="Tableau de bord Coolify">
                        </div>
                    </div>

                    <!-- Item 4: Un site local -->
                    <div class="checklist-item">
                        <h3>✅ Un site local prêt</h3>
                        <p>Des fichiers HTML/CSS/JS sur ton ordinateur. Rien de complexe, juste un site basique.</p>
                        <p class="example">Exemple de structure :</p>
                        <pre><code>mon-site/
├── index.html
├── style.css
├── script.js
└── images/
    └── logo.png</code></pre>
                    </div>
                </div>
            </div>
        </section>

        <!-- Placeholder for other sections (will be added in next tasks) -->
        <section id="preparer" class="section section-preparer">
            <div class="container">
                <h2>📁 Étape 2 : Préparer ton site</h2>
                <p>À remplir...</p>
            </div>
        </section>

        <section id="deployer" class="section section-deployer">
            <div class="container">
                <h2>🚀 Étape 3 : Utiliser Deploy-Site</h2>
                <p>À remplir...</p>
            </div>
        </section>

        <section id="termux" class="section section-termux">
            <div class="container">
                <h2>🤖 Bonus : Termux (Pour les avancés)</h2>
                <p>À remplir...</p>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Automatisation Boost - Tutoriels libres et gratuits</p>
            <nav class="footer-links">
                <a href="https://docs.claude.ai" target="_blank">Docs Claude Code</a>
                <a href="https://github.com" target="_blank">GitHub</a>
                <a href="https://coolify.io" target="_blank">Coolify</a>
            </nav>
        </div>
    </footer>
</body>
</html>
```

- [ ] **Step 2: Create style.css with responsive foundation**

```css
/* Reset & Base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #fafafa;
}

/* Container */
.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px 0;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.header .logo {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
}

.header .tagline {
    font-size: 18px;
    opacity: 0.95;
    font-weight: 300;
}

/* Hero Section */
.hero {
    background: white;
    padding: 60px 20px;
    text-align: center;
    border-bottom: 1px solid #eee;
}

.hero h2 {
    font-size: 32px;
    margin-bottom: 20px;
    color: #222;
}

.hero .lead {
    font-size: 18px;
    color: #555;
    margin-bottom: 15px;
    line-height: 1.8;
}

.hero .subtitle {
    font-size: 14px;
    color: #888;
    margin-bottom: 10px;
}

.hero .description {
    font-size: 16px;
    color: #666;
    max-width: 600px;
    margin: 20px auto 0;
}

/* Sections */
.section {
    padding: 60px 20px;
    background: white;
    border-bottom: 1px solid #eee;
}

.section h2 {
    font-size: 28px;
    margin-bottom: 20px;
    color: #222;
}

.section .intro-text {
    font-size: 16px;
    color: #555;
    margin-bottom: 30px;
}

/* Checklist */
.checklist {
    display: grid;
    gap: 30px;
}

.checklist-item {
    background: #f9f9f9;
    border: 2px solid #eee;
    border-radius: 8px;
    padding: 30px;
    transition: all 0.3s ease;
}

.checklist-item:hover {
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.checklist-item h3 {
    font-size: 18px;
    color: #222;
    margin-bottom: 10px;
}

.checklist-item p {
    color: #666;
    margin-bottom: 15px;
}

.checklist-item .btn-link {
    display: inline-block;
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
    margin-bottom: 20px;
    transition: color 0.2s;
}

.checklist-item .btn-link:hover {
    color: #764ba2;
    text-decoration: underline;
}

.checklist-item .example {
    font-size: 14px;
    color: #888;
    margin-top: 15px;
}

/* Code snippets */
pre {
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 15px;
    border-radius: 6px;
    overflow-x: auto;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.5;
    margin: 15px 0;
}

code {
    font-family: 'Courier New', monospace;
}

/* Screenshot placeholder */
.screenshot-placeholder {
    margin: 20px 0;
    background: #f5f5f5;
    border: 2px dashed #ccc;
    border-radius: 6px;
    padding: 20px;
    text-align: center;
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.screenshot-placeholder img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}

/* Footer */
.footer {
    background: #222;
    color: #fff;
    padding: 40px 20px;
    text-align: center;
    border-top: 1px solid #444;
}

.footer p {
    margin-bottom: 15px;
    font-size: 14px;
}

.footer-links {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
}

.footer-links a {
    color: #aaa;
    text-decoration: none;
    transition: color 0.2s;
}

.footer-links a:hover {
    color: #fff;
}

/* Responsive Design - Mobile First */
@media (max-width: 768px) {
    .header .logo {
        font-size: 24px;
    }

    .header .tagline {
        font-size: 16px;
    }

    .hero h2 {
        font-size: 24px;
    }

    .hero .lead {
        font-size: 16px;
    }

    .section h2 {
        font-size: 22px;
    }

    .checklist-item {
        padding: 20px;
    }

    .footer-links {
        gap: 10px;
    }
}

@media (max-width: 480px) {
    .container {
        padding: 0 15px;
    }

    .header {
        padding: 30px 0;
    }

    .hero {
        padding: 40px 15px;
    }

    .section {
        padding: 40px 15px;
    }

    .header .logo {
        font-size: 20px;
    }

    .hero h2 {
        font-size: 20px;
    }

    .section h2 {
        font-size: 18px;
    }
}
```

- [ ] **Step 3: Create assets directory structure**

```bash
mkdir -p assets/screenshots
touch assets/logo.svg
```

- [ ] **Step 4: Test basic HTML renders**

Open `index.html` in a browser (double-click or `open index.html` on Mac)
Expected: See header, hero section, prérequis section with basic styling

- [ ] **Step 5: Commit**

```bash
git add index.html style.css assets/
git commit -m "feat: create base HTML structure and responsive CSS for tutorial page

- Add semantic HTML structure with header, hero, sections, footer
- Implement mobile-first responsive design with CSS media queries
- Create assets directory for screenshots and logo
- Add basic styling with gradient header and clean layout

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 2: Fill Section 2 - Préparer ton site (HTML & content)

**Files:**
- Modify: `index.html` (replace placeholder Étape 2)

- [ ] **Step 1: Replace "Étape 2" placeholder with full content**

Find this section in `index.html`:
```html
        <section id="preparer" class="section section-preparer">
            <div class="container">
                <h2>📁 Étape 2 : Préparer ton site</h2>
                <p>À remplir...</p>
            </div>
        </section>
```

Replace with:
```html
        <section id="preparer" class="section section-preparer">
            <div class="container">
                <h2>📁 Étape 2 : Préparer ton site</h2>
                <p class="intro-text">Avant de déployer, assure-toi que tes fichiers sont bien organisés.</p>

                <div class="steps">
                    <!-- Step 1 -->
                    <div class="step">
                        <div class="step-number">1</div>
                        <div class="step-content">
                            <h3>Organise tes fichiers</h3>
                            <p>Crée un dossier pour ton site avec la structure suivante :</p>
                            <pre><code>mon-site/
├── index.html
├── style.css
├── script.js
└── images/
    └── logo.png</code></pre>
                            <p class="tip">💡 <strong>Conseil :</strong> Tous les fichiers doivent être dans le même dossier ou dans des sous-dossiers bien organisés.</p>
                        </div>
                    </div>

                    <!-- Step 2 -->
                    <div class="step">
                        <div class="step-number">2</div>
                        <div class="step-content">
                            <h3>Crée le dossier projet</h3>
                            <p>Ouvre ton terminal et tape :</p>
                            <pre><code>mkdir mon-site
cd mon-site</code></pre>
                            <div class="screenshot-placeholder">
                                <img src="assets/screenshots/terminal-mkdir.png" alt="Terminal - création dossier">
                            </div>
                        </div>
                    </div>

                    <!-- Step 3 -->
                    <div class="step">
                        <div class="step-number">3</div>
                        <div class="step-content">
                            <h3>Teste en local</h3>
                            <p>Avant de déployer, vérifie que ton site marche sur ton ordi :</p>
                            <pre><code>python -m http.server</code></pre>
                            <p>Ou si tu as Node.js :</p>
                            <pre><code>npx serve</code></pre>
                            <p>Ensuite, ouvre <code>http://localhost:8000</code> dans ton navigateur.</p>
                            <div class="screenshot-placeholder">
                                <img src="assets/screenshots/local-test.png" alt="Site ouvert localement">
                            </div>
                            <p class="tip">💡 <strong>Conseil :</strong> Si ton site marche ici, il marchera aussi une fois déployé !</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
```

- [ ] **Step 2: Add CSS for steps styling**

Add to `style.css` (after `.checklist-item` styles):

```css
/* Steps */
.steps {
    display: grid;
    gap: 40px;
}

.step {
    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid #eee;
}

.step:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.step-number {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: bold;
    flex-shrink: 0;
}

.step-content h3 {
    font-size: 20px;
    color: #222;
    margin-bottom: 12px;
}

.step-content p {
    color: #555;
    margin-bottom: 12px;
}

.step-content pre {
    margin: 15px 0;
}

.tip {
    background: #e3f2fd;
    border-left: 4px solid #2196f3;
    padding: 12px 15px;
    border-radius: 4px;
    font-size: 14px;
    margin-top: 15px;
}

.tip strong {
    color: #1976d2;
}

/* Responsive steps */
@media (max-width: 768px) {
    .step {
        grid-template-columns: 1fr;
        gap: 15px;
    }

    .step-number {
        width: 60px;
        height: 60px;
        font-size: 24px;
    }

    .step-content h3 {
        font-size: 18px;
    }
}
```

- [ ] **Step 3: Preview in browser**

Refresh the browser. Expected: See "Étape 2" with 3 numbered steps, code snippets, and tips.

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: add Étape 2 - Préparer ton site section

- Add 3 numbered steps with clear instructions
- Include code snippets for directory setup and local testing
- Add screenshot placeholders for visual reference
- Style step numbers with gradient circles
- Add mobile-responsive grid layout

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 3: Fill Section 3 - Utiliser Deploy-Site (HTML & content)

**Files:**
- Modify: `index.html` (replace placeholder Étape 3)

- [ ] **Step 1: Replace "Étape 3" placeholder with full content**

Find this section in `index.html`:
```html
        <section id="deployer" class="section section-deployer">
            <div class="container">
                <h2>🚀 Étape 3 : Utiliser Deploy-Site</h2>
                <p>À remplir...</p>
            </div>
        </section>
```

Replace with:
```html
        <section id="deployer" class="section section-deployer">
            <div class="container">
                <h2>🚀 Étape 3 : Utiliser Deploy-Site</h2>
                <p class="intro-text">C'est maintenant qu'on déploie ! Suis ces 4 étapes simples.</p>

                <div class="steps">
                    <!-- Step 1 -->
                    <div class="step">
                        <div class="step-number">1</div>
                        <div class="step-content">
                            <h3>Crée un repo GitHub</h3>
                            <p>1. Va sur <a href="https://github.com/new" target="_blank">github.com/new</a></p>
                            <p>2. Nomme-le <code>mon-site</code></p>
                            <p>3. Clique <strong>"Create repository"</strong></p>
                            <div class="screenshot-placeholder">
                                <img src="assets/screenshots/github-create-repo.png" alt="Créer repo GitHub">
                            </div>
                        </div>
                    </div>

                    <!-- Step 2 -->
                    <div class="step">
                        <div class="step-number">2</div>
                        <div class="step-content">
                            <h3>Pousse ton code sur GitHub</h3>
                            <p>Dans ton terminal, depuis le dossier <code>mon-site/</code>, tape :</p>
                            <pre><code>git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TONUSERNAME/mon-site.git
git branch -M main
git push -u origin main</code></pre>
                            <p class="tip">💡 <strong>Conseil :</strong> Remplace <code>TONUSERNAME</code> par ton nom d'utilisateur GitHub.</p>
                            <div class="screenshot-placeholder">
                                <img src="assets/screenshots/git-push-success.png" alt="Push réussi">
                            </div>
                        </div>
                    </div>

                    <!-- Step 3 -->
                    <div class="step">
                        <div class="step-number">3</div>
                        <div class="step-content">
                            <h3>Lance le skill deploy-site</h3>
                            <p>Maintenant, tu vas utiliser Claude Code pour déployer automatiquement.</p>
                            <p>Dans ton terminal (depuis n'importe quel dossier), tape :</p>
                            <pre><code>deploy-site mon-site/</code></pre>
                            <p><strong>Ou</strong>, si tu utilises Claude Code directement :</p>
                            <pre><code>/deploy-site</code></pre>
                            <p>Le skill va :</p>
                            <ul class="deploy-steps">
                                <li>✅ Vérifier que c'est bon sur GitHub</li>
                                <li>✅ Créer une app sur Coolify</li>
                                <li>✅ Attendre que ça soit en ligne</li>
                                <li>✅ Te donner l'URL de ton site</li>
                            </ul>
                            <div class="screenshot-placeholder">
                                <img src="assets/screenshots/deploy-in-progress.png" alt="Déploiement en cours">
                            </div>
                        </div>
                    </div>

                    <!-- Step 4 -->
                    <div class="step">
                        <div class="step-number">4</div>
                        <div class="step-content">
                            <h3>Ton site est en ligne ! 🎉</h3>
                            <p>Le skill va afficher quelque chose comme :</p>
                            <pre><code>SITE_EN_LIGNE: https://mon-site-abc123.coolify.app</code></pre>
                            <p>Clique sur l'URL ou copie-la dans ton navigateur.</p>
                            <div class="screenshot-placeholder">
                                <img src="assets/screenshots/site-live.png" alt="Site en ligne">
                            </div>
                            <p class="success-message">🎊 Bravo ! Ton site est maintenant accessible sur Internet. Tu peux partager l'URL avec qui tu veux !</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
```

- [ ] **Step 2: Add CSS for new elements (ul.deploy-steps, success-message)**

Add to `style.css` (at the end):

```css
/* Deploy steps list */
.deploy-steps {
    list-style: none;
    margin: 15px 0;
    padding-left: 0;
}

.deploy-steps li {
    padding: 8px 0;
    color: #555;
}

/* Success message */
.success-message {
    background: #f0f9ff;
    border-left: 4px solid #10b981;
    padding: 15px;
    border-radius: 4px;
    font-size: 15px;
    color: #047857;
    margin-top: 20px;
    font-weight: 500;
}

/* Link styling in content */
.step-content a {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.step-content a:hover {
    text-decoration: underline;
}

.step-content code {
    background: #f5f5f5;
    padding: 2px 6px;
    border-radius: 3px;
    color: #d63384;
}
```

- [ ] **Step 3: Preview in browser**

Refresh. Expected: See "Étape 3" with 4 numbered steps, GitHub instructions, deploy command, and success message.

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: add Étape 3 - Utiliser Deploy-Site section

- Add 4 numbered steps: Create repo → Push to GitHub → Run deploy-site → Site online
- Include exact Git commands to push code
- Add deploy-site command variations (CLI and Claude Code)
- Add visual checklist of what the skill does
- Include success message and next steps

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 4: Fill Section 4 - Bonus Termux (HTML & content)

**Files:**
- Modify: `index.html` (replace placeholder Étape Bonus)

- [ ] **Step 1: Replace "Bonus Termux" placeholder with full content**

Find this section in `index.html`:
```html
        <section id="termux" class="section section-termux">
            <div class="container">
                <h2>🤖 Bonus : Termux (Pour les avancés)</h2>
                <p>À remplir...</p>
            </div>
        </section>
```

Replace with:
```html
        <section id="termux" class="section section-termux bonus-section">
            <div class="container">
                <h2>🤖 Bonus : Termux (Pour les avancés)</h2>
                <p class="intro-text">Tu peux aussi déployer ton site directement depuis ton téléphone Android !</p>

                <div class="bonus-card">
                    <h3>Qu'est-ce que Termux ?</h3>
                    <p>
                        <strong>Termux</strong> est un émulateur de terminal pour Android. 
                        Il te permet de faire du développement et des déploiements directement sur ton téléphone, 
                        sans avoir besoin d'un ordi. C'est parfait si tu es toujours en déplacement !
                    </p>

                    <h3 style="margin-top: 25px;">Comment installer Termux ?</h3>
                    <ol class="bonus-steps">
                        <li>Va sur le <a href="https://play.google.com/store/apps/details?id=com.termux" target="_blank">Google Play Store</a></li>
                        <li>Cherche "Termux"</li>
                        <li>Installe l'app</li>
                    </ol>

                    <h3 style="margin-top: 25px;">Déployer depuis Termux</h3>
                    <p>Une fois Termux installé, tu peux :</p>
                    <ol class="bonus-steps">
                        <li>Cloner ton repo : <code class="inline-code">git clone https://github.com/TONUSERNAME/mon-site.git</code></li>
                        <li>Entrer dans le dossier : <code class="inline-code">cd mon-site</code></li>
                        <li>Lancer le déploiement : <code class="inline-code">deploy-site</code></li>
                    </ol>

                    <p class="tip" style="margin-top: 20px;">
                        💡 <strong>Conseil :</strong> C'est plus avancé que l'approche ordinateur. 
                        Assure-toi que tu comprends bien les étapes du tutoriel avant de l'essayer sur mobile.
                    </p>
                </div>

                <div class="next-steps">
                    <h3>Et ensuite ?</h3>
                    <ul>
                        <li>📚 <a href="https://docs.claude.ai" target="_blank">Explore la doc complète de Claude Code</a></li>
                        <li>🔗 <a href="https://github.com" target="_blank">Maîtrise GitHub pour gérer tes projets</a></li>
                        <li>🚀 <a href="https://coolify.io" target="_blank">Apprends Coolify pour plus de contrôle</a></li>
                    </ul>
                </div>
            </div>
        </section>
```

- [ ] **Step 2: Add CSS for bonus section styling**

Add to `style.css` (at the end):

```css
/* Bonus section */
.bonus-section {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.bonus-card {
    background: white;
    border: 2px solid #667eea;
    border-radius: 8px;
    padding: 30px;
    margin: 30px 0;
}

.bonus-card h3 {
    color: #222;
    font-size: 18px;
    margin-bottom: 12px;
}

.bonus-card p {
    color: #555;
    margin-bottom: 15px;
}

.bonus-steps {
    list-style: decimal;
    margin-left: 25px;
    color: #555;
}

.bonus-steps li {
    margin-bottom: 10px;
    line-height: 1.6;
}

.inline-code {
    background: #f5f5f5;
    padding: 2px 6px;
    border-radius: 3px;
    color: #d63384;
    font-family: 'Courier New', monospace;
}

.next-steps {
    background: #f9f9f9;
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 25px;
    margin-top: 30px;
}

.next-steps h3 {
    font-size: 18px;
    color: #222;
    margin-bottom: 15px;
}

.next-steps ul {
    list-style: none;
    padding-left: 0;
}

.next-steps li {
    padding: 10px 0;
    color: #555;
}

.next-steps a {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.next-steps a:hover {
    text-decoration: underline;
}

/* Responsive bonus */
@media (max-width: 768px) {
    .bonus-card {
        padding: 20px;
    }

    .next-steps {
        padding: 20px;
    }
}
```

- [ ] **Step 3: Preview in browser**

Refresh. Expected: See "Bonus Termux" section with info about Termux, installation steps, and next steps links.

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: add Bonus Termux section for advanced users

- Add explanation of Termux for Android
- Include installation steps from Google Play Store
- Add deployment instructions from mobile
- Include warning that this is advanced content
- Add 'next steps' section with links to docs

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 5: Create placeholder images and finalize assets

**Files:**
- Create: `assets/screenshots/*.png` (placeholder images)
- Create: `assets/logo.svg`

- [ ] **Step 1: Create simple SVG logo**

Create `assets/logo.svg`:

```xml
<svg width="200" height="50" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background circle -->
  <circle cx="25" cy="25" r="20" fill="url(#grad)"/>
  
  <!-- Lightning bolt symbol (⚡) -->
  <text x="25" y="32" font-size="28" fill="white" text-anchor="middle" font-weight="bold">⚡</text>
  
  <!-- Text -->
  <text x="50" y="22" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#222">
    Automatisation
  </text>
  <text x="50" y="38" font-family="Arial, sans-serif" font-size="14" fill="#666">
    Boost
  </text>
</svg>
```

- [ ] **Step 2: Create placeholder PNG images**

For now, create simple placeholder images using ImageMagick or online tool. 
If ImageMagick is available:

```bash
convert -size 800x500 xc:white \
  -pointsize 24 -draw "text 200,200 'Claude Code Screenshot'" \
  assets/screenshots/claude-code.png

convert -size 800x500 xc:white \
  -pointsize 24 -draw "text 200,200 'GitHub Repository'" \
  assets/screenshots/github-new-repo.png

convert -size 800x500 xc:white \
  -pointsize 24 -draw "text 200,200 'Coolify Dashboard'" \
  assets/screenshots/coolify-dashboard.png

convert -size 800x500 xc:white \
  -pointsize 24 -draw "text 200,200 'Git Push Success'" \
  assets/screenshots/git-push-success.png

convert -size 800x500 xc:white \
  -pointsize 24 -draw "text 200,200 'Deploy in Progress'" \
  assets/screenshots/deploy-in-progress.png

convert -size 800x500 xc:white \
  -pointsize 24 -draw "text 200,200 'Site Live'" \
  assets/screenshots/site-live.png
```

If ImageMagick is not available, create basic HTML or use placeholder images from placeholder.com.

Alternative (using simple HTML comment as placeholder):
Create each PNG as a 1x1 transparent pixel placeholder. Then in the HTML, add `alt` text that describes what should be there. Screenshot replacement can happen later.

- [ ] **Step 3: Update HTML to reference logo.svg**

In `index.html`, update the header logo line from:
```html
            <h1 class="logo">⚡ Automatisation Boost</h1>
```

To:
```html
            <img src="assets/logo.svg" alt="Automatisation Boost Logo" class="logo-img">
            <h1 class="logo">Automatisation Boost</h1>
```

And add CSS for `.logo-img`:

```css
.logo-img {
    height: 50px;
    margin-bottom: 10px;
}
```

- [ ] **Step 4: Verify all images load without errors**

Open the page in browser. All screenshot placeholders should show (either with proper placeholder images or with alt text visible).

Expected: No broken image icons, clean layout.

- [ ] **Step 5: Commit**

```bash
git add assets/
git commit -m "feat: add assets - logo and screenshot placeholders

- Create SVG logo with gradient and emoji
- Add placeholder images for all screenshots (to be replaced with real captures)
- Include descriptive alt text for accessibility

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 6: Test responsive design and accessibility

**Files:**
- No new files, but verify existing `index.html` and `style.css`

- [ ] **Step 1: Test on desktop (1200px+)**

Open page in browser with full width. Expected:
- Header centered and readable
- Sections properly spaced
- Code snippets not wrapping awkwardly
- Links and buttons easily clickable

- [ ] **Step 2: Test on tablet (768px)**

Resize browser to 768px width (or use DevTools device emulation). Expected:
- Sections still readable
- Font sizes adjusted via media query
- No horizontal scrolling

- [ ] **Step 3: Test on mobile (480px)**

Resize to 480px. Expected:
- Single column layout
- Touch-friendly spacing (buttons/links large enough)
- No overflow
- All sections visible without scrolling too much

- [ ] **Step 4: Test on actual phone (optional but recommended)**

Access via `http://localhost:8000` on your phone. Take screenshot of home screen and mid-page.

- [ ] **Step 5: Check accessibility**

- All images have `alt` text (inspect HTML)
- Color contrast passes WCAG AA (text color #333 on #fafafa ✅)
- Links are underlined or obvious (use keyboard Tab to test)
- Headings in proper order (h1, h2, h3)

Run quick accessibility check:
```bash
# If you have axe DevTools browser extension, run it.
# Otherwise, just manually verify:
# - Tab through the page, all interactive elements are reachable
# - No content hidden from screen readers
```

- [ ] **Step 6: Commit (if changes were needed)**

If no changes needed:
```bash
git status
```

Expected: Clean tree (no unstaged changes)

If changes were made:
```bash
git add index.html style.css
git commit -m "fix: responsive design and accessibility tweaks

- Adjust spacing on mobile for better touch targets
- Improve color contrast for accessibility
- Ensure headings follow proper hierarchy

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 7: Deploy to automatisationboost.com using deploy-site

**Files:**
- All files (ready to deploy)

- [ ] **Step 1: Verify all content is in place**

Check that index.html includes all 4 sections + footer:
```bash
grep -c "section id=" index.html
```

Expected: 4 (prerequis, preparer, deployer, termux)

- [ ] **Step 2: Test locally one more time**

```bash
python -m http.server 8000
```

Open http://localhost:8000, scroll through entire page.
Expected: No broken images, all text visible, no console errors.

- [ ] **Step 3: Create a repo on GitHub (if not already done)**

1. Go to github.com/new
2. Create repo: `automatisationboost-tutorial`
3. Clone it locally or init an existing folder

- [ ] **Step 4: Push code to GitHub**

```bash
git remote add origin https://github.com/YOURUSER/automatisationboost-tutorial.git
git branch -M main
git push -u origin main
```

- [ ] **Step 5: Deploy using deploy-site skill**

```bash
/deploy-site
```

Or:

```bash
deploy-site .
```

Expected output:
```
SITE_EN_LIGNE: https://automatisationboost.com (or assigned URL from Coolify)
```

- [ ] **Step 6: Verify deployment**

1. Visit the URL from the output
2. Test all sections load
3. Test responsive design (open DevTools, test mobile view)
4. Click all links to ensure they work

Expected: Full page renders, all links functional, looks good on mobile.

- [ ] **Step 7: Final commit**

```bash
git add .
git commit -m "chore: ready for deployment

- All content complete and tested
- Responsive design verified on mobile/tablet/desktop
- Accessibility checked
- Ready to deploy to automatisationboost.com

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Summary

This plan creates a complete, beginner-friendly tutorial page for the deploy-site skill:

1. **Task 1** - Base HTML structure and responsive CSS
2. **Task 2** - Section 2: Prepare Your Site (3 steps)
3. **Task 3** - Section 3: Deploy Site (4 steps with GitHub + deploy-site)
4. **Task 4** - Section 4: Bonus Termux (advanced users)
5. **Task 5** - Assets (logo, placeholder images)
6. **Task 6** - Responsive & accessibility testing
7. **Task 7** - Deploy to automatisationboost.com

**Estimated total time:** 2-3 hours for complete implementation.


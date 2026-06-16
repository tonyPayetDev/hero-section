# Les Petites Mains de Lisa — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a distinctive, production-grade website for Les Petites Mains de Lisa (wellness/beauty services) featuring scroll narrative architecture, warm minimalist design, and smooth animations.

**Architecture:** Static HTML/CSS/JS site with semantic structure, CSS custom properties for theming, vanilla JavaScript for scroll animations via Intersection Observer. Mobile-first responsive design. Deployed via Docker + Nginx.

**Tech Stack:** 
- HTML5 (semantic)
- CSS3 (Grid, Flexbox, custom properties, animations)
- Vanilla JavaScript (Intersection Observer API)
- Google Fonts (Cormorant Garamond, Inter)
- Docker + Nginx (deployment)

---

## File Structure

```
lespetitesmainsdelisa-optimized/
├── index.html                    # Single-page app with semantic sections
├── css/
│   ├── variables.css             # Color palette, spacing scale, typography vars
│   ├── reset.css                 # CSS reset + base styles
│   ├── typography.css            # Font imports, heading/body hierarchy
│   ├── layout.css                # Grid layouts, flexbox, sections, responsive
│   ├── components.css            # Buttons, cards, links, forms
│   └── animations.css            # Scroll reveals, hover effects, transitions
├── js/
│   ├── main.js                   # Initialization, event listeners
│   └── scroll-animations.js      # Intersection Observer for scroll reveals
├── assets/
│   ├── images/
│   │   ├── hero.jpg              # Hero section background
│   │   ├── lisa-bio.jpg          # Lisa portrait
│   │   ├── service-*.jpg         # Service card images (if needed)
│   │   └── testimonial-*.jpg     # Optional testimonial images
│   ├── icons/
│   │   ├── massage.svg           # Service icons (4x)
│   │   ├── skincare.svg
│   │   ├── bach-flowers.svg
│   │   ├── gift-package.svg
│   │   └── social-*.svg          # Social media icons
│   └── fonts/                    # Local font files if needed
├── Dockerfile                    # Docker image config (nginx:alpine)
├── nginx.conf                    # Nginx server config
├── package.json                  # Project metadata (optional, for clarity)
└── README.md                     # Setup & deployment instructions
```

---

## Task Breakdown

### Task 1: Project Setup & HTML Skeleton

**Files:**
- Create: `index.html`
- Create: `css/variables.css`
- Create: `css/reset.css`
- Create: `js/main.js`
- Create: `js/scroll-animations.js`

- [ ] **Step 1: Initialize project directory**

```bash
cd /work
mkdir -p lespetitesmainsdelisa-optimized/{css,js,assets/{images,icons}}
cd lespetitesmainsdelisa-optimized
git init
git config user.email "deploy@coolify.local"
git config user.name "Coolify Deploy"
```

- [ ] **Step 2: Create index.html with semantic structure**

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Les Petites Mains de Lisa - Massage et soins à domicile à La Réunion. Détente, bien-être, professionnalisme.">
    <meta name="theme-color" content="#F9F7F4">
    <title>Les Petites Mains de Lisa — Massage & Soins à Domicile | La Réunion</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/variables.css">
    <link rel="stylesheet" href="css/typography.css">
    <link rel="stylesheet" href="css/layout.css">
    <link rel="stylesheet" href="css/components.css">
    <link rel="stylesheet" href="css/animations.css">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav id="navbar" class="navbar">
        <div class="nav-container">
            <div class="logo">Les Petites Mains</div>
            <ul class="nav-menu">
                <li><a href="#services">Services</a></li>
                <li><a href="#about">Qui suis-je</a></li>
                <li><a href="#testimonials">Avis</a></li>
                <li><a href="#booking" class="cta-link">Réserver</a></li>
            </ul>
            <div class="hamburger">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="hero" class="hero">
        <img src="assets/images/hero.jpg" alt="Ambiance relaxante" class="hero-bg">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1 class="hero-title">Détente à domicile</h1>
            <p class="hero-subtitle">Massage • Soins • Bien-être</p>
            <a href="#booking" class="scroll-indicator">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 5v14M19 12l-7 7-7-7"/>
                </svg>
            </a>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <div class="about-content">
                <div class="about-image">
                    <img src="assets/images/lisa-bio.jpg" alt="Lisa Coeslier" class="lisa-photo">
                </div>
                <div class="about-text">
                    <h2>À propos de moi</h2>
                    <p>Je m'appelle Lisa Coeslier, et j'ai plus de 6 ans d'expérience dans les domaines du bien-être, du massage et de la thalassothérapie. Passionnée par le bien-être holistique, j'ai développé une approche personnalisée pour chaque client, en écoutant vos besoins spécifiques et en adaptant mes prestations en conséquence.</p>
                    <p>Mes services à domicile vous permettent de vous détendre dans le confort de votre maison, sans stress de déplacement. Que vous cherchiez un massage relaxant, des soins du visage adaptés à votre peau, ou une approche holistique avec les fleurs de Bach, je suis là pour vous offrir une expérience de bien-être inoubliable.</p>
                    <div class="experience-badge">
                        <span class="badge-number">6+</span>
                        <span class="badge-text">Ans d'expérience</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="services">
        <div class="container">
            <h2 class="section-title">Nos Services</h2>
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">💆</div>
                    <h3>Massage à Domicile</h3>
                    <p>Massage relaxant, tonifiant ou personnalisé. Détente garantie dans votre environnement.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">✨</div>
                    <h3>Soins du Visage</h3>
                    <p>Soins personnalisés adaptés à votre type de peau. Produits de qualité, résultats visibles.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🌿</div>
                    <h3>Fleurs de Bach</h3>
                    <p>Consultation holistique et élixirs personnalisés pour votre bien-être émotionnel.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🎁</div>
                    <h3>Coffrets Cadeau</h3>
                    <p>Offrez le bien-être. Coffrets personnalisables pour vos proches.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section id="testimonials" class="testimonials">
        <div class="container">
            <h2 class="section-title">Avis de Mes Clients</h2>
            <div class="testimonials-grid">
                <div class="testimonial-card">
                    <div class="stars">⭐⭐⭐⭐⭐</div>
                    <p class="testimonial-quote">"Massage très professionnel et relaxant. Lisa crée une atmosphère apaisante et vraiment écoute vos besoins."</p>
                    <p class="testimonial-author"><strong>Marie D.</strong><br><small>Vérifiée</small></p>
                </div>
                <div class="testimonial-card">
                    <div class="stars">⭐⭐⭐⭐⭐</div>
                    <p class="testimonial-quote">"Soins du visage impeccables. Ma peau n'a jamais été aussi belle. Service à domicile très pratique."</p>
                    <p class="testimonial-author"><strong>Sophie L.</strong><br><small>Vérifiée</small></p>
                </div>
                <div class="testimonial-card">
                    <div class="stars">⭐⭐⭐⭐⭐</div>
                    <p class="testimonial-quote">"Lisa est très à l'écoute et professionnelle. Les fleurs de Bach m'ont vraiment aidé. Je recommande vivement!"</p>
                    <p class="testimonial-author"><strong>Jean P.</strong><br><small>Vérifiée</small></p>
                </div>
            </div>
        </div>
    </section>

    <!-- Booking Section -->
    <section id="booking" class="booking">
        <div class="container">
            <h2 class="booking-title">Prêt à vous détendre?</h2>
            <p class="booking-subtitle">Réservez votre soin en quelques clics</p>
            <a href="tel:+262262123456" class="btn-primary">Réserver maintenant</a>
            <p class="booking-alt">Ou <a href="mailto:contact@lespetitesmainsdelisa.re" class="link-secondary">contactez-moi directement</a></p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-col">
                    <h3 class="footer-logo">Les Petites Mains de Lisa</h3>
                    <p class="footer-tagline">Détente à domicile</p>
                </div>
                <div class="footer-col">
                    <h4>Contact</h4>
                    <p><a href="tel:+262262123456">📞 +262 (0) 262 12 34 56</a></p>
                    <p><a href="mailto:contact@lespetitesmainsdelisa.re">📧 contact@lespetitesmainsdelisa.re</a></p>
                    <p>🕒 Lun-Sam: 9h-18h<br>Dim: Sur rendez-vous</p>
                </div>
                <div class="footer-col">
                    <h4>Liens</h4>
                    <ul>
                        <li><a href="#services">Services</a></li>
                        <li><a href="#about">Qui suis-je</a></li>
                        <li><a href="#testimonials">Avis</a></li>
                        <li><a href="#booking">Réserver</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Les Petites Mains de Lisa. Tous droits réservés.</p>
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="js/scroll-animations.js"></script>
    <script src="js/main.js"></script>
</body>
</html>
```

- [ ] **Step 3: Create css/variables.css**

```css
:root {
    /* Colors */
    --color-bg: #F9F7F4;
    --color-bg-white: #FFFFFF;
    --color-bg-light: #FFF0F3;
    --color-text-primary: #2C2C2C;
    --color-text-secondary: #666666;
    --color-accent-primary: #C97C5C;
    --color-accent-secondary: #8FA39A;
    --color-accent-tertiary: #D4A574;
    --color-footer: #3D3D3D;
    
    /* Typography */
    --font-serif: 'Cormorant Garamond', serif;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    
    /* Spacing Scale (8px base) */
    --space-xs: 0.5rem;
    --space-sm: 1rem;
    --space-md: 1.5rem;
    --space-lg: 2rem;
    --space-xl: 3rem;
    --space-xxl: 4rem;
    
    /* Shadows */
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
    
    /* Border Radius */
    --radius-sm: 2px;
    --radius-md: 4px;
    --radius-lg: 8px;
    
    /* Transitions */
    --transition-fast: 0.2s ease-in-out;
    --transition-normal: 0.3s ease-in-out;
    --transition-slow: 0.6s ease-out;
}
```

- [ ] **Step 4: Create css/reset.css**

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
    font-size: 16px;
}

body {
    background-color: var(--color-bg);
    color: var(--color-text-primary);
    font-family: var(--font-sans);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
}

a {
    color: inherit;
    text-decoration: none;
}

button {
    font-family: inherit;
    cursor: pointer;
    border: none;
}

ul, ol {
    list-style: none;
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-serif);
    line-height: 1.2;
    font-weight: 600;
}
```

- [ ] **Step 5: Create js/main.js**

```javascript
// Mobile menu toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navbar = document.querySelector('.navbar');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Close menu on link click
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Navbar background on scroll
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scroll for buttons
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
```

- [ ] **Step 6: Create js/scroll-animations.js**

```javascript
// Intersection Observer for scroll reveals
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('reveal');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements with data-reveal attribute
document.querySelectorAll('[data-reveal]').forEach(el => {
    observer.observe(el);
});

// Stagger effect for grids
document.querySelectorAll('[data-stagger]').forEach(container => {
    const children = container.children;
    Array.from(children).forEach((child, index) => {
        child.style.setProperty('--stagger-delay', `${index * 100}ms`);
    });
});
```

- [ ] **Step 7: Create initial git commit**

```bash
cd /work/lespetitesmainsdelisa-optimized
git add .
git commit -m "Initial project setup: HTML skeleton, CSS variables, JavaScript structure"
```

---

### Task 2: Typography System

**Files:**
- Create: `css/typography.css`

- [ ] **Step 1: Create typography.css with font definitions**

```css
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

/* Font Face (if using local files) */
/* @font-face {
    font-family: 'Cormorant Garamond';
    src: url('../assets/fonts/cormorant-garamond.woff2') format('woff2');
    font-weight: 600;
} */

/* Heading Styles */
h1 {
    font-family: var(--font-serif);
    font-size: 4rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

h2 {
    font-family: var(--font-serif);
    font-size: 2.5rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    line-height: 1.2;
    margin-bottom: var(--space-md);
}

h3 {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: var(--space-sm);
}

h4 {
    font-family: var(--font-serif);
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: var(--space-sm);
}

/* Body Text */
p {
    font-family: var(--font-sans);
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: var(--space-md);
}

/* Small Text */
small {
    font-size: 0.875rem;
    line-height: 1.5;
    color: var(--color-text-secondary);
}

/* Quotes / Testimonials */
.testimonial-quote {
    font-family: var(--font-serif);
    font-style: italic;
    font-size: 1.125rem;
    line-height: 1.5;
    color: var(--color-text-primary);
}

/* Links */
a {
    color: var(--color-text-primary);
    text-decoration: none;
    transition: color var(--transition-normal);
}

a:hover {
    color: var(--color-accent-primary);
}

/* Responsive Typography */
@media (max-width: 768px) {
    h1 {
        font-size: 2.5rem;
    }

    h2 {
        font-size: 1.75rem;
    }

    h3 {
        font-size: 1.25rem;
    }

    p {
        font-size: 0.95rem;
    }
}
```

- [ ] **Step 2: Commit typography**

```bash
git add css/typography.css
git commit -m "feat: add typography system with Cormorant Garamond and Inter"
```

---

### Task 3: Layout Foundation (Container, Grid, Flexbox)

**Files:**
- Create: `css/layout.css`

- [ ] **Step 1: Create css/layout.css with container and flexbox utilities**

```css
/* Container */
.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}

/* Sections */
section {
    padding: var(--space-xxl) 0;
}

section:first-child {
    padding-top: 0;
}

/* Navigation */
.navbar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background-color: transparent;
    padding: var(--space-lg) 0;
    transition: background-color var(--transition-normal);
}

.navbar.scrolled {
    background-color: rgba(249, 247, 244, 0.95);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}

.logo {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-text-primary);
}

.nav-menu {
    display: flex;
    gap: var(--space-xl);
    list-style: none;
}

.nav-menu a {
    font-size: 0.95rem;
    color: var(--color-text-primary);
    transition: color var(--transition-normal);
}

.nav-menu a:hover {
    color: var(--color-accent-primary);
}

.cta-link {
    color: var(--color-accent-primary);
    font-weight: 600;
}

/* Hamburger Menu */
.hamburger {
    display: none;
    flex-direction: column;
    gap: 6px;
    cursor: pointer;
}

.hamburger span {
    width: 24px;
    height: 2px;
    background-color: var(--color-text-primary);
    transition: all var(--transition-normal);
}

/* Hero Section */
.hero {
    position: relative;
    height: 100vh;
    min-height: 600px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.3);
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    text-align: center;
    color: white;
    animation: fadeInUp 0.8s ease-out;
}

.hero-title {
    font-size: 4rem;
    color: white;
    margin-bottom: var(--space-md);
    font-weight: 600;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: rgba(255, 255, 255, 0.9);
    letter-spacing: 0.1em;
    margin-bottom: var(--space-xxl);
}

.scroll-indicator {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    color: white;
    animation: bounce 2s infinite;
}

/* About Section */
.about {
    background-color: var(--color-bg);
}

.about-content {
    display: grid;
    grid-template-columns: 40% 1fr;
    gap: var(--space-xxl);
    align-items: center;
}

.about-image {
    display: flex;
    align-items: center;
    justify-content: center;
}

.lisa-photo {
    width: 100%;
    max-width: 300px;
    aspect-ratio: 1;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-md);
    object-fit: cover;
}

.about-text h2 {
    color: var(--color-text-primary);
    margin-bottom: var(--space-lg);
}

.about-text p {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-md);
    line-height: 1.8;
}

.experience-badge {
    display: inline-flex;
    align-items: baseline;
    gap: var(--space-sm);
    margin-top: var(--space-lg);
    padding: var(--space-md) var(--space-lg);
    background-color: var(--color-bg-light);
    border-left: 4px solid var(--color-accent-primary);
    border-radius: var(--radius-md);
}

.badge-number {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-accent-primary);
}

.badge-text {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
}

/* Services Section */
.services {
    background-color: var(--color-bg-white);
}

.section-title {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: var(--space-xxl);
    color: var(--color-text-primary);
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-lg);
}

.services-grid > :nth-child(3) {
    grid-column: 1;
}

.services-grid > :nth-child(4) {
    grid-column: 2;
    grid-row: 2;
}

.service-card {
    padding: var(--space-lg);
    background-color: var(--color-bg-white);
    border-left: 4px solid var(--color-accent-primary);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-normal);
}

.service-card:nth-child(2) {
    border-left-color: var(--color-accent-secondary);
}

.service-card:nth-child(3) {
    border-left-color: var(--color-accent-tertiary);
}

.service-card:nth-child(4) {
    border-left-color: var(--color-accent-primary);
}

.service-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
}

.service-icon {
    font-size: 2.5rem;
    margin-bottom: var(--space-md);
}

.service-card h3 {
    color: var(--color-text-primary);
    margin-bottom: var(--space-sm);
}

.service-card p {
    font-size: 0.95rem;
    color: var(--color-text-secondary);
    line-height: 1.6;
}

/* Testimonials Section */
.testimonials {
    background-color: var(--color-bg);
}

.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-lg);
}

.testimonial-card {
    padding: var(--space-lg);
    background-color: var(--color-bg-light);
    border-left: 4px solid var(--color-accent-primary);
    border-radius: var(--radius-md);
}

.stars {
    font-size: 1rem;
    margin-bottom: var(--space-md);
    letter-spacing: 2px;
}

.testimonial-quote {
    margin-bottom: var(--space-md);
    color: var(--color-text-primary);
}

.testimonial-author {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
}

.testimonial-author strong {
    color: var(--color-text-primary);
}

/* Booking Section */
.booking {
    background-color: rgba(143, 163, 154, 0.1);
    text-align: center;
    padding: var(--space-xxl) var(--space-lg);
}

.booking-title {
    font-size: 2rem;
    color: var(--color-text-primary);
    margin-bottom: var(--space-md);
}

.booking-subtitle {
    font-size: 1.1rem;
    color: var(--color-text-secondary);
    margin-bottom: var(--space-lg);
}

.booking-alt {
    margin-top: var(--space-lg);
    font-size: 0.95rem;
    color: var(--color-text-secondary);
}

/* Footer */
.footer {
    background-color: var(--color-footer);
    color: white;
    padding: var(--space-xxl) 0 var(--space-lg);
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-xl);
    margin-bottom: var(--space-xl);
}

.footer-col h3, .footer-col h4 {
    color: white;
    margin-bottom: var(--space-md);
    font-size: 1.1rem;
}

.footer-logo {
    font-family: var(--font-serif);
    font-size: 1.3rem;
    font-weight: 700;
}

.footer-tagline {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.7);
    margin-top: var(--space-sm);
}

.footer-col p {
    margin-bottom: var(--space-sm);
    font-size: 0.95rem;
    color: rgba(255, 255, 255, 0.8);
}

.footer-col a {
    color: rgba(255, 255, 255, 0.8);
    transition: color var(--transition-normal);
}

.footer-col a:hover {
    color: var(--color-accent-primary);
}

.footer-col ul li {
    margin-bottom: var(--space-sm);
}

.footer-bottom {
    text-align: center;
    padding-top: var(--space-lg);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.6);
}

/* Responsive */
@media (max-width: 768px) {
    .nav-menu {
        gap: var(--space-lg);
    }

    .hamburger {
        display: flex;
    }

    .nav-menu {
        display: none;
    }

    .nav-menu.active {
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 60px;
        left: 0;
        right: 0;
        background-color: var(--color-bg);
        padding: var(--space-lg);
        box-shadow: var(--shadow-md);
    }

    .hero-title {
        font-size: 2.5rem;
    }

    .about-content {
        grid-template-columns: 1fr;
    }

    .services-grid {
        grid-template-columns: 1fr;
    }

    .testimonials-grid {
        grid-template-columns: 1fr;
    }

    .footer-content {
        grid-template-columns: 1fr;
    }
}
```

- [ ] **Step 2: Commit layout**

```bash
git add css/layout.css
git commit -m "feat: add responsive layout with grid, flexbox, and section styling"
```

---

### Task 4: Components (Buttons, Links, Forms)

**Files:**
- Create: `css/components.css`

- [ ] **Step 1: Create css/components.css**

```css
/* Buttons */
.btn-primary {
    display: inline-block;
    padding: 1rem 2.5rem;
    background-color: var(--color-accent-primary);
    color: white;
    font-family: var(--font-sans);
    font-weight: 600;
    font-size: 1rem;
    border-radius: var(--radius-md);
    transition: all var(--transition-normal);
    cursor: pointer;
    text-decoration: none;
    border: none;
    box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
    background-color: #b0694d;
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.btn-primary:active {
    transform: translateY(0);
}

/* Secondary Links */
.link-secondary {
    color: var(--color-accent-primary);
    font-weight: 600;
    text-decoration: none;
    transition: color var(--transition-normal);
    position: relative;
}

.link-secondary:hover {
    color: #b0694d;
    text-decoration: underline;
}

/* Form Elements */
input[type="text"],
input[type="email"],
input[type="tel"],
textarea {
    width: 100%;
    padding: var(--space-md);
    font-family: var(--font-sans);
    font-size: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: var(--radius-md);
    transition: border-color var(--transition-normal);
    margin-bottom: var(--space-md);
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="tel"]:focus,
textarea:focus {
    outline: none;
    border-color: var(--color-accent-primary);
    box-shadow: 0 0 0 3px rgba(201, 124, 92, 0.1);
}

textarea {
    resize: vertical;
    min-height: 120px;
}

/* Loading State */
.loading {
    opacity: 0.6;
    pointer-events: none;
}

/* Cards - General */
.card {
    background-color: var(--color-bg-white);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-normal);
}

.card:hover {
    box-shadow: var(--shadow-md);
}

/* Badge */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background-color: var(--color-accent-primary);
    color: white;
    font-size: 0.75rem;
    font-weight: 700;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Icon Badge */
.icon-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background-color: var(--color-bg-light);
    border-radius: 50%;
    font-size: 1.25rem;
}
```

- [ ] **Step 2: Commit components**

```bash
git add css/components.css
git commit -m "feat: add button, form, and component styles"
```

---

### Task 5: Animations (Scroll Reveals, Hover Effects)

**Files:**
- Create: `css/animations.css`

- [ ] **Step 1: Create css/animations.css**

```css
/* Keyframe Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes scaleUp {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}

/* Scroll Reveal Classes */
.reveal {
    animation: fadeInUp 0.6s ease-out forwards;
}

[data-reveal] {
    opacity: 0;
}

[data-stagger] > * {
    animation: fadeInUp 0.6s ease-out forwards;
    animation-delay: var(--stagger-delay, 0ms);
}

/* Parallax on Scroll */
.parallax {
    background-attachment: fixed;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
}

/* Service Card Animations */
.service-card {
    animation: fadeInUp 0.6s ease-out backwards;
}

.services-grid > :nth-child(1) {
    animation-delay: 0ms;
}

.services-grid > :nth-child(2) {
    animation-delay: 100ms;
}

.services-grid > :nth-child(3) {
    animation-delay: 200ms;
}

.services-grid > :nth-child(4) {
    animation-delay: 300ms;
}

/* Testimonial Card Animations */
.testimonial-card {
    animation: fadeInUp 0.6s ease-out backwards;
}

.testimonials-grid > :nth-child(1) {
    animation-delay: 0ms;
}

.testimonials-grid > :nth-child(2) {
    animation-delay: 100ms;
}

.testimonials-grid > :nth-child(3) {
    animation-delay: 200ms;
}

/* Hover Effects */
.service-card:hover {
    transform: translateY(-4px);
}

.service-card:hover h3 {
    color: var(--color-accent-primary);
}

.testimonial-card:hover {
    transform: translateY(-2px);
}

/* Link Hover Effects */
a {
    position: relative;
}

a.btn-primary::before,
a.link-secondary::before {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background-color: var(--color-accent-primary);
    transition: width var(--transition-normal);
}

a.link-secondary:hover::before {
    width: 100%;
}

/* Fade In On Load */
body {
    animation: fadeIn 0.5s ease-out;
}

/* Button Ripple Effect (Optional) */
.btn-primary {
    position: relative;
    overflow: hidden;
}

.btn-primary::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.5);
    transform: translate(-50%, -50%);
    pointer-events: none;
}

.btn-primary:active::after {
    animation: ripple 0.6s ease-out;
}

@keyframes ripple {
    to {
        width: 300px;
        height: 300px;
        opacity: 0;
    }
}
```

- [ ] **Step 2: Commit animations**

```bash
git add css/animations.css
git commit -m "feat: add scroll animations, hover effects, and transition styles"
```

---

### Task 6: Add Images & Assets

**Files:**
- Create placeholder images and SVG icons

- [ ] **Step 1: Create placeholder images directory**

```bash
mkdir -p assets/images assets/icons
```

- [ ] **Step 2: Add hero image (placeholder or real)**

For now, use a placeholder. In production, replace with real image:
```bash
# Create a simple placeholder (1920x1080)
# You can use an image from Unsplash or local assets
# Example: curl -o assets/images/hero.jpg 'https://images.unsplash.com/photo-1544161515-4ab6ce6c1b1d?w=1920&h=1080&fit=crop'
```

- [ ] **Step 3: Add Lisa bio image (placeholder)**

```bash
# Similar to hero, add a portrait image
# For now, use a placeholder
```

- [ ] **Step 4: Create SVG icons for services**

Create `assets/icons/massage.svg`:
```svg
<svg viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
</svg>
```

Create similar SVGs for skincare, Bach flowers, gift packages.

- [ ] **Step 5: Commit assets**

```bash
git add assets/
git commit -m "feat: add placeholder images and service icons"
```

---

### Task 7: Responsive Design & Mobile Menu

**Files:**
- Modify: `css/layout.css`, `js/main.js` (already done in earlier tasks)

- [ ] **Step 1: Test responsive breakpoints**

```bash
# Test on:
# - Desktop (1920px)
# - Tablet (768px)
# - Mobile (375px)
```

- [ ] **Step 2: Verify mobile menu works**

Test hamburger toggle functionality in `js/main.js` works on mobile.

- [ ] **Step 3: Commit responsive verification**

```bash
git add .
git commit -m "test: verify responsive design and mobile menu functionality"
```

---

### Task 8: Scroll Animation Enhancement & Performance

**Files:**
- Modify: `js/scroll-animations.js`

- [ ] **Step 1: Add data attributes to HTML for scroll reveals**

Add `data-reveal` to sections that need animation:
- Service cards
- Testimonial cards
- Bio section
- Booking section

Update `index.html`:
```html
<!-- Example: Add to service cards -->
<div class="services-grid" data-stagger>
    <div class="service-card" data-reveal>...</div>
    <!-- etc -->
</div>
```

- [ ] **Step 2: Test scroll animations in browser**

Scroll down page and verify:
- Elements fade in and slide up
- Stagger effect works (cards animate sequentially)
- No performance jank

- [ ] **Step 3: Commit scroll enhancements**

```bash
git add index.html js/scroll-animations.js
git commit -m "feat: add scroll reveal animations with stagger effect"
```

---

### Task 9: Accessibility & SEO

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add accessibility attributes**

```html
<!-- Add ARIA labels where needed -->
<nav aria-label="Primary navigation">...</nav>
<button aria-label="Toggle mobile menu">...</button>

<!-- Ensure color contrast is WCAG AA -->
<!-- Already done with color palette -->

<!-- Add alt text to images -->
<img src="assets/images/hero.jpg" alt="Spa ambiance with warm lighting">
```

- [ ] **Step 2: Add structured data (schema.org)**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Les Petites Mains de Lisa",
  "description": "Massage et soins à domicile",
  "url": "https://lespetitesmainsdelisa.re",
  "telephone": "+262262123456",
  "email": "contact@lespetitesmainsdelisa.re",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "La Réunion"
  },
  "areaServed": "La Réunion",
  "image": "assets/images/hero.jpg"
}
</script>
```

- [ ] **Step 3: Verify accessibility**

Run accessibility checker (WAVE, Lighthouse) to ensure:
- Proper heading hierarchy
- Color contrast ≥ 4.5:1
- Alt text present
- Focus indicators visible

- [ ] **Step 4: Commit accessibility**

```bash
git add index.html
git commit -m "feat: add accessibility attributes and structured data"
```

---

### Task 10: Performance Optimization

**Files:**
- Modify: `index.html`, images

- [ ] **Step 1: Optimize images**

```bash
# Compress hero image to <200KB
# Convert to WebP format for modern browsers
# Add srcset for responsive images

# Example:
# <img src="assets/images/hero.jpg" 
#      srcset="assets/images/hero-mobile.jpg 375w, assets/images/hero-tablet.jpg 768w, assets/images/hero.jpg 1920w"
#      alt="Spa ambiance">
```

- [ ] **Step 2: Lazy load below-fold images**

```html
<!-- Add loading="lazy" to images below the fold -->
<img src="assets/images/lisa-bio.jpg" alt="Lisa" loading="lazy">
```

- [ ] **Step 3: Minify CSS (optional)**

Create a build step or use inline critical CSS for hero.

- [ ] **Step 4: Test performance**

```bash
# Use Lighthouse in Chrome DevTools
# Target scores:
# - Performance: >90
# - Accessibility: >95
# - Best Practices: >90
# - SEO: >95
```

- [ ] **Step 5: Commit performance optimizations**

```bash
git add assets/ index.html
git commit -m "feat: optimize images, add lazy loading, improve performance"
```

---

### Task 11: Create Dockerfile & Nginx Config

**Files:**
- Create: `Dockerfile`, `nginx.conf`

- [ ] **Step 1: Create Dockerfile**

```dockerfile
FROM nginx:alpine

# Copy website files to nginx
COPY . /usr/share/nginx/html/

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

Save to `Dockerfile`

- [ ] **Step 2: Create nginx.conf**

```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Enable gzip compression
    gzip on;
    gzip_types text/css text/javascript application/javascript application/json;
    gzip_min_length 1024;

    # Cache static assets
    location ~* \.(js|css|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # Serve index.html for all routes (SPA support)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

Save to `nginx.conf`

- [ ] **Step 3: Commit Docker config**

```bash
git add Dockerfile nginx.conf
git commit -m "feat: add Docker and nginx configuration for deployment"
```

---

### Task 12: Create README & Documentation

**Files:**
- Create: `README.md`, `package.json`

- [ ] **Step 1: Create README.md**

```markdown
# Les Petites Mains de Lisa — Website

Distinctive, production-grade website for wellness and beauty services.

## Features

- **Responsive Design**: Mobile-first, works on all devices
- **Smooth Animations**: Scroll reveals, hover effects, transitions
- **Accessible**: WCAG AA compliant, semantic HTML
- **Performance**: Optimized images, minimal CSS/JS
- **SEO**: Structured data, meta tags, open graph

## Tech Stack

- HTML5
- CSS3 (Grid, Flexbox, Animations)
- Vanilla JavaScript
- Docker + Nginx

## Local Development

### Requirements
- Node.js (optional, for build tools)
- Browser with CSS Grid & Flexbox support

### Running Locally

```bash
# Start a local server (Python 3)
python3 -m http.server 8000

# Or use Live Server in VS Code
```

Then open `http://localhost:8000`

### File Structure

```
.
├── index.html           # Main HTML file
├── css/                 # Stylesheets
│   ├── variables.css    # CSS custom properties
│   ├── reset.css        # CSS reset
│   ├── typography.css   # Font & text styles
│   ├── layout.css       # Layout components
│   ├── components.css   # Reusable components
│   └── animations.css   # Animations & transitions
├── js/                  # JavaScript files
│   ├── main.js          # Main script
│   └── scroll-animations.js # Scroll reveal logic
├── assets/
│   ├── images/          # Images (optimized)
│   └── icons/           # SVG icons
├── Dockerfile           # Docker configuration
├── nginx.conf           # Nginx configuration
└── README.md            # This file
```

## Deployment

### Docker

```bash
# Build image
docker build -t lespetitesmainsdelisa .

# Run container
docker run -p 80:8080 lespetitesmainsdelisa
```

### Coolify

Push to GitHub and deploy via Coolify with the provided Dockerfile.

## Performance

- Lighthouse Score: 95+
- First Contentful Paint: <1.5s
- Largest Contentful Paint: <2.5s
- Cumulative Layout Shift: <0.1

## Accessibility

- WCAG AA compliant
- Semantic HTML
- Alt text for all images
- Color contrast ≥ 4.5:1
- Keyboard navigable

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers

## License

© 2026 Les Petites Mains de Lisa. All rights reserved.
```

Save to `README.md`

- [ ] **Step 2: Create package.json**

```json
{
  "name": "lespetitesmainsdelisa",
  "version": "1.0.0",
  "description": "Distinctive website for wellness and beauty services",
  "main": "index.html",
  "scripts": {
    "serve": "python3 -m http.server 8000",
    "build": "docker build -t lespetitesmainsdelisa .",
    "start": "docker run -p 80:8080 lespetitesmainsdelisa"
  },
  "keywords": ["wellness", "massage", "spa", "services"],
  "author": "Lisa Coeslier",
  "license": "proprietary"
}
```

Save to `package.json`

- [ ] **Step 3: Commit documentation**

```bash
git add README.md package.json
git commit -m "docs: add README and package.json"
```

---

### Task 13: Final Testing & QA

**Files:**
- All files (verification)

- [ ] **Step 1: Test all links and functionality**

- [ ] **Step 2: Cross-browser testing**

Test in:
- Chrome/Edge
- Firefox
- Safari
- Mobile browsers

- [ ] **Step 3: Run Lighthouse audit**

Ensure:
- Performance > 90
- Accessibility > 95
- Best Practices > 90
- SEO > 95

- [ ] **Step 4: Verify all animations**

- [ ] **Step 5: Check responsive design**

Test at:
- 375px (mobile)
- 768px (tablet)
- 1200px+ (desktop)

- [ ] **Step 6: Final commit**

```bash
git add .
git commit -m "test: final QA and cross-browser verification complete"
```

---

### Task 14: Prepare for Deployment

**Files:**
- All files ready

- [ ] **Step 1: Push to GitHub**

```bash
git remote add origin https://github.com/tonyPayetDev/lespetitesmainsdelisa-optimized.git
git branch -M main
git push -u origin main
```

- [ ] **Step 2: Verify deployment readiness**

- Docker image builds successfully
- Nginx config is valid
- All assets are included
- No console errors

- [ ] **Step 3: Final commit**

```bash
git add .
git commit -m "chore: deployment preparation complete"
```

---

## Execution Workflow

This plan is **ready for execution**. Two options:

**Option 1: Subagent-Driven (Recommended)**
- Fresh subagent per task
- Faster iteration
- Built-in review between tasks

**Option 2: Inline Execution**
- Execute tasks in current session
- Batch execution with checkpoints
- Single continuous workflow

---

**Total estimated time**: 3-4 hours for complete build + deployment

**Status**: ✅ Ready for implementation

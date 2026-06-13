// ===== Navbar Scroll Effect =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// ===== Mobile Menu Toggle =====
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    menuToggle.classList.toggle('active');
});

// Close menu on link click
navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        menuToggle.classList.remove('active');
    });
});

// ===== Counter Animation =====
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-count');
        const duration = 2000;
        const start = performance.now();

        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            counter.textContent = Math.floor(eased * target).toLocaleString('fr-FR');
            if (progress < 1) requestAnimationFrame(update);
        }

        requestAnimationFrame(update);
    });
}

// Trigger counters when hero is visible
const heroObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            heroObserver.disconnect();
        }
    });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) heroObserver.observe(heroStats);

// ===== Event Filters =====
const filterButtons = document.querySelectorAll('.filter-btn');
const eventCards = document.querySelectorAll('.event-card');

filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.getAttribute('data-filter');

        eventCards.forEach(card => {
            if (filter === 'all' || card.getAttribute('data-category') === filter) {
                card.classList.remove('hidden');
                card.style.animation = 'fadeInUp 0.4s ease forwards';
            } else {
                card.classList.add('hidden');
            }
        });
    });
});

// ===== Form Validation & Submit =====
const form = document.getElementById('registrationForm');
const successModal = document.getElementById('successModal');
const closeModal = document.getElementById('closeModal');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Remove previous errors
    form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    form.querySelectorAll('.error-msg').forEach(el => el.remove());

    let isValid = true;

    // Validate required fields
    const nom = document.getElementById('nom');
    const prenom = document.getElementById('prenom');
    const email = document.getElementById('email');
    const telephone = document.getElementById('telephone');
    const evenement = document.getElementById('evenement');
    const conditions = document.getElementById('conditions');

    if (!nom.value.trim()) { showError(nom, 'Veuillez entrer votre nom'); isValid = false; }
    if (!prenom.value.trim()) { showError(prenom, 'Veuillez entrer votre prénom'); isValid = false; }

    if (!email.value.trim()) {
        showError(email, 'Veuillez entrer votre email');
        isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        showError(email, 'Veuillez entrer un email valide');
        isValid = false;
    }

    if (!telephone.value.trim()) {
        showError(telephone, 'Veuillez entrer votre téléphone');
        isValid = false;
    } else if (!/^[\d\s+()-]{10,}$/.test(telephone.value)) {
        showError(telephone, 'Numéro de téléphone invalide');
        isValid = false;
    }

    if (!evenement.value) { showError(evenement, 'Veuillez choisir un événement'); isValid = false; }

    if (!conditions.checked) {
        showError(conditions.closest('.checkbox-group'), 'Vous devez accepter les conditions');
        isValid = false;
    }

    if (isValid) {
        const btnText = form.querySelector('.btn-text');
        const btnLoader = form.querySelector('.btn-loader');
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';

        // Simulate submission
        setTimeout(() => {
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
            successModal.classList.add('active');
            form.reset();
        }, 1500);
    }
});

function showError(element, message) {
    element.classList.add('error');
    const msg = document.createElement('span');
    msg.className = 'error-msg';
    msg.style.cssText = 'color:#e63946;font-size:0.8rem;margin-top:4px;display:block;';
    msg.textContent = message;
    element.closest('.form-group, .checkbox-group').appendChild(msg);
}

// Close modal
closeModal.addEventListener('click', () => {
    successModal.classList.remove('active');
});

successModal.addEventListener('click', (e) => {
    if (e.target === successModal) successModal.classList.remove('active');
});

// ===== Scroll Animations =====
const animateOnScroll = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.event-card, .gallery-item, .contact-card, .info-feature').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    animateOnScroll.observe(el);
});

// ===== Smooth scroll for nav links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

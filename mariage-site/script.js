// ===== Countdown Timer =====
function updateCountdown() {
    const weddingDate = new Date('2026-07-12T15:00:00');
    const now = new Date();
    const diff = weddingDate - now;

    if (diff <= 0) {
        document.getElementById('days').textContent = '0';
        document.getElementById('hours').textContent = '0';
        document.getElementById('minutes').textContent = '0';
        document.getElementById('seconds').textContent = '0';
        return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    document.getElementById('days').textContent = days;
    document.getElementById('hours').textContent = hours;
    document.getElementById('minutes').textContent = minutes;
    document.getElementById('seconds').textContent = seconds;
}

updateCountdown();
setInterval(updateCountdown, 1000);

// ===== Show/Hide presence details =====
const presenceSelect = document.getElementById('presence');
const detailsPresence = document.getElementById('details-presence');

presenceSelect.addEventListener('change', function () {
    if (this.value === 'oui') {
        detailsPresence.classList.remove('hidden');
    } else {
        detailsPresence.classList.add('hidden');
    }
});

// Initially hidden until "oui" is selected
detailsPresence.classList.add('hidden');

// ===== Form Submission =====
const form = document.getElementById('rsvp-form');
const confirmation = document.getElementById('confirmation');

// Endpoint to POST RSVP data — replace with your Formspree/backend URL
const RSVP_ENDPOINT = 'https://formspree.io/f/YOUR_FORM_ID';

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Envoi en cours…';

    const formData = new FormData(form);

    fetch(RSVP_ENDPOINT, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
    })
        .then(function (response) {
            if (!response.ok) {
                return response.json().then(function (body) {
                    throw new Error((body && body.error) || 'Erreur réseau');
                });
            }
            // Show confirmation
            form.style.display = 'none';
            confirmation.classList.remove('hidden');
            confirmation.scrollIntoView({ behavior: 'smooth', block: 'center' });
        })
        .catch(function (err) {
            console.error('RSVP submission error:', err);
            const errorMsg = form.querySelector('.rsvp-error');
            if (errorMsg) {
                errorMsg.textContent = 'Une erreur est survenue. Veuillez réessayer ou nous contacter directement.';
                errorMsg.classList.remove('hidden');
            } else {
                alert('Une erreur est survenue. Veuillez réessayer ou nous contacter directement.');
            }
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
        });
});

// ===== Smooth scroll for nav links =====
document.querySelectorAll('#navbar a').forEach(function (link) {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const target = document.querySelector(targetId);
        if (target) {
            const navHeight = document.getElementById('navbar').offsetHeight;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
            window.scrollTo({ top: targetPosition, behavior: 'smooth' });
        }
    });
});

// ===== Navbar scroll effect =====
let lastScroll = 0;
window.addEventListener('scroll', function () {
    const navbar = document.getElementById('navbar');
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.12)';
    } else {
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.08)';
    }

    lastScroll = currentScroll;
});

// ===== Animate elements on scroll =====
function animateOnScroll() {
    const elements = document.querySelectorAll('.timeline-item, .detail-card, .programme-item, .galerie-item');

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    elements.forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

animateOnScroll();

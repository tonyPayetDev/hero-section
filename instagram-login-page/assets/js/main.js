'use strict';

/* ===========================
   PASSWORD TOGGLE
   =========================== */
function initPasswordToggle() {
  const toggles = document.querySelectorAll('.password-toggle');
  toggles.forEach(toggle => {
    toggle.addEventListener('click', function () {
      const input = this.closest('.password-wrapper').querySelector('.form-input');
      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';
      this.textContent = isPassword ? 'Hide' : 'Show';
    });
  });
}

/* ===========================
   LOGIN FORM
   =========================== */
function initLoginForm() {
  const form = document.getElementById('loginForm');
  if (!form) return;

  const submitBtn = form.querySelector('[type="submit"]');
  const alertEl = form.querySelector('.alert');
  const usernameInput = form.querySelector('#username');
  const passwordInput = form.querySelector('#password');

  // Enable/disable button based on input
  function checkInputs() {
    const hasUser = usernameInput.value.trim().length > 0;
    const hasPass = passwordInput.value.trim().length > 0;
    submitBtn.disabled = !(hasUser && hasPass);
  }

  usernameInput.addEventListener('input', checkInputs);
  passwordInput.addEventListener('input', checkInputs);

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Simulate loading
    submitBtn.classList.add('btn-loading');
    submitBtn.textContent = 'Logging in...';

    setTimeout(() => {
      submitBtn.classList.remove('btn-loading');
      submitBtn.textContent = 'Log in';

      // Show demo error (since no real backend)
      if (alertEl) {
        alertEl.classList.add('show');
        setTimeout(() => alertEl.classList.remove('show'), 4000);
      }
    }, 1800);
  });
}

/* ===========================
   RESET PASSWORD FORM
   =========================== */
function initResetForm() {
  const form = document.getElementById('resetForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const btn = form.querySelector('[type="submit"]');
    const emailInput = form.querySelector('.form-input');
    const successMsg = document.getElementById('resetSuccess');

    if (!emailInput.value.trim()) return;

    btn.classList.add('btn-loading');
    btn.textContent = 'Sending...';

    setTimeout(() => {
      btn.classList.remove('btn-loading');
      btn.textContent = 'Send reset link';
      form.reset();

      if (successMsg) {
        successMsg.classList.add('show');
        setTimeout(() => successMsg.classList.remove('show'), 5000);
      }
      showToast('✉️', 'Reset link sent! Check your email.');
    }, 2000);
  });
}

/* ===========================
   FACEBOOK LOGIN
   =========================== */
function initFacebookLogin() {
  const btn = document.getElementById('facebookLoginBtn');
  if (!btn) return;

  btn.addEventListener('click', function () {
    this.classList.add('btn-loading');
    this.querySelector('.fb-btn-text').textContent = 'Connecting...';

    setTimeout(() => {
      this.classList.remove('btn-loading');
      this.querySelector('.fb-btn-text').textContent = 'Log in with Facebook';
      showToast('ℹ️', 'Facebook login requires app configuration.');
    }, 1500);
  });
}

/* ===========================
   TOAST NOTIFICATION
   =========================== */
function showToast(icon, message) {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }

  toast.innerHTML = `<span class="toast-icon">${icon}</span><span>${message}</span>`;
  toast.classList.add('show');

  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => toast.classList.remove('show'), 3500);
}

/* ===========================
   SCROLL ANIMATIONS
   =========================== */
function initScrollAnimations() {
  const elements = document.querySelectorAll('[data-animate]');
  if (!elements.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, i * 80);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  elements.forEach(el => observer.observe(el));
}

/* ===========================
   STATS COUNTER ANIMATION
   =========================== */
function animateCounter(el, target, suffix) {
  const duration = 1500;
  const start = performance.now();
  const startVal = 0;

  function update(time) {
    const elapsed = time - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(startVal + (target - startVal) * eased);
    el.textContent = current + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

function initStatsAnimation() {
  const stats = document.querySelectorAll('[data-counter]');
  if (!stats.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.counter);
          const suffix = el.dataset.suffix || '';
          animateCounter(el, target, suffix);
          observer.unobserve(el);
        }
      });
    },
    { threshold: 0.5 }
  );

  stats.forEach(el => observer.observe(el));
}

/* ===========================
   PHONE MOCKUP CAROUSEL
   =========================== */
function initPhoneCarousel() {
  const screens = document.querySelectorAll('.phone-post-placeholder');
  const colors = [
    'linear-gradient(135deg, #f09433, #e6683c)',
    'linear-gradient(135deg, #dc2743, #cc2366)',
    'linear-gradient(135deg, #bc1888, #833ab4)',
    'linear-gradient(135deg, #1877F2, #0d6ae0)',
    'linear-gradient(135deg, #F3425F, #bc1888)',
    'linear-gradient(135deg, #e6683c, #f09433)',
  ];

  screens.forEach((screen, i) => {
    screen.style.background = colors[i % colors.length];
  });
}

/* ===========================
   SMOOTH SCROLL FOR ANCHORS
   =========================== */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

/* ===========================
   CREATE ACCOUNT CTA
   =========================== */
function initCreateAccount() {
  const btn = document.getElementById('createAccountBtn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    showToast('🎉', 'Account creation coming soon! Stay tuned.');
  });
}

/* ===========================
   INIT ALL
   =========================== */
document.addEventListener('DOMContentLoaded', function () {
  initPasswordToggle();
  initLoginForm();
  initResetForm();
  initFacebookLogin();
  initScrollAnimations();
  initStatsAnimation();
  initPhoneCarousel();
  initSmoothScroll();
  initCreateAccount();
});

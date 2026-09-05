// Reveal cards on scroll and animate the joke stats once they are visible.
// The `js` class gates the hidden state, so content stays readable without JS.
document.documentElement.classList.add('js');

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function animateCount(el) {
  const target = Number(el.dataset.count);
  if (reduceMotion || target === 0) {
    el.textContent = target.toLocaleString('fr-FR');
    return;
  }
  const duration = 900;
  const start = performance.now();
  const step = (now) => {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(target * eased).toLocaleString('fr-FR');
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('visible');
    entry.target.querySelectorAll('[data-count]').forEach(animateCount);
    observer.unobserve(entry.target);
  });
}, { threshold: 0.25 });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

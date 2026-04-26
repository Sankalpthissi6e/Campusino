// ========================================
// CAMPUSINO — Main JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', () => {
  initToasts();
  initFadeAnimations();
  initMobileNav();
  initTabs();
  initSearch();
});

// --- Toast Notification System ---
function initToasts() {
  const container = document.querySelector('.toast-container');
  if (!container) return;
  const toasts = container.querySelectorAll('.toast');
  toasts.forEach((toast, i) => {
    setTimeout(() => {
      toast.style.animation = 'slideOut 0.3s ease forwards';
      setTimeout(() => toast.remove(), 300);
    }, 4000 + i * 500);
    const close = toast.querySelector('.toast-close');
    if (close) close.addEventListener('click', () => {
      toast.style.animation = 'slideOut 0.3s ease forwards';
      setTimeout(() => toast.remove(), 300);
    });
  });
}

// --- Fade-in on Scroll ---
function initFadeAnimations() {
  const els = document.querySelectorAll('.fade-in');
  if (!els.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  els.forEach(el => observer.observe(el));
}

// --- Mobile Nav Toggle ---
function initMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (!toggle || !links) return;
  toggle.addEventListener('click', () => {
    links.classList.toggle('open');
    toggle.textContent = links.classList.contains('open') ? '✕' : '☰';
  });
}

// --- Tab System ---
function initTabs() {
  const btns = document.querySelectorAll('.tab-btn');
  if (!btns.length) return;
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      btns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      const el = document.getElementById(target);
      if (el) el.classList.add('active');
    });
  });
}

// --- Live Search Filter ---
function initSearch() {
  const input = document.getElementById('searchInput');
  if (!input) return;
  let timeout;
  input.addEventListener('input', () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      const q = input.value.toLowerCase().trim();
      document.querySelectorAll('.product-card').forEach(card => {
        const title = (card.querySelector('h3') || {}).textContent || '';
        const desc = (card.querySelector('.desc') || {}).textContent || '';
        const match = title.toLowerCase().includes(q) || desc.toLowerCase().includes(q);
        card.closest('.fade-in').style.display = match ? '' : 'none';
      });
    }, 250);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initToasts();
  initFadeAnimations();
  initMobileNav();
  initTabs();
  initSearch();
  initDarkMode();
  initGamification();
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

// --- Dark Mode Toggle ---
function initDarkMode() {
  const btn = document.getElementById('darkModeToggle');
  if (!btn) return;
  const saved = localStorage.getItem('campusino-theme');
  if (saved === 'dark') document.body.classList.add('dark-mode');
  updateToggleIcon(btn);

  btn.addEventListener('click', () => {
    // Add transition animation
    const overlay = document.createElement('div');
    overlay.className = 'mode-switch-overlay';
    document.body.appendChild(overlay);
    requestAnimationFrame(() => overlay.classList.add('active'));

    setTimeout(() => {
      document.body.classList.toggle('dark-mode');
      const isDark = document.body.classList.contains('dark-mode');
      localStorage.setItem('campusino-theme', isDark ? 'dark' : 'light');
      updateToggleIcon(btn);
      // Award XP for first toggle
      if (!localStorage.getItem('campusino-xp-darkmode')) {
        localStorage.setItem('campusino-xp-darkmode', '1');
        addXP(10, 'Explorer: Tried dark mode!');
      }
    }, 250);

    setTimeout(() => {
      overlay.classList.remove('active');
      setTimeout(() => overlay.remove(), 400);
    }, 500);
  });
}

function updateToggleIcon(btn) {
  const isDark = document.body.classList.contains('dark-mode');
  btn.innerHTML = isDark ? '☀️' : '🌙';
  btn.title = isDark ? 'Switch to light mode' : 'Switch to dark mode';
}

// --- Gamification System ---
function initGamification() {
  updateXPBar();
  trackActions();
}

function getXP() {
  return parseInt(localStorage.getItem('campusino-xp') || '0');
}

function getLevel(xp) {
  if (xp >= 500) return { level: 5, title: 'Campus Legend', next: 999, icon: '👑' };
  if (xp >= 300) return { level: 4, title: 'Power Trader', next: 500, icon: '⚡' };
  if (xp >= 150) return { level: 3, title: 'Active Trader', next: 300, icon: '🔥' };
  if (xp >= 50) return { level: 2, title: 'Rising Star', next: 150, icon: '⭐' };
  return { level: 1, title: 'Newcomer', next: 50, icon: '🌱' };
}

function addXP(amount, reason) {
  const current = getXP();
  const newXP = current + amount;
  const oldLevel = getLevel(current);
  const newLevel = getLevel(newXP);
  localStorage.setItem('campusino-xp', newXP.toString());
  updateXPBar();

  // Show XP toast
  showXPToast('+' + amount + ' XP: ' + reason);

  // Level up notification
  if (newLevel.level > oldLevel.level) {
    setTimeout(() => showXPToast('🎉 Level Up! ' + newLevel.icon + ' ' + newLevel.title), 1500);
  }
}

function showXPToast(msg) {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = 'toast xp-toast';
  toast.innerHTML = msg + '<button class="toast-close">&times;</button>';
  container.appendChild(toast);
  toast.querySelector('.toast-close').addEventListener('click', () => {
    toast.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  });
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

function updateXPBar() {
  const bar = document.getElementById('xpBar');
  const label = document.getElementById('xpLabel');
  const levelBadge = document.getElementById('levelBadge');
  if (!bar) return;

  const xp = getXP();
  const info = getLevel(xp);
  const prevThreshold = info.level === 1 ? 0 : [0, 0, 50, 150, 300, 500][info.level];
  const progress = Math.min(((xp - prevThreshold) / (info.next - prevThreshold)) * 100, 100);

  bar.style.width = progress + '%';
  if (label) label.textContent = xp + ' XP';
  if (levelBadge) levelBadge.textContent = info.icon + ' Lv.' + info.level;
}

function trackActions() {
  // Award XP for visiting pages
  const path = window.location.pathname;
  const visited = JSON.parse(localStorage.getItem('campusino-visited') || '[]');

  if (!visited.includes(path)) {
    visited.push(path);
    localStorage.setItem('campusino-visited', JSON.stringify(visited));
    if (path === '/') addXP(5, 'Browsed marketplace');
    else if (path === '/orders') addXP(5, 'Checked orders');
    else if (path === '/wishlist') addXP(5, 'Viewed wishlist');
    else if (path === '/messages') addXP(5, 'Opened messages');
    else if (path === '/profile') addXP(10, 'Visited profile');
    else if (path.startsWith('/product/')) addXP(3, 'Viewed a product');
  }

  // Streak tracking
  const today = new Date().toDateString();
  const lastVisit = localStorage.getItem('campusino-last-visit');
  const streak = parseInt(localStorage.getItem('campusino-streak') || '0');

  if (lastVisit !== today) {
    localStorage.setItem('campusino-last-visit', today);
    const yesterday = new Date(Date.now() - 86400000).toDateString();
    if (lastVisit === yesterday) {
      localStorage.setItem('campusino-streak', (streak + 1).toString());
      if (streak + 1 > 1) addXP(5, streak + 1 + '-day streak! 🔥');
    } else if (!lastVisit) {
      localStorage.setItem('campusino-streak', '1');
    } else {
      localStorage.setItem('campusino-streak', '1');
    }
  }

  const streakEl = document.getElementById('streakCount');
  if (streakEl) {
    const s = parseInt(localStorage.getItem('campusino-streak') || '1');
    streakEl.textContent = '🔥 ' + s;
  }
}

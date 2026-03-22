// ============================================================
// DesiGrowth — App Utilities (scripts/app.js)
// Shared UI helpers used by all protected pages.
// ============================================================

// ── SVG icon helpers ─────────────────────────────────────────
const _ICONS = {
  home:     `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>`,
  plus:     `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>`,
  chart:    `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`,
  ads:      `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"/></svg>`,
  user:     `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>`,
  logout:   `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>`,
};

const _NAV = [
  { id: 'dashboard', href: './dashboard.html',  icon: _ICONS.home,  label: 'Dashboard'       },
  { id: 'builder',   href: './builder.html',     icon: _ICONS.plus,  label: 'Create Campaign' },
  { id: 'analytics', href: './analytics.html',   icon: _ICONS.chart, label: 'Analytics'       },
  { id: 'ads',       href: './ads.html',          icon: _ICONS.ads,   label: 'Ads Manager'     },
  { id: 'profile',   href: './profile.html',      icon: _ICONS.user,  label: 'Profile'         },
];

// ── Sidebar renderer ─────────────────────────────────────────
function renderSidebar(activePage) {
  const name    = getUserDisplayName();
  const initial = getUserInitial();

  const linkHtml = _NAV.map(l => {
    const active = l.id === activePage;
    const cls = active
      ? 'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm bg-orange-50 text-orange-600 font-semibold'
      : 'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition';
    return `<a href="${l.href}" class="${cls}">${l.icon}<span>${l.label}</span></a>`;
  }).join('');

  // Desktop sidebar
  const sidebarEl = document.getElementById('sidebar');
  if (sidebarEl) {
    sidebarEl.innerHTML = `
      <aside class="hidden lg:flex flex-col w-64 bg-white border-r border-gray-100 fixed h-full z-20">
        <div class="px-6 py-5 border-b border-gray-100">
          <a href="../index.html" class="text-xl font-bold text-orange-500">🌱 DesiGrowth</a>
          <p class="text-xs text-gray-400 mt-0.5">AI Marketing Platform</p>
        </div>
        <nav class="flex-1 p-4 space-y-1 overflow-y-auto">${linkHtml}</nav>
        <div class="p-4 border-t border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 bg-orange-100 rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-orange-600 font-bold text-sm">${initial}</span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-900 truncate">${name}</p>
              <p class="text-xs text-gray-400">Logged in</p>
            </div>
            <button onclick="logout()" title="Logout" class="text-gray-400 hover:text-red-500 transition p-1 rounded-lg hover:bg-red-50">${_ICONS.logout}</button>
          </div>
        </div>
      </aside>`;
  }

  // Mobile top bar
  const mobileNavEl = document.getElementById('mobileNav');
  if (mobileNavEl) {
    const mobileLinks = _NAV.map(l => {
      const active = l.id === activePage;
      const cls = active
        ? 'flex-1 py-2 flex flex-col items-center gap-0.5 text-xs text-orange-500 font-semibold'
        : 'flex-1 py-2 flex flex-col items-center gap-0.5 text-xs text-gray-400 hover:text-gray-600';
      return `<a href="${l.href}" class="${cls}">${l.icon}<span>${l.label.split(' ')[0]}</span></a>`;
    }).join('');

    mobileNavEl.innerHTML = `
      <nav class="lg:hidden fixed top-0 left-0 right-0 bg-white border-b border-gray-100 z-20 px-4 py-3 flex items-center justify-between shadow-sm">
        <a href="../index.html" class="text-lg font-bold text-orange-500">🌱 DesiGrowth</a>
        <div class="flex items-center gap-3">
          <div class="w-7 h-7 bg-orange-100 rounded-full flex items-center justify-center">
            <span class="text-orange-600 font-bold text-xs">${initial}</span>
          </div>
          <button onclick="logout()" class="text-xs text-red-500 font-medium">Logout</button>
        </div>
      </nav>
      <nav class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 z-20 flex shadow-lg">
        ${mobileLinks}
      </nav>`;
  }
}

// ── Toast notification ────────────────────────────────────────
function showToast(message, type = 'success') {
  const colors = { success: 'bg-green-500', error: 'bg-red-500', info: 'bg-blue-500', warning: 'bg-yellow-500' };
  const toast = document.createElement('div');
  toast.className = `fixed top-4 right-4 z-[100] ${colors[type] || colors.success} text-white px-5 py-3 rounded-xl shadow-xl text-sm font-medium max-w-xs`;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.transition = 'opacity 0.3s'; toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 3000);
}

// ── Loading overlay ───────────────────────────────────────────
function showLoading(message = 'Generating your campaign...') {
  if (document.getElementById('_dgLoading')) return;
  const el = document.createElement('div');
  el.id = '_dgLoading';
  el.className = 'fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-[90]';
  el.innerHTML = `
    <div class="bg-white rounded-2xl p-8 shadow-2xl text-center max-w-xs w-full mx-4">
      <div class="relative w-16 h-16 mx-auto mb-5">
        <div class="animate-spin h-16 w-16 border-4 border-orange-200 border-t-orange-500 rounded-full"></div>
        <div class="absolute inset-0 flex items-center justify-center text-2xl">🌱</div>
      </div>
      <h3 class="font-bold text-gray-900 mb-1">AI is Working...</h3>
      <p class="text-gray-500 text-sm">${message}</p>
    </div>`;
  document.body.appendChild(el);
}

function hideLoading() {
  const el = document.getElementById('_dgLoading');
  if (el) el.remove();
}

// ── Date formatter ────────────────────────────────────────────
function formatDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

// ── Status badge helper ───────────────────────────────────────
function statusBadge(status) {
  if (status === 'generated') return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">✓ Generated</span>`;
  if (status === 'draft')     return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700">◷ Draft</span>`;
  return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">${status}</span>`;
}

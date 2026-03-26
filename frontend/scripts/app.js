// ===============================
// GLOBAL UTILITIES
// ===============================

// 📅 Format date
function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
}


// 🏷️ Status badge UI
function statusBadge(status) {
  const map = {
    active: 'bg-green-50 text-green-600 border-green-100',
    paused: 'bg-yellow-50 text-yellow-600 border-yellow-100',
    completed: 'bg-gray-100 text-gray-600 border-gray-200'
  };

  const cls = map[status] || 'bg-gray-100 text-gray-600 border-gray-200';

  return `
    <span class="text-xs font-semibold px-2.5 py-1 rounded-full border ${cls}">
      ${status || 'unknown'}
    </span>
  `;
}


// 👤 Get user name (safe)
function getUserDisplayName() {
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    return user.name || 'User';
  } catch {
    return 'User';
  }
}


// ===============================
// LOADING OVERLAY
// ===============================
function showLoading(text = 'Loading...') {
  let el = document.getElementById('globalLoader');

  if (!el) {
    el = document.createElement('div');
    el.id = 'globalLoader';
    el.className = `
      fixed inset-0 z-50 flex items-center justify-center
      bg-black/30 backdrop-blur-sm
    `;

    el.innerHTML = `
      <div class="bg-white rounded-2xl px-6 py-5 flex items-center gap-3 shadow-lg">
        <svg class="w-5 h-5 animate-spin text-orange-500" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
        </svg>
        <span id="loaderText" class="text-sm text-gray-700 font-medium">${text}</span>
      </div>
    `;

    document.body.appendChild(el);
  } else {
    el.style.display = 'flex';
    document.getElementById('loaderText').textContent = text;
  }
}

function hideLoading() {
  const el = document.getElementById('globalLoader');
  if (el) el.style.display = 'none';
}


// ===============================
// SIDEBAR (DESKTOP)
// ===============================
function renderSidebar(active = '') {
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  sidebar.innerHTML = `
    <aside class="hidden lg:flex fixed left-0 top-0 h-full w-64 bg-white border-r border-gray-100 flex-col justify-between p-5">
      
      <!-- Logo -->
      <div>
        <h1 class="text-xl font-bold text-orange-500 mb-8">DesiGrowth</h1>

        <!-- Nav -->
        <nav class="space-y-2">

          ${navItem('dashboard', 'Dashboard', '/pages/dashboard.html', active)}
          ${navItem('builder', 'Create Campaign', '/pages/builder.html', active)}
          ${navItem('analytics', 'Analytics', '/pages/analytics.html', active)}
         ${navItem('profile', 'Profile', '/pages/profile.html', active)}

        </nav>
      </div>

      <!-- Logout -->
      <button onclick="logout()" class="text-sm text-red-500 hover:text-red-600 font-medium">
        Logout
      </button>

    </aside>
  `;
}


// ===============================
// MOBILE NAV
// ===============================
function renderMobileNav(active = '') {
  const mobile = document.getElementById('mobileNav');
  if (!mobile) return;

  mobile.innerHTML = `
    <div class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 flex justify-around py-2 z-50">

      ${mobileItem('dashboard', '🏠', '/pages/dashboard.html', active)}
      ${mobileItem('builder', '➕', '/pages/builder.html', active)}
      ${mobileItem('analytics', '📊', '/pages/analytics.html', active)}
      ${mobileItem('profile', '👤', '/pages/profile.html', active)}

    </div>
  `;
}


// ===============================
// NAV HELPERS
// ===============================
function navItem(key, label, href, active) {
  const isActive = key === active;

  return `
    <a href="${href}"
      class="block px-4 py-2 rounded-xl text-sm font-medium transition
      ${isActive ? 'bg-orange-50 text-orange-600' : 'text-gray-600 hover:bg-gray-50'}">
      ${label}
    </a>
  `;
}

function mobileItem(key, icon, href, active) {
  const isActive = key === active;

  return `
    <a href="${href}" class="flex flex-col items-center text-xs ${
      isActive ? 'text-orange-500' : 'text-gray-400'
    }">
      <span class="text-lg">${icon}</span>
    </a>
  `;
}


// ===============================
// INIT COMMON UI
// ===============================
document.addEventListener('DOMContentLoaded', () => {
  // render mobile nav automatically
  renderMobileNav();
});
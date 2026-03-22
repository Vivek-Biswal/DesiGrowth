// ============================================================
// DesiGrowth — Auth Module (scripts/auth.js)
// Manages JWT token + user session in localStorage
// ============================================================

const DG_TOKEN_KEY = 'dg_token';
const DG_USER_KEY  = 'dg_user';

function getToken() {
  return localStorage.getItem(DG_TOKEN_KEY);
}

function getUser() {
  try { return JSON.parse(localStorage.getItem(DG_USER_KEY)); }
  catch { return null; }
}

function setAuth(token, user) {
  localStorage.setItem(DG_TOKEN_KEY, token);
  localStorage.setItem(DG_USER_KEY, JSON.stringify(user));
}

function clearAuth() {
  localStorage.removeItem(DG_TOKEN_KEY);
  localStorage.removeItem(DG_USER_KEY);
}

function logout() {
  clearAuth();
  const inPages = window.location.pathname.includes('/pages/');
  window.location.href = inPages ? './login.html' : './pages/login.html';
}

/** Redirect to login if no token. Call at top of every protected page. */
function requireAuth() {
  if (!getToken()) {
    const inPages = window.location.pathname.includes('/pages/');
    window.location.href = inPages ? './login.html' : './pages/login.html';
  }
}

function getUserDisplayName() {
  const u = getUser();
  return u ? (u.name || u.email || 'User') : 'User';
}

function getUserInitial() {
  return getUserDisplayName().charAt(0).toUpperCase();
}

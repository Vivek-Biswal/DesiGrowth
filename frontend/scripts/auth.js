// ===============================
// TOKEN MANAGEMENT
// ===============================

// Save token
function setToken(token) {
  localStorage.setItem('token', token);
}

// Get token
function getToken() {
  return localStorage.getItem('token');
}

// Remove token
function clearToken() {
  localStorage.removeItem('token');
}


// ===============================
// USER MANAGEMENT (optional but useful)
// ===============================

// Save user data
function setUser(user) {
  localStorage.setItem('user', JSON.stringify(user));
}

// Get user data
function getUser() {
  try {
    return JSON.parse(localStorage.getItem('user') || '{}');
  } catch {
    return {};
  }
}

// Clear user
function clearUser() {
  localStorage.removeItem('user');
}


// ===============================
// AUTH GUARD (PROTECT PAGES)
// ===============================
function requireAuth() {
  const token = getToken();

  if (!token) {
    // Not logged in → redirect
    window.location.href = '/pages/login.html';
    return;
  }
}


// ===============================
// OPTIONAL: AUTO VALIDATE TOKEN
// ===============================
async function validateToken() {
  try {
    const res = await api.getUser();
    setUser(res.user); // store fresh user
    return true;
  } catch (err) {
    logout(); // invalid token → logout
    return false;
  }
}


// ===============================
// LOGOUT
// ===============================
function logout() {
  clearToken();
  clearUser();

  // Optional: clear other app data
  localStorage.removeItem('ads');
  localStorage.removeItem('latest_campaign');

  window.location.href = '/pages/login.html';
}


// ===============================
// OPTIONAL: INIT AUTH STATE
// ===============================
async function initAuth() {
  const token = getToken();

  if (!token) return;

  // Try to validate token silently
  await validateToken();
}
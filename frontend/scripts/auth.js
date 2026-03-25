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
// USER MANAGEMENT
// ===============================

// Save user
function setUser(user) {
  localStorage.setItem('user', JSON.stringify(user));
}

// Get user
function getUser() {
  try {
    return JSON.parse(localStorage.getItem('user') || '{}');
  } catch {
    return {};
  }
}

// Remove user
function clearUser() {
  localStorage.removeItem('user');
}


// ===============================
// AUTH CHECK
// ===============================

// Protect pages
function requireAuth() {
  const token = getToken();

  if (!token) {
    window.location.href = '/pages/login.html';
  }
}


// ===============================
// LOGOUT
// ===============================

function logout() {
  clearToken();
  clearUser();

  // optional cleanup
  localStorage.removeItem('latest_campaign');

  window.location.href = '/pages/login.html';
}


// ===============================
// OPTIONAL: AUTO VALIDATE USER
// ===============================

async function validateToken() {
  try {
    const res = await api.getUser();
    setUser(res.user);
    return true;
  } catch (err) {
    logout();
    return false;
  }
}
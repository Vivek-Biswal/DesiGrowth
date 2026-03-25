// ============================================================
// DesiGrowth — Auth Utility (FINAL FIXED)
// ============================================================

// ================= TOKEN =================
function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function removeToken() {
  localStorage.removeItem("token");
}

// ================= AUTH CHECK =================
function isAuthenticated() {
  return !!getToken();
}

// ================= REQUIRE AUTH =================
function requireAuth() {
  if (!isAuthenticated()) {
    window.location.href = "/pages/login.html";
  }
}

// ================= REQUIRE GUEST =================
function requireGuest() {
  if (isAuthenticated()) {
    window.location.href = "/pages/dashboard.html";
  }
}

// ================= LOAD USER =================
async function loadUser() {
  try {
    const res = await window.api.getUser();

    if (res && res.user) {
      const nameEl = document.querySelector("#userName");
      if (nameEl) nameEl.textContent = res.user.name || "User";
    }

  } catch (err) {
    console.error("User load failed:", err);

    // 🔥 IMPORTANT FIX: if token invalid → logout
    logout();
  }
}

// ================= LOGOUT =================
function logout() {
  removeToken();
  window.location.href = "/pages/login.html";
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", () => {

  const path = window.location.pathname;

  // 🔐 Protect dashboard & private pages
  if (path.includes("dashboard") || path.includes("builder") || path.includes("preview")) {
    requireAuth();
    loadUser();
  }

  // 🚫 Prevent logged-in users from accessing login/signup
  if (path.includes("login") || path.includes("signup")) {
    requireGuest();
  }

});

// ================= EXPORT (IMPORTANT) =================
window.auth = {
  getToken,
  setToken,
  removeToken,
  logout
};
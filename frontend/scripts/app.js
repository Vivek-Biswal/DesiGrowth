// ============================================================
// DesiGrowth — Frontend App Logic (FINAL)
// ============================================================

// ================= TOKEN =================
function setToken(token) {
  localStorage.setItem("token", token);
}

function getToken() {
  return localStorage.getItem("token");
}

function removeToken() {
  localStorage.removeItem("token");
}

// ================= LOGIN =================
async function handleLogin(e) {
  e.preventDefault();

  const email = document.querySelector("#email").value;
  const password = document.querySelector("#password").value;

  const errorBox = document.querySelector("#error");
  errorBox.textContent = "";

  try {
    const res = await window.api.login(email, password);

    // save token
    setToken(res.access_token || res.token);

    // redirect
    window.location.href = "/pages/dashboard.html";

  } catch (err) {
    console.error(err);
    errorBox.textContent = err.message || "Login failed";
  }
}

// ================= SIGNUP =================
async function handleSignup(e) {
  e.preventDefault();

  const name = document.querySelector("#name").value;
  const email = document.querySelector("#email").value;
  const password = document.querySelector("#password").value;

  const errorBox = document.querySelector("#error");
  errorBox.textContent = "";

  try {
    await window.api.signup(name, email, password);

    alert("Signup successful! Please login.");
    window.location.href = "/pages/login.html";

  } catch (err) {
    console.error(err);
    errorBox.textContent = err.message || "Signup failed";
  }
}

// ================= AUTH CHECK =================
function requireAuth() {
  if (!getToken()) {
    window.location.href = "/pages/login.html";
  }
}

// ================= LOGOUT =================
function logout() {
  removeToken();
  window.location.href = "/pages/login.html";
}

// ================= AUTO INIT =================
document.addEventListener("DOMContentLoaded", () => {

  // Login page
  const loginForm = document.querySelector("#loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  }

  // Signup page
  const signupForm = document.querySelector("#signupForm");
  if (signupForm) {
    signupForm.addEventListener("submit", handleSignup);
  }

});
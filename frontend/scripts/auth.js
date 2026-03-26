// ===============================
// TOKEN MANAGEMENT
// ===============================
function setToken(token) {
  localStorage.setItem("token", token);
}

function getToken() {
  return localStorage.getItem("token");
}

function clearToken() {
  localStorage.removeItem("token");
}


// ===============================
// USER MANAGEMENT
// ===============================
function setUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

function getUser() {
  try {
    return JSON.parse(localStorage.getItem("user") || "{}");
  } catch {
    return {};
  }
}

function clearUser() {
  localStorage.removeItem("user");
}


// ===============================
// AUTH CHECK
// ===============================
function requireAuth() {
  const token = getToken();

  if (!token) {
    window.location.href = "login.html";
  }
}


// ===============================
// LOGOUT
// ===============================
function logout() {
  clearToken();
  clearUser();
  window.location.href = "login.html";
}


// ===============================
// SIGNUP
// ===============================
async function handleSignup(e) {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await api.signup({ name, email, password });

    setToken(res.data.access_token);
    setUser(res.data.user);

    window.location.href = "dashboard.html";

  } catch (err) {
    showError(err.message);
  }
}


// ===============================
// LOGIN
// ===============================
async function handleLogin(e) {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await api.login({ email, password });

    setToken(res.data.access_token);
    setUser(res.data.user);

    window.location.href = "dashboard.html";

  } catch (err) {
    showError(err.message);
  }
}


// ===============================
// ERROR DISPLAY
// ===============================
function showError(message) {
  const el = document.getElementById("errorBox");
  if (!el) return;

  el.innerText = message;
  el.style.display = "block";
}
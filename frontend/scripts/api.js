// ===============================
// API BASE URL (DEV + PRODUCTION)
// ===============================
const API_BASE =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:5000"
    : "https://desigrowth-2.onrender.com";
    

// ===============================
// TOKEN HANDLING
// ===============================
function getToken() {
  return localStorage.getItem("token");
}

function clearAuth() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}


// ===============================
// GENERIC REQUEST FUNCTION
// ===============================
async function request(path, method = "GET", body = null, auth = false) {
  try {
    const headers = {
      "Content-Type": "application/json"
    };

    // 🔐 Attach token if needed
    if (auth) {
      const token = getToken();
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
    }

    const res = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null
    });

    let data;

    // ✅ Safe JSON parse
    try {
      data = await res.json();
    } catch {
      throw new Error("Invalid server response");
    }

    // 🔴 HANDLE AUTH ERROR (IMPORTANT)
    if (res.status === 401) {
      clearAuth();
      window.location.href = "login.html";
      throw new Error("Session expired. Please login again.");
    }

    // ❌ Other errors
    if (!res.ok) {
      throw new Error(data.message || "Request failed");
    }

    return data;

  } catch (err) {
    console.error("API ERROR:", err.message);
    throw err;
  }
}


// ===============================
// API OBJECT
// ===============================
const api = {

  // 🔐 AUTH
  signup: (payload) =>
    request("/auth/signup", "POST", payload),

  login: (payload) =>
    request("/auth/login", "POST", payload),

  getUser: () =>
    request("/auth/user", "GET", null, true),


  // 📢 CAMPAIGN
  createCampaign: (payload) =>
    request("/campaign/create", "POST", payload, true),

  getCampaigns: () =>
    request("/campaign/all", "GET", null, true),

};


// ===============================
// EXPORT GLOBAL
// ===============================
window.api = api;
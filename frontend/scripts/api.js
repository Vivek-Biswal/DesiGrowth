// ===============================
// API BASE URL (DEV + PRODUCTION)
// ===============================
const API_BASE =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:5000"
    : "https://desigrowth-2.onrender.com";

// ===============================
// HELPER: GET TOKEN
// ===============================
function getToken() {
  return localStorage.getItem("token");
}


// ===============================
// GENERIC REQUEST FUNCTION
// ===============================
async function request(path, method = "GET", body = null, auth = false) {
  try {
    const headers = {
      "Content-Type": "application/json"
    };

    // 🔐 Add token if required
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

    // ⚠️ Handle non-JSON safely
    let data;
    try {
      data = await res.json();
    } catch {
      throw new Error("Invalid server response");
    }

    // ❌ Handle API errors
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
// EXPORT TO GLOBAL (IMPORTANT)
// ===============================
window.api = api;
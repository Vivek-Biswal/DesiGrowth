// ===============================
// API BASE URL (PRODUCTION + LOCAL)
// ===============================
const API_BASE =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:5000"
    : "https://desigrowth-ar7l.onrender.com";


// ===============================
// TOKEN HANDLING
// ===============================
function getToken() {
  return localStorage.getItem("token");
}

function setAuth(data) {
  if (data?.data?.access_token) {
    localStorage.setItem("token", data.data.access_token);
    localStorage.setItem("user", JSON.stringify(data.data.user));
  }
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
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

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
      body: body ? JSON.stringify(body) : null,
      signal: controller.signal
    });

    clearTimeout(timeout);

    let data;
    try {
      data = await res.json();
    } catch {
      throw new Error("Invalid server response");
    }

    // 🔐 Handle expired session
    if (res.status === 401) {
      clearAuth();
      window.location.href = "/pages/login.html";
      throw new Error("Session expired. Please login again.");
    }

    // ❌ Other errors
    if (!res.ok) {
      throw new Error(data.message || data.error || "Request failed");
    }

    return data;

  } catch (err) {
    console.error("❌ API ERROR:", err.message);

    if (err.name === "AbortError") {
      throw new Error("Server timeout. Try again.");
    }

    if (err.message.includes("Failed to fetch")) {
      throw new Error("Cannot connect to server. Check backend or CORS.");
    }

    throw err;
  }
}


// ===============================
// API OBJECT
// ===============================
const api = {

  // 🔐 AUTH
  signup: async (payload) => {
    const res = await request("/auth/signup", "POST", payload);
    setAuth(res);
    return res;
  },

  login: async (payload) => {
    const res = await request("/auth/login", "POST", payload);
    setAuth(res);
    return res;
  },

  getUser: async () => {
    const res = await request("/auth/user", "GET", null, true);
    return res.data.user; // ✅ FIXED
  },


  // 📢 CAMPAIGNS
  createCampaign: (payload) =>
    request("/campaign/create", "POST", payload, true),

  getCampaigns: async () => {
    const res = await request("/campaign/all", "GET", null, true);
    return res.data.campaigns; // ✅ FIXED
  },


  // 📢 ADS
  publishAd: (payload) =>
    request("/ads/publish", "POST", payload, true),

  getAds: async () => {
    const res = await request("/ads/all", "GET", null, true);
    return res.data.ads || [];
  }
};


// ===============================
// EXPORT GLOBAL
// ===============================
window.api = api;
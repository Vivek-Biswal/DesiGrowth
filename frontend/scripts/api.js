// ============================================================
// DesiGrowth — FINAL API CLIENT
// ============================================================

const API_BASE = window.location.hostname === "localhost"
  ? "http://127.0.0.1:5000"
  : "https://desigrowth-2.onrender.com";

// ================= TOKEN =================
function getToken() {
  return localStorage.getItem("token");
}

// ================= FETCH =================
async function _fetch(path, options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {})
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const res = await fetch(API_BASE + path, {
      ...options,
      headers
    });

    const text = await res.text();

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error("Invalid server response");
    }

    if (!res.ok) {
      throw new Error(data.error || "Request failed");
    }

    return data;

  } catch (err) {
    console.error("API ERROR:", err);
    throw err;
  }
}

// ================= API =================
const api = {

  // AUTH
  async login(email, password) {
    return _fetch("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
  },

  async signup(name, email, password) {
    return _fetch("/auth/signup", {
      method: "POST",
      body: JSON.stringify({ name, email, password })
    });
  },

  async getUser() {
    return _fetch("/auth/user");
  },

  // CAMPAIGNS
  async createCampaign(data) {
    return _fetch("/campaign/create", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },

  async getCampaigns() {
    return _fetch("/campaign/all");
  },

  async getCampaign(id) {
    return _fetch(`/campaign/${id}`);
  },

  // AI
  async generateAI(data) {
    return _fetch("/ai/generate", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }
};

// ================= EXPORT =================
window.api = api;
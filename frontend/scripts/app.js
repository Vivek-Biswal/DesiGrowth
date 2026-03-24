// ============================================================
// DesiGrowth — API Client (FINAL FIXED VERSION)
// ============================================================

// ✅ Correct backend URL (auto switch local + production)
const API_BASE = window.location.hostname === "localhost"
  ? "http://127.0.0.1:5000"
  : "https://desigrowth.onrender.com";

// ============================================================
// Helper: Get Token
// ============================================================
function getToken() {
  return localStorage.getItem("token");
}

// ============================================================
// Internal Fetch Helper
// ============================================================
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

// ============================================================
// API METHODS
// ============================================================
const api = {

  // 🔐 AUTH
  async login(email, password) {
    return _fetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  },

  async signup(name, email, password) {
    return _fetch('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ name, email, password })
    });
  },

  async getUser() {
    return _fetch('/auth/user');
  },

  // 📊 CAMPAIGNS
  async createCampaign(data) {
    return _fetch('/campaign/create', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  async getCampaigns() {
    return _fetch('/campaign/all');
  },

  async getCampaign(id) {
    return _fetch(`/campaign/${id}`);
  },

  // 🤖 AI
  async generateAI(data) {
    return _fetch('/ai/generate', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
};

// ============================================================
// Export globally
// ============================================================
window.api = api;
// ============================================================
// DesiGrowth API Layer
// Handles all backend communication
// ============================================================

// 🔥 Dynamic API base (LOCAL + PRODUCTION)
const API_BASE = window.location.hostname === "localhost"
  ? "http://127.0.0.1:5000"
  : "https://desigrowth.onrender.com";  // ✅ correct URL

// ============================================================
// Helper: Get Auth Token
// ============================================================
function getToken() {
  return localStorage.getItem("token");
}

// ============================================================
// Helper: Request Wrapper
// ============================================================
async function request(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...(getToken() && { Authorization: `Bearer ${getToken()}` })
      },
      ...options
    });

    // 🔥 Handle non-JSON safely
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
// Auth APIs
// ============================================================
const api = {

  async signup(name, email, password) {
    return request("/auth/signup", {
      method: "POST",
      body: JSON.stringify({ name, email, password })
    });
  },

  async login(email, password) {
    return request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
  },

  async getUser() {
    return request("/auth/user");
  },

  // ============================================================
  // Campaign APIs
  // ============================================================

  async createCampaign(data) {
    return request("/campaign/create", {
      method: "POST",
      body: JSON.stringify(data)
    });
  },

  async getCampaigns() {
    return request("/campaign/all");
  },

  async getCampaign(id) {
    return request(`/campaign/${id}`);
  },

  // ============================================================
  // AI APIs
  // ============================================================

  async generateAI(data) {
    return request("/ai/generate", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }

};

// ============================================================
// Export (global)
// ============================================================
window.api = api;
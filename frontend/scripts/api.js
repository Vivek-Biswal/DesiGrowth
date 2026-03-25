// ===============================
// API BASE URL
// ===============================
const API_BASE = 'http://127.0.0.1:5000';


// ===============================
// HELPER: HEADERS
// ===============================
function getHeaders(auth = true) {
  const headers = {
    'Content-Type': 'application/json'
  };

  if (auth) {
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  return headers;
}


// ===============================
// HELPER: HANDLE RESPONSE
// ===============================
async function handleResponse(res) {
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.message || data.error || 'Something went wrong');
  }

  return data;
}


// ===============================
// API OBJECT
// ===============================
const api = {

  // =========================
  // 🔐 AUTH
  // =========================

  async login(email, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: getHeaders(false),
      body: JSON.stringify({ email, password })
    });

    return handleResponse(res);
  },

  async signup(name, email, password) {
    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: 'POST',
      headers: getHeaders(false),
      body: JSON.stringify({ name, email, password })
    });

    return handleResponse(res);
  },

  async getUser() {
    const res = await fetch(`${API_BASE}/auth/user`, {
      method: 'GET',
      headers: getHeaders(true)
    });

    return handleResponse(res);
  },


  // =========================
  // 📢 CAMPAIGNS
  // =========================

  async getCampaigns() {
    const res = await fetch(`${API_BASE}/campaign/all`, {
      method: 'GET',
      headers: getHeaders(true)
    });

    return handleResponse(res);
  },

  async createCampaign(data) {
    const res = await fetch(`${API_BASE}/campaign/create`, {
      method: 'POST',
      headers: getHeaders(true),
      body: JSON.stringify(data)
    });

    return handleResponse(res);
  },


  // =========================
  // 🤖 AI GENERATION
  // =========================

  async generateAI(data) {
    const res = await fetch(`${API_BASE}/ai/generate`, {
      method: 'POST',
      headers: getHeaders(true),
      body: JSON.stringify(data)
    });

    return handleResponse(res);
  }

};
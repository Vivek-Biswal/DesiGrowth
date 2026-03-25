// ===============================
// API BASE URL
// ===============================
const API_BASE = 'http://127.0.0.1:5000'; // change if deployed


// ===============================
// HELPER: GET HEADERS WITH TOKEN
// ===============================
function getHeaders(isAuthRequired = true) {
  const headers = {
    'Content-Type': 'application/json'
  };

  if (isAuthRequired) {
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
  let data;

  try {
    data = await res.json();
  } catch {
    throw new Error('Invalid server response');
  }

  if (!res.ok) {
    throw new Error(data.message || 'Something went wrong');
  }

  return data;
}


// ===============================
// AUTH APIs
// ===============================
const api = {

  // 🔐 LOGIN
  async login(email, password) {
    const res = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: getHeaders(false), // no token needed
      body: JSON.stringify({ email, password })
    });

    return handleResponse(res);
  },


  // 📝 SIGNUP
  async signup(name, email, password) {
    const res = await fetch(`${API_BASE}/signup`, {
      method: 'POST',
      headers: getHeaders(false),
      body: JSON.stringify({ name, email, password })
    });

    return handleResponse(res);
  },


  // 👤 GET USER PROFILE
  async getUser() {
    const res = await fetch(`${API_BASE}/user`, {
      method: 'GET',
      headers: getHeaders(true)
    });

    return handleResponse(res);
  },


  // ===============================
  // CAMPAIGN APIs
  // ===============================

  // 📦 GET ALL CAMPAIGNS
  async getCampaigns() {
    const res = await fetch(`${API_BASE}/campaigns`, {
      method: 'GET',
      headers: getHeaders(true)
    });

    return handleResponse(res);
  },


  // 🚀 CREATE CAMPAIGN
  async createCampaign(data) {
    const res = await fetch(`${API_BASE}/campaigns`, {
      method: 'POST',
      headers: getHeaders(true),
      body: JSON.stringify(data)
    });

    return handleResponse(res);
  },


  // ❌ DELETE CAMPAIGN (optional)
  async deleteCampaign(id) {
    const res = await fetch(`${API_BASE}/campaigns/${id}`, {
      method: 'DELETE',
      headers: getHeaders(true)
    });

    return handleResponse(res);
  }

};
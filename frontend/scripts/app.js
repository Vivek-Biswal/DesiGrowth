// ============================================================
// DesiGrowth — API Client (scripts/api.js)
// Single source of truth for all backend calls.
// Uses mock data automatically when no token is present.
// To switch backend: change API_BASE below.
// ============================================================

const API_BASE = 'https://desigrowth-2.onrender.com';

// ── Mock data ────────────────────────────────────────────────
const _MOCK = {
  user: { id: 'demo001', name: 'Ramesh Sharma', email: 'ramesh@example.com', provider: 'email', created_at: new Date().toISOString() },
  campaigns: [
    {
      id: 'c001', business: 'Sharma Grocery', product: 'Premium Basmati Rice', offer: '20% OFF',
      festival: 'Diwali', location: 'Delhi', status: 'generated',
      caption: '🎉 Celebrate Diwali with the finest Basmati Rice! Sharma Grocery brings you 20% OFF — limited time only. Visit us today!',
      hashtags: '#diwali #sale #rice #delhi #discount',
      poster_url: null, created_at: new Date(Date.now() - 86400000).toISOString()
    },
    {
      id: 'c002', business: 'City Electronics', product: 'Bluetooth Speaker', offer: '15% OFF',
      festival: 'New Year', location: 'Mumbai', status: 'generated',
      caption: '🎆 Ring in the New Year with booming sound! City Electronics offers 15% OFF on all Bluetooth Speakers. Grab yours now!',
      hashtags: '#newyear #electronics #sale #mumbai #offer',
      poster_url: null, created_at: new Date(Date.now() - 172800000).toISOString()
    },
    {
      id: 'c003', business: 'Fresh Mart', product: 'Organic Vegetables', offer: '10% OFF',
      festival: 'Weekend Sale', location: 'Bangalore', status: 'draft',
      caption: '🥦 Stay healthy this weekend! Fresh Mart brings you farm-fresh Organic Vegetables at 10% OFF. Limited stock!',
      hashtags: '#organic #vegetables #bangalore #healthy #sale',
      poster_url: null, created_at: new Date(Date.now() - 259200000).toISOString()
    }
  ]
};

// ── Internal fetch helper ────────────────────────────────────
async function _fetch(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(API_BASE + path, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
    throw new Error(err.error || `Request failed (${res.status})`);
  }
  return res.json();
}

// ── API object ───────────────────────────────────────────────
const api = {

  /** POST /login */
  async login(email, password) {
    return _fetch('/login', { method: 'POST', body: JSON.stringify({ email, password }) });
  },

  /** POST /signup */
  async signup(name, email, password) {
    return _fetch('/signup', { method: 'POST', body: JSON.stringify({ name, email, password }) });
  },

  /** GET /user */
  async getUser() {
    if (!getToken()) return { status: 'success', user: _MOCK.user };
    try { return await _fetch('/user'); }
    catch { return { status: 'success', user: _MOCK.user }; }
  },

  /** GET /campaigns */
  async getCampaigns() {
    if (!getToken()) return { status: 'success', campaigns: _MOCK.campaigns, count: _MOCK.campaigns.length };
    try { return await _fetch('/campaigns'); }
    catch { return { status: 'success', campaigns: _MOCK.campaigns, count: _MOCK.campaigns.length }; }
  },

  /** POST /campaign/create — saves to DB, generates poster (JWT required) */
  async createCampaign(data) {
    if (!getToken()) {
      await new Promise(r => setTimeout(r, 1800));
      return {
        status: 'success',
        campaign: {
          id: 'demo_' + Date.now(),
          ...data,
          caption: `🎉 ${data.business} is offering ${data.offer} on ${data.product}${data.festival ? ' this ' + data.festival : ''}! Don't miss out — visit us${data.location ? ' in ' + data.location : ''} today.`,
          hashtags: '#sale #offer #localbusiness #india #smallbusiness',
          poster_url: null,
          status: 'generated',
          created_at: new Date().toISOString()
        }
      };
    }
    return _fetch('/campaign/create', { method: 'POST', body: JSON.stringify(data) });
  },

  /** POST /generate-campaign — legacy no-auth endpoint */
  async generateCampaignLegacy(data) {
    const res = await fetch(API_BASE + '/generate-campaign', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  }
};

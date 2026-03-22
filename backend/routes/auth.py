"""
routes/auth.py
--------------
Authentication routes:
  POST /signup              - Register with email + password
  POST /login               - Login with email + password
  GET  /auth/google         - Start Google OAuth flow
  GET  /auth/google/callback - Handle Google OAuth callback
  GET  /user                - Get current user profile (JWT required)
"""

import email
import uuid
from datetime import datetime, timezone

import bcrypt
from authlib.integrations.requests_client import OAuth2Session
from flask import Blueprint, current_app, jsonify, redirect, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from models.db import Query, get_users_table
from utils.helpers import error, require_fields, success

auth_bp = Blueprint("auth", __name__)

# ──────────────────────────────────────────────
# GOOGLE OAUTH CONSTANTS
# ──────────────────────────────────────────────
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_SCOPE = "openid email profile"


# ──────────────────────────────────────────────
# POST /signup
# ──────────────────────────────────────────────
@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    Register a new user with email and password.

    Request body:
        { "name": "...", "email": "...", "password": "..." }

    Response (201):
        { "status": "success", "token": "...", "user": { id, name, email, created_at } }
    """
    data = request.get_json()
    err, code = require_fields(data, ["name", "email", "password"])
    if err:
        return err, code

    users = get_users_table()
    User = Query()

    # Check duplicate email
    if users.search(User.email == data["email"].lower()):
        return error("An account with this email already exists.", 409)

    # Hash password
    hashed_pw = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    user = {
        "id": uuid.uuid4().hex,
        "name": data["name"].strip(),
        "email": data["email"].lower().strip(),
        "password": hashed_pw,
        "provider": "email",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    users.insert(user)

    token = create_access_token(identity=user["id"])
    return success(
        {
            "token": token,
            "user": _safe_user(user),
        },
        201,
    )


# ──────────────────────────────────────────────
# POST /login
# ──────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login with email and password.

    Request body:
        { "email": "...", "password": "..." }

    Response (200):
        { "status": "success", "token": "...", "user": { id, name, email, created_at } }
    """
    data = request.get_json()
    err, code = require_fields(data, ["email", "password"])
    if err:
        return err, code

    users = get_users_table()
    User = Query()

    email = data["email"].lower().strip()
    results = users.search(User.email == email)
    if not results:
        return error("Invalid email or password.", 401)

    user = results[0]

    # Google-only accounts have no password
    if user.get("provider") == "google":
        return error("This account uses Google login. Please sign in with Google.", 401)

    if not bcrypt.checkpw(
        data["password"].encode("utf-8"), user["password"].encode("utf-8")
    ):
        return error("Invalid email or password.", 401)

    token = create_access_token(identity=user["id"])
    return success({"token": token, "user": _safe_user(user)})


# ──────────────────────────────────────────────
# GET /auth/google
# ──────────────────────────────────────────────
@auth_bp.route("/auth/google")
def google_login():
    """
    Redirect the user to Google's OAuth consent screen.
    The frontend should open this URL in a browser window/tab.
    """
    cfg = current_app.config
    client_id = cfg["GOOGLE_CLIENT_ID"]
    redirect_uri = cfg["GOOGLE_REDIRECT_URI"]

    if not client_id or client_id == "your_google_client_id_here":
        return error(
            "Google OAuth is not configured. Set GOOGLE_CLIENT_ID in .env.", 503
        )

    oauth = OAuth2Session(client_id, scope=GOOGLE_SCOPE, redirect_uri=redirect_uri)
    auth_url, _ = oauth.create_authorization_url(
        GOOGLE_AUTH_URL, access_type="offline", prompt="select_account"
    )
    return redirect(auth_url)


# ──────────────────────────────────────────────
# GET /auth/google/callback
# ──────────────────────────────────────────────
@auth_bp.route("/auth/google/callback")
def google_callback():
    """
    Handle the redirect back from Google.
    Fetches user info, creates account if new, returns JWT.

    Response (200):
        { "status": "success", "token": "...", "user": { id, name, email, created_at } }
    """
    cfg = current_app.config
    client_id = cfg["GOOGLE_CLIENT_ID"]
    client_secret = cfg["GOOGLE_CLIENT_SECRET"]
    redirect_uri = cfg["GOOGLE_REDIRECT_URI"]

    oauth = OAuth2Session(client_id, scope=GOOGLE_SCOPE, redirect_uri=redirect_uri)

    # Exchange code for access token
    token = oauth.fetch_token(
        GOOGLE_TOKEN_URL,
        authorization_response=request.url,
        client_secret=client_secret,
    )

    # Get Google user info
    resp = oauth.get(GOOGLE_USERINFO_URL)
    google_user = resp.json()

    email = google_user.get("email", "").lower()
    name = google_user.get("name", email)
    google_id = google_user.get("sub", "")

    if not email:
        return error("Could not retrieve email from Google.", 400)

    users = get_users_table()
    User = Query()
    results = users.search(User.email == email)

    if results:
        user = results[0]
    else:
        user = {
            "id": uuid.uuid4().hex,
            "name": name,
            "email": email,
            "password": None,
            "provider": "google",
            "google_id": google_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        users.insert(user)

    jwt_token = create_access_token(identity=user["id"])
    return success({"token": jwt_token, "user": _safe_user(user)})


# ──────────────────────────────────────────────
# GET /user
# ──────────────────────────────────────────────
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    """
    Get the currently logged-in user's profile.

    Headers:
        Authorization: Bearer <token>

    Response (200):
        { "status": "success", "user": { id, name, email, provider, created_at } }
    """
    user_id = get_jwt_identity()
    users = get_users_table()
    User = Query()

    results = users.search(User.id == user_id)
    if not results:
        return error("User not found.", 404)

    return success({"user": _safe_user(results[0])})


# ──────────────────────────────────────────────
# HELPER
# ──────────────────────────────────────────────
def _safe_user(user: dict) -> dict:
    """Return user dict without sensitive fields (password, google_id)."""
    return {
        "id": user.get("id"),
        "name": user.get("name"),
        "email": user.get("email"),
        "provider": user.get("provider", "email"),
        "created_at": user.get("created_at"),
    }

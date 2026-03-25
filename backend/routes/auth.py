from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from tinydb import Query
from datetime import datetime

from backend.models.db import get_db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

User = Query()


# =========================
# 🔐 SIGNUP
# =========================
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    db = get_db()

    # ✅ Validation
    if not data or not data.get("email") or not data.get("password") or not data.get("name"):
        return jsonify({"error": "Missing required fields"}), 400

    # ✅ Check if user exists
    if db.search(User.email == data["email"]):
        return jsonify({"error": "User already exists"}), 400

    # ✅ Create user
    user = {
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"]),
        "created_at": datetime.utcnow().isoformat()
    }

    db.insert(user)

    # ✅ Generate token (IMPORTANT FIX)
    token = create_access_token(identity=data["email"])

    return jsonify({
        "status": "success",
        "access_token": token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }), 201


# =========================
# 🔐 LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    db = get_db()

    # ✅ Validation
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    # ✅ Find user
    user = db.get(User.email == data["email"])

    # ❌ Invalid credentials
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ Generate token
    token = create_access_token(identity=user["email"])

    return jsonify({
        "status": "success",
        "access_token": token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }), 200


# =========================
# 👤 GET USER (PROTECTED)
# =========================
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    db = get_db()
    email = get_jwt_identity()

    user = db.get(User.email == email)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "status": "success",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "created_at": user.get("created_at")
        }
    }), 200


# =========================
# 🧪 DEBUG ROUTE (OPTIONAL)
# =========================
@auth_bp.route("/test", methods=["GET"])
def test():
    return jsonify({
        "status": "success",
        "message": "Auth route working 🚀"
    })
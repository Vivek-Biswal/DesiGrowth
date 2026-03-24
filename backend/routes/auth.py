from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from tinydb import Query

from backend.models.db import get_db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

User = Query()


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    db = get_db()

    # ✅ validation
    if not data or not data.get("email") or not data.get("password") or not data.get("name"):
        return jsonify({"error": "Missing required fields"}), 400

    if db.search(User.email == data["email"]):
        return jsonify({"error": "User already exists"}), 400

    user = {
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }

    db.insert(user)

    return jsonify({"status": "success"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()

    # ✅ validation
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    user = db.get(User.email == data["email"])

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user["email"])

    return jsonify({
        "status": "success",
        "access_token": token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    })


@auth_bp.route("/user", methods=["GET"])
@jwt_required()   # ✅ IMPORTANT FIX
def get_user():
    db = get_db()
    email = get_jwt_identity()

    user = db.get(User.email == email)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    })
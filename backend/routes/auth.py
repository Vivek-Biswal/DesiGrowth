from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from tinydb import Query

# ✅ FIXED IMPORT
from backend.models.db import get_db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

User = Query()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    db = get_db()

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

    user = db.get(User.email == data["email"])

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user["email"])

    return jsonify({
        "status": "success",
        "access_token": token
    })


@auth_bp.route("/user", methods=["GET"])
def get_user():
    return jsonify({
        "user": {
            "name": "Demo User"
        }
    })
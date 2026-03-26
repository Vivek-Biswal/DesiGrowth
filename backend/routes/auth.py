from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson import ObjectId

from backend.models.db import users
from backend.utils.helpers import require_fields, success, error


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ===============================
# 🔹 SIGNUP
# ===============================
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    err, code = require_fields(data, ["name", "email", "password"])
    if err:
        return err, code

    name = data["name"]
    email = data["email"]
    password = data["password"]

    # Check existing user
    if users.find_one({"email": email}):
        return error("Email already registered", 400)

    # Hash password
    hashed_password = generate_password_hash(password)

    # Create user
    user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }

    result = users.insert_one(user)

    # Create JWT token
    access_token = create_access_token(identity=str(result.inserted_id))

    return success({
        "access_token": access_token,
        "user": {
            "id": str(result.inserted_id),
            "name": name,
            "email": email
        }
    }, message="User created successfully")


# ===============================
# 🔹 LOGIN
# ===============================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    print("LOGIN DATA:", data)  # DEBUG

    err, code = require_fields(data, ["email", "password"])
    if err:
        return err, code

    email = data["email"]
    password = data["password"]

    user = users.find_one({"email": email})

    if not user:
        return error("Invalid credentials", 401)

    if not check_password_hash(user["password"], password):
        return error("Invalid credentials", 401)

    access_token = create_access_token(identity=str(user["_id"]))

    return success({
        "access_token": access_token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }, message="Login successful")


# ===============================
# 🔹 GET CURRENT USER
# ===============================
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()

    user = users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return error("User not found", 404)

    return success({
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "created_at": str(user.get("created_at"))  # IMPORTANT FIX
        }
    })
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from backend.models.db import users
from backend.utils.helpers import require_fields, success, error

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# 🔹 SIGNUP
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Validate fields
    err, code = require_fields(data, ["name", "email", "password"])
    if err:
        return err, code

    name = data["name"]
    email = data["email"]
    password = data["password"]

    # Check if user already exists
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

    return success({
        "message": "User created successfully",
        "user_id": str(result.inserted_id)
    })


# 🔹 LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Validate fields
    err, code = require_fields(data, ["email", "password"])
    if err:
        return err, code

    email = data["email"]
    password = data["password"]

    # Find user
    user = users.find_one({"email": email})

    if not user:
        return error("Invalid credentials", 401)

    # Check password
    if not check_password_hash(user["password"], password):
        return error("Invalid credentials", 401)

    # Generate JWT token
    access_token = create_access_token(identity=str(user["_id"]))

    return success({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    })
from flask import jsonify


# ===============================
# ✅ SUCCESS RESPONSE
# ===============================
def success(data=None, message="Success", code=200):
    response = {
        "status": "success",
        "message": message,
        "data": data or {}
    }
    return jsonify(response), code


# ===============================
# ❌ ERROR RESPONSE
# ===============================
def error(message="Something went wrong", code=400):
    response = {
        "status": "error",
        "message": message
    }
    return jsonify(response), code


# ===============================
# 🔍 REQUIRED FIELDS VALIDATION
# ===============================
def require_fields(data, fields):
    # Check if body exists
    if not data:
        return error("Missing JSON body"), 400

    # Check required fields
    for field in fields:
        if field not in data or data[field] == "":
            return error(f"{field} is required"), 400

    return None, None
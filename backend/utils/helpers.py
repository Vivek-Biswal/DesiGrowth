"""
utils/helpers.py
----------------
Shared utility functions used across routes.
"""

from flask import jsonify


def require_fields(data: dict, fields: list):
    """
    Validate required fields in request data.
    Returns (None, None) if valid, else (error_response, status_code)
    """

    if not data:
        return error("Request body must be JSON"), 400

    for field in fields:
        value = data.get(field)

        # Check missing or empty
        if value is None or str(value).strip() == "":
            return error(f"'{field}' is required"), 400

    return None, None


def success(data: dict = None, status: int = 200):
    """
    Standard success response
    """
    response = {"status": "success"}

    if data:
        response.update(data)

    return jsonify(response), status


def error(message: str, status: int = 400):
    """
    Standard error response
    """
    return jsonify({
        "status": "error",
        "message": message
    }), status
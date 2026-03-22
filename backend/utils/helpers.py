"""
utils/helpers.py
----------------
Shared utility functions used across routes.
"""

from flask import request, jsonify


def require_fields(data: dict, fields: list):
    """
    Check that all required fields exist and are non-empty in a dict.
    Returns (None, None) if OK, or (error_response, 400) if a field is missing.

    Usage:
        data = request.get_json()
        err, code = require_fields(data, ["email", "password"])
        if err:
            return err, code
    """
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    for field in fields:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    return None, None


def success(data: dict, status: int = 200):
    """Return a standard success JSON response."""
    return jsonify({"status": "success", **data}), status


def error(message: str, status: int = 400):
    """Return a standard error JSON response."""
    return jsonify({"status": "error", "error": message}), status

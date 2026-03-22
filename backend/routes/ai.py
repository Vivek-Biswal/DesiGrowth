"""
routes/ai.py
------------
AI content generation route:
  POST /generate-content  - Generate marketing caption, hashtags, and campaign idea
"""

import os
import sys

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

# Allow importing ai_module from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ai_module.ai_generator import generate_marketing_content

from utils.helpers import error, require_fields, success

ai_bp = Blueprint("ai", __name__)


# ──────────────────────────────────────────────
# POST /generate-content
# ──────────────────────────────────────────────
@ai_bp.route("/generate-content", methods=["POST"])
@jwt_required()
def generate_content():
    """
    Generate AI marketing content for a product.
    This is the clean endpoint for Member 3 (AI Engine) to extend.

    Headers:
        Authorization: Bearer <token>

    Request body:
        {
            "product":       "Shirt",
            "offer":         "50% OFF",
            "business_type": "Clothing Store",
            "festival":      "Diwali",      (optional)
            "location":      "Mumbai"        (optional)
        }

    Response (200):
        {
            "status":   "success",
            "caption":  "Shop our stunning Diwali collection...",
            "hashtags": ["#diwali", "#sale", "#fashion", "#offer", "#clothing"],
            "idea":     "Run a 3-day flash sale with WhatsApp broadcast..."
        }
    """
    data = request.get_json()
    err, code = require_fields(data, ["product", "offer", "business_type"])
    if err:
        return err, code

    product = data["product"]
    offer = data["offer"]
    business_type = data["business_type"]
    festival = data.get("festival", "")
    location = data.get("location", "")

    # Call ai_module — passes business_type as both business name and type context
    result = generate_marketing_content(
        business=business_type,
        product=product,
        offer=offer,
        festival=festival,
        location=location,
    )

    # Parse hashtags into a list if it's a string
    raw_hashtags = result.get("hashtags", "")
    if isinstance(raw_hashtags, str):
        hashtag_list = [
            tag.strip() for tag in raw_hashtags.split() if tag.startswith("#")
        ]
    else:
        hashtag_list = raw_hashtags

    return success(
        {
            "caption": result.get("caption", ""),
            "hashtags": hashtag_list,
            "idea": result.get("idea", result.get("cta", "Visit our store today!")),
        }
    )

"""
routes/campaign.py
------------------
Campaign routes (all require a valid JWT token):
  POST /campaign/create       - Generate AI content + poster, save campaign
  GET  /campaigns             - List all campaigns for the current user
  GET  /campaign/<id>         - Get a single campaign by ID
"""

import os
import uuid
from datetime import datetime, timezone

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from PIL import Image, ImageDraw, ImageFont

from models.db import Query, get_campaigns_table

# Allow importing ai_module from the project root
from ai_module.ai_generator import generate_marketing_content

from utils.helpers import error, require_fields, success

campaign_bp = Blueprint("campaign", __name__)


# ──────────────────────────────────────────────
# POST /campaign/create
# ──────────────────────────────────────────────
@campaign_bp.route("/campaign/create", methods=["POST"])
@jwt_required()
def create_campaign():
    """
    Create a new campaign: runs AI generation + poster creation, saves to DB.

    Headers:
        Authorization: Bearer <token>

    Request body:
        {
            "business":  "Sharma Grocery",
            "product":   "Premium Rice",
            "offer":     "20% OFF",
            "festival":  "Diwali",       (optional)
            "location":  "Delhi"          (optional)
        }

    Response (201):
        {
            "status": "success",
            "campaign": {
                "id", "user_id", "business", "product", "offer",
                "festival", "location", "caption", "hashtags",
                "poster_url", "status", "created_at"
            }
        }
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    err, code = require_fields(data, ["business", "product", "offer"])
    if err:
        return err, code

    business = data["business"]
    product = data["product"]
    offer = data["offer"]
    festival = data.get("festival", "")
    location = data.get("location", "")

    # ── AI content ──
    ai_result = generate_marketing_content(business, product, offer, festival, location)
    caption = ai_result.get("caption", "")
    hashtags = ai_result.get("hashtags", "")
    if isinstance(hashtags, str):
        hashtags = [tag.strip() for tag in hashtags.split() if tag.startswith("#")]

    # ── Poster ──
    poster_filename = _create_poster(business, product, offer, current_app)
    poster_url = request.host_url.rstrip("/") + "/poster/" + poster_filename

    # ── Save to DB ──
    campaign = {
        "id": uuid.uuid4().hex,
        "user_id": user_id,
        "business": business,
        "product": product,
        "offer": offer,
        "festival": festival,
        "location": location,
        "caption": caption,
        "hashtags": hashtags,
        "poster_url": poster_url,
        "status": "generated",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    get_campaigns_table().insert(campaign)

    return success({"campaign": campaign}, 201)


# ──────────────────────────────────────────────
# GET /campaigns
# ──────────────────────────────────────────────
@campaign_bp.route("/campaigns", methods=["GET"])
@jwt_required()
def list_campaigns():
    """
    Return all campaigns belonging to the current user, newest first.

    Headers:
        Authorization: Bearer <token>

    Response (200):
        { "status": "success", "campaigns": [ ...campaign objects... ] }
    """
    user_id = get_jwt_identity()
    Campaign = Query()

    campaigns = get_campaigns_table().search(Campaign.user_id == user_id)

    # Sort newest first
    campaigns.sort(key=lambda c: c.get("created_at", ""), reverse=True)

    return success({"campaigns": campaigns, "count": len(campaigns)})


# ──────────────────────────────────────────────
# GET /campaign/<id>
# ──────────────────────────────────────────────
@campaign_bp.route("/campaign/<campaign_id>", methods=["GET"])
@jwt_required()
def get_campaign(campaign_id):
    """
    Return a single campaign by ID.
    Only the owner can access their campaign.

    Headers:
        Authorization: Bearer <token>

    Response (200):
        { "status": "success", "campaign": { ...campaign object... } }
    """
    user_id = get_jwt_identity()
    Campaign = Query()

    results = get_campaigns_table().search(
        (Campaign.id == campaign_id) & (Campaign.user_id == user_id)
    )

    if not results:
        return error("Campaign not found.", 404)

    return success({"campaign": results[0]})


# ──────────────────────────────────────────────
# INTERNAL: Poster creator
# ──────────────────────────────────────────────
def _create_poster(business: str, product: str, offer: str, app) -> str:
    """Generate a simple marketing poster using Pillow. Returns filename."""
    poster_folder = app.config["POSTER_FOLDER"]
    os.makedirs(poster_folder, exist_ok=True)

    width, height = 800, 800
    img = Image.new("RGB", (width, height), (255, 245, 230))
    draw = ImageDraw.Draw(img)

    # Gradient-style background stripe
    draw.rectangle([0, 0, width, 140], fill=(255, 102, 0))

    try:
        font_large = ImageFont.truetype("arial.ttf", 56)
        font_medium = ImageFont.truetype("arial.ttf", 38)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        font_large = font_medium = font_small = ImageFont.load_default()

    # Business name (white on orange header)
    draw.text((40, 40), business, fill="white", font=font_large)

    # Product
    draw.text((40, 200), f"🛍  {product}", fill="#333333", font=font_medium)

    # Offer (prominent)
    draw.rectangle([30, 290, 770, 380], fill=(255, 230, 200))
    draw.text((50, 305), f"🎉  {offer}", fill=(200, 0, 0), font=font_large)

    # Footer
    draw.rectangle([0, 720, width, height], fill=(50, 50, 50))
    draw.text((40, 745), "Powered by DesiGrowth", fill="white", font=font_small)

    filename = f"poster_{uuid.uuid4().hex}.png"
    img.save(os.path.join(poster_folder, filename))

    return filename

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from backend.models.db import campaigns
from backend.utils.helpers import require_fields, success, error

# ✅ Correct imports
from backend.ai_module.ai_generator import generate_content
from backend.poster_engine.poster_generator import generate_poster

campaign_bp = Blueprint("campaign", __name__, url_prefix="/campaign")


# 🔹 CREATE CAMPAIGN
@campaign_bp.route("/create", methods=["POST"])
@jwt_required()
def create_campaign():
    data = request.get_json()

    err, code = require_fields(data, ["business", "product", "offer"])
    if err:
        return err, code

    user_id = get_jwt_identity()

    business = data["business"]
    product = data["product"]
    offer = data["offer"]

    # 🔥 STEP 1: AI GENERATION
    ai_result = generate_content(business, product, offer)

    caption = ai_result.get("caption", "")
    hashtags = ai_result.get("hashtags", [])

    # 🔥 STEP 2: POSTER GENERATION (FIXED)
    poster_path = generate_poster(
        business,
        product,
        offer,
        caption,
        image_path=None  # you are not using image yet
    )

    campaign = {
        "user_id": user_id,
        "business": business,
        "product": product,
        "offer": offer,
        "caption": caption,
        "hashtags": hashtags,
        "poster_url": poster_path,
        "status": "generated",
        "created_at": datetime.utcnow()
    }

    result = campaigns.insert_one(campaign)

    return success({
        "campaign": {
            "_id": str(result.inserted_id),
            "business": business,
            "product": product,
            "offer": offer,
            "caption": caption,
            "hashtags": hashtags,
            "poster_url": poster_path,
            "status": "generated"
        }
    })

# 🔹 GET ALL CAMPAIGNS
@campaign_bp.route("/all", methods=["GET"])
@jwt_required()
def get_campaigns():
    user_id = get_jwt_identity()

    user_campaigns = list(campaigns.find({"user_id": user_id}))

    for c in user_campaigns:
        c["_id"] = str(c["_id"])

    return success({
        "campaigns": user_campaigns
    })


# 🔹 GET SINGLE CAMPAIGN
@campaign_bp.route("/<campaign_id>", methods=["GET"])
@jwt_required()
def get_campaign(campaign_id):
    from bson import ObjectId

    campaign = campaigns.find_one({"_id": ObjectId(campaign_id)})

    if not campaign:
        return error("Campaign not found", 404)

    campaign["_id"] = str(campaign["_id"])

    return success({
        "campaign": campaign
    })


# 🔹 DELETE CAMPAIGN
@campaign_bp.route("/<campaign_id>", methods=["DELETE"])
@jwt_required()
def delete_campaign(campaign_id):
    from bson import ObjectId

    result = campaigns.delete_one({"_id": ObjectId(campaign_id)})

    if result.deleted_count == 0:
        return error("Campaign not found", 404)

    return success({
        "message": "Campaign deleted"
    })
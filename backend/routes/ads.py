from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId

from backend.models.db import campaigns, ads
from backend.utils.helpers import success, error

ads_bp = Blueprint("ads", __name__, url_prefix="/ads")


# ===============================
# 🚀 PUBLISH AD
# ===============================
@ads_bp.route("/publish", methods=["POST"])
@jwt_required()
def publish_ad():
    data = request.get_json()
    user_id = get_jwt_identity()

    campaign_id = data.get("campaign_id")
    platforms = data.get("platforms", ["whatsapp"])  # default

    if not campaign_id:
        return error("campaign_id is required", 400)

    campaign = campaigns.find_one({"_id": ObjectId(campaign_id)})

    if not campaign:
        return error("Campaign not found", 404)

    results = []

    for platform in platforms:
        ad_entry = {
            "user_id": user_id,
            "campaign_id": campaign_id,
            "platform": platform,
            "status": "publishing",
            "created_at": datetime.utcnow(),
            "error": None
        }

        try:
            # ===============================
            # 🟢 WHATSAPP (REAL)
            # ===============================
            if platform == "whatsapp":
                message = f"""
{campaign.get('business')}

{campaign.get('product')} - {campaign.get('offer')}

{campaign.get('caption')}

{' '.join(campaign.get('hashtags', []))}
                """

                import urllib.parse
                whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(message)}"

                ad_entry["status"] = "ready"
                ad_entry["external_ad_id"] = whatsapp_url

            # ===============================
            # 🟡 META (SIMULATED)
            # ===============================
            elif platform == "meta":
                ad_entry["status"] = "live"
                ad_entry["external_ad_id"] = "meta_demo_123"

            # ===============================
            # 🟡 GOOGLE (SIMULATED)
            # ===============================
            elif platform == "google":
                ad_entry["status"] = "live"
                ad_entry["external_ad_id"] = "google_demo_456"

        except Exception as e:
            ad_entry["status"] = "failed"
            ad_entry["error"] = str(e)

        # Save to DB
        result = ads.insert_one(ad_entry)
        ad_entry["_id"] = str(result.inserted_id)

        results.append(ad_entry)

    return success({
        "ads": results
    })
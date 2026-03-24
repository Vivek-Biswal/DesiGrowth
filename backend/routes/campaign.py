from flask import Blueprint, request, jsonify
from datetime import datetime

from backend.models.db import get_db

campaign_bp = Blueprint("campaign", __name__, url_prefix="/campaign")


@campaign_bp.route("/create", methods=["POST"])
def create_campaign():
    data = request.json
    db = get_db()

    campaign = {
        "id": str(datetime.now().timestamp()),
        "data": data,
        "created_at": datetime.now().isoformat()
    }

    db.insert(campaign)

    return jsonify({
        "status": "success",
        "campaign": campaign
    })


@campaign_bp.route("/all", methods=["GET"])
def get_campaigns():
    db = get_db()
    campaigns = db.all()

    return jsonify({
        "campaigns": campaigns
    })
from flask import Blueprint, request, jsonify
from backend.ai_module.ai_generator import generate_marketing_content

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

@ai_bp.route("/generate", methods=["POST"])
def generate_ai():
    data = request.json

    result = generate_marketing_content(data)

    return jsonify({
        "status": "success",
        "caption": result["caption"],
        "hashtags": result["hashtags"]
    })
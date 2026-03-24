from flask import Blueprint, request, jsonify

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


@ai_bp.route("/generate", methods=["POST"])
def generate_ai():
    data = request.json

    return jsonify({
        "status": "success",
        "caption": f"🔥 Special offer on {data.get('product', 'product')}!",
        "hashtags": "#sale #offer #india"
    })
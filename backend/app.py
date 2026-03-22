"""
backend/app.py
--------------
Flask application factory.
All routes are registered via Blueprints.

Endpoints:
  GET  /                        - Health check
  POST /signup                  - Register (email + password)
  POST /login                   - Login (email + password)
  GET  /auth/google             - Start Google OAuth
  GET  /auth/google/callback    - Google OAuth callback
  GET  /user                    - Current user profile  [JWT]
  POST /campaign/create         - Create campaign        [JWT]
  GET  /campaigns               - List campaigns         [JWT]
  GET  /campaign/<id>           - Get campaign           [JWT]
  POST /generate-content        - AI content generation  [JWT]
  POST /generate-campaign       - Legacy alias (no auth) - kept for frontend compat
  GET  /poster/<filename>       - Serve poster image
"""

import os
import sys
import uuid

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from PIL import Image, ImageDraw, ImageFont

# ── Project root on sys.path so ai_module is importable ──
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ai_module.ai_generator import generate_marketing_content

from config import Config
from models.db import init_db
from routes.ai import ai_bp
from routes.auth import auth_bp
from routes.campaign import campaign_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    CORS(app)
    JWTManager(app)

    # Database
    init_db(app.config["DATABASE_PATH"])
    os.makedirs(app.config["POSTER_FOLDER"], exist_ok=True)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(campaign_bp)
    app.register_blueprint(ai_bp)

    # ── Health check ──
    @app.route("/")
    def home():
        return jsonify({"status": "ok", "message": "DesiGrowth Backend Running"})

    # ── Serve poster images ──
    @app.route("/poster/<filename>")
    def serve_poster(filename):
        return send_from_directory(app.config["POSTER_FOLDER"], filename)

    # ── Legacy /generate-campaign (no auth) — keeps existing frontend working ──
    @app.route("/generate-campaign", methods=["POST"])
    def generate_campaign_legacy():
        data = request.get_json() or {}
        business = data.get("business", "")
        product = data.get("product", "")
        offer = data.get("offer", "")
        festival = data.get("festival", "")
        location = data.get("location", "")

        ai_result = generate_marketing_content(business, product, offer, festival, location)

        poster_folder = app.config["POSTER_FOLDER"]
        os.makedirs(poster_folder, exist_ok=True)
        img = Image.new("RGB", (800, 800), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        try:
            f1 = ImageFont.truetype("arial.ttf", 60)
            f2 = ImageFont.truetype("arial.ttf", 40)
        except OSError:
            f1 = f2 = ImageFont.load_default()
        draw.text((100, 100), business, fill="black", font=f1)
        draw.text((100, 300), product, fill="blue", font=f2)
        draw.text((100, 450), offer, fill="red", font=f2)
        filename = f"poster_{uuid.uuid4().hex}.png"
        img.save(os.path.join(poster_folder, filename))
        poster_url = request.host_url + "poster/" + filename

        return jsonify({
            "caption": ai_result.get("caption", ""),
            "hashtags": ai_result.get("hashtags", ""),
            "poster": poster_url,
        })

    return app


# ── Entry point ──
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

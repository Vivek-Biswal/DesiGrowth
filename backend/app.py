from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

from config import Config
from models.db import init_db

from routes.auth import auth_bp
from routes.campaign import campaign_bp
from routes.ai import ai_bp


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # Ensure folders exist
    os.makedirs(app.config["POSTER_FOLDER"], exist_ok=True)

    # Init DB
    init_db(app.config["DATABASE_PATH"])

    # ✅ CORS (IMPORTANT)
    CORS(app)

    # JWT
    jwt = JWTManager(app)

    # Debug logs
    print("🚀 Backend starting...")
    print("GEMINI:", "SET" if os.getenv("GEMINI_API_KEY") else "MISSING")
    print("JWT:", "SET" if os.getenv("JWT_SECRET_KEY") else "MISSING")

    @app.before_request
    def log_request():
        print(f"{request.method} {request.path}")

    # Register routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(campaign_bp)
    app.register_blueprint(ai_bp)

    # Health check
    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "DesiGrowth Backend Running 🚀"
        })

    # Poster route
    @app.route("/poster/<filename>")
    def serve_poster(filename):
        return send_from_directory(app.config["POSTER_FOLDER"], filename)

    # Error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

    return app


# 🚀 LOCAL RUN ONLY (Render uses Gunicorn)
if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
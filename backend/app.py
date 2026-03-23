from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Config + DB
from config import Config
from models.db import init_db

# Routes
from routes.auth import auth_bp
from routes.campaign import campaign_bp
from routes.ai import ai_bp


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # ✅ INIT DB
    init_db(app.config["DATABASE_PATH"])

    # ✅ 🔥 FIXED CORS (VERY IMPORTANT)
    CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:5500",
                "http://127.0.0.1:5500",
                "https://desi-growth.vercel.app"
            ]
        }
    })

    # Optional but helpful
    app.config['CORS_HEADERS'] = 'Content-Type'

    # JWT
    jwt = JWTManager(app)

    # Logging
    @app.before_request
    def log_request():
        print(f"{request.method} {request.path}")

    # Blueprints
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
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
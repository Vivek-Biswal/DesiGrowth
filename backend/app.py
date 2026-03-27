from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Config
from backend.config import Config

# Routes
from backend.routes.auth import auth_bp
from backend.routes.campaign import campaign_bp
from backend.routes.ai import ai_bp
from backend.routes.ads import ads_bp


def create_app():
    app = Flask(__name__)

    # ===============================
    # CONFIG
    # ===============================
    app.config.from_object(Config)

    # ===============================
    # ✅ FINAL CORS FIX (IMPORTANT)
    # ===============================
    CORS(
        app,
        origins="*",
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        supports_credentials=True
    )

    # ===============================
    # OPTIONAL: EXTRA SAFETY HEADERS
    # ===============================
    @app.after_request
    def after_request(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    # ===============================
    # ENV CHECK
    # ===============================
    if not os.getenv("MONGO_URI"):
        raise Exception("❌ MONGO_URI is missing")

    os.makedirs(app.config["POSTER_FOLDER"], exist_ok=True)

    # ===============================
    # JWT
    # ===============================
    JWTManager(app)

    # ===============================
    # LOGGING
    # ===============================
    print("🚀 Backend starting...")
    print("MongoDB:", "CONNECTED" if os.getenv("MONGO_URI") else "MISSING")
    print("GEMINI:", "SET" if os.getenv("GEMINI_API_KEY") else "MISSING")
    print("JWT:", "SET" if os.getenv("JWT_SECRET_KEY") else "MISSING")

    @app.before_request
    def log_request():
        print(f"{request.method} {request.path}")

    # ===============================
    # ROUTES
    # ===============================
    app.register_blueprint(auth_bp)
    app.register_blueprint(campaign_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(ads_bp)

    # ===============================
    # HEALTH CHECK
    # ===============================
    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "DesiGrowth Backend Running 🚀"
        })

    # ===============================
    # POSTER SERVING
    # ===============================
    @app.route("/poster/<filename>")
    def serve_poster(filename):
        return send_from_directory(app.config["POSTER_FOLDER"], filename)

    # ===============================
    # ERROR HANDLER
    # ===============================
    @app.errorhandler(Exception)
    def handle_exception(e):
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

    return app


# ===============================
# GUNICORN ENTRY
# ===============================
app = create_app()


# ===============================
# LOCAL RUN
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
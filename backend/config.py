import os
from dotenv import load_dotenv

# Load .env from the project root (one level up from backend/)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens don't expire (good for hackathon demo)

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI = os.getenv(
        "GOOGLE_REDIRECT_URI", "http://localhost:5000/auth/google/callback"
    )

    # Database
    DATABASE_PATH = os.path.join(
        os.path.dirname(__file__), os.getenv("DATABASE_PATH", "database.json")
    )

    # Poster folder
    POSTER_FOLDER = os.path.join(
        os.path.dirname(__file__), os.getenv("POSTER_FOLDER", "posters")
    )

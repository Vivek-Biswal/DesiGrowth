import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    DATABASE_PATH = os.path.join(
        os.path.dirname(__file__), "database.json"
    )

    POSTER_FOLDER = os.path.join(
        os.path.dirname(__file__), "posters"
    )
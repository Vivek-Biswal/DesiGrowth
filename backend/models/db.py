"""
models/db.py
------------
Single TinyDB instance for the entire app.
All data is stored in backend/database.json.
"""

from tinydb import TinyDB, Query
from flask import current_app

# Module-level db handle (initialized in app factory via init_db)
_db = None


def init_db(db_path: str):
    """Call once during app startup to open the database file."""
    global _db
    _db = TinyDB(db_path, indent=2, sort_keys=True)


def get_db() -> TinyDB:
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db


def get_users_table():
    """Return the 'users' table."""
    return get_db().table("users")


def get_campaigns_table():
    """Return the 'campaigns' table."""
    return get_db().table("campaigns")


# Convenience re-export so callers can do: from models.db import Query
__all__ = ["init_db", "get_db", "get_users_table", "get_campaigns_table", "Query"]

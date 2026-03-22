from tinydb import TinyDB, Query

_db = None


def init_db(db_path: str):
    global _db
    _db = TinyDB(db_path, indent=2, sort_keys=True)


def get_db() -> TinyDB:
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db


def get_users_table():
    return get_db().table("users")


def get_campaigns_table():
    return get_db().table("campaigns")


__all__ = ["init_db", "get_db", "get_users_table", "get_campaigns_table", "Query"]
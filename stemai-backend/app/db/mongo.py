# app/db/mongo.py
from pymongo import MongoClient
from app.config import get_settings

_client = None
_db = None

def get_db():
    """Return a synchronous PyMongo database connection."""
    global _client, _db
    if _db is None:
        settings = get_settings()
        _client = MongoClient(settings.MONGODB_URI)
        _db = _client[settings.MONGODB_DB]
    return _db

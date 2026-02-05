
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
DB_NAME = "support_saas"

_client = None
_db = None

async def get_db():
    """
    Returns a singleton MongoDB database instance.
    """
    global _client, _db

    if _client is None:
        print("=====Creating MongoDB client====")
        _client = AsyncIOMotorClient(MONGO_URL)
        _db = _client[DB_NAME]

    return _db

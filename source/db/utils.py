from motor.motor_asyncio import AsyncIOMotorCollection
from db.db import MongoDB, MONGO_DB_NAME


async def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    return MongoDB.client[MONGO_DB_NAME][collection_name]

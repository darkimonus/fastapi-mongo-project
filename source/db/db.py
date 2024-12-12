from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from conf import config
import logging

MONGO_HOST = config("MONGO_HOST", "localhost")
MONGO_PORT = int(config("MONGO_PORT", 27017))
MONGO_USER = config("MONGO_INITDB_ROOT_USERNAME", "admin")
MONGO_PASS = config("MONGO_INITDB_ROOT_PASSWORD", "admin")
MONGO_DB_NAME = config("MONGO_DB_NAME", "fastapi_db")


class MongoDB:
    client = None

    @staticmethod
    async def connect():
        """
            Initialize MongoDB connection
        """
        MongoDB.client = AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
        )
        logger = logging.getLogger('info')
        try:
            await MongoDB.client.server_info()
            logger.info("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            logger.info(f"Failed to connect to MongoDB: {e}")

    @staticmethod
    async def close():
        """
            Close MongoDB connection
        """
        if MongoDB.client:
            MongoDB.client.close()
            logger = logging.getLogger('info')
            logger.info("MongoDB connection closed")

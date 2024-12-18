from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from conf import settings as s
import logging


class MongoDB:
    client = None

    @staticmethod
    async def connect():
        """
            Initialize MongoDB connection
        """
        MongoDB.client = AsyncIOMotorClient(
            f"mongodb://{s.db.mongo_user}:{s.db.mongo_pass}@{s.db.mongo_host}:{s.db.mongo_port}/{s.db.mongo_db_name}"
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

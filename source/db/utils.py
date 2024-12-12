from motor.motor_asyncio import AsyncIOMotorCollection
from db.db import MongoDB, MONGO_DB_NAME
from datetime import timedelta, datetime
from settings import RESERVATION_BEFORE_AND_AFTER_TIME


async def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    return MongoDB.client[MONGO_DB_NAME][collection_name]


def check_time(start_time: datetime, end_time: datetime) -> tuple:
    buffer = timedelta(minutes=RESERVATION_BEFORE_AND_AFTER_TIME)
    start_check = start_time - buffer
    end_check = end_time + buffer
    return start_check, end_check

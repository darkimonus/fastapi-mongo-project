from motor.motor_asyncio import AsyncIOMotorCollection
from db.db import MongoDB
from datetime import timedelta, datetime
from conf import settings


async def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    return MongoDB.client[settings.db.mongo_db_name][collection_name]


def check_time(start_time: datetime, end_time: datetime) -> tuple:
    buffer = timedelta(minutes=settings.reservation_before_and_after_time)
    start_check = start_time - buffer
    end_check = end_time + buffer
    return start_check, end_check

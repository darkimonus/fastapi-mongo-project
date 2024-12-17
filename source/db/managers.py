from pydantic import BaseModel
from db.utils import get_collection, check_time
from db.models import (
    Food,
    Restaurant,
    Table,
    ReservationTable,
    Reservation,
    OrderedFood,
    Order,
    User,
    PhoneAuthModel,
)

from bson import ObjectId
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from random import randint

"""
This function

Parameters:
- 

Raises:

Returns:

"""


class BaseManager:
    _collection_name: Optional[str] = None
    model = BaseModel
    unique_field: Optional[str] = None

    @staticmethod
    def serialize(document: dict) -> dict:
        document["_id"] = str(document["_id"])
        return document

    @classmethod
    async def find_documents(cls, query: Dict[str, Any] = None,
                             skip: int = 0, limit: int = 0,
                             projection: Optional[Dict[str, int]] = None) -> List[dict]:
        """
        This function uses motor collection to find documents in _collection_name collection using provided
        arguments.

        Parameters:
        - query: mongodb query
        - skip: how many documents motor should skip
        - limit: how many documents should be retrieved from db
        - projection: which fields should be retrieved

        Raises:

        Returns:
        List of dictionaries that contain documents info.
        """

        collection = await get_collection(cls._collection_name)
        cursor = collection.find(query or {}, projection=projection).skip(skip).limit(limit)
        return [cls.serialize(doc) async for doc in cursor]

    @classmethod
    async def find_document(cls, field: str, value: str | ObjectId) -> Optional[dict]:
        """
        This function uses motor collection to find document in _collection_name collection using provided
        field and value.

        Parameters:
        - field: field that will be used to search for document
        - value: value of provided field

        Raises:

        Returns:
        Dictionary with document data or None if no document has been found.
        """
        if field == '_id':
            value = ObjectId(value)

        collection = await get_collection(cls._collection_name)
        document = await collection.find_one({field: value})
        if document:
            return cls.serialize(dict(document))
        else:
            return None

    @classmethod
    async def create_document(cls, document: model) -> dict:
        """
        This function uses motor collection to create document in _collection_name collection using provided
        arguments. It also checks if there is another object with unique field for this collection.

        Parameters:
        - document: object of manager model that contains document information which will be inserted

        Raises:
        - ValueError: if another document with the same unique field value is present in collection

        Returns:
        Dictionary with success message.
        """
        collection = await get_collection(cls._collection_name)

        if cls.unique_field:
            unique_value = getattr(document, cls.unique_field, None)
            if unique_value and await cls.find_document(cls.unique_field, unique_value):
                raise ValueError(f"{cls.model.__name__} with this {cls.unique_field} already exists.")

        result = await collection.insert_one(document.model_dump())
        return {"message": f"{cls.model.__name__} created",
                "_id": str(result.inserted_id)}

    @classmethod
    async def update_document_entirely(cls, document_id: ObjectId, document: model):
        """
        This function uses motor collection to entirely update document in _collection_name collection using provided
        document_id and pydantic model object.

        Parameters:
        - document_id: _id of document that should be updated
        - document: object of manager model that contains document information which will be inserted

        Raises:
        - ValueError: if document with provided _id doesn't exist

        Returns:
        Dictionary with success message.
        """
        collection = await get_collection(cls._collection_name)

        existing_document = await cls.find_document('_id', document_id)
        if not existing_document:
            raise ValueError(f"{cls.model.__name__} with this {document_id} _id does not exist.")

        update_data = document.model_dump(exclude_unset=True)
        result = await collection.update_one(
            {"_id": document_id},
            {"$set": update_data},
        )

        if result.matched_count == 0:
            raise ValueError(f"{cls.model.__name__} update failed. {result.raw_result}")
        return {"message": f"Updated {cls.model.__name__} with {str(document_id)} _id."}

    @classmethod
    async def update_document(cls, document_id: ObjectId, update_data: dict):
        """
        This function uses motor collection to partially update document in _collection_name collection using provided
        document_id and update_data dictionary.

        Parameters:
        - document_id: _id of document that should be updated
        - update_data: dictionary that contains fields and their new values

        Raises:
        - ValueError: if document with provided _id doesn't exist

        Returns:
        Dictionary with success message.
        """
        collection = await get_collection(cls._collection_name)

        existing_document = await cls.find_document('_id', document_id)
        if not existing_document:
            raise ValueError(f"{cls.model.__name__} with this {document_id} _id does not exist.")

        result = await collection.update_one(
            {"_id": document_id},
            {"$set": update_data},
        )

        if result.matched_count == 0:
            raise ValueError(f"{cls.model.__name__} update failed. {result.raw_result}")
        return {"message": f"Updated {cls.model.__name__} with {str(document_id)} _id."}

    @classmethod
    async def delete_document(cls, field: str, value: str | ObjectId) -> str:
        """
        This function uses motor collection to delete document in _collection_name collection using provided
        field and it's value.

        Parameters:
        - field: field that will be used to search for document
        - value: value of provided field

        Raises:

        Returns:
        Success or fail message.
        """
        if field == '_id':
            value = ObjectId(value)

        collection = await get_collection(cls._collection_name)
        result = await collection.delete_one({field: value})
        if result.deleted_count == 1:
            return f"{cls.model.__name__} document with {field} with value {value} was successfully deleted."
        else:
            return str(result)


class FoodsManager(BaseManager):
    _collection_name = 'food'
    model = Food
    unique_field = 'name'

    @classmethod
    async def find_food_by_id(cls, document_id: ObjectId):
        return await cls.find_document('_id', document_id)

    @classmethod
    async def get_food_by_name(cls, document_name: str):
        return await cls.find_document('name', document_name)

    @classmethod
    async def create_food(cls, document: Food):
        return await cls.create_document(document)

    @classmethod
    async def find_by_kind(cls, kind: str) -> List[dict]:
        return await cls.find_documents(query={"kind": kind})


class RestaurantsManager(BaseManager):
    _collection_name = 'restaurants'
    model = Restaurant
    unique_field = 'address'

    @classmethod
    async def create_restaurant(cls, document: Restaurant):
        return await cls.create_document(document)


class TablesManager(BaseManager):
    _collection_name = 'tables'
    model = Table
    unique_field = 'number'

    @classmethod
    async def create_table(cls, document: Table):
        if await RestaurantsManager.find_document('address', document.restaurant.address):
            return await cls.create_document(document)
        else:
            raise ValueError(f"Provided {RestaurantsManager.model.__name__} not found.")


class ReservationsManager(BaseManager):
    _collection_name = 'reservations'
    model = Reservation

    @classmethod
    async def check_overlapping_reservations(cls, table_id: ObjectId, start_time: datetime, end_time: datetime) -> bool:
        start_check, end_check = check_time(start_time, end_time)

        overlapping_reservations = await cls.find_documents({
            "table_id": table_id,
            "status": {"$ne": "cancelled"},
            "$or": [
                {"start_time": {"$lt": end_check, "$gte": start_time}},
                {"end_time": {"$lte": end_time, "$gte": start_check}},
                {"start_time": {"$lte": start_check}, "end_time": {"$gte": end_check}}
            ]
        })

        return bool(overlapping_reservations)

    @classmethod
    async def create_document(cls, document: Reservation):
        if await TablesManager.find_document('_id', document.table_id):
            if cls.check_overlapping_reservations(ObjectId(document.table_id), document.start_time, document.end_time):
                raise ValueError("The table is already reserved for the specified time range.")
            return await super().create_document(document)
        else:
            raise ValueError(f"Provided {TablesManager.model.__name__} with _id {document.table_id} not found.")

    @classmethod
    async def find_reservations_by_table(cls, table_id: str):
        return await cls.find_documents({'table_id': ObjectId(table_id)})

    @classmethod
    async def find_table_reservations_by_day(cls, table_id: str, date: datetime):
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = start_of_day + timedelta(days=1)

        return await cls.find_documents({
            'table_id': ObjectId(table_id),
            'start_time': {'$lt': end_of_day},
            'end_time': {'$gte': start_of_day}
        })

    @classmethod
    async def find_reservations_by_restaurant(cls, restaurant_id: str) -> List[dict]:
        tables = await TablesManager.find_documents(
            {'restaurant_id': ObjectId(restaurant_id)}, projection={'_id': 1})

        if not tables:
            return []

        table_ids = [table['_id'] for table in tables]

        reservations = await cls.find_documents({'table_id': {'$in': table_ids}})

        return reservations

    @classmethod
    async def find_restaurant_reservations_by_day(cls, restaurant_id: str, date: datetime) -> List[dict]:
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = start_of_day + timedelta(days=1)

        tables = await TablesManager.find_documents(
            {'restaurant_id': ObjectId(restaurant_id)}, projection={'_id': 1})

        if not tables:
            return []

        table_ids = [table['_id'] for table in tables]

        reservations = await cls.find_documents({
            'table_id': {'$in': table_ids},
            'start_time': {'$lt': end_of_day},
            'end_time': {'$gte': start_of_day}
        })

        return reservations


class OrdersManager(BaseManager):
    _collection_name = 'orders'
    model = Order

    @staticmethod
    async def serialize(document: dict) -> dict:
        document = super().serialize(document)
        document['date'] = datetime.fromisoformat(document.get("date"))
        return document

    @classmethod
    async def create_order(cls, instance: Order):
        table = await TablesManager.find_document('_id', ObjectId(instance.table_id))
        if table:
            return await cls.create_document(instance)
        else:
            raise ValueError(f"Table with _id {Order.table_id} doesn't exist.")

    @classmethod
    async def update_order_status(cls, order_id: str, status: str):
        return await cls.update_document(ObjectId(order_id), {'status': status})

    @classmethod
    async def find_table_orders_by_day(cls, table_id: str, date: datetime):
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = start_of_day + timedelta(days=1)

        return await cls.find_documents({
            'table_id': ObjectId(table_id),
            'date': {'$gte': start_of_day, '$lt': end_of_day}
        })


class PhoneCodesManager(BaseManager):
    model = PhoneAuthModel
    _collection_name = 'phone_codes'
    unique_field = 'phone_number'

    @classmethod
    async def setup_ttl_index(cls):
        """
        This function ensures that all documents in phone_codes collection will be deleted in 5 minutes.
        """
        collection = await get_collection(cls._collection_name)
        await collection.create_index("created_at", expireAfterSeconds=300)

    @classmethod
    async def generate_code(cls, phone_number: str) -> str:
        """
        This function generates and saves to db code that will be sent to user for authentication purpose.

        Parameters:
        - phone_number: number of user's phone

        Returns:
        Code that will be sent to user.
        """
        code = str(randint(1000, 9999))
        document = cls.model(phone_number=phone_number, code=code)
        await cls.create_document(document)
        return code

    @classmethod
    async def verify_code(cls, phone_number: str, code: str) -> bool:
        """
        This function attempts to find document with provided code and phone number in phone_codes collection.

        Parameters:
        - phone_number: number of user's phone
        - code: code that was sent to user

        Returns:
        True if code is valid, false if code was deleted, doesn't exist or is invalid.
        """
        document = await cls.find_document('phone_number', phone_number)
        if document and document['code'] == code:
            await cls.delete_document('phone_number', phone_number)
            return True
        return False

    @classmethod
    async def delete_expired_code(cls, phone_number: str):
        await cls.delete_document('phone_number', phone_number)


class UsersManager(BaseManager):
    model = User
    _collection_name = 'users'
    unique_field = 'phone_number'

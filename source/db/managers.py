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
)

from bson import ObjectId
from typing import Optional, List, Dict, Any
from datetime import datetime


class BaseManager:
    _collection_name: Optional[str] = None
    model = BaseModel

    @staticmethod
    def serialize(document: dict) -> dict:
        document["_id"] = str(document["_id"])
        return document

    @classmethod
    def _check_fields(cls, query: Dict[str, str | ObjectId]):
        """
        This method is designed to check query for fields that doesn't exist.
        """
        errors = []
        for field in query.keys():
            if field != '_id' and field not in cls.model.model_fields:
                errors.append(field)
        return errors

    @classmethod
    async def find_documents(cls, query: Dict[str, Any] = None,
                             skip: int = 0, limit: int = 0) -> List[dict]:
        if query:
            fields_errors = cls._check_fields(query)
            if len(fields_errors) > 0:
                raise ValueError(f"{cls.model.__name__} doesn't have this fields {fields_errors}")

        collection = await get_collection(cls._collection_name)
        cursor = collection.find(query or {}).skip(skip).limit(limit)
        return [cls.serialize(doc) async for doc in cursor]

    @classmethod
    async def find_document(cls, field: str, value: str | ObjectId) -> Optional[dict]:
        if field == '_id':
            value = ObjectId(value)
        fields_errors = cls._check_fields({field: value})
        if len(fields_errors) > 0:
            raise ValueError(f"{cls.model.__name__} doesn't have this fields {fields_errors}")

        collection = await get_collection(cls._collection_name)
        document = await collection.find_one({field: value})
        if document:
            return cls.serialize(dict(document))
        else:
            return None

    @classmethod
    async def create_document(cls, document: model, field: Optional[str]) -> dict:
        collection = await get_collection(cls._collection_name)
        if field:
            if await cls.find_document(field, document.name):
                raise ValueError(f"{cls.model.__name__} with this "
                                 f"{field} (that should be unique) already exists.")

        result = await collection.insert_one(document.model_dump())
        return {"message": f"{cls.model.__name__} created",
                "id": str(result.inserted_id)}

    @classmethod
    async def update_document_entirely(cls, document_id: ObjectId, document: model):
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
        if field == '_id':
            value = ObjectId(value)
        fields_errors = cls._check_fields({field: value})
        if len(fields_errors) > 0:
            raise ValueError(f"{cls.model.__name__} doesn't have this fields {fields_errors}")

        collection = await get_collection(cls._collection_name)
        result = await collection.delete_one({field: value})
        if result.deleted_count == 1:
            return f"{cls.model.__name__} document with {field} with value {value} was successfully deleted."
        else:
            return str(result)


class FoodsManager(BaseManager):
    _collection_name = 'food'
    model = Food

    @classmethod
    async def find_food_by_id(cls, document_id: ObjectId):
        return await cls.find_document('_id', document_id)

    @classmethod
    async def get_food_by_name(cls, document_name: str):
        return await cls.find_document('name', document_name)

    @classmethod
    async def create_food(cls, document: Food):
        return await cls.create_document(document, 'name')

    @classmethod
    async def find_by_kind(cls, kind: str) -> List[dict]:
        return await cls.find_documents(query={"kind": kind})


class RestaurantsManager(BaseManager):
    _collection_name = 'restaurants'
    model = Restaurant

    @classmethod
    async def create_restaurant(cls, document: Restaurant):
        return await cls.create_document(document, 'address')

    @classmethod
    async def find_restaurant(cls, address: str):
        return await cls.find_document('address', address)


class TablesManager(BaseManager):
    _collection_name = 'tables'
    model = Table

    @classmethod
    async def create_table(cls, document: Table):
        if await RestaurantsManager.find_restaurant(document.restaurant.address):
            return await cls.create_document(document, 'number')
        else:
            raise ValueError(f"Provided {RestaurantsManager.model.__name__} not found.")

    @classmethod
    async def find_tables_by_restaurant(cls, argument: str):
        return await cls.find_documents({'restaurant_id': argument})


class ReservationsManager(BaseManager):
    _collection_name = 'reservations'
    model = Reservation

    @classmethod
    async def create_reservation(cls, document: Reservation):
        if await TablesManager.find_document('_id', document.table_id):
            start_check, end_check = check_time(document.start_time, document.end_time)

            overlapping_reservations = await cls.find_documents({
                "table_id": document.table_id,
                "status": {"$ne": "cancelled"},
                "$or": [
                    {"start_time": {"$lt": end_check, "$gte": document.start_time}},
                    {"end_time": {"$lte": document.end_time, "$gte": start_check}},
                    {"start_time": {"$lte": start_check}, "end_time": {"$gte": end_check}}
                ]
            })

            if overlapping_reservations:
                raise ValueError("The table is already reserved for the specified time range.")
            return await cls.create_document(document, None)
        else:
            raise ValueError(f"Provided {TablesManager.model.__name__} with _id {document.table_id} not found.")

    @classmethod
    async def find_reservations_by_table(cls, table_id):
        return await cls.find_document('table_id', table_id)


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
            return await cls.create_document(instance, None)
        else:
            raise ValueError(f"Table with _id {Order.table_id} doesn't exist.")

    @classmethod
    async def update_order_status(cls, order_id: str, status: str):
        return await cls.update_document(ObjectId(order_id), {'status': status})

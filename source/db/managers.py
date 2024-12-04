from pydantic import BaseModel
from db.utils import get_collection
from db.models import (
    Food,
    Restaurant,
)

from bson import ObjectId
from typing import Optional, List, Dict


class BaseManager:
    _collection_name: Optional[str] = None
    model = BaseModel

    @staticmethod
    def serialize(document: dict) -> dict:
        document["_id"] = str(document["_id"])
        return document

    @classmethod
    def _check_fields(cls, query: Dict[str, str | ObjectId]):
        errors = []
        for field in query.keys():
            if field != '_id' and field not in cls.model.model_fields:
                errors.append(field)
        return errors

    @classmethod
    async def find_documents(cls, query: Dict[str, str | ObjectId] = None,
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
    async def update_document(cls, document_id: ObjectId, document: model):
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


class TablesManager(BaseManager):
    _collection_name = 'restaurants'
    model = Restaurant

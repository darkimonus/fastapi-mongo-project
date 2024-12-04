from fastapi import APIRouter, HTTPException
from db.managers import FoodsManager
from db.models import Food

from utils import convert_to_mongo_id

router = APIRouter()


@router.post("/foods/")
async def create_food(food: Food):
    try:
        return await FoodsManager.create_food(food)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/foods/{kind}/")
async def get_foods_by_kind(kind: str):
    instances = await FoodsManager.find_by_kind(kind)
    return instances


@router.get("/foods/")
async def get_foods():
    instances = await FoodsManager.find_documents()
    return instances


@router.put("/foods/update/{_id}", status_code=201)
async def update_food(_id: str, food: Food):
    try:
        return await FoodsManager.update_document(convert_to_mongo_id(_id), food)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

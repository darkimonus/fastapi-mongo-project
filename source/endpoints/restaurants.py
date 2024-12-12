from fastapi import APIRouter, HTTPException
from db.managers import RestaurantsManager, ReservationsManager, TablesManager
from db.models import Restaurant, TableStatusEnum
from utils import convert_to_mongo_id

router = APIRouter()


@router.post("/restaurants/")
async def create_restaurant(instance: Restaurant):
    try:
        return await RestaurantsManager.create_restaurant(instance)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/restaurants/")
async def get_restaurants():
    instances = await RestaurantsManager.find_documents()
    return instances


@router.get("/restaurants/{address}")
async def get_restaurant(_id: str):
    instance = await RestaurantsManager.find_document('_id', _id)
    if not instance:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return instance


@router.get('/restaurants/{_id}/reservations/')
async def get_restaurant_reservations(_id: str):
    instances = await ReservationsManager.find_documents()
    return instances


@router.get("/restaurants/{_id}/tables/")
async def get_restaurant_tables_by_id(_id: str) -> list:
    try:
        instances = await TablesManager.find_tables_by_restaurant(_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return instances


@router.get("/restaurants/{_id}/tables/{status}/")
async def get_restaurant_tables_by_status(_id: str, status: TableStatusEnum):
    try:
        instances = await TablesManager.find_documents(
            {
                'restaurant_id': convert_to_mongo_id(_id),
                'status': status,
            })
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return instances

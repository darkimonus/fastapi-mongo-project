from fastapi import APIRouter, HTTPException
from db.managers import ReservationsManager
from db.models import Reservation, ReservationStatusEnum

router = APIRouter()


@router.post("/restaurants/{}")
async def create_restaurant(instance: Restaurant):
    try:
        return await RestaurantsManager.create_restaurant(instance)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/restaurants/")
async def get_restaurants():
    instances = await RestaurantsManager.find_documents()
    return instances


@router.get("/restaurants/{address}/reser")
async def get_restaurant_reservations(address: str):
    instance = await RestaurantsManager.find_restaurant(address)
    if not instance:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return instance

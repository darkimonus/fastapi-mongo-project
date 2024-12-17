from fastapi import APIRouter, HTTPException
from db.managers import ReservationsManager
from db.models import Reservation, ReservationStatusEnum

router = APIRouter(prefix='/reservations')


@router.post("/")
async def create_restaurant(instance: Reservation):
    try:
        return await ReservationsManager.create_document(instance)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def get_reservations():
    instances = await ReservationsManager.find_documents()
    return instances

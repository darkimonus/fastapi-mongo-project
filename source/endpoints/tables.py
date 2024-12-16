from fastapi import APIRouter, HTTPException, Depends
from db.managers import TablesManager, ReservationsManager
from db.models import Table, TableStatusEnum
from utils import convert_to_mongo_id
from typing import Optional
from datetime import datetime

router = APIRouter()


@router.post("/tables/")
async def create_table(instance: Table):
    try:
        return await TablesManager.create_table(instance)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tables/")
async def get_tables():
    instances = await TablesManager.find_documents()
    return instances


@router.get("/tables/{_id}")
async def get_table(_id: str):
    document = await TablesManager.find_document('_id', _id)
    if not document:
        raise HTTPException(status_code=404, detail="Table not found")
    return document


@router.put("/tables/{_id}", status_code=201)
async def update_table_status(_id: str, status: TableStatusEnum):
    try:
        return await TablesManager.update_document(convert_to_mongo_id(_id), {'status': status})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tables/{_id}/reservations/")
async def get_table_reservations(_id: str):
    return await ReservationsManager.find_reservations_by_table(_id)

@router.get("/tables/{_id}/reservations/{day}/")
async def get_table_reservations(_id: str, day: datetime):
    return await ReservationsManager.find_table_reservations_by_day(_id, datetime)

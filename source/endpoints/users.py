# users.py
from fastapi import APIRouter, HTTPException
from db import users

router = APIRouter()


@router.post("/users/")
async def create_user(user: users.User):
    try:
        return await users.create_user(user)
    except ValueError:
        raise HTTPException(status_code=400, detail="Email already exists.")


@router.get("/users/{email}")
async def get_user(email: str):
    user = await users.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

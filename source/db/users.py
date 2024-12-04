from pydantic import BaseModel, EmailStr, Field
from db.utils import get_collection


class User(BaseModel):
    email: EmailStr
    password: str
    full_name: str = Field(..., min_length=3)


def serialize_user(user: dict) -> dict:
    user["_id"] = str(user["_id"])
    return user


async def create_user(user: User):
    collection = await get_collection('users')
    if await get_user_by_email(user.email):
        raise ValueError("User with this email already exists.")

    result = await collection.insert_one(user.model_dump())
    return {"message": "User created", "user_id": str(result.inserted_id)}


async def get_user_by_email(email: str):
    collection = await get_collection('users')
    user = await collection.find_one({"email": email})
    print(user)
    if user:
        return serialize_user(user)
    else:
        return None

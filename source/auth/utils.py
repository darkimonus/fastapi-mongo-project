from config import (
    SECRET_KEY,
    REFRESH_SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
)
from auth.tasks import send_auth_code

import jwt
from datetime import datetime, timedelta, timezone


def request_auth_code(phone: str):
    send_auth_code(phone)


def authenticate_user(phone: str):
    pass


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

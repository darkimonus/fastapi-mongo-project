from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.utils import create_access_token
from db.models import Token
from typing import Optional, Any

router = APIRouter()


@router.post("/auth/code/")
async def login_for_access_token(phone: str, code: str, refresh_token: Optional[Any]) -> Token:



@router.post("/auth/token/")
async def login_for_access_token(phone, code, refresh_token) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

from conf import settings
from auth.tasks import send_sms_code
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated
from db.models import User, TokenData
from db.managers import UsersManager, PhoneCodesManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def request_auth_code(phone: str):
    code = await PhoneCodesManager.generate_code(phone)
    send_sms_code.delay(phone, code)


async def authenticate_user(phone: str, code: str):
    if settings.auth_jwt.sms_verification:
        verified = await PhoneCodesManager.verify_code(phone, code)
        if verified:
            user_exists = await check_user_existence(phone)
            if user_exists:
                user = await UsersManager.find_document('phone_number', phone)
                user_id = user.get('_id')
            else:
                user_id = create_user(phone)

            access_token = create_access_token(
                {'_id': user_id},
                timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)
            )
            refresh_token = create_refresh_token(
                {'_id': user_id},
                timedelta(minutes=settings.auth_jwt.refresh_token_expire_minutes)
            )
            return {'access_token': access_token, 'refresh_token': refresh_token}
        else:
            raise ValueError('Invalid code.')


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.auth_jwt.accessprivate_key_path.read_text(),
        algorithm=settings.auth_jwt.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_jwt.refresh_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.auth_jwt.refresh_private_key_path.read_text(),
        algorithm=settings.auth_jwt.algorithm
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.auth_jwt.private_key_path.read_text(),
            algorithms=[settings.auth_jwt.algorithm]
        )
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = await UsersManager.find_document('_id', token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def check_user_existence(phone: str) -> bool:
    user = await UsersManager.find_document('phone_number', phone)
    if user:
        return True
    else:
        return False


async def create_user(phone: str):
    result = await UsersManager.create_document(User(phone_number=phone))
    return result.get('_id')


async def get_current_user_using_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.auth_jwt.refresh_private_key_path.read_text(),
            algorithms=[settings.auth_jwt.algorithm]
        )
        phone: str = payload.get("phone")
        if phone is None:
            raise credentials_exception
        token_data = TokenData(phone=phone)
    except InvalidTokenError:
        raise credentials_exception
    user = await UsersManager.find_document('phone', token_data.phone)
    if user is None:
        user = await UsersManager.create_document(User(phone_number=phone))
    return user

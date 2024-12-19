from fastapi import APIRouter, HTTPException
from pydantic_extra_types.phone_numbers import PhoneNumber
from auth.utils import authenticate_user
from db.models import VerificationRequest
from auth.utils import request_auth_code

router = APIRouter(prefix='/auth')


@router.post('/code')
async def get_verification_code(phone: PhoneNumber):
    try:
        await request_auth_code(phone)
        return {'message': 'Your code will be delivered soon.'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/')
async def authenticate_for_tokens(request: VerificationRequest):
    try:
        tokens = await authenticate_user(request.phone, request.code)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post('/refresh')
async def refresh_access_token(request: RefreshTokenRequest):
    try:
        # Валидируем refresh_token
        payload = validate_refresh_token(request.refresh_token)

        # Создаём новый access_token
        new_access_token = create_access_token(data={"sub": payload["sub"]})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=400, detail="Could not refresh access token")

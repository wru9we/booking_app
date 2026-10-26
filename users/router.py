import asyncio
from fastapi_cache.decorator import cache

from fastapi import APIRouter, Depends, HTTPException, Response, status
from users.auth import authenticate_user, create_access_token, get_password_hash
from users.dependencies import get_current_user
from users.models import Users
from users.service import UserService

from users.schemas import SUserAuth

from users.auth import verify_password


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user["id"])})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")

@router.get("/me")
@cache(expire=20)
async def get_me(current_user: Users = Depends(get_current_user)):
    await asyncio.sleep(1)
    return current_user
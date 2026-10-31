import asyncio

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from rooms.service import RoomsService

router = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router.get("")
@cache(expire=20)
async def all_rooms():
    await asyncio.sleep(3)
    return await RoomsService.find_all()


@router.get("/{room_id}")
@cache(expire=10)
async def get_room_id(room_id: int):
    await asyncio.sleep(1)
    return await RoomsService.find_by_id(room_id)

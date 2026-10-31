import asyncio

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from hotels.service import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("")
@cache(expire=20)
async def get_all_hotels():
    await asyncio.sleep(3)
    return await HotelService.find_all()


@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel_id(hotel_id: int):
    await asyncio.sleep(1)
    return await HotelService.find_by_id(hotel_id)

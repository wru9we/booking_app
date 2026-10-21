from fastapi import APIRouter

from hotels.service import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("")
async def get_all_hotels():
    return await HotelService.find_all()


@router.get("/{hotel_id}")
async def get_hotel_id(hotel_id: int):
    return await HotelService.find_by_id(hotel_id)

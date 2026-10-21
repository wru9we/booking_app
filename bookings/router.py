from datetime import date

from fastapi import APIRouter, Depends

from bookings.schemas import SBooking
from bookings.service import BookingService
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_my_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingService.find_all(user_id=user["id"])


@router.get("/{booking_id}")
async def get_booking_id(booking_id: int) -> SBooking | None:
    return await BookingService.find_by_id(booking_id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    await BookingService.add(user["id"], room_id, date_from, date_to)

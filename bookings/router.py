import asyncio
from datetime import date

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as

from bookings.schemas import SBooking
from bookings.service import BookingService
from tasks.tasks import send_booking_confirmation_template
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
@cache(expire=20)
async def get_my_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    await asyncio.sleep(3)
    return await BookingService.find_all(user_id=user["id"])


@router.get("/{booking_id}")
@cache(expire=10)
async def get_booking_id(booking_id: int) -> SBooking | None:
    await asyncio.sleep(1)
    return await BookingService.find_by_id(booking_id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingService.add(user["id"], room_id, date_from, date_to)
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_template.delay(booking_dict, user.email)
    return booking_dict

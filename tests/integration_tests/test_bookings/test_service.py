from bookings.service import BookingService
from datetime import datetime
async def test_add_and_get_booking():
    new_booking = await BookingService.add(
        user_id=2,
        room_id=1,
        date_from=datetime.strptime("2026-11-04", "%Y-%m-%d"),
        date_to=datetime.strptime("2026-11-11", "%Y-%m-%d")
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 1

    new_booking = await BookingService.find_by_id(new_booking.id)

    assert new_booking is not None

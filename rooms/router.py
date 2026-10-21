from fastapi import APIRouter

from rooms.service import RoomsService

router = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router.get("")
async def all_rooms():
    return await RoomsService.find_all()


@router.get("/{room_id}")
async def get_room_id(room_id: int):
    return await RoomsService.find_by_id(room_id)

from fastapi import FastAPI
from sqladmin import Admin, ModelView
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from bookings.models import Bookings
from datebase import engine, async_session_maker
from bookings.router import router as router_bookings
from hotels.router import router as router_hotels
from rooms.models import Rooms
from users.models import Users
from hotels.models import Hotels
from users.router import router as router_users
from rooms.router import router as router_rooms

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)


@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


app.mount("/static", StaticFiles(directory="frontend"), name="static")


admin = Admin(app, engine, session_maker=async_session_maker)


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]


class BookingAdmin(ModelView, model=Bookings):
    column_list = [
        Bookings.id,
        Bookings.room_id,
        Bookings.user_id,
        Bookings.date_from,
        Bookings.date_to,
        Bookings.price,
        Bookings.total_days,
        Bookings.total_price,
    ]


class RoomAdmin(ModelView, model=Rooms):
    column_list = [
        Rooms.id,
        Rooms.hotel_id,
        Rooms.name,
        Rooms.description,
        Rooms.price,
        Rooms.services,
        Rooms.quantity,
        Rooms.image_id,
    ]


class HotelAdmin(ModelView, model=Hotels):
    column_list = [
        Hotels.id,
        Hotels.name,
        Hotels.location,
        Hotels.services,
        Hotels.rooms_quantity,
        Hotels.image_id,
    ]


admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
admin.add_view(BookingAdmin)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

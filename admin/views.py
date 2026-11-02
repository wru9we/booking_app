from sqladmin import ModelView

from bookings.models import Bookings
from hotels.models import Hotels
from rooms.models import Rooms
from users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [c.name for c in Users.__table__.c]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"



class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"

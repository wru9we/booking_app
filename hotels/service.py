from hotels.models import Hotels
from service.base import BaseService


class HotelService(BaseService):
    model = Hotels

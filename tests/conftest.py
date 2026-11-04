import asyncio
from datetime import datetime
import json
import pytest
import pytest_asyncio
from sqlalchemy import insert

from httpx import ASGITransport, AsyncClient

from datebase import Base, async_session_maker, engine
from config import settings
from main import app as fastapi_app

from bookings.models import Bookings
from hotels.models import Hotels
from rooms.models import Rooms
from users.models import Users

@pytest_asyncio.fixture(scope="session", autouse=True, loop_scope="session")
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", "r") as file:
            return json.load(file)
        
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def ac():
        transport = ASGITransport(app=fastapi_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
             yield ac

@pytest_asyncio.fixture(scope="function")
async def authenticated_ac():
        transport = ASGITransport(app=fastapi_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
             await ac.post("/auth/login", json={
                  "email": "test@test.com",
                  "password": "test",
             })
             assert ac.cookies["booking_access_token"]
             yield ac

@pytest_asyncio.fixture(scope="function")
async def session():
     async with async_session_maker() as session:
          yield session
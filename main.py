import time

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from prometheus_fastapi_instrumentator import Instrumentator

from admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from bookings.models import Bookings
from bookings.router import router as router_bookings
from config import settings
from datebase import async_session_maker, engine
from hotels.models import Hotels
from hotels.router import router as router_hotels
from rooms.models import Rooms
from rooms.router import router as router_rooms
from users.models import Users
from users.router import router as router_users
from images.router import router as router_images
from pages.router import router as router_pages
from prometheus.router import router as router_prometheus
from admin.auth import authentication_backend
from logger import logger

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

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
app.include_router(router_images)
app.include_router(router_prometheus)

app.include_router(router_pages)

app.mount("/static", StaticFiles(directory="static"), "static")


admin = Admin(app, engine, session_maker=async_session_maker, authentication_backend=authentication_backend)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin", "/metrics"],
)
instrumentator.instrument(app).expose(app)

admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

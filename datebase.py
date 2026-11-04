from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

if settings.MODE == "TEST":
    DATEBASE_URL = settings.TEST_DATEBASE_URL
    DATEBASE_PARAMS = {"poolclass": NullPool}
else:
    DATEBASE_URL = settings.DATEBASE_URL
    DATEBASE_PARAMS = {}


engine = create_async_engine(DATEBASE_URL, **DATEBASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

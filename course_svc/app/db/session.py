import asyncio
from sys import modules

import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings


async def create_test_db():
    conn = await asyncpg.connect(user=settings.DATABASE_USER,
                                 password=settings.DATABASE_PASSWORD,
                                 host=settings.DATABASE_HOST)
    await conn.fetch(f'DROP DATABASE IF EXISTS {settings.TEST_DATABASE}')
    await conn.fetch(f'CREATE DATABASE {settings.TEST_DATABASE}')

    await conn.close()


DATABASE_URI = settings.ASYNC_DATABASE_URI
if "pytest" in modules:
    DATABASE_URI = settings.ASYNC_TEST_DATABASE_URI
print(DATABASE_URI)
async_engine = create_async_engine(
    DATABASE_URI,
    echo=False,
    future=True,
    pool_size=settings.POOL_SIZE,
    max_overflow=64,
)

if "pytest" in modules:
    asyncio.run(create_test_db())

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

from typing import Generator

from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession

from db import async_session


async def get_db() -> Generator[AsyncSession, None, None]:
    async with async_session() as session:
        yield session


async def require_app_key(app_key: str = Header(...)):
    return app_key

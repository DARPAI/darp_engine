from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.errors import FastApiError
from src.logger import logger
from src.settings import settings

async_engine = create_async_engine(
    settings.database_url_async,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
)

session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    session = session_maker()

    try:
        yield session
        await session.commit()
    except FastApiError as error:
        await session.rollback()
        raise error
    except Exception as error:
        logger.error(f"Encountered an exception while processing request:\n{error}")
        await session.rollback()
        raise
    finally:
        await session.close()

# app/core/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class cho tất cả models"""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency để inject database session"""
    async with AsyncSessionLocal() as session:
        yield session
        # Không cần await session.close() vì async with đã tự động close


# Optional: Hàm dispose engine khi app shutdown
async def close_db_connection():
    """Đóng engine khi FastAPI shutdown"""
    await async_engine.dispose()
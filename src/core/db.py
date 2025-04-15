from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import settings

DATABASE_URL = settings.postgres.db_uri

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.postgres.echo,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.max_overflow,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для FastAPI"""
    async with AsyncSessionLocal() as session:
        yield session

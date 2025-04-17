from contextlib import contextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.core.config import settings

DATABASE_URL_ASYNC = settings.postgres.db_async_uri
DATABASE_URL_SYNC = settings.postgres.db_sync_uri

# async
engine = create_async_engine(
    DATABASE_URL_ASYNC,
    echo=settings.postgres.echo,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.max_overflow,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# sync
SyncEngine = create_engine(DATABASE_URL_SYNC, echo=False)
SyncSessionLocal = sessionmaker(bind=SyncEngine, expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для FastAPI"""
    async with AsyncSessionLocal() as session:
        yield session


@contextmanager
def get_sync_db_session() -> Generator[Session, None, None]:
    """Синхронная сессия для Celery."""
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

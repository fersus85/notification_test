import logging
import pickle
from typing import Any

from redis.asyncio import Redis

from src.core.config import settings

logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self):
        self.redis = Redis.from_url(settings.redis.connection_url)

    async def get(self, key: str) -> str | None:
        """Получение данных из кэша."""
        try:
            cached_val = await self.redis.get(key)
            return pickle.loads(cached_val) if cached_val else None
        except Exception as ex:
            logger.error("Error retrieving from cache: %s", ex)
            return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Сохранение данных в кэш с TTL."""
        try:
            await self.redis.set(key, pickle.dumps(value), ex=ttl)
            logger.debug("Result stored in cache")
        except Exception as ex:
            logger.error("Error storing to cache: %s", ex)

    async def delete(self, key: str) -> None:
        """Удаление данных из кэша."""
        try:
            await self.redis.delete(key)
        except Exception as ex:
            logger.error("Error deleting from cache: %s", ex)
            return None

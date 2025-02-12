"""Redis cache implementation."""
from typing import Any, Dict, Optional, Union
import redis.asyncio as redis
from fastapi import Depends
from app.core.config.settings import Settings, get_settings
import json
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis cache implementation."""

    def __init__(self, client: redis.Redis):
        """Initialize Redis cache."""
        self._client = client

    async def ping(self) -> bool:
        try:
            return await self._client.ping()
        except Exception:
            logger.error("Error pinging Redis")
            return False

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        try:
            value = await self._client.get(key)
            return value if value else None
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {str(e)}")
            return None

    async def set(
        self,
        key: str,
        value: Union[str, bytes, int, float],
        expire: Optional[int] = None
    ) -> bool:
        """Set value in cache."""
        try:
            return await self._client.set(key, value, ex=expire)
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {str(e)}")
            return False

    async def delete(self, key: str) -> int:
        """Delete value from cache."""
        try:
            return await self._client.delete(key)
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {str(e)}")
            return 0

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return await self._client.exists(key)
        except Exception as e:
            logger.error(f"Error checking key {key} existence in Redis: {str(e)}")
            return False

    async def expire(self, key: str, seconds: int) -> bool:
        """Set key expiration time."""
        try:
            return await self._client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Error setting expiration for key {key} in Redis: {str(e)}")
            return False

    async def ttl(self, key: str) -> int:
        """Get key time to live."""
        try:
            return await self._client.ttl(key)
        except Exception as e:
            logger.error(f"Error getting TTL for key {key} from Redis: {str(e)}")
            return -1

    async def incr(self, key: str) -> int:
        try:
            return await self._client.incr(key)
        except Exception as e:
            logger.error(f"Error incrementing key {key} in Redis: {str(e)}")
            return 0

    async def clear_pattern(self, pattern: str) -> bool:
        try:
            keys = await self._client.keys(pattern)
            if keys:
                return await self._client.delete(*keys) > 0
            return True
        except Exception as e:
            logger.error(f"Error clearing pattern {pattern} from Redis: {str(e)}")
            return False

    # Rate limiting methods
    async def zadd(self, key: str, mapping: dict) -> int:
        try:
            return await self._client.zadd(key, mapping)
        except Exception as e:
            logger.error(f"Error adding member to sorted set {key} in Redis: {str(e)}")
            return 0

    async def zcard(self, key: str) -> int:
        try:
            return await self._client.zcard(key)
        except Exception as e:
            logger.error(f"Error getting sorted set cardinality {key} in Redis: {str(e)}")
            return 0

    async def zremrangebyscore(self, key: str, min_score: float, max_score: float) -> int:
        try:
            return await self._client.zremrangebyscore(key, min_score, max_score)
        except Exception as e:
            logger.error(f"Error removing members from sorted set {key} by score in Redis: {str(e)}")
            return 0

    async def close(self):
        """Close Redis connection."""
        await self._client.close()

async def get_redis_client(settings: Settings = Depends(get_settings)) -> RedisCache:
    """Get Redis client."""
    client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return RedisCache(client)

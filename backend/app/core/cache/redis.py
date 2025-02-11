from typing import Any, Optional
from redis import Redis
from fastapi import Depends
from app.core.config.settings import get_settings
import json
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour

    async def ping(self) -> bool:
        """Test Redis connection"""
        try:
            return self.redis.ping()
        except Exception as e:
            logger.error(f"Error pinging Redis: {str(e)}")
            return False

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {str(e)}")
            return None

    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache"""
        try:
            ttl = ttl or self.default_ttl
            return self.redis.setex(
                key,
                ttl,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {str(e)}")
            return False

    async def clear_pattern(self, pattern: str) -> bool:
        """Clear all keys matching pattern"""
        try:
            keys = self.redis.keys(pattern)
            if keys:
                return bool(self.redis.delete(*keys))
            return True
        except Exception as e:
            logger.error(f"Error clearing pattern {pattern} from Redis: {str(e)}")
            return False


def get_redis() -> Redis:
    """Get Redis client"""
    settings = get_settings()
    return Redis.from_url(settings.REDIS_URL)


async def get_redis_cache(redis: Redis = Depends(get_redis)) -> RedisCache:
    """Get Redis cache instance"""
    return RedisCache(redis)

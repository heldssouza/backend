from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import asyncio
import redis.asyncio as redis
from app.core.config.settings import get_settings

settings = get_settings()

class RateLimiter:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)
        self.rate_limit = settings.RATE_LIMIT_PER_MINUTE
        self.window = 60  # 1 minute window

    async def is_rate_limited(self, key: str) -> bool:
        async with self.redis.pipeline() as pipe:
            now = datetime.utcnow().timestamp()
            window_start = now - self.window
            
            # Remove old requests
            await pipe.zremrangebyscore(key, 0, window_start)
            
            # Count requests in current window
            await pipe.zcard(key)
            
            # Add current request
            await pipe.zadd(key, {str(now): now})
            
            # Set expiry on the key
            await pipe.expire(key, self.window)
            
            _, request_count, *_ = await pipe.execute()
            
            return request_count > self.rate_limit

    async def get_remaining_requests(self, key: str) -> int:
        async with self.redis.pipeline() as pipe:
            now = datetime.utcnow().timestamp()
            window_start = now - self.window
            
            await pipe.zremrangebyscore(key, 0, window_start)
            await pipe.zcard(key)
            
            _, request_count = await pipe.execute()
            
            return max(0, self.rate_limit - request_count)

class RateLimitMiddleware:
    def __init__(self):
        self.limiter = RateLimiter()

    async def __call__(self, request: Request, call_next):
        # Skip rate limiting for certain paths
        if request.url.path in settings.RATE_LIMIT_EXCLUDE_PATHS:
            return await call_next(request)

        # Create a unique key based on IP and tenant
        key = f"rate_limit:{request.client.host}:{request.headers.get('X-Tenant-ID', 'default')}"
        
        is_limited = await self.limiter.is_rate_limited(key)
        remaining = await self.limiter.get_remaining_requests(key)
        
        # Add rate limit headers
        headers = {
            "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_MINUTE),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(int((datetime.utcnow() + timedelta(seconds=60)).timestamp()))
        }
        
        if is_limited:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
                headers=headers
            )
        
        response = await call_next(request)
        
        # Add headers to response
        response.headers.update(headers)
        return response

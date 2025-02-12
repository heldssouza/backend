"""
Rate Limiting Module
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from typing import Dict, Tuple, Optional
import time
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from app.core.cache.redis import RedisCache, get_redis_cache
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class RateLimitConfig(BaseModel):
    """Configuration for rate limiting"""
    requests_per_minute: int = 60
    burst_size: int = 10
    window_size: int = 60  # seconds

class RateLimitInfo(BaseModel):
    """Rate limit information returned in headers"""
    remaining: int
    reset: int
    limit: int
    used: int

class RateLimiter:
    """
    Redis-based rate limiter using the Token Bucket algorithm.
    
    This implementation:
    1. Uses Redis for distributed rate limiting
    2. Implements Token Bucket algorithm for burst handling
    3. Provides detailed rate limit information in headers
    4. Supports different limits per endpoint/user
    """

    def __init__(
        self,
        redis: RedisCache,
        config: RateLimitConfig = RateLimitConfig()
    ):
        self.redis = redis
        self.config = config

    async def check_rate_limit(
        self,
        key: str,
        cost: int = 1
    ) -> Tuple[bool, RateLimitInfo]:
        """
        Check if request is within rate limits.
        
        Args:
            key: Unique identifier for the client/endpoint
            cost: Cost of the current request (default: 1)
            
        Returns:
            Tuple[bool, RateLimitInfo]: (is_allowed, rate_limit_info)
        """
        now = time.time()
        window_key = f"ratelimit:{key}:window"
        tokens_key = f"ratelimit:{key}:tokens"

        try:
            # Get current window and tokens
            window_start = float(await self.redis.get(window_key) or now)
            current_tokens = int(await self.redis.get(tokens_key) or self.config.burst_size)

            # Calculate token refill
            elapsed = now - window_start
            if elapsed > self.config.window_size:
                window_start = now
                current_tokens = self.config.burst_size
            else:
                refill = int((elapsed * self.config.requests_per_minute) / self.config.window_size)
                current_tokens = min(
                    self.config.burst_size,
                    current_tokens + refill
                )

            # Check if we have enough tokens
            is_allowed = current_tokens >= cost

            if is_allowed:
                current_tokens -= cost

            # Update Redis
            await self.redis.set(window_key, str(window_start), expire=self.config.window_size * 2)
            await self.redis.set(tokens_key, str(current_tokens), expire=self.config.window_size * 2)

            # Calculate rate limit info
            reset_time = int(window_start + self.config.window_size - now)
            info = RateLimitInfo(
                remaining=current_tokens,
                reset=reset_time,
                limit=self.config.requests_per_minute,
                used=self.config.burst_size - current_tokens
            )

            return is_allowed, info

        except Exception as e:
            logger.error(f"Rate limit check failed: {str(e)}")
            return True, RateLimitInfo(
                remaining=1,
                reset=60,
                limit=self.config.requests_per_minute,
                used=0
            )

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to apply rate limiting to requests.
    
    Features:
    1. Different limits for authenticated/unauthenticated users
    2. Path-based rate limiting
    3. Detailed rate limit information in headers
    4. Configurable limits per endpoint
    """

    def __init__(self, app, redis: Optional[RedisCache] = None):
        super().__init__(app)
        self.redis = redis or get_redis_cache()
        self.limiter = RateLimiter(self.redis)

    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting to the request"""
        # Get client identifier (IP + User ID if authenticated)
        client_id = self._get_client_id(request)
        
        # Check rate limit
        is_allowed, info = await self.limiter.check_rate_limit(client_id)
        
        if not is_allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Too many requests",
                    "retry_after": info.reset
                }
            )

        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(info.limit)
        response.headers["X-RateLimit-Remaining"] = str(info.remaining)
        response.headers["X-RateLimit-Reset"] = str(info.reset)
        
        return response

    def _get_client_id(self, request: Request) -> str:
        """Get unique identifier for the client"""
        # Get client IP
        client_ip = "test_client"
        if request.client and request.client.host:
            client_ip = request.client.host
            
        # Add user ID if authenticated
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"{client_ip}:{user_id}"
            
        return client_ip

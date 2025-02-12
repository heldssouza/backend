"""Security dependencies."""
from functools import wraps
from typing import Optional, List, Annotated
from fastapi import Depends, HTTPException, status, Request, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.security.auth import SecurityService
from app.core.tenant.context import TenantContext
from app.services.master.user import UserService
from app.models.master.user import User
from app.core.cache.redis import RedisCache, get_redis_client
from app.schemas.master.user import TokenData
from app.core.config.settings import get_settings
import time

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_security_service(
    db: Session = Depends(get_db)
) -> SecurityService:
    """
    Get security service instance.
    """
    return SecurityService(db)


def rate_limit(max_requests: int, window_seconds: int):
    """
    Rate limiting dependency.
    
    Args:
        max_requests: Maximum number of requests allowed in the time window
        window_seconds: Time window in seconds
        
    Returns:
        Dependency function
    """
    async def dependency(
        request: Request,
        redis: RedisCache = Depends(get_redis_client)
    ):
        # Get client IP or use test client IP if None
        client_ip = request.client.host if request.client else "test-client"
        
        # Create Redis key
        key = f"rate_limit:{client_ip}:{request.url.path}"
        
        # Get current timestamp
        now = int(time.time())
        
        # Get request count in window
        window_start = now - window_seconds
        
        # Remove old requests
        await redis.zremrangebyscore(key, 0, window_start)
        
        # Count requests in window
        request_count = await redis.zcard(key)
        
        if request_count >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests"
            )
            
        # Add current request
        await redis.zadd(key, {str(now): now})
        
        # Set expiry
        await redis.expire(key, window_seconds)
        
    return dependency


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from token.

    Args:
        token: JWT token
        db: Database session

    Returns:
        User: Current user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(
            username=username,
            tenant_id=payload.get("tenant_id"),
            scopes=payload.get("scopes", [])
        )
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Get current active user.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """
    Get current admin user.

    Args:
        current_user: Current active user

    Returns:
        User: Current admin user

    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user


async def get_tenant_id(
    x_tenant_id: Annotated[str, Header()]
) -> int:
    """
    Get tenant ID from header.

    Args:
        x_tenant_id: Tenant ID from header

    Returns:
        int: Tenant ID

    Raises:
        HTTPException: If tenant ID is invalid
    """
    try:
        return int(x_tenant_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid tenant ID"
        )

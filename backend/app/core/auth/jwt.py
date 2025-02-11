"""JWT token handling."""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import jwt
from app.core.config.settings import get_settings

settings = get_settings()

ALGORITHM = "HS256"


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    
    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=ALGORITHM
    )


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new refresh token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    
    return jwt.encode(
        to_encode,
        settings.jwt_refresh_secret_key,
        algorithm=ALGORITHM
    )


def decode_token(token: str, verify_exp: bool = True) -> Dict[str, Any]:
    """
    Decode and verify a JWT token.
    """
    try:
        # Try to decode as access token first
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
            options={"verify_exp": verify_exp}
        )
    except jwt.JWTError:
        try:
            # If that fails, try as refresh token
            return jwt.decode(
                token,
                settings.jwt_refresh_secret_key,
                algorithms=[ALGORITHM],
                options={"verify_exp": verify_exp}
            )
        except jwt.JWTError as e:
            raise e

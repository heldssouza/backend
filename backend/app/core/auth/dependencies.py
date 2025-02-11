"""Authentication dependencies."""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.models.master.user import User
from app.core.auth.jwt import ALGORITHM, decode_token
from app.core.auth.schemas import TokenPayload
from app.core.config.settings import get_settings
from app.core.tenant.context import TenantContext

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get current user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)
        if token_data.type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(
        User.username == token_data.sub,
        User.tenant_id == token_data.tenant_id
    ).first()
    
    if not user:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )
    
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current user and verify if it's an admin.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def get_tenant_id() -> int:
    """
    Get tenant ID from context or use default.
    """
    tenant_id = TenantContext.get_tenant_id()
    return int(tenant_id) if tenant_id else int(settings.DEFAULT_TENANT_ID)

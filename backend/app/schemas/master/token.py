from typing import Optional, List
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: str
    tenant_id: Optional[int] = None
    scopes: List[str] = []


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    requires_2fa: bool = False


class TokenData(BaseModel):
    """Schema for token payload."""
    username: str
    scopes: List[str] = []


class RefreshToken(BaseModel):
    """Refresh token schema."""
    refresh_token: str

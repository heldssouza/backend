from typing import Optional, List
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: str
    tenant_id: Optional[int] = None
    scopes: List[str] = []


class Token(BaseModel):
    """Token schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class RefreshToken(BaseModel):
    """Refresh token schema."""
    refresh_token: str

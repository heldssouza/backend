"""Authentication schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str
    refresh_token: str


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: str
    tenant_id: Optional[int] = None
    exp: Optional[int] = None
    type: str


class TokenData(BaseModel):
    """Token data schema."""
    username: str
    tenant_id: Optional[int] = None
    scopes: List[str] = []


class RefreshToken(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class TwoFactorSetup(BaseModel):
    """Two-factor authentication setup response schema."""
    secret: str
    qr_code: str


class TwoFactorEnable(BaseModel):
    """Two-factor authentication enable request schema."""
    code: str


class TwoFactorVerify(BaseModel):
    """Two-factor authentication verify request schema."""
    code: str


class UserLogin(BaseModel):
    """User login request schema."""
    username: str
    password: str
    tenant_id: Optional[int] = None


class UserCreate(BaseModel):
    """User creation request schema."""
    username: str
    email: EmailStr
    password: constr(min_length=8)
    first_name: str
    last_name: str
    tenant_id: Optional[int] = None
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    """User update request schema."""
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserInDB(BaseModel):
    """User database schema."""
    user_id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr
from uuid import UUID


class UserBase(BaseModel):
    """Base User schema."""
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: constr(min_length=8)
    tenant_id: Optional[int] = None
    role_ids: Optional[List[int]] = []


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[constr(min_length=8)] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserInDB(UserBase):
    """Schema for user stored in database."""
    UserID: int
    CreatedAt: datetime
    LastLoginAt: Optional[datetime] = None
    TwoFactorEnabled: bool = False

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"
    requires_2fa: bool = False


class TokenData(BaseModel):
    """Schema for token payload."""
    email: str
    tenant_id: Optional[int] = None
    scopes: List[str] = []

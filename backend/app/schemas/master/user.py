from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    """Base User schema."""
    username: constr(min_length=3, max_length=100)
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: constr(min_length=8)
    tenant_id: int
    role_ids: List[int]


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    username: Optional[constr(min_length=3, max_length=100)] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[constr(min_length=8)] = None


class UserInDB(UserBase):
    """Schema for user stored in database."""
    user_id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    two_factor_enabled: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"
    requires_2fa: bool = False


class TokenData(BaseModel):
    """Schema for token payload."""
    username: str
    tenant_id: Optional[int] = None
    scopes: List[str] = []

from pydantic import BaseModel, UUID4, Field, EmailStr
from typing import Optional
from datetime import datetime

class TenantBase(BaseModel):
    """Base schema for tenant data."""
    name: str = Field(..., min_length=1, max_length=100)
    subdomain: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True

class TenantCreate(TenantBase):
    """Schema for creating a new tenant."""
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8)
    admin_full_name: str

class TenantUpdate(BaseModel):
    """Schema for updating a tenant."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    subdomain: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None

class TenantInDB(TenantBase):
    """Schema for tenant data as stored in database."""
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TenantResponse(TenantInDB):
    """Schema for tenant response."""
    pass

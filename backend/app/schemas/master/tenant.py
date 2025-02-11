from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


class TenantBase(BaseModel):
    """Base Tenant schema."""
    name: constr(min_length=1, max_length=100)
    database_name: constr(min_length=1, max_length=100)
    is_active: bool = True
    settings: Optional[str] = None


class TenantCreate(TenantBase):
    """Schema for creating a new tenant."""
    pass


class TenantUpdate(TenantBase):
    """Schema for updating a tenant."""
    name: Optional[constr(min_length=1, max_length=100)] = None
    database_name: Optional[constr(min_length=1, max_length=100)] = None
    is_active: Optional[bool] = None


class TenantInDB(TenantBase):
    """Schema for tenant stored in database."""
    tenant_id: int
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True

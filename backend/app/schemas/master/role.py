from typing import Optional, List
from pydantic import BaseModel, constr


class PermissionBase(BaseModel):
    """Base Permission schema."""
    code: constr(min_length=1, max_length=100)
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    """Schema for creating a new permission."""
    pass


class PermissionInDB(PermissionBase):
    """Schema for permission stored in database."""
    permission_id: int

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    """Base Role schema."""
    name: constr(min_length=1, max_length=100)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a new role."""
    permission_ids: List[int]


class RoleUpdate(RoleBase):
    """Schema for updating a role."""
    name: Optional[constr(min_length=1, max_length=100)] = None
    permission_ids: Optional[List[int]] = None


class RoleInDB(RoleBase):
    """Schema for role stored in database."""
    role_id: int
    permissions: List[PermissionInDB]

    class Config:
        from_attributes = True


class UserTenantRoleCreate(BaseModel):
    """Schema for assigning role to user in tenant."""
    user_id: int
    tenant_id: int
    role_id: int

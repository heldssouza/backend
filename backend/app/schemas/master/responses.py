"""Response schemas for the API."""
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.master.role import RoleInDB
from app.schemas.master.user import UserInDB


class RoleResponse(RoleInDB):
    """Schema for role response."""
    pass


class UserResponse(UserInDB):
    """Schema for user response."""
    roles: List[RoleResponse] = []

"""Master models package."""
from app.models.master.tenant import Tenant
from app.models.master.user import User
from app.models.master.role import Role
from app.models.master.permission import Permission
from app.models.master.association_tables import UserRoles, RolePermissions

__all__ = ["Tenant", "User", "Role", "Permission", "UserRoles", "RolePermissions"]

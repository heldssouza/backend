"""Permission constants."""
from enum import Enum


class PermissionCode(str, Enum):
    """Permission codes."""
    # User permissions
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    
    # Role permissions
    CREATE_ROLE = "create_role"
    READ_ROLE = "read_role"
    UPDATE_ROLE = "update_role"
    DELETE_ROLE = "delete_role"
    
    # Tenant permissions
    CREATE_TENANT = "create_tenant"
    READ_TENANT = "read_tenant"
    UPDATE_TENANT = "update_tenant"
    DELETE_TENANT = "delete_tenant"


PERMISSIONS = [
    # User permissions
    {
        "name": "Create User",
        "code": PermissionCode.CREATE_USER,
        "description": "Create new users"
    },
    {
        "name": "Read User",
        "code": PermissionCode.READ_USER,
        "description": "View user information"
    },
    {
        "name": "Update User",
        "code": PermissionCode.UPDATE_USER,
        "description": "Update user information"
    },
    {
        "name": "Delete User",
        "code": PermissionCode.DELETE_USER,
        "description": "Delete users"
    },
    
    # Role permissions
    {
        "name": "Create Role",
        "code": PermissionCode.CREATE_ROLE,
        "description": "Create new roles"
    },
    {
        "name": "Read Role",
        "code": PermissionCode.READ_ROLE,
        "description": "View role information"
    },
    {
        "name": "Update Role",
        "code": PermissionCode.UPDATE_ROLE,
        "description": "Update role information"
    },
    {
        "name": "Delete Role",
        "code": PermissionCode.DELETE_ROLE,
        "description": "Delete roles"
    },
    
    # Tenant permissions
    {
        "name": "Create Tenant",
        "code": PermissionCode.CREATE_TENANT,
        "description": "Create new tenants"
    },
    {
        "name": "Read Tenant",
        "code": PermissionCode.READ_TENANT,
        "description": "View tenant information"
    },
    {
        "name": "Update Tenant",
        "code": PermissionCode.UPDATE_TENANT,
        "description": "Update tenant information"
    },
    {
        "name": "Delete Tenant",
        "code": PermissionCode.DELETE_TENANT,
        "description": "Delete tenants"
    }
]

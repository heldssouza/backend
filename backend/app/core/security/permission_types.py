"""Permission types for RBAC."""
from enum import Enum


class PermissionType(str, Enum):
    """Permission types."""
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

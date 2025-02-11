from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.security.dependencies import get_current_user, get_current_admin_user, get_tenant_id
from app.core.security.permissions import get_permission_checker
from app.services.master.role import RoleService
from app.services.master.audit import AuditService
from app.schemas.master.role import (
    RoleCreate,
    RoleUpdate,
    RoleInDB,
    PermissionBase,
    PermissionCreate,
    PermissionInDB
)
from app.models.master.user import User

router = APIRouter()


@router.get("/", response_model=List[RoleInDB])
async def list_roles(
    current_user: Annotated[User, Depends(get_current_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    tenant_id: int = Depends(get_tenant_id)
):
    """
    List all roles.
    Requires LIST_ROLES permission.
    """
    await permission_checker.require_permission(
        "LIST_ROLES",
        current_user,
        tenant_id
    )
    
    role_service = RoleService(db)
    return role_service.get_roles(tenant_id, skip=skip, limit=limit)


@router.post("/", response_model=RoleInDB, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Create new role.
    Requires MANAGE_ROLES permission and admin access.
    """
    await permission_checker.require_permission(
        "MANAGE_ROLES",
        current_user,
        tenant_id
    )
    
    role_service = RoleService(db)
    audit_service = AuditService(db)
    
    # Check if role name exists
    if role_service.get_role_by_name(role_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role name already exists"
        )
    
    # Create role
    role = role_service.create_role(role_data, tenant_id)
    
    # Log the creation
    audit_service.log_action(
        user=current_user,
        tenant_id=tenant_id,
        action="CREATE_ROLE",
        entity_type="role",
        entity_id=str(role.role_id),
        new_values=role.dict()
    )
    
    return role


@router.get("/{role_id}", response_model=RoleInDB)
async def get_role(
    role_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Get specific role details.
    Requires VIEW_ROLE permission.
    """
    await permission_checker.require_permission(
        "VIEW_ROLE",
        current_user,
        tenant_id
    )
    
    role_service = RoleService(db)
    role = role_service.get_role(role_id, tenant_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role


@router.put("/{role_id}", response_model=RoleInDB)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Update role details.
    Requires MANAGE_ROLES permission and admin access.
    """
    await permission_checker.require_permission(
        "MANAGE_ROLES",
        current_user,
        tenant_id
    )
    
    role_service = RoleService(db)
    audit_service = AuditService(db)
    
    # Get current role data for audit
    old_role = role_service.get_role(role_id, tenant_id)
    if not old_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Update role
    updated_role = role_service.update_role(role_id, role_data, tenant_id)
    if not updated_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update role"
        )
    
    # Log the change
    audit_service.log_action(
        user=current_user,
        tenant_id=tenant_id,
        action="UPDATE_ROLE",
        entity_type="role",
        entity_id=str(role_id),
        old_values=old_role.dict(),
        new_values=updated_role.dict()
    )
    
    return updated_role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Delete role.
    Requires MANAGE_ROLES permission and admin access.
    """
    await permission_checker.require_permission(
        "MANAGE_ROLES",
        current_user,
        tenant_id
    )
    
    role_service = RoleService(db)
    audit_service = AuditService(db)
    
    # Get role data for audit
    role = role_service.get_role(role_id, tenant_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Delete role
    if not role_service.delete_role(role_id, tenant_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not delete role"
        )
    
    # Log the change
    audit_service.log_action(
        user=current_user,
        tenant_id=tenant_id,
        action="DELETE_ROLE",
        entity_type="role",
        entity_id=str(role_id),
        old_values=role.dict()
    )


@router.get("/permissions", response_model=List[PermissionInDB])
async def list_permissions(
    current_user: Annotated[User, Depends(get_current_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    tenant_id: int = Depends(get_tenant_id)
):
    """
    List all permissions.
    Requires LIST_PERMISSIONS permission.
    """
    await permission_checker.require_permission(
        "LIST_PERMISSIONS",
        current_user,
        tenant_id
    )
    
    role_service = RoleService(db)
    return role_service.get_permissions(tenant_id, skip=skip, limit=limit)


@router.post("/permissions", response_model=PermissionInDB)
async def create_permission(
    permission_data: PermissionCreate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Create new permission.
    Requires MANAGE_PERMISSIONS permission and admin access.
    """
    await permission_checker.require_permission(
        "MANAGE_PERMISSIONS",
        current_user,
        tenant_id
    )
    
    role_service = RoleService(db)
    audit_service = AuditService(db)
    
    # Check if permission code exists
    if role_service.get_permission_by_code(permission_data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission code already exists"
        )
    
    # Create permission
    permission = role_service.create_permission(
        code=permission_data.code,
        description=permission_data.description,
        tenant_id=tenant_id
    )
    
    # Log the creation
    audit_service.log_action(
        user=current_user,
        tenant_id=tenant_id,
        action="CREATE_PERMISSION",
        entity_type="permission",
        entity_id=str(permission.permission_id),
        new_values=permission.dict()
    )
    
    return permission

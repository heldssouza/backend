from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.security.dependencies import get_current_user, get_current_admin_user, get_tenant_id
from app.core.security.permissions import get_permission_checker
from app.services.master.tenant import TenantService
from app.services.master.audit import AuditService
from app.schemas.master.tenant import TenantCreate, TenantUpdate, TenantInDB
from app.schemas.master.user import UserInDB
from app.models.master.user import User

router = APIRouter()


@router.get("/", response_model=List[TenantInDB])
async def list_tenants(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    List all tenants.
    Requires admin access.
    """
    tenant_service = TenantService(db)
    return tenant_service.get_tenants(skip=skip, limit=limit)


@router.post("/", response_model=TenantInDB, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_data: TenantCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create new tenant.
    Requires admin access.
    """
    tenant_service = TenantService(db)
    audit_service = AuditService(db)
    
    # Check if tenant name exists
    if tenant_service.get_tenant_by_name(tenant_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant name already exists"
        )
    
    # Create tenant
    tenant = tenant_service.create_tenant(tenant_data, current_user)
    
    # Log audit
    await audit_service.log_action(
        action="CREATE_TENANT",
        entity_type="TENANT",
        entity_id=tenant.id,
        user_id=current_user.id,
        tenant_id=tenant.id,
        changes=tenant_data.model_dump()
    )
    
    return tenant


@router.get("/{tenant_id}", response_model=TenantInDB)
async def get_tenant(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db)
):
    """
    Get specific tenant details.
    Requires VIEW_TENANT permission.
    """
    await permission_checker.require_permission(
        "VIEW_TENANT",
        current_user,
        tenant_id
    )
    
    tenant_service = TenantService(db)
    tenant = tenant_service.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    return tenant


@router.put("/{tenant_id}", response_model=TenantInDB)
async def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update tenant details.
    Requires admin access.
    """
    tenant_service = TenantService(db)
    audit_service = AuditService(db)
    
    # Get existing tenant
    tenant = tenant_service.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    # Update tenant
    updated_tenant = tenant_service.update_tenant(tenant_id, tenant_data)
    
    # Log audit
    await audit_service.log_action(
        action="UPDATE_TENANT",
        entity_type="TENANT",
        entity_id=tenant_id,
        user_id=current_user.id,
        tenant_id=tenant_id,
        changes=tenant_data.model_dump()
    )
    
    return updated_tenant


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete tenant (soft delete).
    Requires admin access.
    """
    tenant_service = TenantService(db)
    audit_service = AuditService(db)
    
    # Get existing tenant
    tenant = tenant_service.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    # Delete tenant
    tenant_service.delete_tenant(tenant_id)
    
    # Log audit
    await audit_service.log_action(
        action="DELETE_TENANT",
        entity_type="TENANT",
        entity_id=tenant_id,
        user_id=current_user.id,
        tenant_id=tenant_id
    )


@router.get("/{tenant_id}/users", response_model=List[UserInDB])
async def get_tenant_users(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get users in tenant.
    Requires LIST_TENANT_USERS permission.
    """
    await permission_checker.require_permission(
        "LIST_TENANT_USERS",
        current_user,
        tenant_id
    )
    
    tenant_service = TenantService(db)
    return tenant_service.get_tenant_users(tenant_id, skip=skip, limit=limit)

from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.security.dependencies import get_current_user, get_current_admin_user, get_tenant_id
from app.core.security.permissions import get_permission_checker
from app.services.master.user import UserService
from app.services.master.audit import AuditService
from app.schemas.master.user import UserCreate, UserUpdate, UserInDB
from app.models.master.user import User

router = APIRouter()


@router.get("/", response_model=List[UserInDB])
async def list_users(
    current_user: Annotated[User, Depends(get_current_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    tenant_id: int = Depends(get_tenant_id)
):
    """
    List users in tenant.
    Requires LIST_USERS permission.
    """
    await permission_checker.require_permission(
        "LIST_USERS",
        current_user,
        tenant_id
    )
    
    user_service = UserService(db)
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserInDB)
async def get_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Get specific user details.
    Requires VIEW_USER permission.
    """
    await permission_checker.require_permission(
        "VIEW_USER",
        current_user,
        tenant_id
    )

    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Update user details.
    Requires UPDATE_USER permission.
    """
    await permission_checker.require_permission(
        "UPDATE_USER",
        current_user,
        tenant_id
    )

    user_service = UserService(db)
    audit_service = AuditService(db)

    # Get current user data for audit
    current_data = user_service.get_user(user_id)
    if not current_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user
    updated_user = user_service.update_user(user_id, user_data)

    # Log audit
    await audit_service.log_change(
        user_id=current_user.id,
        action="UPDATE",
        table_name="users",
        record_id=str(user_id),
        old_values=current_data.model_dump(),
        new_values=updated_user.model_dump(),
        tenant_id=tenant_id
    )

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Delete user (soft delete).
    Requires DELETE_USER permission and admin access.
    """
    await permission_checker.require_permission(
        "DELETE_USER",
        current_user,
        tenant_id
    )

    user_service = UserService(db)
    audit_service = AuditService(db)

    # Get current user data for audit
    current_data = user_service.get_user(user_id)
    if not current_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete user
    user_service.delete_user(user_id)

    # Log audit
    await audit_service.log_change(
        user_id=current_user.id,
        action="DELETE",
        table_name="users",
        record_id=str(user_id),
        old_values=current_data.model_dump(),
        new_values={"is_active": False},
        tenant_id=tenant_id
    )


@router.post("/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def assign_role(
    user_id: int,
    role_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    permission_checker = Depends(get_permission_checker),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id)
):
    """
    Assign role to user.
    Requires MANAGE_USER_ROLES permission and admin access.
    """
    await permission_checker.require_permission(
        "MANAGE_USER_ROLES",
        current_user,
        tenant_id
    )

    user_service = UserService(db)
    audit_service = AuditService(db)

    # Assign role
    user_service.assign_role(user_id, role_id)

    # Log audit
    await audit_service.log_change(
        user_id=current_user.id,
        action="ASSIGN_ROLE",
        table_name="user_roles",
        record_id=f"{user_id}_{role_id}",
        old_values={},
        new_values={"user_id": user_id, "role_id": role_id},
        tenant_id=tenant_id
    )

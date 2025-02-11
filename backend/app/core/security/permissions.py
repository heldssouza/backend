from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.models.master.user import User
from app.models.master.permission import Permission
from app.models.master.role import Role


class PermissionChecker:
    """Check user permissions in specific tenant context."""

    def __init__(self, db: Session):
        self.db = db

    async def check_permission(
        self,
        user_id: int,
        tenant_id: int,
        permission_code: str
    ) -> bool:
        """
        Check if user has specific permission in tenant.

        Args:
            user_id: User ID
            tenant_id: Tenant ID
            permission_code: Permission code to check

        Returns:
            bool: True if user has permission, False otherwise
        """
        # Get user's roles in tenant
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return False

        # Check if any of user's roles has the required permission
        for role in user.roles:
            if role.tenant_id != tenant_id:
                continue
            
            for permission in role.permissions:
                if permission.code == permission_code:
                    return True

        return False

    async def require_permission(
        self,
        permission_code: str,
        user: User,
        tenant_id: Optional[int] = None,
    ) -> None:
        """
        Require specific permission to proceed.

        Args:
            permission_code: Required permission code
            user: Current user
            tenant_id: Optional tenant ID

        Raises:
            HTTPException: If user doesn't have required permission
        """
        # Superusers bypass permission check
        if user.is_superuser:
            return

        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant ID is required"
            )

        has_permission = await self.check_permission(
            user.user_id,
            tenant_id,
            permission_code
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )


def get_permission_checker(db: Session = Depends(get_db)) -> PermissionChecker:
    """Dependency for getting permission checker."""
    return PermissionChecker(db)

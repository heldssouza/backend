from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.master.role import Role, Permission
from app.schemas.master.role import RoleCreate, RoleUpdate


class RoleService:
    """Service for role and permission operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_role(self, role_id: int) -> Optional[Role]:
        """Get role by ID."""
        return self.db.query(Role).filter(Role.role_id == role_id).first()

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Get role by name."""
        return self.db.query(Role).filter(Role.name == name).first()

    def get_roles(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Role]:
        """Get list of roles."""
        return self.db.query(Role).offset(skip).limit(limit).all()

    def create_role(self, role_data: RoleCreate) -> Role:
        """Create new role."""
        # Create role
        db_role = Role(
            name=role_data.name,
            description=role_data.description
        )
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)

        # Assign permissions
        if role_data.permission_ids:
            permissions = (
                self.db.query(Permission)
                .filter(Permission.permission_id.in_(role_data.permission_ids))
                .all()
            )
            db_role.permissions = permissions
            self.db.commit()

        return db_role

    def update_role(
        self,
        role_id: int,
        role_data: RoleUpdate
    ) -> Optional[Role]:
        """Update role."""
        db_role = self.get_role(role_id)
        if not db_role:
            return None

        update_data = role_data.model_dump(exclude_unset=True)
        
        # Update basic fields
        for field in ["name", "description"]:
            if field in update_data:
                setattr(db_role, field, update_data[field])

        # Update permissions if provided
        if "permission_ids" in update_data:
            permissions = (
                self.db.query(Permission)
                .filter(Permission.permission_id.in_(update_data["permission_ids"]))
                .all()
            )
            db_role.permissions = permissions

        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def delete_role(self, role_id: int) -> bool:
        """Delete role."""
        db_role = self.get_role(role_id)
        if not db_role:
            return False

        self.db.delete(db_role)
        self.db.commit()
        return True

    def get_permission(self, permission_id: int) -> Optional[Permission]:
        """Get permission by ID."""
        return (
            self.db.query(Permission)
            .filter(Permission.permission_id == permission_id)
            .first()
        )

    def get_permission_by_code(self, code: str) -> Optional[Permission]:
        """Get permission by code."""
        return (
            self.db.query(Permission)
            .filter(Permission.code == code)
            .first()
        )

    def get_permissions(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Permission]:
        """Get list of permissions."""
        return self.db.query(Permission).offset(skip).limit(limit).all()

    def create_permission(
        self,
        code: str,
        description: Optional[str] = None
    ) -> Permission:
        """Create new permission."""
        db_permission = Permission(code=code, description=description)
        self.db.add(db_permission)
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission

    def delete_permission(self, permission_id: int) -> bool:
        """Delete permission."""
        db_permission = self.get_permission(permission_id)
        if not db_permission:
            return False

        self.db.delete(db_permission)
        self.db.commit()
        return True

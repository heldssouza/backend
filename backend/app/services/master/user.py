from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.master.user import User
from app.models.master.role import Role
from app.models.master.user_tenant import UserTenantRole
from app.schemas.master.user import UserCreate, UserUpdate
from app.services.master.auth import AuthService


class UserService:
    """Service for user operations."""

    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService(db)

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[User]:
        """Get list of users."""
        query = self.db.query(User)
        if active_only:
            query = query.filter(User.is_active == True)
        return query.offset(skip).limit(limit).all()

    def create_user(self, user_data: UserCreate) -> User:
        """Create new user."""
        # Hash the password
        hashed_password = self.auth_service.get_password_hash(user_data.password)
        
        # Create user
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        # Assign roles in tenant
        for role_id in user_data.role_ids:
            user_tenant_role = UserTenantRole(
                user_id=db_user.user_id,
                tenant_id=user_data.tenant_id,
                role_id=role_id
            )
            self.db.add(user_tenant_role)
        
        self.db.commit()
        return db_user

    def update_user(
        self,
        user_id: int,
        user_data: UserUpdate
    ) -> Optional[User]:
        """Update user."""
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        
        # Hash password if it's being updated
        if "password" in update_data:
            update_data["password_hash"] = self.auth_service.get_password_hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        db_user = self.get_user(user_id)
        if not db_user:
            return False

        # Soft delete - just mark as inactive
        db_user.is_active = False
        self.db.commit()
        return True

    def assign_role(
        self,
        user_id: int,
        role_id: int,
        tenant_id: int
    ) -> Optional[Role]:
        """Assign role to user in tenant."""
        # Check if role exists
        role = self.db.query(Role).filter(Role.role_id == role_id).first()
        if not role:
            return None

        # Check if user already has this role in this tenant
        existing = self.db.query(UserTenantRole).filter(
            UserTenantRole.user_id == user_id,
            UserTenantRole.role_id == role_id,
            UserTenantRole.tenant_id == tenant_id
        ).first()

        if not existing:
            # Create new user-tenant-role association
            user_tenant_role = UserTenantRole(
                user_id=user_id,
                tenant_id=tenant_id,
                role_id=role_id
            )
            self.db.add(user_tenant_role)
            self.db.commit()

        return role

    def get_user_roles(
        self,
        user_id: int,
        tenant_id: int
    ) -> List[Role]:
        """Get user roles in tenant."""
        return self.db.query(Role).join(
            UserTenantRole,
            Role.role_id == UserTenantRole.role_id
        ).filter(
            UserTenantRole.user_id == user_id,
            UserTenantRole.tenant_id == tenant_id
        ).all()

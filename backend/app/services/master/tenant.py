from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.master.tenant import Tenant
from app.models.master.user import User
from app.schemas.master.tenant import TenantCreate, TenantUpdate


class TenantService:
    """Service for tenant operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_tenant(self, tenant_id: int) -> Optional[Tenant]:
        """Get tenant by ID."""
        return self.db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()

    def get_tenant_by_name(self, name: str) -> Optional[Tenant]:
        """Get tenant by name."""
        return self.db.query(Tenant).filter(Tenant.name == name).first()

    def get_tenants(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[Tenant]:
        """Get list of tenants."""
        query = self.db.query(Tenant)
        if active_only:
            query = query.filter(Tenant.is_active == True)
        return query.offset(skip).limit(limit).all()

    def create_tenant(
        self,
        tenant_data: TenantCreate,
        created_by: User
    ) -> Tenant:
        """Create new tenant."""
        db_tenant = Tenant(
            **tenant_data.model_dump(),
            created_by=created_by.user_id
        )
        self.db.add(db_tenant)
        self.db.commit()
        self.db.refresh(db_tenant)
        return db_tenant

    def update_tenant(
        self,
        tenant_id: int,
        tenant_data: TenantUpdate
    ) -> Optional[Tenant]:
        """Update tenant."""
        db_tenant = self.get_tenant(tenant_id)
        if not db_tenant:
            return None

        update_data = tenant_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tenant, field, value)

        self.db.commit()
        self.db.refresh(db_tenant)
        return db_tenant

    def delete_tenant(self, tenant_id: int) -> bool:
        """Delete tenant."""
        db_tenant = self.get_tenant(tenant_id)
        if not db_tenant:
            return False

        # Soft delete - just mark as inactive
        db_tenant.is_active = False
        self.db.commit()
        return True

    def get_tenant_users(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get users in tenant."""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return []
        
        return (
            self.db.query(User)
            .join(User.tenant_roles)
            .filter(User.tenant_roles.any(tenant_id=tenant_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

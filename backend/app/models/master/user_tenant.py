from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db.base import Base


class UserTenantRole(Base):
    """Association model for User-Tenant-Role relationship."""
    
    __tablename__ = "user_tenant_roles"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)

    # Relationships
    user = relationship("User", back_populates="tenant_roles")
    tenant = relationship("Tenant", back_populates="users")
    role = relationship("Role", back_populates="user_tenant_roles")

    def __repr__(self):
        return f"<UserTenantRole user_id={self.user_id} tenant_id={self.tenant_id} role_id={self.role_id}>"

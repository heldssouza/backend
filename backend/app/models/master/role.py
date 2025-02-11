"""Role model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import List
from app.core.db.base import Base
from app.models.master.permission import Permission


class Role(Base):
    """Role model."""
    
    __tablename__ = "Roles"
    __table_args__ = {"schema": "dbo"}

    RoleID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Description = Column(String(255))
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    TenantID = Column(Integer, ForeignKey("dbo.Tenants.TenantID"), nullable=False)

    # Relationships
    Tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="Roles")
    Users: Mapped[List["User"]] = relationship("User", secondary="dbo.UserRoles", back_populates="Roles")
    Permissions: Mapped[List[Permission]] = relationship(Permission, secondary="dbo.RolePermissions", back_populates="Roles")

    def __repr__(self):
        return f"<Role {self.Name}>"

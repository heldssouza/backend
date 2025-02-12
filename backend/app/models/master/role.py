"""Role model."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.db.base import Base
from app.models.master.permission import Permission


class Role(Base):
    """Role model."""
    
    __tablename__ = "Roles"
    __table_args__ = {"schema": "dbo"}

    RoleID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Name: Mapped[str] = mapped_column(String(100), nullable=False)
    Description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    TenantID: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dbo.Tenants.TenantID"),
        nullable=False,
        index=True
    )
    IsActive: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('1'),
        nullable=False
    )
    CreatedAt: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text('GETDATE()'),
        nullable=False
    )
    CreatedBy: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("dbo.Users.UserID"),
        nullable=True
    )
    UpdatedAt: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text('GETDATE()'),
        nullable=False
    )
    UpdatedBy: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("dbo.Users.UserID"),
        nullable=True
    )
    IsDeleted: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('0'),
        nullable=False,
        index=True
    )

    # Regular relationships
    Tenant: Mapped["Tenant"] = relationship(
        "Tenant",
        back_populates="Roles",
        foreign_keys=[TenantID]
    )
    Users: Mapped[List["User"]] = relationship(
        "User",
        secondary="dbo.UserRoles",
        back_populates="Roles"
    )
    Permissions: Mapped[List[Permission]] = relationship(
        Permission,
        secondary="dbo.RolePermissions",
        back_populates="Roles"
    )

    def __repr__(self):
        return f"<Role {self.Name}>"

"""Tenant model."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.db.base import Base


class Tenant(Base):
    """Tenant model following SQL Server conventions."""
    
    __tablename__ = "Tenants"
    __table_args__ = {"schema": "dbo"}

    TenantID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Name: Mapped[str] = mapped_column(String(100), nullable=False)
    Subdomain: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
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

    # Self-referential relationships
    created_by_user = relationship(
        "User",
        foreign_keys=[CreatedBy],
        backref="created_tenants"
    )
    updated_by_user = relationship(
        "User",
        foreign_keys=[UpdatedBy],
        backref="updated_tenants"
    )

    # Regular relationships
    Users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="Tenant",
        foreign_keys="[User.TenantID]"
    )
    Roles: Mapped[List["Role"]] = relationship(
        "Role",
        back_populates="Tenant",
        foreign_keys="[Role.TenantID]"
    )

    def __repr__(self):
        return f"<Tenant {self.Name}>"

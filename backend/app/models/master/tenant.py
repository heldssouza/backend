"""Tenant model."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID
from app.core.db.base import Base


class Tenant(Base):
    """Tenant model following SQL Server conventions."""
    
    __tablename__ = "Tenants"
    __table_args__ = {"schema": "dbo"}

    TenantID: Mapped[UUID] = mapped_column(UNIQUEIDENTIFIER, primary_key=True, index=True)
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
    UpdatedAt: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text('GETDATE()'),
        nullable=False
    )
    IsDeleted: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('0'),
        nullable=False,
        index=True
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

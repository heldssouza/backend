"""User model."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, ForeignKey, text, DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID
from app.models.master.base_model import BaseModel


class User(BaseModel):
    """User model following SQL Server conventions."""
    
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    UserID: Mapped[UUID] = mapped_column(UNIQUEIDENTIFIER, primary_key=True, index=True)
    Email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    Username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    HashedPassword: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    FirstName: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    LastName: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    IsActive: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('1'),
        nullable=False
    )
    IsSuperuser: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('0'),
        nullable=False
    )
    TenantID: Mapped[UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        ForeignKey("dbo.Tenants.TenantID"),
        nullable=False,
        index=True
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
        index=True,
        default=False
    )

    # Relacionamentos regulares
    Tenant: Mapped["Tenant"] = relationship(
        "Tenant",
        foreign_keys=[TenantID],
        back_populates="Users"
    )
    Roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary="dbo.UserRoles",
        back_populates="Users"
    )
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    two_factor_auth: Mapped[Optional["TwoFactorAuth"]] = relationship(
        "TwoFactorAuth",
        back_populates="user",
        uselist=False
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.Email}>"

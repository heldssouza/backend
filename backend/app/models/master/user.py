"""User model."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.master.base_model import BaseModel


class User(BaseModel):
    """User model following SQL Server conventions."""
    
    __tablename__ = "Users"

    UserID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Email: Mapped[str] = mapped_column(
        String(100, collation='Latin1_General_CI_AI'),
        unique=True,
        nullable=False,
        index=True
    )
    HashedPassword: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    FirstName: Mapped[Optional[str]] = mapped_column(
        String(100, collation='Latin1_General_CI_AI')
    )
    LastName: Mapped[Optional[str]] = mapped_column(
        String(100, collation='Latin1_General_CI_AI')
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
    TenantID: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dbo.Tenants.TenantID"),
        nullable=False,
        index=True
    )

    # Relationships
    Tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="Users")
    Roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary="dbo.UserRoles",
        back_populates="Users",
        lazy="selectin"  # Eager loading for roles
    )

    def __repr__(self) -> str:
        """String representation of the user."""
        return f"<User {self.Email}>"

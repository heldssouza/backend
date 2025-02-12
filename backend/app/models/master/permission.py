"""Permission model."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.db.base import Base


class Permission(Base):
    """Permission model."""
    
    __tablename__ = "Permissions"
    __table_args__ = {"schema": "dbo"}

    PermissionID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Name: Mapped[str] = mapped_column(String(100), nullable=False)
    Code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    Description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
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
    Roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary="dbo.RolePermissions",
        back_populates="Permissions"
    )

    def __repr__(self):
        return f"<Permission {self.Name}>"

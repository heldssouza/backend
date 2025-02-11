"""Permission model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped
from typing import List
from app.core.db.base import Base


class Permission(Base):
    """Permission model."""
    
    __tablename__ = "Permissions"
    __table_args__ = {"schema": "dbo"}

    PermissionID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Code = Column(String(100), unique=True, nullable=False)
    Description = Column(String(255))
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    Roles: Mapped[List["Role"]] = relationship("Role", secondary="dbo.RolePermissions", back_populates="Permissions")

    def __repr__(self):
        return f"<Permission {self.Name}>"

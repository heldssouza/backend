"""Tenant model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped
from typing import List
from app.core.db.base import Base


class Tenant(Base):
    """Tenant model."""
    
    __tablename__ = "Tenants"
    __table_args__ = {"schema": "dbo"}

    TenantID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Domain = Column(String(100), nullable=False)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    Users: Mapped[List["User"]] = relationship("User", back_populates="Tenant")
    Roles: Mapped[List["Role"]] = relationship("Role", back_populates="Tenant")

    def __repr__(self):
        return f"<Tenant {self.Name}>"

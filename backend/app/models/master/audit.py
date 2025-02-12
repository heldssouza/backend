"""Audit log model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, text
from sqlalchemy.orm import relationship, Mapped
from app.core.db.base import Base


class AuditLog(Base):
    """Audit log for tracking system activities."""
    
    __tablename__ = "AuditLogs"
    __table_args__ = {"schema": "dbo"}

    AuditLogID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("dbo.Users.UserID"))
    TenantID = Column(Integer, ForeignKey("dbo.Tenants.TenantID"))
    Action = Column(String(100), nullable=False)
    EntityType = Column(String(50))  # Type of entity being acted upon
    EntityID = Column(String(50))    # ID of entity being acted upon
    OldValues = Column(JSON)         # Previous values in case of updates
    NewValues = Column(JSON)         # New values in case of updates
    IPAddress = Column(String(50))
    UserAgent = Column(String(255))
    CreatedAt = Column(DateTime, server_default=text('GETDATE()'))
    AdditionalData = Column(JSON)    # Any additional context

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="audit_logs")
    tenant: Mapped["Tenant"] = relationship("Tenant")

    def __repr__(self):
        return f"<AuditLog {self.Action} by UserID={self.UserID}>"

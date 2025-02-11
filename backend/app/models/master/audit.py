from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.db.base import Base


class AuditLog(Base):
    """Audit log for tracking system activities."""
    
    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"))
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))  # Type of entity being acted upon
    entity_id = Column(String(50))    # ID of entity being acted upon
    old_values = Column(JSON)         # Previous values in case of updates
    new_values = Column(JSON)         # New values in case of updates
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    additional_data = Column(JSON)    # Any additional context

    # Relationships
    user = relationship("User", back_populates="audit_logs")
    tenant = relationship("Tenant")

    def __repr__(self):
        return f"<AuditLog {self.action} by user_id={self.user_id}>"

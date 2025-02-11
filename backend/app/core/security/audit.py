from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.models.base import BaseModel
from datetime import datetime
from typing import Dict, Any
import json

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    
    user_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    table_name = Column(String(100), nullable=False)
    record_id = Column(String(50), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(200))
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

class AuditTrail:
    @staticmethod
    def log_change(
        session,
        user_id: int,
        action: str,
        table_name: str,
        record_id: str,
        old_values: Dict[str, Any] = None,
        new_values: Dict[str, Any] = None,
        ip_address: str = None,
        user_agent: str = None
    ):
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=json.dumps(old_values) if old_values else None,
            new_values=json.dumps(new_values) if new_values else None,
            ip_address=ip_address,
            user_agent=user_agent
        )
        session.add(audit_log)
        session.flush()

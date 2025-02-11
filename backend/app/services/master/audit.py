from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.master.audit import AuditLog
from app.models.master.user import User


class AuditService:
    """Service for audit operations."""

    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        user: User,
        tenant_id: int,
        action: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Create audit log entry."""
        audit_log = AuditLog(
            user_id=user.user_id,
            tenant_id=tenant_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            additional_data=additional_data
        )
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        return audit_log

    def get_audit_logs(
        self,
        tenant_id: int,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get audit logs with filters."""
        query = self.db.query(AuditLog).filter(AuditLog.tenant_id == tenant_id)

        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        if entity_id:
            query = query.filter(AuditLog.entity_id == entity_id)
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)

        return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()

    def get_audit_log(self, log_id: int) -> Optional[AuditLog]:
        """Get audit log by ID."""
        return self.db.query(AuditLog).filter(AuditLog.log_id == log_id).first()

    def get_user_actions(
        self,
        user_id: int,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get all actions performed by a user in a tenant."""
        return (
            self.db.query(AuditLog)
            .filter(
                AuditLog.user_id == user_id,
                AuditLog.tenant_id == tenant_id
            )
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_entity_history(
        self,
        entity_type: str,
        entity_id: str,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get history of changes for an entity."""
        return (
            self.db.query(AuditLog)
            .filter(
                AuditLog.entity_type == entity_type,
                AuditLog.entity_id == entity_id,
                AuditLog.tenant_id == tenant_id
            )
            .order_by(AuditLog.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

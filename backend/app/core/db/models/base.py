from sqlalchemy import Column, DateTime, Boolean, Integer, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AuditableModel(Base):
    """Base model with audit fields."""
    __abstract__ = True
    
    created_at = Column(DateTime, server_default=text('GETDATE()'), nullable=False)
    created_by = Column(Integer, nullable=True)  # Removida FK temporariamente
    updated_at = Column(DateTime, server_default=text('GETDATE()'), nullable=False)
    updated_by = Column(Integer, nullable=True)  # Removida FK temporariamente
    is_deleted = Column(Boolean, server_default=text('0'), nullable=False)

class TenantModel(AuditableModel):
    """Base model for tenant-specific tables."""
    __abstract__ = True
    
    tenant_id = Column(Integer, ForeignKey('dbo.Tenants.id'), nullable=False, index=True)

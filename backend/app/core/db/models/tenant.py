from sqlalchemy import Column, String, Boolean, Integer, text
from .base import AuditableModel

class Tenant(AuditableModel):
    """Model for tenant information."""
    __tablename__ = 'Tenants'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    subdomain = Column(String(100), nullable=False, unique=True)
    database_name = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, server_default=text('1'), nullable=False)

from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, JSON, text
from sqlalchemy.orm import relationship
from ..db.models.base import TenantModel

class TwoFactorAuth(TenantModel):
    """Model for two-factor authentication settings."""
    __tablename__ = 'TwoFactorAuth'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('dbo.Users.id'), nullable=False, unique=True)
    secret = Column(String(32), nullable=False)
    is_enabled = Column(Boolean, server_default=text('0'), nullable=False)
    backup_codes = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="two_factor_auth")

class RefreshToken(TenantModel):
    """Model for refresh tokens."""
    __tablename__ = 'RefreshTokens'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('dbo.Users.id'), nullable=False)
    token = Column(String(64), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, server_default=text('0'), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")

class SecurityLog(TenantModel):
    """Model for security audit logs."""
    __tablename__ = 'SecurityLogs'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('dbo.Users.id'), nullable=True)
    event_type = Column(String(50), nullable=False)  # LOGIN, PASSWORD_CHANGE, etc
    ip_address = Column(String(45))
    user_agent = Column(String(200))
    status = Column(String(20), nullable=False)  # SUCCESS, FAILED
    details = Column(JSON)
    
    # Relationships
    user = relationship("User")

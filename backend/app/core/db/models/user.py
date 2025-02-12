from sqlalchemy import Column, String, Boolean, Integer, text
from sqlalchemy.orm import relationship
from .base import TenantModel

class User(TenantModel):
    """Model for user information."""
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_active = Column(Boolean, server_default=text('1'), nullable=False)
    is_superuser = Column(Boolean, server_default=text('0'), nullable=False)
    
    # Relationships
    roles = relationship("Role", secondary="dbo.UserRoles", back_populates="users")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    two_factor_auth = relationship("TwoFactorAuth", back_populates="user", uselist=False)

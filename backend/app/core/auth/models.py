from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table, text
from sqlalchemy.orm import relationship
from ..db.models.base import TenantModel, Base

class Permission(Base):
    """Model for system permissions."""
    __tablename__ = 'Permissions'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    
    # Relationships
    roles = relationship("Role", secondary="dbo.RolePermissions", back_populates="permissions")

class Role(TenantModel):
    """Model for user roles."""
    __tablename__ = 'Roles'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, server_default=text('1'), nullable=False)
    
    # Relationships
    users = relationship("User", secondary="dbo.UserRoles", back_populates="roles")
    permissions = relationship("Permission", secondary="dbo.RolePermissions", back_populates="roles")

# Association Tables
role_permissions = Table('RolePermissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('dbo.Roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('dbo.Permissions.id'), primary_key=True),
    schema='dbo'
)

user_roles = Table('UserRoles', Base.metadata,
    Column('user_id', Integer, ForeignKey('dbo.Users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('dbo.Roles.id'), primary_key=True),
    schema='dbo'
)

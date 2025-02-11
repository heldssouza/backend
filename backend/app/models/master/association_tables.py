"""Association tables for many-to-many relationships."""
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.db.base import Base


# Association table for User-Role relationship
UserRoles = Table(
    "UserRoles",
    Base.metadata,
    Column("UserID", Integer, ForeignKey("dbo.Users.UserID"), primary_key=True),
    Column("RoleID", Integer, ForeignKey("dbo.Roles.RoleID"), primary_key=True),
    schema="dbo"
)

# Association table for Role-Permission relationship
RolePermissions = Table(
    "RolePermissions",
    Base.metadata,
    Column("RoleID", Integer, ForeignKey("dbo.Roles.RoleID"), primary_key=True),
    Column("PermissionID", Integer, ForeignKey("dbo.Permissions.PermissionID"), primary_key=True),
    schema="dbo"
)

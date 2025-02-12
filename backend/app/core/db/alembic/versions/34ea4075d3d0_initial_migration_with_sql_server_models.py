"""Initial migration with SQL Server models

Revision ID: 34ea4075d3d0
Revises: 4e6758a3365c
Create Date: 2025-02-11 20:24:03.897863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34ea4075d3d0'
down_revision: Union[str, None] = '4e6758a3365c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Tenants',
    sa.Column('TenantID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=100), nullable=False),
    sa.Column('Subdomain', sa.String(length=100), nullable=False),
    sa.Column('IsActive', sa.Boolean(), server_default=sa.text('1'), nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
    sa.Column('CreatedBy', sa.Integer(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
    sa.Column('UpdatedBy', sa.Integer(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.PrimaryKeyConstraint('TenantID', name=op.f('pk_Tenants')),
    sa.UniqueConstraint('Subdomain', name=op.f('uq_Tenants_Subdomain')),
    schema='dbo'
    )
    op.create_index(op.f('ix_dbo_Tenants_IsDeleted'), 'Tenants', ['IsDeleted'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_Tenants_TenantID'), 'Tenants', ['TenantID'], unique=False, schema='dbo')
    op.create_table('Users',
    sa.Column('UserID', sa.Integer(), nullable=False),
    sa.Column('Email', sa.String(length=100), nullable=False),
    sa.Column('HashedPassword', sa.String(length=100), nullable=False),
    sa.Column('FirstName', sa.String(length=100), nullable=True),
    sa.Column('LastName', sa.String(length=100), nullable=True),
    sa.Column('IsActive', sa.Boolean(), server_default=sa.text('1'), nullable=False),
    sa.Column('IsSuperuser', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.Column('TenantID', sa.Integer(), nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
    sa.Column('CreatedBy', sa.Integer(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
    sa.Column('UpdatedBy', sa.Integer(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.Users.UserID'], name=op.f('fk_Users_CreatedBy_Users')),
    sa.ForeignKeyConstraint(['TenantID'], ['dbo.Tenants.TenantID'], name=op.f('fk_Users_TenantID_Tenants')),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.Users.UserID'], name=op.f('fk_Users_UpdatedBy_Users')),
    sa.PrimaryKeyConstraint('UserID', name=op.f('pk_Users')),
    schema='dbo'
    )
    op.create_index(op.f('ix_dbo_Users_Email'), 'Users', ['Email'], unique=True, schema='dbo')
    op.create_index(op.f('ix_dbo_Users_IsDeleted'), 'Users', ['IsDeleted'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_Users_TenantID'), 'Users', ['TenantID'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_Users_UserID'), 'Users', ['UserID'], unique=False, schema='dbo')
    op.create_table('Permissions',
    sa.Column('PermissionID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=100), nullable=False),
    sa.Column('Code', sa.String(length=100), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('IsActive', sa.Boolean(), server_default=sa.text('1'), nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
    sa.Column('CreatedBy', sa.Integer(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
    sa.Column('UpdatedBy', sa.Integer(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.Users.UserID'], name=op.f('fk_Permissions_CreatedBy_Users')),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.Users.UserID'], name=op.f('fk_Permissions_UpdatedBy_Users')),
    sa.PrimaryKeyConstraint('PermissionID', name=op.f('pk_Permissions')),
    sa.UniqueConstraint('Code', name=op.f('uq_Permissions_Code')),
    schema='dbo'
    )
    op.create_index(op.f('ix_dbo_Permissions_IsDeleted'), 'Permissions', ['IsDeleted'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_Permissions_PermissionID'), 'Permissions', ['PermissionID'], unique=False, schema='dbo')
    op.create_table('Roles',
    sa.Column('RoleID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=100), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('TenantID', sa.Integer(), nullable=False),
    sa.Column('IsActive', sa.Boolean(), server_default=sa.text('1'), nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
    sa.Column('CreatedBy', sa.Integer(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
    sa.Column('UpdatedBy', sa.Integer(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.Users.UserID'], name=op.f('fk_Roles_CreatedBy_Users')),
    sa.ForeignKeyConstraint(['TenantID'], ['dbo.Tenants.TenantID'], name=op.f('fk_Roles_TenantID_Tenants')),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.Users.UserID'], name=op.f('fk_Roles_UpdatedBy_Users')),
    sa.PrimaryKeyConstraint('RoleID', name=op.f('pk_Roles')),
    schema='dbo'
    )
    op.create_index(op.f('ix_dbo_Roles_IsDeleted'), 'Roles', ['IsDeleted'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_Roles_RoleID'), 'Roles', ['RoleID'], unique=False, schema='dbo')
    op.create_index(op.f('ix_dbo_Roles_TenantID'), 'Roles', ['TenantID'], unique=False, schema='dbo')
    op.create_table('RolePermissions',
    sa.Column('RoleID', sa.Integer(), nullable=False),
    sa.Column('PermissionID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['PermissionID'], ['dbo.Permissions.PermissionID'], name=op.f('fk_RolePermissions_PermissionID_Permissions')),
    sa.ForeignKeyConstraint(['RoleID'], ['dbo.Roles.RoleID'], name=op.f('fk_RolePermissions_RoleID_Roles')),
    sa.PrimaryKeyConstraint('RoleID', 'PermissionID', name=op.f('pk_RolePermissions')),
    schema='dbo'
    )
    op.create_table('UserRoles',
    sa.Column('UserID', sa.Integer(), nullable=False),
    sa.Column('RoleID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['RoleID'], ['dbo.Roles.RoleID'], name=op.f('fk_UserRoles_RoleID_Roles')),
    sa.ForeignKeyConstraint(['UserID'], ['dbo.Users.UserID'], name=op.f('fk_UserRoles_UserID_Users')),
    sa.PrimaryKeyConstraint('UserID', 'RoleID', name=op.f('pk_UserRoles')),
    schema='dbo'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserRoles', schema='dbo')
    op.drop_table('RolePermissions', schema='dbo')
    op.drop_index(op.f('ix_dbo_Roles_TenantID'), table_name='Roles', schema='dbo')
    op.drop_index(op.f('ix_dbo_Roles_RoleID'), table_name='Roles', schema='dbo')
    op.drop_index(op.f('ix_dbo_Roles_IsDeleted'), table_name='Roles', schema='dbo')
    op.drop_table('Roles', schema='dbo')
    op.drop_index(op.f('ix_dbo_Permissions_PermissionID'), table_name='Permissions', schema='dbo')
    op.drop_index(op.f('ix_dbo_Permissions_IsDeleted'), table_name='Permissions', schema='dbo')
    op.drop_table('Permissions', schema='dbo')
    op.drop_index(op.f('ix_dbo_Users_UserID'), table_name='Users', schema='dbo')
    op.drop_index(op.f('ix_dbo_Users_TenantID'), table_name='Users', schema='dbo')
    op.drop_index(op.f('ix_dbo_Users_IsDeleted'), table_name='Users', schema='dbo')
    op.drop_index(op.f('ix_dbo_Users_Email'), table_name='Users', schema='dbo')
    op.drop_table('Users', schema='dbo')
    op.drop_index(op.f('ix_dbo_Tenants_TenantID'), table_name='Tenants', schema='dbo')
    op.drop_index(op.f('ix_dbo_Tenants_IsDeleted'), table_name='Tenants', schema='dbo')
    op.drop_table('Tenants', schema='dbo')
    # ### end Alembic commands ###

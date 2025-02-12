"""Create role_permissions table

Revision ID: 006_create_role_permissions
Revises: 005_create_roles
Create Date: 2025-02-12 11:06:10.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006_create_role_permissions'
down_revision = '005_create_roles'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('RolePermissions',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['permission_id'], ['dbo.Permissions.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['dbo.Roles.id'], ),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
        schema='dbo'
    )
    op.create_index('ix_RolePermissions_permission_id', 'RolePermissions', ['permission_id'], schema='dbo')
    op.create_index('ix_RolePermissions_role_id', 'RolePermissions', ['role_id'], schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_RolePermissions_role_id', table_name='RolePermissions', schema='dbo')
    op.drop_index('ix_RolePermissions_permission_id', table_name='RolePermissions', schema='dbo')
    op.drop_table('RolePermissions', schema='dbo')

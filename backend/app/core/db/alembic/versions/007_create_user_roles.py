"""Create user_roles table

Revision ID: 007_create_user_roles
Revises: 006_create_role_permissions
Create Date: 2025-02-12 11:06:20.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '007_create_user_roles'
down_revision = '006_create_role_permissions'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('UserRoles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['dbo.Roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['dbo.Users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
        schema='dbo'
    )
    op.create_index('ix_UserRoles_role_id', 'UserRoles', ['role_id'], schema='dbo')
    op.create_index('ix_UserRoles_user_id', 'UserRoles', ['user_id'], schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_UserRoles_user_id', table_name='UserRoles', schema='dbo')
    op.drop_index('ix_UserRoles_role_id', table_name='UserRoles', schema='dbo')
    op.drop_table('UserRoles', schema='dbo')

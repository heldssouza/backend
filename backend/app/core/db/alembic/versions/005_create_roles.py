"""Create roles table

Revision ID: 005_create_roles
Revises: 004_create_permissions
Create Date: 2025-02-12 11:06:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005_create_roles'
down_revision = '004_create_permissions'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('Roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['dbo.Tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='dbo'
    )
    op.create_index('ix_Roles_tenant_id', 'Roles', ['tenant_id'], schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_Roles_tenant_id', table_name='Roles', schema='dbo')
    op.drop_table('Roles', schema='dbo')

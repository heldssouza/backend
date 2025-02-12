"""Create users table

Revision ID: 003_create_users
Revises: 002_create_tenants
Create Date: 2025-02-12 11:04:20.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003_create_users'
down_revision = '002_create_tenants'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('Users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('1'), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['dbo.Tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
        schema='dbo'
    )
    op.create_index('ix_Users_email', 'Users', ['email'], unique=True, schema='dbo')
    op.create_index('ix_Users_username', 'Users', ['username'], unique=True, schema='dbo')
    op.create_index('ix_Users_tenant_id', 'Users', ['tenant_id'], schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_Users_tenant_id', table_name='Users', schema='dbo')
    op.drop_index('ix_Users_username', table_name='Users', schema='dbo')
    op.drop_index('ix_Users_email', table_name='Users', schema='dbo')
    op.drop_table('Users', schema='dbo')

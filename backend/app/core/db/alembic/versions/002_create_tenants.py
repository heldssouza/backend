"""Create tenants table

Revision ID: 002_create_tenants
Revises: 001_create_schema
Create Date: 2025-02-12 11:04:10.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_create_tenants'
down_revision = '001_create_schema'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('Tenants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('subdomain', sa.String(length=100), nullable=False),
        sa.Column('database_name', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('subdomain'),
        sa.UniqueConstraint('database_name'),
        schema='dbo'
    )
    op.create_index('ix_Tenants_subdomain', 'Tenants', ['subdomain'], unique=True, schema='dbo')
    op.create_index('ix_Tenants_database_name', 'Tenants', ['database_name'], unique=True, schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_Tenants_database_name', table_name='Tenants', schema='dbo')
    op.drop_index('ix_Tenants_subdomain', table_name='Tenants', schema='dbo')
    op.drop_table('Tenants', schema='dbo')

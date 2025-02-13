"""Create tenants table

Revision ID: 002_create_tenants
Revises: 001_initial
Create Date: 2025-02-12 11:04:20.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

# revision identifiers, used by Alembic.
revision = '002_create_tenants'
down_revision = '001_initial'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Primeiro criamos a tabela sem as foreign keys
    op.create_table('Tenants',
        sa.Column('TenantID', UNIQUEIDENTIFIER(), nullable=False),
        sa.Column('Name', sa.String(length=100), nullable=False),
        sa.Column('Subdomain', sa.String(length=100), nullable=False),
        sa.Column('IsActive', sa.Boolean(), server_default=sa.text('1'), nullable=False),
        sa.Column('CreatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('CreatedBy', UNIQUEIDENTIFIER(), nullable=True),
        sa.Column('UpdatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('UpdatedBy', UNIQUEIDENTIFIER(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.PrimaryKeyConstraint('TenantID'),
        sa.UniqueConstraint('Subdomain'),
        schema='dbo'
    )
    op.create_index('ix_Tenants_TenantID', 'Tenants', ['TenantID'], unique=False, schema='dbo')
    op.create_index('ix_Tenants_IsDeleted', 'Tenants', ['IsDeleted'], unique=False, schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_Tenants_IsDeleted', table_name='Tenants', schema='dbo')
    op.drop_index('ix_Tenants_TenantID', table_name='Tenants', schema='dbo')
    op.drop_table('Tenants', schema='dbo')

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
        sa.Column('TenantID', sa.Integer(), nullable=False),
        sa.Column('Name', sa.String(length=100), nullable=False),
        sa.Column('Subdomain', sa.String(length=100), nullable=False),
        sa.Column('DatabaseName', sa.String(length=50), nullable=False),
        sa.Column('IsActive', sa.Boolean(), server_default=sa.text('1'), nullable=False),
        sa.Column('CreatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('CreatedBy', sa.Integer(), nullable=True),
        sa.Column('UpdatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('UpdatedBy', sa.Integer(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.PrimaryKeyConstraint('TenantID'),
        sa.UniqueConstraint('Subdomain'),
        sa.UniqueConstraint('DatabaseName'),
        schema='dbo'
    )
    op.create_index('ix_Tenants_Subdomain', 'Tenants', ['Subdomain'], unique=True, schema='dbo')
    op.create_index('ix_Tenants_DatabaseName', 'Tenants', ['DatabaseName'], unique=True, schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_Tenants_DatabaseName', table_name='Tenants', schema='dbo')
    op.drop_index('ix_Tenants_Subdomain', table_name='Tenants', schema='dbo')
    op.drop_table('Tenants', schema='dbo')

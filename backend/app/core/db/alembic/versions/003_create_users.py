"""Create users table

Revision ID: 003_create_users
Revises: 002_create_tenants
Create Date: 2025-02-12 11:04:20.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

# revision identifiers, used by Alembic.
revision = '003_create_users'
down_revision = '002_create_tenants'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('Users',
        sa.Column('UserID', UNIQUEIDENTIFIER(), nullable=False),
        sa.Column('TenantID', UNIQUEIDENTIFIER(), nullable=False),
        sa.Column('Username', sa.String(length=100), nullable=False),
        sa.Column('Email', sa.String(length=255), nullable=False),
        sa.Column('HashedPassword', sa.String(length=255), nullable=False),
        sa.Column('FirstName', sa.String(length=100), nullable=True),
        sa.Column('LastName', sa.String(length=100), nullable=True),
        sa.Column('IsActive', sa.Boolean(), server_default=sa.text('1'), nullable=False),
        sa.Column('IsSuperuser', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.Column('CreatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('CreatedBy', UNIQUEIDENTIFIER(), nullable=True),
        sa.Column('UpdatedAt', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('UpdatedBy', UNIQUEIDENTIFIER(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.ForeignKeyConstraint(['TenantID'], ['dbo.Tenants.TenantID'], ),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.Users.UserID'], ),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.Users.UserID'], ),
        sa.PrimaryKeyConstraint('UserID'),
        sa.UniqueConstraint('Email'),
        sa.UniqueConstraint('Username'),
        schema='dbo'
    )
    op.create_index('ix_Users_Email', 'Users', ['Email'], unique=True, schema='dbo')
    op.create_index('ix_Users_Username', 'Users', ['Username'], unique=True, schema='dbo')
    op.create_index('ix_Users_TenantID', 'Users', ['TenantID'], schema='dbo')
    op.create_index('ix_Users_UserID', 'Users', ['UserID'], unique=False, schema='dbo')
    op.create_index('ix_Users_IsDeleted', 'Users', ['IsDeleted'], unique=False, schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_Users_IsDeleted', table_name='Users', schema='dbo')
    op.drop_index('ix_Users_UserID', table_name='Users', schema='dbo')
    op.drop_index('ix_Users_TenantID', table_name='Users', schema='dbo')
    op.drop_index('ix_Users_Username', table_name='Users', schema='dbo')
    op.drop_index('ix_Users_Email', table_name='Users', schema='dbo')
    op.drop_table('Users', schema='dbo')

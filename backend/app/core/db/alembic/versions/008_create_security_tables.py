"""Create security tables

Revision ID: 008_create_security_tables
Revises: 007_create_user_roles
Create Date: 2025-02-12 11:06:30.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '008_create_security_tables'
down_revision = '007_create_user_roles'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # TwoFactorAuth table
    op.create_table('TwoFactorAuth',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('secret_key', sa.String(length=32), nullable=False),
        sa.Column('is_enabled', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.Column('backup_codes', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['dbo.Users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='dbo'
    )
    op.create_index('ix_TwoFactorAuth_user_id', 'TwoFactorAuth', ['user_id'], unique=True, schema='dbo')

    # RefreshTokens table
    op.create_table('RefreshTokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['dbo.Users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='dbo'
    )
    op.create_index('ix_RefreshTokens_token', 'RefreshTokens', ['token'], unique=True, schema='dbo')
    op.create_index('ix_RefreshTokens_user_id', 'RefreshTokens', ['user_id'], schema='dbo')

    # SecurityLogs table
    op.create_table('SecurityLogs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('event_data', sa.String(length=1000), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['dbo.Tenants.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['dbo.Users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='dbo'
    )
    op.create_index('ix_SecurityLogs_tenant_id', 'SecurityLogs', ['tenant_id'], schema='dbo')
    op.create_index('ix_SecurityLogs_user_id', 'SecurityLogs', ['user_id'], schema='dbo')
    op.create_index('ix_SecurityLogs_event_type', 'SecurityLogs', ['event_type'], schema='dbo')
    op.create_index('ix_SecurityLogs_created_at', 'SecurityLogs', ['created_at'], schema='dbo')

def downgrade() -> None:
    op.drop_table('SecurityLogs', schema='dbo')
    op.drop_table('RefreshTokens', schema='dbo')
    op.drop_table('TwoFactorAuth', schema='dbo')

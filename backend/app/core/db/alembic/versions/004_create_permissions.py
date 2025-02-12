"""Create permissions table

Revision ID: 004_create_permissions
Revises: 003_create_users
Create Date: 2025-02-12 11:04:30.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004_create_permissions'
down_revision = '003_create_users'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('Permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('GETDATE()'), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        schema='dbo'
    )
    op.create_index('ix_Permissions_code', 'Permissions', ['code'], unique=True, schema='dbo')

def downgrade() -> None:
    op.drop_index('ix_Permissions_code', table_name='Permissions', schema='dbo')
    op.drop_table('Permissions', schema='dbo')

"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2025-02-13 01:48:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dbo')
    BEGIN
        EXEC('CREATE SCHEMA dbo')
    END
    """)

def downgrade() -> None:
    op.execute("""
    IF EXISTS (SELECT * FROM sys.schemas WHERE name = 'dbo')
    BEGIN
        EXEC('DROP SCHEMA dbo')
    END
    """)

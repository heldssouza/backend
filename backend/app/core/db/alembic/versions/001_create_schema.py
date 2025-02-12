"""Create schema

Revision ID: 001_create_schema
Create Date: 2025-02-12 11:04:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_create_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create schema if it doesn't exist
    op.execute('IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N\'dbo\') EXEC(\'CREATE SCHEMA [dbo]\')')

def downgrade() -> None:
    # We don't want to drop the schema on downgrade
    pass

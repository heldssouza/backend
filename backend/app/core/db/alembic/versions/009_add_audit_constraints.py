"""Add audit constraints

Revision ID: 009_add_audit_constraints
Revises: 008_create_security_tables
Create Date: 2025-02-12 11:06:40.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '009_add_audit_constraints'
down_revision = '008_create_security_tables'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add FK constraints for created_by and updated_by
    tables = ['Tenants', 'Users', 'Permissions', 'Roles']
    
    for table in tables:
        op.create_foreign_key(
            f'fk_{table}_created_by_Users',
            table,
            'Users',
            ['created_by'],
            ['id'],
            source_schema='dbo',
            referent_schema='dbo'
        )
        op.create_foreign_key(
            f'fk_{table}_updated_by_Users',
            table,
            'Users',
            ['updated_by'],
            ['id'],
            source_schema='dbo',
            referent_schema='dbo'
        )

def downgrade() -> None:
    tables = ['Tenants', 'Users', 'Permissions', 'Roles']
    
    for table in tables:
        op.drop_constraint(
            f'fk_{table}_updated_by_Users',
            table,
            type_='foreignkey',
            schema='dbo'
        )
        op.drop_constraint(
            f'fk_{table}_created_by_Users',
            table,
            type_='foreignkey',
            schema='dbo'
        )

"""Add tenant audit constraints

Revision ID: 004_add_tenant_audit_constraints
Revises: 003_create_users
Create Date: 2025-02-13 01:53:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004_add_tenant_audit_constraints'
down_revision = '003_create_users'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Agora que a tabela Users existe, podemos adicionar as foreign keys na tabela Tenants
    op.create_foreign_key(
        'fk_tenants_created_by_users',
        'Tenants',
        'Users',
        ['CreatedBy'],
        ['UserID'],
        source_schema='dbo',
        referent_schema='dbo'
    )
    op.create_foreign_key(
        'fk_tenants_updated_by_users',
        'Tenants',
        'Users',
        ['UpdatedBy'],
        ['UserID'],
        source_schema='dbo',
        referent_schema='dbo'
    )

def downgrade() -> None:
    op.drop_constraint('fk_tenants_updated_by_users', 'Tenants', schema='dbo', type_='foreignkey')
    op.drop_constraint('fk_tenants_created_by_users', 'Tenants', schema='dbo', type_='foreignkey')

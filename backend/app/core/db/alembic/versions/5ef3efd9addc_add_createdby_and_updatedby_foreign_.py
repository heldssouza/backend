"""Add CreatedBy and UpdatedBy foreign keys to Tenants

Revision ID: 5ef3efd9addc
Revises: 34ea4075d3d0
Create Date: 2025-02-11 20:25:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ef3efd9addc'
down_revision: Union[str, None] = '34ea4075d3d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add foreign key constraints
    op.create_foreign_key(
        'fk_Tenants_CreatedBy_Users',
        'Tenants',
        'Users',
        ['CreatedBy'],
        ['UserID'],
        source_schema='dbo',
        referent_schema='dbo'
    )
    op.create_foreign_key(
        'fk_Tenants_UpdatedBy_Users',
        'Tenants',
        'Users',
        ['UpdatedBy'],
        ['UserID'],
        source_schema='dbo',
        referent_schema='dbo'
    )


def downgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint(
        'fk_Tenants_CreatedBy_Users',
        'Tenants',
        schema='dbo',
        type_='foreignkey'
    )
    op.drop_constraint(
        'fk_Tenants_UpdatedBy_Users',
        'Tenants',
        schema='dbo',
        type_='foreignkey'
    )

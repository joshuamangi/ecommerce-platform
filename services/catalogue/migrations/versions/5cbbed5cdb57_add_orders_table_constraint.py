"""add orders table constraint

Revision ID: 5cbbed5cdb57
Revises: 0ccd343f731e
Create Date: 2026-05-21 19:39:00.708116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cbbed5cdb57'
down_revision: Union[str, Sequence[str], None] = '0ccd343f731e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_check_constraint(
        'check_quantity_positive',
        'orders',
        'quantity > 0'
    )


def downgrade():
    op.drop_constraint(
        'check_quantity_positive',
        'orders',
        type='check'
    )

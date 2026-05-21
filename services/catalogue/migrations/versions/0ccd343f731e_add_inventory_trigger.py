"""add_inventory_trigger

Revision ID: 0ccd343f731e
Revises: 0409e3099714
Create Date: 2026-05-21 18:33:51.408101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ccd343f731e'
down_revision: Union[str, Sequence[str], None] = '0409e3099714'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Execute the trigger function and trigger definition
    op.execute("""
        CREATE OR REPLACE FUNCTION decrement_inventory()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE catalogue
            SET stock_quantity = stock_quantity - NEW.quantity
            WHERE id = NEW.catalogue_id AND stock_quantity >= NEW.quantity;
        
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Insufficient stock for product ID %', NEW.catalogue_id;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER trg_decrement_inventory
        AFTER INSERT ON orders
        FOR EACH ROW
        EXECUTE FUNCTION decrement_inventory();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_decrement_inventory ON orders;")
    op.execute("DROP FUNCTION IF EXISTS decrement_inventory();")

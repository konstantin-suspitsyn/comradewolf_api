"""create olap_connection olap_foreign_key

Revision ID: 8beb3128244b
Revises: 232aee365e6b
Create Date: 2024-04-30 10:06:05.836390

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '8beb3128244b'
down_revision: Union[str, None] = '232aee365e6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

        ALTER TABLE cwb.log DROP CONSTRAINT IF EXISTS olap_connection_olap_table_fk;
        
        ALTER TABLE cwb.olap_connection ADD CONSTRAINT olap_connection_olap_table_fk FOREIGN KEY (olap_id) REFERENCES 
        cwb.olap_table(id) ON DELETE CASCADE ON UPDATE CASCADE;

    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
        ALTER TABLE cwb.log DROP CONSTRAINT IF EXISTS olap_connection_olap_table_fk;
    """))

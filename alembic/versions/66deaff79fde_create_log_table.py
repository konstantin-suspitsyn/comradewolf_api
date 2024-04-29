"""create log table

Revision ID: 66deaff79fde
Revises: 31824ca9c3fc
Create Date: 2024-04-29 15:52:10.856779

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '66deaff79fde'
down_revision: Union[str, None] = '31824ca9c3fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cwb.log (
            id bigserial NOT NULL,
            olap_table_id int8 NOT NULL,
            user_id int8 NOT NULL,
            query text NULL,
            message text NULL,
            created_at timestamp NOT NULL,
            updated_at timestamp NULL,
            CONSTRAINT log_pk PRIMARY KEY (id)
        );

    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("DROP TABLE cwb.log;"))

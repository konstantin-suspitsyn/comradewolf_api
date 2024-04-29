"""create olap_table table

Revision ID: 31824ca9c3fc
Revises: c02bd0e79bc2
Create Date: 2024-04-29 15:50:54.490892

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '31824ca9c3fc'
down_revision: Union[str, None] = 'c02bd0e79bc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cwb.olap_table (
            id bigserial NOT NULL,
            "name" varchar(255) NOT NULL,
            link_toml varchar(1000) NOT NULL,
            created_at timestamp NOT NULL,
            updated_at timestamp NULL,
            database_type_id int8 NULL,
            CONSTRAINT olap_list_link_toml_unique UNIQUE (link_toml),
            CONSTRAINT tables_list_pk PRIMARY KEY (id)
        );

    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("DROP TABLE cwb.olap_table;"))

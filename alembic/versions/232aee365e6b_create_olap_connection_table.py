"""create olap_connection table

Revision ID: 232aee365e6b
Revises: 9cd8a386bd34
Create Date: 2024-04-30 10:05:44.392990

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '232aee365e6b'
down_revision: Union[str, None] = '9cd8a386bd34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cwb.olap_connection (
            id bigserial NOT NULL,
            host varchar(255) NOT NULL,
            host_type int2 NOT NULL,
            port varchar(50) NOT NULL,
            port_type int2 NOT NULL,
            username varchar(255) NOT NULL,
            username_type int2 NOT NULL,
            "password" varchar(1000) NOT NULL,
            password_type int2 NOT NULL,
            "database" varchar(50) NOT NULL,
            database_type int2 NOT NULL,
            olap_id int8 NOT NULL,
            additional text NULL,
            "comment" text NULL,
            created_at timestamp NOT NULL,
            updated_at timestamp NULL,
            CONSTRAINT olap_connection_pk PRIMARY KEY (id)
        );

    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("DROP TABLE cwb.olap_connection;"))

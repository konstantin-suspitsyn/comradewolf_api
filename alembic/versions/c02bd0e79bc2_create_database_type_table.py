"""create database_type table

Revision ID: c02bd0e79bc2
Revises: 557609e3ad84
Create Date: 2024-04-29 15:49:22.718524

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'c02bd0e79bc2'
down_revision: Union[str, None] = '557609e3ad84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cwb.database_type (
            id int8 NOT NULL,
            "name" varchar(50) NOT NULL,
            CONSTRAINT database_type_pk PRIMARY KEY (id),
            CONSTRAINT database_type_unique UNIQUE (name)
        );
    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("DROP TABLE cwb.database_type;"))

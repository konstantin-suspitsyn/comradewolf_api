"""create user table

Revision ID: 557609e3ad84
Revises: 
Create Date: 2024-04-29 15:39:23.284087

"""
from typing import Sequence, Union
from sqlalchemy.sql import text
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '557609e3ad84'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cwb."user" (
        id bigserial NOT NULL,
        username varchar(100) NOT NULL,
        "password" varchar(255) NOT NULL,
        created_at timestamp NOT NULL,
        updated_at timestamp NULL,
        email varchar(255) NOT NULL,
        CONSTRAINT user_pk PRIMARY KEY (id),
        CONSTRAINT user_unique UNIQUE (username)
        );
    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("DROP TABLE cwb.\"user\";"))

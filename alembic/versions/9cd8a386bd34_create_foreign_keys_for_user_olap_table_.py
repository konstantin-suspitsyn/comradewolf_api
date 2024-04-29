"""create foreign keys for user olap_table database_type

Revision ID: 9cd8a386bd34
Revises: 66deaff79fde
Create Date: 2024-04-29 15:54:51.406775

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '9cd8a386bd34'
down_revision: Union[str, None] = '66deaff79fde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
    
        ALTER TABLE cwb.log DROP CONSTRAINT IF EXISTS log_olap_table_fk;
        ALTER TABLE cwb.log DROP CONSTRAINT IF EXISTS log_user_fk;
        
        ALTER TABLE cwb.log ADD CONSTRAINT log_olap_table_fk FOREIGN KEY (olap_table_id) REFERENCES cwb.olap_table(id)
        ON DELETE CASCADE ON UPDATE CASCADE;
        ALTER TABLE cwb.log ADD CONSTRAINT log_user_fk FOREIGN KEY (user_id) REFERENCES cwb."user"(id) ON DELETE CASCADE
        ON UPDATE CASCADE;
        
        ALTER TABLE cwb.olap_table DROP CONSTRAINT IF EXISTS olap_table_database_type_fk;
                
        ALTER TABLE cwb.olap_table ADD CONSTRAINT olap_table_database_type_fk FOREIGN KEY (database_type_id) 
        REFERENCES cwb.database_type(id) ON DELETE CASCADE ON UPDATE CASCADE;
        
    """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("DROP TABLE cwb.log;"))

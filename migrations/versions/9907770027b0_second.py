"""second

Revision ID: 9907770027b0
Revises: 70b6f8aa94bb
Create Date: 2023-10-12 00:54:01.658892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9907770027b0'
down_revision: Union[str, None] = '70b6f8aa94bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('answer', sa.String(), nullable=True))
    op.drop_column('question', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('question', 'answer')
    # ### end Alembic commands ###
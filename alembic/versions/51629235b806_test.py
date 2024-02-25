"""test

Revision ID: 51629235b806
Revises: d7b5a8cf3cf2
Create Date: 2024-02-25 20:40:40.000122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51629235b806'
down_revision: Union[str, None] = 'd7b5a8cf3cf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profiles', 'custom_status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profiles', sa.Column('custom_status', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

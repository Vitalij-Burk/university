"""create table for users

Revision ID: da7f5a7d4b48
Revises: ad60ad51e9cd
Create Date: 2025-03-15 20:09:13.920918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da7f5a7d4b48'
down_revision: Union[str, None] = 'ad60ad51e9cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

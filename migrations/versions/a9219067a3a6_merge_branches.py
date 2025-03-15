"""merge branches

Revision ID: a9219067a3a6
Revises: 3153f9451de0, 8ba0a7ec5a6b
Create Date: 2025-03-13 18:32:34.498312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9219067a3a6'
down_revision: Union[str, None] = ('3153f9451de0', '8ba0a7ec5a6b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

"""merge branches

Revision ID: 3d7a30f42ee1
Revises: a76998afee0d
Create Date: 2025-03-16 12:34:56.053905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d7a30f42ee1'
down_revision: Union[str, None] = 'a76998afee0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

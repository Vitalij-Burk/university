"""merge branches

Revision ID: c63aad81b9ab
Revises: 3d7a30f42ee1
Create Date: 2025-03-16 12:36:37.460103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c63aad81b9ab'
down_revision: Union[str, None] = '3d7a30f42ee1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

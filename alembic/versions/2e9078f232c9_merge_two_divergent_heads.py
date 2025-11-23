"""Merge two divergent heads

Revision ID: 2e9078f232c9
Revises: 031f6c3e2109, 4e4fc6cd2af4
Create Date: 2025-11-23 22:18:51.506325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e9078f232c9'
down_revision: Union[str, Sequence[str], None] = ('031f6c3e2109', '4e4fc6cd2af4')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

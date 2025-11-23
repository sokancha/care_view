"""Merge conflicting development branches

Revision ID: 8c5cfa3ffd82
Revises: 4c1b9e0f2d3a, 59d155d2259d
Create Date: 2025-11-19 19:53:46.684494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c5cfa3ffd82'
down_revision: Union[str, Sequence[str], None] = ('4c1b9e0f2d3a', '59d155d2259d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

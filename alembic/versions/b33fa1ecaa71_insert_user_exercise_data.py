"""insert_user_exercise_data

Revision ID: b33fa1ecaa71
Revises: a5db8c87d228
Create Date: 2025-12-08 01:46:42.491506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b33fa1ecaa71'
down_revision: Union[str, Sequence[str], None] = '06a02da413b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

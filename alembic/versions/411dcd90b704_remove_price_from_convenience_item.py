"""remove_price_from_convenience_item

Revision ID: 411dcd90b704
Revises: 6c2d92271340
Create Date: 2025-12-07 18:07:54.646529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '411dcd90b704'
down_revision: Union[str, Sequence[str], None] = '6c2d92271340'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: ConvenienceItem 테이블에서 image_url과 price 컬럼을 삭제합니다."""
    
    # 1. price 컬럼 삭제
    op.drop_column('convenience_items', 'price')
    
    # 2. image_url 컬럼 삭제
    op.drop_column('convenience_items', 'image_url')


def downgrade() -> None:
    """Downgrade schema: 삭제했던 price와 image_url 컬럼을 다시 추가합니다."""
    
    # 1. image_url 컬럼 복구 (원래 String(500), nullable=True)
    op.add_column('convenience_items', sa.Column('image_url', sa.String(length=500), nullable=True))
    
    # 2. price 컬럼 복구 (원래 Integer, nullable=True)
    op.add_column('convenience_items', sa.Column('price', sa.Integer(), nullable=True))

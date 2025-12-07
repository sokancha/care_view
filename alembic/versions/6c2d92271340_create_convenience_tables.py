"""create_convenience_tables

Revision ID: 6c2d92271340
Revises: 6dcd053eb76a
Create Date: 2025-12-07 18:02:05.163318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c2d92271340'
down_revision: Union[str, Sequence[str], None] = '6dcd053eb76a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Creates recipe_sets, convenience_items, and set_composition tables."""
    # 1. RecipeSet 테이블 생성
    op.create_table(
        'recipe_sets',
        sa.Column('set_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('set_type', sa.String(length=50), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('total_calorie', sa.Float(), nullable=False),
        sa.Column('total_carbs', sa.Float(), nullable=False),
        sa.Column('total_protein', sa.Float(), nullable=False),
        sa.Column('total_fat', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('set_id')
    )
    op.create_index(op.f('ix_recipe_sets_set_id'), 'recipe_sets', ['set_id'], unique=False)
    
    # 2. ConvenienceItem 테이블 생성
    op.create_table(
        'convenience_items',
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('calorie', sa.Float(), nullable=False),
        sa.Column('carbs', sa.Float(), nullable=False),
        sa.Column('protein', sa.Float(), nullable=False),
        sa.Column('fat', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('item_id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_convenience_items_item_id'), 'convenience_items', ['item_id'], unique=False)

    # 3. SetComposition 테이블 생성 (중간 연결 테이블)
    op.create_table(
        'set_composition',
        sa.Column('set_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=50), nullable=False),
        # 외래 키(FK) 설정
        sa.ForeignKeyConstraint(['set_id'], ['recipe_sets.set_id'], ),
        sa.ForeignKeyConstraint(['item_id'], ['convenience_items.item_id'], ),
        sa.PrimaryKeyConstraint('set_id', 'item_id') # 복합 기본 키
    )


def downgrade() -> None:
    """Downgrade schema: Drops the three convenience tables."""
    # 3. SetComposition 테이블 삭제 (FK 때문에 가장 먼저 삭제)
    op.drop_table('set_composition')
    
    # 2. ConvenienceItem 테이블 삭제
    op.drop_index(op.f('ix_convenience_items_item_id'), table_name='convenience_items')
    op.drop_table('convenience_items')
    
    # 1. RecipeSet 테이블 삭제
    op.drop_index(op.f('ix_recipe_sets_set_id'), table_name='recipe_sets')
    op.drop_table('recipe_sets')

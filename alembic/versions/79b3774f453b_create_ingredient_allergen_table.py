"""create ingredient allergen table

Revision ID: 79b3774f453b
Revises: e2d6f2d01539
Create Date: 2025-12-03 23:20:57.245903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79b3774f453b'
down_revision: Union[str, Sequence[str], None] = 'e2d6f2d01539'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""create ingredient allergen table

Revision ID: 79b3774f453b
Revises: e2d6f2d01539
Create Date: 2025-12-03 23:20:57.245903

"""
# ... (생략)

def upgrade() -> None:
    """Upgrade schema: Create ingredient_allergen (M:N) table."""
    op.create_table(
        'ingredient_allergen',
        # ingredient_id (복합 PK, FK)
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        # allergy_id (복합 PK, FK)
        sa.Column('allergy_id', sa.Integer(), nullable=False),
        
        # 1. 외래 키 정의: ingredient_id -> ingredients
        sa.ForeignKeyConstraint(
            ['ingredient_id'], 
            ['ingredients.ingredient_id'], 
            name='fk_ingredient_allergen_ingredient_id'
        ),
        # 2. 외래 키 정의: allergy_id -> allergies (PK가 'id'임을 반영하여 수정)
        sa.ForeignKeyConstraint(
            ['allergy_id'], 
            ['allergies.id'], # <--- **이 부분을 'allergies.id'로 수정했습니다!**
            name='fk_ingredient_allergen_allergy_id'
        ),
        # 3. 복합 기본 키 설정
        sa.PrimaryKeyConstraint('ingredient_id', 'allergy_id')
    )


def downgrade() -> None:
    """Downgrade schema: Drop ingredient_allergen table."""
    op.drop_table('ingredient_allergen')

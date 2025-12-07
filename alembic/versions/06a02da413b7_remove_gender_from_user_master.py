"""remove_gender_from_user_master

Revision ID: 06a02da413b7
Revises: a5db8c87d228  # 👈 여기를 'a5db8c87d228'로 변경
Create Date: 2025-12-08 01:50:57.567560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06a02da413b7'
down_revision: Union[str, Sequence[str], None] = 'a5db8c87d228' # ⚠️ 'a5db8c87d228'로 수정됨
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    user_master 테이블에서 gender 컬럼을 삭제하고,
    고유 제약 조건(UniqueConstraint)에서 gender를 제거합니다.
    """
    op.drop_constraint('uq_user_group', 'user_master', type_='unique')
    op.drop_column('user_master', 'gender')
    
    # 새로운 고유 제약 조건 추가 (gender 제외)
    op.create_unique_constraint(
        'uq_user_group', 
        'user_master', 
        ['age_group', 'bmi_grade']
    )


def downgrade() -> None:
    """
    gender 컬럼을 복구하고, 기존의 고유 제약 조건을 되돌립니다.
    """
    op.drop_constraint('uq_user_group', 'user_master', type_='unique')
    op.add_column('user_master', sa.Column('gender', sa.String(length=1), nullable=False))
    
    # 기존의 고유 제약 조건 복구
    op.create_unique_constraint(
        'uq_user_group', 
        'user_master', 
        ['age_group', 'bmi_grade', 'gender']
    )

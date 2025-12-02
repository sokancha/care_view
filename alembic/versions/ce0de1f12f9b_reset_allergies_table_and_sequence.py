"""reset_allergies_table_and_sequence

Revision ID: ce0de1f12f9b
Revises: 6c3a1b2e4d0f
Create Date: 2025-12-02 23:35:38.701529

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce0de1f12f9b'
down_revision: Union[str, Sequence[str], None] = '6c3a1b2e4d0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """
    allergies 테이블의 ID를 생성하는 시퀀스(Sequence)의 값을 1로 재설정합니다.
    (PostgreSQL의 기본 시퀀스 이름은 '테이블명_컬럼명_seq' 형식입니다.)
    """
    print("-> allergies_id_seq 시퀀스 카운터 1로 재설정 시작...")
    
    # 🚨 setval(시퀀스명, 다음 값, is_called)
    # 'false'는 다음 INSERT 시 ID가 1이 됨을 의미합니다.
    op.execute(
        sa.text("SELECT setval('allergies_id_seq', 1, false);")
    )
    
    print("-> 시퀀스 재설정 완료. 다음 INSERT는 ID 1부터 시작합니다.")


def downgrade() -> None:
    """시퀀스 재설정은 되돌리기가 복잡하므로 비워둡니다."""
    pass

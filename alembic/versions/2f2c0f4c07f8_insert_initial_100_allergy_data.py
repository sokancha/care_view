"""Insert initial 100 allergy data

Revision ID: 2f2c0f4c07f8
Revises: e3d3c500cacc
Create Date: 2025-11-12 16:08:48.337023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column 


# revision identifiers, used by Alembic.
# 이 부분이 Alembic이 리비전 ID를 인식하는 데 필수적인 부분입니다.
revision: str = '2f2c0f4c07f8'
down_revision: Union[str, Sequence[str], None] = 'bd14f3b715e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 100가지 알레르기 항목 목록 (식품/첨가물 중심으로 재구성)
INITIAL_ALLERGIES = [
    # [주요 식품 알레르기 및 기본] (1-20)
    '우유', '대두', '메밀', '땅콩', '밀', '생선', '게', '새우', '돼지고기', '복숭아', 
    '토마토', '아황산염', '호두', '닭고기', '쇠고기', '오징어', '조개류', '잣', '키위',
    '달걀',

    # [견과류 및 씨앗류] (21-30)
    '아몬드', '캐슈넛', '피스타치오', '마카다미아', '헤이즐넛', '브라질너트', '해바라기씨',
    '참깨', '양귀비씨', '호박씨', 

    # [곡물 및 콩류] (31-40)
    '옥수수', '쌀', '귀리', '보리', '호밀', '콩(강낭콩)', '렌틸콩', '병아리콩', '녹두',
    '밀가루',

    # [과일] (41-55)
    '사과', '바나나', '포도', '오렌지', '레몬', '딸기', '파인애플', '아보카도', '망고', 
    '멜론', '배', '자두', '체리', '블루베리', '라즈베리',

    # [채소] (56-70)
    '감자', '당근', '샐러리', '양파', '마늘', '생강', '아스파라거스', '버섯', '파',
    '시금치', '양배추', '브로콜리', '파프리카', '고추', '가지',

    # [첨가물 및 기타 가공 성분] (71-85)
    '효모', '식용 색소(타르트라진)', 'MSG (L-글루탐산나트륨)', '아질산염', '젤라틴', 
    '코코아', '바닐라', '커피', '차(카페인)', 
    '술/주정', '카라멜 색소', '인공 감미료', '방부제', '유화제', '팜유', 

    # [향신료 및 기타 식품] (86-100)
    '후추', '계피', '올리브', '무', '배추', '호박', '허브(딜)', '허브(바질)', 
    '허브(오레가노)', '허브(파슬리)', '허브(로즈마리)', '오리알', '메추리알', 
    '염소고기', '오리고기', '메추리고기', '아티초크', '케이퍼', '피클', '밤'
]


def upgrade() -> None:
    """데이터 마이그레이션 실행: 100가지 식품 관련 알레르기 데이터를 'allergies' 테이블에 삽입합니다."""
    
    # 1. 대상 테이블 객체 정의
    allergy_table = table(
        'allergies', 
        column('name', sa.String(length=100)) 
    )
    
    # 2. 데이터 삽입 (bulk_insert 사용)
    op.bulk_insert(
        allergy_table,
        [{"name": name} for name in INITIAL_ALLERGIES]
    )


def downgrade() -> None:
    """데이터 마이그레이션 되돌리기: 삽입된 100개 알레르기 데이터를 삭제합니다."""
    
    # op.execute를 사용하여 SQL DELETE 쿼리를 직접 실행
    op.execute(
        sa.text("DELETE FROM allergies WHERE name IN :names").bindparams(names=tuple(INITIAL_ALLERGIES))
    )
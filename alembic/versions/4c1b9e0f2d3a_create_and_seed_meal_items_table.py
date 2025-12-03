from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Text


# revision identifiers, used by Alembic.
revision: str = '4c1b9e0f2d3a'
down_revision: Union[str, Sequence[str], None] = '31a7c8d9e0f1' # 이 마이그레이션은 레시피 데이터 삽입(31a7c8d9e0f1) 다음에 실행되어야 함
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 레시피에서 추출된 Meal Item 데이터 목록 (총 47개)
INITIAL_MEAL_ITEMS = [
    {"item_id": 1, "name": "통밀 팬케이크"},
    {"item_id": 2, "name": "베리 세트"},
    {"item_id": 3, "name": "계란 스크램블"},
    {"item_id": 4, "name": "아보카도 토스트"},
    {"item_id": 5, "name": "그릭 요거트"},
    {"item_id": 6, "name": "그래놀라"},
    {"item_id": 7, "name": "시금치 & 치즈 오믈렛"},
    {"item_id": 8, "name": "오버나이트 오트밀"},
    {"item_id": 9, "name": "바나나 스무디"},
    {"item_id": 10, "name": "아몬드"},
    {"item_id": 11, "name": "두부 샐러드"},
    {"item_id": 12, "name": "현미 주먹밥"},
    {"item_id": 13, "name": "닭가슴살 샌드위치"},
    {"item_id": 14, "name": "통밀빵"},
    {"item_id": 15, "name": "버섯 볶음밥"},
    {"item_id": 16, "name": "채소 볶음밥"},
    {"item_id": 17, "name": "훈제 연어"},
    {"item_id": 18, "name": "크림치즈 베이글"},
    {"item_id": 19, "name": "퀴노아 샐러드"},
    {"item_id": 20, "name": "포케 볼"},
    {"item_id": 21, "name": "비건 타코"},
    {"item_id": 22, "name": "멕시칸 렌틸콩"},
    {"item_id": 23, "name": "저염 소고기 찹스테이크"},
    {"item_id": 24, "name": "구운 채소"},
    {"item_id": 25, "name": "에그인헬 (샥슈카)"},
    {"item_id": 26, "name": "병아리콩 커리"},
    {"item_id": 27, "name": "통밀 난"},
    {"item_id": 28, "name": "렌틸콩 수프"},
    {"item_id": 29, "name": "호밀빵"},
    {"item_id": 30, "name": "돼지고기 앞다리살 간장 불고기"},
    {"item_id": 31, "name": "현미밥"},
    {"item_id": 32, "name": "버섯 된장찌개"},
    {"item_id": 33, "name": "참치마요 김밥"},
    {"item_id": 34, "name": "우동 (소량)"},
    {"item_id": 35, "name": "연어 스테이크"},
    {"item_id": 36, "name": "아스파라거스"},
    {"item_id": 37, "name": "양고기 숄더랙 구이"},
    {"item_id": 38, "name": "해산물 봉골레 파스타"},
    {"item_id": 39, "name": "두부 & 김치 볶음"},
    {"item_id": 40, "name": "토마토 & 모짜렐라 카프레제"},
    {"item_id": 41, "name": "매콤 닭봉 구이"},
    {"item_id": 42, "name": "콜리플라워 라이스"},
    {"item_id": 43, "name": "참치 스테이크"},
    {"item_id": 44, "name": "보리 리조또"},
    {"item_id": 45, "name": "해물 순두부찌개"},
    {"item_id": 46, "name": "채소 가득 월남쌈"},
    {"item_id": 47, "name": "땅콩 소스"}
]


def upgrade() -> None:
    """
    Meal_Item 테이블을 생성하고 초기 품목 데이터를 삽입합니다.
    """
    # 1. Meal_Item 테이블 생성 (주석 처리 - 테이블이 이미 존재하거나 이전 시도에서 생성됨)
    # op.create_table(
    #     'meal_items',
    #     sa.Column('item_id', sa.Integer, primary_key=True, index=True),
    #     sa.Column('name', sa.String(255), nullable=False, unique=True),
    #     # 데이터베이스 스키마와 일치시키기 위해 cooking_method 추가 (nullable=True)
    #     sa.Column('cooking_method', sa.Text, nullable=True), 
    # )
    
    # 2. bulk_insert를 위한 테이블 객체 정의
    meal_item_table = table(
        'meal_items', 
        column('item_id', Integer),
        column('name', String),
    )

    # 3. 초기 데이터 삽입
    # 참고: 테이블에 이미 동일한 item_id를 가진 데이터가 있다면, 이 단계에서 Duplicate Key 오류가 발생할 수 있습니다.
    op.bulk_insert(
        meal_item_table,
        INITIAL_MEAL_ITEMS
    )
    print(f"총 {len(INITIAL_MEAL_ITEMS)}개의 초기 Meal Item 데이터 삽입 완료.")


def downgrade() -> None:
    """
    마이그레이션을 되돌려 Meal_Item 테이블을 삭제합니다.
    CASCADE 옵션을 사용하여 meal_items에 종속된 모든 객체(다른 테이블의 외래 키 등)도 함께 삭제됩니다.
    """
    op.execute(sa.text("DROP TABLE meal_items CASCADE"))
    print("Meal_Item 테이블 및 종속 객체 삭제 완료 (롤백).")

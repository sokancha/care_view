"""add_ingredient

Revision ID: 6f4b37574943
Revises: ce0de1f12f9b
Create Date: 2025-12-02 23:49:13.271319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, text


# revision identifiers, used as Alembic.
revision: str = '6f4b37574943'
down_revision: Union[str, Sequence[str], None] = 'ce0de1f12f9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Meal_Item과 일반적인 요리에 사용되는 모든 핵심 및 부재료 데이터 목록 (총 79개)
INITIAL_INGREDIENTS = [
    {"ingredient_id": 1, "name": "통밀"},
    {"ingredient_id": 2, "name": "베리"},
    {"ingredient_id": 3, "name": "계란"},
    {"ingredient_id": 4, "name": "아보카도"},
    {"ingredient_id": 5, "name": "요거트"},
    {"ingredient_id": 6, "name": "그래놀라"},
    {"ingredient_id": 7, "name": "시금치"},
    {"ingredient_id": 8, "name": "치즈"}, 
    {"ingredient_id": 9, "name": "오트밀"},
    {"ingredient_id": 10, "name": "바나나"},
    {"ingredient_id": 11, "name": "아몬드"},
    {"ingredient_id": 12, "name": "두부"},
    {"ingredient_id": 13, "name": "양상추"},
    {"ingredient_id": 14, "name": "현미"},
    {"ingredient_id": 15, "name": "닭고기"},
    {"ingredient_id": 16, "name": "버섯"},
    {"ingredient_id": 17, "name": "쌀"},
    {"ingredient_id": 18, "name": "연어"},
    {"ingredient_id": 19, "name": "크림치즈"},
    {"ingredient_id": 20, "name": "베이글"},
    {"ingredient_id": 21, "name": "퀴노아"},
    {"ingredient_id": 22, "name": "참치"},
    {"ingredient_id": 23, "name": "렌틸콩"},
    {"ingredient_id": 24, "name": "병아리콩"},
    {"ingredient_id": 25, "name": "소고기"},
    {"ingredient_id": 26, "name": "토마토"},
    {"ingredient_id": 27, "name": "커리"}, 
    {"ingredient_id": 28, "name": "호밀"},
    {"ingredient_id": 29, "name": "돼지고기"},
    {"ingredient_id": 30, "name": "된장"},
    {"ingredient_id": 31, "name": "김"},
    {"ingredient_id": 32, "name": "우동면"},
    {"ingredient_id": 33, "name": "아스파라거스"},
    {"ingredient_id": 34, "name": "양고기"},
    {"ingredient_id": 35, "name": "조개"},
    {"ingredient_id": 36, "name": "새우"},
    {"ingredient_id": 37, "name": "파스타면"},
    {"ingredient_id": 38, "name": "김치"},
    {"ingredient_id": 39, "name": "콜리플라워"},
    {"ingredient_id": 40, "name": "보리"},
    {"ingredient_id": 41, "name": "라이스페이퍼"},
    {"ingredient_id": 42, "name": "땅콩"},
    {"ingredient_id": 43, "name": "밀가루"}, 
    {"ingredient_id": 44, "name": "설탕"}, 
    {"ingredient_id": 45, "name": "버터"},
    {"ingredient_id": 46, "name": "메이플 시럽"},
    {"ingredient_id": 47, "name": "꿀"},
    {"ingredient_id": 48, "name": "우유"}, 
    {"ingredient_id": 49, "name": "베이킹 파우더"},
    {"ingredient_id": 50, "name": "소금"},
    {"ingredient_id": 51, "name": "후추"},
    {"ingredient_id": 52, "name": "올리브 오일"},
    {"ingredient_id": 53, "name": "식용유"}, 
    {"ingredient_id": 54, "name": "간장"},
    {"ingredient_id": 55, "name": "고추장"},
    {"ingredient_id": 56, "name": "고춧가루"},
    {"ingredient_id": 57, "name": "깨"}, 
    {"ingredient_id": 58, "name": "참기름"},
    {"ingredient_id": 59, "name": "다진 마늘"},
    {"ingredient_id": 60, "name": "생강"},
    {"ingredient_id": 61, "name": "청주/맛술"},
    {"ingredient_id": 62, "name": "케첩"},
    {"ingredient_id": 63, "name": "마요네즈"},
    {"ingredient_id": 64, "name": "머스타드"},
    {"ingredient_id": 65, "name": "레몬"}, 
    {"ingredient_id": 66, "name": "식초"},
    {"ingredient_id": 67, "name": "피클"},
    {"ingredient_id": 68, "name": "양파"},
    {"ingredient_id": 69, "name": "당근"},
    {"ingredient_id": 70, "name": "감자"},
    {"ingredient_id": 71, "name": "대파"}, 
    {"ingredient_id": 72, "name": "청양고추"},
    {"ingredient_id": 73, "name": "밀 또띠아"},
    {"ingredient_id": 74, "name": "닭봉"},
    {"ingredient_id": 75, "name": "육수 재료"}, 
    {"ingredient_id": 76, "name": "전분/가루"}, 
    {"ingredient_id": 77, "name": "마늘"},
    {"ingredient_id": 78, "name": "모짜렐라 치즈"}, 
    {"ingredient_id": 79, "name": "바질"}, 
]


def upgrade() -> None:
    """Upgrade schema: ingredients 테이블을 생성하고 데이터를 삽입합니다."""
    """
    # 1. ingredients 테이블 생성 (테이블이 이미 존재하면 오류가 발생할 수 있습니다.)
    # 컬럼이 사라졌다면 테이블을 삭제하고 다시 생성하는 것이 가장 안전합니다.
    # 만약 테이블이 이미 존재한다면, 다음 단계에서 오류가 발생할 수 있습니다.
    try:
        op.create_table(
            'ingredients',
            sa.Column('ingredient_id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(255), nullable=False, unique=True),
        )
        print("ingredients 테이블을 새로 생성했습니다.")
    except Exception as e:
        # 테이블이 이미 존재할 경우 (컬럼만 사라진 경우) DDL 오류는 무시합니다.
        print(f"ingredients 테이블 생성 중 오류 발생 (이미 존재할 가능성): {e}")
    """

    # 2. bulk_insert를 위한 테이블 객체 정의
    ingredient_table = table(
        'ingredients',
        column('ingredient_id', Integer),
        column('name', String),
    )
    
    # 3. 초기 데이터 삽입
    op.execute(text("DELETE FROM ingredients"))
    
    # 시퀀스 재설정 (데이터를 다시 1부터 채우기 위함)
    op.execute(text("SELECT setval('ingredients_ingredient_id_seq', 1, false)"))
    
    op.bulk_insert(
        ingredient_table,
        INITIAL_INGREDIENTS
    )
    print(f"총 {len(INITIAL_INGREDIENTS)}개의 Ingredient 데이터 삽입 완료.")


def downgrade() -> None:
    """Downgrade schema: ingredients 테이블을 삭제합니다."""
    # 테이블 구조는 이 마이그레이션에서 생성했으므로, 테이블 자체를 삭제합니다.
    op.execute(text("DROP TABLE ingredients CASCADE"))
    print("ingredients 테이블 및 종속 객체 삭제 완료 (롤백).")

"""Insert initial data into RecipeComposition table.
(Total 54 entries covering all 30 recipes)

Revision ID: 5d0e2c3b8f7a
Revises: 4c1b9e0f2d3a
Create Date: 2025-11-20 19:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column 
from sqlalchemy import String, Integer, Float


# revision identifiers, used by Alembic.
revision: str = '5d0e2c3b8f7a'
down_revision: Union[str, Sequence[str], None] = '4c1b9e0f2d3a' # Meal_Item 데이터 삽입 다음 순서
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 30개 레시피의 구성을 정의하는 데이터 목록 (총 54개)
# Format: {"recipe_id": X, "item_id": Y, "amount": A, "unit": "U"}
INITIAL_RECIPE_COMPOSITIONS = [
    # ☀️ A. 아침 식단 (Breakfast, ID 1-10)
    # 1. 통밀 팬케이크 & 베리 세트 (ID: 1)
    {"recipe_id": 1, "item_id": 1, "amount": 3.0, "unit": "장"},     # 통밀 팬케이크 3장
    {"recipe_id": 1, "item_id": 2, "amount": 100.0, "unit": "g"},    # 베리 세트 100g

    # 2. 계란 스크램블 & 아보카도 토스트 (ID: 2)
    {"recipe_id": 2, "item_id": 3, "amount": 1.0, "unit": "볼"},     # 계란 스크램블 1볼 (계란 2개 분량)
    {"recipe_id": 2, "item_id": 4, "amount": 1.0, "unit": "개"},     # 아보카도 토스트 1개 (통밀빵 1조각 기준)

    # 3. 그릭 요거트 & 그래놀라 볼 (ID: 3)
    {"recipe_id": 3, "item_id": 5, "amount": 150.0, "unit": "g"},    # 그릭 요거트 150g
    {"recipe_id": 3, "item_id": 6, "amount": 40.0, "unit": "g"},     # 그래놀라 40g

    # 4. 시금치 & 치즈 오믈렛 (ID: 4)
    {"recipe_id": 4, "item_id": 7, "amount": 1.0, "unit": "개"},     # 시금치 & 치즈 오믈렛 1개

    # 5. 오버나이트 오트밀 (견과류) (ID: 5)
    {"recipe_id": 5, "item_id": 8, "amount": 1.0, "unit": "컵"},     # 오버나이트 오트밀 1컵
    {"recipe_id": 5, "item_id": 10, "amount": 15.0, "unit": "g"},    # 아몬드 15g

    # 6. 바나나 & 아몬드 스무디 (ID: 6)
    {"recipe_id": 6, "item_id": 9, "amount": 1.0, "unit": "잔"},     # 바나나 스무디 1잔
    {"recipe_id": 6, "item_id": 10, "amount": 10.0, "unit": "g"},    # 아몬드 10g (토핑용)

    # 7. 두부 샐러드 & 현미 주먹밥 (ID: 7)
    {"recipe_id": 7, "item_id": 11, "amount": 1.0, "unit": "접시"},   # 두부 샐러드 1접시
    {"recipe_id": 7, "item_id": 12, "amount": 2.0, "unit": "개"},     # 현미 주먹밥 2개

    # 8. 닭가슴살 샌드위치 (통밀빵) (ID: 8)
    {"recipe_id": 8, "item_id": 13, "amount": 1.0, "unit": "개"},     # 닭가슴살 샌드위치 1개
    {"recipe_id": 8, "item_id": 14, "amount": 2.0, "unit": "조각"},   # 통밀빵 2조각 (샌드위치 구성용)

    # 9. 버섯 & 채소 볶음밥 (소량) (ID: 9)
    {"recipe_id": 9, "item_id": 15, "amount": 150.0, "unit": "g"},    # 버섯 볶음밥 150g
    {"recipe_id": 9, "item_id": 16, "amount": 50.0, "unit": "g"},     # 채소 볶음밥 (곁들임용) 50g

    # 10. 훈제 연어 & 크림치즈 베이글 (ID: 10)
    {"recipe_id": 10, "item_id": 17, "amount": 80.0, "unit": "g"},    # 훈제 연어 80g
    {"recipe_id": 10, "item_id": 18, "amount": 1.0, "unit": "개"},    # 크림치즈 베이글 1개

    # 🥗 B. 점심 식단 (Lunch, ID 11-20)
    # 11. 닭가슴살 & 퀴노아 샐러드 (ID: 11)
    {"recipe_id": 11, "item_id": 13, "amount": 80.0, "unit": "g"},    # 닭가슴살 80g (샌드위치용 닭가슴살 아이템 재활용)
    {"recipe_id": 11, "item_id": 19, "amount": 150.0, "unit": "g"},   # 퀴노아 샐러드 150g

    # 12. 포케 볼 (연어/참치) (ID: 12)
    {"recipe_id": 12, "item_id": 20, "amount": 1.0, "unit": "그릇"},   # 포케 볼 1그릇
    {"recipe_id": 12, "item_id": 31, "amount": 150.0, "unit": "g"},   # 현미밥 150g (포케 볼 베이스)

    # 13. 멕시칸 비건 타코 세트 (ID: 13)
    {"recipe_id": 13, "item_id": 21, "amount": 2.0, "unit": "개"},     # 비건 타코 2개
    {"recipe_id": 13, "item_id": 22, "amount": 100.0, "unit": "g"},   # 멕시칸 렌틸콩 100g

    # 14. 저염 소고기 찹스테이크 & 구운 채소 (ID: 14)
    {"recipe_id": 14, "item_id": 23, "amount": 100.0, "unit": "g"},   # 저염 소고기 찹스테이크 100g
    {"recipe_id": 14, "item_id": 24, "amount": 150.0, "unit": "g"},   # 구운 채소 150g

    # 15. 에그인헬 (Shakshuka) (ID: 15)
    {"recipe_id": 15, "item_id": 25, "amount": 1.0, "unit": "그릇"},   # 에그인헬 1그릇
    {"recipe_id": 15, "item_id": 29, "amount": 2.0, "unit": "조각"},   # 호밀빵 2조각 (곁들임)

    # 16. 병아리콩 커리 & 난 (통밀) (ID: 16)
    {"recipe_id": 16, "item_id": 26, "amount": 250.0, "unit": "g"},   # 병아리콩 커리 250g
    {"recipe_id": 16, "item_id": 27, "amount": 1.0, "unit": "장"},     # 통밀 난 1장

    # 17. 렌틸콩 수프 & 호밀빵 (ID: 17)
    {"recipe_id": 17, "item_id": 28, "amount": 300.0, "unit": "ml"},  # 렌틸콩 수프 300ml
    {"recipe_id": 17, "item_id": 29, "amount": 2.0, "unit": "조각"},   # 호밀빵 2조각

    # 18. 돼지고기 앞다리살 간장 불고기 세트 (ID: 18)
    {"recipe_id": 18, "item_id": 30, "amount": 150.0, "unit": "g"},   # 돼지고기 앞다리살 간장 불고기 150g
    {"recipe_id": 18, "item_id": 31, "amount": 150.0, "unit": "g"},   # 현미밥 150g

    # 19. 현미밥 & 버섯 된장찌개 세트 (ID: 19)
    {"recipe_id": 19, "item_id": 31, "amount": 150.0, "unit": "g"},   # 현미밥 150g
    {"recipe_id": 19, "item_id": 32, "amount": 1.0, "unit": "뚝배기"}, # 버섯 된장찌개 1뚝배기

    # 20. 참치마요 김밥 (저염) & 우동(소량) (ID: 20)
    {"recipe_id": 20, "item_id": 33, "amount": 1.0, "unit": "줄"},     # 참치마요 김밥 1줄
    {"recipe_id": 20, "item_id": 34, "amount": 150.0, "unit": "ml"},  # 우동(소량) 150ml (국물)

    # 🌙 C. 저녁 식단 (Dinner, ID 21-30)
    # 21. 연어 스테이크 & 아스파라거스 (ID: 21)
    {"recipe_id": 21, "item_id": 35, "amount": 120.0, "unit": "g"},   # 연어 스테이크 120g
    {"recipe_id": 21, "item_id": 36, "amount": 6.0, "unit": "줄기"},   # 아스파라거스 6줄기

    # 22. 양고기 숄더랙 구이 & 샐러드 (ID: 22)
    {"recipe_id": 22, "item_id": 37, "amount": 180.0, "unit": "g"},   # 양고기 숄더랙 구이 180g
    {"recipe_id": 22, "item_id": 24, "amount": 100.0, "unit": "g"},   # 구운 채소 100g (곁들임)

    # 23. 해산물 봉골레 파스타 (통밀면) (ID: 23)
    {"recipe_id": 23, "item_id": 38, "amount": 1.0, "unit": "접시"},   # 해산물 봉골레 파스타 1접시

    # 24. 두부 & 김치 볶음 (저염) (ID: 24)
    {"recipe_id": 24, "item_id": 39, "amount": 150.0, "unit": "g"},   # 두부 & 김치 볶음 150g
    {"recipe_id": 24, "item_id": 31, "amount": 100.0, "unit": "g"},   # 현미밥 100g (곁들임)

    # 25. 토마토 & 모짜렐라 카프레제 세트 (ID: 25)
    {"recipe_id": 25, "item_id": 40, "amount": 1.0, "unit": "접시"},   # 토마토 & 모짜렐라 카프레제 1접시
    {"recipe_id": 25, "item_id": 29, "amount": 1.0, "unit": "조각"},   # 호밀빵 1조각 (곁들임)

    # 26. 매콤 닭봉 구이 & 콜리플라워 라이스 (ID: 26)
    {"recipe_id": 26, "item_id": 41, "amount": 5.0, "unit": "개"},     # 매콤 닭봉 구이 5개
    {"recipe_id": 26, "item_id": 42, "amount": 130.0, "unit": "g"},   # 콜리플라워 라이스 130g

    # 27. 참치 스테이크 & 구운 채소 (ID: 27)
    {"recipe_id": 27, "item_id": 43, "amount": 120.0, "unit": "g"},   # 참치 스테이크 120g
    {"recipe_id": 27, "item_id": 24, "amount": 150.0, "unit": "g"},   # 구운 채소 150g

    # 28. 버섯 리조또 (보리) (ID: 28)
    {"recipe_id": 28, "item_id": 44, "amount": 250.0, "unit": "g"},   # 보리 리조또 250g

    # 29. 해물 순두부찌개 (맑은 국물) (ID: 29)
    {"recipe_id": 29, "item_id": 45, "amount": 1.0, "unit": "뚝배기"}, # 해물 순두부찌개 1뚝배기
    {"recipe_id": 29, "item_id": 31, "amount": 150.0, "unit": "g"},   # 현미밥 150g

    # 30. 채소 가득 월남쌈 & 땅콩 소스 (ID: 30)
    {"recipe_id": 30, "item_id": 46, "amount": 4.0, "unit": "개"},     # 채소 가득 월남쌈 4개
    {"recipe_id": 30, "item_id": 47, "amount": 30.0, "unit": "g"},    # 땅콩 소스 30g
]


def upgrade() -> None:
    """
    RecipeComposition 테이블에 초기 구성 데이터를 삽입합니다. (총 54개)
    """
    # 1. recipe_composition 테이블 객체 정의
    recipe_composition_table = table(
        'recipe_composition', 
        column('recipe_id', Integer),
        column('item_id', Integer),
        column('amount', Float),
        column('unit', String),
    )

    # 2. 초기 데이터 삽입
    op.bulk_insert(
        recipe_composition_table,
        INITIAL_RECIPE_COMPOSITIONS
    )
    print(f"총 {len(INITIAL_RECIPE_COMPOSITIONS)}개의 초기 Recipe Composition 데이터 삽입 완료.")


def downgrade() -> None:
    """
    마이그레이션을 되돌려 삽입된 RecipeComposition 데이터를 삭제합니다.
    """
    # 삽입했던 레시피 ID 목록 추출
    recipe_ids_to_delete = tuple(
        set(r['recipe_id'] for r in INITIAL_RECIPE_COMPOSITIONS)
    )

    # recipe_id를 기준으로 해당 레코드들을 모두 삭제
    op.execute(
        sa.text("DELETE FROM recipe_composition WHERE recipe_id IN :ids").bindparams(ids=recipe_ids_to_delete)
    )
    print("Recipe Composition 데이터 삭제 완료 (롤백).")
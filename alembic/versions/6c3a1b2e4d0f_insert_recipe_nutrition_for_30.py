"""insert_recipe_nutrition_for_30

Revision ID: 6c3a1b2e4d0f
Revises: 31a7c8d9e0f1
Create Date: 2025-11-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, Float

# revision identifiers, used by Alembic.
revision: str = '6c3a1b2e4d0f'
down_revision: Union[str, Sequence[str], None] = '5d0e2c3b8f7a' # 레시피 30개 삽입 마이그레이션 다음 단계
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ----------------------------------------------------
# 30개 레시피에 대한 고정된 영양 데이터 정의
# 칼로리(kcal), 탄수화물(g), 단백질(g), 지방(g)
# ----------------------------------------------------
RECIPE_NUTRITION_DATA = [
    # ☀️ A. 아침 식단 (Breakfast, ID 1-10)
    {"recipe_id": 1, "calories": 450.0, "carbohydrates": 55.0, "protein": 12.0, "fat": 20.0}, # 통밀 팬케이크 & 베리 세트
    {"recipe_id": 2, "calories": 520.0, "carbohydrates": 40.0, "protein": 30.0, "fat": 28.0}, # 계란 스크램블 & 아보카도 토스트
    {"recipe_id": 3, "calories": 380.0, "carbohydrates": 45.0, "protein": 18.0, "fat": 14.0}, # 그릭 요거트 & 그래놀라 볼
    {"recipe_id": 4, "calories": 410.0, "carbohydrates": 15.0, "protein": 35.0, "fat": 22.0}, # 시금치 & 치즈 오믈렛
    {"recipe_id": 5, "calories": 320.0, "carbohydrates": 48.0, "protein": 10.0, "fat": 10.0}, # 오버나이트 오트밀 (견과류)
    {"recipe_id": 6, "calories": 280.0, "carbohydrates": 45.0, "protein": 8.0, "fat": 8.0},  # 바나나 & 아몬드 스무디
    {"recipe_id": 7, "calories": 490.0, "carbohydrates": 60.0, "protein": 25.0, "fat": 15.0}, # 두부 샐러드 & 현미 주먹밥
    {"recipe_id": 8, "calories": 550.0, "carbohydrates": 45.0, "protein": 40.0, "fat": 25.0}, # 닭가슴살 샌드위치 (통밀빵)
    {"recipe_id": 9, "calories": 390.0, "carbohydrates": 40.0, "protein": 15.0, "fat": 18.0}, # 버섯 & 채소 볶음밥 (소량)
    {"recipe_id": 10, "calories": 580.0, "carbohydrates": 50.0, "protein": 30.0, "fat": 28.0},# 훈제 연어 & 크림치즈 베이글
    
    # 🥗 B. 점심 식단 (Lunch, ID 11-20)
    {"recipe_id": 11, "calories": 480.0, "carbohydrates": 40.0, "protein": 45.0, "fat": 18.0}, # 닭가슴살 & 퀴노아 샐러드
    {"recipe_id": 12, "calories": 590.0, "carbohydrates": 65.0, "protein": 35.0, "fat": 22.0}, # 포케 볼 (연어/참치)
    {"recipe_id": 13, "calories": 620.0, "carbohydrates": 80.0, "protein": 30.0, "fat": 18.0}, # 멕시칸 비건 타코 세트
    {"recipe_id": 14, "calories": 750.0, "carbohydrates": 30.0, "protein": 55.0, "fat": 45.0}, # 저염 소고기 찹스테이크 & 구운 채소
    {"recipe_id": 15, "calories": 550.0, "carbohydrates": 50.0, "protein": 30.0, "fat": 25.0}, # 에그인헬 (Shakshuka)
    {"recipe_id": 16, "calories": 680.0, "carbohydrates": 90.0, "protein": 28.0, "fat": 25.0}, # 병아리콩 커리 & 난 (통밀)
    {"recipe_id": 17, "calories": 450.0, "carbohydrates": 55.0, "protein": 20.0, "fat": 16.0}, # 렌틸콩 수프 & 호밀빵
    {"recipe_id": 18, "calories": 720.0, "carbohydrates": 70.0, "protein": 45.0, "fat": 30.0}, # 돼지고기 앞다리살 간장 불고기 세트
    {"recipe_id": 19, "calories": 650.0, "carbohydrates": 75.0, "protein": 35.0, "fat": 25.0}, # 현미밥 & 버섯 된장찌개 세트
    {"recipe_id": 20, "calories": 510.0, "carbohydrates": 70.0, "protein": 20.0, "fat": 18.0}, # 참치마요 김밥 (저염) & 우동(소량)
    
    # 🌙 C. 저녁 식단 (Dinner, ID 21-30)
    {"recipe_id": 21, "calories": 580.0, "carbohydrates": 25.0, "protein": 40.0, "fat": 35.0}, # 연어 스테이크 & 아스파라거스
    {"recipe_id": 22, "calories": 620.0, "carbohydrates": 20.0, "protein": 50.0, "fat": 40.0}, # 양고기 숄더랙 구이 & 샐러드
    {"recipe_id": 23, "calories": 480.0, "carbohydrates": 60.0, "protein": 25.0, "fat": 15.0}, # 해산물 봉골레 파스타 (통밀면)
    {"recipe_id": 24, "calories": 350.0, "carbohydrates": 10.0, "protein": 30.0, "fat": 20.0}, # 두부 & 김치 볶음 (저염)
    {"recipe_id": 25, "calories": 380.0, "carbohydrates": 20.0, "protein": 22.0, "fat": 25.0}, # 토마토 & 모짜렐라 카프레제 세트
    {"recipe_id": 26, "calories": 490.0, "carbohydrates": 15.0, "protein": 55.0, "fat": 25.0}, # 매콤 닭봉 구이 & 콜리플라워 라이스
    {"recipe_id": 27, "calories": 540.0, "carbohydrates": 20.0, "protein": 45.0, "fat": 30.0}, # 참치 스테이크 & 구운 채소
    {"recipe_id": 28, "calories": 420.0, "carbohydrates": 65.0, "protein": 15.0, "fat": 12.0}, # 버섯 리조또 (보리)
    {"recipe_id": 29, "calories": 390.0, "carbohydrates": 30.0, "protein": 30.0, "fat": 15.0}, # 해물 순두부찌개 (맑은 국물)
    {"recipe_id": 30, "calories": 320.0, "carbohydrates": 40.0, "protein": 10.0, "fat": 12.0}, # 채소 가득 월남쌈 & 땅콩 소스
]


def upgrade() -> None:
    """데이터 마이그레이션 실행: 30개 레시피의 영양 성분 데이터를 'recipe_nutrition' 테이블에 삽입합니다."""

    recipe_nutrition_table = table(
        'recipe_nutrition',
        column('recipe_id', Integer),
        column('calories', Float),
        column('carbohydrates', Float),
        column('protein', Float),
        column('fat', Float),
    )

    # 정의된 고정 데이터를 bulk_insert로 삽입합니다.
    op.bulk_insert(recipe_nutrition_table, RECIPE_NUTRITION_DATA)
    print("30개 레시피에 대한 영양 성분 데이터(고정값) 삽입 완료.")


def downgrade() -> None:
    """데이터 마이그레이션 되돌리기: 삽입된 영양 성분 데이터를 삭제합니다."""

    # 삽입된 recipe_id (1번부터 30번) 리스트 생성
    recipe_ids_to_delete = [data['recipe_id'] for data in RECIPE_NUTRITION_DATA]
    
    recipe_nutrition_table = table(
        'recipe_nutrition',
        column('recipe_id', Integer),
    )

    op.execute(
        recipe_nutrition_table.delete().where(
            recipe_nutrition_table.c.recipe_id.in_(recipe_ids_to_delete)
        )
    )
    print("30개 레시피 영양 성분 데이터 삭제 완료 (롤백).")
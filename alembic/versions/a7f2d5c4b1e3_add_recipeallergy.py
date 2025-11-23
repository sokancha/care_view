"""Insert initial recipe_allergen data for 30 recipes (Total 54 entries)

Revision ID: a7f2d5c4b1e3
Revises: 6c3a1b2e4d0f
Create Date: 2025-11-20 19:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column 
from sqlalchemy import Integer


# revision identifiers, used by Alembic.
revision: str = 'a7f2d5c4b1e3'
down_revision: Union[str, Sequence[str], None] = '6c3a1b2e4d0f' # 최신 리비전 ID로 업데이트
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 30개 레시피와 알레르기 항목 매핑 정의 (총 54개 항목)
# 알레르기 ID는 이전에 삽입된 INITIAL_ALLERGIES의 순서(1부터 시작)를 따릅니다.
# 주요 알레르기 ID: 1:우유, 2:대두, 4:땅콩, 5:밀, 6:생선, 9:돼지고기, 11:토마토, 14:닭고기, 15:쇠고기, 17:조개류, 20:달걀, 21:아몬드, 32:쌀, 34:귀리, 35:보리, 36:렌틸콩, 37:병아리콩, 42:바나나
INITIAL_RECIPE_ALLERGENS = [
    # Recipe 1: 통밀 팬케이크 & 베리 세트 (밀, 우유, 달걀)
    {"recipe_id": 1, "allergy_id": 5},   # 밀 (팬케이크 가루)
    {"recipe_id": 1, "allergy_id": 1},   # 우유
    {"recipe_id": 1, "allergy_id": 20},  # 달걀

    # Recipe 2: 계란 스크램블 & 아보카도 토스트 (달걀, 밀, 우유)
    {"recipe_id": 2, "allergy_id": 20},  # 달걀
    {"recipe_id": 2, "allergy_id": 5},   # 밀 (통밀빵)
    {"recipe_id": 2, "allergy_id": 1},   # 우유 (스크램블 시 사용)

    # Recipe 3: 그릭 요거트 & 그래놀라 볼 (우유, 밀, 아몬드)
    {"recipe_id": 3, "allergy_id": 1},   # 우유 (요거트)
    {"recipe_id": 3, "allergy_id": 5},   # 밀 (그래놀라)
    {"recipe_id": 3, "allergy_id": 21},  # 아몬드 (견과류)

    # Recipe 4: 시금치 & 치즈 오믈렛 (달걀, 우유)
    {"recipe_id": 4, "allergy_id": 20},  # 달걀
    {"recipe_id": 4, "allergy_id": 1},   # 우유 (치즈)

    # Recipe 5: 오버나이트 오트밀 (견과류) (귀리, 우유, 아몬드)
    {"recipe_id": 5, "allergy_id": 34},  # 귀리
    {"recipe_id": 5, "allergy_id": 1},   # 우유
    {"recipe_id": 5, "allergy_id": 21},  # 아몬드

    # Recipe 6: 바나나 & 아몬드 스무디 (바나나, 아몬드, 우유)
    {"recipe_id": 6, "allergy_id": 42},  # 바나나
    {"recipe_id": 6, "allergy_id": 21},  # 아몬드
    {"recipe_id": 6, "allergy_id": 1},   # 우유 (우유/요거트 베이스)

    # Recipe 7: 두부 샐러드 & 현미 주먹밥 (대두, 쌀)
    {"recipe_id": 7, "allergy_id": 2},   # 대두 (두부)
    {"recipe_id": 7, "allergy_id": 32},  # 쌀 (현미 주먹밥)

    # Recipe 8: 닭가슴살 샌드위치 (통밀빵) (닭고기, 밀, 달걀)
    {"recipe_id": 8, "allergy_id": 14},  # 닭고기
    {"recipe_id": 8, "allergy_id": 5},   # 밀 (통밀빵)
    {"recipe_id": 8, "allergy_id": 20},  # 달걀 (마요네즈)

    # Recipe 9: 버섯 & 채소 볶음밥 (소량) (쌀, 대두)
    {"recipe_id": 9, "allergy_id": 32},  # 쌀
    {"recipe_id": 9, "allergy_id": 2},   # 대두 (간장/소스)

    # Recipe 10: 훈제 연어 & 크림치즈 베이글 (생선, 밀, 우유)
    {"recipe_id": 10, "allergy_id": 6},  # 생선 (연어)
    {"recipe_id": 10, "allergy_id": 5},  # 밀 (베이글)
    {"recipe_id": 10, "allergy_id": 1},  # 우유 (크림치즈)

    # Recipe 11: 닭가슴살 & 퀴노아 샐러드 (닭고기, 대두)
    {"recipe_id": 11, "allergy_id": 14}, # 닭고기
    {"recipe_id": 11, "allergy_id": 2},  # 대두 (드레싱)

    # Recipe 12: 포케 볼 (연어/참치) (생선, 대두, 쌀)
    {"recipe_id": 12, "allergy_id": 6},  # 생선 (연어/참치)
    {"recipe_id": 12, "allergy_id": 2},  # 대두 (간장)
    {"recipe_id": 12, "allergy_id": 32}, # 쌀 (밥)

    # Recipe 13: 멕시칸 비건 타코 세트 (밀, 렌틸콩)
    {"recipe_id": 13, "allergy_id": 5},  # 밀 (또띠아)
    {"recipe_id": 13, "allergy_id": 36}, # 렌틸콩

    # Recipe 14: 저염 소고기 찹스테이크 & 구운 채소 (쇠고기, 대두)
    {"recipe_id": 14, "allergy_id": 15}, # 쇠고기
    {"recipe_id": 14, "allergy_id": 2},  # 대두 (소스)

    # Recipe 15: 에그인헬 (Shakshuka) (달걀, 토마토, 밀)
    {"recipe_id": 15, "allergy_id": 20}, # 달걀
    {"recipe_id": 15, "allergy_id": 11}, # 토마토
    {"recipe_id": 15, "allergy_id": 5},  # 밀 (곁들임 빵)

    # Recipe 16: 병아리콩 커리 & 난 (통밀) (병아리콩, 밀)
    {"recipe_id": 16, "allergy_id": 37}, # 병아리콩
    {"recipe_id": 16, "allergy_id": 5},  # 밀 (난)

    # Recipe 17: 렌틸콩 수프 & 호밀빵 (렌틸콩, 밀)
    {"recipe_id": 17, "allergy_id": 36}, # 렌틸콩
    {"recipe_id": 17, "allergy_id": 5},  # 밀 (호밀빵)

    # Recipe 18: 돼지고기 앞다리살 간장 불고기 세트 (돼지고기, 대두, 쌀)
    {"recipe_id": 18, "allergy_id": 9},  # 돼지고기
    {"recipe_id": 18, "allergy_id": 2},  # 대두 (간장)
    {"recipe_id": 18, "allergy_id": 32}, # 쌀 (현미밥)

    # Recipe 19: 현미밥 & 버섯 된장찌개 세트 (쌀, 대두, 조개류)
    {"recipe_id": 19, "allergy_id": 32}, # 쌀
    {"recipe_id": 19, "allergy_id": 2},  # 대두 (된장)
    {"recipe_id": 19, "allergy_id": 17}, # 조개류 (육수)

    # Recipe 20: 참치마요 김밥 (저염) & 우동(소량) (생선, 달걀, 밀, 대두)
    {"recipe_id": 20, "allergy_id": 6},  # 생선 (참치)
    {"recipe_id": 20, "allergy_id": 20}, # 달걀 (마요네즈)
    {"recipe_id": 20, "allergy_id": 5},  # 밀 (우동면/김밥 밥)
    {"recipe_id": 20, "allergy_id": 2},  # 대두 (간장/소스)

    # Recipe 21: 연어 스테이크 & 아스파라거스 (생선)
    {"recipe_id": 21, "allergy_id": 6},  # 생선 (연어)

    # Recipe 22: 양고기 숄더랙 구이 & 샐러드 (대두)
    {"recipe_id": 22, "allergy_id": 2},  # 대두 (드레싱)

    # Recipe 23: 해산물 봉골레 파스타 (통밀면) (조개류, 밀, 대두)
    {"recipe_id": 23, "allergy_id": 17}, # 조개류
    {"recipe_id": 23, "allergy_id": 5},  # 밀 (파스타면)
    {"recipe_id": 23, "allergy_id": 2},  # 대두 (소스)

    # Recipe 24: 두부 & 김치 볶음 (저염) (대두, 쌀)
    {"recipe_id": 24, "allergy_id": 2},  # 대두 (두부)
    {"recipe_id": 24, "allergy_id": 32}, # 쌀 (현미밥)

    # Recipe 25: 토마토 & 모짜렐라 카프레제 세트 (토마토, 우유, 밀)
    {"recipe_id": 25, "allergy_id": 11}, # 토마토
    {"recipe_id": 25, "allergy_id": 1},  # 우유 (모짜렐라)
    {"recipe_id": 25, "allergy_id": 5},  # 밀 (곁들임 빵)

    # Recipe 26: 매콤 닭봉 구이 & 콜리플라워 라이스 (닭고기, 대두)
    {"recipe_id": 26, "allergy_id": 14}, # 닭고기
    {"recipe_id": 26, "allergy_id": 2},  # 대두 (소스)

    # Recipe 27: 참치 스테이크 & 구운 채소 (생선, 대두)
    {"recipe_id": 27, "allergy_id": 6},  # 생선 (참치)
    {"recipe_id": 27, "allergy_id": 2},  # 대두 (소스/드레싱)

    # Recipe 28: 버섯 리조또 (보리) (우유, 보리)
    {"recipe_id": 28, "allergy_id": 1},  # 우유 (크림/치즈)
    {"recipe_id": 28, "allergy_id": 35}, # 보리

    # Recipe 29: 해물 순두부찌개 (맑은 국물) (조개류, 대두, 쌀)
    {"recipe_id": 29, "allergy_id": 17}, # 조개류
    {"recipe_id": 29, "allergy_id": 2},  # 대두 (순두부)
    {"recipe_id": 29, "allergy_id": 32}, # 쌀 (현미밥)

    # Recipe 30: 채소 가득 월남쌈 & 땅콩 소스 (땅콩, 대두)
    {"recipe_id": 30, "allergy_id": 4},  # 땅콩 (땅콩 소스)
    {"recipe_id": 30, "allergy_id": 2},  # 대두 (땅콩 소스/라이스페이퍼)
]


def upgrade() -> None:
    """
    Recipe_Allergen 테이블에 초기 데이터를 삽입합니다.
    """
    # 1. recipe_allergen 테이블 객체 정의
    recipe_allergen_table = table(
        'recipe_allergen', 
        column('recipe_id', Integer),
        column('allergy_id', Integer),
    )

    # 2. 초기 데이터 삽입
    op.bulk_insert(
        recipe_allergen_table,
        INITIAL_RECIPE_ALLERGENS
    )
    print(f"총 {len(INITIAL_RECIPE_ALLERGENS)}개의 초기 Recipe Allergen 데이터 삽입 완료.")


def downgrade() -> None:
    """
    마이그레이션을 되돌려 삽입된 Recipe_Allergen 데이터를 삭제합니다.
    """
    # 삽입했던 레시피 ID 목록 추출
    recipe_ids_to_delete = tuple(
        set(r['recipe_id'] for r in INITIAL_RECIPE_ALLERGENS)
    )

    # recipe_id를 기준으로 해당 레코드들을 모두 삭제 (복합 PK이기 때문에 recipe_id로 삭제해도 무방함)
    op.execute(
        sa.text("DELETE FROM recipe_allergen WHERE recipe_id IN :ids").bindparams(ids=recipe_ids_to_delete)
    )
    print("Recipe Allergen 데이터 삭제 완료 (롤백).")
"""add_reicpe_allergen

Revision ID: af11d159a06f
Revises: b7773c86bd38
Create Date: 2025-12-03 00:08:02.825257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, text


# revision identifiers, used by Alembic.
revision: str = 'af11d159a06f'
down_revision: Union[str, Sequence[str], None] = 'b7773c86bd38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 레시피 ID와 알레르기 ID를 연결하는 초기 데이터
# Recipe ID: 1-30
# Allergy ID List (선택된 주요 알레르겐, 제공된 목록 기반):
# 1:우유, 2:대두, 4:땅콩, 5:밀, 6:생선, 8:새우, 9:돼지고기, 11:토마토, 14:닭고기, 15:쇠고기, 17:조개류, 20:달걀, 21:아몬드, 33:귀리, 34:보리, 35:호밀
INITIAL_RECIPE_ALLERGENS = [
    # 1. 통밀 팬케이크 & 베리 세트 (밀, 달걀, 우유)
    {"recipe_id": 1, "allergy_id": 5},
    {"recipe_id": 1, "allergy_id": 20},
    {"recipe_id": 1, "allergy_id": 1},

    # 2. 계란 스크램블 & 아보카도 토스트 (달걀, 밀 - 통밀빵)
    {"recipe_id": 2, "allergy_id": 20},
    {"recipe_id": 2, "allergy_id": 5},

    # 3. 그릭 요거트 & 그래놀라 볼 (우유, 밀, 아몬드/견과류)
    {"recipe_id": 3, "allergy_id": 1},
    {"recipe_id": 3, "allergy_id": 5},
    {"recipe_id": 3, "allergy_id": 21}, 

    # 4. 시금치 & 치즈 오믈렛 (달걀, 우유)
    {"recipe_id": 4, "allergy_id": 20},
    {"recipe_id": 4, "allergy_id": 1},

    # 5. 오버나이트 오트밀 (귀리, 우유, 아몬드/견과류)
    {"recipe_id": 5, "allergy_id": 33}, 
    {"recipe_id": 5, "allergy_id": 1},
    {"recipe_id": 5, "allergy_id": 21},

    # 6. 바나나 & 아몬드 스무디 (우유, 아몬드/견과류)
    {"recipe_id": 6, "allergy_id": 1},
    {"recipe_id": 6, "allergy_id": 21},

    # 7. 두부 샐러드 & 현미 주먹밥 (대두 - 두부)
    {"recipe_id": 7, "allergy_id": 2},

    # 8. 닭가슴살 샌드위치 (통밀빵) (닭고기, 밀, 달걀 - 마요네즈)
    {"recipe_id": 8, "allergy_id": 14},
    {"recipe_id": 8, "allergy_id": 5},
    {"recipe_id": 8, "allergy_id": 20},

    # 9. 버섯 & 채소 볶음밥 (대두, 밀 - 간장)
    {"recipe_id": 9, "allergy_id": 2},
    {"recipe_id": 9, "allergy_id": 5},

    # 10. 훈제 연어 & 크림치즈 베이글 (생선, 밀, 우유)
    {"recipe_id": 10, "allergy_id": 6},
    {"recipe_id": 10, "allergy_id": 5},
    {"recipe_id": 10, "allergy_id": 1},

    # 11. 닭가슴살 & 퀴노아 샐러드 (닭고기)
    {"recipe_id": 11, "allergy_id": 14},

    # 12. 포케 볼 (연어/참치) (생선, 대두, 밀 - 간장)
    {"recipe_id": 12, "allergy_id": 6},
    {"recipe_id": 12, "allergy_id": 2},
    {"recipe_id": 12, "allergy_id": 5},

    # 13. 멕시칸 비건 타코 세트 (대두 - 두부/콩, 밀 - 또띠아)
    {"recipe_id": 13, "allergy_id": 2},
    {"recipe_id": 13, "allergy_id": 5},

    # 14. 저염 소고기 찹스테이크 & 구운 채소 (쇠고기)
    {"recipe_id": 14, "allergy_id": 15},

    # 15. 에그인헬 (Shakshuka) (토마토, 달걀, 우유 - 치즈)
    {"recipe_id": 15, "allergy_id": 11},
    {"recipe_id": 15, "allergy_id": 20},
    {"recipe_id": 15, "allergy_id": 1},

    # 16. 병아리콩 커리 & 난 (통밀) (밀, 우유 - 커리/난 반죽)
    {"recipe_id": 16, "allergy_id": 5},
    {"recipe_id": 16, "allergy_id": 1},

    # 17. 렌틸콩 수프 & 호밀빵 (호밀)
    {"recipe_id": 17, "allergy_id": 35},

    # 18. 돼지고기 앞다리살 간장 불고기 세트 (돼지고기, 대두, 밀 - 간장)
    {"recipe_id": 18, "allergy_id": 9},
    {"recipe_id": 18, "allergy_id": 2},
    {"recipe_id": 18, "allergy_id": 5},

    # 19. 현미밥 & 버섯 된장찌개 세트 (대두 - 된장, 두부)
    {"recipe_id": 19, "allergy_id": 2},

    # 20. 참치마요 김밥 (저염) & 우동(소량) (생선, 달걀, 밀 - 우동)
    {"recipe_id": 20, "allergy_id": 6},
    {"recipe_id": 20, "allergy_id": 20},
    {"recipe_id": 20, "allergy_id": 5},

    # 21. 연어 스테이크 & 아스파라거스 (생선)
    {"recipe_id": 21, "allergy_id": 6},

    # 22. 양고기 숄더랙 구이 & 샐러드 (양고기는 주요 알레르겐 목록에서 제외)
    # 알레르기 정보 없음

    # 23. 해산물 봉골레 파스타 (통밀면) (조개류, 밀)
    {"recipe_id": 23, "allergy_id": 17},
    {"recipe_id": 23, "allergy_id": 5},

    # 24. 두부 & 김치 볶음 (저염) (대두)
    {"recipe_id": 24, "allergy_id": 2},

    # 25. 토마토 & 모짜렐라 카프레제 세트 (토마토, 우유)
    {"recipe_id": 25, "allergy_id": 11},
    {"recipe_id": 25, "allergy_id": 1},

    # 26. 매콤 닭봉 구이 & 콜리플라워 라이스 (닭고기, 대두, 밀 - 고추장)
    {"recipe_id": 26, "allergy_id": 14},
    {"recipe_id": 26, "allergy_id": 2},
    {"recipe_id": 26, "allergy_id": 5},

    # 27. 참치 스테이크 & 구운 채소 (생선)
    {"recipe_id": 27, "allergy_id": 6},

    # 28. 버섯 리조또 (보리) (보리, 우유 - 치즈)
    {"recipe_id": 28, "allergy_id": 34},
    {"recipe_id": 28, "allergy_id": 1},

    # 29. 해물 순두부찌개 (대두, 새우)
    {"recipe_id": 29, "allergy_id": 2},
    {"recipe_id": 29, "allergy_id": 8},

    # 30. 채소 가득 월남쌈 & 땅콩 소스 (땅콩, 닭고기)
    {"recipe_id": 30, "allergy_id": 4},
    {"recipe_id": 30, "allergy_id": 14}, 
]


def upgrade() -> None:
    """Upgrade schema: recipe_allergen 테이블에 초기 데이터를 삽입합니다."""
    
    # 1. bulk_insert를 위한 테이블 객체 정의
    recipe_allergen_table = table(
        'recipe_allergen',
        column('recipe_id', Integer),
        column('allergy_id', Integer),
    )
    
    # 2. 초기 데이터 삽입
    # 데이터 삽입 전 기존 데이터 삭제 (재실행 시 중복 방지)
    op.execute(text("DELETE FROM recipe_allergen"))
    
    op.bulk_insert(
        recipe_allergen_table,
        INITIAL_RECIPE_ALLERGENS
    )
    print(f"총 {len(INITIAL_RECIPE_ALLERGENS)}개의 RecipeAllergen 연결 데이터 삽입 완료.")


def downgrade() -> None:
    """Downgrade schema: recipe_allergen 테이블에 삽입된 데이터를 삭제합니다."""
    # recipe_allergen 테이블의 모든 데이터를 삭제하여 롤백합니다.
    op.execute(text("DELETE FROM recipe_allergen"))
    print("recipe_allergen 테이블의 초기 데이터 삭제 완료 (롤백).")

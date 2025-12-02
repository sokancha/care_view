"""add_item_ingredient

Revision ID: b7773c86bd38
Revises: 6f4b37574943
Create Date: 2025-12-03 00:03:26.021165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float, text


# revision identifiers, used by Alembic.
revision: str = 'b7773c86bd38'
down_revision: Union[str, Sequence[str], None] = '6f4b37574943'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Meal Item과 Ingredient를 연결하는 초기 데이터 (총 47개 Item의 구성 재료)
# item_id는 요청하신 Meal Item 목록을 기준으로 작성되었으며, ingredient_id는 이전 마이그레이션의 ID를 사용합니다.
INITIAL_ITEM_INGREDIENTS = [
    # 1. 통밀 팬케이크
    {"item_id": 1, "ingredient_id": 1, "amount": 100.0, "unit": "g"},       # 통밀
    {"item_id": 1, "ingredient_id": 3, "amount": 1.0, "unit": "개"},        # 계란
    {"item_id": 1, "ingredient_id": 48, "amount": 100.0, "unit": "ml"},     # 우유
    {"item_id": 1, "ingredient_id": 49, "amount": 5.0, "unit": "g"},        # 베이킹 파우더
    {"item_id": 1, "ingredient_id": 46, "amount": 15.0, "unit": "ml"},      # 메이플 시럽
    
    # 2. 베리 세트
    {"item_id": 2, "ingredient_id": 2, "amount": 150.0, "unit": "g"},       # 베리
    
    # 3. 계란 스크램블
    {"item_id": 3, "ingredient_id": 3, "amount": 2.0, "unit": "개"},        # 계란
    {"item_id": 3, "ingredient_id": 45, "amount": 5.0, "unit": "g"},        # 버터 (또는 올리브 오일)
    {"item_id": 3, "ingredient_id": 50, "amount": 1.0, "unit": "g"},        # 소금
    {"item_id": 3, "ingredient_id": 51, "amount": 0.5, "unit": "g"},        # 후추
    
    # 4. 아보카도 토스트
    {"item_id": 4, "ingredient_id": 4, "amount": 100.0, "unit": "g"},       # 아보카도
    {"item_id": 4, "ingredient_id": 14, "amount": 1.0, "unit": "장"},       # 현미 (또는 통밀) 빵
    {"item_id": 4, "ingredient_id": 50, "amount": 0.5, "unit": "g"},        # 소금
    {"item_id": 4, "ingredient_id": 52, "amount": 5.0, "unit": "ml"},       # 올리브 오일
    
    # 5. 그릭 요거트
    {"item_id": 5, "ingredient_id": 5, "amount": 150.0, "unit": "g"},       # 요거트 (그릭)
    {"item_id": 5, "ingredient_id": 47, "amount": 10.0, "unit": "g"},       # 꿀 (선택)
    
    # 6. 그래놀라
    {"item_id": 6, "ingredient_id": 6, "amount": 50.0, "unit": "g"},        # 그래놀라
    {"item_id": 6, "ingredient_id": 48, "amount": 100.0, "unit": "ml"},     # 우유
    
    # 7. 시금치 & 치즈 오믈렛
    {"item_id": 7, "ingredient_id": 3, "amount": 3.0, "unit": "개"},        # 계란
    {"item_id": 7, "ingredient_id": 7, "amount": 50.0, "unit": "g"},        # 시금치
    {"item_id": 7, "ingredient_id": 8, "amount": 30.0, "unit": "g"},        # 치즈
    {"item_id": 7, "ingredient_id": 52, "amount": 5.0, "unit": "ml"},       # 올리브 오일
    
    # 8. 오버나이트 오트밀
    {"item_id": 8, "ingredient_id": 9, "amount": 50.0, "unit": "g"},        # 오트밀
    {"item_id": 8, "ingredient_id": 48, "amount": 150.0, "unit": "ml"},     # 우유
    {"item_id": 8, "ingredient_id": 2, "amount": 50.0, "unit": "g"},        # 베리
    
    # 9. 바나나 스무디
    {"item_id": 9, "ingredient_id": 10, "amount": 1.0, "unit": "개"},       # 바나나
    {"item_id": 9, "ingredient_id": 48, "amount": 150.0, "unit": "ml"},     # 우유
    
    # 10. 아몬드
    {"item_id": 10, "ingredient_id": 11, "amount": 30.0, "unit": "g"},      # 아몬드
    
    # 11. 두부 샐러드
    {"item_id": 11, "ingredient_id": 12, "amount": 100.0, "unit": "g"},     # 두부
    {"item_id": 11, "ingredient_id": 13, "amount": 50.0, "unit": "g"},      # 양상추
    {"item_id": 11, "ingredient_id": 69, "amount": 30.0, "unit": "g"},      # 당근
    {"item_id": 11, "ingredient_id": 52, "amount": 15.0, "unit": "ml"},     # 올리브 오일 (드레싱)
    
    # 12. 현미 주먹밥
    {"item_id": 12, "ingredient_id": 14, "amount": 150.0, "unit": "g"},     # 현미
    {"item_id": 12, "ingredient_id": 31, "amount": 2.0, "unit": "장"},      # 김
    {"item_id": 12, "ingredient_id": 57, "amount": 3.0, "unit": "g"},       # 깨
    {"item_id": 12, "ingredient_id": 58, "amount": 5.0, "unit": "ml"},      # 참기름
    
    # 13. 닭가슴살 샌드위치
    {"item_id": 13, "ingredient_id": 15, "amount": 100.0, "unit": "g"},     # 닭고기 (가슴살)
    {"item_id": 13, "ingredient_id": 13, "amount": 30.0, "unit": "g"},      # 양상추
    {"item_id": 13, "ingredient_id": 26, "amount": 30.0, "unit": "g"},      # 토마토
    {"item_id": 13, "ingredient_id": 14, "amount": 2.0, "unit": "장"},      # 통밀빵 (14번 현미를 통밀 대용으로)
    {"item_id": 13, "ingredient_id": 63, "amount": 10.0, "unit": "g"},      # 마요네즈 (소량)
    
    # 14. 통밀빵 (단품)
    {"item_id": 14, "ingredient_id": 1, "amount": 100.0, "unit": "g"},      # 통밀
    
    # 15. 버섯 볶음밥
    {"item_id": 15, "ingredient_id": 16, "amount": 50.0, "unit": "g"},      # 버섯
    {"item_id": 15, "ingredient_id": 17, "amount": 150.0, "unit": "g"},     # 쌀 (밥)
    {"item_id": 15, "ingredient_id": 68, "amount": 30.0, "unit": "g"},      # 양파
    {"item_id": 15, "ingredient_id": 54, "amount": 5.0, "unit": "ml"},      # 간장
    
    # 16. 채소 볶음밥
    {"item_id": 16, "ingredient_id": 17, "amount": 150.0, "unit": "g"},     # 쌀 (밥)
    {"item_id": 16, "ingredient_id": 68, "amount": 30.0, "unit": "g"},      # 양파
    {"item_id": 16, "ingredient_id": 69, "amount": 30.0, "unit": "g"},      # 당근
    {"item_id": 16, "ingredient_id": 70, "amount": 30.0, "unit": "g"},      # 감자
    {"item_id": 16, "ingredient_id": 52, "amount": 10.0, "unit": "ml"},     # 올리브 오일
    
    # 17. 훈제 연어
    {"item_id": 17, "ingredient_id": 18, "amount": 100.0, "unit": "g"},     # 연어
    
    # 18. 크림치즈 베이글
    {"item_id": 18, "ingredient_id": 20, "amount": 1.0, "unit": "개"},      # 베이글
    {"item_id": 18, "ingredient_id": 19, "amount": 30.0, "unit": "g"},      # 크림치즈
    
    # 19. 퀴노아 샐러드
    {"item_id": 19, "ingredient_id": 21, "amount": 50.0, "unit": "g"},      # 퀴노아
    {"item_id": 19, "ingredient_id": 13, "amount": 50.0, "unit": "g"},      # 양상추
    {"item_id": 19, "ingredient_id": 26, "amount": 30.0, "unit": "g"},      # 토마토
    {"item_id": 19, "ingredient_id": 52, "amount": 15.0, "unit": "ml"},     # 올리브 오일 (드레싱)

    # 20. 포케 볼
    {"item_id": 20, "ingredient_id": 17, "amount": 150.0, "unit": "g"},     # 쌀 (밥)
    {"item_id": 20, "ingredient_id": 22, "amount": 50.0, "unit": "g"},      # 참치
    {"item_id": 20, "ingredient_id": 4, "amount": 30.0, "unit": "g"},       # 아보카도
    {"item_id": 20, "ingredient_id": 68, "amount": 20.0, "unit": "g"},      # 양파
    {"item_id": 20, "ingredient_id": 54, "amount": 10.0, "unit": "ml"},     # 간장 (소스)
    
    # 21. 비건 타코
    {"item_id": 21, "ingredient_id": 73, "amount": 2.0, "unit": "장"},      # 밀 또띠아
    {"item_id": 21, "ingredient_id": 12, "amount": 50.0, "unit": "g"},      # 두부
    {"item_id": 21, "ingredient_id": 13, "amount": 20.0, "unit": "g"},      # 양상추
    {"item_id": 21, "ingredient_id": 26, "amount": 20.0, "unit": "g"},      # 토마토
    {"item_id": 21, "ingredient_id": 68, "amount": 10.0, "unit": "g"},      # 양파
    
    # 22. 멕시칸 렌틸콩
    {"item_id": 22, "ingredient_id": 23, "amount": 100.0, "unit": "g"},     # 렌틸콩
    {"item_id": 22, "ingredient_id": 26, "amount": 50.0, "unit": "g"},      # 토마토
    {"item_id": 22, "ingredient_id": 68, "amount": 30.0, "unit": "g"},      # 양파
    {"item_id": 22, "ingredient_id": 59, "amount": 5.0, "unit": "g"},       # 다진 마늘
    
    # 23. 저염 소고기 찹스테이크
    {"item_id": 23, "ingredient_id": 25, "amount": 150.0, "unit": "g"},     # 소고기
    {"item_id": 23, "ingredient_id": 16, "amount": 30.0, "unit": "g"},      # 버섯
    {"item_id": 23, "ingredient_id": 68, "amount": 30.0, "unit": "g"},      # 양파
    {"item_id": 23, "ingredient_id": 52, "amount": 10.0, "unit": "ml"},     # 올리브 오일
    
    # 24. 구운 채소
    {"item_id": 24, "ingredient_id": 33, "amount": 50.0, "unit": "g"},      # 아스파라거스
    {"item_id": 24, "ingredient_id": 69, "amount": 50.0, "unit": "g"},      # 당근
    {"item_id": 24, "ingredient_id": 70, "amount": 50.0, "unit": "g"},      # 감자
    {"item_id": 24, "ingredient_id": 52, "amount": 5.0, "unit": "ml"},      # 올리브 오일
    
    # 25. 에그인헬 (샥슈카)
    {"item_id": 25, "ingredient_id": 26, "amount": 200.0, "unit": "g"},     # 토마토 (소스)
    {"item_id": 25, "ingredient_id": 3, "amount": 2.0, "unit": "개"},        # 계란
    {"item_id": 25, "ingredient_id": 59, "amount": 5.0, "unit": "g"},       # 다진 마늘
    {"item_id": 25, "ingredient_id": 78, "amount": 20.0, "unit": "g"},      # 모짜렐라 치즈
    {"item_id": 25, "ingredient_id": 79, "amount": 2.0, "unit": "g"},       # 바질
    
    # 26. 병아리콩 커리
    {"item_id": 26, "ingredient_id": 24, "amount": 100.0, "unit": "g"},     # 병아리콩
    {"item_id": 26, "ingredient_id": 27, "amount": 30.0, "unit": "g"},      # 커리
    {"item_id": 26, "ingredient_id": 68, "amount": 30.0, "unit": "g"},      # 양파
    
    # 27. 통밀 난
    {"item_id": 27, "ingredient_id": 1, "amount": 50.0, "unit": "g"},       # 통밀
    {"item_id": 27, "ingredient_id": 5, "amount": 30.0, "unit": "g"},       # 요거트 (반죽용)
    
    # 28. 렌틸콩 수프
    {"item_id": 28, "ingredient_id": 23, "amount": 80.0, "unit": "g"},      # 렌틸콩
    {"item_id": 28, "ingredient_id": 68, "amount": 20.0, "unit": "g"},      # 양파
    {"item_id": 28, "ingredient_id": 69, "amount": 10.0, "unit": "g"},      # 당근
    
    # 29. 호밀빵 (단품)
    {"item_id": 29, "ingredient_id": 28, "amount": 100.0, "unit": "g"},     # 호밀
    
    # 30. 돼지고기 앞다리살 간장 불고기
    {"item_id": 30, "ingredient_id": 29, "amount": 150.0, "unit": "g"},     # 돼지고기
    {"item_id": 30, "ingredient_id": 54, "amount": 15.0, "unit": "ml"},     # 간장
    {"item_id": 30, "ingredient_id": 59, "amount": 5.0, "unit": "g"},       # 다진 마늘
    {"item_id": 30, "ingredient_id": 68, "amount": 30.0, "unit": "g"},      # 양파
    
    # 31. 현미밥 (단품)
    {"item_id": 31, "ingredient_id": 14, "amount": 150.0, "unit": "g"},     # 현미
    
    # 32. 버섯 된장찌개
    {"item_id": 32, "ingredient_id": 16, "amount": 50.0, "unit": "g"},      # 버섯
    {"item_id": 32, "ingredient_id": 30, "amount": 20.0, "unit": "g"},      # 된장
    {"item_id": 32, "ingredient_id": 12, "amount": 50.0, "unit": "g"},      # 두부
    {"item_id": 32, "ingredient_id": 71, "amount": 10.0, "unit": "g"},      # 대파
    {"item_id": 32, "ingredient_id": 75, "amount": 300.0, "unit": "ml"},    # 육수 재료
    
    # 33. 참치마요 김밥
    {"item_id": 33, "ingredient_id": 17, "amount": 100.0, "unit": "g"},     # 쌀 (밥)
    {"item_id": 33, "ingredient_id": 31, "amount": 1.0, "unit": "장"},      # 김
    {"item_id": 33, "ingredient_id": 22, "amount": 30.0, "unit": "g"},      # 참치
    {"item_id": 33, "ingredient_id": 63, "amount": 10.0, "unit": "g"},      # 마요네즈
    
    # 34. 우동 (소량)
    {"item_id": 34, "ingredient_id": 32, "amount": 100.0, "unit": "g"},     # 우동면
    {"item_id": 34, "ingredient_id": 75, "amount": 250.0, "unit": "ml"},    # 육수 재료
    
    # 35. 연어 스테이크
    {"item_id": 35, "ingredient_id": 18, "amount": 150.0, "unit": "g"},     # 연어
    {"item_id": 35, "ingredient_id": 52, "amount": 10.0, "unit": "ml"},     # 올리브 오일
    {"item_id": 35, "ingredient_id": 50, "amount": 1.0, "unit": "g"},        # 소금
    {"item_id": 35, "ingredient_id": 51, "amount": 0.5, "unit": "g"},        # 후추
    
    # 36. 아스파라거스 (단품)
    {"item_id": 36, "ingredient_id": 33, "amount": 100.0, "unit": "g"},     # 아스파라거스
    
    # 37. 양고기 숄더랙 구이
    {"item_id": 37, "ingredient_id": 34, "amount": 200.0, "unit": "g"},     # 양고기
    {"item_id": 37, "ingredient_id": 52, "amount": 10.0, "unit": "ml"},     # 올리브 오일
    {"item_id": 37, "ingredient_id": 50, "amount": 1.0, "unit": "g"},        # 소금
    {"item_id": 37, "ingredient_id": 51, "amount": 0.5, "unit": "g"},        # 후추
    
    # 38. 해산물 봉골레 파스타
    {"item_id": 38, "ingredient_id": 37, "amount": 100.0, "unit": "g"},     # 파스타면
    {"item_id": 38, "ingredient_id": 35, "amount": 100.0, "unit": "g"},     # 조개
    {"item_id": 38, "ingredient_id": 52, "amount": 15.0, "unit": "ml"},     # 올리브 오일
    {"item_id": 38, "ingredient_id": 59, "amount": 5.0, "unit": "g"},       # 다진 마늘
    
    # 39. 두부 & 김치 볶음
    {"item_id": 39, "ingredient_id": 12, "amount": 150.0, "unit": "g"},     # 두부
    {"item_id": 39, "ingredient_id": 38, "amount": 100.0, "unit": "g"},     # 김치
    {"item_id": 39, "ingredient_id": 53, "amount": 10.0, "unit": "ml"},     # 식용유
    
    # 40. 토마토 & 모짜렐라 카프레제
    {"item_id": 40, "ingredient_id": 26, "amount": 100.0, "unit": "g"},     # 토마토
    {"item_id": 40, "ingredient_id": 78, "amount": 50.0, "unit": "g"},      # 모짜렐라 치즈
    {"item_id": 40, "ingredient_id": 79, "amount": 2.0, "unit": "g"},       # 바질
    {"item_id": 40, "ingredient_id": 52, "amount": 5.0, "unit": "ml"},      # 올리브 오일
    
    # 41. 매콤 닭봉 구이
    {"item_id": 41, "ingredient_id": 74, "amount": 150.0, "unit": "g"},     # 닭봉
    {"item_id": 41, "ingredient_id": 55, "amount": 10.0, "unit": "g"},      # 고추장
    {"item_id": 41, "ingredient_id": 56, "amount": 5.0, "unit": "g"},       # 고춧가루
    {"item_id": 41, "ingredient_id": 59, "amount": 5.0, "unit": "g"},       # 다진 마늘
    
    # 42. 콜리플라워 라이스
    {"item_id": 42, "ingredient_id": 39, "amount": 150.0, "unit": "g"},     # 콜리플라워
    {"item_id": 42, "ingredient_id": 52, "amount": 5.0, "unit": "ml"},      # 올리브 오일
    
    # 43. 참치 스테이크
    {"item_id": 43, "ingredient_id": 22, "amount": 150.0, "unit": "g"},     # 참치 (스테이크용)
    {"item_id": 43, "ingredient_id": 50, "amount": 1.0, "unit": "g"},        # 소금
    {"item_id": 43, "ingredient_id": 51, "amount": 0.5, "unit": "g"},        # 후추
    
    # 44. 보리 리조또
    {"item_id": 44, "ingredient_id": 40, "amount": 100.0, "unit": "g"},     # 보리
    {"item_id": 44, "ingredient_id": 16, "amount": 50.0, "unit": "g"},      # 버섯
    {"item_id": 44, "ingredient_id": 8, "amount": 20.0, "unit": "g"},       # 치즈 (파마산)
    {"item_id": 44, "ingredient_id": 75, "amount": 200.0, "unit": "ml"},    # 육수 재료
    
    # 45. 해물 순두부찌개
    {"item_id": 45, "ingredient_id": 12, "amount": 200.0, "unit": "g"},     # 두부 (순두부)
    {"item_id": 45, "ingredient_id": 36, "amount": 50.0, "unit": "g"},      # 새우
    {"item_id": 45, "ingredient_id": 56, "amount": 5.0, "unit": "g"},       # 고춧가루
    {"item_id": 45, "ingredient_id": 75, "amount": 250.0, "unit": "ml"},    # 육수 재료
    
    # 46. 채소 가득 월남쌈
    {"item_id": 46, "ingredient_id": 41, "amount": 5.0, "unit": "장"},      # 라이스페이퍼
    {"item_id": 46, "ingredient_id": 13, "amount": 30.0, "unit": "g"},      # 양상추
    {"item_id": 46, "ingredient_id": 69, "amount": 30.0, "unit": "g"},      # 당근
    {"item_id": 46, "ingredient_id": 15, "amount": 50.0, "unit": "g"},      # 닭고기 (닭가슴살)
    
    # 47. 땅콩 소스 (월남쌈용)
    {"item_id": 47, "ingredient_id": 42, "amount": 20.0, "unit": "g"},      # 땅콩
    {"item_id": 47, "ingredient_id": 54, "amount": 10.0, "unit": "ml"},     # 간장
]


def upgrade() -> None:
    """Upgrade schema: item_ingredient 테이블에 초기 데이터를 삽입합니다."""
    
    # 1. bulk_insert를 위한 테이블 객체 정의
    item_ingredient_table = table(
        'item_ingredient',
        column('item_id', Integer),
        column('ingredient_id', Integer),
        column('amount', Float),
        column('unit', String),
    )
    
    # 2. 초기 데이터 삽입
    # 데이터 삽입 전 기존 데이터 삭제 (재실행 시 중복 방지)
    op.execute(text("DELETE FROM item_ingredient"))
    
    op.bulk_insert(
        item_ingredient_table,
        INITIAL_ITEM_INGREDIENTS
    )
    print(f"총 {len(INITIAL_ITEM_INGREDIENTS)}개의 ItemIngredient 연결 데이터 삽입 완료.")


def downgrade() -> None:
    """Downgrade schema: item_ingredient 테이블에 삽입된 데이터를 삭제합니다."""
    # item_ingredient 테이블의 모든 데이터를 삭제하여 롤백합니다.
    op.execute(text("DELETE FROM item_ingredient"))
    print("item_ingredient 테이블의 초기 데이터 삭제 완료 (롤백).")

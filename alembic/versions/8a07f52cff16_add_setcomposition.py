from typing import Sequence, Union, List, Dict, Any

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '8a07f52cff16'
down_revision: Union[str, Sequence[str], None] = '9a30336e2818'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# =================================================================
# SET_COMPOSITION_DATA: RecipeSet과 ConvenienceItem 간의 M:N 연결 데이터
# =================================================================
SET_COMPOSITION_DATA: List[Dict[str, Any]] = [
    # 1. 육개장 컵라면 & 참치마요 삼각김밥
    {'set_id': 1, 'item_id': 1, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 1, 'item_id': 2, 'amount': 1.0, 'unit': '개'},
    
    # 2. 신라면 & 공기밥 & 스트링치즈
    {'set_id': 2, 'item_id': 3, 'amount': 1.0, 'unit': '봉지'},
    {'set_id': 2, 'item_id': 4, 'amount': 2.0, 'unit': '개'},
    {'set_id': 2, 'item_id': 5, 'amount': 1.0, 'unit': '개'},

    # 3. 튀김우동 & 김치볶음밥 삼각김밥
    {'set_id': 3, 'item_id': 6, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 3, 'item_id': 7, 'amount': 1.0, 'unit': '개'},

    # 4. 참깨라면 & 왕만두 4개
    {'set_id': 4, 'item_id': 8, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 4, 'item_id': 9, 'amount': 4.0, 'unit': '개'}, # 왕만두 4개

    # 5. 진라면(순한맛) & 전주비빔 삼각김밥 2개
    {'set_id': 5, 'item_id': 10, 'amount': 1.0, 'unit': '봉지'},
    {'set_id': 5, 'item_id': 11, 'amount': 2.0, 'unit': '개'},

    # 6. 육개장 컵밥 & 핫바 2종
    {'set_id': 6, 'item_id': 12, 'amount': 1.0, 'unit': '개'},
    {'set_id': 6, 'item_id': 13, 'amount': 2.0, 'unit': '개'},

    # 7. 오모리 김치찌개 라면 & 계란 2개
    {'set_id': 7, 'item_id': 14, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 7, 'item_id': 15, 'amount': 2.0, 'unit': '개'},
    
    # 8. 미역국 컵밥 & 불고기 김밥
    {'set_id': 8, 'item_id': 16, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 8, 'item_id': 17, 'amount': 1.0, 'unit': '줄'},

    # 9. 사발면 & 김치 볶음밥 도시락
    {'set_id': 9, 'item_id': 18, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 9, 'item_id': 19, 'amount': 1.0, 'unit': '개'},

    # 10. 봉지 라면 & 물만두
    {'set_id': 10, 'item_id': 20, 'amount': 1.0, 'unit': '봉지'},
    {'set_id': 10, 'item_id': 21, 'amount': 1.0, 'unit': '봉지'}, # 물만두 1봉지

    # 11. 매콤 떡볶이 & 순대
    {'set_id': 11, 'item_id': 22, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 11, 'item_id': 23, 'amount': 1.0, 'unit': '접시'},

    # 12. 비빔면 2개 & 삶은 계란 2개
    {'set_id': 12, 'item_id': 24, 'amount': 2.0, 'unit': '개'},
    {'set_id': 12, 'item_id': 25, 'amount': 2.0, 'unit': '개'},

    # 13. 크림 파스타 & 마늘빵 1개
    {'set_id': 13, 'item_id': 26, 'amount': 1.0, 'unit': '개'},
    {'set_id': 13, 'item_id': 27, 'amount': 1.0, 'unit': '개'},

    # 14. 핫도그 2개 & 미니 콜라
    {'set_id': 14, 'item_id': 28, 'amount': 2.0, 'unit': '개'},
    {'set_id': 14, 'item_id': 29, 'amount': 1.0, 'unit': '캔'},

    # 15. 불닭 컵라면 & 김밥 한 줄
    {'set_id': 15, 'item_id': 30, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 15, 'item_id': 31, 'amount': 1.0, 'unit': '줄'},

    # 16. 고기반찬 도시락 & 미니 컵라면
    {'set_id': 16, 'item_id': 32, 'amount': 1.0, 'unit': '개'},
    {'set_id': 16, 'item_id': 33, 'amount': 1.0, 'unit': '컵'},

    # 17. 비빔밥 컵 & 미니 된장국
    {'set_id': 17, 'item_id': 34, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 17, 'item_id': 35, 'amount': 1.0, 'unit': '개'},

    # 18. 제육볶음 덮밥 & 매실 음료
    {'set_id': 18, 'item_id': 36, 'amount': 1.0, 'unit': '개'},
    {'set_id': 18, 'item_id': 37, 'amount': 1.0, 'unit': '병'},

    # 19. 불고기 백반 도시락 & 보리차
    {'set_id': 19, 'item_id': 38, 'amount': 1.0, 'unit': '개'},
    {'set_id': 19, 'item_id': 39, 'amount': 1.0, 'unit': '병'},

    # 20. 돈까스 도시락 & 미니 젤리
    {'set_id': 20, 'item_id': 40, 'amount': 1.0, 'unit': '개'},
    {'set_id': 20, 'item_id': 41, 'amount': 1.0, 'unit': '봉지'},

    # 21. 김치찌개 도시락 & 흰 쌀밥
    {'set_id': 21, 'item_id': 42, 'amount': 1.0, 'unit': '개'},
    {'set_id': 21, 'item_id': 43, 'amount': 1.0, 'unit': '공기'},

    # 22. 카레 컵밥 & 닭가슴살 큐브
    {'set_id': 22, 'item_id': 44, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 22, 'item_id': 45, 'amount': 1.0, 'unit': '팩'},

    # 23. 미니 닭볶음탕 & 주먹밥 1개
    {'set_id': 23, 'item_id': 46, 'amount': 1.0, 'unit': '개'},
    {'set_id': 23, 'item_id': 47, 'amount': 1.0, 'unit': '개'},

    # 24. 콩나물 해장국 컵 & 숙취 해소 음료
    {'set_id': 24, 'item_id': 48, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 24, 'item_id': 49, 'amount': 1.0, 'unit': '병'},

    # 25. 따뜻한 어묵탕 & 소시지바
    {'set_id': 25, 'item_id': 50, 'amount': 1.0, 'unit': '개'},
    {'set_id': 25, 'item_id': 51, 'amount': 1.0, 'unit': '개'},

    # 26. 치즈 불닭 컵밥 & 쿨피스
    {'set_id': 26, 'item_id': 52, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 26, 'item_id': 53, 'amount': 1.0, 'unit': '팩'},

    # 27. 불고기 김밥 & 봉지 라면
    {'set_id': 27, 'item_id': 17, 'amount': 1.0, 'unit': '줄'},
    {'set_id': 27, 'item_id': 20, 'amount': 1.0, 'unit': '봉지'},

    # 28. 참치마요 주먹밥 & 컵 떡볶이
    {'set_id': 28, 'item_id': 54, 'amount': 1.0, 'unit': '개'},
    {'set_id': 28, 'item_id': 55, 'amount': 1.0, 'unit': '컵'},

    # 29. 짜파게티 & 계란 후라이 2개
    {'set_id': 29, 'item_id': 56, 'amount': 1.0, 'unit': '봉지'},
    {'set_id': 29, 'item_id': 57, 'amount': 2.0, 'unit': '개'},

    # 30. 김밥 한 줄 & 컵 우동
    {'set_id': 30, 'item_id': 31, 'amount': 1.0, 'unit': '줄'},
    {'set_id': 30, 'item_id': 58, 'amount': 1.0, 'unit': '컵'},

    # 31. 햄 치즈 샌드위치 & 아메리카노
    {'set_id': 31, 'item_id': 59, 'amount': 1.0, 'unit': '개'},
    {'set_id': 31, 'item_id': 60, 'amount': 1.0, 'unit': '컵'},

    # 32. 닭가슴살 샐러드 & 미니 컵밥
    {'set_id': 32, 'item_id': 61, 'amount': 1.0, 'unit': '팩'},
    {'set_id': 32, 'item_id': 62, 'amount': 1.0, 'unit': '컵'},

    # 33. 에그마요 샌드위치 & 바나나 우유
    {'set_id': 33, 'item_id': 63, 'amount': 1.0, 'unit': '개'},
    {'set_id': 33, 'item_id': 64, 'amount': 1.0, 'unit': '팩'},

    # 34. 미니 피자빵 & 오렌지 주스
    {'set_id': 34, 'item_id': 65, 'amount': 1.0, 'unit': '개'},
    {'set_id': 34, 'item_id': 66, 'amount': 1.0, 'unit': '병'},

    # 35. 전복죽 & 식혜
    {'set_id': 35, 'item_id': 67, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 35, 'item_id': 68, 'amount': 1.0, 'unit': '캔'},

    # 36. 프로틴 쉐이크 & 바나나
    {'set_id': 36, 'item_id': 69, 'amount': 1.0, 'unit': '팩'},
    {'set_id': 36, 'item_id': 70, 'amount': 1.0, 'unit': '개'},

    # 37. 견과류 믹스 & 저당 요거트
    {'set_id': 37, 'item_id': 71, 'amount': 1.0, 'unit': '팩'},
    {'set_id': 37, 'item_id': 72, 'amount': 1.0, 'unit': '개'},

    # 38. 저탄수 샐러드 & 아보카도 퓨레
    {'set_id': 38, 'item_id': 73, 'amount': 1.0, 'unit': '팩'},
    {'set_id': 38, 'item_id': 74, 'amount': 1.0, 'unit': '개'},

    # 39. 두유 & 고구마 샐러드 팩
    {'set_id': 39, 'item_id': 75, 'amount': 1.0, 'unit': '팩'},
    {'set_id': 39, 'item_id': 76, 'amount': 1.0, 'unit': '팩'},

    # 40. 미니 닭가슴살 포케 & 곤약밥
    {'set_id': 40, 'item_id': 77, 'amount': 1.0, 'unit': '개'},
    {'set_id': 40, 'item_id': 78, 'amount': 1.0, 'unit': '개'},

    # 41. 훈제란 & 스트링치즈 & 저지방 우유
    {'set_id': 41, 'item_id': 79, 'amount': 2.0, 'unit': '개'}, 
    {'set_id': 41, 'item_id': 5, 'amount': 1.0, 'unit': '개'},
    {'set_id': 41, 'item_id': 80, 'amount': 1.0, 'unit': '팩'},

    # 42. 단팥빵 & 흰 우유
    {'set_id': 42, 'item_id': 81, 'amount': 1.0, 'unit': '개'},
    {'set_id': 42, 'item_id': 82, 'amount': 1.0, 'unit': '팩'},

    # 43. 허니버터칩 & 콜라
    {'set_id': 43, 'item_id': 83, 'amount': 1.0, 'unit': '봉지'},
    {'set_id': 43, 'item_id': 84, 'amount': 1.0, 'unit': '캔'},

    # 44. 마카롱 2개 & 아메리카노
    {'set_id': 44, 'item_id': 85, 'amount': 2.0, 'unit': '개'},
    {'set_id': 44, 'item_id': 60, 'amount': 1.0, 'unit': '컵'},

    # 45. 초코 우유 & 초코 파이
    {'set_id': 45, 'item_id': 86, 'amount': 1.0, 'unit': '팩'},
    {'set_id': 45, 'item_id': 87, 'amount': 1.0, 'unit': '상자'}, 

    # 46. 에너지 드링크 & 젤리
    {'set_id': 46, 'item_id': 88, 'amount': 1.0, 'unit': '캔'},
    {'set_id': 46, 'item_id': 89, 'amount': 1.0, 'unit': '봉지'},

    # 47. 프레첼 & 탄산수
    {'set_id': 47, 'item_id': 90, 'amount': 1.0, 'unit': '봉지'},
    {'set_id': 47, 'item_id': 91, 'amount': 1.0, 'unit': '병'},

    # 48. 따뜻한 우유 & 꿀
    {'set_id': 48, 'item_id': 92, 'amount': 1.0, 'unit': '팩'},
    {'set_id': 48, 'item_id': 93, 'amount': 1.0, 'unit': '스틱'}, 

    # 49. 나쵸 & 소시지 & 탄산수
    {'set_id': 49, 'item_id': 94, 'amount': 1.0, 'unit': '봉지'},
    {'set_id': 49, 'item_id': 51, 'amount': 1.0, 'unit': '개'},
    {'set_id': 49, 'item_id': 91, 'amount': 1.0, 'unit': '병'},

    # 50. 과일 컵 & 탄산수
    {'set_id': 50, 'item_id': 95, 'amount': 1.0, 'unit': '컵'},
    {'set_id': 50, 'item_id': 91, 'amount': 1.0, 'unit': '병'},
]


def upgrade() -> None:
    """Upgrade schema: Insert set_composition data."""
    
    # op.bulk_insert를 사용하여 데이터 삽입
    op.bulk_insert(
        sa.table(
            'set_composition',
            sa.column('set_id', sa.Integer),
            sa.column('item_id', sa.Integer),
            sa.column('amount', sa.Float),
            sa.column('unit', sa.String),
        ),
        SET_COMPOSITION_DATA
    )


def downgrade() -> None:
    """Downgrade schema: Delete inserted set compositions."""
    
    # set_id 목록을 추출하여 해당 set에 속하는 모든 데이터를 삭제합니다.
    set_ids_to_delete = sorted(list(set(data['set_id'] for data in SET_COMPOSITION_DATA)))
    
    # SetComposition은 set_id와 item_id가 복합 PK이므로, set_id만으로 삭제합니다.
    op.execute(
        sa.text("DELETE FROM set_composition WHERE set_id IN :ids")
        .bindparams(ids=tuple(set_ids_to_delete))
    )

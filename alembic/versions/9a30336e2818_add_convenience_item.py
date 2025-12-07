from typing import Sequence, Union, List, Dict, Any

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '9a30336e2818'
down_revision: Union[str, Sequence[str], None] = 'b22a2e3368a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# =================================================================
# CONVENIENCE_ITEM_DATA: Recipe Sets에서 추출한 개별 상품 목록 및 추정 영양 성분
# =================================================================
# 개별 상품의 영양 성분은 상위 세트 총합을 기준으로 합리적으로 추정됨.
CONVENIENCE_ITEM_DATA: List[Dict[str, Any]] = [
    # 식사 항목 (set_id: 1 ~ 30)
    {'item_id': 1, 'name': '육개장 컵라면', 'calorie': 450.0, 'carbs': 75.0, 'protein': 10.0, 'fat': 10.0},
    {'item_id': 2, 'name': '참치마요 삼각김밥', 'calorie': 230.0, 'carbs': 30.0, 'protein': 15.0, 'fat': 8.0},
    {'item_id': 3, 'name': '신라면', 'calorie': 500.0, 'carbs': 75.0, 'protein': 12.0, 'fat': 15.0},
    {'item_id': 4, 'name': '공기밥', 'calorie': 150.0, 'carbs': 35.0, 'protein': 4.0, 'fat': 1.0}, # 1개 기준
    {'item_id': 5, 'name': '스트링치즈', 'calorie': 100.0, 'carbs': 0.0, 'protein': 12.0, 'fat': 10.0},
    {'item_id': 6, 'name': '튀김우동', 'calorie': 450.0, 'carbs': 75.0, 'protein': 10.0, 'fat': 12.0},
    {'item_id': 7, 'name': '김치볶음밥 삼각김밥', 'calorie': 270.0, 'carbs': 45.0, 'protein': 10.0, 'fat': 8.0},
    {'item_id': 8, 'name': '참깨라면', 'calorie': 400.0, 'carbs': 65.0, 'protein': 10.0, 'fat': 15.0},
    {'item_id': 9, 'name': '왕만두', 'calorie': 62.5, 'carbs': 10.0, 'protein': 5.0, 'fat': 5.0}, # 1개 기준 (총 4개, set_id 4)
    {'item_id': 10, 'name': '진라면', 'calorie': 500.0, 'carbs': 75.0, 'protein': 10.0, 'fat': 15.0},
    {'item_id': 11, 'name': '전주비빔 삼각김밥', 'calorie': 225.0, 'carbs': 37.5, 'protein': 10.0, 'fat': 5.0}, # 1개 기준 (총 2개, set_id 5)
    {'item_id': 12, 'name': '육개장 컵밥', 'calorie': 550.0, 'carbs': 90.0, 'protein': 20.0, 'fat': 15.0},
    {'item_id': 13, 'name': '핫바', 'calorie': 150.0, 'carbs': 15.0, 'protein': 7.5, 'fat': 7.5}, # 1종 기준 (총 2종, set_id 6)
    {'item_id': 14, 'name': '오모리 김치찌개 라면', 'calorie': 450.0, 'carbs': 70.0, 'protein': 15.0, 'fat': 10.0},
    {'item_id': 15, 'name': '계란', 'calorie': 85.0, 'carbs': 5.0, 'protein': 10.0, 'fat': 4.0}, # 1개 기준 (총 2개, set_id 7)
    {'item_id': 16, 'name': '미역국 컵밥', 'calorie': 350.0, 'carbs': 55.0, 'protein': 15.0, 'fat': 8.0},
    {'item_id': 17, 'name': '불고기 김밥', 'calorie': 430.0, 'carbs': 60.0, 'protein': 25.0, 'fat': 12.0},
    {'item_id': 18, 'name': '사발면', 'calorie': 350.0, 'carbs': 50.0, 'protein': 10.0, 'fat': 15.0},
    {'item_id': 19, 'name': '김치 볶음밥 도시락', 'calorie': 570.0, 'carbs': 80.0, 'protein': 25.0, 'fat': 15.0},
    {'item_id': 20, 'name': '봉지 라면', 'calorie': 500.0, 'carbs': 75.0, 'protein': 12.0, 'fat': 15.0},
    {'item_id': 21, 'name': '물만두', 'calorie': 350.0, 'carbs': 55.0, 'protein': 16.0, 'fat': 10.0},
    {'item_id': 22, 'name': '매콤 떡볶이', 'calorie': 500.0, 'carbs': 90.0, 'protein': 15.0, 'fat': 8.0},
    {'item_id': 23, 'name': '순대', 'calorie': 350.0, 'carbs': 50.0, 'protein': 10.0, 'fat': 17.0},
    {'item_id': 24, 'name': '비빔면', 'calorie': 380.0, 'carbs': 55.0, 'protein': 10.0, 'fat': 12.0}, # 1개 기준 (총 2개, set_id 12)
    {'item_id': 25, 'name': '삶은 계란', 'calorie': 60.0, 'carbs': 1.0, 'protein': 5.0, 'fat': 3.0}, # 1개 기준 (총 2개, set_id 12)
    {'item_id': 26, 'name': '크림 파스타', 'calorie': 600.0, 'carbs': 75.0, 'protein': 20.0, 'fat': 25.0},
    {'item_id': 27, 'name': '마늘빵', 'calorie': 150.0, 'carbs': 15.0, 'protein': 10.0, 'fat': 5.0},
    {'item_id': 28, 'name': '핫도그', 'calorie': 350.0, 'carbs': 50.0, 'protein': 10.0, 'fat': 15.0}, # 1개 기준 (총 2개, set_id 14)
    {'item_id': 29, 'name': '미니 콜라', 'calorie': 80.0, 'carbs': 10.0, 'protein': 0.0, 'fat': 0.0},
    {'item_id': 30, 'name': '불닭 컵라면', 'calorie': 550.0, 'carbs': 80.0, 'protein': 10.0, 'fat': 20.0},
    {'item_id': 31, 'name': '김밥 한 줄', 'calorie': 450.0, 'carbs': 70.0, 'protein': 20.0, 'fat': 15.0},
    {'item_id': 32, 'name': '고기반찬 도시락', 'calorie': 750.0, 'carbs': 80.0, 'protein': 35.0, 'fat': 30.0},
    {'item_id': 33, 'name': '미니 컵라면', 'calorie': 200.0, 'carbs': 40.0, 'protein': 10.0, 'fat': 10.0},
    {'item_id': 34, 'name': '비빔밥 컵', 'calorie': 550.0, 'carbs': 85.0, 'protein': 20.0, 'fat': 15.0},
    {'item_id': 35, 'name': '미니 된장국', 'calorie': 100.0, 'carbs': 15.0, 'protein': 5.0, 'fat': 3.0},
    {'item_id': 36, 'name': '제육볶음 덮밥', 'calorie': 680.0, 'carbs': 95.0, 'protein': 30.0, 'fat': 20.0},
    {'item_id': 37, 'name': '매실 음료', 'calorie': 100.0, 'carbs': 15.0, 'protein': 10.0, 'fat': 5.0},
    {'item_id': 38, 'name': '불고기 백반 도시락', 'calorie': 700.0, 'carbs': 100.0, 'protein': 30.0, 'fat': 20.0},
    {'item_id': 39, 'name': '보리차', 'calorie': 50.0, 'carbs': 10.0, 'protein': 5.0, 'fat': 2.0},
    {'item_id': 40, 'name': '돈까스 도시락', 'calorie': 800.0, 'carbs': 100.0, 'protein': 35.0, 'fat': 30.0},
    {'item_id': 41, 'name': '미니 젤리', 'calorie': 50.0, 'carbs': 15.0, 'protein': 5.0, 'fat': 0.0},
    {'item_id': 42, 'name': '김치찌개 도시락', 'calorie': 600.0, 'carbs': 85.0, 'protein': 25.0, 'fat': 15.0},
    {'item_id': 43, 'name': '흰 쌀밥', 'calorie': 80.0, 'carbs': 15.0, 'protein': 5.0, 'fat': 5.0},
    {'item_id': 44, 'name': '카레 컵밥', 'calorie': 450.0, 'carbs': 70.0, 'protein': 15.0, 'fat': 10.0},
    {'item_id': 45, 'name': '닭가슴살 큐브', 'calorie': 150.0, 'carbs': 15.0, 'protein': 15.0, 'fat': 8.0},
    {'item_id': 46, 'name': '미니 닭볶음탕', 'calorie': 450.0, 'carbs': 35.0, 'protein': 35.0, 'fat': 15.0},
    {'item_id': 47, 'name': '주먹밥', 'calorie': 230.0, 'carbs': 40.0, 'protein': 10.0, 'fat': 7.0},
    {'item_id': 48, 'name': '콩나물 해장국 컵', 'calorie': 350.0, 'carbs': 50.0, 'protein': 15.0, 'fat': 10.0},
    {'item_id': 49, 'name': '숙취 해소 음료', 'calorie': 100.0, 'carbs': 10.0, 'protein': 5.0, 'fat': 5.0},
    {'item_id': 50, 'name': '따뜻한 어묵탕', 'calorie': 200.0, 'carbs': 20.0, 'protein': 20.0, 'fat': 10.0},
    {'item_id': 51, 'name': '소시지바', 'calorie': 170.0, 'carbs': 10.0, 'protein': 10.0, 'fat': 6.0},
    {'item_id': 52, 'name': '치즈 불닭 컵밥', 'calorie': 650.0, 'carbs': 90.0, 'protein': 25.0, 'fat': 20.0},
    {'item_id': 53, 'name': '쿨피스', 'calorie': 230.0, 'carbs': 35.0, 'protein': 10.0, 'fat': 8.0},
    {'item_id': 54, 'name': '참치마요 주먹밥', 'calorie': 270.0, 'carbs': 40.0, 'protein': 15.0, 'fat': 10.0},
    {'item_id': 55, 'name': '컵 떡볶이', 'calorie': 480.0, 'carbs': 80.0, 'protein': 10.0, 'fat': 10.0},
    {'item_id': 56, 'name': '짜파게티', 'calorie': 600.0, 'carbs': 85.0, 'protein': 15.0, 'fat': 25.0},
    {'item_id': 57, 'name': '계란 후라이', 'calorie': 100.0, 'carbs': 5.0, 'protein': 5.0, 'fat': 2.5}, # 1개 기준 (총 2개, set_id 29)
    {'item_id': 58, 'name': '컵 우동', 'calorie': 300.0, 'carbs': 50.0, 'protein': 10.0, 'fat': 5.0},

    # 간단식사/간식 항목 (set_id: 31 ~ 50)
    {'item_id': 59, 'name': '햄 치즈 샌드위치', 'calorie': 380.0, 'carbs': 50.0, 'protein': 15.0, 'fat': 12.0},
    {'item_id': 60, 'name': '아메리카노', 'calorie': 30.0, 'carbs': 5.0, 'protein': 3.0, 'fat': 2.0},
    {'item_id': 61, 'name': '닭가슴살 샐러드', 'calorie': 300.0, 'carbs': 30.0, 'protein': 25.0, 'fat': 15.0},
    {'item_id': 62, 'name': '미니 컵밥', 'calorie': 250.0, 'carbs': 25.0, 'protein': 5.0, 'fat': 10.0},
    {'item_id': 63, 'name': '에그마요 샌드위치', 'calorie': 350.0, 'carbs': 55.0, 'protein': 10.0, 'fat': 10.0},
    {'item_id': 64, 'name': '바나나 우유', 'calorie': 100.0, 'carbs': 15.0, 'protein': 5.0, 'fat': 2.0},
    {'item_id': 65, 'name': '미니 피자빵', 'calorie': 380.0, 'carbs': 55.0, 'protein': 15.0, 'fat': 10.0},
    {'item_id': 66, 'name': '오렌지 주스', 'calorie': 100.0, 'carbs': 10.0, 'protein': 5.0, 'fat': 5.0},
    {'item_id': 67, 'name': '전복죽', 'calorie': 250.0, 'carbs': 40.0, 'protein': 10.0, 'fat': 5.0},
    {'item_id': 68, 'name': '식혜', 'calorie': 100.0, 'carbs': 10.0, 'protein': 5.0, 'fat': 5.0},
    {'item_id': 69, 'name': '프로틴 쉐이크', 'calorie': 300.0, 'carbs': 40.0, 'protein': 10.0, 'fat': 12.0},
    {'item_id': 70, 'name': '바나나', 'calorie': 130.0, 'carbs': 20.0, 'protein': 5.0, 'fat': 4.0},
    {'item_id': 71, 'name': '견과류 믹스', 'calorie': 150.0, 'carbs': 10.0, 'protein': 5.0, 'fat': 10.0},
    {'item_id': 72, 'name': '저당 요거트', 'calorie': 130.0, 'carbs': 20.0, 'protein': 10.0, 'fat': 0.0},
    {'item_id': 73, 'name': '저탄수 샐러드', 'calorie': 150.0, 'carbs': 5.0, 'protein': 10.0, 'fat': 15.0},
    {'item_id': 74, 'name': '아보카도 퓨레', 'calorie': 200.0, 'carbs': 10.0, 'protein': 5.0, 'fat': 10.0},
    {'item_id': 75, 'name': '두유', 'calorie': 150.0, 'carbs': 15.0, 'protein': 10.0, 'fat': 10.0},
    {'item_id': 76, 'name': '고구마 샐러드 팩', 'calorie': 200.0, 'carbs': 30.0, 'protein': 8.0, 'fat': 5.0},
    {'item_id': 77, 'name': '미니 닭가슴살 포케', 'calorie': 300.0, 'carbs': 30.0, 'protein': 25.0, 'fat': 10.0},
    {'item_id': 78, 'name': '곤약밥', 'calorie': 110.0, 'carbs': 15.0, 'protein': 5.0, 'fat': 3.0},
    {'item_id': 79, 'name': '훈제란', 'calorie': 100.0, 'carbs': 5.0, 'protein': 10.0, 'fat': 5.0},
    {'item_id': 80, 'name': '저지방 우유', 'calorie': 50.0, 'carbs': 5.0, 'protein': 5.0, 'fat': 5.0},
    {'item_id': 81, 'name': '단팥빵', 'calorie': 450.0, 'carbs': 75.0, 'protein': 10.0, 'fat': 15.0},
    {'item_id': 82, 'name': '흰 우유', 'calorie': 130.0, 'carbs': 15.0, 'protein': 5.0, 'fat': 3.0},
    {'item_id': 83, 'name': '허니버터칩', 'calorie': 500.0, 'carbs': 55.0, 'protein': 5.0, 'fat': 30.0},
    {'item_id': 84, 'name': '콜라', 'calorie': 150.0, 'carbs': 20.0, 'protein': 0.0, 'fat': 5.0},
    {'item_id': 85, 'name': '마카롱', 'calorie': 210.0, 'carbs': 30.0, 'protein': 4.0, 'fat': 9.0}, # 1개 기준 (총 2개, set_id 44)
    {'item_id': 86, 'name': '초코 우유', 'calorie': 150.0, 'carbs': 20.0, 'protein': 5.0, 'fat': 5.0},
    {'item_id': 87, 'name': '초코 파이', 'calorie': 450.0, 'carbs': 70.0, 'protein': 10.0, 'fat': 15.0},
    {'item_id': 88, 'name': '에너지 드링크', 'calorie': 200.0, 'carbs': 50.0, 'protein': 2.0, 'fat': 0.0},
    {'item_id': 89, 'name': '젤리', 'calorie': 180.0, 'carbs': 35.0, 'protein': 0.0, 'fat': 4.0},
    {'item_id': 90, 'name': '프레첼', 'calorie': 300.0, 'carbs': 40.0, 'protein': 8.0, 'fat': 10.0},
    {'item_id': 91, 'name': '탄산수', 'calorie': 100.0, 'carbs': 20.0, 'protein': 0.0, 'fat': 5.0},
    {'item_id': 92, 'name': '따뜻한 우유', 'calorie': 150.0, 'carbs': 15.0, 'protein': 8.0, 'fat': 8.0},
    {'item_id': 93, 'name': '꿀', 'calorie': 100.0, 'carbs': 20.0, 'protein': 2.0, 'fat': 0.0},
    {'item_id': 94, 'name': '나쵸', 'calorie': 300.0, 'carbs': 30.0, 'protein': 10.0, 'fat': 15.0},
    {'item_id': 95, 'name': '과일 컵', 'calorie': 50.0, 'carbs': 15.0, 'protein': 2.0, 'fat': 1.0},
]


def upgrade() -> None:
    """Upgrade schema: Insert convenience_items data."""
    
    # op.bulk_insert를 사용하여 데이터 삽입
    op.bulk_insert(
        sa.table(
            'convenience_items',
            sa.column('item_id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('calorie', sa.Float),
            sa.column('carbs', sa.Float),
            sa.column('protein', sa.Float),
            sa.column('fat', sa.Float),
        ),
        CONVENIENCE_ITEM_DATA
    )
    
    # item_id 시퀀스 조정 (DB 종류에 따라 필요)
    max_id = max(item['item_id'] for item in CONVENIENCE_ITEM_DATA)
    # PostgreSQL 등을 위한 예시:
    # op.execute(text(f"SELECT setval('convenience_items_item_id_seq', {max_id}, true)"))


def downgrade() -> None:
    """Downgrade schema: Delete inserted convenience items."""
    
    # 삽입했던 item_id 목록을 추출
    item_ids_to_delete = [data['item_id'] for data in CONVENIENCE_ITEM_DATA]
    
    # DELETE 쿼리를 사용하여 해당 ID의 데이터 삭제
    op.execute(
        sa.text("DELETE FROM convenience_items WHERE item_id IN :ids")
        .bindparams(ids=tuple(item_ids_to_delete))
    )
    
    # 데이터베이스 시퀀스 조정 (DB 종류에 따라 필요)
    # op.execute(text("SELECT setval('convenience_items_item_id_seq', (SELECT MAX(item_id) FROM convenience_items), false)"))

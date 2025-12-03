"""Insert 30 initial recipes (Breakfast, Lunch, Dinner) - Image URLs removed

Revision ID: 31a7c8d9e0f1
Revises: 2f2c0f4c07f8
Create Date: 2025-11-20 18:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column 
from sqlalchemy import String, Integer, Text


# revision identifiers, used by Alembic.
revision: str = '31a7c8d9e0f1'
down_revision: Union[str, Sequence[str], None] = '2f2c0f4c07f8' # 이전 알레르기 마이그레이션 ID
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# image_url 필드를 제거한 30개 레시피 데이터 정의
INITIAL_RECIPES = [
    # ☀️ A. 아침 식단 (Breakfast, ID 1-10)
    {
        "recipe_id": 1, 
        "name": "통밀 팬케이크 & 베리 세트", 
        "description": "바쁜 아침, 통밀 팬케이크와 신선한 베리로 탄수화물과 항산화 성분을 빠르게 충전합니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://wholeandheavenlyoven.com/wp-content/uploads/2017/01/Healthy-Mixed-Berry-Multi-Grain-Pancakes2.jpg"
    },
    {
        "recipe_id": 2, 
        "name": "계란 스크램블 & 아보카도 토스트", 
        "description": "양질의 단백질과 건강한 지방을 제공하는 대표적인 아침 식단. 포만감이 오래 지속됩니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://revcook.com/cdn/shop/articles/loaded_avo_toast_recipe_8f49eca2-16c5-4f3c-b307-34db23711af1.png?v=1755821498&width=2048"
    },
    {
        "recipe_id": 3, 
        "name": "그릭 요거트 & 그래놀라 볼", 
        "description": "유산균이 풍부한 그릭 요거트에 견과류와 그래놀라를 곁들여 장 건강을 돕습니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://mycasualpantry.com/wp-content/uploads/2022/07/Greek-Yogurt-with-Granola-and-Fruit-bowl-1200-%C3%97-1200-px-500x375.jpg"
    },
    {
        "recipe_id": 4, 
        "name": "시금치 & 치즈 오믈렛", 
        "description": "채소를 포함한 단백질 중심 식단. 다채로운 영양소를 한 번에 섭취할 수 있습니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://www.kosterina.com/cdn/shop/articles/omlette.png?crop=center&format=pjpg&height=1000&v=1509746565&width=1500"
    },
    {
        "recipe_id": 5, 
        "name": "오버나이트 오트밀 (견과류)", 
        "description": "전날 미리 준비하여 아침에 바로 먹을 수 있는 간편식. 식이섬유가 풍부합니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://www.simplywhisked.com/wp-content/uploads/2021/12/Overnight-Oatmeal-1200-3-500x500.jpg"
    },
    {
        "recipe_id": 6, 
        "name": "바나나 & 아몬드 스무디", 
        "description": "소화가 잘되고 빠르게 에너지를 공급하는 액상 식단입니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0DMGyeHqEmARTuB162TtveuUrLwAaZ9aysw&s"
    },
    {
        "recipe_id": 7, 
        "name": "두부 샐러드 & 현미 주먹밥", 
        "description": "가볍지만 든든한 동양식 아침. 식물성 단백질과 복합 탄수화물을 제공합니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://www.chompslurrpburp.com/wp-content/uploads/2022/06/peanut-tofu-and-mango-800x500.jpg"
    },
    {
        "recipe_id": 8, 
        "name": "닭가슴살 샌드위치 (통밀빵)", 
        "description": "통밀빵을 사용하여 혈당 관리에 용이하며, 닭가슴살로 단백질을 보충합니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://www.brownberry.com/sites/default/files/recipe/ABO_15600_JuneXX_2017_GrilledChickenPestoSandwich_1400x650.jpg"
    },
    {
        "recipe_id": 9, 
        "name": "버섯 & 채소 볶음밥 (소량)", 
        "description": "밥을 선호하는 분들을 위한 저염 볶음밥. 채소 위주로 구성되어 부담이 적습니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://www.littlesugarsnaps.com/wp-content/uploads/2021/04/Mushroom-Fried-Rice-0789C.jpg"
    },
    {
        "recipe_id": 10, 
        "name": "훈제 연어 & 크림치즈 베이글", 
        "description": "오메가-3 지방산이 풍부한 연어를 활용한 특별한 아침 세트입니다.", 
        "meal_type": "Breakfast",
        "image_url": "https://www.warburtons.co.uk/wp-content/uploads/2020/12/Bagel-Recipe-Card-1200x1000.png"
    },

    # 🥗 B. 점심 식단 (Lunch, ID 11-20)
    {
        "recipe_id": 11, 
        "name": "닭가슴살 & 퀴노아 샐러드", 
        "description": "슈퍼푸드 퀴노아를 주재료로 사용하여 높은 포만감과 영양 균형을 잡은 식단입니다.", 
        "meal_type": "Lunch",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNohZp3QPfpQmqVnri356NbxDkX46T-kulQA&s"
    },
    {
        "recipe_id": 12, 
        "name": "포케 볼 (연어/참치)", 
        "description": "다양한 채소와 생선 단백질을 간장 기반 소스로 버무린 하와이안 퓨전 건강식입니다.", 
        "meal_type": "Lunch",
        "image_url": "https://thebigmansworld.com/wp-content/uploads/2024/06/salmon-poke-bowl-recipe.jpg"
    },
    {
        "recipe_id": 13, 
        "name": "멕시칸 비건 타코 세트", 
        "description": "렌틸콩 또는 검은콩을 활용하여 식물성 단백질을 섭취하는 활력 넘치는 점심입니다.", 
        "meal_type": "Lunch",
        "image_url": "https://www.twopeasandtheirpod.com/wp-content/uploads/2021/06/Veggie-Tacos4577-500x500.jpg"
    },
    {
        "recipe_id": 14, 
        "name": "저염 소고기 찹스테이크 & 구운 채소", 
        "description": "단백질과 철분 보충에 좋으며, 구운 채소가 소화를 돕습니다.", 
        "meal_type": "Lunch",
        "image_url": "https://thewholecook.com/wp-content/uploads/2023/01/Steak-with-Roasted-Veggies-1-3-500x500.jpg"
    },
    {
        "recipe_id": 15, 
        "name": "에그인헬 (Shakshuka)", 
        "description": "토마토 베이스 소스에 계란을 넣어 만든 중동식 요리. 빵과 곁들여 먹습니다.", 
        "meal_type": "Lunch",
        "image_url": "https://static.wtable.co.kr/image/production/service/recipe/682/a22619e9-6bdb-46e7-8ebe-1789ddc87070.jpg"
    },
    {
        "recipe_id": 16, 
        "name": "병아리콩 커리 & 난 (통밀)", 
        "description": "섬유질이 풍부한 병아리콩을 주재료로 한 인도식 건강 커리입니다.", 
        "meal_type": "Lunch",
        "image_url": "https://media-cdn.tripadvisor.com/media/photo-m/1280/1b/85/fa/b3/chicken-curry-with-mint.jpg"
    },
    {
        "recipe_id": 17, 
        "name": "렌틸콩 수프 & 호밀빵", 
        "description": "가볍지만 영양가가 풍부하여 오후 활동에 필요한 에너지를 제공합니다.", 
        "meal_type": "Lunch",
        "image_url": "https://vegan.org/wp-content/uploads/2024/03/Lentil-Soup--1024x768.jpg"
    },
    {
        "recipe_id": 18, 
        "name": "돼지고기 앞다리살 간장 불고기 세트", 
        "description": "저지방 부위인 앞다리살을 사용하여 칼로리를 낮춘 한국식 건강 점심입니다.", 
        "meal_type": "Lunch",
        "image_url": "https://www.chopsticksandflour.com/wp-content/uploads/2019/05/soy-sauce-pork-bulgogi-horizontal-600x400.jpg"
    },
    {
        "recipe_id": 19, 
        "name": "현미밥 & 버섯 된장찌개 세트", 
        "description": "전통적인 한식 세트로, 발효 식품인 된장을 통해 장 건강을 챙깁니다.", 
        "meal_type": "Lunch",
        "image_url": "https://mykoreankitchen.com/wp-content/uploads/2020/02/1.-Doenjang-Jjigae.jpg"
    },
    {
        "recipe_id": 20, 
        "name": "참치마요 김밥 (저염) & 우동(소량)", 
        "description": "간편하게 즐기는 저염 김밥과 소량의 국물 요리로 구성된 세트입니다.", 
        "meal_type": "Lunch",
        "image_url": "https://www.koreanbapsang.com/wp-content/uploads/2015/05/DSC_08431-e1431961213188.jpg"
    },

    # 🌙 C. 저녁 식단 (Dinner, ID 21-30)
    {
        "recipe_id": 21, 
        "name": "연어 스테이크 & 아스파라거스", 
        "description": "오메가-3와 단백질을 중심으로 구성하여 피로 회복과 수면의 질 향상에 도움을 줍니다.", 
        "meal_type": "Dinner",
        "image_url": "https://natashaskitchen.com/wp-content/uploads/2017/06/Salmon-and-Asparagus-3.jpg"
    },
    {
        "recipe_id": 22, 
        "name": "양고기 숄더랙 구이 & 샐러드", 
        "description": "양질의 단백질과 미네랄을 섭취할 수 있는 저녁 만찬입니다.", 
        "meal_type": "Dinner",
        "image_url": "https://www.theoriginaldish.com/wp-content/uploads/2021/03/Spiced-Rack-of-Lamb-9-683x1024.jpg"
    },
    {
        "recipe_id": 23, 
        "name": "해산물 봉골레 파스타 (통밀면)", 
        "description": "통밀 파스타를 사용하여 GI 지수를 낮추고, 신선한 해산물로 풍미를 더했습니다.", 
        "meal_type": "Dinner",
        "image_url": "https://www.sipandfeast.com/wp-content/uploads/2024/07/linguine-alle-vongole-recipe-snippet-2.jpg"
    },
    {
        "recipe_id": 24, 
        "name": "두부 & 김치 볶음 (저염)", 
        "description": "늦은 시간 부담 없이 즐길 수 있는 식물성 단백질 중심의 야식/저녁입니다.", 
        "meal_type": "Dinner",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeVxjqxsiU3sjgEKZ2KTZHL276P2EbwXsP_w&s"
    },
    {
        "recipe_id": 25, 
        "name": "토마토 & 모짜렐라 카프레제 세트", 
        "description": "신선하고 가벼운 이탈리아식 전채 세트로, 저녁 식사 대용으로 좋습니다.", 
        "meal_type": "Dinner",
        "image_url": "https://cdn.apartmenttherapy.info/image/upload/f_jpg,q_auto:eco,c_fill,g_auto,w_1500,ar_1:1/k%2Farchive%2F3b432b41ce04c96a08d77befa42b9881a587a436"
    },
    {
        "recipe_id": 26, 
        "name": "매콤 닭봉 구이 & 콜리플라워 라이스", 
        "description": "밥 대신 콜리플라워 라이스를 사용하여 탄수화물을 극도로 낮춘 저탄고단 식단입니다.", 
        "meal_type": "Dinner",
        "image_url": "https://www.primaverakitchen.com/wp-content/uploads/2018/12/Spicy-Chicken-with-Cauliflower-Rice-Primavera-Kitchen-5.jpg"
    },
    {
        "recipe_id": 27, 
        "name": "참치 스테이크 & 구운 채소", 
        "description": "고단백 저지방 참치를 활용하여 다음 날까지 든든한 포만감을 유지합니다.", 
        "meal_type": "Dinner",
        "image_url": "https://www.sainsburysmagazine.co.uk/uploads/media/2400x1800/09/5059-Warm-Tuna-Nicoise-Ratatou-Inside-1120.jpg?v=1-0"
    },
    {
        "recipe_id": 28, 
        "name": "버섯 리조또 (보리)", 
        "description": "쌀 대신 보리를 사용하여 식이섬유를 높인 건강한 이탈리아식 리조또입니다.", 
        "meal_type": "Dinner",
        "image_url": "https://familystylefood.com/wp-content/uploads/2022/02/Barley-Risotto-Serving.jpg"
    },
    {
        "recipe_id": 29, 
        "name": "해물 순두부찌개 (맑은 국물)", 
        "description": "칼칼하면서도 속을 편안하게 해주는 맑은 순두부찌개 세트입니다.", 
        "meal_type": "Dinner",
        "image_url": "https://www.koreanbapsang.com/wp-content/uploads/2012/02/DSC_0009-e1542090040119.jpg"
    },
    {
        "recipe_id": 30, 
        "name": "채소 가득 월남쌈 & 땅콩 소스", 
        "description": "다양한 채소를 한 번에 섭취할 수 있으며, 가벼운 포만감을 제공합니다.", 
        "meal_type": "Dinner",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdG1Guje-CwCBmpYe-TXdUq-BXiYtaIWBlCA&s"
    },
]

# 'recipes' 테이블 구조 정의 (image_url 컬럼 제거)
recipe_table = table(
    'recipes', 
    column('recipe_id', sa.Integer),
    column('name', sa.String(255)),
    column('description', sa.Text),
    column('meal_type', sa.String(50)),
    column('image_url', sa.String(500)),
    
)

def upgrade() -> None:
    """데이터 마이그레이션 실행: 30개의 초기 레시피 데이터를 'recipes' 테이블에 삽입합니다."""
    op.bulk_insert(
        recipe_table,
        INITIAL_RECIPES
    )
    print("30개 레시피 데이터 삽입 완료 (image_url 제외).")


def downgrade() -> None:
    """데이터 마이그레이션 되돌리기: 삽입된 30개 레시피 데이터를 삭제합니다."""
    # 삽입했던 recipe_id (1부터 30)의 레코드를 모두 삭제
    recipe_ids_to_delete = tuple(r['recipe_id'] for r in INITIAL_RECIPES)
    
    op.execute(
        sa.text("DELETE FROM recipes WHERE recipe_id IN :ids").bindparams(ids=recipe_ids_to_delete)
    )
    print("30개 레시피 데이터 삭제 완료 (롤백).")

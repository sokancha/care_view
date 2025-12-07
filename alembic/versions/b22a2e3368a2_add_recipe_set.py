from typing import Sequence, Union, List, Dict, Any

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = 'b22a2e3368a2'
down_revision: Union[str, Sequence[str], None] = '411dcd90b704'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# =================================================================
# 50가지 편의점 베스트 조합 데이터 (일반 분류: 식사, 간단식사, 간식)
# =================================================================
RECIPE_SET_DATA: List[Dict[str, Any]] = [
    # 1-10: [식사] (Heavy Combos)
    {
        'set_id': 1, 'name': '육개장 컵라면 & 참치마요 삼각김밥', 'set_type': '식사', 
        'image_url': 'https://mblogthumb-phinf.pstatic.net/20160420_114/lavender6566_1461154891043ibSu8_JPEG/2016-04-20_09.17.04_1.jpg?type=w800', 'total_calorie': 680.0, 'total_carbs': 105.0, 'total_protein': 25.0, 'total_fat': 18.0
    },
    {
        'set_id': 2, 'name': '신라면 & 공기밥 & 스트링치즈', 'set_type': '식사', 
        'image_url': 'https://www.costco.co.kr/medias/sys_master/images/h77/h5f/139386647674910.jpg', 'total_calorie': 750.0, 'total_carbs': 110.0, 'total_protein': 28.0, 'total_fat': 25.0
    },
    {
        'set_id': 3, 'name': '튀김우동 & 김치볶음밥 삼각김밥', 'set_type': '식사', 
        'image_url': 'https://sitem.ssgcdn.com/15/10/66/item/1000353661015_i1_332.jpg', 'total_calorie': 720.0, 'total_carbs': 120.0, 'total_protein': 20.0, 'total_fat': 20.0
    },
    {
        'set_id': 4, 'name': '참깨라면 & 왕만두 4개', 'set_type': '식사', 
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoQChRPEIfGb90_7ORbEknUhjq3MoO3aHQ9A&s', 'total_calorie': 650.0, 'total_carbs': 95.0, 'total_protein': 25.0, 'total_fat': 20.0
    },
    {
        'set_id': 5, 'name': '진라면(순한맛) & 전주비빔 삼각김밥 2개', 'set_type': '식사', 
        'image_url': 'https://mblogthumb-phinf.pstatic.net/20150909_226/wogur1157_1441808215746aY1Q1_JPEG/20150817-IMG_9267.jpg?type=w420', 'total_calorie': 950.0, 'total_carbs': 150.0, 'total_protein': 30.0, 'total_fat': 25.0
    },
    {
        'set_id': 6, 'name': '육개장 컵밥 & 핫바 2종', 'set_type': '식사', 
        'image_url': 'https://cdn.011st.com/11dims/resize/1000x1000/quality/75/11src/product/4546854477/B.jpg?513000000', 'total_calorie': 850.0, 'total_carbs': 120.0, 'total_protein': 35.0, 'total_fat': 30.0
    },
    {
        'set_id': 7, 'name': '오모리 김치찌개 라면 & 계란 2개', 'set_type': '식사', 
        'image_url': 'https://img.etoday.co.kr/pto_db/2022/01/20220117133100_1709137_594_623.jpg', 'total_calorie': 620.0, 'total_carbs': 80.0, 'total_protein': 35.0, 'total_fat': 18.0
    },
    {
        'set_id': 8, 'name': '미역국 컵밥 & 불고기 김밥', 'set_type': '식사', 
        'image_url': 'https://cdn.otokimall.com/data/product/etc/20251103/1762148713452haS0g.skkjwz69t2cw.jpg', 'total_calorie': 780.0, 'total_carbs': 115.0, 'total_protein': 40.0, 'total_fat': 20.0
    },
    {
        'set_id': 9, 'name': '사발면 & 김치 볶음밥 도시락', 'set_type': '식사', 
        'image_url': 'https://blog.kakaocdn.net/dna/wS2g6/btsonwbrvuA/AAAAAAAAAAAAAAAAAAAAAFDITAPiYJMPCSYqHNGTF8h4ynksUQe8kUCH5Jw0jo5t/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1767193199&allow_ip=&allow_referer=&signature=u0yIHagTwqKoWJREsdeQFXvgHRY%3D', 'total_calorie': 920.0, 'total_carbs': 130.0, 'total_protein': 35.0, 'total_fat': 30.0
    },
    {
        'set_id': 10, 'name': '봉지 라면 & 물만두', 'set_type': '식사', 
        'image_url': 'https://fastmall.co.kr/web/product/medium/202511/f9771601cdbbfb557f9b92cc3c6236c7.jpg', 'total_calorie': 850.0, 'total_carbs': 130.0, 'total_protein': 28.0, 'total_fat': 25.0
    },
    
    # 11-20: [식사] (Main Meals & Instant Meals)
    {
        'set_id': 11, 'name': '매콤 떡볶이 & 순대', 'set_type': '식사', 
        'image_url': 'https://sitem.ssgcdn.com/20/74/94/item/1000641947420_i1_750.jpg', 'total_calorie': 850.0, 'total_carbs': 140.0, 'total_protein': 25.0, 'total_fat': 25.0
    },
    {
        'set_id': 12, 'name': '비빔면 2개 & 삶은 계란 2개', 'set_type': '식사', 
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcq-qDF_C0OwRpUfDQEcmGBtgv4OaHd4p-wg&s', 'total_calorie': 880.0, 'total_carbs': 125.0, 'total_protein': 35.0, 'total_fat': 28.0
    },
    {
        'set_id': 13, 'name': '크림 파스타 & 마늘빵 1개', 'set_type': '식사', 
        'image_url': 'https://img.danawa.com/prod_img/500000/371/879/img/15879371_1.jpg?_v=20230711125420', 'total_calorie': 750.0, 'total_carbs': 90.0, 'total_protein': 30.0, 'total_fat': 30.0
    },
    {
        'set_id': 14, 'name': '핫도그 2개 & 미니 콜라', 'set_type': '식사', 
        'image_url': 'https://image2.lotteimall.com/goods/35/49/70/12704935_1.jpg', 'total_calorie': 780.0, 'total_carbs': 110.0, 'total_protein': 20.0, 'total_fat': 30.0
    },
    {
        'set_id': 15, 'name': '불닭 컵라면 & 김밥 한 줄', 'set_type': '식사', 
        'image_url': 'https://asset.m-gs.kr/prod/1038210326/1/550', 'total_calorie': 1000.0, 'total_carbs': 150.0, 'total_protein': 30.0, 'total_fat': 35.0
    },
    {
        'set_id': 16, 'name': '고기반찬 도시락 & 미니 컵라면', 'set_type': '식사', 
        'image_url': 'https://dimg.donga.com/wps/NEWS/IMAGE/2016/02/11/76393975.2.jpg', 'total_calorie': 950.0, 'total_carbs': 120.0, 'total_protein': 45.0, 'total_fat': 40.0
    },
    {
        'set_id': 17, 'name': '비빔밥 컵 & 미니 된장국', 'set_type': '식사', 
        'image_url': 'https://thumbnews.nateimg.co.kr/view610///news.nateimg.co.kr/orgImg/mk/2023/03/16/20230317_01150118000002_L00.jpg', 'total_calorie': 650.0, 'total_carbs': 100.0, 'total_protein': 25.0, 'total_fat': 18.0
    },
    {
        'set_id': 18, 'name': '제육볶음 덮밥 & 매실 음료', 'set_type': '식사', 
        'image_url': 'https://msave.emart24.co.kr/cmsbo/upload/nHq/plu_image/500x500/8809030112736.JPG', 'total_calorie': 780.0, 'total_carbs': 110.0, 'total_protein': 40.0, 'total_fat': 25.0
    },
    {
        'set_id': 19, 'name': '불고기 백반 도시락 & 보리차', 'set_type': '식사', 
        'image_url': 'https://digitalchosun.dizzo.com/site/data/img_dir/2018/05/11/2018051111479_2.jpg', 'total_calorie': 750.0, 'total_carbs': 110.0, 'total_protein': 35.0, 'total_fat': 22.0
    },
    {
        'set_id': 20, 'name': '돈까스 도시락 & 미니 젤리', 'set_type': '식사', 
        'image_url': 'https://img3.yna.co.kr/etc/inner/KR/2015/06/14/AKR20150614013600030_01_i_P2.jpg', 'total_calorie': 850.0, 'total_carbs': 115.0, 'total_protein': 40.0, 'total_fat': 30.0
    },
    
    # 21-30: [식사] (Continued Main Meals)
    {
        'set_id': 21, 'name': '김치찌개 도시락 & 흰 쌀밥', 'set_type': '식사', 
        'image_url': 'https://cphoto.asiae.co.kr/listimglink/1/2016012108320568295_1.jpg', 'total_calorie': 680.0, 'total_carbs': 100.0, 'total_protein': 30.0, 'total_fat': 20.0
    },
    {
        'set_id': 22, 'name': '카레 컵밥 & 닭가슴살 큐브', 'set_type': '식사', 
        'image_url': 'https://lottemartzetta.com/images-v3/932dcbc7-fca8-4d43-bcde-f73d1ce3cc7d/06e7c904-ab89-4711-94b8-40ec1dca87dc/500x500.jpg', 'total_calorie': 600.0, 'total_carbs': 85.0, 'total_protein': 30.0, 'total_fat': 18.0
    },
    {
       'set_id': 23, 'name': '미니 닭볶음탕 & 주먹밥 1개', 'set_type': '식사', 
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyO9GzHsd1pRjin0aGZgR2O9BppNUA0UbX4A&s', 'total_calorie': 680.0, 'total_carbs': 75.0, 'total_protein': 45.0, 'total_fat': 22.0
    },
    {
        'set_id': 24, 'name': '콩나물 해장국 컵 & 숙취 해소 음료', 'set_type': '식사', 
        'image_url': 'https://cdn.otokimall.com/data/product/detail/20221125/1736387879036Hgqkd.1h821sdka0oj4.jpg', 'total_calorie': 450.0, 'total_carbs': 60.0, 'total_protein': 20.0, 'total_fat': 15.0
    },
    {
        'set_id': 25, 'name': '따뜻한 어묵탕 & 소시지바', 'set_type': '식사', 
        'image_url': 'https://tqklhszfkvzk6518638.edge.naverncp.com/product/8809265025221.jpg', 'total_calorie': 370.0, 'total_carbs': 30.0, 'total_protein': 30.0, 'total_fat': 16.0
    },
    {
        'set_id': 26, 'name': '치즈 불닭 컵밥 & 쿨피스', 'set_type': '식사', 
        'image_url': 'https://img.danawa.com/prod_img/500000/698/990/img/3990698_1.jpg?_v=20251105064037', 'total_calorie': 880.0, 'total_carbs': 125.0, 'total_protein': 35.0, 'total_fat': 28.0
    },
    {
        'set_id': 27, 'name': '불고기 김밥 & 봉지 라면', 'set_type': '식사', 
        'image_url': 'https://pbs.twimg.com/media/EreLeILVcAAhCzP.png', 'total_calorie': 850.0, 'total_carbs': 130.0, 'total_protein': 30.0, 'total_fat': 20.0
    },
    {
        'set_id': 28, 'name': '참치마요 주먹밥 & 컵 떡볶이', 'set_type': '식사', 
        'image_url': 'https://cdn.otokimall.com/data/product/etc/20241206/1733445033163UcG4j.1iave5skibbs1.jpg', 'total_calorie': 750.0, 'total_carbs': 120.0, 'total_protein': 25.0, 'total_fat': 20.0
    },
    {
        'set_id': 29, 'name': '짜파게티 & 계란 후라이 2개', 'set_type': '식사', 
        'image_url': 'https://i.namu.wiki/i/6ZOW9BT-Pm1bDuhYuFX005WjHvPZoFiTEqUXSLFRDnNP8-X0pRqCjy3ZEm-t2ItkD082fhtGWqQd7--CAFQDhw.webp', 'total_calorie': 800.0, 'total_carbs': 110.0, 'total_protein': 20.0, 'total_fat': 30.0
    },
    {
        'set_id': 30, 'name': '김밥 한 줄 & 컵 우동', 'set_type': '식사', 
        'image_url': 'https://img.danawa.com/prod_img/500000/543/878/img/18878543_1.jpg?shrink=360:360&_v=20230131131211', 'total_calorie': 720.0, 'total_carbs': 120.0, 'total_protein': 20.0, 'total_fat': 20.0
    },

    # 31-40: [간단식사] (Simple Meals & Quick Options)
    {
        'set_id': 31, 'name': '햄 치즈 샌드위치 & 아메리카노', 'set_type': '간단식사', 
        'image_url': 'https://allbakery.co.kr/data/item/62-1001/64yA66eM7IOM65Oc7ZaE7LmY7KaI.jpg', 'total_calorie': 410.0, 'total_carbs': 55.0, 'total_protein': 18.0, 'total_fat': 14.0
    },
    {
        'set_id': 32, 'name': '닭가슴살 샐러드 & 미니 컵밥', 'set_type': '간단식사', 
        'image_url': 'https://msave.emart24.co.kr/cmsbo/upload/nHq/plu_image/500x500/8801068928730.JPG', 'total_calorie': 550.0, 'total_carbs': 55.0, 'total_protein': 30.0, 'total_fat': 25.0
    },
    {
        'set_id': 33, 'name': '에그마요 샌드위치 & 바나나 우유', 'set_type': '간단식사', 
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRckx27l9EmcjXzOZcyQt-Cos4hzVQpYGs-bQ&s', 'total_calorie': 450.0, 'total_carbs': 70.0, 'total_protein': 15.0, 'total_fat': 12.0
    },
    {
        'set_id': 34, 'name': '미니 피자빵 & 오렌지 주스', 'set_type': '간단식사', 
        'image_url': 'https://thumbnail.coupangcdn.com/thumbnails/remote/492x492ex/image/vendor_inventory/6266/5b306ad007af77a3939c96a1ce6702412a29dba0abd91bcbfd3ef517f785.jpg', 'total_calorie': 480.0, 'total_carbs': 65.0, 'total_protein': 20.0, 'total_fat': 15.0
    },
    {
        'set_id': 35, 'name': '전복죽 & 식혜', 'set_type': '간단식사', 
        'image_url': 'https://img.danawa.com/prod_img/500000/236/362/img/13362236_1.jpg?shrink=360:360&_v=20210215110814', 'total_calorie': 350.0, 'total_carbs': 50.0, 'total_protein': 15.0, 'total_fat': 10.0
    },
    {
        'set_id': 36, 'name': '프로틴 쉐이크 & 바나나', 'set_type': '간단식사', 
        'image_url': 'https://mblogthumb-phinf.pstatic.net/MjAyMzA1MTRfNDgg/MDAxNjg0MDAxOTQ1MDgy.rGGyvjt5o-1REN8eEj2jYuUDa4asI3YlRHfjkVvmry0g.uqRYsCmRE7zXrcacGQLUtUCHfqUrLejl4V1f-VJn3N4g.JPEG.sun2hwa/SE-3BBFC81B-A3BA-4714-BF79-62438A0DEEC3.jpg?type=w800', 'total_calorie': 430.0, 'total_carbs': 60.0, 'total_protein': 15.0, 'total_fat': 16.0
    },
    {
        'set_id': 37, 'name': '견과류 믹스 & 저당 요거트', 'set_type': '간단식사', 
        'image_url': 'https://gdimg.gmarket.co.kr/1782664978/still/400?ver=1738738679', 'total_calorie': 280.0, 'total_carbs': 30.0, 'total_protein': 15.0, 'total_fat': 10.0
    },
    {
        'set_id': 38, 'name': '저탄수 샐러드 & 아보카도 퓨레', 'set_type': '간단식사', 
        'image_url': 'https://img.daily.co.kr/@files/www.daily.co.kr/content_watermark/food/2020/20200902/31cc221b9c30d927755ba7dc974f3d7a.jpg', 'total_calorie': 350.0, 'total_carbs': 15.0, 'total_protein': 15.0, 'total_fat': 25.0
    },
    {
        'set_id': 39, 'name': '두유 & 고구마 샐러드 팩', 'set_type': '간단식사', 
        'image_url': 'https://img.danawa.com/prod_img/500000/006/600/img/9600006_1.jpg?_v=20190930153638', 'total_calorie': 350.0, 'total_carbs': 45.0, 'total_protein': 18.0, 'total_fat': 10.0
    },
    {
        'set_id': 40, 'name': '미니 닭가슴살 포케 & 곤약밥', 'set_type': '간단식사', 
        'image_url': 'https://m.ftscrt.com/food/35dd841c-fe41-4362-aef8-f0dd633975dc_lg_sq.jpg', 'total_calorie': 410.0, 'total_carbs': 45.0, 'total_protein': 30.0, 'total_fat': 13.0
    },

    # 41-50: [간식] (Snacks & Desserts & Emergency)
    {
        'set_id': 41, 'name': '훈제란 & 스트링치즈 & 저지방 우유', 'set_type': '간식', 
        'image_url': 'https://tqklhszfkvzk6518638.edge.naverncp.com/product/8801898160010.jpg', 'total_calorie': 350.0, 'total_carbs': 15.0, 'total_protein': 30.0, 'total_fat': 20.0
    },
    {
        'set_id': 42, 'name': '단팥빵 & 흰 우유', 'set_type': '간식', 
        'image_url': 'https://img1.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202507/24/dailylife/20250724090007581tkhb.jpg', 'total_calorie': 580.0, 'total_carbs': 90.0, 'total_protein': 15.0, 'total_fat': 18.0
    },
    {
        'set_id': 43, 'name': '허니버터칩 & 콜라', 'set_type': '간식', 
        'image_url': 'https://i.namu.wiki/i/RS2VCGdeMMITO--qK5hHEUFK-dqLAy9vkYdErODvqhywVYy5P9-mrV7qqmXbdwId4RhQtgsGGrH8ZY9eiavB3g.webp', 'total_calorie': 650.0, 'total_carbs': 75.0, 'total_protein': 5.0, 'total_fat': 35.0
    },
    {
        'set_id': 44, 'name': '마카롱 2개 & 아메리카노', 'set_type': '간식', 
        'image_url': 'https://www.esquirekorea.co.kr/resources_old/online/org_online_image/eq/883c13d0-3570-4852-80de-35a605bda682.jpg', 'total_calorie': 450.0, 'total_carbs': 70.0, 'total_protein': 8.0, 'total_fat': 18.0
    },
    {
        'set_id': 45, 'name': '초코 우유 & 초코 파이', 'set_type': '간식', 
        'image_url': 'https://contents.lotteon.com/itemimage/20251205092713/LM/88/01/11/75/34/91/2_/00/1/LM8801117534912_001_1.jpg', 'total_calorie': 600.0, 'total_carbs': 90.0, 'total_protein': 15.0, 'total_fat': 20.0
    },
    {
        'set_id': 46, 'name': '에너지 드링크 & 젤리', 'set_type': '간식', 
        'image_url': 'https://www.costco.co.kr/medias/sys_master/images/h8a/he4/228219758051358.jpg', 'total_calorie': 380.0, 'total_carbs': 85.0, 'total_protein': 2.0, 'total_fat': 4.0
    },
    {
        'set_id': 47, 'name': '프레첼 & 탄산수', 'set_type': '간식', 
        'image_url': 'https://thumbnail.coupangcdn.com/thumbnails/remote/492x492ex/image/vendor_inventory/b8a0/718c8f8b2256b51d7f376a56e96096a224ac9800b735e920b51bd18b221b.jpg', 'total_calorie': 400.0, 'total_carbs': 60.0, 'total_protein': 8.0, 'total_fat': 15.0
    },
    {
        'set_id': 48, 'name': '따뜻한 우유 & 꿀', 'set_type': '간식', 
        'image_url': 'https://cdn.011st.com/11dims/resize/1000x1000/quality/75/11src/product/1024122392/B.jpg?781000000', 'total_calorie': 250.0, 'total_carbs': 35.0, 'total_protein': 10.0, 'total_fat': 8.0
    },
    {
        'set_id': 49, 'name': '나쵸 & 소시지 & 탄산수', 'set_type': '간식', 
        'image_url': 'https://i.namu.wiki/i/4YfFuz40mRCXgYPfokojA-c09q8cvb8_v_nhiTpUA7MG6pi4K3PRSqjTxqFTHacBLmpXxU1bqH8BdLzGT2dQcA.webp', 'total_calorie': 520.0, 'total_carbs': 50.0, 'total_protein': 20.0, 'total_fat': 28.0
    },
    {
        'set_id': 50, 'name': '과일 컵 & 탄산수', 'set_type': '간식', 
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJoZjhIViohN74pjc0J3n6zPNqdoQzK8Q5MA&ss', 'total_calorie': 150.0, 'total_carbs': 35.0, 'total_protein': 2.0, 'total_fat': 1.0
    },
]

def upgrade() -> None:
    """Upgrade schema: Insert 50 convenience store recipe sets (General categories)."""
    
    # op.bulk_insert를 사용하여 데이터 삽입
    op.bulk_insert(
        sa.table(
            'recipe_sets', # 테이블 이름: 'recipe_sets'
            sa.column('set_id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('set_type', sa.String),
            sa.column('image_url', sa.String),
            sa.column('total_calorie', sa.Float),
            sa.column('total_carbs', sa.Float),
            sa.column('total_protein', sa.Float),
            sa.column('total_fat', sa.Float),
        ),
        RECIPE_SET_DATA
    )
    
    # 데이터베이스 시퀀스 조정 (DB 종류에 따라 필요)
    # op.execute(text("SELECT setval('recipe_set_set_id_seq', 50, true)"))


def downgrade() -> None:
    """Downgrade schema: Delete inserted recipe sets."""
    
    # 삽입했던 set_id 목록을 추출
    set_ids_to_delete = [data['set_id'] for data in RECIPE_SET_DATA]
    
    # DELETE 쿼리를 사용하여 해당 ID의 데이터 삭제
    # ⚠️ 테이블 이름을 'recipe_sets'로 수정했습니다.
    op.execute(
        sa.text("DELETE FROM recipe_sets WHERE set_id IN :ids")
        .bindparams(ids=tuple(set_ids_to_delete))
    )
    
    # 데이터베이스 시퀀스 조정 (DB 종류에 따라 필요)
    # op.execute(text("SELECT setval('recipe_set_set_id_seq', (SELECT MAX(set_id) FROM recipe_sets), false)"))

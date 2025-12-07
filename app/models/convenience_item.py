from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# NOTE: 실제 프로젝트에서는 Base는 app.core.database에서 import 됩니다.
# 여기서는 예시를 위해 임시로 정의합니다.
Base = declarative_base()


# =================================================================
# 1. RECIPE_SET 테이블: RecipeSet (세트 정보 및 요약)
# =================================================================
class RecipeSet(Base):
    """편의점 식단 추천의 전체 세트(고단백 샐러드 세트 등) 정의."""
    __tablename__ = "recipe_sets"

    set_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255), nullable=False)           # 세트 이름 (예: '고단백 샐러드 세트')
    set_type = Column(String(50), nullable=False)        # 세트 목적/유형 (예: '고단백', '다이어트', '운동 후')
    image_url = Column(String(500), nullable=True)       # 세트 대표 이미지 URL
    
    # 영양 성분 필드 (세트 전체의 총합)
    total_calorie = Column(Float, nullable=False)        # 총 칼로리 (화면의 450 kcal)
    total_carbs = Column(Float, nullable=False)          # 총 탄수화물
    total_protein = Column(Float, nullable=False)        # 총 단백질
    total_fat = Column(Float, nullable=False)            # 총 지방
    
    # ORM 관계
    composition = relationship("SetComposition", back_populates="recipe_set")


# =================================================================
# 2. ITEM 테이블: ConvenienceItem (개별 편의점 상품 정보)
# =================================================================
class ConvenienceItem(Base):
    """레시피를 구성하는 개별 편의점 상품 목록 (영양 정보 원본)."""
    __tablename__ = "convenience_items"

    item_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255), nullable=False, unique=True) # 상품명 (예: '닭가슴살 샐러드 (1개, 200g)')
    
    # 해당 상품의 개별 영양 성분 (세트 총합 계산의 기준)
    calorie = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)

    # ORM 관계
    recipe_sets = relationship("SetComposition", back_populates="item")


# =================================================================
# 3. SET_ITEM_DETAIL 테이블: SetComposition (세트 구성 상세 연결)
# =================================================================
class SetComposition(Base):
    """레시피(세트)가 어떤 상품(ConvenienceItem)으로 구성되었는지 정의하는 M:N 관계 테이블"""
    __tablename__ = "set_composition"

    # 복합 PK
    set_id = Column(Integer, ForeignKey("recipe_sets.set_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("convenience_items.item_id"), primary_key=True)
    
    # 구성 정보
    amount = Column(Float, nullable=False)                   # 세트 내 상품 수량
    unit = Column(String(50), nullable=False)                # 수량 단위

    # ORM 관계
    recipe_set = relationship("RecipeSet", back_populates="composition")
    item = relationship("ConvenienceItem", back_populates="recipe_sets")

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base # 프로젝트의 Base 클래스 import (가정)


# =================================================================
# 4) Ingredient_Allergen 테이블 (Ingredient와 Allergy 연결 - M:N 관계 테이블)
# =================================================================
class IngredientAllergen(Base):
    """
    원재료(Ingredient)가 어떤 알레르기(Allergy)를 포함하는지 정의하는 M:N 관계 테이블.
    (Association Object 패턴 사용)
    """
    __tablename__ = "ingredient_allergen"
    
    # 복합 PK이자 외래 키: Ingredient 테이블 참조
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"), primary_key=True)
    
    # 복합 PK이자 외래 키: Allergy 테이블 참조
    # (주의: Allergy 테이블의 PK 컬럼 이름이 'allergy_id'여야 함)
    allergy_id = Column(Integer, ForeignKey("allergies.id"), primary_key=True)
    
    # ORM 관계
    # Ingredient 모델에 back_populates="allergens" 설정이 필요합니다.
    ingredient = relationship("Ingredient", back_populates="allergens")
    
    # Allergy 모델에 back_populates="ingredients" 설정이 필요합니다.
    allergy = relationship("Allergy", back_populates="ingredients_allergens")

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base 


class IngredientAllergen(Base):
    """
    원재료(Ingredient)가 어떤 알레르기(Allergy)를 포함하는지 정의하는 M:N 관계 테이블.
    (Association Object 패턴 사용)
    """
    __tablename__ = "ingredient_allergen"
    
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"), primary_key=True)

    allergy_id = Column(Integer, ForeignKey("allergies.id"), primary_key=True)
    
    ingredient = relationship("Ingredient", back_populates="allergens")
    
    allergy = relationship("Allergy", back_populates="ingredients_allergens")

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


# =================================================================
# 1) Recipe 테이블 (아침,점심,저녁 각각의 전체 세트 구성)
# =================================================================
class Recipe(Base):
    """전체 레시피 세트(아침, 점심, 저녁)를 정의하는 테이블 모델."""
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True) # 레시피의 고유 식별자 (PK)
    name = Column(String(255), nullable=False)                # 레시피 이름 (NOT NULL)
    description = Column(Text, nullable=True)                 # 추천 이유, 간단한 설명
    meal_type = Column(String(50), nullable=False)            # 식사 유형 (NOT NULL)
    image_url = Column(String(500), nullable=True)            # 레시피 대표 이미지 URL
    
    # ORM 관계
    # 영양 정보 (RecipeNutrition과 1:1 관계)
    nutrition = relationship("RecipeNutrition", back_populates="recipe", uselist=False) 
    
    # 구성 품목 (RecipeComposition과의 M:N 관계)
    composition = relationship("RecipeComposition", back_populates="recipe")
    
    # 알레르기 목록 (RecipeAllergen과의 M:N 관계)
    allergens = relationship("RecipeAllergen", back_populates="recipe")


# =================================================================
# 2) Meal_Item 테이블 (식단 구성 품목 목록)
# =================================================================
class MealItem(Base):
    """레시피를 구성하는 개별 품목(음식) 목록."""
    __tablename__ = "meal_items"

    item_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255), nullable=False, unique=True)
    cooking_method = Column(Text, nullable=True)

    cooking_steps = relationship(
        "CookingStep", 
        back_populates="item", 
        order_by="CookingStep.step_number", # 순서대로 정렬 (선택 사항)
        cascade="all, delete-orphan"        # MealItem 삭제 시 함께 삭제 (선택 사항)
    )

    # ORM 관계
    # 레시피 구성 (RecipeComposition과의 M:N 관계)
    recipes = relationship("RecipeComposition", back_populates="item")
    
    # 원재료 구성 (ItemIngredient와의 M:N 관계)
    ingredients = relationship("ItemIngredient", back_populates="item")


# =================================================================
# 3) Ingredient 테이블 (원재료 목록)
# =================================================================
class Ingredient(Base):
    """원재료 목록"""
    __tablename__ = "ingredients"

    ingredient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    
    # 알레르기 테이블에 맞게 기존 allergen_id 컬럼 제거
    # allergen_id 컬럼 제거

    # ORM 관계 (ItemIngredient와의 M:N 관계)
    meal_items = relationship("ItemIngredient", back_populates="ingredient")

    allergens = relationship("IngredientAllergen", back_populates="ingredient")
    
    # 알레르기 관계는 IngredientAllergen 테이블을 통해 다른 파일에서 설정되어야 합니다.
    # allergies = relationship("IngredientAllergen", back_populates="ingredient")


# =================================================================
# 4) Recipe_Nutrition 테이블(레시피 내 영양 성분 정보)
# =================================================================
class RecipeNutrition(Base):
    """레시피 전체의 영양 성분 정보 (Recipe와 1:1 관계)"""
    __tablename__ = "recipe_nutrition"
    
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True) 
    
    calories = Column(Float, nullable=False)
    carbohydrates = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)

    # ORM 관계 (Recipe와 1:1)
    recipe = relationship("Recipe", back_populates="nutrition")

# =================================================================
# 관계 테이블 정의 (Association Objects)
# =================================================================

# 1) Recipe_Composition 테이블(Recipe와 Meal_Item 연결)
class RecipeComposition(Base):
    """레시피가 어떤 품목(MealItem)으로 구성되었는지 정의하는 M:N 관계 테이블"""
    __tablename__ = "recipe_composition"

    # 복합 PK
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("meal_items.item_id"), primary_key=True)
    
    amount = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    # ORM 관계
    recipe = relationship("Recipe", back_populates="composition")
    item = relationship("MealItem", back_populates="recipes")


# 2) Item_Ingredient 테이블(Meal_Item과 Ingredient 연결)
class ItemIngredient(Base):
    """품목이 어떤 원재료로 구성되었는지 정의하는 M:N 관계 테이블"""
    __tablename__ = "item_ingredient"

    # 복합 PK
    item_id = Column(Integer, ForeignKey("meal_items.item_id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"), primary_key=True)
    
    amount = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    # ORM 관계
    item = relationship("MealItem", back_populates="ingredients")
    # **수정**: back_populates 추가
    ingredient = relationship("Ingredient", back_populates="meal_items") 


# 3) Recipe_Allergen 테이블(레시피 알레르기 목록)
class RecipeAllergen(Base):
    """각 레시피가 포함하는 알레르기 정보를 정의하는 M:N 관계 테이블"""
    __tablename__ = "recipe_allergen"

    # 복합 PK
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    # **수정**: Foreign Key를 'allergies.id'로 변경
    # **수정**: 컬럼 이름을 'allergy_id'로 변경
    allergy_id = Column(Integer, ForeignKey("allergies.id"), primary_key=True)

    # ORM 관계
    recipe = relationship("Recipe", back_populates="allergens")
    # **수정**: relationship 이름을 'allergy'로 변경
    # (Allergy 모델에 back_populates='recipes'가 있다고 가정)
    allergy = relationship("Allergy", back_populates="recipes")

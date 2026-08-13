from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Recipe(Base):
    """전체 레시피 세트(아침, 점심, 저녁)를 정의하는 테이블 모델."""
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255), nullable=False)                
    description = Column(Text, nullable=True)                 
    meal_type = Column(String(50), nullable=False)            
    image_url = Column(String(500), nullable=True)            
    
    nutrition = relationship("RecipeNutrition", back_populates="recipe", uselist=False) 
    
    composition = relationship("RecipeComposition", back_populates="recipe")
    
    allergens = relationship("RecipeAllergen", back_populates="recipe")


class MealItem(Base):
    """레시피를 구성하는 개별 품목(음식) 목록."""
    __tablename__ = "meal_items"

    item_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255), nullable=False, unique=True)
    cooking_method = Column(Text, nullable=True)

    cooking_steps = relationship(
        "CookingStep", 
        back_populates="item", 
        order_by="CookingStep.step_number", 
        cascade="all, delete-orphan"        
    )

    recipes = relationship("RecipeComposition", back_populates="item")

    ingredients = relationship("ItemIngredient", back_populates="item")


class Ingredient(Base):
    """원재료 목록"""
    __tablename__ = "ingredients"

    ingredient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)


    meal_items = relationship("ItemIngredient", back_populates="ingredient")

    allergens = relationship("IngredientAllergen", back_populates="ingredient")
    

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


class RecipeComposition(Base):
    """레시피가 어떤 품목(MealItem)으로 구성되었는지 정의하는 M:N 관계 테이블"""
    __tablename__ = "recipe_composition"

    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("meal_items.item_id"), primary_key=True)
    
    amount = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    recipe = relationship("Recipe", back_populates="composition")
    item = relationship("MealItem", back_populates="recipes")


class ItemIngredient(Base):
    """품목이 어떤 원재료로 구성되었는지 정의하는 M:N 관계 테이블"""
    __tablename__ = "item_ingredient"

    
    item_id = Column(Integer, ForeignKey("meal_items.item_id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"), primary_key=True)
    
    amount = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    
    item = relationship("MealItem", back_populates="ingredients")
    
    ingredient = relationship("Ingredient", back_populates="meal_items") 



class RecipeAllergen(Base):
    """각 레시피가 포함하는 알레르기 정보를 정의하는 M:N 관계 테이블"""
    __tablename__ = "recipe_allergen"

    
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    
    allergy_id = Column(Integer, ForeignKey("allergies.id"), primary_key=True)

    
    recipe = relationship("Recipe", back_populates="allergens")

    allergy = relationship("Allergy", back_populates="recipes")

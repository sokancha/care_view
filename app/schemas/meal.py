from pydantic import BaseModel
from typing import List, Dict, Union

# --- 1. 재료 이름 정의 스키마 ---
# RecipeComposition 모델의 'item' 관계가 참조하는 객체의 이름만 담습니다.
class ItemNameSchema(BaseModel):
    name: str 
    
    class Config:
        from_attributes = True

class IngredientNameSchema(BaseModel):
    """Ingredient 모델의 이름만 포함하는 스키마"""
    name: str 
    
    class Config:
        from_attributes = True

# --- 2. 레시피 구성 스키마 (핵심 수정) ---
# DB의 recipe_composition 테이블 구조 + 관계를 반영합니다.
class RecipeCompositionSchema(BaseModel):
    """
    RecipeComposition 모델을 매핑하며, 재료 이름(name)을 관계 객체(item)에서 가져옵니다.
    """
    # recipe_composition 테이블의 필드
    amount: float 
    unit: str 
    
    # 🌟 핵심: RecipeComposition 모델의 'item' 관계 객체를 로드
    item: ItemNameSchema 

    # 🌟 응답에 필요한 'name' 필드를 계산된 속성으로 추가 (item.name에서 값을 읽음)
    @property
    def name(self) -> str:
        # ORM 객체가 로드된 후 item.name을 반환
        return self.item.name 
    
    class Config:
        from_attributes = True
        # Pydantic V2에서는 computed_fields=["name"]가 필요할 수 있습니다.
        # computed_fields = ["name"] 


# --- (기존 스키마 유지) 영양 성분 스키마 ---
class NutritionSchema(BaseModel):
    calories: float
    carbohydrates: float
    protein: float
    fat: float
    
    class Config:
        from_attributes = True

# --- 3. 레시피 상세 스키마 (수정) ---
# composition 리스트가 새로운 RecipeCompositionSchema를 참조합니다.
class RecipeDetailSchema(BaseModel):
    recipe_id: int
    name: str
    description: Union[str, None]
    meal_type: str
    image_url: Union[str, None]
    
    nutrition: NutritionSchema 
    
    # 🌟 수정: composition 리스트가 RecipeCompositionSchema를 참조하도록 변경
    composition: List[RecipeCompositionSchema] 
    
    class Config:
        from_attributes = True

# --- (기존 스키마 유지) 메인 추천 스키마 ---
class MainRecommendationSchema(BaseModel):
    breakfast: Union[RecipeDetailSchema, None] = None
    lunch: Union[RecipeDetailSchema, None] = None
    dinner: Union[RecipeDetailSchema, None] = None

# --- (기존 스키마 유지) 총 영양 성분 스키마 ---
class TotalNutritionSchema(BaseModel):
    """추천된 3가지 레시피의 총 영양 성분 합계"""
    calories: float
    carbohydrates: float
    protein: float
    fat: float
    
    class Config:
        from_attributes = True


# --- (기존 스키마 유지) 최종 응답 스키마 ---
class MainRecommendationResponse(BaseModel):
    """메인 페이지 추천의 최종 응답 스키마 (추천 목록 + 총계)"""
    # 기존 MainRecommendationSchema의 내용
    breakfast: Union[RecipeDetailSchema, None] = None
    lunch: Union[RecipeDetailSchema, None] = None
    dinner: Union[RecipeDetailSchema, None] = None
    
    totals: TotalNutritionSchema 
    
    class Config:
        from_attributes = True

class ItemIngredientDetailSchema(BaseModel):
    amount: float
    unit: str
    # ItemIngredient 모델의 'ingredient' 관계에서 Ingredient.name을 가져옴
    ingredient: IngredientNameSchema

class CookingStepSchema(BaseModel):
    step_number: int
    step_description: str
    
    class Config:
        from_attributes = True

class MealItemRecipeSchema(BaseModel):
    item_id: int
    name: str
    
    # MealItem 모델의 'ingredients' 관계 참조
    ingredients: List[ItemIngredientDetailSchema] 
    
    # MealItem 모델의 'cooking_steps' 관계 참조
    cooking_steps: List[CookingStepSchema]
    
    class Config:
        from_attributes = True

class ConvenienceItemSchema(BaseModel):
    item_id: int
    name: str
    
    class Config:
        from_attributes = True

class SetCompositionSchema(BaseModel):
    amount: float
    unit: str
    
    # 🚨 핵심: SetComposition 모델의 'item' 관계 객체를 로드 (ConvenienceItemSchema 사용)
    item: ConvenienceItemSchema 

    class Config:
        from_attributes = True

class ConvenienceSetResponse(BaseModel):
    set_id: int
    name: str 
    set_type: str 
    image_url: Union[str, None]
    
    # 세트의 총 영양소 (RecipeSet 테이블 컬럼 그대로 매핑)
    total_calorie: float
    total_carbs: float
    total_protein: float
    total_fat: float
    
    # 🚨 핵심: 세트의 구성품 목록 (RecipeSet.composition 관계 객체 사용)
    composition: List[SetCompositionSchema] 

    class Config:
        from_attributes = True

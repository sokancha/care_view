from pydantic import BaseModel
from typing import List, Dict, Union

class ItemNameSchema(BaseModel):
    name: str 
    
    class Config:
        from_attributes = True

class IngredientNameSchema(BaseModel):
    """Ingredient 모델의 이름만 포함하는 스키마"""
    name: str 
    
    class Config:
        from_attributes = True

class RecipeCompositionSchema(BaseModel):
    """
    RecipeComposition 모델을 매핑하며, 재료 이름(name)을 관계 객체(item)에서 가져옵니다.
    """
    amount: float 
    unit: str 
    
    item: ItemNameSchema 

    @property
    def name(self) -> str:
        # ORM 객체가 로드된 후 item.name을 반환
        return self.item.name 
    
    class Config:
        from_attributes = True
        # Pydantic V2에서는 computed_fields=["name"]가 필요할 수 있습니다.
        # computed_fields = ["name"] 


class NutritionSchema(BaseModel):
    calories: float
    carbohydrates: float
    protein: float
    fat: float
    
    class Config:
        from_attributes = True

class RecipeDetailSchema(BaseModel):
    recipe_id: int
    name: str
    description: Union[str, None]
    meal_type: str
    image_url: Union[str, None]
    
    nutrition: NutritionSchema 

    composition: List[RecipeCompositionSchema] 
    
    class Config:
        from_attributes = True

class MainRecommendationSchema(BaseModel):
    breakfast: Union[RecipeDetailSchema, None] = None
    lunch: Union[RecipeDetailSchema, None] = None
    dinner: Union[RecipeDetailSchema, None] = None

class TotalNutritionSchema(BaseModel):
    """추천된 3가지 레시피의 총 영양 성분 합계"""
    calories: float
    carbohydrates: float
    protein: float
    fat: float
    
    class Config:
        from_attributes = True


class MainRecommendationResponse(BaseModel):
    """메인 페이지 추천의 최종 응답 스키마 (추천 목록 + 총계)"""
    breakfast: Union[RecipeDetailSchema, None] = None
    lunch: Union[RecipeDetailSchema, None] = None
    dinner: Union[RecipeDetailSchema, None] = None
    
    totals: TotalNutritionSchema 
    
    class Config:
        from_attributes = True

class ItemIngredientDetailSchema(BaseModel):
    amount: float
    unit: str
    ingredient: IngredientNameSchema

class CookingStepSchema(BaseModel):
    step_number: int
    step_description: str
    
    class Config:
        from_attributes = True

class MealItemRecipeSchema(BaseModel):
    item_id: int
    name: str
    
    ingredients: List[ItemIngredientDetailSchema] 
    
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
    
    item: ConvenienceItemSchema 

    class Config:
        from_attributes = True

class ConvenienceSetResponse(BaseModel):
    set_id: int
    name: str 
    set_type: str 
    image_url: Union[str, None]
    
    total_calorie: float
    total_carbs: float
    total_protein: float
    total_fat: float
    
    composition: List[SetCompositionSchema] 

    class Config:
        from_attributes = True

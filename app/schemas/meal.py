from pydantic import BaseModel
from typing import List, Dict, Union

class MealItemSchema(BaseModel):
    name: str  
    amount: float  
    unit: str 
    
    class Config:
        from_attributes = True

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
    
    composition: List[MealItemSchema] 
    
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
    # 기존 MainRecommendationSchema의 내용
    breakfast: Union[RecipeDetailSchema, None] = None
    lunch: Union[RecipeDetailSchema, None] = None
    dinner: Union[RecipeDetailSchema, None] = None
    
    totals: TotalNutritionSchema 
    
    class Config:
        from_attributes = True

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
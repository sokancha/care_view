# api/endpoints/meals.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.core.database import get_db 
from app.schemas.meal import MainRecommendationResponse, TotalNutritionSchema
from app.services.meal_service import get_main_page_recommendations
from app.api.dependencies import get_current_user # 인증 의존성 가정
from app.models.user import User

router = APIRouter(prefix="/api/meals", tags=['meals'])

@router.get("/recommendations/main", response_model=MainRecommendationResponse)
def get_main_recommendations( 
    db: Session = Depends(get_db), # 🚨 Session 타입으로 변경
    current_user: User = Depends(get_current_user) 
):
    user_id: int = current_user.id # type: ignore
    
    recommendations_data = get_main_page_recommendations(db, user_id)
    
    # 2. 총 영양 성분 합계 계산 로직 (Nutrition Aggregation)
    total_calories = 0.0
    total_carbohydrates = 0.0
    total_protein = 0.0
    total_fat = 0.0
    
    # 추천된 레시피 객체들을 순회하며 영양소 합산
    for meal_type in ["breakfast", "lunch", "dinner"]:
        recipe = recommendations_data.get(meal_type)
        if recipe and recipe.nutrition:
            total_calories += recipe.nutrition.calories
            total_carbohydrates += recipe.nutrition.carbohydrates
            total_protein += recipe.nutrition.protein
            total_fat += recipe.nutrition.fat
            
    # 3. 합산된 총 영양 성분 스키마 생성
    totals = TotalNutritionSchema(
        calories=total_calories,
        carbohydrates=total_carbohydrates,
        protein=total_protein,
        fat=total_fat,
    )

    # 4. 최종 응답 데이터 구성
    response_data = {
        "breakfast": recommendations_data.get("breakfast"),
        "lunch": recommendations_data.get("lunch"),
        "dinner": recommendations_data.get("dinner"),
        "totals": totals
    }
    
    return response_data

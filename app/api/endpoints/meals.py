# api/endpoints/meals.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session 
from typing import List, Annotated, Union

from app.core.database import get_db 
from app.schemas.meal import MainRecommendationResponse, TotalNutritionSchema
from app.services.meal_service import get_main_page_recommendations
from app.api.dependencies import get_current_user # 인증 의존성 가정
from app.models.user import User

from app.services.meals_items_crud import (
    get_user_allergy_ids, 
    get_meal_items_by_ingredients_and_allergens
)
from app.schemas.meal import MealItemRecipeSchema, ConvenienceSetResponse
from app.services.convenience_crud import get_convenience_store_sets


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


@router.get(
    "/recommendations/by-ingredients",
    response_model=List[MealItemRecipeSchema], # 🚨 Meal Item 응답 스키마 사용
    summary="냉장고 재료와 사용자 알레르기를 기반으로 단품 요리(Meal Item) 추천"
)
def get_recommendations_by_ingredients(
    # 쿼리 파라미터: 재료 이름 리스트 (예: ingredient_names=닭고기&ingredient_names=양파)
    ingredient_names: Annotated[List[str], Query(
        description="사용자가 가진 재료 이름 목록 (예: 닭고기, 양파)",
        min_length=1
    )],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """
    사용자가 입력한 재료 목록을 모두 사용하여 만들 수 있고, 동시에 사용자의 알레르기 
    유발 재료를 포함하지 않는 Meal Item 목록을 반환합니다.
    """
    
    user_id: int = current_user.id # type: ignore
    
    # 1. 사용자 알레르기 ID 목록 조회
    user_allergy_ids = get_user_allergy_ids(db, user_id)
    
    # 2. Meal Item 추천 로직 실행
    recommended_items = get_meal_items_by_ingredients_and_allergens(
        db=db,
        ingredient_names=ingredient_names,
        user_allergy_ids=user_allergy_ids
    )

    if not recommended_items:
        # 추천 결과가 없으면 빈 리스트 반환 (HTTP 200)
        return []
    
    # 3. ORM 객체를 Pydantic 모델로 변환 (response_model이 처리)
    return recommended_items

@router.get(
    "/convenience/sets",
    response_model=List[ConvenienceSetResponse], 
    summary="편의점 레시피 세트 목록 조회",
)
def get_convenience_recommendations(
    db: Session = Depends(get_db),
    # set_type 파라미터를 받아 특정 유형만 필터링 가능 (예: ?set_type=다이어트)
):
    """
    편의점 식단 페이지에 표시할 레시피 세트 목록을 반환합니다. 
    구성된 상품의 상세 정보(이름, 양, 단위, 개별 영양소)를 포함합니다.
    """
    
    recommended_sets = get_convenience_store_sets(db)
    
    if not recommended_sets:
        # 추천 결과가 없으면 빈 리스트 반환
        return []
    
    # ORM 객체는 Pydantic 모델(response_model=List[ConvenienceSetResponse])에 의해 자동으로 변환됩니다.
    return recommended_sets

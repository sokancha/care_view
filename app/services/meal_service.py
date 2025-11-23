from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, and_, exists, func
from sqlalchemy.ext.asyncio import AsyncSession 

from app.models.meal import (
    Recipe, 
    RecipeNutrition, 
    RecipeComposition, 
    MealItem, 
    RecipeAllergen
)
from app.models.allergy import Allergy
from app.models.user import User 
from typing import Dict, Union, Any, List


async def get_main_page_recommendations(db: AsyncSession, user_id: int) -> Dict[str, Union[Recipe, None]]:
    """
    사용자의 알레르기 정보를 기반으로 아침, 점심, 저녁 식단을 각각 하나씩 추천합니다.
    """
    
    # 사용자가 피해야 할 알레르기 ID 목록을 조회
    user_query = select(User).where(User.id == user_id).options(selectinload(User.allergies))
    
    user = (await db.execute(user_query)).scalar_one_or_none()

    if user and hasattr(user, 'allergies') and user.allergies:
        # 사용자가 가진 알레르기 ID 목록을 추출
        forbidden_allergy_ids: List[int] = [allergy.id for allergy in user.allergies]
    else:
        # 알레르기 정보가 없으면 필터링하지 않습니다.
        forbidden_allergy_ids: List[int] = []

    # 알레르기 필터링 조건 생성
    allergy_filter_subquery = select(RecipeAllergen.recipe_id).where(
        RecipeAllergen.allergy_id.in_(forbidden_allergy_ids)
    )
    
    base_query = select(Recipe)

    # 알레르기 ID 목록이 있다면, 해당 알레르기를 포함하는 레시피를 제외
    if forbidden_allergy_ids:
        base_query = base_query.where(
            ~Recipe.recipe_id.in_(allergy_filter_subquery.scalar_subquery())
        )
    
    # 데이터 로딩 최적화
    query_with_loads = base_query.options(
        joinedload(Recipe.nutrition),
        selectinload(Recipe.composition).joinedload(RecipeComposition.item) 
    )
    
    # 식사 유형별 레시피 조회 및 랜덤 선택
    meal_types = ["Breakfast", "Lunch", "Dinner"]
    recommendations: Dict[str, Union[Recipe, None]] = {}

    for meal_type in meal_types:
        meal_query = query_with_loads.where(Recipe.meal_type == meal_type)
        
        random_recipe = (
            await db.execute(
                meal_query
                .order_by(func.random()) 
                .limit(1)                
            )
        ).scalar_one_or_none()

        if random_recipe:
            recommendations[meal_type.lower()] = random_recipe
    
    return recommendations
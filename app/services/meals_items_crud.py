from sqlalchemy.orm import Session, aliased, joinedload
from sqlalchemy import func, distinct, and_
from typing import List

# ----------------------------------------------------------------------
# 1. 필수 모델 및 Core Table 임포트
# (사용자님의 프로젝트 구조에 맞게 경로를 설정했습니다.)
# ----------------------------------------------------------------------
# [Meal, Ingredient 관련 모델]
from app.models.meal import MealItem, Ingredient, ItemIngredient 
# [알레르기 관련 모델]
from app.models.ingredient_allergy import IngredientAllergen 
from app.models.allergy import user_allergy_association 
# [조리 과정 관련 모델]
from app.models.cooking_step import CookingStep 


# ----------------------------------------------------------------------
# 2. 사용자 알레르기 ID 조회 함수
# ----------------------------------------------------------------------
def get_user_allergy_ids(db: Session, user_id: int) -> List[int]:
    """특정 사용자가 설정한 알레르기 ID 목록을 조회합니다."""
    
    # SQLAlchemy Core Table인 user_allergy_association을 쿼리
    # .all() 결과는 튜플 리스트 형태: [(id1,), (id2,), ...]
    allergy_ids_tuples = (
        db.query(user_allergy_association.c.allergy_id)
        .filter(user_allergy_association.c.user_id == user_id)
        .all() 
    )
    # 튜플에서 ID 값만 추출하여 리스트로 반환
    return [aid for (aid,) in allergy_ids_tuples]


# ----------------------------------------------------------------------
# 3. 핵심 식단 추천 로직 함수
# ----------------------------------------------------------------------
def get_meal_items_by_ingredients_and_allergens(
    db: Session, 
    ingredient_names: List[str], 
    user_allergy_ids: List[int] # get_user_allergy_ids 함수로부터 전달받음
):
    """
    사용자 입력 재료를 모두 포함하고, 알레르기를 유발하는 재료는 포함하지 않는
    Meal Item 목록을 조회합니다.
    """
    
    # 1. 입력 재료 이름 -> ID 목록 조회 (SQLAlchemy 1.x 호환)
    input_ingredient_ids_tuples = (
        db.query(Ingredient.ingredient_id) 
        .filter(Ingredient.name.in_(ingredient_names))
        .all()
    )
    input_ingredient_ids = [ing_id for (ing_id,) in input_ingredient_ids_tuples]
    
    if not input_ingredient_ids:
        return []

    required_count = len(input_ingredient_ids)
    
    # 2. 알레르기 유발 재료 ID 목록 조회 (제외 기준)
    allergen_ingredient_ids_tuples = (
        db.query(IngredientAllergen.ingredient_id)
        .filter(IngredientAllergen.allergy_id.in_(user_allergy_ids))
        .distinct()
        .all()
    )
    allergen_ingredient_ids = [ing_id for (ing_id,) in allergen_ingredient_ids_tuples]

    # 3. 알레르기 포함 Item ID 목록 (제외 대상 서브쿼리)
    allergy_containing_item_ids = (
        db.query(ItemIngredient.item_id)
        .filter(ItemIngredient.ingredient_id.in_(allergen_ingredient_ids))
        .distinct()
        .subquery()
    )

    # 4. 필터링: 입력 재료 모두 포함 + 알레르기 Item 제외
    final_recommended_item_ids_tuples = (
        db.query(ItemIngredient.item_id)
        .filter(
            and_(
                ItemIngredient.ingredient_id.in_(input_ingredient_ids),
                # 알레르기 포함 항목을 제외하는 핵심 로직 (NOT IN)
                ItemIngredient.item_id.notin_(allergy_containing_item_ids) 
            )
        )
        # 입력 재료 개수와 일치하는 Meal Item만 선별 (GROUP BY/HAVING)
        .group_by(ItemIngredient.item_id)
        .having(func.count(distinct(ItemIngredient.ingredient_id)) == required_count)
        .all()
    )
    final_recommended_item_ids = [item_id for (item_id,) in final_recommended_item_ids_tuples]
    
    if not final_recommended_item_ids:
        return []

    # 5. Meal Item 상세 정보 및 관계 테이블 JOIN (Eager Loading)
    recommended_meal_items_query = (
        db.query(MealItem)
        .filter(MealItem.item_id.in_(final_recommended_item_ids)) 
        .options(
            # ItemIngredient를 거쳐 Ingredient 상세 정보까지 로드
            joinedload(MealItem.ingredients).joinedload(ItemIngredient.ingredient),
            # 조리 과정 상세 로드
            joinedload(MealItem.cooking_steps)
        )
        .all()
    )
    
    return recommended_meal_items_query

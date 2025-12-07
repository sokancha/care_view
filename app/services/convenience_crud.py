from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Dict, Union

# ----------------------------------------------------------------------
# 1. 필수 모델 임포트 경로 수정 (모델이 models/convenience_item.py에 있음)
# ----------------------------------------------------------------------
from app.models.convenience_item import (
    RecipeSet, 
    ConvenienceItem, 
    SetComposition
)


# ----------------------------------------------------------------------
# 2. 편의점 세트 목록 조회 함수
# ----------------------------------------------------------------------
def get_convenience_store_sets(db: Session, limit: int = 6):
    """
    모든 편의점 레시피 세트 목록을 조회합니다. 
    set_composition과 convenience_items 상세 정보까지 Eager Loading합니다.
    """
    query = db.query(RecipeSet)

    query = query.order_by(func.random())

    if limit > 0:
        query = query.limit(limit) # 🚨 limit 적용

    # RecipeSet -> SetComposition -> ConvenienceItem의 관계를 미리 로드
    sets = query.options(
        joinedload(RecipeSet.composition)
        .joinedload(SetComposition.item) 
    ).all()
    
    return sets

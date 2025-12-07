from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base # 사용자님의 프로젝트 구조에 맞추어 Base 클래스를 가져옵니다.

# =================================================================
# CookingStep 테이블 (조리 단계별 설명)
# MealItem과 1:N 관계
# =================================================================
class CookingStep(Base):
    """
    개별 MealItem의 조리 단계를 순서대로 저장하는 테이블 모델입니다.
    MealItem 테이블과 1:N 관계를 가집니다.
    """
    __tablename__ = "cooking_steps"

    # 기본 키: 단계별 고유 식별자
    step_id = Column(Integer, primary_key=True, index=True)
    
    # 외래 키: MealItem 테이블을 참조 (1:N 관계의 '1' 쪽 참조)
    # MealItem의 item_id를 외래키로 사용합니다.
    item_id = Column(Integer, ForeignKey("meal_items.item_id"), nullable=False)
    
    # 조리 단계의 순서 (정렬용)
    step_number = Column(Integer, nullable=False)
    
    # 조리 단계에 대한 상세 설명 (사진 속 텍스트)
    step_description = Column(Text, nullable=False)

    # ORM 관계
    # MealItem과의 관계 설정 (MealItem 모델에 back_populates를 설정해야 합니다.)
    item = relationship("MealItem", back_populates="cooking_steps")

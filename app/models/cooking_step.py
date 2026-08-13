from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base # 사용자님의 프로젝트 구조에 맞추어 Base 클래스를 가져옵니다.

class CookingStep(Base):
    """
    개별 MealItem의 조리 단계를 순서대로 저장하는 테이블 모델입니다.
    MealItem 테이블과 1:N 관계를 가집니다.
    """
    __tablename__ = "cooking_steps"

    step_id = Column(Integer, primary_key=True, index=True)
    
    item_id = Column(Integer, ForeignKey("meal_items.item_id"), nullable=False)
    
    step_number = Column(Integer, nullable=False)
    
    step_description = Column(Text, nullable=False)
    item = relationship("MealItem", back_populates="cooking_steps")

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base  


class HealthMetric(Base):
    """
    사용자의 건강 지표를 시간순으로 기록하는 테이블 모델.
    users 테이블과 1:N 관계를 가집니다.
    """
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="metrics") 


    weight_kg = Column(Float, nullable=False)           
    bmi = Column(Float, nullable=True)                  
    sleep_duration_hours = Column(Float, nullable=True) 
    exercise_duration_hours = Column(Float, nullable=True) 
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

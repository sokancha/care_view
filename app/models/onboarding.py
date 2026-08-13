from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text, Date 
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base 
from .user import User


class OnboardingConfig(Base):
    """
    사용자의 온보딩 6단계 설정 정보를 저장하는 테이블 모델.
    나이는 date_of_birth를 기준으로 API에서 실시간 계산합니다.
    """
    __tablename__ = "onboarding_configs"

    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", back_populates="config")

    goal = Column(String(50), nullable=False) 
    
    weekly_workout_schedule = Column(Text, nullable=True) 
    workouts_per_week = Column(Integer, nullable=True) 
    intensity_level = Column(String(20), nullable=True) 
    
    date_of_birth = Column(Date, nullable=True)
    height_cm = Column(Float, nullable=True) 
    current_weight_kg = Column(Float, nullable=True)
    target_weight_kg = Column(Float, nullable=True) 
    
    
    job_type = Column(String(30), nullable=True) 
    activity_level = Column(String(30), nullable=True) 

    is_onboarding_complete = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

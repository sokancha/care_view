from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text, Date # 🚨 Date 임포트 추가
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

# Base 객체 임포트 (app/core/database.py에 정의됨)
from app.core.database import Base 
# User 모델과의 ORM 관계 설정을 위해 User 모델을 임포트합니다.
from .user import User


class OnboardingConfig(Base):
    """
    사용자의 온보딩 6단계 설정 정보를 저장하는 테이블 모델.
    나이는 date_of_birth를 기준으로 API에서 실시간 계산합니다.
    """
    __tablename__ = "onboarding_configs"

    # 1. 고유 키 및 관계 설정
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", back_populates="config")

    # 2. 목표 설정 (Goal) - Step 1
    goal = Column(String(50), nullable=False) 
    
    # 3. 운동 스케줄 (Workout Schedule) - Step 2
    weekly_workout_schedule = Column(Text, nullable=True) 
    workouts_per_week = Column(Integer, nullable=True) 
    intensity_level = Column(String(20), nullable=True) 
    
    # 4. 기본 정보 (Basic Info) - Step 3 
    
    # 🚨 age 컬럼 삭제, date_of_birth로 대체 확정
    date_of_birth = Column(Date, nullable=True)
    height_cm = Column(Float, nullable=True) 
    current_weight_kg = Column(Float, nullable=True)
    target_weight_kg = Column(Float, nullable=True) 
    
    
    # 5. 직업/활동 레벨 (Activity Level) - Step 4
    job_type = Column(String(30), nullable=True) 
    activity_level = Column(String(30), nullable=True) 

    # 6. 완료 상태 및 시간 - Step 6
    is_onboarding_complete = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
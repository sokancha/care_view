from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text
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
    users 테이블과 1:1 관계를 가집니다.
    """
    __tablename__ = "onboarding_configs"

    # 1. 고유 키 및 관계 설정
    id = Column(Integer, primary_key=True, index=True)
    
    # 외래 키: users 테이블의 id를 참조하며, unique=True로 1:1 관계를 보장합니다.
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # ORM 관계 설정: User 모델을 참조하여 config.user 형태로 접근 가능
    user = relationship("User", back_populates="config")


    # 2. 목표 설정 (Goal) - Step 1
    # 선택지: 'fat_loss' (체지방 감소), 'muscle_gain' (근육량 증가)
    goal = Column(String(50), nullable=False) 
    
    # 3. 운동 스케줄 (Workout Schedule) - Step 2
    # 요일별 상세 운동 시간을 JSON 문자열 (TEXT)로 저장
    weekly_workout_schedule = Column(Text, nullable=True) 

    workouts_per_week = Column(Integer, nullable=True) # 주간 운동 횟수
    intensity_level = Column(String(20), nullable=True) # 운동 강도
    
    # 4. 기본 정보 (Basic Info) - Step 3 
    age = Column(Integer, nullable=True)             # 나이
    height_cm = Column(Float, nullable=True)        # 신장 (cm)
    current_weight_kg = Column(Float, nullable=True) # 현재 체중 (kg)
    target_weight_kg = Column(Float, nullable=True)  # 목표 체중 (kg)
    
    
    # 5. 직업/활동 레벨 (Activity Level) - Step 4
    job_type = Column(String(30), nullable=True) # 선택된 직업 유형 (예: 'student', 'worker')
    activity_level = Column(String(30), nullable=True) # 신체 활동 수준 (예: 'moderate', 'high')


    # 6. 완료 상태 및 시간 - Step 6
    # 온보딩 완료 여부 (True/False)를 저장합니다.
    is_onboarding_complete = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
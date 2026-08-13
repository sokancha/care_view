from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base 
from datetime import datetime
from .allergy import user_allergy_association


class User(Base):
    """
    사용자 정보를 저장하는 테이블 모델.
    회원가입 창의 필수 입력 정보와 약관 동의 정보를 포함하며, OnboardingConfig와 1:1 관계를 가집니다.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String) 
    
    full_name = Column(String, index=True, nullable=True)
    gender = Column(String, nullable=True) 
    
    provider = Column(String, default="email")
    is_active = Column(Boolean, default=True)
    
    is_terms_agreed = Column(Boolean, default=False, nullable=False)
    is_privacy_agreed = Column(Boolean, default=False, nullable=False)
    is_marketing_agreed = Column(Boolean, nullable=False, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    config = relationship("OnboardingConfig", back_populates="user", uselist=False)
    
    metrics = relationship("HealthMetric", back_populates="user", cascade="all, delete-orphan")
    

    allergies = relationship(
        "Allergy",
        secondary=user_allergy_association,
        back_populates="users"
    )

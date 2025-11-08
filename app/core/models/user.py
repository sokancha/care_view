from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship # 🚨 추가: 관계 설정을 위해 임포트
from sqlalchemy.sql import func
from app.core.database import Base # app.core.database에서 정의된 Base를 가져옵니다.
from datetime import datetime

class User(Base):
    """
    사용자 정보를 저장하는 테이블 모델.
    회원가입 창의 필수 입력 정보와 약관 동의 정보를 포함하며, OnboardingConfig와 1:1 관계를 가집니다.
    """
    __tablename__ = "users"

    # 1. 핵심 인증 정보
    id = Column(Integer, primary_key=True, index=True)
    
    # 이메일 (로그인 ID)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # 해시 처리된 비밀번호 (Google 로그인의 경우 NULL일 수 있음)
    hashed_password = Column(String) 
    
    # 2. 사용자 식별 정보
    full_name = Column(String, index=True, nullable=True) # 이름 (홍길동)
    
    # 성별 정보 추가: 'male', 'female', 'other' 등 문자열로 저장
    gender = Column(String, nullable=True) 
    
    # 3. 서비스 및 계정 상태
    provider = Column(String, default="email") # 가입 방식: 'email' 또는 'google' 등
    is_active = Column(Boolean, default=True) # 🚨 추가: 사용자 계정 활성화 상태
    
    # 4. 약관 동의 정보 (회원가입 창에 명시된 필수/선택 동의 사항)
    is_terms_agreed = Column(Boolean, default=False, nullable=False) # 이용약관 동의 (필수)
    is_privacy_agreed = Column(Boolean, default=False, nullable=False) # 개인정보 처리방침 동의 (필수)
    is_marketing_agreed = Column(Boolean, default=False, nullable=False) # 🚨 추가: 마케팅 동의 (선택)
    

    # 5. 시간 정보
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 가입 시점 기록
    
    # 6. 관계 (Relationships)
    # 🚨 추가: OnboardingConfig와 1:1 관계 설정 (back_populates="user", uselist=False)
    # User.config로 온보딩 설정에 접근 가능
    config = relationship("OnboardingConfig", back_populates="user", uselist=False)
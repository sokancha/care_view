from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func 
from app.core.database import Base
from datetime import datetime

class User(Base):

    __tablename__ = "users"

    # 핵심 인증 정보
    id = Column(Integer, primary_key=True, index=True)
    
    # 이메일 (로그인 ID)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # 해시 처리된 비밀번호 (Google 로그인의 경우 NULL일 수 있음)
    hashed_password = Column(String) 
    
    # 사용자 식별 정보
    full_name = Column(String, index=True, nullable=True)
    
    # 성별 정보 추가: 'male', 'female', 'other' 등 문자열로 저장
    gender = Column(String, nullable=True) 
    
    # 서비스 및 계정 상태
    provider = Column(String, default="email") # 가입 방식: 'email' 또는 'google' 등

    # 약관 동의 정보 (회원가입 창에 명시된 필수/선택 동의 사항)
    is_terms_agreed = Column(Boolean, default=False, nullable=False) # 이용약관 동의 (필수)
    is_privacy_agreed = Column(Boolean, default=False, nullable=False) # 개인정보 처리방침 동의 (필수)
  

    # 시간 정보
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 가입 시점 기록
    
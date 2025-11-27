from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from .user import User
from .onboarding import OnboardingConfig
from .allergy import Allergy
from .main_health_metric import HealthMetric 
from .meal import *


# BaseUser: 사용자 정보를 담는 기본 스키마 (필수 필드)
class BaseUser(BaseModel):
    """
    사용자가 회원가입 시 입력해야 하는 정보의 기본 스키마입니다.
    """
    email: EmailStr = Field(..., description="사용자 이메일 (로그인 ID)")
    password: str = Field(..., min_length=8, description="비밀번호 (최소 8자)")
    full_name: Optional[str] = Field(None, description="사용자 이름")
    gender: Optional[str] = Field(None, description="성별 ('male', 'female', 'other' 등)")
    
    # 약관 동의 (회원가입 창에 필수/선택 항목)
    is_terms_agreed: bool = Field(False, description="이용약관 동의 여부 (필수)")
    is_privacy_agreed: bool = Field(False, description="개인정보 처리방침 동의 여부 (필수)")
    is_marketing_agreed: bool = Field(False, description="마케팅 정보 수신 동의 여부 (선택)")

# UserCreate: 회원가입 요청 시 사용 (BaseUser 상속)
class UserCreate(BaseUser):
    # BaseUser의 필드를 그대로 사용
    pass

# UserInDBBase: DB에서 읽어올 때 사용되는 기본 스키마 (비밀번호 제외)
class UserInDBBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    full_name: Optional[str]
    gender: Optional[str]
    is_active: bool
    provider: str
    is_terms_agreed: bool
    is_privacy_agreed: bool
    is_marketing_agreed: bool
    created_at: datetime

    class Config:
        from_attributes = True

# UserResponse: API 응답 시 사용 (클라이언트에게 반환)
class UserResponse(UserInDBBase):
    pass
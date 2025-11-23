# 데이터 검증/형식 : API 요청 및 응답 데이터의 구조(Pydantic 모델)를 정의

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# BaseUser: 모든 사용자 데이터의 기본 필드 정의
class BaseUser(BaseModel):
    # 사용자가 회원가입 시 입력하는 정보의 기본 스키마
    # EmailStr은 Pydantic이 이메일 형식을 자동으로 검증
    email: EmailStr = Field(..., description="사용자 이메일 (로그인 ID)")
    
    # 비밀번호는 Create 스키마에만 포함
    password: str = Field(..., min_length=8, description="비밀번호 (최소 8자)")
    
    full_name: Optional[str] = Field(None, description="사용자 이름")
    gender: Optional[str] = Field(None, description="성별 ('male', 'female', 'other' 등)")
    
    is_terms_agreed: bool = Field(False, description="이용약관 동의 여부 (필수)")
    is_privacy_agreed: bool = Field(False, description="개인정보 처리방침 동의 여부 (필수)")

# UserCreate: 회원가입 요청 (POST /register)
class UserCreate(BaseUser):
    pass

# UserLogin: 로그인 요청 (POST /login)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# UserInDBBase: DB에서 읽어올 때 사용 (비밀번호 등 민감정보 제외)
class UserInDBBase(BaseModel):
    # DB 모델에서 데이터를 읽어와 API 응답 형태로 변환하기 위한 기본 스키마
    id: Optional[int] = None
    email: EmailStr
    full_name: Optional[str]
    gender: Optional[str]
    is_terms_agreed: bool
    is_privacy_agreed: bool
    
    created_at: datetime

    # Pydantic 모델로 변환할 수 있도록 허용
    class Config:
        from_attributes = True 

# UserResponse: API 응답 (POST /register 성공 시)
class UserResponse(UserInDBBase):
    # UserInDBBase를 상속받아 안전하게 비밀번호 필드를 제외한 정보만 반환
    pass

# 6. Token 스키마 (로그인 응답 시 사용)
class Token(BaseModel):

    access_token: str
    token_type: str = "bearer"
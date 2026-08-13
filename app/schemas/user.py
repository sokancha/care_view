

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class BaseUser(BaseModel):

    email: EmailStr = Field(..., description="사용자 이메일 (로그인 ID)")

    password: str = Field(..., min_length=8, description="비밀번호 (최소 8자)")
    
    full_name: Optional[str] = Field(None, description="사용자 이름")
    gender: Optional[str] = Field(None, description="성별 ('male', 'female', 'other' 등)")
    
    is_terms_agreed: bool = Field(False, description="이용약관 동의 여부 (필수)")
    is_privacy_agreed: bool = Field(False, description="개인정보 처리방침 동의 여부 (필수)")

class UserCreate(BaseUser):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInDBBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    full_name: Optional[str]
    gender: Optional[str]
    is_terms_agreed: bool
    is_privacy_agreed: bool
    
    created_at: datetime

    class Config:
        from_attributes = True 

class UserResponse(UserInDBBase):

    pass

class Token(BaseModel):

    access_token: str
    token_type: str = "bearer"

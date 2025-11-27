#클라이언트 요청을 받아 처리하는 라우터를 정의

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.api.dependencies import get_current_user
from app.services import user_crud
from app.core.security import verify_password, create_access_token
from app.models.user import User

# APIRouter 객체 생성
router = APIRouter(prefix="/api/user", tags=["Users"])

# 회원가입 엔드포인트
@router.post(
    "/register", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):

    # 이메일 중복 확인
    db_user = user_crud.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이메일이 이미 등록되어 있습니다."
        )
    
    # 사용자 생성 (비밀번호 해시 포함)
    new_user = user_crud.create_user(db=db, user=user_data)
    
    return new_user

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_for_access_token(
    user_data: UserLogin, # 🚨 JSON Body를 받습니다.
    db: Session = Depends(get_db)
):
    
    # DB에서 사용자 조회
    user: User | None = user_crud.get_user_by_email(db, email=user_data.email)
    
    # 사용자 존재 및 비밀번호 검증
    if user is None or not verify_password(user_data.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이메일 또는 비밀번호가 잘못되었습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 액세스 토큰 생성
    access_token = create_access_token(
        subject=user.id 
    )
    
    # 토큰 반환
    return {"access_token": access_token, "token_type": "bearer"}


# 현재 사용자 정보 조회(토큰 필요) 엔드포인트
@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(get_current_user)
):
    # 인증된 JWT 토큰을 사용하여 현재 로그인한 사용자 정보를 반환
    return current_user

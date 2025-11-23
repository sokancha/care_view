# FastAPI의 핵심 의존성 로직을 정의 -> 라우터 간에 재사용 ㅇ

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import decode_token
from app.services import user_crud
from app.core.database import get_db
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    # HTTP Bearer 토큰을 검증하고, 현재 로그인된 사용자 객체를 반환

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # 사용자 ID (sub) 추출
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # DB에서 사용자 ID로 사용자 객체 조회
    user = user_crud.get_user_by_id(db, user_id=user_id) 
    
    if user is None:
        raise credentials_exception
        
    return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


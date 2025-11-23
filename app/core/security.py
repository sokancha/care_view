# 보안 로직 : 비밀번호 해시/검증, JWT 토큰 생성/디코딩 등 핵심 보안 함수

from datetime import datetime, timedelta, timezone
from typing import Any
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import settings

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


# 비밀번호 검증 (로그인 시 사용)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 일반 텍스트 비밀번호와 해시된 비밀번호를 비교
    return pwd_context.verify(plain_password, hashed_password)

# JWT 토큰 생성
def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 토큰에 포함될 데이터 (payload)
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # JWT 인코딩
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# 3. 토큰 디코딩
def decode_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        print(f"Token decoding failed (Key/Algorithm/Expiry mismatch): {e}")
        return None
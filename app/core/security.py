# 보안 로직 : 비밀번호 해시/검증, JWT 토큰 생성/디코딩 등 핵심 보안 함수

from datetime import datetime, timedelta, timezone
from typing import Any
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import settings

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

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

# app/core/config.py

from pydantic_settings import BaseSettings 
from typing import Final 
import os 

class Settings(BaseSettings):

    # 🚨 수정: DATABASE_URL의 하드코딩된 기본값을 제거했습니다.
    # 이제 이 값은 Pydantic에 의해 환경 변수(DATABASE_URL)에서 필수로 로드됩니다.
    DATABASE_URL: str = ""
    
    # 보안 키 (JWT 토큰 생성에 사용)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "_DFDTWqmwznAiJLte696DXnBbsxAP6_AKaKUqpxXCefwMRMY6UVjeA")

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    
    class Config:
        env_file = ".env" 

settings: Final[Settings] = Settings()

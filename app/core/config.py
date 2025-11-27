# 애플리케이션 설정 : DB URL, SECRET_KEY, JWT 만료 시간 등 환경 변수와 상수

from pydantic_settings import BaseSettings
from typing import Final
import os

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql://postgres:awrdezcqe1324!@db:5432/careview_db"
    # 보안 키 (JWT 토큰 생성에 사용)

    SECRET_KEY: str = os.getenv("SECRET_KEY", "_DFDTWqmwznAiJLte696DXnBbsxAP6_AKaKUqpxXCefwMRMY6UVjeA")

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

   

    class Config:

        env_file = ".env"



settings: Final[Settings] = Settings()
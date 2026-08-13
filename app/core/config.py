# app/core/config.py

from pydantic_settings import BaseSettings 
from typing import Final 
import os 

class Settings(BaseSettings):

    DATABASE_URL: str = ""
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "_DFDTWqmwznAiJLte696DXnBbsxAP6_AKaKUqpxXCefwMRMY6UVjeA")

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    
    class Config:
        env_file = ".env" 

settings: Final[Settings] = Settings()

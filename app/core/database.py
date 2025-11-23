# app/core/database.py


# DB 연결 관리 : SQLAlchemy 엔진 생성 등
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🚨 중요: Docker Compose 내부 통신 HOST는 'db'
# '********' 부분은 실제 POSTGRES_PASSWORD 값으로 대체해야 합니다.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:awrdezcqe1324!@db:5432/careview_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False
)

# 모든 모델이 상속받을 기본 클래스
Base = declarative_base()

# FastAPI 의존성 주입을 위한 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
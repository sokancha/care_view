# DB 연결 관리 : SQLAlchemy 엔진 생성 등
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

def create_tables(engine):
    """DB 엔진을 사용하여 Base에 정의된 모든 테이블을 생성합니다."""
    # 모든 모델 클래스(User, Allergy 등)를 포함하는 Base.metadata를 사용합니다.
    Base.metadata.create_all(bind=engine)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker # type: ignore
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
from typing import Tuple

# 모든 모델이 상속받을 기본 클래스 (기존 Base와 동일)
Base = declarative_base()

# 비동기 엔진과 세션 팩토리를 생성하는 함수
def get_async_engine(db_url: str) -> Tuple[Engine, async_sessionmaker[AsyncSession]]:
    """
    주어진 URL로 비동기 PostgreSQL 엔진과 세션 팩토리를 생성합니다.
    """
    # PostgreSQL 비동기 드라이버 (asyncpg) 사용을 위해 URL을 수정합니다.
    # 예: postgresql+asyncpg://user:password@host/dbname
    async_db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

    # 비동기 엔진 생성
    async_engine = create_async_engine(
        async_db_url,
        echo=False,  # SQL 쿼리를 출력하지 않음
        pool_pre_ping=True
    )

    # 비동기 세션 팩토리 생성
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    return async_engine, AsyncSessionLocal
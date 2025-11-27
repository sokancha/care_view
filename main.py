from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore 
from contextlib import asynccontextmanager
import os
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from typing import AsyncGenerator

from app.core.config import settings
from app.api.endpoints import user as user_api
from app.api.endpoints import onboarding as onboarding_api
from app.api.endpoints import main_page as main_page_api
from app.api.endpoints import record as record_api
# Pylance 오류 무시: db_session 파일을 루트에서 찾을 수 없을 때 발생합니다.
from app.core.db_session import get_async_engine, Base 

async_engine = None
AsyncSessionLocal = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 시작 시 DB 연결 설정 및 테이블 생성(마이그레이션)을 수행합니다.
    종료 시 DB 연결을 정리합니다.
    """
    global async_engine, AsyncSessionLocal
    
    # DB 연결 정보는 환경 변수에서 로드됩니다.
    # AWS ECS 환경에서 이 환경 변수를 주입할 예정입니다.
    DB_URL = os.environ.get("DATABASE_URL")

    if not DB_URL:
        # 배포 환경에서는 반드시 환경 변수가 설정되어야 합니다.
        raise RuntimeError("DATABASE_URL 환경 변수가 필요합니다. AWS ECS에서 설정해야 합니다.")

    # 비동기 엔진 및 세션 팩토리 초기화
    # get_async_engine은 (엔진, 세션 팩토리) 튜플을 반환합니다.
    async_engine, AsyncSessionLocal = get_async_engine(DB_URL) # type: ignore
    
    print("데이터베이스 비동기 연결 설정 완료.")

    # 서버 시작 시, DB 스키마(테이블) 자동 생성/마이그레이션 실행
    async with async_engine.begin() as conn:
        print("데이터베이스 테이블 생성(마이그레이션) 시작...")
        # Base.metadata.create_all은 동기 함수이므로 run_sync로 실행합니다.
        await conn.run_sync(Base.metadata.create_all) 
        print("데이터베이스 테이블 생성 완료.")

    # 서버 시작
    yield
    
    # 서버 종료 시 엔진 연결 정리
    if async_engine:
        await async_engine.dispose() # type: ignore
    print("애플리케이션 종료 작업 완료.")

# ------------------------------------------------------------
# 4. FastAPI 애플리케이션 인스턴스 생성
# ------------------------------------------------------------

app = FastAPI(
    title="CareView API",
    version="v1",
    description="로그인, 회원가입, 일정 관리 등을 위한 API",
    lifespan=lifespan # 라이프사이클 관리 함수 적용
)

# ------------------------------------------------------------
# 5. DB 세션 의존성 주입 함수
# ------------------------------------------------------------

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    비동기 DB 세션을 제공하는 의존성 주입 함수입니다.
    """
    if AsyncSessionLocal is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    try:
        # AsyncSessionLocal을 사용하여 비동기 세션 생성
        async with AsyncSessionLocal() as session: # type: ignore
            yield session
    finally:
        pass 

# ------------------------------------------------------------
# 6. 라우터 포함 (API 엔드포인트)
# ------------------------------------------------------------

# 사용자 API 라우터 연결 (기존 app/main.py 로직)
app.include_router(user_api.router, tags=["Users"])
app.include_router(onboarding_api.router, tags=["Onboarding"])
app.include_router(record_api.router, tags=["Record"])
app.include_router(main_page_api.router, tags=["Main Page"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to CareView API V1"}

# 헬스 체크 엔드포인트 추가 (DB 연결 확인용)
@app.get("/health", tags=["Root"])
async def health_check(db: AsyncSession = Depends(get_async_db)):
    """
    DB 연결 상태를 포함한 헬스 체크 엔드포인트입니다.
    """
    try:
        # 간단한 쿼리로 DB 연결 확인
        await db.execute("SELECT 1")
        return {"status": "ok", "db_connection": "successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB Connection Failed: {e}")

# ------------------------------------------------------------
# 7. OpenAPI (Swagger) 커스텀 설정
# ------------------------------------------------------------

def custom_openapi():
    # 기존 app/main.py의 커스텀 OpenAPI 로직을 그대로 사용
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # "BearerAuth"라는 이름으로 HTTP Bearer 스키마를 정의
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer", 
            "bearerFormat": "JWT"
        }
    }
    
    security_requirement = [{"BearerAuth": []}]
    for route in openapi_schema["paths"].values():
        for method in route.values():
            tags = method.get('tags', [])
            # 인증이 필요한 모든 태그에 보안 적용
            if tags and any(tag in ['Users', 'Onboarding', 'Record', 'Main Page'] for tag in tags):
                method["security"] = security_requirement

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# 앱 초기화 : FastAPI 인스턴스를 생성하고, 라우터를 연결, 미들웨어 및 OpenAPI 설정(Swagger UI)을 담당.
#from app.core.models.user import User  # 🚨 이전 경로 (주석 처리 또는 삭제)

# 🚨 수정! 🚨
# 이제 models 폴더는 core 안에 있으므로 경로를 'app.core.models'로 변경합니다.
from app.core.models.user import User  # User 모델을 임포트하여 DB 세션 등에 사용합니다.
from fastapi import FastAPI



app = FastAPI(title="CareView Health Dashboard API")
from fastapi import FastAPI
from app.api.endpoints import user as user_api
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="CareView API",
    version="v1",
    description="로그인, 회원가입, 일정 관리 등을 위한 API"
)

# 사용자 API 라우터 연결
app.include_router(
    user_api.router,
    tags=["Users"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to CareView API V1"}


def custom_openapi():
    # 스키마가 이미 생성되었으면 캐시된 것을 반환
    if app.openapi_schema:
        return app.openapi_schema
    
    # 기본 OpenAPI 스키마를 생성
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
            if method.get('tags') and 'Users' in method.get('tags', []):
                method["security"] = security_requirement

    # 커스터마이징된 스키마를 앱에 저장하고 반환
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# custom_openapi 함수를 FastAPI의 스웨거에 연결
app.openapi = custom_openapi
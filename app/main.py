from fastapi import FastAPI
from app.api.endpoints import user as user_api
from app.api.endpoints import onboarding as onboarding_api
from app.api.endpoints import record as record_api
from fastapi.openapi.utils import get_openapi
from app.api.endpoints import main_page as main_page_api
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import meals as meals_api
from app.api.endpoints import exercise
from app.api.endpoints import expected_effect

app = FastAPI(
    title="CareView API",
    version="v1",
    description="로그인, 회원가입, 일정 관리 등을 위한 API"
)

origins = [
    "http://localhost:3000",  
    "http://localhost:8000",
    "http://localhost:5173",
    "https://careview-front.onrender.com",
    "https://careview.kro.kr",
    "www.careview.kro.kr",
]
# 3. 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              
    allow_credentials=True,             
    allow_methods=["*"],                
    allow_headers=["*"],                
)

app.include_router(user_api.router, tags=["Users"])
app.include_router(onboarding_api.router, tags=["Onboarding"])
app.include_router(record_api.router, tags=["Record"])
app.include_router(main_page_api.router, tags=["Main Page"])
app.include_router(meals_api.router, tags=["meals"])
app.include_router(exercise.router, tags=["Exercise"])
app.include_router(expected_effect.router, tags=["Expected Effect"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CareView API V1"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
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
            if tags and any(tag in ['Users', 'Onboarding', 'Record', 'Main Page', 'meals', 'Exercise', 'Expected Effect'] for tag in tags):
                method["security"] = security_requirement

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/health", status_code=200, tags=["Health Check"])
def health_check():
    """
    Render 헬스 체크를 위한 엔드포인트.
    데이터베이스 연결 확인 등의 로직을 추가할 수도 있습니다.
    """
    return {"status": "ok", "message": "Server is running"}

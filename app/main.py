from fastapi import FastAPI
# from app.models.user import User  # 🚨 이전 경로 (주석 처리 또는 삭제)

# 🚨 수정! 🚨
# 이제 models 폴더는 core 안에 있으므로 경로를 'app.core.models'로 변경합니다.
from app.core.models.user import User  # User 모델을 임포트하여 DB 세션 등에 사용합니다.


app = FastAPI(title="CareView Health Dashboard API")

@app.get("/")
def read_root():
    return {"message": "CareView API is Running! (FastAPI + Docker)"}
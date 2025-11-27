from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.main_page import (
    MainPageResponse,
    UserBasicInfo,
    TodayMetrics,
    WeeklyTrends
)
from app.api.dependencies import get_current_user
from app.services import main_page_crud
from app.models.user import User

router = APIRouter(prefix="/api/main", tags=["Main Page"])


@router.get(
    "/dashboard",
    response_model=MainPageResponse,
    status_code=status.HTTP_200_OK,
    tags=["Main Page"]
)
def get_main_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    메인 페이지 대시보드 데이터 조회
    
    - 사용자 기본 정보 (이름, 나이, 키, BMI)
    - 오늘의 건강 지표 (몸무게, 운동시간, 수면시간)
    - 일주일 추이 데이터 (7일간 몸무게, 운동시간, 수면시간)
    """
    
    # 1. 사용자 기본 정보
    user_info = main_page_crud.get_user_basic_info(db, current_user.id) # type: ignore
    
    # 2. 오늘의 건강 지표
    today_metrics = main_page_crud.get_today_metrics(db, current_user.id) # type: ignore
    
    # 3. 일주일 추이 데이터
    weekly_trends = main_page_crud.get_weekly_trends(db, current_user.id) # type: ignore
    
    return MainPageResponse(
        user_info=UserBasicInfo(**user_info),
        today_metrics=TodayMetrics(**today_metrics),
        weekly_trends=WeeklyTrends(**weekly_trends)
    )

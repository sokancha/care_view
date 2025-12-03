from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.core.database import get_db
from app.schemas.record import (
    HealthMetricCreate,
    HealthMetricResponse,
    RecordPageResponse,
    WeeklyRecords,
    DailyRecord,
    WeeklySummary
)
from app.api.dependencies import get_current_user
from app.services import record_crud
from app.models.user import User

router = APIRouter(prefix="/api/record", tags=["Record"])

@router.post(
    "/metric",
    response_model=HealthMetricResponse,
    status_code=status.HTTP_200_OK,
    description="특정 날짜의 건강 기록을 생성하거나 수정합니다."
)
def save_health_record(
    metric_data: HealthMetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """건강 기록 저장 (Upsert)"""
    saved_metric = record_crud.upsert_health_metric(
        db=db,
        user_id=current_user.id, # type: ignore
        data=metric_data
    )
    
    # 전일 대비 변화량 계산
    weight_change = record_crud.calculate_weight_change(db, current_user.id, saved_metric) # type: ignore
    
    # DB 객체(saved_metric)의 recorded_at에서 날짜만 뽑아 .date 속성에 넣어줍니다.
    saved_metric.date = saved_metric.recorded_at.date()

    # 이제 Pydantic이 .date를 찾을 수 있어서 에러가 나지 않습니다.
    response = HealthMetricResponse.model_validate(saved_metric)
    response.weight_change = weight_change
    
    return response

@router.get(
    "/page",
    response_model=RecordPageResponse,
    status_code=status.HTTP_200_OK
)
def get_record_page(
    target_date: Optional[date] = Query(None, description="조회 기준 날짜 (YYYY-MM-DD). 미입력 시 오늘."),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    기록실 주간 뷰 데이터 조회.
    이전/다음 주 조회 시 프론트에서 target_date를 계산해서 요청하면 됩니다.
    """
    if target_date is None:
        target_date = date.today()
    
    # 1. 주간 기록 조회
    weekly_data = record_crud.get_weekly_records(db, current_user.id, target_date) # type: ignore
    
    # 2. 각 일자별 체중 변화량 주입
    processed_daily_records = []
    for day_data in weekly_data["daily_records"]:
        metric_obj = day_data["metric"]
        if metric_obj:
            # ⭐ [여기 수정] DB 객체(metric_obj)에 date 필드가 없어서 에러가 납니다.
            # 변환하기 전에 수동으로 넣어줘야 합니다!
            metric_obj.date = day_data["date"]
            
            metric_resp = HealthMetricResponse.model_validate(metric_obj)
            metric_resp.weight_change = record_crud.calculate_weight_change(db, current_user.id, metric_obj) # type: ignore
            day_data["metric"] = metric_resp
        
        processed_daily_records.append(DailyRecord(**day_data))

    # 3. 주간 요약 조회
    summary_data = record_crud.get_weekly_summary(db, current_user.id, target_date) # type: ignore
    
    return RecordPageResponse(
        current_year=target_date.year,
        current_month=target_date.month,
        weekly_records=WeeklyRecords(
            year=weekly_data["year"],
            week_number=weekly_data["week_number"],
            start_date=weekly_data["start_date"],
            end_date=weekly_data["end_date"],
            daily_records=processed_daily_records
        ),
        weekly_summary=WeeklySummary(**summary_data)
    )

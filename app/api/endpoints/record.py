from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
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
    
    # 미래 날짜 입력 방지
    if metric_data.date > date.today():
        raise HTTPException(
            status_code=400,
            detail="미래 날짜는 입력할 수 없습니다."
        )
    
    # 1년 이전 데이터 입력 방지 (선택사항)
    if metric_data.date < date.today() - timedelta(days=365):
        raise HTTPException(
            status_code=400,
            detail="1년 이전 데이터는 입력할 수 없습니다."
        )
    
    saved_metric = record_crud.upsert_health_metric(
        db=db,
        user_id=current_user.id,  # type: ignore
        data=metric_data
    )
    
    return HealthMetricResponse.model_validate(saved_metric)


@router.get(
    "/page",
    response_model=RecordPageResponse,
    status_code=status.HTTP_200_OK,
    description="기록실 주간 뷰 데이터 조회. target_date 미입력 시 오늘 날짜 기준."
)
def get_record_page(
    target_date: Optional[date] = Query(None, description="조회 기준 날짜 (YYYY-MM-DD)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """기록실 주간 뷰 데이터 조회"""
    if target_date is None:
        target_date = date.today()
    
    # 1. 주간 기록 조회
    weekly_data = record_crud.get_weekly_records(db, current_user.id, target_date)  # type: ignore
    
    # 2. 각 일자별 데이터 처리
    processed_daily_records = []
    for day_data in weekly_data["daily_records"]:
        metric_obj = day_data["metric"]
        
        if metric_obj:
            metric_resp = HealthMetricResponse.model_validate(metric_obj)
            day_data["metric"] = metric_resp
        
        processed_daily_records.append(DailyRecord(**day_data))

    # 3. 주간 요약 조회
    summary_data = record_crud.get_weekly_summary(db, current_user.id, target_date)  # type: ignore
    
    return RecordPageResponse(
        weekly_records=WeeklyRecords(
            start_date=weekly_data["start_date"],
            end_date=weekly_data["end_date"],
            daily_records=processed_daily_records
        ),
        weekly_summary=WeeklySummary(**summary_data)
    )

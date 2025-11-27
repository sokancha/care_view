from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.schemas.record import (
    HealthMetricCreate,
    HealthMetricUpdate,
    HealthMetricResponse,
    WeeklyRecords,
    WeeklySummary,
    RecordPageResponse,
    DailyRecord
)
from app.api.dependencies import get_current_user
from app.services import record_crud
from app.models.user import User

router = APIRouter(prefix="/api/record", tags=["Record"])


# ==================== 건강 기록 CRUD ====================

@router.post(
    "/metric",
    response_model=HealthMetricResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Record"]
)
def create_health_record(
    metric_data: HealthMetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """새 건강 기록 추가 (+ 버튼)"""
    new_metric = record_crud.create_health_metric(
        db=db,
        user_id=current_user.id, # type: ignore
        weight_kg=metric_data.weight_kg,
        sleep_duration_hours=metric_data.sleep_duration_hours,
        exercise_duration_hours=metric_data.exercise_duration_hours,
        recorded_at=metric_data.recorded_at
    )
    
    # 전일 대비 체중 변화 계산
    weight_change = record_crud.calculate_weight_change(db, current_user.id, new_metric) # type: ignore
    
    response = HealthMetricResponse.model_validate(new_metric)
    response.weight_change = weight_change
    
    return response


@router.get(
    "/metric/{metric_id}",
    response_model=HealthMetricResponse,
    status_code=status.HTTP_200_OK,
    tags=["Record"]
)
def get_health_record_detail(
    metric_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """특정 건강 기록 상세 조회"""
    metric = record_crud.get_health_metric_by_id(db, metric_id, current_user.id) # type: ignore
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="기록을 찾을 수 없습니다."
        )
    
    weight_change = record_crud.calculate_weight_change(db, current_user.id, metric) # type: ignore
    
    response = HealthMetricResponse.model_validate(metric)
    response.weight_change = weight_change
    
    return response


@router.put(
    "/metric/{metric_id}",
    response_model=HealthMetricResponse,
    status_code=status.HTTP_200_OK,
    tags=["Record"]
)
def update_health_record(
    metric_id: int,
    metric_data: HealthMetricUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """건강 기록 수정"""
    metric = record_crud.get_health_metric_by_id(db, metric_id, current_user.id) # type: ignore
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="기록을 찾을 수 없습니다."
        )
    
    updated_metric = record_crud.update_health_metric(
        db=db,
        metric=metric,
        weight_kg=metric_data.weight_kg,
        sleep_duration_hours=metric_data.sleep_duration_hours,
        exercise_duration_hours=metric_data.exercise_duration_hours,
        recorded_at=metric_data.recorded_at
    )
    
    weight_change = record_crud.calculate_weight_change(db, current_user.id, updated_metric) # type: ignore
    
    response = HealthMetricResponse.model_validate(updated_metric)
    response.weight_change = weight_change
    
    return response


# ==================== 기록실 페이지 (주간 뷰) ====================

@router.get(
    "/page",
    response_model=RecordPageResponse,
    status_code=status.HTTP_200_OK,
    tags=["Record"]
)
def get_record_page(
    target_date: Optional[date] = Query(None, description="조회할 날짜 (기본: 오늘, 해당 날짜가 속한 주를 조회)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    기록실 페이지 전체 데이터 조회
    - 일주일 단위 기록 (월~일)
    - 이번 주 요약 (최신 체중, 전일 대비 변화, 총 운동시간, 운동일수, 총 수면시간)
    """
    if target_date is None:
        target_date = date.today()
    
    # 주간 기록
    weekly_records_data = record_crud.get_weekly_records(db, current_user.id, target_date) # type: ignore
    
    # 각 기록에 전일 대비 체중 변화 추가
    for daily_record in weekly_records_data["daily_records"]:
        for metric in daily_record["metrics"]:
            metric.weight_change = record_crud.calculate_weight_change(db, current_user.id, metric) # type: ignore
    
    # 주간 요약
    weekly_summary_data = record_crud.get_weekly_summary(db, current_user.id, target_date) # type: ignore
    
    return RecordPageResponse(
        current_year=target_date.year,
        current_month=target_date.month,
        weekly_records=WeeklyRecords(
            year=weekly_records_data["year"],
            week_number=weekly_records_data["week_number"],
            start_date=weekly_records_data["start_date"],
            end_date=weekly_records_data["end_date"],
            daily_records=[DailyRecord(**day) for day in weekly_records_data["daily_records"]]
        ),
        weekly_summary=WeeklySummary(**weekly_summary_data)
    )
    
# ==================== 주 네비게이션 ====================

@router.get(
    "/week/previous",
    response_model=RecordPageResponse,
    status_code=status.HTTP_200_OK,
    tags=["Record"]
)
def get_previous_week(
    current_year: int = Query(..., description="현재 연도"),
    current_month: int = Query(..., description="현재 월"),
    current_date: date = Query(..., description="현재 조회 중인 날짜"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """이전 주로 이동 (왼쪽 화살표) - 7일 전 주 표시"""
    # 7일 전 날짜 계산
    previous_week_date = current_date - timedelta(days=7)
    
    # 주간 기록
    weekly_records_data = record_crud.get_weekly_records(db, current_user.id, previous_week_date) # type: ignore
    
    # 전일 대비 체중 변화 추가
    for daily_record in weekly_records_data["daily_records"]:
        for metric in daily_record["metrics"]:
            metric.weight_change = record_crud.calculate_weight_change(db, current_user.id, metric) # type: ignore
    
    # 주간 요약
    weekly_summary_data = record_crud.get_weekly_summary(db, current_user.id, previous_week_date) # type: ignore
    
    # 이전 주의 연도/월 계산 (해당 주의 시작일 기준)
    prev_year = weekly_records_data["start_date"].year
    prev_month = weekly_records_data["start_date"].month
    
    return RecordPageResponse(
        current_year=prev_year,
        current_month=prev_month,
        weekly_records=WeeklyRecords(
            year=weekly_records_data["year"],
            week_number=weekly_records_data["week_number"],
            start_date=weekly_records_data["start_date"],
            end_date=weekly_records_data["end_date"],
            daily_records=[DailyRecord(**day) for day in weekly_records_data["daily_records"]]
        ),
        weekly_summary=WeeklySummary(**weekly_summary_data)
    )


@router.get(
    "/week/next",
    response_model=RecordPageResponse,
    status_code=status.HTTP_200_OK,
    tags=["Record"]
)
def get_next_week(
    current_year: int = Query(..., description="현재 연도"),
    current_month: int = Query(..., description="현재 월"),
    current_date: date = Query(..., description="현재 조회 중인 날짜"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """다음 주로 이동 (오른쪽 화살표) - 7일 후 주 표시"""
    # 7일 후 날짜 계산
    next_week_date = current_date + timedelta(days=7)
    
    # 주간 기록
    weekly_records_data = record_crud.get_weekly_records(db, current_user.id, next_week_date) # type: ignore
    
    # 전일 대비 체중 변화 추가
    for daily_record in weekly_records_data["daily_records"]:
        for metric in daily_record["metrics"]:
            metric.weight_change = record_crud.calculate_weight_change(db, current_user.id, metric) # type: ignore
    
    # 주간 요약
    weekly_summary_data = record_crud.get_weekly_summary(db, current_user.id, next_week_date) # type: ignore
    
    # 다음 주의 연도/월 계산 (해당 주의 시작일 기준)
    next_year = weekly_records_data["start_date"].year
    next_month = weekly_records_data["start_date"].month
    
    return RecordPageResponse(
        current_year=next_year,
        current_month=next_month,
        weekly_records=WeeklyRecords(
            year=weekly_records_data["year"],
            week_number=weekly_records_data["week_number"],
            start_date=weekly_records_data["start_date"],
            end_date=weekly_records_data["end_date"],
            daily_records=[DailyRecord(**day) for day in weekly_records_data["daily_records"]]
        ),
        weekly_summary=WeeklySummary(**weekly_summary_data)
    )

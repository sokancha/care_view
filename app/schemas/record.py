from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


# ==================== 건강 기록 CRUD ====================

class HealthMetricCreate(BaseModel):
    """건강 기록 생성 요청"""
    weight_kg: float = Field(..., gt=0, lt=500, description="체중 (kg)")
    sleep_duration_hours: Optional[float] = Field(None, ge=0, le=24, description="수면 시간 (시간)")
    exercise_duration_hours: Optional[float] = Field(None, ge=0, description="운동 시간 (시간)")
    recorded_at: Optional[datetime] = Field(None, description="기록 시간 (기본값: 현재 시간)")

    class Config:
        json_schema_extra = {
            "example": {
                "weight_kg": 72.5,
                "sleep_duration_hours": 7.5,
                "exercise_duration_hours": 1.0,
                "recorded_at": "2025-11-05T09:00:00"
            }
        }


class HealthMetricUpdate(BaseModel):
    """건강 기록 수정 요청"""
    weight_kg: Optional[float] = Field(None, gt=0, lt=500)
    sleep_duration_hours: Optional[float] = Field(None, ge=0, le=24)
    exercise_duration_hours: Optional[float] = Field(None, ge=0)
    recorded_at: Optional[datetime] = None


class HealthMetricResponse(BaseModel):
    """건강 기록 응답"""
    id: int
    user_id: int
    weight_kg: float
    bmi: Optional[float] = None
    sleep_duration_hours: Optional[float] = None
    exercise_duration_hours: Optional[float] = None
    recorded_at: datetime
    weight_change: Optional[float] = Field(None, description="전일 대비 체중 변화 (kg)")

    class Config:
        from_attributes = True


# ==================== 주간 기록 ====================

class DailyRecord(BaseModel):
    """일별 기록 요약"""
    date: date
    metrics: List[HealthMetricResponse] = Field(default=[], description="해당 날짜의 모든 기록")
    latest_weight: Optional[float] = Field(None, description="해당 날짜 최신 체중")
    total_sleep: Optional[float] = Field(None, description="해당 날짜 총 수면 시간")
    total_exercise: Optional[float] = Field(None, description="해당 날짜 총 운동 시간")


class WeeklyRecords(BaseModel):
    """주간 기록 (7일)"""
    year: int
    week_number: int = Field(..., description="해당 연도의 몇 번째 주")
    start_date: date
    end_date: date
    daily_records: List[DailyRecord]


# ==================== 주간 요약 ====================

class WeeklySummary(BaseModel):
    """이번 주 요약"""
    latest_weight_kg: Optional[float] = Field(None, description="이번 주 최신 체중")
    weight_change_kg: Optional[float] = Field(None, description="이번 주 체중 변화 (시작 대비)")
    total_exercise_hours: float = Field(default=0, description="이번 주 총 운동 시간 (시간)")
    exercise_days_count: int = Field(default=0, description="이번 주 운동한 일수")
    total_sleep_hours: float = Field(default=0, description="이번 주 총 수면 시간 (시간)")
    average_sleep_hours: Optional[float] = Field(None, description="이번 주 평균 수면 시간")


# ==================== 기록실 페이지 전체 응답 ====================

class RecordPageResponse(BaseModel):
    """기록실 페이지 전체 데이터"""
    current_year: int
    current_month: int
    weekly_records: WeeklyRecords
    weekly_summary: WeeklySummary
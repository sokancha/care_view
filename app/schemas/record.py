from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date as DateType

class HealthMetricCreate(BaseModel):
    """건강 기록 생성/수정 요청"""
    date: DateType = Field(..., description="기록할 날짜 (필수)") 
    weight_kg: Optional[float] = Field(None, gt=0, lt=500, description="체중 (kg)")
    sleep_duration_hours: Optional[float] = Field(None, ge=0, le=24, description="수면 시간")
    exercise_duration_hours: Optional[float] = Field(None, ge=0, description="운동 시간")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-11-05",
                "weight_kg": 72.5,
                "sleep_duration_hours": 7.5,
                "exercise_duration_hours": 1.0
            }
        }

class HealthMetricResponse(BaseModel):
    """건강 기록 응답 (간소화)"""
    id: int
    user_id: int
    weight_kg: Optional[float]
    sleep_duration_hours: Optional[float]
    exercise_duration_hours: Optional[float]

    class Config:
        from_attributes = True

class DailyRecord(BaseModel):
    """일별 기록"""
    date: DateType
    metric: Optional[HealthMetricResponse] = Field(None, description="해당 날짜의 기록")

class WeeklyRecords(BaseModel):
    """주간 기록"""
    start_date: DateType
    end_date: DateType
    daily_records: List[DailyRecord]

class WeeklySummary(BaseModel):
    """주간 요약"""
    latest_weight_kg: Optional[float] = Field(None, description="이번 주 최신 체중")
    total_exercise_hours: float = Field(..., description="이번 주 총 운동 시간")
    total_sleep_hours: float = Field(..., description="이번 주 총 수면 시간")

class RecordPageResponse(BaseModel):
    """기록실 페이지 응답 (간소화)"""
    weekly_records: WeeklyRecords
    weekly_summary: WeeklySummary

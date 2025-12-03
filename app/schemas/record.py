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
    id: int
    user_id: int
    date: DateType
    weight_kg: Optional[float]
    bmi: Optional[float]
    sleep_duration_hours: Optional[float]
    exercise_duration_hours: Optional[float]
    weight_change: Optional[float] = Field(None, description="전일 대비 체중 변화")

    class Config:
        from_attributes = True

class DailyRecord(BaseModel):
    date: DateType
    metric: Optional[HealthMetricResponse] = Field(None, description="해당 날짜의 기록")

class WeeklyRecords(BaseModel):
    year: int
    week_number: int
    start_date: DateType
    end_date: DateType
    daily_records: List[DailyRecord]

class WeeklySummary(BaseModel):
    latest_weight_kg: Optional[float]
    weight_change_kg: Optional[float]
    total_exercise_hours: float
    total_sleep_hours: float

class RecordPageResponse(BaseModel):
    current_year: int
    current_month: int
    weekly_records: WeeklyRecords
    weekly_summary: WeeklySummary

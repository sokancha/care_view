from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import date

class WorkoutTimeSlot(BaseModel):
    start_time: Optional[str] = Field(None, description="운동 시작 시간 (30분 단위, 예: '09:00'). 운동하지 않는 경우 None")
    end_time: Optional[str] = Field(None, description="운동 종료 시간 (30분 단위, 예: '10:30'). 운동하지 않는 경우 None")

# Step 1: 운동 목적 선택
class OnboardingStep1(BaseModel):
    """온보딩 1단계 - 운동 목적 선택"""
    goal: str = Field(..., description="운동 목적: 'fat_loss' (체지방 감소) 또는 'muscle_gain' (근육량 증가)")

    class Config:
        json_schema_extra = {
            "example": {
                "goal": "fat_loss"
            }
        }


# Step 2: 주간 운동 스케줄
class OnboardingStep2(BaseModel):
    """온보딩 2단계 - 요일별 운동 가능 시간"""
    weekly_workout_schedule: Dict[str, WorkoutTimeSlot] = Field(
        ..., 
        description="요일별 운동 시작 및 종료 시간"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "weekly_workout_schedule": {
                    "monday": {"start_time": "09:00", "end_time": "10:30"},
                    "tuesday": {"start_time": "10:30", "end_time": "12:00"},
                    "wednesday": {"start_time": None, "end_time": None}, # 운동 안 함
                    "thursday": {"start_time": "14:00", "end_time": "15:00"},
                    "friday": {"start_time": "18:00", "end_time": "19:30"},
                    "saturday": {"start_time": "10:00", "end_time": "12:00"},
                    "sunday": {"start_time": None, "end_time": None}
                }
            }
        }


# Step 3: 기본 정보 및 알레르기
class OnboardingStep3(BaseModel):
    """온보딩 3단계 - 기본 정보 및 알레르기"""
    date_of_birth: date = Field(..., description="생년월일 (YYYY-MM-DD)")
    height_cm: float = Field(..., gt=0, lt=300, description="신장 (cm)")
    current_weight_kg: float = Field(..., gt=0, lt=500, description="현재 체중 (kg)")
    allergy_ids: List[int] = Field(default=[], description="선택된 알레르기 ID 목록")

    class Config:
        json_schema_extra = {
            "example": {
                "date_of_birth": "2000-01-01",
                "height_cm": 175.5,
                "current_weight_kg": 70.0,
                "allergy_ids": [1, 3, 5]
            }
        }


# Step 4: 직업 선택
class OnboardingStep4(BaseModel):
    """온보딩 4단계 - 직업 선택"""
    job_type: str = Field(..., description="직업 유형: 'student' (학생) 또는 'worker' (직장인)")

    class Config:
        json_schema_extra = {
            "example": {
                "job_type": "student"
            }
        }


# Step 5: 온보딩 완료
class OnboardingStep5(BaseModel):
    """온보딩 5단계 - 시작하기"""
    is_onboarding_complete: bool = Field(default=True, description="온보딩 완료 여부")

    class Config:
        json_schema_extra = {
            "example": {
                "is_onboarding_complete": True
            }
        }



# 온보딩 설정 응답 스키마
class OnboardingConfigResponse(BaseModel):
    """온보딩 설정 조회 응답"""
    id: int
    user_id: int
    goal: Optional[str] = None
    weekly_workout_schedule: Optional[str] = None
    date_of_birth: Optional[date] = None
    height_cm: Optional[float] = None
    current_weight_kg: Optional[float] = None
    job_type: Optional[str] = None
    is_onboarding_complete: bool = False

    class Config:
        from_attributes = True
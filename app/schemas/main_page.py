from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date as date_type  # ⬅️ 별칭 사용


# ==================== 사용자 기본 정보 ====================

class UserBasicInfo(BaseModel):
    """사용자 기본 정보 (왼쪽 프로필)"""
    full_name: Optional[str] = Field(None, description="이름")
    age: Optional[int] = Field(None, description="나이")
    height_cm: Optional[float] = Field(None, description="신장 (cm)")
    bmi: Optional[float] = Field(None, description="최신 BMI")


# ==================== 오늘 데이터 ====================

class TodayMetrics(BaseModel):
    """오늘의 건강 지표"""
    weight_kg: Optional[float] = Field(None, description="오늘 몸무게 (kg)")
    exercise_hours: Optional[float] = Field(None, description="오늘 총 운동시간 (시간)")
    sleep_hours: Optional[float] = Field(None, description="오늘 수면시간 (시간)")


# ==================== 일주일 추이 데이터 ====================

class DailyTrend(BaseModel):
    """일별 추이 데이터"""
    date: date_type = Field(..., description="날짜")  # ⬅️ date_type 사용
    value: Optional[float] = Field(None, description="측정값")


class WeeklyTrends(BaseModel):
    """일주일 추이 데이터 (그래프용)"""
    weight_trend: List[DailyTrend] = Field(default=[], description="7일간 몸무게 추이")
    exercise_trend: List[DailyTrend] = Field(default=[], description="7일간 운동시간 추이")
    sleep_trend: List[DailyTrend] = Field(default=[], description="7일간 수면시간 추이")


# ==================== 메인 페이지 전체 응답 ====================

class MainPageResponse(BaseModel):
    """메인 페이지 전체 데이터"""
    user_info: UserBasicInfo
    today_metrics: TodayMetrics
    weekly_trends: WeeklyTrends

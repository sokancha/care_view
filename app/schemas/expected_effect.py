from pydantic import BaseModel, Field
from typing import List

class WeeklyPrediction(BaseModel):
    """주차별 예측 데이터"""
    week: int = Field(..., description="주차 (1~4)")
    predicted_weight: float = Field(..., description="예상 체중 (kg)")
    predicted_bmi: float = Field(..., description="예상 BMI")

class ExpectedEffectResponse(BaseModel):
    """기대 효과 응답 (최적화 버전)"""
    # 현재 상태
    current_weight: float = Field(..., description="현재 체중 (kg)")
    current_bmi: float = Field(..., description="현재 BMI")
    
    # 총 운동시간 (기존 변수명 유지)
    total_exercise_minutes: float = Field(..., description="오늘까지 총 운동시간 (분)")
    
    # 주차별 데이터 (기존 변수명 유지)
    weekly_predictions: List[WeeklyPrediction] = Field(..., description="주차별 체중/BMI 예측")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "current_weight": 70.5,
                "current_bmi": 23.5,
                "total_exercise_minutes": 960.0,
                "weekly_predictions": [
                    {"week": 1, "predicted_weight": 69.9, "predicted_bmi": 23.3},
                    {"week": 2, "predicted_weight": 69.3, "predicted_bmi": 23.1},
                    {"week": 3, "predicted_weight": 68.6, "predicted_bmi": 22.9},
                    {"week": 4, "predicted_weight": 68.0, "predicted_bmi": 22.7}
                ]
            }
        }
    }

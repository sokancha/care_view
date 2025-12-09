from pydantic import BaseModel, Field
from typing import List

class WeeklyPrediction(BaseModel):
    """주차별 예측 데이터"""
    week: int = Field(..., description="주차 (1~4)")
    predicted_weight: float = Field(..., description="예상 체중 (kg)")
    predicted_bmi: float = Field(..., description="예상 BMI")


class ExpectedEffectResponse(BaseModel):
    """기대 효과 페이지 응답"""
    # 현재 상태
    current_weight: float = Field(..., description="현재 체중 (kg)")
    current_bmi: float = Field(..., description="현재 BMI")
    
    # 4주 후 예측
    predicted_weight_4weeks: float = Field(..., description="4주 후 예상 체중 (kg)")
    predicted_bmi_4weeks: float = Field(..., description="4주 후 예상 BMI")
    weight_change_4weeks: float = Field(..., description="4주간 예상 체중 변화 (kg, 양수면 감량)")
    bmi_change_4weeks: float = Field(..., description="4주간 예상 BMI 변화")
    
    # 총 운동시간
    total_exercise_minutes: float = Field(..., description="오늘까지 총 운동시간 (분)")
    
    # 주차별 예측 그래프 데이터
    weekly_predictions: List[WeeklyPrediction] = Field(..., description="주차별 체중/BMI 예측")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "current_weight": 70.5,
                "current_bmi": 23.5,
                "predicted_weight_4weeks": 68.0,
                "predicted_bmi_4weeks": 22.7,
                "weight_change_4weeks": 2.5,
                "total_exercise_hours": 16.0,
                "weekly_predictions": [
                    {"week": 1, "predicted_weight": 69.9, "predicted_bmi": 23.3},
                    {"week": 2, "predicted_weight": 69.3, "predicted_bmi": 23.1},
                    {"week": 3, "predicted_weight": 68.6, "predicted_bmi": 22.9},
                    {"week": 4, "predicted_weight": 68.0, "predicted_bmi": 22.7}
                ]
            }
        }
    }

from pydantic import BaseModel, Field
from typing import List

class ExerciseItem(BaseModel):
    """개별 운동 정보"""
    movement_name: str = Field(description="운동 이름")
    step_name: str = Field(description="운동 단계 (준비운동/본운동/마무리운동)")
    duration_min: int = Field(description="소요 시간 (분)")
    calorie_kcal: int = Field(description="소모 칼로리 (kcal)")

    class Config:
        from_attributes = True


class ExerciseSet(BaseModel):
    """시간대별 운동 세트 (아침/점심/저녁)"""
    exercises: List[ExerciseItem] = Field(description="운동 구성 (준비+본+마무리)")
    total_duration_min: int = Field(description="세트 총 소요시간")
    total_calorie_kcal: int = Field(description="세트 총 칼로리")


class ExerciseRecommendationResponse(BaseModel):
    """운동 추천 전체 응답"""
    morning: ExerciseSet = Field(description="아침 운동")
    lunch: ExerciseSet = Field(description="점심 운동")
    dinner: ExerciseSet = Field(description="저녁 운동")
    
    total_duration_min: int = Field(description="하루 총 운동시간")
    total_calorie_kcal: int = Field(description="하루 총 칼로리 소모")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "morning": {
                    "exercises": [
                        {
                            "movement_name": "동적 스트레칭",
                            "step_name": "준비운동",
                            "duration_min": 10,
                            "calorie_kcal": 50
                        },
                        {
                            "movement_name": "빠르게 걷기",
                            "step_name": "본운동",
                            "duration_min": 30,
                            "calorie_kcal": 150
                        },
                        {
                            "movement_name": "정적 스트레칭",
                            "step_name": "마무리운동",
                            "duration_min": 5,
                            "calorie_kcal": 20
                        }
                    ],
                    "total_duration_min": 45,
                    "total_calorie_kcal": 220
                },
                "lunch": {
                    "exercises": [],
                    "total_duration_min": 30,
                    "total_calorie_kcal": 180
                },
                "dinner": {
                    "exercises": [],
                    "total_duration_min": 25,
                    "total_calorie_kcal": 160
                },
                "total_duration_min": 100,
                "total_calorie_kcal": 560
            }
        }
    }

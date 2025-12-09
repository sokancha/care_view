from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List

from app.models.main_health_metric import HealthMetric


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """BMI 계산"""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def get_total_exercise_minutes(db: Session, user_id: int) -> float:
    """오늘까지 총 운동시간 계산 (분 단위)"""
    total_hours = db.query(
        func.sum(HealthMetric.exercise_duration_hours)
    ).filter(
        HealthMetric.user_id == user_id,
        HealthMetric.exercise_duration_hours.isnot(None)
    ).scalar()
    
    # 시간을 분으로 변환
    total_minutes = (total_hours or 0.0) * 60
    return round(total_minutes, 1)


def predict_weight_change(
    db: Session,
    user_id: int,
    current_weight: float,
    daily_calorie_burn: float
) -> Dict:
    """
    4주 후 체중 변화 예측 (로직 유지)
    """
    # 기본 칼로리 계산 (1kg 감량 = 7,700 kcal)
    CALORIES_PER_KG = 7700
    
    # 주당 체중 감량 (kg)
    weekly_weight_loss = (daily_calorie_burn * 7) / CALORIES_PER_KG
    
    # 주차별 예측
    predictions = []
    for week in range(1, 5):
        predicted_weight = round(current_weight - (weekly_weight_loss * week), 1)
        predictions.append({
            "week": week,
            "predicted_weight": predicted_weight
        })
    
    return {
        "weekly_weight_loss": weekly_weight_loss,
        "predictions": predictions
    }


def generate_expected_effect(
    db: Session,
    user_id: int,
    current_weight: float,
    height_cm: float,
    daily_calorie_burn: float
) -> Dict:
    """
    기대 효과 데이터 생성
    """
    
    # 1. 현재 BMI 계산
    current_bmi = calculate_bmi(current_weight, height_cm)
    
    # 2. 4주 후 체중 예측 계산 (로직 유지)
    prediction_data = predict_weight_change(
        db, user_id, current_weight, daily_calorie_burn
    )
    
    # 3. 주차별 BMI 계산 (로직 유지)
    weekly_predictions = []
    for pred in prediction_data["predictions"]:
        weekly_predictions.append({
            "week": pred["week"],
            "predicted_weight": pred["predicted_weight"],
            "predicted_bmi": calculate_bmi(pred["predicted_weight"], height_cm)
        })
    
    # 4. 총 운동시간 (분)
    total_exercise_minutes = get_total_exercise_minutes(db, user_id)
    
    # 5. 결과 반환 (수정됨: 중복 필드 제거, 필요한 데이터만 리턴)
    return {
        "current_weight": current_weight,
        "current_bmi": current_bmi,
        "total_exercise_minutes": total_exercise_minutes,
        "weekly_predictions": weekly_predictions
    }

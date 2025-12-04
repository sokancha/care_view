from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date, timedelta, time

from app.models.main_health_metric import HealthMetric
from app.models.onboarding import OnboardingConfig
from app.schemas.record import HealthMetricCreate

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """BMI 계산"""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def upsert_health_metric(db: Session, user_id: int, data: HealthMetricCreate) -> HealthMetric:
    """해당 날짜에 기록이 없으면 생성, 있으면 업데이트 (Upsert)"""
    target_start = datetime.combine(data.date, time.min)
    target_end = datetime.combine(data.date, time.max)
    
    existing_metric = db.query(HealthMetric).filter(
        and_(
            HealthMetric.user_id == user_id,
            HealthMetric.recorded_at >= target_start,
            HealthMetric.recorded_at <= target_end
        )
    ).first()

    config = db.query(OnboardingConfig).filter(OnboardingConfig.user_id == user_id).first()
    
    if existing_metric:
        # [Update] 기존 기록 업데이트
        if data.weight_kg is not None:
            existing_metric.weight_kg = data.weight_kg
            if config and config.height_cm:
                existing_metric.bmi = calculate_bmi(data.weight_kg, config.height_cm)
        
        if data.sleep_duration_hours is not None:
            existing_metric.sleep_duration_hours = data.sleep_duration_hours
            
        if data.exercise_duration_hours is not None:
            existing_metric.exercise_duration_hours = data.exercise_duration_hours
            
        db.commit()
        db.refresh(existing_metric)
        return existing_metric
    
    else:
        # [Create] 새 기록 생성
        bmi = None
        if data.weight_kg and config and config.height_cm:
            bmi = calculate_bmi(data.weight_kg, config.height_cm)
            
        record_time = datetime.combine(data.date, time(12, 0))
        
        new_metric = HealthMetric(
            user_id=user_id,
            weight_kg=data.weight_kg,
            bmi=bmi,
            sleep_duration_hours=data.sleep_duration_hours,
            exercise_duration_hours=data.exercise_duration_hours,
            recorded_at=record_time
        )
        db.add(new_metric)
        db.commit()
        db.refresh(new_metric)
        return new_metric


def get_weekly_records(db: Session, user_id: int, target_date: date) -> dict:
    """특정 날짜가 포함된 주의 기록 조회 (월~일)"""
    weekday = target_date.isoweekday()
    start_date = target_date - timedelta(days=weekday - 1)
    end_date = start_date + timedelta(days=6)
    
    metrics = db.query(HealthMetric).filter(
        and_(
            HealthMetric.user_id == user_id,
            HealthMetric.recorded_at >= datetime.combine(start_date, time.min),
            HealthMetric.recorded_at <= datetime.combine(end_date, time.max)
        )
    ).all()
    
    metrics_map = {m.recorded_at.date(): m for m in metrics}
    
    daily_records = []
    for i in range(7):
        current_day = start_date + timedelta(days=i)
        metric = metrics_map.get(current_day)
        
        daily_records.append({
            "date": current_day,
            "metric": metric
        })
        
    return {
        "start_date": start_date,
        "end_date": end_date,
        "daily_records": daily_records
    }


def get_weekly_summary(db: Session, user_id: int, target_date: date) -> dict:
    """
    이번 주 요약 정보 계산
    - 최신일의 체중
    - 총 운동 시간
    - 총 수면 시간
    """
    weekday = target_date.isoweekday()
    start_date = target_date - timedelta(days=weekday - 1)
    end_date = start_date + timedelta(days=6)
    
    metrics = db.query(HealthMetric).filter(
        and_(
            HealthMetric.user_id == user_id,
            HealthMetric.recorded_at >= datetime.combine(start_date, time.min),
            HealthMetric.recorded_at <= datetime.combine(end_date, time.max)
        )
    ).order_by(HealthMetric.recorded_at).all()
    
    if not metrics:
        return {
            "latest_weight_kg": None,
            "total_exercise_hours": 0.0,
            "total_sleep_hours": 0.0
        }
    
    # 최신일의 체중 (마지막부터 역순 탐색)
    latest_weight = None
    for metric in reversed(metrics):
        if metric.weight_kg is not None:
            latest_weight = metric.weight_kg
            break
    
    total_exercise = sum(m.exercise_duration_hours or 0.0 for m in metrics)
    total_sleep = sum(m.sleep_duration_hours or 0.0 for m in metrics)
    
    return {
        "latest_weight_kg": latest_weight,
        "total_exercise_hours": round(total_exercise, 1),
        "total_sleep_hours": round(total_sleep, 1)
    }

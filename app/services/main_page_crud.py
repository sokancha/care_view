from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date, timedelta
from typing import Optional
from app.models.user import User
from app.models.onboarding import OnboardingConfig
from app.models.main_health_metric import HealthMetric


# ==================== 사용자 기본 정보 ====================

def get_user_basic_info(db: Session, user_id: int) -> dict:
    """사용자 기본 정보 조회 (이름, 나이, 키, 최신 BMI)"""
    user = db.query(User).filter(User.id == user_id).first()
    config = db.query(OnboardingConfig).filter(OnboardingConfig.user_id == user_id).first()

    korean_age = None
    if config and config.date_of_birth:
        today = date.today()
        # 생일이 지났는지 여부는 상관없이 연도만 계산하고 +1
        korean_age = (today.year - config.date_of_birth.year) + 1
    
    # 최신 BMI 조회
    latest_metric = db.query(HealthMetric).filter(
        HealthMetric.user_id == user_id
    ).order_by(HealthMetric.recorded_at.desc()).first()
    
    return {
        "full_name": user.full_name if user else None,
        "age": korean_age,
        "height_cm": config.height_cm if config else None,
        "bmi": latest_metric.bmi if latest_metric else None
    }


# ==================== 오늘 데이터 ====================

def get_today_metrics(db: Session, user_id: int) -> dict:
    """오늘의 건강 지표 (몸무게, 운동시간, 수면시간)"""
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    # 오늘의 모든 기록 조회
    metrics = db.query(HealthMetric).filter(
        and_(
            HealthMetric.user_id == user_id,
            HealthMetric.recorded_at >= start_of_day,
            HealthMetric.recorded_at <= end_of_day
        )
    ).order_by(HealthMetric.recorded_at).all()
    
    if not metrics:
        return {
            "weight_kg": None,
            "exercise_hours": None,
            "sleep_hours": None
        }
    
    # 최신 몸무게
    latest_weight = metrics[-1].weight_kg
    
    # 오늘 총 운동시간 합계
    total_exercise = 0
    for metric in metrics:
        if metric.exercise_duration_hours:
            total_exercise += metric.exercise_duration_hours
    
    # 오늘 총 수면시간 합계
    total_sleep = 0
    for metric in metrics:
        if metric.sleep_duration_hours:
            total_sleep += metric.sleep_duration_hours
    
    return {
        "weight_kg": latest_weight,
        "exercise_hours": total_exercise if total_exercise > 0 else None,
        "sleep_hours": total_sleep if total_sleep > 0 else None
    }


# ==================== 일주일 추이 데이터 ====================

def get_weekly_trends(db: Session, user_id: int) -> dict:
    """일주일 추이 데이터 (7일간 몸무게, 운동시간, 수면시간)"""
    today = date.today()
    seven_days_ago = today - timedelta(days=6)
    
    start_datetime = datetime.combine(seven_days_ago, datetime.min.time())
    end_datetime = datetime.combine(today, datetime.max.time())
    
    # 7일간의 모든 기록 조회
    metrics = db.query(HealthMetric).filter(
        and_(
            HealthMetric.user_id == user_id,
            HealthMetric.recorded_at >= start_datetime,
            HealthMetric.recorded_at <= end_datetime
        )
    ).order_by(HealthMetric.recorded_at).all()
    
    # 날짜별로 그룹화
    daily_metrics = {}
    for metric in metrics:
        metric_date = metric.recorded_at.date()
        if metric_date not in daily_metrics:
            daily_metrics[metric_date] = []
        daily_metrics[metric_date].append(metric)
    
    # 7일간의 추이 데이터 생성
    weight_trend = []
    exercise_trend = []
    sleep_trend = []
    
    for i in range(7):
        current_date = seven_days_ago + timedelta(days=i)
        day_metrics = daily_metrics.get(current_date, [])
        
        # 해당 날짜의 최신 몸무게
        latest_weight = day_metrics[-1].weight_kg if day_metrics else None
        
        # 해당 날짜의 총 운동시간
        total_exercise = 0
        for m in day_metrics:
            if m.exercise_duration_hours:
                total_exercise += m.exercise_duration_hours
        
        # 해당 날짜의 총 수면시간
        total_sleep = 0
        for m in day_metrics:
            if m.sleep_duration_hours:
                total_sleep += m.sleep_duration_hours
        
        weight_trend.append({
            "date": current_date,
            "value": latest_weight
        })
        
        exercise_trend.append({
            "date": current_date,
            "value": total_exercise if total_exercise > 0 else None
        })
        
        sleep_trend.append({
            "date": current_date,
            "value": total_sleep if total_sleep > 0 else None
        })
    
    return {
        "weight_trend": weight_trend,
        "exercise_trend": exercise_trend,
        "sleep_trend": sleep_trend
    }

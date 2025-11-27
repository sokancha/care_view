from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, date, timedelta
from typing import Optional, List, Tuple
from app.models.main_health_metric import HealthMetric
from app.models.onboarding import OnboardingConfig


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """BMI 계산: 체중(kg) / (신장(m))^2"""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


# ==================== 건강 기록 CRUD ====================

def create_health_metric(
    db: Session,
    user_id: int,
    weight_kg: float,
    sleep_duration_hours: Optional[float],
    exercise_duration_hours: Optional[float],
    recorded_at: Optional[datetime] = None
) -> HealthMetric:
    """새 건강 기록 생성"""
    # BMI 계산을 위해 사용자의 신장 조회
    config = db.query(OnboardingConfig).filter(OnboardingConfig.user_id == user_id).first()
    bmi = None
    if config and config.height_cm:
        bmi = calculate_bmi(weight_kg, config.height_cm)
    
    # 기록 시간이 없으면 현재 시간 사용
    if recorded_at is None:
        recorded_at = datetime.now()
    
    new_metric = HealthMetric(
        user_id=user_id,
        weight_kg=weight_kg,
        bmi=bmi,
        sleep_duration_hours=sleep_duration_hours,
        exercise_duration_hours=exercise_duration_hours,
        recorded_at=recorded_at
    )
    
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric


def get_health_metric_by_id(db: Session, metric_id: int, user_id: int) -> Optional[HealthMetric]:
    """특정 건강 기록 조회 (본인 것만)"""
    return db.query(HealthMetric).filter(
        and_(
            HealthMetric.id == metric_id,
            HealthMetric.user_id == user_id
        )
    ).first()


def update_health_metric(
    db: Session,
    metric: HealthMetric,
    weight_kg: Optional[float],
    sleep_duration_hours: Optional[float],
    exercise_duration_hours: Optional[float],
    recorded_at: Optional[datetime]
) -> HealthMetric:
    """건강 기록 수정"""
    if weight_kg is not None:
        metric.weight_kg = weight_kg # type: ignore
        # BMI 재계산
        config = db.query(OnboardingConfig).filter(OnboardingConfig.user_id == metric.user_id).first()
        if config and config.height_cm:
            metric.bmi = calculate_bmi(weight_kg, config.height_cm) # type: ignore
    
    if sleep_duration_hours is not None:
        metric.sleep_duration_hours = sleep_duration_hours # type: ignore
    
    if exercise_duration_hours is not None:
        metric.exercise_duration_hours = exercise_duration_hours # type: ignore
    
    if recorded_at is not None:
        metric.recorded_at = recorded_at # type: ignore
    
    db.commit()
    db.refresh(metric)
    return metric


def delete_health_metric(db: Session, metric: HealthMetric) -> None:
    """건강 기록 삭제"""
    db.delete(metric)
    db.commit()


# ==================== 주간 기록 조회 ====================

def get_week_date_range(target_date: date) -> Tuple[date, date]:
    """주어진 날짜가 속한 주의 월요일과 일요일 반환 (월요일 시작)"""
    # ISO 주 기준: 월요일=1, 일요일=7
    weekday = target_date.isoweekday()
    start_date = target_date - timedelta(days=weekday - 1)  # 월요일
    end_date = start_date + timedelta(days=6)  # 일요일
    return start_date, end_date


def get_weekly_records(db: Session, user_id: int, target_date: date) -> dict:
    """특정 주의 일별 기록 조회"""
    start_date, end_date = get_week_date_range(target_date)
    
    # 해당 주의 모든 기록 조회
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
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
    
    # 7일간의 일별 기록 생성
    daily_records = []
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        day_metrics = daily_metrics.get(current_date, [])
        
        # 해당 날짜의 최신 체중, 총 수면/운동 시간 계산
        latest_weight = None
        total_sleep = 0
        total_exercise = 0
        
        if day_metrics:
            # 최신 기록의 체중
            latest_weight = day_metrics[-1].weight_kg
            
            # 총 수면/운동 시간 (None이 아닌 값만 합산)
            for m in day_metrics:
                if m.sleep_duration_hours:
                    total_sleep += m.sleep_duration_hours
                if m.exercise_duration_hours:
                    total_exercise += m.exercise_duration_hours
        
        daily_records.append({
            "date": current_date,
            "metrics": day_metrics,
            "latest_weight": latest_weight,
            "total_sleep": total_sleep if total_sleep > 0 else None,
            "total_exercise": total_exercise if total_exercise > 0 else None
        })
    
    # ISO 주 번호 계산
    week_number = start_date.isocalendar()[1]
    
    return {
        "year": start_date.year,
        "week_number": week_number,
        "start_date": start_date,
        "end_date": end_date,
        "daily_records": daily_records
    }


def calculate_weight_change(db: Session, user_id: int, current_metric: HealthMetric) -> Optional[float]:
    """전일 대비 체중 변화 계산"""
    current_date = current_metric.recorded_at.date()
    previous_date = current_date - timedelta(days=1)
    
    # 전일의 가장 최근 기록 조회
    previous_start = datetime.combine(previous_date, datetime.min.time())
    previous_end = datetime.combine(previous_date, datetime.max.time())
    
    previous_metric = db.query(HealthMetric).filter(
        and_(
            HealthMetric.user_id == user_id,
            HealthMetric.recorded_at >= previous_start,
            HealthMetric.recorded_at <= previous_end
        )
    ).order_by(desc(HealthMetric.recorded_at)).first()
    
    if previous_metric:
        return round(current_metric.weight_kg - previous_metric.weight_kg, 1)
    
    return None


# ==================== 주간 요약 ====================

def get_weekly_summary(db: Session, user_id: int, target_date: date) -> dict:
    """이번 주 요약 정보"""
    start_date, end_date = get_week_date_range(target_date)
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    # 해당 주의 모든 기록
    metrics = db.query(HealthMetric).filter(
        and_(
            HealthMetric.user_id == user_id,
            HealthMetric.recorded_at >= start_datetime,
            HealthMetric.recorded_at <= end_datetime
        )
    ).order_by(HealthMetric.recorded_at).all()
    
    if not metrics:
        return {
            "latest_weight_kg": None,
            "weight_change_kg": None,
            "total_exercise_hours": 0,
            "exercise_days_count": 0,
            "total_sleep_hours": 0,
            "average_sleep_hours": None
        }
    
    # 최신 체중
    latest_weight = metrics[-1].weight_kg
    
    # 주 시작 시 체중 (첫 기록)
    start_weight = metrics[0].weight_kg
    weight_change = round(latest_weight - start_weight, 1)
    
    # 운동 관련 계산
    total_exercise = 0
    exercise_days = set()
    
    # 수면 관련 계산
    total_sleep = 0
    sleep_count = 0
    
    for metric in metrics:
        # 운동
        if metric.exercise_duration_hours and metric.exercise_duration_hours > 0:
            total_exercise += metric.exercise_duration_hours
            exercise_days.add(metric.recorded_at.date())
        
        # 수면
        if metric.sleep_duration_hours and metric.sleep_duration_hours > 0:
            total_sleep += metric.sleep_duration_hours
            sleep_count += 1
    
    # 평균 수면 시간
    average_sleep = round(total_sleep / sleep_count, 1) if sleep_count > 0 else None
    
    return {
        "latest_weight_kg": latest_weight,
        "weight_change_kg": weight_change,
        "total_exercise_hours": total_exercise,
        "exercise_days_count": len(exercise_days),
        "total_sleep_hours": total_sleep,
        "average_sleep_hours": average_sleep
    }

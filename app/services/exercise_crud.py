from sqlalchemy.orm import Session
from sqlalchemy import and_
import random
from typing import List, Dict
from datetime import date

from app.models.exercise import UserMaster, ExerciseMaster, UserExerciseLink


def calculate_age_group(date_of_birth: date) -> str:
    """생년월일로 연령대 계산"""
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    if age < 20:
        return "10대"
    elif age < 30:
        return "20대"
    elif age < 40:
        return "30대"
    elif age < 50:
        return "40대"
    elif age < 60:
        return "50대"
    else:
        return "60대 이상"


def calculate_bmi_grade(weight_kg: float, height_cm: float) -> str:
    """
    체중과 키로 BMI 등급 계산
    
    CSV 데이터의 BMI_IDEX_GRAD_NM 기준:
    - 저체중: BMI < 18.5
    - 정상: 18.5 <= BMI < 23
    - 비만전단계비만: 23 <= BMI < 25
    - 1단계비만: 25 <= BMI < 30
    - 2단계비만: 30 <= BMI < 35
    - 3단계비만: BMI >= 35
    """
    bmi = weight_kg / ((height_cm / 100) ** 2)
    
    if bmi < 18.5:
        return "저체중"
    elif bmi < 23:
        return "정상"
    elif bmi < 25:
        return "비만전단계비만"  # ✅ CSV와 일치
    elif bmi < 30:
        return "1단계비만"
    elif bmi < 35:
        return "2단계비만"
    else:
        return "3단계비만"


def get_user_group_id(db: Session, age_group: str, bmi_grade: str) -> int:
    """사용자의 연령대와 BMI 등급으로 user_id 조회"""
    user_group = db.query(UserMaster).filter(
        and_(
            UserMaster.age_group == age_group,
            UserMaster.bmi_grade == bmi_grade
        )
    ).first()
    
    if not user_group:
        raise ValueError(f"해당 조건의 사용자 그룹을 찾을 수 없습니다: {age_group}, {bmi_grade}")
    
    return user_group.user_id


def get_exercise_by_step(
    db: Session, 
    user_id: int, 
    step_name: str, 
    exclude_ids: List[int] = None
) -> Dict:
    """특정 단계(준비/본/마무리)의 운동 1개 랜덤 조회"""
    query = db.query(
        ExerciseMaster.movement_name,
        ExerciseMaster.step_name,
        UserExerciseLink.calorie_kcal,
        UserExerciseLink.duration_min,
        ExerciseMaster.exercise_id
    ).join(
        UserExerciseLink,
        UserExerciseLink.exercise_id == ExerciseMaster.exercise_id
    ).filter(
        and_(
            UserExerciseLink.user_id == user_id,
            ExerciseMaster.step_name == step_name
        )
    )
    
    # 이미 선택된 운동 제외 (중복 방지)
    if exclude_ids:
        query = query.filter(ExerciseMaster.exercise_id.notin_(exclude_ids))
    
    exercises = query.all()
    
    if not exercises:
        raise ValueError(f"{step_name} 운동을 찾을 수 없습니다.")
    
    # 랜덤 선택
    selected = random.choice(exercises)
    
    return {
        "movement_name": selected.movement_name,
        "step_name": selected.step_name,
        "duration_min": selected.duration_min,
        "calorie_kcal": selected.calorie_kcal,
        "exercise_id": selected.exercise_id
    }


def create_exercise_set(db: Session, user_id: int, exclude_ids: List[int] = None) -> Dict:
    """하나의 운동 세트 생성 (준비+본+마무리)"""
    if exclude_ids is None:
        exclude_ids = []
    
    # 1. 준비운동 선택
    warmup = get_exercise_by_step(db, user_id, "준비운동", exclude_ids)
    exclude_ids.append(warmup["exercise_id"])
    
    # 2. 본운동 선택
    main = get_exercise_by_step(db, user_id, "본운동", exclude_ids)
    exclude_ids.append(main["exercise_id"])
    
    # 3. 마무리운동 선택
    cooldown = get_exercise_by_step(db, user_id, "마무리운동", exclude_ids)
    exclude_ids.append(cooldown["exercise_id"])
    
    exercises = [warmup, main, cooldown]
    
    total_duration = sum(e["duration_min"] for e in exercises)
    total_calorie = sum(e["calorie_kcal"] for e in exercises)
    
    return {
        "exercises": exercises,
        "total_duration_min": total_duration,
        "total_calorie_kcal": total_calorie
    }


def generate_daily_exercise_plan(
    db: Session, 
    date_of_birth: date, 
    weight_kg: float, 
    height_cm: float
) -> Dict:
    """
    아침/점심/저녁 운동 추천 생성
    
    Args:
        db: 데이터베이스 세션
        date_of_birth: 생년월일
        weight_kg: 체중 (kg)
        height_cm: 키 (cm)
    
    Returns:
        아침/점심/저녁 운동 세트 + 총 시간/칼로리
    """
    # 1. 연령대와 BMI 등급 계산
    age_group = calculate_age_group(date_of_birth)
    bmi_grade = calculate_bmi_grade(weight_kg, height_cm)
    
    # 2. 사용자 그룹 ID 조회
    user_id = get_user_group_id(db, age_group, bmi_grade)
    
    # 2. 중복 방지를 위한 이미 선택된 운동 ID 리스트
    used_exercise_ids = []
    
    # 3. 아침 운동 생성
    morning_set = create_exercise_set(db, user_id, used_exercise_ids)
    
    # 4. 점심 운동 생성 (아침과 다른 운동)
    lunch_set = create_exercise_set(db, user_id, used_exercise_ids)
    
    # 5. 저녁 운동 생성 (아침, 점심과 다른 운동)
    dinner_set = create_exercise_set(db, user_id, used_exercise_ids)
    
    # 6. 전체 합계 계산
    total_duration = (
        morning_set["total_duration_min"] +
        lunch_set["total_duration_min"] +
        dinner_set["total_duration_min"]
    )
    
    total_calorie = (
        morning_set["total_calorie_kcal"] +
        lunch_set["total_calorie_kcal"] +
        dinner_set["total_calorie_kcal"]
    )
    
    return {
        "morning": morning_set,
        "lunch": lunch_set,
        "dinner": dinner_set,
        "total_duration_min": total_duration,
        "total_calorie_kcal": total_calorie
    }

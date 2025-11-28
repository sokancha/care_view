from sqlalchemy.orm import Session
from app.models.onboarding import OnboardingConfig
from app.models.user import User
from app.models.allergy import Allergy
import json
from typing import Dict, Optional, List, Any
from datetime import date # date 객체만 임포트
from typing import List

# 1. 온보딩 설정 조회 또는 생성 (CRUD 핵심 함수)

def get_onboarding_config(db: Session, user_id: int) -> Optional[OnboardingConfig]:
    """사용자의 온보딩 설정을 조회합니다."""
    return db.query(OnboardingConfig).filter(OnboardingConfig.user_id == user_id).first()


def create_onboarding_config(db: Session, user_id: int) -> OnboardingConfig:
    """새 온보딩 설정을 생성합니다."""
    # goal 필드가 NOT NULL이므로 초기값을 'not_set'으로 설정합니다.
    db_config = OnboardingConfig(user_id=user_id, goal="not_set")
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


# 2. 단계별 업데이트 로직

def update_step1_goal(db: Session, user_id: int, goal: str) -> OnboardingConfig:
    """Step 1: 운동 목적을 업데이트합니다."""
    config = get_onboarding_config(db, user_id)
    if not config:
        config = create_onboarding_config(db, user_id)
    
    config.goal = goal # type: ignore
    db.commit()
    db.refresh(config)
    return config


def update_step2_schedule(db: Session, user_id: int, schedule: Dict[str, Any]) -> OnboardingConfig:
    """Step 2: 주간 운동 스케줄 (시작/종료 시간)을 업데이트합니다."""
    config = get_onboarding_config(db, user_id)
    if not config:
        config = create_onboarding_config(db, user_id)

    # 🚨 수정: 딕셔너리를 JSON 문자열로 변환 (sort_keys=False로 순서 유지)
    config.weekly_workout_schedule = json.dumps(schedule, ensure_ascii=False, sort_keys=False) # type: ignore
    db.commit()
    db.refresh(config)
    return config


def update_step3_basic_info(
    db: Session, 
    user_id: int, 
    date_of_birth: date,
    height_cm: float, 
    current_weight_kg: float, 
    allergy_ids: List[int]
) -> OnboardingConfig:
    """Step 3: 기본 정보와 알레르기 정보를 업데이트합니다."""
    config = get_onboarding_config(db, user_id)
    if not config:
        config = create_onboarding_config(db, user_id)
    
    # 1. OnboardingConfig 업데이트
    config.date_of_birth = date_of_birth # type: ignore
    config.height_cm = height_cm # type: ignore
    config.current_weight_kg = current_weight_kg # type: ignore
    
    # 2. 알레르기 정보 업데이트 (User 모델의 M:N 관계 사용)
    user = db.query(User).filter(User.id == user_id).first()
    
    # 🚨 추가: user가 존재하는지 확인
    if not user:
        raise ValueError(f"사용자 ID {user_id}를 찾을 수 없습니다.")
    
    # 기존 알레르기 관계 초기화
    user.allergies = []
    
    if allergy_ids:
        # 유효한 알레르기 ID인지 확인
        allergies = db.query(Allergy).filter(Allergy.id.in_(allergy_ids)).all()
        if len(allergies) != len(allergy_ids):
            # 존재하지 않는 ID 찾기
            found_ids = {a.id for a in allergies}
            missing_ids = [aid for aid in allergy_ids if aid not in found_ids]
            raise ValueError(f"알레르기 ID {missing_ids}를 찾을 수 없습니다.")
        user.allergies.extend(allergies)

    db.commit()
    db.refresh(config)
    return config


def update_step4_job(db: Session, user_id: int, job_type: str) -> OnboardingConfig:
    """Step 4: 직업 유형을 업데이트합니다."""
    config = get_onboarding_config(db, user_id)
    if not config:
        config = create_onboarding_config(db, user_id)
    
    config.job_type = job_type # type: ignore
    db.commit()
    db.refresh(config)
    return config


def complete_onboarding(db: Session, user_id: int) -> OnboardingConfig:
    """Step 5: 온보딩 완료 플래그를 True로 설정합니다."""
    config = get_onboarding_config(db, user_id)
    if not config:
        raise ValueError("온보딩 설정이 존재하지 않습니다.")
    
    config.is_onboarding_complete = True # type: ignore
    db.commit()
    db.refresh(config)
    return config

def get_all_allergies(db: Session) -> List[Allergy]:
    """알레르기 전체 목록 조회"""
    return db.query(Allergy).order_by(Allergy.id).all()

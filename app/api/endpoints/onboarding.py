from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, time

from app.core.database import get_db
from app.schemas.onboarding import (
    OnboardingStep1,
    OnboardingStep2,
    OnboardingStep3,
    OnboardingStep4,
    OnboardingStep5,
    OnboardingConfigResponse
)
from app.api.dependencies import get_current_user
from app.services import onboarding_crud
from app.models.user import User
from typing import Dict, Any

# APIRouter 객체 생성
router = APIRouter(prefix="/api/onboarding", tags=["Onboarding"])


# 온보딩 현재 상태 조회
@router.get(
    "/status",
    response_model=OnboardingConfigResponse,
    status_code=status.HTTP_200_OK,
    tags=["Onboarding"]
)
def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 사용자의 온보딩 진행 상태 조회. 설정이 없으면 새로 생성합니다."""
    config = onboarding_crud.get_onboarding_config(db, user_id=current_user.id)
    
    # 온보딩 설정이 없으면 새로 생성
    if not config:
        config = onboarding_crud.create_onboarding_config(db, user_id=current_user.id)
    
    return config


# Step 1: 운동 목적 설정
@router.post(
    "/step1",
    response_model=OnboardingConfigResponse,
    status_code=status.HTTP_200_OK,
    tags=["Onboarding"]
)
def set_goal(
    step_data: OnboardingStep1,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Step 1: 운동 목적 설정 (체지방 감소 또는 근육량 증가)"""
    
    # 유효한 목적인지 검증
    if step_data.goal not in ["fat_loss", "muscle_gain"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="올바른 목적을 선택해주세요. ('fat_loss' 또는 'muscle_gain')"
        )
    
    config = onboarding_crud.update_step1_goal(
        db=db,
        user_id=current_user.id,
        goal=step_data.goal
    )
    
    return config


# Step 2: 주간 운동 스케줄 설정
@router.post(
    "/step2",
    response_model=OnboardingConfigResponse,
    status_code=status.HTTP_200_OK,
    tags=["Onboarding"]
)
def set_workout_schedule(
    step_data: OnboardingStep2,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Step 2: 요일별 운동 가능 시작/종료 시간 설정"""
    
    # 요일 검증
    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    schedule_to_save: Dict[str, Any] = {}

    for day, slot in step_data.weekly_workout_schedule.items():
        if day not in valid_days:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"올바르지 않은 요일입니다: {day}"
            )
        
        start_time = slot.start_time
        end_time = slot.end_time

        # 1. 일관성 검증: 시작 시간과 종료 시간 중 하나만 있으면 안 됨 (둘 다 None이거나 둘 다 str이어야 함)
        if (start_time is not None) != (end_time is not None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"[{day}] 시작 시간과 종료 시간 중 하나만 제공되었습니다. 둘 다 설정하거나 둘 다 비워두세요."
            )
        
        # 2. 시간 순서 검증: 시작 < 종료여야 함 (시간 문자열 비교로 간단하게 처리)
        if start_time is not None and end_time is not None:
            if start_time >= end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"[{day}] 시작 시간({start_time})은 종료 시간({end_time})보다 빨라야 합니다."
                )

        # 🚨 수정된 부분: Pydantic 객체(slot)를 순수 Python dict으로 변환합니다.
        schedule_to_save[day] = slot.model_dump()
    
    # CRUD 함수 호출 시 Dict[str, dict] 형태의 schedule_to_save 전달
    config = onboarding_crud.update_step2_schedule(
        db=db,
        user_id=current_user.id,
        schedule=schedule_to_save
    )
    
    return config


# Step 3: 기본 정보 및 알레르기 설정
@router.post(
    "/step3",
    response_model=OnboardingConfigResponse,
    status_code=status.HTTP_200_OK,
    tags=["Onboarding"]
)
def set_basic_info(
    step_data: OnboardingStep3,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Step 3: 나이, 신장, 체중 및 알레르기 정보 설정"""
    
    try:
        config = onboarding_crud.update_step3_basic_info(
            db=db,
            user_id=current_user.id,
            date_of_birth=step_data.date_of_birth,
            height_cm=step_data.height_cm,
            current_weight_kg=step_data.current_weight_kg,
            allergy_ids=step_data.allergy_ids
        )
        return config
    except ValueError as e:
        # CRUD 함수에서 알레르기 ID를 찾지 못한 경우 발생
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Step 4: 직업 설정
@router.post(
    "/step4",
    response_model=OnboardingConfigResponse,
    status_code=status.HTTP_200_OK,
    tags=["Onboarding"]
)
def set_job_type(
    step_data: OnboardingStep4,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Step 4: 직업 유형 설정 (학생 또는 직장인)"""
    
    # 유효한 직업 유형인지 검증
    if step_data.job_type not in ["student", "worker"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="올바른 직업 유형을 선택해주세요. ('student' 또는 'worker')"
        )
    
    config = onboarding_crud.update_step4_job(
        db=db,
        user_id=current_user.id,
        job_type=step_data.job_type
    )
    
    return config


# Step 5: 온보딩 완료
@router.post(
    "/step5",
    response_model=OnboardingConfigResponse,
    status_code=status.HTTP_200_OK,
    tags=["Onboarding"]
)
def complete_onboarding_flow(
    step_data: OnboardingStep5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Step 5: 온보딩 완료 처리 (시작하기 버튼)"""
    
    try:
        config = onboarding_crud.complete_onboarding(
            db=db,
            user_id=current_user.id
        )
        return config
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
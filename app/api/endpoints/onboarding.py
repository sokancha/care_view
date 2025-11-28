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
    OnboardingConfigResponse,
    GoalResponse,
    JobResponse,
    AllergyResponse,
    AllergyItem
)
from app.api.dependencies import get_current_user
from app.services import onboarding_crud
from app.models.user import User

# APIRouter 객체 생성
router = APIRouter(prefix="/api/onboarding", tags=["Onboarding"])

GOALS = ["fat_loss", "muscle_gain"]
JOBS = ["student", "worker"]

@router.get("/goals", response_model=GoalResponse, status_code=status.HTTP_200_OK)
def get_goals(current_user: User = Depends(get_current_user)):
    """Step 1에서 선택 가능한 운동 목적 목록 조회"""
    return {"goals": GOALS}

@router.get("/jobs", response_model=JobResponse, status_code=status.HTTP_200_OK)
def get_jobs(current_user: User = Depends(get_current_user)):
    """Step 4에서 선택 가능한 직업 목록 조회"""
    return {"jobs": JOBS}

@router.get("/allergies", response_model=AllergyResponse, status_code=status.HTTP_200_OK)
def get_allergies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Step 3에서 선택 가능한 알레르기 목록 조회 (ID 1~100)"""
    allergies = onboarding_crud.get_all_allergies(db)
    return {"allergies": [AllergyItem(id=a.id, name=a.name) for a in allergies]} # type: ignore


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
    config = onboarding_crud.get_onboarding_config(db, user_id=current_user.id) # type: ignore
    
    # 온보딩 설정이 없으면 새로 생성
    if not config:
        config = onboarding_crud.create_onboarding_config(db, user_id=current_user.id) # type: ignore
    
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
    if step_data.goal not in GOALS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="올바른 목적을 선택해주세요. ('fat_loss' 또는 'muscle_gain')"
        )
    
    return onboarding_crud.update_step1_goal(
        db=db,
        user_id=current_user.id, # type: ignore
        goal=step_data.goal
    
    )


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
    """Step 2: 요일별 운동 가능 시작/종료 시간 설정 (7일 전체)"""
    
    # 7일 전체를 dict로 변환
    schedule_dict = {
        "monday": step_data.monday.model_dump(),
        "tuesday": step_data.tuesday.model_dump(),
        "wednesday": step_data.wednesday.model_dump(),
        "thursday": step_data.thursday.model_dump(),
        "friday": step_data.friday.model_dump(),
        "saturday": step_data.saturday.model_dump(),
        "sunday": step_data.sunday.model_dump()
    }
    
    # 시간 유효성 검증
    for day, slot in schedule_dict.items():
        start_time = slot.get("start_time")
        end_time = slot.get("end_time")
        
        has_start = start_time is not None
        has_end = end_time is not None

        # 시작 시간과 종료 시간 일관성 검증
        if has_start != has_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"[{day}] 시작 시간과 종료 시간 중 하나만 제공되었습니다. 둘 다 설정하거나 둘 다 비워두세요."
            )
        
        # 시간 순서 검증
        if has_start and has_end:
            if start_time >= end_time:
                 raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"[{day}] 시작 시간({start_time})은 종료 시간({end_time})보다 빨라야 합니다."
                )
    
    return onboarding_crud.update_step2_schedule(
        db=db,
        user_id=current_user.id, # type: ignore
        schedule=schedule_dict
    )


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
            user_id=current_user.id, # type: ignore
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
    
    """Step 4: 직업 유형 설정 (학생 또는 직장인)"""
    if step_data.job_type not in JOBS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="올바른 직업 유형을 선택해주세요. ('student' 또는 'worker')"
        )
    
    return onboarding_crud.update_step4_job(
        db=db,
        user_id=current_user.id, # type: ignore
        job_type=step_data.job_type
    )


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
            user_id=current_user.id  # type: ignore
        )
        return config
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

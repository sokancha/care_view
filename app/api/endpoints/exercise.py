from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.exercise import ExerciseRecommendationResponse, ExerciseSet, ExerciseItem
from app.api.dependencies import get_current_user
from app.services import exercise_crud
from app.models.user import User
from app.models.onboarding import OnboardingConfig

router = APIRouter(prefix="/api/exercise", tags=["Exercise"])


@router.get(
    "/recommend",
    response_model=ExerciseRecommendationResponse,
    status_code=status.HTTP_200_OK,
    description="사용자 맞춤 하루 운동 추천 (아침/점심/저녁)"
)
def get_exercise_recommendation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    사용자의 생년월일, 키, 체중을 기반으로 하루 운동을 추천합니다.
    
    - 아침/점심/저녁 각각 준비운동+본운동+마무리운동 조합
    - 총 운동시간 및 칼로리 소모량 제공
    """
    
    # 1. 사용자 온보딩 정보 조회
    config = db.query(OnboardingConfig).filter(
        OnboardingConfig.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail="온보딩 정보를 찾을 수 없습니다. 먼저 온보딩을 완료해주세요."
        )
    
    # 2. 필수 정보 확인
    if not config.date_of_birth:
        raise HTTPException(
            status_code=400,
            detail="생년월일 정보가 없습니다."
        )
    
    if not config.height_cm or not config.current_weight_kg:
        raise HTTPException(
            status_code=400,
            detail="키 또는 체중 정보가 없습니다."
        )
    
    # 3. 운동 추천 생성 (생년월일, 체중, 키 전달)
    try:
        recommendation = exercise_crud.generate_daily_exercise_plan(
            db=db,
            date_of_birth=config.date_of_birth,
            weight_kg=config.current_weight_kg,
            height_cm=config.height_cm
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=f"운동 추천 생성 실패: {str(e)}"
        )
    
    # 4. 응답 구성
    return ExerciseRecommendationResponse(
        morning=ExerciseSet(
            exercises=[ExerciseItem(**ex) for ex in recommendation["morning"]["exercises"]],
            total_duration_min=recommendation["morning"]["total_duration_min"],
            total_calorie_kcal=recommendation["morning"]["total_calorie_kcal"]
        ),
        lunch=ExerciseSet(
            exercises=[ExerciseItem(**ex) for ex in recommendation["lunch"]["exercises"]],
            total_duration_min=recommendation["lunch"]["total_duration_min"],
            total_calorie_kcal=recommendation["lunch"]["total_calorie_kcal"]
        ),
        dinner=ExerciseSet(
            exercises=[ExerciseItem(**ex) for ex in recommendation["dinner"]["exercises"]],
            total_duration_min=recommendation["dinner"]["total_duration_min"],
            total_calorie_kcal=recommendation["dinner"]["total_calorie_kcal"]
        ),
        total_duration_min=recommendation["total_duration_min"],
        total_calorie_kcal=recommendation["total_calorie_kcal"]
    )

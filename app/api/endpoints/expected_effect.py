from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.expected_effect import ExpectedEffectResponse
from app.api.dependencies import get_current_user
from app.services import expected_effect_crud, exercise_crud
from app.models.user import User
from app.models.onboarding import OnboardingConfig
from app.models.main_health_metric import HealthMetric

router = APIRouter(prefix="/api/expected-effect", tags=["Expected Effect"])


@router.get(
    "",
    response_model=ExpectedEffectResponse,
    status_code=status.HTTP_200_OK,
    description="운동 지속 시 4주 후 기대 효과 예측"
)
def get_expected_effect(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    추천 운동을 계속 할 경우 4주 후 예상 체중, BMI 변화를 보여줍니다.
    
    - 현재 체중/BMI
    - 오늘까지 총 운동시간 (분)
    - 주차별 체중/BMI 예측 그래프 데이터
    """
    
    # 1. 온보딩 정보 조회
    config = db.query(OnboardingConfig).filter(
        OnboardingConfig.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail="온보딩 정보를 찾을 수 없습니다."
        )
    
    if not config.height_cm or not config.current_weight_kg:
        raise HTTPException(
            status_code=400,
            detail="키 또는 체중 정보가 없습니다."
        )
    
    # 2. 최신 체중 조회 (기록실에서 가장 최근 입력값)
    latest_metric = db.query(HealthMetric).filter(
        HealthMetric.user_id == current_user.id,
        HealthMetric.weight_kg.isnot(None)
    ).order_by(HealthMetric.recorded_at.desc()).first()
    
    # 최신 기록이 있으면 그걸 사용, 없으면 온보딩 체중 사용
    current_weight = latest_metric.weight_kg if latest_metric else config.current_weight_kg
    
    # 3. 추천 운동 조회 (일일 칼로리 계산)
    try:
        if not config.date_of_birth:
            raise HTTPException(status_code=400, detail="생년월일 정보가 없습니다.")
        
        recommendation = exercise_crud.generate_daily_exercise_plan(
            db=db,
            date_of_birth=config.date_of_birth,
            weight_kg=current_weight,
            height_cm=config.height_cm
        )
        
        # 일일 총 칼로리 소모
        daily_calorie_burn = recommendation["total_calorie_kcal"]
        
    except ValueError:
        # 운동 추천 실패 시 기본값 (하루 500kcal 소모 가정)
        daily_calorie_burn = 500
    
    # 4. 기대 효과 계산
    effect_data = expected_effect_crud.generate_expected_effect(
        db=db,
        user_id=current_user.id,
        current_weight=current_weight,
        height_cm=config.height_cm,
        daily_calorie_burn=daily_calorie_burn
    )
    
    # 5. 응답 구성
    return ExpectedEffectResponse(**effect_data)

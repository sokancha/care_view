from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base # Base 객체 임포트 (경로를 확인해 주세요)


class HealthMetric(Base):
    """
    사용자의 건강 지표를 시간순으로 기록하는 테이블 모델.
    users 테이블과 1:N 관계를 가집니다.
    """
    __tablename__ = "health_metrics"

    # 1. 핵심 ID
    id = Column(Integer, primary_key=True, index=True)
    
    # 2. 관계 설정
    # 외래 키: users 테이블의 id를 참조하는 1:N 관계
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # ORM 관계 설정 (User 모델에 'metrics' 관계가 추가되었다고 가정)
    user = relationship("User", back_populates="metrics") 

    # 3. 측정 지표 (대시보드 및 기록실의 핵심 동적 데이터)
    weight_kg = Column(Float, nullable=False)           # 측정 몸무게 (kg)
    bmi = Column(Float, nullable=True)                  # 체질량 지수 (BMI)
    sleep_duration_hours = Column(Float, nullable=True) # 총 수면 시간 (시간)
    exercise_duration_hours = Column(Float, nullable=True) # 총 운동 시간 (시간)
    
    # 4. 시간 정보
    # 이 필드가 '가장 최근' 기록을 찾기 위한 핵심 필드입니다.
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
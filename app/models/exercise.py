from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base # 실제 프로젝트 경로에 맞게 임포트 경로를 확인하세요.

# SQLAlchemy의 Base 객체가 정의되었다고 가정합니다.
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base() 
# (실제 프로젝트에서는 위 Base 정의 대신 프로젝트의 Base 객체를 사용하세요.)

# class Base: # 임시 Base 클래스 정의 (실제 사용 시 대체 필요)
#     pass 

# ----------------------------------------------------------------------
# 1. UserMaster (사용자 그룹 정보)
# ----------------------------------------------------------------------
class UserMaster(Base):
    """
    사용자 그룹의 인구통계학적 정보를 관리하는 마스터 테이블입니다.
    """
    __tablename__ = 'user_master' 

    user_id = Column(Integer, primary_key=True) 
    
    # 직관적인 컬럼명 적용
    age_group = Column(String(10), nullable=False)        # 연령대 (예: 10대)
    bmi_grade = Column(String(20), nullable=False)        # BMI 등급 (예: 1단계비만)

    # UserExerciseLink 테이블과 1:N 관계 설정
    exercise_links = relationship("UserExerciseLink", back_populates="user_group")
    
    __table_args__ = (
        UniqueConstraint('age_group', 'bmi_grade', name='uq_user_group'),
    )

    def __repr__(self):
        return f"<UserMaster ID:{self.user_id} - {self.age_group}/{self.bmi_grade}>"

# ----------------------------------------------------------------------
# 2. ExerciseMaster (운동 종목 기준 정보)
# ----------------------------------------------------------------------
class ExerciseMaster(Base):
    """
    운동 종목의 표준 정보를 관리하는 마스터 테이블입니다.
    """
    __tablename__ = 'exercise_master' 

    exercise_id = Column(Integer, primary_key=True)

    # 직관적인 컬럼명 적용
    step_name = Column(String(50), nullable=False)          # 운동 단계 (준비운동, 본운동)
    movement_name = Column(String(100), nullable=False)     # 운동 종목명 (동적 스트레칭 등)
    
    # UserExerciseLink 테이블과 1:N 관계 설정
    user_links = relationship("UserExerciseLink", back_populates="exercise_item")
    
    __table_args__ = (
        UniqueConstraint('step_name', 'movement_name', name='uq_exercise_name'),
    )

    def __repr__(self):
        return f"<ExerciseMaster ID:{self.exercise_id} - {self.movement_name}>"

# ----------------------------------------------------------------------
# 3. UserExerciseLink (연결 테이블 - 원본 데이터의 핵심 정보 저장)
# ----------------------------------------------------------------------
class UserExerciseLink(Base):
    """
    사용자 그룹과 운동 종목을 연결하고, 해당 조합의 표준 칼로리 및 시간 값을 저장합니다.
    """
    __tablename__ = 'user_exercise_link'

    link_id = Column(Integer, primary_key=True) 

    # 외래키
    user_id = Column(Integer, ForeignKey('user_master.user_id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercise_master.exercise_id'), nullable=False)

    # 직관적인 컬럼명 적용
    calorie_kcal = Column(Integer, nullable=False)       # 해당 조합의 표준 칼로리
    duration_min = Column(Integer, nullable=False)       # 해당 조합의 표준 시간 (분)

    # ORM 관계 (Relationship)
    user_group = relationship("UserMaster", back_populates="exercise_links")
    exercise_item = relationship("ExerciseMaster", back_populates="user_links")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'exercise_id', name='uq_user_exercise_link'),
    )

    def __repr__(self):
        return f"<Link ID:{self.link_id} - U:{self.user_id}, E:{self.exercise_id}>"

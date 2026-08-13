from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base 

class UserMaster(Base):
    """
    사용자 그룹의 인구통계학적 정보를 관리하는 마스터 테이블입니다.
    """
    __tablename__ = 'user_master' 

    user_id = Column(Integer, primary_key=True) 

    age_group = Column(String(10), nullable=False)        
    bmi_grade = Column(String(20), nullable=False)        

    exercise_links = relationship("UserExerciseLink", back_populates="user_group")
    
    __table_args__ = (
        UniqueConstraint('age_group', 'bmi_grade', name='uq_user_group'),
    )

    def __repr__(self):
        return f"<UserMaster ID:{self.user_id} - {self.age_group}/{self.bmi_grade}>"

class ExerciseMaster(Base):
    """
    운동 종목의 표준 정보를 관리하는 마스터 테이블입니다.
    """
    __tablename__ = 'exercise_master' 

    exercise_id = Column(Integer, primary_key=True)

    step_name = Column(String(50), nullable=False)          
    movement_name = Column(String(100), nullable=False)     
    
    user_links = relationship("UserExerciseLink", back_populates="exercise_item")
    
    __table_args__ = (
        UniqueConstraint('step_name', 'movement_name', name='uq_exercise_name'),
    )

    def __repr__(self):
        return f"<ExerciseMaster ID:{self.exercise_id} - {self.movement_name}>"

class UserExerciseLink(Base):
    """
    사용자 그룹과 운동 종목을 연결하고, 해당 조합의 표준 칼로리 및 시간 값을 저장합니다.
    """
    __tablename__ = 'user_exercise_link'

    link_id = Column(Integer, primary_key=True) 

    
    user_id = Column(Integer, ForeignKey('user_master.user_id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercise_master.exercise_id'), nullable=False)

    
    calorie_kcal = Column(Integer, nullable=False)       
    duration_min = Column(Integer, nullable=False)       

    
    user_group = relationship("UserMaster", back_populates="exercise_links")
    exercise_item = relationship("ExerciseMaster", back_populates="user_links")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'exercise_id', name='uq_user_exercise_link'),
    )

    def __repr__(self):
        return f"<Link ID:{self.link_id} - U:{self.user_id}, E:{self.exercise_id}>"

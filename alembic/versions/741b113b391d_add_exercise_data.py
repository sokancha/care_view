"""add_exercise_csv_Data

Revision ID: 39f79fce12af
Revises: 206a2a590a91
Create Date: 2025-12-08 04:57:26.180191

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import csv
import os

# revision identifiers, used by Alembic.
revision: str = '741b113b391d'
down_revision: Union[str, Sequence[str], None] = 'b33fa1ecaa71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert CSV data into existing tables."""

    # Alembic DB 연결
    bind = op.get_bind()
    session = Session(bind=bind)

    # CSV 경로 (care_view 폴더 안)
    csv_path = "cleaned_exercise_data.csv"

    # 모델 정의 (Alembic 환경에서 바로 사용)
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    class UserMaster(Base):
        __tablename__ = 'user_master'
        user_id = sa.Column(sa.Integer, primary_key=True)
        age_group = sa.Column(sa.String(10), nullable=False)
        bmi_grade = sa.Column(sa.String(20), nullable=False)

    class ExerciseMaster(Base):
        __tablename__ = 'exercise_master'
        exercise_id = sa.Column(sa.Integer, primary_key=True)
        step_name = sa.Column(sa.String(50), nullable=False)
        movement_name = sa.Column(sa.String(100), nullable=False)

    class UserExerciseLink(Base):
        __tablename__ = 'user_exercise_link'
        link_id = sa.Column(sa.Integer, primary_key=True)
        user_id = sa.Column(sa.Integer, nullable=False)
        exercise_id = sa.Column(sa.Integer, nullable=False)
        calorie_kcal = sa.Column(sa.Integer, nullable=False)
        duration_min = sa.Column(sa.Integer, nullable=False)

    # CSV 읽어서 DB 삽입
    with open(csv_path, encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            age_group = row["AGRDE_FLAG_NM"]
            bmi_grade = row["BMI_IDEX_GRAD_NM"]

            step_name = row["SPORTS_STEP_NM"]
            movement_name = row["RECOMEND_MVM_NM"]
            calorie = int(row["CALORIE_KCAL"])
            duration = int(row["EXERCISE_TIME_MIN"])

            # UserMaster 중복 체크
            user = session.query(UserMaster).filter_by(
                age_group=age_group, bmi_grade=bmi_grade
            ).first()
            if not user:
                user = UserMaster(age_group=age_group, bmi_grade=bmi_grade)
                session.add(user)
                session.flush()  # user_id 바로 사용 가능

            # ExerciseMaster 중복 체크
            ex = session.query(ExerciseMaster).filter_by(
                step_name=step_name, movement_name=movement_name
            ).first()
            if not ex:
                ex = ExerciseMaster(step_name=step_name, movement_name=movement_name)
                session.add(ex)
                session.flush()  # exercise_id 바로 사용 가능

            # UserExerciseLink 생성
            link = session.query(UserExerciseLink).filter_by(
                user_id=user.user_id, exercise_id=ex.exercise_id
            ).first()
            if not link:
                link = UserExerciseLink(
                    user_id=user.user_id,
                    exercise_id=ex.exercise_id,
                    calorie_kcal=calorie,
                    duration_min=duration
                )
                session.add(link)

    session.commit()


def downgrade() -> None:
    """Downgrade: 데이터 삭제하지 않음."""
    pass

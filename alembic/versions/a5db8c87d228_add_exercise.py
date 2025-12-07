from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5db8c87d228'
down_revision: Union[str, Sequence[str], None] = '8a07f52cff16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Creates UserMaster, ExerciseMaster, and UserExerciseLink tables."""
    
    # ----------------------------------------------------------------------
    # 1. UserMaster 테이블 생성
    # ----------------------------------------------------------------------
    op.create_table(
        'user_master',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('age_group', sa.String(length=10), nullable=False),
        sa.Column('bmi_grade', sa.String(length=20), nullable=False),
        sa.Column('gender', sa.String(length=1), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('age_group', 'bmi_grade', 'gender', name='uq_user_group')
    )
    
    # ----------------------------------------------------------------------
    # 2. ExerciseMaster 테이블 생성
    # ----------------------------------------------------------------------
    op.create_table(
        'exercise_master',
        sa.Column('exercise_id', sa.Integer(), nullable=False),
        sa.Column('step_name', sa.String(length=50), nullable=False),
        sa.Column('movement_name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('exercise_id'),
        sa.UniqueConstraint('step_name', 'movement_name', name='uq_exercise_name')
    )

    # ----------------------------------------------------------------------
    # 3. UserExerciseLink 테이블 생성
    # ----------------------------------------------------------------------
    op.create_table(
        'user_exercise_link',
        sa.Column('link_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exercise_id', sa.Integer(), nullable=False),
        sa.Column('calorie_kcal', sa.Integer(), nullable=False),
        sa.Column('duration_min', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('link_id'),
        # 외래 키 정의
        sa.ForeignKeyConstraint(['user_id'], ['user_master.user_id'], ),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercise_master.exercise_id'], ),
        # 고유 제약 조건
        sa.UniqueConstraint('user_id', 'exercise_id', name='uq_user_exercise_link')
    )


def downgrade() -> None:
    """Downgrade schema: Drops all three tables created in upgrade."""
    # 생성된 테이블을 역순으로 삭제합니다.
    op.drop_table('user_exercise_link')
    op.drop_table('exercise_master')
    op.drop_table('user_master')

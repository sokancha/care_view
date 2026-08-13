
import sys
import os


current_script_dir = os.path.dirname(os.path.abspath(__file__))

project_root_dir = os.path.dirname(current_script_dir)

sys.path.append(project_root_dir)


from app.core.database import engine, create_tables 

import app.models.user
import app.models.allergy
import app.models.meal
import app.models.onboarding
import app.models.main_health_metric

def init_db():
    print("데이터베이스 초기화 시작...")
    try:
        create_tables(engine)
        print("✅ 모든 테이블 생성이 완료되었습니다.")
        
        print("데이터베이스 초기화 성공.")
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()

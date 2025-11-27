# app/initial_data.py

import sys
import os

# =================================================================
# 🚨 수정된 부분: Python Path 조정 
# 현재 스크립트가 app/initial_data.py에 있으므로, 
# 'app' 패키지를 임포트하기 위해 상위 디렉토리(프로젝트 루트)를 Path에 추가해야 합니다.
# =================================================================

# 1. 현재 스크립트의 디렉토리를 가져옵니다. (예: /app/app)
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 프로젝트 루트 디렉토리를 계산합니다. (예: /app)
project_root_dir = os.path.dirname(current_script_dir)

# 3. 프로젝트 루트를 sys.path에 추가합니다.
sys.path.append(project_root_dir)


# =================================================================
# DB 및 모델 임포트
# =================================================================

# 이제 sys.path에 프로젝트 루트가 있으므로, 'app'을 정상적으로 찾을 수 있습니다.
from app.core.database import engine, create_tables 

# 🚨 중요: 모든 ORM 모델 파일을 명시적으로 임포트하여 Base.metadata에 등록합니다.
import app.models.user
import app.models.allergy
import app.models.meal
import app.models.onboarding
import app.models.main_health_metric
# 여기에 프로젝트의 다른 모든 모델 파일도 추가해야 합니다.


def init_db():
    print("데이터베이스 초기화 시작...")
    try:
        # 1. 모든 테이블 생성
        # Base.metadata에 등록된 모든 모델을 참조하여 테이블을 생성합니다.
        create_tables(engine)
        print("✅ 모든 테이블 생성이 완료되었습니다.")
        
        # 2. 초기 데이터 (예: 알레르기 목록, 기본 설정 등) 삽입 로직을 여기에 추가 가능
        
        print("데이터베이스 초기화 성공.")
    except Exception as e:
        # DB 연결 문자열 오류, 권한 오류 등 다른 문제 발생 시 로그 출력
        print(f"❌ 데이터베이스 초기화 중 오류 발생: {e}")
        # 배포가 실패하도록 sys.exit(1)을 호출할 수도 있지만, 일단은 로그만 남깁니다.
        sys.exit(1)

if __name__ == "__main__":
    init_db()

import sys
import os

# 프로젝트 루트 경로를 Python 경로에 추가하여 절대 임포트가 가능하도록 합니다.
# (예: from app.core.database import Base)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from app.core.database import engine, create_tables # 방금 추가한 함수 임포트

# 🚨 중요: 모든 ORM 모델 파일을 명시적으로 임포트해야 
# Base.metadata에 해당 테이블 정보가 등록됩니다.
# (이 부분이 빠지면 테이블이 생성되지 않습니다.)
import app.models.user
import app.models.allergy
import app.models.meal
import app.models.onboarding
import app.models.main_health_metric
# 프로젝트에 있는 다른 모델 파일들도 모두 여기에 임포트해야 합니다. 


def init_db():
    print("데이터베이스 초기화 시작...")
    try:
        # 1. 모든 테이블 생성
        create_tables(engine)
        print("✅ 모든 테이블 생성이 완료되었습니다.")
        
        # 2. 초기 데이터 (알레르기 목록 등) 삽입 로직을 여기에 추가 가능
        
        print("데이터베이스 초기화 성공.")
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 중 오류 발생: {e}")
        # 실패 시 로그를 남기고 종료하는 것이 좋음

if __name__ == "__main__":
    init_db()

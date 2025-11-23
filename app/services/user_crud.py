# 사용자 생성(회원가입) 및 조회 로직 구현

from sqlalchemy.orm import Session
from app.models.user import User 
from app.schemas.user import UserCreate
from passlib.context import CryptContext

# 비밀번호 해시를 위한 CryptContext 객체 생성
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# 헬퍼 함수: 비밀번호 해시
def get_password_hash(password: str) -> str:
    safe_password = password
    return pwd_context.hash(safe_password)

# READ (사용자 조회)
def get_user_by_email(db: Session, email: str) -> User | None:
    # 이메일을 통해 DB에서 사용자를 조회
    return db.query(User).filter(User.email == email).first()

# CREATE (사용자 생성: 회원가입 로직)
def create_user(db: Session, user: UserCreate) -> User:
    # 새로운 사용자를 생성하고 DB에 저장
    
    # 비밀번호 해시 처리
    hashed_password = get_password_hash(user.password)
    
    # User 모델 인스턴스 생성
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        gender=user.gender,
        is_terms_agreed=user.is_terms_agreed,
        is_privacy_agreed=user.is_privacy_agreed,
    )
    
    # DB에 추가 및 커밋
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    # ID를 기준으로 사용자 정보를 조회
    return db.query(User).filter(User.id == user_id).first()
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base # app.core.database에서 정의된 Base를 가져옵니다.


# 1. 사용자-알레르기 중간 테이블 정의 (SQLAlchemy Core Table)
# User와 Allergy의 다대다(Many-to-Many) 관계를 연결합니다.
# 이 코드는 User 모델에서 secondary 인수로 사용됩니다.
user_allergy_association = Table(
    'user_allergies', 
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True), # User 테이블의 PK를 참조
    Column('allergy_id', Integer, ForeignKey('allergies.id'), primary_key=True) # Allergy 테이블의 PK를 참조
)


# 2. 알레르기(Allergy) 테이블 모델
class Allergy(Base):
    """
    개별 알레르기 항목 정보를 저장하는 테이블 모델.
    """
    __tablename__ = "allergies"

    # 고유 ID
    id = Column(Integer, primary_key=True, index=True)
    
    # 알레르기 이름 (예: 땅콩, 우유, 꽃가루)
    name = Column(String(100), unique=True, nullable=False) 

    # 관계 (Relationships)
    # User 모델과의 다대다 관계 설정.
    # secondary 인수로 위에서 정의한 중간 테이블을 사용합니다.
    # User 모델에서 back_populates="users"로 설정해야 합니다.
    users = relationship(
        "User", 
        secondary=user_allergy_association, 
        back_populates="allergies"
        
    )

    recipes = relationship("RecipeAllergen", back_populates="allergy")

    ingredients_allergens = relationship("IngredientAllergen", back_populates="allergy")

    def __repr__(self):
        return f"<Allergy(id={self.id}, name='{self.name}')>"

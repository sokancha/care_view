from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base # app.core.database에서 정의된 Base를 가져옵니다.


user_allergy_association = Table(
    'user_allergies', 
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True), # User 테이블의 PK를 참조
    Column('allergy_id', Integer, ForeignKey('allergies.id'), primary_key=True) # Allergy 테이블의 PK를 참조
)

class Allergy(Base):
    """
    개별 알레르기 항목 정보를 저장하는 테이블 모델.
    """
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(100), unique=True, nullable=False) 

    users = relationship(
        "User", 
        secondary=user_allergy_association, 
        back_populates="allergies"
        
    )

    recipes = relationship("RecipeAllergen", back_populates="allergy")

    ingredients_allergens = relationship("IngredientAllergen", back_populates="allergy")

    def __repr__(self):
        return f"<Allergy(id={self.id}, name='{self.name}')>"

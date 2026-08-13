from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class RecipeSet(Base):
    """편의점 식단 추천의 전체 세트(고단백 샐러드 세트 등) 정의."""
    __tablename__ = "recipe_sets"

    set_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255), nullable=False)           
    set_type = Column(String(50), nullable=False)        
    image_url = Column(String(500), nullable=True)       
    
    total_calorie = Column(Float, nullable=False)        
    total_carbs = Column(Float, nullable=False)          
    total_protein = Column(Float, nullable=False)        
    total_fat = Column(Float, nullable=False)            
    
    composition = relationship("SetComposition", back_populates="recipe_set")


class ConvenienceItem(Base):
    """레시피를 구성하는 개별 편의점 상품 목록 (영양 정보 원본)."""
    __tablename__ = "convenience_items"

    item_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255), nullable=False, unique=True) # 상품명 (예: '닭가슴살 샐러드 (1개, 200g)')
    
    calorie = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)

    recipe_sets = relationship("SetComposition", back_populates="item")


class SetComposition(Base):
    """레시피(세트)가 어떤 상품(ConvenienceItem)으로 구성되었는지 정의하는 M:N 관계 테이블"""
    __tablename__ = "set_composition"

    set_id = Column(Integer, ForeignKey("recipe_sets.set_id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("convenience_items.item_id"), primary_key=True)
    
    amount = Column(Float, nullable=False)                   
    unit = Column(String(50), nullable=False)                

    recipe_set = relationship("RecipeSet", back_populates="composition")
    item = relationship("ConvenienceItem", back_populates="recipe_sets")

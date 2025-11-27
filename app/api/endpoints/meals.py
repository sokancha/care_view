from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from app.core.database import get_db 
from app.schemas.meal import MainRecommendationSchema
from app.services.meal_service import get_main_page_recommendations


router = APIRouter()

@router.get("/recommendations/main", response_model=MainRecommendationSchema)
async def get_main_recommendations(
    db: AsyncSession = Depends(get_db), 
):
    user_id = 1 
    
    recommendations = await get_main_page_recommendations(db, user_id)
    
    return MainRecommendationSchema(**recommendations)
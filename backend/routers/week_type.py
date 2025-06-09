from fastapi import APIRouter
from services.week_type_service import week_type_service

router = APIRouter()

#Отримати поточний тип тижня (чисельник/знаменник)
@router.get("/week-type")
async def get_current_week_type():
    return week_type_service.get_current_week_type() 
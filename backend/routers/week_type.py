from fastapi import APIRouter, Query
from services.week_type_service import week_type_service

router = APIRouter()

#Отримати поточний тип тижня (чисельник/знаменник)
@router.get("/week-type")
async def get_current_week_type():
    return week_type_service.get_current_week_type()

@router.get("/week-type/range")
async def get_week_type_for_range(
    start_date: str = Query(..., description="Початкова дата у форматі YYYY-MM-DD"),
    end_date: str = Query(..., description="Кінцева дата у форматі YYYY-MM-DD")
):
    return week_type_service.get_week_type_for_date_range(start_date, end_date) 
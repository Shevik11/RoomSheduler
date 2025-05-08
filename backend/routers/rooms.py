from fastapi import APIRouter, Query
from typing import Optional, List
from dependencies.database import get_db

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)

@router.get("/suggestions/", response_model=List[str])
async def get_room_suggestions(
    query: str = Query(None, description="Search query for room number"),
    name_group: Optional[str] = None,
    number_of_subgroup: Optional[int] = None,
    day_of_week: Optional[str] = None,
    nominator: Optional[str] = None,
    number_of_para: Optional[int] = None,
    name_of_para: Optional[str] = None,
    teacher: Optional[str] = None,
    busy: Optional[bool] = None
):
    # Build your base query
    base_query = """
        SELECT DISTINCT room 
        FROM schedule 
        WHERE 1=1
    """
    params = []
    
    # Add filters based on provided parameters
    if query:
        base_query += " AND room ILIKE %s"
        params.append(f"%{query}%")
    
    if name_group:
        base_query += " AND name_group = %s"
        params.append(name_group)
    
    if number_of_subgroup is not None:
        base_query += " AND number_of_subgroup = %s"
        params.append(number_of_subgroup)
    
    if day_of_week:
        base_query += " AND day_of_week = %s"
        params.append(day_of_week)
    
    if nominator:
        base_query += " AND nominator = %s"
        params.append(nominator)
    
    if number_of_para is not None:
        base_query += " AND number_of_para = %s"
        params.append(number_of_para)
    
    if name_of_para:
        base_query += " AND name_of_para ILIKE %s"
        params.append(f"%{name_of_para}%")
    
    if teacher:
        base_query += " AND teacher ILIKE %s"
        params.append(f"%{teacher}%")
    
    if busy is not None:
        base_query += " AND busy = %s"
        params.append(busy)
    
    # Add order by to sort results
    base_query += " ORDER BY room"
    
    # Execute query and return results
    database = await get_db()
    results = await database.fetch_all(base_query, params)
    return [row["room"] for row in results] 
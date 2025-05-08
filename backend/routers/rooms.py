from fastapi import APIRouter, Query, Depends
from typing import Optional, List
from dependencies.database import get_db
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

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
    busy: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    # Build your base query
    base_query = """
        SELECT DISTINCT room 
        FROM schedule 
        WHERE 1=1
    """
    params = {}
    
    # Add filters based on provided parameters
    if query:
        base_query += " AND room ILIKE :query"
        params["query"] = f"%{query}%"
    
    if name_group:
        base_query += " AND name_group = :name_group"
        params["name_group"] = name_group
    
    if number_of_subgroup is not None:
        base_query += " AND number_of_subgroup = :number_of_subgroup"
        params["number_of_subgroup"] = number_of_subgroup
    
    if day_of_week:
        base_query += " AND day_of_week = :day_of_week"
        params["day_of_week"] = day_of_week
    
    if nominator:
        base_query += " AND nominator = :nominator"
        params["nominator"] = nominator
    
    if number_of_para is not None:
        base_query += " AND number_of_para = :number_of_para"
        params["number_of_para"] = number_of_para
    
    if name_of_para:
        base_query += " AND name_of_para ILIKE :name_of_para"
        params["name_of_para"] = f"%{name_of_para}%"
    
    if teacher:
        base_query += " AND teacher ILIKE :teacher"
        params["teacher"] = f"%{teacher}%"
    
    if busy is not None:
        base_query += " AND busy = :busy"
        params["busy"] = busy
    
    # Add order by to sort results
    base_query += " ORDER BY room"
    
    # Execute query and return results
    stmt = text(base_query)
    result = db.execute(stmt, params)
    rows = result.all()
    return [row[0] for row in rows] 
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.models import Days
from dependencies.database import get_db
from fastapi.responses import JSONResponse
from typing import List

router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)

@router.get("/suggestions/", response_model=List[str])
def get_group_suggestions(
    query: str = Query(None, description="Search query for group name"),
    number_of_subgroup: int | None = None,
    day_of_week: str | None = None,
    nominator: str | None = None,
    namb_of_para: int | None = None,
    name_of_para: str | None = None,
    room: str | None = None,
    teacher: str | None = None,
    busy: bool | None = None,
    db: Session = Depends(get_db),
):
    db_query = db.query(Days.name_group).distinct()

    if query:
        db_query = db_query.filter(Days.name_group.ilike(f"%{query}%"))
    if number_of_subgroup:
        db_query = db_query.filter(Days.number_of_subgroup == number_of_subgroup)
    if day_of_week:
        db_query = db_query.filter(Days.day_of_week == day_of_week)
    if nominator:
        db_query = db_query.filter(Days.nominator == nominator)
    if namb_of_para:
        db_query = db_query.filter(Days.namb_of_para == namb_of_para)
    if name_of_para:
        db_query = db_query.filter(Days.name_of_para.ilike(f"%{name_of_para}%"))
    if room:
        db_query = db_query.filter(Days.room == room)
    if teacher:
        db_query = db_query.filter(Days.teacher.ilike(f"%{teacher}%"))
    if busy is not None:
        db_query = db_query.filter(Days.busy == busy)

    groups = [group[0] for group in db_query.all() if group[0]]
    return groups 
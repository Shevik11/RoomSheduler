from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.models import Days
from dependencies.database import get_db
from fastapi.responses import JSONResponse
from typing import List

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)

@router.get("/suggestions/", response_model=List[str])
def get_room_suggestions(
    query: str = Query(None, description="Search query for room number"),
    name_group: str | None = None,
    number_of_subgroup: int | None = None,
    day_of_week: str | None = None,
    nominator: str | None = None,
    namb_of_para: int | None = None,
    name_of_para: str | None = None,
    teacher: str | None = None,
    busy: bool | None = None,
    db: Session = Depends(get_db),
):
    db_query = db.query(Days.room).distinct()

    if query:
        db_query = db_query.filter(Days.room.ilike(f"%{query}%"))
    if name_group:
        db_query = db_query.filter(Days.name_group == name_group)
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
    if teacher:
        db_query = db_query.filter(Days.teacher.ilike(f"%{teacher}%"))
    if busy is not None:
        db_query = db_query.filter(Days.busy == busy)

    rooms = [room[0] for room in db_query.all() if room[0]]
    return rooms

@router.get("/all_rooms/")
def get_all_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Days.room).distinct().all()
    return JSONResponse(content=[room[0] for room in rooms if room[0]])

@router.get("/busy_rooms/")
def get_busy_rooms(
    name_group: str | None = Query(None),
    number_of_subgroup: int | None = Query(None),
    day_of_week: str | None = Query(None),
    nominator: str | None = Query(None),
    time_of_para: str | None = Query(None),
    namb_of_para: int | None = Query(None),
    name_of_para: str | None = Query(None),
    teacher: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Days.room).distinct().filter(Days.busy == True)

    if name_group:
        query = query.filter(Days.name_group == name_group)
    if number_of_subgroup:
        query = query.filter(Days.number_of_subgroup == number_of_subgroup)
    if day_of_week:
        query = query.filter(Days.day_of_week == day_of_week)
    if nominator:
        query = query.filter(Days.nominator == nominator)
    if namb_of_para:
        query = query.filter(Days.namb_of_para == namb_of_para)
    if name_of_para:
        query = query.filter(Days.name_of_para.ilike(f"%{name_of_para}%"))
    if teacher:
        query = query.filter(Days.teacher.ilike(f"%{teacher}%"))

    rooms = [room[0] for room in query.all() if room[0]]
    return JSONResponse(content=rooms)

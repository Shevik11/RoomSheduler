from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.models import Days
from dependencies.database import get_db
from typing import List
from sqlalchemy import distinct

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"]
)

@router.get("/suggestions/", response_model=List[str])
def get_lesson_suggestions(
    query: str = Query(None, description="Search query for subject name"),
    name_group: str | None = None,
    number_of_subgroup: int | None = None,
    day_of_week: str | None = None,
    nominator: str | None = None,
    namb_of_para: int | None = None,
    room: str | None = None,
    teacher: str | None = None,
    busy: bool | None = None,
    db: Session = Depends(get_db),
):
    db_query = db.query(Days.name_of_para).distinct()

    if query:
        db_query = db_query.filter(Days.name_of_para.ilike(f"%{query}%"))
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
    if room:
        db_query = db_query.filter(Days.room == room)
    if teacher:
        db_query = db_query.filter(Days.teacher.ilike(f"%{teacher}%"))
    if busy is not None:
        db_query = db_query.filter(Days.busy == busy)

    lessons = [lesson[0] for lesson in db_query.all() if lesson[0]]
    return lessons 


@router.get('/all/')
def get_all_subjects(db: Session = Depends(get_db)):
    subjects = db.query(distinct(Days.name_of_para)).filter(Days.name_of_para != '').all()
    return [subject[0] for subject in subjects]
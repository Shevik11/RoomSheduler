from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.models import Days
from services.days import fetch_days_by_filters
from dependencies.database import get_db
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/all_days/')
def get_all_days(db: Session = Depends(get_db)):
    days = db.query(Days).all()
    result_list = []
    for day in days:
        day_dict = day.__dict__.copy()
        if "_sa_instance_state" in day_dict:
            del day_dict["_sa_instance_state"]
        result_list.append(day_dict)
    return JSONResponse(content=result_list)

@router.get("/days/")
def get_days(
        name_group: str | None = Query(None),
        number_of_subgroup: int | None = Query(None),
        day_of_week: str | None = Query(None),
        nominator: str | None = Query(None),
        time_of_para: str | None = Query(None),
        namb_of_para: int | None = Query(None),
        name_of_para: str | None = Query(None),
        room: str | None = Query(default=None),
        teacher: str | None = Query(None),
        busy: bool | None = Query(None),
        db: Session = Depends(get_db),
):
    return fetch_days_by_filters(
        db=db,
        name_group=name_group,
        number_of_subgroup=number_of_subgroup,
        day_of_week=day_of_week,
        nominator=nominator,
        time_of_para=time_of_para,
        namb_of_para=namb_of_para,
        name_of_para=name_of_para,
        room=room,
        teacher=teacher,
        busy=busy
    )




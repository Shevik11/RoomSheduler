from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from bd import get_db
from models import Days
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/all_days/')
def get_all_days(db: Session = Depends(get_db)):
    days = db.query(Days).all()

    # Створюємо список словників вручну
    result_list = []
    for day in days:
        day_dict = day.__dict__.copy()
        if "_sa_instance_state" in day_dict:
            del day_dict["_sa_instance_state"]
        result_list.append(day_dict)

    return JSONResponse(content=result_list)


@app.get("/days/")
def get_days(
        name_group: str = Query(None),
        number_of_subgroup: int = Query(None),
        day_of_week: str = Query(None),
        nominator: str = Query(None),
        time_of_para: str = Query(None),
        namb_of_para: int = Query(None),
        name_of_para: str = Query(None),
        room: str = Query(None),
        teacher: str = Query(None),
        busy: bool = Query(None),
        db: Session = Depends(get_db),
):
    # Будуємо SQL запит вручну
    sql_query = "SELECT * FROM days WHERE 1=1"
    params = {}

    if name_group:
        sql_query += " AND name_group = :name_group"
        params["name_group"] = name_group
    if number_of_subgroup:
        sql_query += " AND number_of_subgroup = :number_of_subgroup"
        params["number_of_subgroup"] = number_of_subgroup
    if day_of_week:
        sql_query += " AND day_of_week = :day_of_week"
        params["day_of_week"] = day_of_week
    if nominator:
        sql_query += " AND nominator = :nominator"
        params["nominator"] = nominator
    if time_of_para:
        sql_query += " AND time_of_para = :time_of_para"
        params["time_of_para"] = time_of_para
    if namb_of_para:
        sql_query += " AND namb_of_para = :namb_of_para"
        params["namb_of_para"] = namb_of_para
    if name_of_para:
        sql_query += " AND name_of_para = :name_of_para"
        params["name_of_para"] = name_of_para
    if room:
        sql_query += " AND room = :room"
        params["room"] = room
    if teacher:
        sql_query += " AND teacher = :teacher"
        params["teacher"] = teacher
    if busy is not None:
        sql_query += " AND busy = :busy"
        params["busy"] = busy

    # Виконуємо запит напряму
    result = db.execute(text(sql_query), params)

    # Отримуємо всі рядки і конвертуємо їх у словники
    rows = result.fetchall()

    # Отримуємо імена колонок
    column_names = result.keys()

    # Створюємо список словників
    result_list = []
    for row in rows:
        row_dict = {}
        for i, column in enumerate(column_names):
            row_dict[column] = row[i]
        result_list.append(row_dict)

    print(f"Загальна кількість рядків: {len(result_list)}")

    return JSONResponse(content=result_list)
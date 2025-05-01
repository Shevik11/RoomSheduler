from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
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
    result_list = []
    for day in days:
        day_dict = day.__dict__.copy()
        if "_sa_instance_state" in day_dict:
            del day_dict["_sa_instance_state"]
        result_list.append(day_dict)
    return JSONResponse(content=result_list)


@app.get("/days/")
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
    sql_query = "SELECT * FROM schedule WHERE 1=1"
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

    result = db.execute(text(sql_query), params)
    rows = result.fetchall()
    column_names = result.keys()

    result_list = []
    for row in rows:
        row_dict = {}
        for i, column in enumerate(column_names):
            row_dict[column] = row[i]
        result_list.append(row_dict)

    return JSONResponse(content=result_list)


@app.get("/room_schedule/")
def get_room_schedule(
    room: str = Query(..., description="Номер аудиторії (наприклад: '1/Б')"),
    db: Session = Depends(get_db)
):
    print(room)
    try:
        # Отримуємо всі пари для цієї аудиторії
        query = text("""
                    SELECT * 
                    FROM schedule
                    WHERE room = :room
                """)

        room_schedule = db.execute(query, {"room": room.strip()}).fetchall()
        print(f"SQL запит знайшов {len(room_schedule)} записів для аудиторії '{room}'")
        # Дні тижня (без суботи)
        days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "Пятниця"]
        paras = range(1, 9)  # Пари з 1 по 8

        # Час пар
        para_times = {
            1: '8:30-10:05',
            2: '10:25-12:00',
            3: '12:20-13:55',
            4: '14:15-15:50',
            5: '16:10-17:45',
            6: '18:05-19:40',
            7: '19:50-21:25',
            8: '21:35-23:10'
        }

        result = {}

        # Створюємо словник для швидкого пошуку розкладу
        schedule_dict = {}
        for item in room_schedule:
            key = (item.day_of_week, item.namb_of_para)
            if key not in schedule_dict:
                schedule_dict[key] = []
            schedule_dict[key].append(item)

        for day in days:
            day_schedule = []
            for para in paras:
                key = (day, para)
                scheduled_items = schedule_dict.get(key, [])

                # Якщо є записи для цього дня і пари
                if scheduled_items:
                    for scheduled in scheduled_items:
                        day_schedule.append({
                            "para": para,
                            "time": para_times.get(para, ''),
                            "status": "Зайнято",
                            "group": scheduled.name_group,
                            "subject": scheduled.name_of_para,
                            "teacher": scheduled.teacher
                        })
                else:
                    day_schedule.append({
                        "para": para,
                        "time": para_times.get(para, ''),
                        "status": "Вільно",
                        "group": None,
                        "subject": None,
                        "teacher": None
                    })

            result[day] = day_schedule

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn  # для FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)
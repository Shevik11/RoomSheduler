from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from models.models import Days
from shemas.day import Days

def fetch_days_by_filters(
    db: Session,
    name_group: str | None,
    number_of_subgroup: int | None,
    day_of_week: str | None,
    nominator: str | None,
    time_of_para: str | None,
    namb_of_para: int | None,
    name_of_para: str | None,
    room: str | None,
    teacher: str | None,
    busy: bool | None,
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


def fetch_room_schedule(room: str, db: Session):
    try:
        query = text("SELECT * FROM schedule WHERE room = :room")
        room_schedule = db.execute(query, {"room": room.strip()}).fetchall()

        days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "Пятниця"]
        paras = range(1, 9)
        para_times = {
            1: '8:30-10:05', 2: '10:25-12:00', 3: '12:20-13:55', 4: '14:15-15:50',
            5: '16:10-17:45', 6: '18:05-19:40', 7: '19:50-21:25', 8: '21:35-23:10'
        }

        result = {}
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

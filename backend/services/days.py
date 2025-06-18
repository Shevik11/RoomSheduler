from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.models import Days
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    query = db.query(Days)
    
    logger.info(f"Filtering with name_group: {name_group}")

    if name_group:
        query = query.filter(Days.name_group == name_group)
    if number_of_subgroup:
        query = query.filter((Days.number_of_subgroup == number_of_subgroup) | (Days.number_of_subgroup == 0))
    if day_of_week:
        query = query.filter(Days.day_of_week == day_of_week)
    if nominator:
        query = query.filter((Days.nominator == nominator) | (Days.nominator == 'both'))
    if namb_of_para:
        query = query.filter(Days.namb_of_para == namb_of_para)
    if name_of_para:
        query = query.filter(Days.name_of_para.ilike(f"%{name_of_para}%"))
    if room:
        query = query.filter(Days.room == room)
    if teacher:
        query = query.filter(Days.teacher.ilike(f"%{teacher}%"))
    if busy is not None:
        query = query.filter(Days.busy == busy)

    results = query.all()
    logger.info(f"Found {len(results)} results")
    
    result_list = [{
        column.name: getattr(row, column.name)
        for column in row.__table__.columns
    } for row in results]

    logger.info(f"Returning {len(result_list)} items")
    return result_list


def fetch_room_schedule(room: str, db: Session):
    try:
        room_schedule = db.query(Days).filter(Days.room == room.strip()).all()

        days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця"]
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

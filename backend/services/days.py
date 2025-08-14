import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.models import Days

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_days_by_filters(
    db: Session,
    name_group: str | None,
    number_of_subgroup: int | None,
    day_of_week: str | None,
    nominator: str | None,
    time_of_para: str | None,  # Currently unused but kept for API compatibility
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
        query = query.filter(
            (Days.number_of_subgroup == number_of_subgroup)
            | (Days.number_of_subgroup == 0)
        )
    if day_of_week:
        query = query.filter(Days.day_of_week == day_of_week)
    if nominator:
        query = query.filter((Days.nominator == nominator) | (Days.nominator == "both"))
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

    result_list = [
        {column.name: getattr(row, column.name) for column in row.__table__.columns}
        for row in results
    ]

    logger.info(f"Returning {len(result_list)} items")
    return result_list


def fetch_room_schedule(room: str, db: Session):
    try:
        room_schedule = db.query(Days).filter(Days.room == room.strip()).all()

        days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]
        paras = range(1, 9)
        para_times = {
            1: "8:30-10:05",
            2: "10:25-12:00",
            3: "12:20-13:55",
            4: "14:15-15:50",
            5: "16:10-17:45",
            6: "18:05-19:40",
            7: "19:50-21:25",
            8: "21:35-23:10",
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
                        day_schedule.append(
                            {
                                "para": para,
                                "time": para_times.get(para, ""),
                                "status": "Зайнято",
                                "group": scheduled.name_group,
                                "subject": scheduled.name_of_para,
                                "teacher": scheduled.teacher,
                            }
                        )
                else:
                    day_schedule.append(
                        {
                            "para": para,
                            "time": para_times.get(para, ""),
                            "status": "Вільно",
                            "group": None,
                            "subject": None,
                            "teacher": None,
                        }
                    )

            result[day] = day_schedule

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_occupied_slots(scheduled_periods):
    """Extract occupied time slots from scheduled periods."""
    occupied_slots = set()
    for period in scheduled_periods:
        if period.nominator == "both":
            occupied_slots.add((period.day_of_week, period.namb_of_para, "numerator"))
            occupied_slots.add((period.day_of_week, period.namb_of_para, "denominator"))
        else:
            occupied_slots.add((period.day_of_week, period.namb_of_para, period.nominator))
    return occupied_slots


def _get_schedule_constants():
    """Get schedule constants for days and para times."""
    days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]
    paras = range(1, 9)
    para_times = {
        1: "8:30-10:05",
        2: "10:25-12:00",
        3: "12:20-13:55",
        4: "14:15-15:50",
        5: "16:10-17:45",
        6: "18:05-19:40",
        7: "19:50-21:25",
        8: "21:35-23:10",
    }
    return days, paras, para_times


def _get_nominators_to_check(nominator):
    """Determine which nominators to check based on input."""
    return [nominator] if nominator else ["numerator", "denominator"]


def _create_free_slot(day, para, nom, group_name, para_times):
    """Create a free slot dictionary."""
    return {
        "day_of_week": day,
        "namb_of_para": para,
        "time_of_para": para_times.get(para, ""),
        "name_of_para": "Вільно",
        "room": "",
        "teacher": "",
        "number_of_subgroup": None,
        "nominator": nom,
        "busy": False,
        "name_group": group_name,
        "key": f"{day}-{para}-Вільно-{group_name}-{nom}",
        "groups": [group_name],
    }


def fetch_group_free_slots(db: Session, group_name: str, nominator: str | None = None):
    """
    Find all free time slots for a specific group by identifying periods
    where the group doesn't have scheduled classes.
    """
    try:
        # Get all scheduled periods for the group
        scheduled_query = db.query(Days).filter(Days.name_group == group_name)
        
        if nominator:
            scheduled_query = scheduled_query.filter(
                (Days.nominator == nominator) | (Days.nominator == "both")
            )
        
        scheduled_periods = scheduled_query.all()
        occupied_slots = _get_occupied_slots(scheduled_periods)
        
        days, paras, para_times = _get_schedule_constants()
        nominators_to_check = _get_nominators_to_check(nominator)
        
        # Find free slots
        free_slots = []
        for day in days:
            for para in paras:
                for nom in nominators_to_check:
                    slot = (day, para, nom)
                    if slot not in occupied_slots:
                        free_slot = _create_free_slot(day, para, nom, group_name, para_times)
                        free_slots.append(free_slot)
        
        logger.info(f"Found {len(free_slots)} free slots for group {group_name}")
        return free_slots
        
    except Exception as e:
        logger.error(f"Error fetching free slots for group {group_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
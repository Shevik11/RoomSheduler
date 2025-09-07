import hashlib
import json
from typing import List

import redis.asyncio as redis
from fastapi import APIRouter, Depends, Query
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.redis import get_redis
from models.models import Days

router = APIRouter(prefix="/teachers", tags=["teachers"])


def generate_teachers_cache_key(**kwargs):
    params_str = "&".join(
        [f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None]
    )
    return f"teachers_suggestions:{hashlib.sha512(params_str.encode()).hexdigest()}"


@router.get("/suggestions/", response_model=List[str])
async def get_teacher_suggestions(
    query: str = Query(None, description="Search query for teacher name"),
    name_group: str | None = None,
    number_of_subgroup: int | None = None,
    day_of_week: str | None = None,
    nominator: str | None = None,
    namb_of_para: int | None = None,
    name_of_para: str | None = None,
    room: str | None = None,
    busy: bool | None = None,
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
):

    cache_key = generate_teachers_cache_key(
        query=query,
        name_group=name_group,
        number_of_subgroup=number_of_subgroup,
        day_of_week=day_of_week,
        nominator=nominator,
        namb_of_para=namb_of_para,
        name_of_para=name_of_para,
        room=room,
        busy=busy,
    )


    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    db_query = db.query(Days.teacher).distinct()

    if query:
        db_query = db_query.filter(Days.teacher.ilike(f"%{query}%"))
    if name_group:
        db_query = db_query.filter(Days.name_group == name_group)
    if number_of_subgroup:
        db_query = db_query.filter(
            (Days.number_of_subgroup == number_of_subgroup)
            | (Days.number_of_subgroup == 0)
        )
    if day_of_week:
        db_query = db_query.filter(Days.day_of_week == day_of_week)
    if nominator:
        db_query = db_query.filter(
            (Days.nominator == nominator) | (Days.nominator == "both")
        )
    if namb_of_para:
        db_query = db_query.filter(Days.namb_of_para == namb_of_para)
    if name_of_para:
        db_query = db_query.filter(Days.name_of_para.ilike(f"%{name_of_para}%"))
    if room:
        db_query = db_query.filter(Days.room == room)
    if busy is not None:
        db_query = db_query.filter(Days.busy == busy)

    teachers = [teacher[0] for teacher in db_query.all() if teacher[0]]


    await redis_client.setex(cache_key, 600, json.dumps(teachers))

    return teachers


@router.get("/all/")
async def get_all_teachers(
    db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)
):
    cache_key = "teachers_all_teachers"


    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    teachers = db.query(distinct(Days.teacher)).filter(Days.teacher != "").all()
    result = [teacher[0] for teacher in teachers]


    await redis_client.setex(cache_key, 1800, json.dumps(result))

    return result


@router.delete("/cache/clear")
async def clear_teachers_cache(redis_client: redis.Redis = Depends(get_redis)):

    keys = await redis_client.keys("teachers_suggestions:*")
    all_teachers_key = await redis_client.keys("teachers_all_teachers")
    keys.extend(all_teachers_key)
    if keys:
        await redis_client.delete(*keys)
    return {"message": f"Cleared {len(keys)} cache entries"}

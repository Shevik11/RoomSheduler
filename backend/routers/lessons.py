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

router = APIRouter(prefix="/lessons", tags=["lessons"])


def generate_lessons_cache_key(**kwargs):
    # generate cache key
    params_str = "&".join(
        [f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None]
    )
    return f"lessons_suggestions:{hashlib.sha512(params_str.encode()).hexdigest()}"


@router.get("/suggestions/", response_model=List[str])
async def get_lesson_suggestions(
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
    redis_client: redis.Redis = Depends(get_redis),
):
    # generate cache key
    cache_key = generate_lessons_cache_key(
        query=query,
        name_group=name_group,
        number_of_subgroup=number_of_subgroup,
        day_of_week=day_of_week,
        nominator=nominator,
        namb_of_para=namb_of_para,
        room=room,
        teacher=teacher,
        busy=busy,
    )

    # try to get data from cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    db_query = db.query(Days.name_of_para).distinct()

    if query:
        db_query = db_query.filter(Days.name_of_para.ilike(f"%{query}%"))
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
    if room:
        db_query = db_query.filter(Days.room == room)
    if teacher:
        db_query = db_query.filter(Days.teacher.ilike(f"%{teacher}%"))
    if busy is not None:
        db_query = db_query.filter(Days.busy == busy)

    lessons = [lesson[0] for lesson in db_query.all() if lesson[0]]

    # save to cache
    await redis_client.setex(cache_key, 600, json.dumps(lessons))

    return lessons


@router.get("/all/")
async def get_all_subjects(
    db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)
):
    cache_key = "lessons_all_subjects"

    # try to get data from cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    subjects = (
        db.query(distinct(Days.name_of_para)).filter(Days.name_of_para != "").all()
    )
    result = [subject[0] for subject in subjects]

    # save to cache
    await redis_client.setex(cache_key, 1800, json.dumps(result))

    return result


@router.delete("/cache/clear")
async def clear_lessons_cache(redis_client: redis.Redis = Depends(get_redis)):
    # clear cache for lessons
    keys = await redis_client.keys("lessons_suggestions:*")
    all_subjects_key = await redis_client.keys("lessons_all_subjects")
    keys.extend(all_subjects_key)
    if keys:
        await redis_client.delete(*keys)
    return {"message": f"Cleared {len(keys)} cache entries"}

import hashlib
import json
from typing import List

import redis.asyncio as redis
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.redis import get_redis
from models.models import Days
from services.days import fetch_room_schedule

router = APIRouter(prefix="/rooms", tags=["rooms"])


def generate_rooms_cache_key(**kwargs):
    # generate cache key
    params_str = "&".join(
        [f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None]
    )
    return f"rooms_suggestions:{hashlib.sha512(params_str.encode()).hexdigest()}"


def generate_busy_rooms_cache_key(**kwargs):
    # generate cache key
    params_str = "&".join(
        [f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None]
    )
    return f"rooms_busy:{hashlib.sha512(params_str.encode()).hexdigest()}"


@router.get("/suggestions/")
async def get_room_suggestions(
    query: str = "",
    name_group: str = None,
    day_of_week: str = None,
    nominator: str = None,
    namb_of_para: int = None,
    teacher: str = None,
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
):
    # generate cache key
    cache_key = generate_rooms_cache_key(
        query=query,
        name_group=name_group,
        day_of_week=day_of_week,
        nominator=nominator,
        namb_of_para=namb_of_para,
        teacher=teacher,
    )

    # try to get data from cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    q = db.query(Days.room).filter(Days.room != "")
    if query:
        q = q.filter(Days.room.ilike(f"%{query}%"))
    if name_group:
        q = q.filter(Days.name_group == name_group)
    if day_of_week:
        q = q.filter(Days.day_of_week == day_of_week)
    if nominator:
        q = q.filter((Days.nominator == nominator) | (Days.nominator == "both"))
    if namb_of_para:
        q = q.filter(Days.namb_of_para == namb_of_para)
    if teacher:
        q = q.filter(Days.teacher.ilike(f"%{teacher}%"))
    rooms = q.distinct().all()
    result = [room[0] for room in rooms]

    # save to cache
    await redis_client.setex(cache_key, 600, json.dumps(result))

    return result


@router.get("/all_rooms/")
async def get_all_rooms(
    db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)
):
    cache_key = "rooms_all_rooms"

    # try to get data from cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return JSONResponse(content=json.loads(cached_data))

    rooms = db.query(Days.room).distinct().all()
    result = [room[0] for room in rooms if room[0]]

    # save to cache
    await redis_client.setex(cache_key, 1800, json.dumps(result))

    return JSONResponse(content=result)


@router.get("/busy_rooms/")
async def get_busy_rooms(
    name_group: str | None = Query(None),
    number_of_subgroup: int | None = Query(None),
    day_of_week: str | None = Query(None),
    nominator: str | None = Query(None),
    time_of_para: str | None = Query(None),
    namb_of_para: int | None = Query(None),
    name_of_para: str | None = Query(None),
    teacher: str | None = Query(None),
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
):
    # generate cache key
    cache_key = generate_busy_rooms_cache_key(
        name_group=name_group,
        number_of_subgroup=number_of_subgroup,
        day_of_week=day_of_week,
        nominator=nominator,
        time_of_para=time_of_para,
        namb_of_para=namb_of_para,
        name_of_para=name_of_para,
        teacher=teacher,
    )

    # try to get data from cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return JSONResponse(content=json.loads(cached_data))

    query = db.query(Days.room).distinct().filter(Days.busy == True)

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
    if teacher:
        query = query.filter(Days.teacher.ilike(f"%{teacher}%"))

    rooms = [room[0] for room in query.all() if room[0]]

    # save to cache
    await redis_client.setex(cache_key, 300, json.dumps(rooms))

    return JSONResponse(content=rooms)


@router.get("/schedule/")
async def get_room_schedule(
    room: str = Query(..., description="Номер аудиторії (наприклад: '1/Б')"),
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
):
    cache_key = f"room_schedule:{hashlib.sha512(room.encode()).hexdigest()}"

    # try to get data from cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    result = fetch_room_schedule(room, db)

    # save to cache
    await redis_client.setex(cache_key, 600, json.dumps(result))

    return result


@router.delete("/cache/clear")
async def clear_rooms_cache(redis_client: redis.Redis = Depends(get_redis)):
    # clear cache for rooms
    keys = await redis_client.keys("rooms_suggestions:*")
    busy_keys = await redis_client.keys("rooms_busy:*")
    schedule_keys = await redis_client.keys("room_schedule:*")
    all_keys = await redis_client.keys("rooms_all_rooms")
    keys.extend(busy_keys)
    keys.extend(schedule_keys)
    keys.extend(all_keys)
    if keys:
        await redis_client.delete(*keys)
    return {"message": f"Cleared {len(keys)} cache entries"}

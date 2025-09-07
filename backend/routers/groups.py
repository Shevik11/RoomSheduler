import hashlib
import json
import logging
from typing import List

import redis.asyncio as redis
from fastapi import APIRouter, Depends, Query
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.redis import get_redis, safe_redis_operation
from models.models import Days

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/groups", tags=["groups"])


def generate_groups_cache_key(**kwargs):
    params_str = "&".join(
        [f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None]
    )
    return f"groups_suggestions:{hashlib.sha512(params_str.encode()).hexdigest()}"


@router.get("/suggestions/", response_model=List[str])
async def get_group_suggestions(
    query: str = Query(None, description="Search query for group name"),
    number_of_subgroup: int | None = None,
    day_of_week: str | None = None,
    nominator: str | None = None,
    namb_of_para: int | None = None,
    name_of_para: str | None = None,
    room: str | None = None,
    teacher: str | None = None,
    busy: bool | None = None,
    db: Session = Depends(get_db),
):
    cache_key = generate_groups_cache_key(
        query=query,
        number_of_subgroup=number_of_subgroup,
        day_of_week=day_of_week,
        nominator=nominator,
        namb_of_para=namb_of_para,
        name_of_para=name_of_para,
        room=room,
        teacher=teacher,
        busy=busy,
    )

    try:

        async def get_cached_data(redis_client):
            return await redis_client.get(cache_key)

        cached_data = await safe_redis_operation(get_cached_data)
        if cached_data:
            logger.info(f"Retrieved groups data from cache for key: {cache_key}")
            return json.loads(cached_data)
    except Exception as e:
        logger.warning(f"Failed to retrieve from cache, falling back to database: {e}")

    logger.info("Fetching groups data from database")
    db_query = db.query(Days.name_group).distinct()

    if query:
        db_query = db_query.filter(Days.name_group.ilike(f"%{query}%"))
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
    if teacher:
        db_query = db_query.filter(Days.teacher.ilike(f"%{teacher}%"))
    if busy is not None:
        db_query = db_query.filter(Days.busy == busy)

    groups = [group[0] for group in db_query.all() if group[0]]

    try:

        async def cache_data(redis_client):
            await redis_client.setex(cache_key, 600, json.dumps(groups))
            return True

        await safe_redis_operation(cache_data)
        logger.info(f"Cached groups data for key: {cache_key}")
    except Exception as e:
        logger.warning(f"Failed to cache data, continuing without cache: {e}")

    return groups


@router.get("/all/")
async def get_all_groups(
    db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)
):
    cache_key = "groups_all_groups"

    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    groups = db.query(distinct(Days.name_group)).filter(Days.name_group != "").all()
    result = [group[0] for group in groups]

    await redis_client.setex(cache_key, 1800, json.dumps(result))

    return result


@router.get("/{group_name}/free-slots/")
async def get_group_free_slots(
    group_name: str,
    nominator: str | None = Query(None, description="Nominator (numerator/denominator)"),
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
):
    """Get free slots for a specific group"""
    from services.days import fetch_group_free_slots
    
    # Generate cache key for free slots
    cache_key = f"group_free_slots:{group_name}:{nominator or 'all'}"
    
    # Try to get from cache
    try:
        async def get_cached_data(redis_client):
            return await redis_client.get(cache_key)
        
        cached_data = await safe_redis_operation(get_cached_data)
        if cached_data:
            logger.info(f"Retrieved free slots from cache for group: {group_name}")
            return json.loads(cached_data)
    except Exception as e:
        logger.warning(f"Failed to retrieve from cache, falling back to database: {e}")
    
    # Fetch from database
    try:
        free_slots = fetch_group_free_slots(db, group_name, nominator)
        
        # Cache the result
        try:
            async def cache_data(redis_client):
                await redis_client.setex(cache_key, 300, json.dumps(free_slots))
                return True
            
            await safe_redis_operation(cache_data)
            logger.info(f"Cached free slots for group: {group_name}")
        except Exception as e:
            logger.warning(f"Failed to cache free slots data: {e}")
        
        return free_slots
    except Exception as e:
        logger.error(f"Error fetching free slots for group: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching free slots: {str(e)}")


@router.delete("/cache/clear")
async def clear_groups_cache(redis_client: redis.Redis = Depends(get_redis)):
    keys = await redis_client.keys("groups_suggestions:*")
    all_groups_key = await redis_client.keys("groups_all_groups")
    keys.extend(all_groups_key)
    if keys:
        await redis_client.delete(*keys)
    return {"message": f"Cleared {len(keys)} cache entries"}

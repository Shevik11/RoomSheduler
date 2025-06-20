from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.models import Days
from services.days import fetch_days_by_filters
from dependencies.database import get_db
from dependencies.redis import get_redis
from fastapi.responses import JSONResponse
import redis.asyncio as redis
import json
import hashlib

router = APIRouter()

def generate_cache_key(**kwargs):
    """Генерує ключ для кешу на основі параметрів запиту"""
    # Створюємо рядок з параметрів для хешування
    params_str = "&".join([f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None])
    return f"days_cache:{hashlib.md5(params_str.encode()).hexdigest()}"

@router.get("/days/")
async def get_days(
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
        redis_client: redis.Redis = Depends(get_redis),
):
    # Генеруємо ключ кешу
    cache_key = generate_cache_key(
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
    
    # Спробуємо отримати дані з кешу
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Якщо в кеші немає, отримуємо з БД
    result = fetch_days_by_filters(
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
    
    # Зберігаємо в кеш на 5 хвилин
    await redis_client.setex(cache_key, 300, json.dumps(result))
    
    return result

@router.delete("/days/cache/clear")
async def clear_days_cache(redis_client: redis.Redis = Depends(get_redis)):
    """Очищення кешу для days"""
    # Видаляємо всі ключі, що починаються з "days_cache:"
    keys = await redis_client.keys("days_cache:*")
    if keys:
        await redis_client.delete(*keys)
    return {"message": f"Cleared {len(keys)} cache entries"}




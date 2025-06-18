from fastapi import APIRouter, Query, Depends
from services.week_type_service import week_type_service
from dependencies.redis import get_redis
import redis.asyncio as redis
import json
import hashlib

router = APIRouter()

def generate_week_type_cache_key(**kwargs):
    """Генерує ключ для кешу на основі параметрів запиту"""
    params_str = "&".join([f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None])
    return f"week_type:{hashlib.md5(params_str.encode()).hexdigest()}"

#Отримати поточний тип тижня (чисельник/знаменник)
@router.get("/week-type")
async def get_current_week_type(redis_client: redis.Redis = Depends(get_redis)):
    cache_key = "week_type_current"
    
    # Спробуємо отримати дані з кешу
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    result = week_type_service.get_current_week_type()
    
    # Зберігаємо в кеш на 1 годину (довший TTL для поточного типу тижня)
    await redis_client.setex(cache_key, 3600, json.dumps(result))
    
    return result

@router.get("/week-type/range")
async def get_week_type_for_range(
    start_date: str = Query(..., description="Початкова дата у форматі YYYY-MM-DD"),
    end_date: str = Query(..., description="Кінцева дата у форматі YYYY-MM-DD"),
    redis_client: redis.Redis = Depends(get_redis)
):
    cache_key = generate_week_type_cache_key(start_date=start_date, end_date=end_date)
    
    # Спробуємо отримати дані з кешу
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    result = week_type_service.get_week_type_for_date_range(start_date, end_date)
    
    # Зберігаємо в кеш на 30 хвилин
    await redis_client.setex(cache_key, 1800, json.dumps(result))
    
    return result

@router.delete("/cache/clear")
async def clear_week_type_cache(redis_client: redis.Redis = Depends(get_redis)):
    """Очищення кешу для week_type"""
    keys = await redis_client.keys("week_type:*")
    if keys:
        await redis_client.delete(*keys)
    return {"message": f"Cleared {len(keys)} cache entries"} 
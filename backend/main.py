import redis.asyncio as redis
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dependencies.redis import get_redis_dependency, health_check
from routers import days, groups, lessons, rooms, teachers, week_type

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутера
app.include_router(days.router)
app.include_router(rooms.router)
app.include_router(lessons.router)
app.include_router(groups.router)
app.include_router(teachers.router)
app.include_router(week_type.router)


@app.get("/health/redis")
async def redis_health_check():
    """Перевірка стану Redis підключення"""
    is_healthy = await health_check()
    return {"redis": "healthy" if is_healthy else "unhealthy"}


@app.get("/test-redis")
async def test_redis(redis_client: redis.Redis = Depends(get_redis_dependency)):
    """Тестовий endpoint для перевірки роботи Redis"""
    await redis_client.set("test_key", "test_value")
    value = await redis_client.get("test_key")
    return {"message": "Redis is working!", "test_value": value}


@app.delete("/cache/clear-all")
async def clear_all_caches(redis_client: redis.Redis = Depends(get_redis_dependency)):
    """Очищення всього кешу"""
    # Патерни ключів для всіх роутерів
    cache_patterns = [
        "days_cache:*",
        "lessons_suggestions:*",
        "lessons_all_subjects",
        "rooms_suggestions:*",
        "rooms_busy:*",
        "room_schedule:*",
        "rooms_all_rooms",
        "groups_suggestions:*",
        "groups_all_groups",
        "teachers_suggestions:*",
        "teachers_all_teachers",
        "week_type:*",
    ]

    all_keys = []
    for pattern in cache_patterns:
        keys = await redis_client.keys(pattern)
        all_keys.extend(keys)

    if all_keys:
        await redis_client.delete(*all_keys)

    return {
        "message": "Cleared all caches",
        "cleared_entries": len(all_keys),
        "patterns": cache_patterns,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

import redis.asyncio as redis
from functools import lru_cache
import os
from dotenv import load_dotenv
from fastapi import Depends

load_dotenv()

# Конфігурація Redis з змінних середовища
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_USERNAME = os.getenv('REDIS_USERNAME')

@lru_cache()
def get_redis():
    """Синхронна функція для отримання Redis клієнта (для dependency injection)"""
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        username=REDIS_USERNAME,
        password=REDIS_PASSWORD,
        decode_responses=True
    )

async def get_redis_async():
    """Асинхронна функція для отримання Redis клієнта"""
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        username=REDIS_USERNAME,
        password=REDIS_PASSWORD,
        decode_responses=True
    )

async def get_redis_dependency():
    """Dependency injection функція для FastAPI"""
    redis_client = get_redis()
    try:
        yield redis_client
    finally:
        await redis_client.close()

async def health_check():
    """Перевірка стану Redis підключення"""
    try:
        redis_client = get_redis()
        await redis_client.ping()
        return True
    except Exception:
        return False 
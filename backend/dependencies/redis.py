import redis.asyncio as redis
from functools import lru_cache
import os
import logging
from dotenv import load_dotenv
from fastapi import Depends

logger = logging.getLogger(__name__)

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_USERNAME = os.getenv('REDIS_USERNAME')

REDIS_DISABLED = os.getenv('REDIS_DISABLED', 'false').lower() == 'true'

# Redis connection settings
REDIS_SETTINGS = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'username': REDIS_USERNAME,
    'password': REDIS_PASSWORD,
    'decode_responses': True,
    'socket_connect_timeout': 5,  
    'socket_timeout': 5,          
    'retry_on_timeout': True,
    'health_check_interval': 30   
}

@lru_cache()
def get_redis():
    try:
        return redis.Redis(**REDIS_SETTINGS)
    except Exception as e:
        logger.error(f"Failed to create Redis client: {e}")
        raise

async def get_redis_async():
    try:
        client = redis.Redis(**REDIS_SETTINGS)
        # Verify the connection is working with a ping
        await client.ping()
        return client
    except Exception as e:
        logger.error(f"Failed to create async Redis client: {e}")
        raise

async def get_redis_dependency():
    redis_client = None
    try:
        redis_client = await get_redis_async()
        yield redis_client
    except Exception as e:
        logger.error(f"Redis dependency failed: {e}")
        raise
    finally:
        if redis_client:
            await redis_client.close()

async def health_check():
    try:
        redis_client = await get_redis_async()
        await redis_client.ping()
        await redis_client.close()
        return True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False

async def safe_redis_operation(operation, fallback_value=None):
    try:
        redis_client = await get_redis_async()
        result = await operation(redis_client)
        await redis_client.close()
        return result
    except Exception as e:
        logger.error(f"Redis operation failed: {e}")
        return fallback_value  

def is_redis_available():
    return not REDIS_DISABLED 
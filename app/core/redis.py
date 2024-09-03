from typing import AsyncGenerator
import redis.asyncio as redis

from app.core.settings import settings


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
    try:
        yield client
    finally:
        await client.aclose()

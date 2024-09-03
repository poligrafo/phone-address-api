import pytest
import redis.asyncio as redis
from app.core.settings import settings

@pytest.fixture
async def redis_client() -> redis.Redis:
    client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
    yield client
    await client.aclose()

import pytest
from httpx import AsyncClient, ASGITransport
import redis.asyncio as redis
from app.main import app


@pytest.mark.asyncio
async def test_write_data(redis_client: redis.Redis) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/write_data", json={"phone": "89090000000", "address": "Test Address"})
        assert response.status_code == 200
        assert response.json() == {"message": "Data saved successfully"}

        stored_value = await redis_client.get("89090000000")
        assert stored_value.decode("utf-8") == "Test Address"


@pytest.mark.asyncio
async def test_check_data(redis_client: redis.Redis) -> None:
    # We pre-record the data in Redis
    await redis_client.set("89090000000", "Test Address")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/check_data", params={"phone": "89090000000"})
        assert response.status_code == 200
        assert response.json() == {"phone": "89090000000", "address": "Test Address"}

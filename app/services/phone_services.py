import logging
from typing import Optional

from fastapi import HTTPException
import redis.asyncio as redis

from app.models.phone_address_schemas import PhoneAddress

logger = logging.getLogger("app")


class PhoneService:
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis = redis_client

    async def write_data(self, data: PhoneAddress) -> None:
        await self.redis.set(data.phone, data.address)
        logger.debug(f"Data written for phone: {data.phone}")

    async def get_data(self, phone: str) -> Optional[str]:
        address = await self.redis.get(phone)
        if not address:
            logger.warning(f"Address not found for phone: {phone}")
            raise HTTPException(status_code=404, detail="Address not found")
        logger.debug(f"Data retrieved for phone: {phone}")
        return address.decode('utf-8')
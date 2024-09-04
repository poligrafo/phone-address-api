import logging
import redis.asyncio as redis

from app.schemas.phone_address_schemas import PhoneAddress

logger = logging.getLogger("app")


class PhoneService:
    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        self.redis = redis_client
        self.ttl = ttl

    async def write_data(self, data: PhoneAddress):
        try:
            await self.redis.set(data.phone, data.address, ex=self.ttl)
            logger.debug(f"Data written for phone: {data.phone}")
        except Exception as e:
            logger.error(f"Error writing data for phone {data.phone}: {str(e)}")
            raise

    async def get_data(self, phone: str) -> str:
        try:
            address = await self.redis.get(phone)
            if not address:
                logger.warning(f"Phone number {phone} not found in the database.")
                raise ValueError(f"Phone number {phone} not found in the database.")
            logger.debug(f"Data retrieved for phone: {phone}")
            return address.decode("utf-8")
        except Exception as e:
            logger.error(f"Error retrieving data for phone {phone}: {str(e)}")
            raise
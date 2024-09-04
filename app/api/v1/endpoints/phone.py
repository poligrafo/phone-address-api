from fastapi import APIRouter, Depends, Query, HTTPException
import redis.asyncio as redis

from app.core.redis import get_redis
from app.schemas.phone_address_schemas import PhoneAddress
from app.services.phone_services import PhoneService

router = APIRouter()


@router.post("/write_data", tags=["Data Management"], summary="Record or update data")
async def write_data(
    data: PhoneAddress,
    redis_client: redis.Redis = Depends(get_redis)
) -> dict[str, str]:
    service = PhoneService(redis_client)
    await service.write_data(data)
    return {"message": "Data saved successfully"}


@router.get("/check_data", tags=["Data Retrieval"], summary="Get data by phone number")
async def check_data(
    phone: str = Query(..., description="Phone number for address search"),
    redis_client: redis.Redis = Depends(get_redis)
) -> dict[str, str]:
    service = PhoneService(redis_client)
    try:
        address = await service.get_data(phone)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"phone": phone, "address": address}

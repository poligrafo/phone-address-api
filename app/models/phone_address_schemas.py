from pydantic import BaseModel, Field


class PhoneAddress(BaseModel):
    phone: str = Field(..., description="The user's phone number")
    address: str = Field(..., description="User's address")

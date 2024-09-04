from pydantic import BaseModel, Field, constr


class PhoneAddress(BaseModel):
    phone: constr(pattern=r'^\d{10,15}$') = Field(..., description="The user's phone number")
    address: str = Field(..., description="User's address")

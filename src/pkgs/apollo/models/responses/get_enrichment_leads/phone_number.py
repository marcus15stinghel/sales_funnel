from pydantic import BaseModel, Field


class PhoneNumber(BaseModel):
    number: str = Field(default=None, alias='raw_number')

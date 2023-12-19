from pydantic import BaseModel, Field
from typing import List
from .phone_number import PhoneNumber


class Contact(BaseModel):
    id: str = Field(default=None, alias='id')
    first_name: str = Field(default=None, alias='first_name')
    last_name: str = Field(default=None, alias='last_name')
    phone_numbers: List[PhoneNumber] = Field(default=None, alias='phone_numbers')
    job_title: str = Field(default=None, alias='title')
    email: str = Field(default=None, alias='email')
    linkedin_url: str = Field(default=None, alias='linkedin_url')

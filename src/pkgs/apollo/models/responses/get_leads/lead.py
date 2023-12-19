from pydantic import BaseModel, Field
from typing import List
from .contact import Contact


class Lead(BaseModel):
    data_contact: List[Contact] = Field(default=None, alias='recipients')
    num_clicks: int = Field(default=None)

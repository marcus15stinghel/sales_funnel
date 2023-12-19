from pydantic import BaseModel, Field
from typing import List
from .lead import Lead


class DataLeads(BaseModel):
    leads: List[Lead] = Field(default=None, alias='emailer_messages')


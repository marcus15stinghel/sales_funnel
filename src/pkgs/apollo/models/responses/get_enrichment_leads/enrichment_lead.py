from pydantic import BaseModel, Field
from typing import Dict
from .data import Data


class EnrichmentLead(BaseModel):
    data: Data = Field(default=None, alias='person')

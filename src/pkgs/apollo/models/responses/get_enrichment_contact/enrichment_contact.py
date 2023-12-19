from pydantic import BaseModel, Field
from .data import Data


class EnrichmentContact(BaseModel):
    data: Data = Field(default=None, alias='person')

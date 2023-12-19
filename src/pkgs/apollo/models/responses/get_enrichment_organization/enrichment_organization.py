from pydantic import BaseModel, Field
from .data import Data


class EnrichmentOrganization(BaseModel):
    data: Data = Field(default=None, alias='organization')

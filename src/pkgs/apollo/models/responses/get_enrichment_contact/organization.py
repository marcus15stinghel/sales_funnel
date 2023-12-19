from pydantic import BaseModel, Field


class Organization(BaseModel):
    web_domain: str = Field(default=None, alias='primary_domain')
    name: str = Field(default=None, alias='name')

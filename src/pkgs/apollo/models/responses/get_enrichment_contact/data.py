from pydantic import BaseModel, Field
from .organization import Organization


class Data(BaseModel):
    organization: Organization = Field(default=None, alias='organization')
    first_name: str = Field(default=None, alias='first_name')
    last_name: str = Field(default=None, alias='last_name')
    email: str = Field(default=None, alias='email')
    linkedin_url: str = Field(default=None, alias='linkedin_url')
    job_title: str = Field(default=None, alias='title')
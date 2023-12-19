from pydantic import BaseModel, Field


class Organization(BaseModel):
    name: str = Field(default=None, alias='name')
    industry: str = Field(default=None, alias='industry')
    employees_number: int = Field(default=None, alias='estimated_num_employees')
    website_url: str = Field(default=None, alias='website_url')
    linkedin_url: str = Field(default=None, alias='linkedin_url')

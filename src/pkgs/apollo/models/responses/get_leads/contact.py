from pydantic import BaseModel, Field


class Contact(BaseModel):
    email: str = Field(default=None, alias="email")
    name: str = Field(default=None, alias="raw_name")
    recipient_type_cd: str = Field(default=None, alias="recipient_type_cd")
    id: str = Field(default=None, alias="contact_id")

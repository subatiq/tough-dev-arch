from __future__ import annotations
from uuid import UUID, uuid4
from pydantic import BaseModel
from pydantic.fields import Field


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    pub_id: UUID
    email: str
    username: str




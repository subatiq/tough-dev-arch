from __future__ import annotations
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel
from pydantic.fields import Field


class UserRole(Enum):
    DEVELOPER = "dev"
    MANAGER = "manager"
    ADMIN = "admin"


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    pub_id: UUID = Field(default_factory=uuid4)
    email: str
    username: str
    role: UserRole


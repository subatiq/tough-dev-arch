from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field


class UserRole(Enum):
    DEVELOPER = "dev"
    MANAGER = "manager"
    ADMIN = "admin"


class User(BaseModel):
    pub_id: UUID = Field(default_factory=uuid4)
    email: str
    username: str
    role: UserRole


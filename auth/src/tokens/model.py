import uuid
from enum import Enum
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class ClientToken(BaseModel):
    access_token: str = Field(default_factory=lambda: str(uuid.uuid4()))
    refresh_token: str = Field(default_factory=lambda: str(uuid.uuid4()))


class Token(ClientToken):
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=10))


class TokenState(Enum):
    OK = 0,
    OUTDATED = 1,
    INVALID = 2


